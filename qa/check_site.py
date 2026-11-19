"""Check generated links, learning interactions, persistence, and responsive layouts."""
import argparse,json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag in ('a','link') and a.get('href'):self.links.append(a['href'])
        if tag in ('audio','script') and a.get('src'):self.links.append(a['src'])

def check_links():
    output=ROOT/'dist';docs={path:Document(path.read_text()) for path in output.rglob('*.html')};count=0
    for path,doc in docs.items():
        assert len(doc.ids)==len(set(doc.ids)),str(path)+' duplicate ids'
        for link in doc.links:
            url=urlsplit(link)
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            assert target.is_relative_to(output),link
            assert target.exists(),str(path)+': missing '+link
            if url.fragment and target.suffix=='.html':assert unquote(url.fragment) in docs[target].ids,str(path)+': missing fragment '+link
            count+=1
    return count

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:8877');parser.add_argument('--skip-links',action='store_true');args=parser.parse_args()
    course=json.loads((ROOT/'course.json').read_text());base=args.base_url.rstrip('/')
    report={'internal_links':check_links() if not args.skip_links else 'deferred','pages':0,'feedback_choices':0,'recall_reveals':0,'labs':0,'widths':[1440,1024,768,620,390,320]}
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        page=browser.new_page(viewport={'width':1440,'height':1000});errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        for c in course['chapters']:
            page.goto(base+'/chapters/'+c['slug']+'.html',wait_until='networkidle')
            for i,lesson in enumerate(c['pages']):
                page.locator(f'[data-page-link="{i}"]').click()
                active=page.locator(f'#p{i+1}');active.wait_for(state='visible')
                assert page.locator('.lesson-page:visible').count()==1
                expected_title = 'The situation' if lesson['type'] == 'story' else lesson['title']
                assert expected_title==active.locator('.lesson-copy h2').inner_text()
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                report['pages']+=1
                if lesson['type']=='decision':
                    assert active.locator('.feedback:visible').count()==0
                    for option in range(3):
                        active.locator(f'input[value="{option}"]').check()
                        active.get_by_role('button',name='Check choice').click()
                        assert active.locator('.feedback:visible').count()==1
                        assert active.locator('.feedback:visible p').inner_text()==lesson['options'][option]['feedback']
                        report['feedback_choices']+=1
                if lesson['type']=='recall':
                    for details in active.locator('.recall-question details').all():
                        details.locator('summary').click();assert details.get_attribute('open') is not None
                    active.get_by_role('button',name='Mark practice as tried').click();report['recall_reveals']+=2
                if lesson['type']=='lab':
                    assert active.locator('textarea').count()==5
                    active.locator('textarea').first.fill('A fictional response kept in this tab.')
                    active.get_by_role('button',name='Mark practice as tried').click();report['labs']+=1
            page.locator('.chapter-options > summary').click()
            assert '8 of 8 pages viewed · 4 of 4 practices tried' in page.locator('[data-chapter-progress]').inner_text()
            page.locator('.chapter-options > summary').click()
        # Notes survive page navigation within the document but never enter local storage.
        page.locator('[data-page-link="0"]').click();page.locator('[data-page-link="7"]').click()
        assert page.locator('#p8 textarea').first.input_value()=='A fictional response kept in this tab.'
        assert 'fictional response' not in page.evaluate('JSON.stringify(localStorage)')
        with page.expect_download() as pending:page.get_by_role('button',name='Download my responses').click()
        download=pending.value
        assert 'fictional response' in Path(download.path()).read_text()
        page.reload(wait_until='networkidle')
        assert page.locator('#p8 textarea').first.input_value()==''
        page.goto(base,wait_until='networkidle')
        assert page.locator('#resume-learning').is_visible()
        assert '8 of 8 pages viewed' in page.locator('[data-progress="continuing"]').inner_text()
        # Layout and keyboard checks cover each kind of lesson at small widths.
        for width in report['widths']:
            page.set_viewport_size({'width':width,'height':1000})
            for url in ('/', '/chapters/one-event.html#p1','/chapters/one-event.html#p2','/chapters/one-event.html#p3','/chapters/one-event.html#p7','/chapters/one-event.html#p8','/workbook.html','/case-final.html'):
                page.goto(base+url,wait_until='networkidle')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(width,url)
            page.goto(base+'/chapters/one-event.html',wait_until='networkidle')
            page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(el)=>el===document.activeElement')
            page.keyboard.press('Enter');assert page.locator('#p1').evaluate('(el)=>el===document.activeElement')
            page.keyboard.press('ArrowRight');assert page.evaluate('location.hash')=='#p2'
        page.goto(base+'/chapters/one-event.html#p7')
        page.locator('.skip').press('Enter')
        assert page.evaluate('location.hash')=='#p7'
        assert page.locator('#p7').evaluate('(el)=>el===document.activeElement')
        # Playback must advance and stop when changing page.
        page.goto(base+'/chapters/one-event.html',wait_until='networkidle')
        audio=page.locator('#p1 audio');audio.evaluate('(a)=>a.play()')
        page.wait_for_function('document.querySelector("#p1 audio").currentTime > .15')
        page.locator('.lesson-page:visible').get_by_role('button',name='Next page').click()
        page.locator('#p2').wait_for()
        assert audio.evaluate('(a)=>a.paused')
        page.locator('#p2 .audio-rate').select_option('1.25')
        assert page.locator('#p2 audio').evaluate('(a)=>a.playbackRate')==1.25
        # Form fields keep arrow keys for editing rather than changing pages.
        page.locator('[data-page-link="7"]').click();page.locator('#p8 textarea').first.focus();page.keyboard.press('ArrowLeft')
        assert page.evaluate('location.hash')=='#p8'
        # Empty/corrupt/unavailable local storage must not prevent learning.
        blocked=browser.new_context()
        blocked.add_init_script('Storage.prototype.getItem=function(){throw new Error("blocked")};Storage.prototype.setItem=function(){throw new Error("blocked")};')
        other=blocked.new_page();other.goto(base+'/chapters/one-event.html',wait_until='networkidle')
        assert other.locator('.lesson-page:visible').count()==1
        other.locator('.chapter-options > summary').click()
        assert 'won’t be saved' in other.locator('[data-progress-status]').inner_text();blocked.close()
        nojs=browser.new_context(java_script_enabled=False)
        other=nojs.new_page();other.goto(base+'/chapters/one-event.html')
        assert other.locator('.lesson-page:visible').count()==8
        other.goto(base+'/reading.html');assert other.locator('.reading-options li').count()==72
        nojs.close();assert not errors,errors
        report.update({'console_errors':errors,'progress':'pass','writing_privacy':'pass','response_export':'pass','audio_playback':'pass','no_javascript':'pass','storage_unavailable':'pass'})
        browser.close()
    print(json.dumps(report,indent=2))
