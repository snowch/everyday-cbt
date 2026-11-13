"""Validate and build the complete static Everyday CBT course."""
import argparse
import base64
import hashlib
import json
import re
import shutil
import textwrap
from html import escape as e
from pathlib import Path
from string import Template
from scripts.narration_text import spoken

ROOT=Path(__file__).resolve().parent
STAGES={'story':'The situation','decision':'Make a decision','concept':'Understand the pattern','example':'Worked example','recall':'Recall practice','lab':'Practical lab'}

def paragraphs(items):
    return ''.join(f'<p>{e(x)}</p>' for x in items)

def field(prompt,key):
    return f'<div class="writing-field"><label for="{key}">{e(prompt)}</label><textarea id="{key}" data-prompt="{e(prompt)}" rows="3" spellcheck="true"></textarea></div>'

def visual(d,key):
    items=d['items'];kind=d['kind'];boxes=[];paths=[]
    if kind=='map':
        positions=[(174,12),(12,176),(336,176),(12,340),(336,340)]
        for i,(x,y) in enumerate(positions):
            for x2,y2 in positions[i+1:]:paths.append(f'<path d="M{x+126} {y+60}L{x2+126} {y2+60}"/>')
    elif kind in ('loop','columns'):
        positions=[(12,24),(336,24),(336,324),(12,324)]
        if kind=='loop':paths=[f'<path d="M264 84H328"/>',f'<path d="M462 144V316"/>',f'<path d="M336 384H272"/>',f'<path d="M138 324V152"/>']
    else:
        positions=[(56+(i*10 if kind=='ladder' else 0),16+i*130) for i in range(len(items))]
        paths=[f'<path d="M300 {131+i*130}v10"/>' for i in range(len(items)-1)]
    for i,(item,(x,y)) in enumerate(zip(items,positions)):
        width=252 if kind in ('map','loop','columns') else 488-i*10 if kind=='ladder' else 488
        lines=textwrap.wrap(item['detail'],width=26 if width==252 else 43)
        detail=''.join(f'<tspan x="{x+width/2}" dy="23">{e(line)}</tspan>' for line in lines)
        boxes.append(f'<g><rect x="{x}" y="{y}" width="{width}" height="114" rx="12" fill="#F2F6F9" stroke="#A9C4D3"/><rect x="{x}" y="{y}" width="5" height="114" rx="2" fill="{["#216B88","#7058A3","#A1486D","#B27B27","#216B88"][i]}"/><text x="{x+width/2}" y="{y+34}" font-size="18" font-weight="700">{e(item["label"])}</text><text x="{x+width/2}" y="{y+43}" font-size="19">{detail}</text></g>')
    desc='; '.join(x['label']+': '+x['detail'] for x in items)
    height=480 if kind in ('map','loop','columns') else len(items)*130+12
    connections=f' marker-start="url(#{key}-arrow)"' if kind=='map' else ''
    return f'<figure class="concept-figure"><svg viewBox="0 0 600 {height}" role="img" aria-labelledby="{key}-title {key}-desc"><title id="{key}-title">{e(d["title"])}</title><desc id="{key}-desc">{e(desc)}</desc><defs><marker id="{key}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 10 5 0 10Z" fill="#7C9FB3"/></marker></defs><g fill="none" stroke="#7C9FB3" stroke-width="2" marker-end="url(#{key}-arrow)"{connections}>{"".join(paths)}</g><g text-anchor="middle" fill="#19394D" font-family="CourseSans,Arial,sans-serif">{"".join(boxes)}</g></svg><figcaption>{e(d["title"])}</figcaption><details class="diagram-key"><summary>Read diagram as text</summary><dl>{''.join(f'<dt>{e(x["label"])}</dt><dd>{e(x["detail"])}</dd>' for x in items)}</dl></details></figure>'

def scene(chapter,key):
    names=['Alex','Nia','Jules'];colours=['#7058A3','#216B88','#A1486D'];people=[]
    for i,(name,colour) in enumerate(zip(names,colours)):
        x=138+i*155
        people.append(f'<g><path d="M{x-40} 355v-78q0-37 40-37t40 37v78" fill="{colour}" stroke="#19394D" stroke-width="3"/><circle cx="{x}" cy="210" r="27" fill="{["#E6AE86","#B77C58","#EBC19D"][i]}" stroke="#19394D" stroke-width="3"/><path d="M{x-26} 208q-7-42 30-32 28 3 22 35l-14-22-16 9-13-7Z" fill="#19394D"/><circle cx="{x-8}" cy="212" r="2" fill="#19394D"/><circle cx="{x+8}" cy="212" r="2" fill="#19394D"/><path d="M{x-6} 225q6 5 12 0" fill="none" stroke="#19394D" stroke-width="2"/><path d="M{x-16} 355l-8 57m40-57 8 57" stroke="#19394D" stroke-width="10" stroke-linecap="round"/><text x="{x}" y="452" text-anchor="middle" fill="#19394D" font-family="CourseSans,Arial,sans-serif" font-size="18">{name}</text></g>')
    labels=['A cancelled session','Check the signup list','One wrong date','An unanswered message','Make room for drawing','Three tasks, two evenings','Ask one clear question','An ordinary greeting','The conversation replays','A realistic commitment','A fairer rota','A difficult week']
    return f'<figure class="story-figure"><svg viewBox="0 0 600 490" role="img" aria-labelledby="{key}-scene-title {key}-scene-desc"><title id="{key}-scene-title">{e(labels[chapter-1])}</title><desc id="{key}-scene-desc">Alex, Nia, and Jules at their community drawing group. The case concerns {e(labels[chapter-1].lower())}.</desc><path d="M32 425V230a268 210 0 0 1 536 0v195Z" fill="#D8E6EE"/><path d="M55 425V230a245 188 0 0 1 490 0v195Z" fill="#F2F6F9" stroke="#A9C4D3" stroke-width="2"/><rect x="132" y="74" width="336" height="54" rx="7" fill="#19394D"/><text x="300" y="108" text-anchor="middle" fill="white" font-family="CourseSans,Arial,sans-serif" font-size="20">{e(labels[chapter-1])}</text>{"".join(people)}<path d="M65 335h470l24 31H41Z" fill="#D8AC5C" stroke="#19394D" stroke-width="3"/><path d="M78 366v63m444-63v63" stroke="#19394D" stroke-width="10" stroke-linecap="round"/><rect x="240" y="293" width="105" height="44" rx="3" fill="#FFF" stroke="#19394D" stroke-width="2"/><path d="M253 305h63m-63 9h76m-76 9h46" stroke="#A9C4D3" stroke-width="3"/><path d="M370 326l44-40" stroke="#7058A3" stroke-width="7" stroke-linecap="round"/></svg><figcaption>Fictional stories. Different people, different meanings.</figcaption></figure>'

def practice(page,reading=False):
    key=page['id'];out=''
    if page['type']=='decision':
        if reading:
            out='<ol class="reading-options">'+''.join(f'<li><strong>{e(o["text"])}</strong><p>{e(o["feedback"])}</p></li>' for o in page['options'])+'</ol>'
        else:
            options=''.join(f'<label class="option"><input type="radio" name="{key}" value="{i}" required><span><span class="option-letter">{"ABC"[i]}.</span> {e(o["text"])}</span></label>' for i,o in enumerate(page['options']))
            feedback=''.join(f'<div class="feedback" data-feedback="{i}" hidden><strong>{"Strongest fit in this situation" if i==page["best"] else "Consider the reasoning"}</strong><p>{e(o["feedback"])}</p></div>' for i,o in enumerate(page['options']))
            out=f'<form class="decision-form" data-practice="{key}"><fieldset><legend class="sr-only">Choose a response for {e(page["title"])}</legend>{options}</fieldset><button class="button primary" type="submit">Check my reasoning</button><div class="feedback-region" aria-live="polite" aria-atomic="true">{feedback}</div></form>'
    if page['type']=='recall':
        for i,q in enumerate(page['questions']):
            out+=f'<section class="recall-question"><h3>{e(q["prompt"])}</h3>'
            if not reading:out+=field('Your reasoning',f'{key}-r{i}')
            out+=f'<details {"open" if reading else ""}><summary>Compare suggested reasoning</summary><p>{e(q["answer"])}</p></details></section>'
        if not reading:out+=f'<button class="button primary" data-tried="{key}">I’ve tried this recall</button>'
    if page['type']=='lab':
        for i,prompt in enumerate(page['fields']):out+=field(prompt,f'{key}-l{i}')
        out+=f'<details {"open" if reading else ""}><summary>Compare a worked lab response</summary><p>{e(page["example"])}</p></details><p class="review-note">{e(page["review"])}</p>'
        if not reading:out+=f'<button class="button primary" data-tried="{key}">I’ve tried this lab</button>'
    return out

def evidence(c):
    links=''.join(f'<li><a href="{e(s["url"])}">{e(s["title"])}</a></li>' for s in c['sources'])
    return f'<details class="evidence"><summary>Evidence, further reading, and limits</summary><p>{e(c["evidence_note"])}</p><ul>{links}</ul><p class="small">Sources checked {COURSE["reviewed"]}. These resources support further study; their publishers have not reviewed or endorsed this course. Stories, diagrams, and examples are original.</p></details>'

def document(title,body,prefix='./',extra='',bodyclass='document-page'):
    return Template((ROOT/'site/document.html').read_text()).substitute(title=e(title),body=body,prefix=prefix,extra=extra,bodyclass=bodyclass,version=e(COURSE['version']))

def render_chapter(c,n,output):
    pages=[]
    for i,p in enumerate(c['pages']):
        key=p['id'];art=visual(p['diagram'],key) if p.get('diagram') else scene(n,key) if p['type'] in ('story','example') else ''
        body=f'<div class="lesson-copy"><p class="lesson-stage">{STAGES[p["type"]]}</p><h2>{e(p["title"])}</h2>{paragraphs(p["paragraphs"])}{practice(p)}</div>'
        clip=ROOT/'audio/clips'/f'{key}.m4a'
        audio=f'<audio controls preload="none" src="../audio/clips/{key}.m4a" aria-label="Narration for {e(p["title"])}"></audio>' if clip.exists() else '<p>Recording is being prepared.</p>'
        transcript=f'<details class="recording-transcript"><summary>Recording transcript</summary><p>{e(spoken(p))}</p></details>'
        pages.append(f'<section class="lesson-page" id="p{i+1}" data-page="{i}" data-id="{key}" data-type="{p["type"]}" tabindex="-1"><div class="lesson {"has-art" if art else ""}">{body}{f"<div class=lesson-art>{art}</div>" if art else ""}</div><div class="narration">{audio}<label>Playback speed <select class="audio-rate" aria-label="Playback speed for page {i+1}"><option value="0.8">0.8×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label></div>{transcript}<nav class="lesson-bottom-controls" aria-label="Page controls"><button class="button" data-step="-1" {"disabled" if i==0 else ""}>Previous page</button><button class="button primary" data-step="1" {"disabled" if i==7 else ""}>Next page</button></nav></section>')
    nav=''.join(f'<a href="#p{i+1}" data-page-link="{i}" aria-label="Page {i+1}: {e(p["title"])}">{i+1}</a>' for i,p in enumerate(c['pages']))
    previous=f'<a href="./{COURSE["chapters"][n-2]["slug"]}.html">Previous chapter</a>' if n>1 else '<a href="../index.html">Course home</a>'
    nextlink=f'<a href="./{COURSE["chapters"][n]["slug"]}.html">Next chapter</a>' if n<12 else '<a href="../case-final.html">Try the final case</a>'
    checkpoint=next((x for x in COURSE['cases'] if x['after']==n),None)
    checkpoint_link=f'<aside class="checkpoint"><h2>Put the skills together.</h2><p>Try an unfamiliar case before moving on.</p><a class="button" href="../{checkpoint["id"]}.html">{e(checkpoint["title"])}</a></aside>' if checkpoint else ''
    body=f'<main id="main" class="player wrap" data-chapter="{e(c["slug"])}" data-page-count="8"><div class="player-heading"><div><p class="eyebrow">Chapter {n:02d} of 12 · {e(c["minutes"])}</p><h1>{e(c["title"])}</h1></div><a href="../workbook.html#lab-{n}">Open workbook</a></div><p class="draft-label">Draft course · practitioner review and learner pilot pending</p><nav class="lesson-nav" aria-label="Lesson pages">{nav}</nav><div class="player-controls"><button class="button" id="previous-page" type="button">Previous</button><span id="page-status" role="status">8 lesson pages</span><button class="button primary" id="next-page" type="button">Next</button></div><noscript><p class="notice">All pages appear below. For questions with their feedback, use the <a href="../reading.html#chapter-{n}">reading edition</a>.</p></noscript>{"".join(pages)}<p class="progress-caption" data-chapter-progress></p><div class="response-tools"><button class="button" data-export>Download my responses</button><button class="button" data-print>Print this chapter</button><p>Your writing stays in this tab and is not saved. Export it before leaving this chapter. Progress records page IDs and practice attempts on this device; it does not store your writing.</p></div>{evidence(c)}{checkpoint_link}<nav class="chapter-navigation" aria-label="Between chapters">{previous}{nextlink}</nav></main>'
    (output/'chapters'/f'{c["slug"]}.html').write_text(document(c['title'],body,'../',bodyclass='chapter-page'))

def render_case(case):
    body=f'<main id="main" class="wrap document" data-case="{case["id"]}"><p class="eyebrow">Independent practice · suggested 20–30 minutes</p><h1>{e(case["title"])}</h1><p>Write your reasoning before comparing the suggestions. More than one approach may fit.</p><section class="case-story"><h2>The situation</h2>{paragraphs(case["story"][:2])}</section>'
    if len(case['story'])>2:body+=f'<details class="new-information"><summary>Reveal new information after your first draft</summary>{paragraphs(case["story"][2:])}</details>'
    for i,(title,prompt,answer) in enumerate(case['tasks'],1):
        body+=f'<section class="case-task"><h2>{i}. {e(title)}</h2><p>{e(prompt)}</p>{field("Your reasoning",case["id"]+"-"+str(i))}<details><summary>Compare suggested reasoning</summary><p>{e(answer)}</p></details></section>'
    body+='<section><h2>Assess your reasoning</h2><p>Use these prompts to identify one strength and one thing to improve. This is formative practice, not certification.</p><ul>'+''.join(f'<li>{e(x)}</li>' for x in case['rubric'])+'</ul></section><div class="response-tools"><button class="button" data-export>Download my responses</button><button class="button" data-print>Print case</button><p>Writing stays in this tab and is not saved. Export before leaving.</p></div><p><a href="./index.html">Return to the course</a></p></main>'
    return document(case['title'],body)

def render_workbook(output):
    body='<main id="main" class="wrap document workbook"><p class="eyebrow">Everyday CBT · practice companion</p><h1>A little understanding.<br>Something to try.</h1><p>Use fictional examples throughout, or choose mild everyday situations you are comfortable considering. Personal writing is optional. This workbook is introductory education, not diagnosis or individual treatment.</p><p class="notice">Writing stays in this tab and is not saved or sent to a server. Download your responses before leaving. For a paper copy, print this page or download the PDF.</p><div class="response-tools"><button class="button" data-export>Download my responses</button><button class="button" data-print>Print workbook</button><a class="button" href="./workbook.pdf">Download workbook PDF</a></div><nav aria-label="Workbook contents"><ol>'+''.join(f'<li><a href="#lab-{n}">{e(c["pages"][-1]["title"])}</a></li>' for n,c in enumerate(COURSE['chapters'],1))+'</ol></nav>'
    for n,c in enumerate(COURSE['chapters'],1):
        lab=c['pages'][-1]
        body+=f'<section class="workbook-lab" id="lab-{n}"><p class="eyebrow">Chapter {n:02d}</p><h2>{e(lab["title"])}</h2>{paragraphs(lab["paragraphs"])}<p><a href="./chapters/{c["slug"]}.html">Read the lesson</a></p>'+practice(lab,reading=True)+'</section>'
    for case in COURSE['cases']:
        body+=f'<section class="workbook-lab"><h2>{e(case["title"])}</h2>{paragraphs(case["story"])}'
        for i,(title,prompt,answer) in enumerate(case['tasks'],1):
            body+=f'<h3>{i}. {e(title)}</h3><p>{e(prompt)}</p>'+field('Your reasoning',f'wb-{case["id"]}-{i}')+f'<details open><summary>Suggested reasoning</summary><p>{e(answer)}</p></details>'
        body+='<h3>Self-assessment</h3><ul>'+''.join(f'<li>{e(x)}</li>' for x in case['rubric'])+'</ul></section>'
    body+='<section><h2>Scope and sources</h2><p>'+e(COURSE['scope'])+'</p><p><a href="./about.html">Course guidance, evidence notes, and sources</a></p></section></main>'
    (output/'workbook.html').write_text(document('Practice workbook',body))
    reading='<main id="main" class="wrap document reading"><p class="eyebrow">Complete reading edition</p><h1>Everyday CBT</h1><p>'+e(COURSE['scope'])+'</p><p>Includes all choices and their feedback, suggested recall answers, and worked lab responses. For recorded narration and interactive decisions, open a chapter from the course home.</p><button class="button" data-print>Print reading edition</button>'
    for n,c in enumerate(COURSE['chapters'],1):
        reading+=f'<section class="reading-chapter" id="chapter-{n}"><p class="eyebrow">Chapter {n:02d}</p><h2>{e(c["title"])}</h2>'
        for p in c['pages']:
            reading+=f'<section class="reading-page"><h3>{e(p["title"])}</h3>{paragraphs(p["paragraphs"])}'+(visual(p['diagram'],'read-'+p['id']) if p.get('diagram') else '')+practice(p,reading=True)+'</section>'
        reading+=evidence(c)+'</section>'
    reading+='</main>'
    (output/'reading.html').write_text(document('Complete reading edition',reading))

def validate(require_audio):
    assert len(COURSE['chapters'])==12
    ids=set();slugs=set();manifest={}
    if (ROOT/'audio/manifest.json').exists():manifest={x['id']:x for x in json.loads((ROOT/'audio/manifest.json').read_text())['clips']}
    for c in COURSE['chapters']:
        assert re.fullmatch('[a-z]+(?:-[a-z]+)*',c['slug']) and c['slug'] not in slugs
        slugs.add(c['slug']);assert len(c['pages'])==8
        assert [p['type'] for p in c['pages']]==['story','decision','concept','concept','example','decision','recall','lab']
        assert c['sources'] and c['evidence_note']
        for p in c['pages']:
            key=p['id'];assert key not in ids;ids.add(key)
            assert p['title'] and all(p['paragraphs'])
            if p['type']=='decision':assert len(p['options'])==3 and 0<=p['best']<3 and all(o['text'] and o['feedback'] for o in p['options'])
            if p['type']=='recall':assert len(p['questions'])==2 and all(q['prompt'] and q['answer'] for q in p['questions'])
            if p['type']=='lab':assert len(p['fields'])==5 and p['example'] and p['review']
            if require_audio:
                record=manifest[key];assert record['text_sha256']==hashlib.sha256(spoken(p).encode()).hexdigest(),key+' stale narration'
                assert hashlib.sha256((ROOT/record['file']).read_bytes()).hexdigest()==record['sha256'],key+' audio hash'
    assert len(COURSE['cases'])==3
    if require_audio:
        assert set(manifest)==ids, 'Unexpected or missing recordings'
        for name in ('workbook.pdf','course.pdf'):
            assert (ROOT/name).read_bytes().startswith(b'%PDF'),name

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--require-audio',action='store_true');args=parser.parse_args()
    COURSE=json.loads((ROOT/'course.json').read_text());validate(args.require_audio)
    output=ROOT/'dist';output.mkdir(exist_ok=True);(output/'chapters').mkdir(exist_ok=True)
    cards=[]
    for n,c in enumerate(COURSE['chapters'],1):
        cards.append(f'<article class="chapter" id="chapter-{c["slug"]}"><span class="chapter-number">{n:02d}</span><div><h3><a class="chapter-link" data-slug="{c["slug"]}" href="./chapters/{c["slug"]}.html">{e(c["title"])}</a></h3><p class="story">{e(c["story"])}</p><p class="chapter-meta">8 pages · 2 decisions · recall · lab</p><p class="chapter-progress" data-progress="{c["slug"]}">Not yet viewed</p></div></article>')
        render_chapter(c,n,output)
    index=Template((ROOT/'site/template.html').read_text()).substitute(title=e(COURSE['title']),status=e(COURSE['status']),chapters='\n'.join(cards))
    (output/'index.html').write_text(index)
    for case in COURSE['cases']:(output/(case['id']+'.html')).write_text(render_case(case))
    render_workbook(output)
    about='<main id="main" class="wrap document"><p class="eyebrow">How to use the course</p><h1>Learn, try, reflect.</h1><p>'+e(COURSE['scope'])+'</p><h2>Choose your pace</h2><p>Each chapter has eight pages: a story, an initial decision, two explanations, a worked example, a new decision, recall, and a lab. Allow 20–30 minutes per chapter plus optional practice between sessions. Use the three independent cases to practise selecting a tool. Suggested time is an estimate, not pilot data.</p><h2>Listen or read</h2><p>Use the recorded audio controls on each page, or read the text and transcript. Narration uses the synthetic Kokoro af_heart voice. Feedback and revealed answers are text-only. Navigation stops playback. Audio speed is adjustable. The reading edition includes every feedback option.</p><h2>Progress and writing</h2><p>Only page IDs, practice attempts, and your last page are saved locally in this browser. They are not a mastery score. Your written responses stay in the current document and are never saved automatically or submitted. Export before leaving. Clearing progress affects this course’s saved progress only. If storage is unavailable, the course still works for this visit.</p><button class="button" data-clear-progress>Clear saved progress</button><p role="status" data-storage-message></p><h2>Use fictional cases if you prefer</h2><p>You can complete every activity without personal disclosure. Keep optional personal examples mild and manageable. Pause or stop an activity that does not fit. Persistent, worsening, or substantially disruptive difficulties deserve support from a qualified professional; you do not need to finish this course first.</p><h2>What has been reviewed</h2><p>The material is an original draft informed by the sources below. No qualified practitioner review, learner pilot, clinical outcome study, independent speech recognition screen, or human narration listening review has taken place. Technical build and browser checks do not establish clinical effectiveness.</p><h2>Chapter evidence notes</h2>'
    for n,c in enumerate(COURSE['chapters'],1):about+=f'<h3>{n:02d}. {e(c["title"])}</h3>'+evidence(c)
    about+='<h2>Credits and rights</h2><p>Visual styling follows Common Ground at the repository owner’s request. All lesson stories, illustrations, diagrams, and implementation here are original. Font notices accompany the unchanged Libre Baskerville and Arimo files. Third-party source readings retain their own rights.</p><p><a href="./FONT-LICENSE.txt">Font licenses</a> · <a href="./THIRD-PARTY-NOTICES.txt">Third-party notices</a> · <a href="https://github.com/snowch/everyday-cbt">Repository and production notes</a></p></main>'
    (output/'about.html').write_text(document('Course guidance and sources',about))
    for asset in ('course.css','app.js','favicon.svg'):shutil.copyfile(ROOT/'site'/asset,output/asset)
    css=(ROOT/'site/style.css').read_text()
    for name in ('LibreBaskerville[wght].ttf','Arimo[wght].ttf'):
        encoded=base64.b64encode((ROOT/'assets/fonts'/name).read_bytes()).decode()
        css=css.replace(f"url('./assets/fonts/{name}')",f"url('data:font/ttf;base64,{encoded}')")
    (output/'style.css').write_text(css)
    for directory in ('assets','licenses','audio'):
        if (ROOT/directory).exists():shutil.copytree(ROOT/directory,output/directory,dirs_exist_ok=True)
    for name in ('FONT-LICENSE.txt','THIRD-PARTY-NOTICES.txt','workbook.pdf','course.pdf'):
        if (ROOT/name).exists():shutil.copyfile(ROOT/name,output/name)
    script='\n\n'.join(c['title']+'\n\n'+'\n\n'.join(p['id']+'\n'+spoken(p) for p in c['pages']) for c in COURSE['chapters'])
    (output/'narration-script.txt').write_text(script+'\n')
    (output/'.nojekyll').touch()
    print('Built 12 chapters, 96 lesson pages, 24 decisions, 24 recall prompts, 12 labs, 3 cases, workbook, and reading edition')
