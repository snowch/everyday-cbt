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
STAGES={'story':'Fictional story','decision':'Decision','concept':'Explanation','example':'Worked example','recall':'Recall practice','lab':'Practice lab'}
WRITING_NOTE = 'Writing is optional. Drafts stay on this page until you reload or leave it. Download any draft you want to keep.'

def paragraphs(items):
    return ''.join(f'<p>{e(x)}</p>' for x in items)

def teaching_copy(page):
    if page['type'] in ('story', 'concept', 'example'):
        return '<ul class="key-messages">'+''.join(f'<li>{e(message)}</li>' for message in page['key_messages'])+'</ul>'
    return lesson_intro(page)

def field(prompt, key, described_by=None, export_prompt=None, label=None):
    description = f' aria-describedby="{described_by}"' if described_by else ''
    return f'<div class="writing-field"><label for="{key}">{e(label or prompt)}</label><textarea id="{key}" data-prompt="{e(export_prompt or prompt)}" rows="3" spellcheck="true"{description}></textarea></div>'

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
    relationship = {
        'map': 'The five parts can affect one another.',
        'loop': 'Read the entries in order. The last can lead back to the first.',
    }.get(kind, '')
    text_intro = f'<p class="diagram-relationship">{e(relationship)}</p>' if relationship else ''
    entries = ''.join(f'<dt>{e(item["label"])}</dt><dd>{e(item["detail"])}</dd>' for item in items)
    return f'<figure class="concept-figure"><svg viewBox="0 0 600 {height}" role="img" aria-labelledby="{key}-title {key}-desc"><title id="{key}-title">{e(d["title"])}</title><desc id="{key}-desc">{e(desc)}</desc><defs><marker id="{key}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 10 5 0 10Z" fill="#7C9FB3"/></marker></defs><g fill="none" stroke="#7C9FB3" stroke-width="2" marker-end="url(#{key}-arrow)"{connections}>{"".join(paths)}</g><g text-anchor="middle" fill="#19394D" font-family="CourseSans,Arial,sans-serif">{"".join(boxes)}</g></svg><figcaption>{e(d["title"])}</figcaption><details class="diagram-key"><summary>Read diagram as text</summary>{text_intro}<dl>{entries}</dl></details><div class="diagram-text">{text_intro}<dl>{entries}</dl></div></figure>'

def scene(chapter,key):
    names=['Alex','Nia','Jules'];colours=['#7058A3','#216B88','#A1486D'];people=[]
    for i,(name,colour) in enumerate(zip(names,colours)):
        x=138+i*155
        people.append(f'<g><path d="M{x-40} 355v-78q0-37 40-37t40 37v78" fill="{colour}" stroke="#19394D" stroke-width="3"/><circle cx="{x}" cy="210" r="27" fill="{["#E6AE86","#B77C58","#EBC19D"][i]}" stroke="#19394D" stroke-width="3"/><path d="M{x-26} 208q-7-42 30-32 28 3 22 35l-14-22-16 9-13-7Z" fill="#19394D"/><circle cx="{x-8}" cy="212" r="2" fill="#19394D"/><circle cx="{x+8}" cy="212" r="2" fill="#19394D"/><path d="M{x-6} 225q6 5 12 0" fill="none" stroke="#19394D" stroke-width="2"/><path d="M{x-16} 355l-8 57m40-57 8 57" stroke="#19394D" stroke-width="10" stroke-linecap="round"/><text x="{x}" y="452" text-anchor="middle" fill="#19394D" font-family="CourseSans,Arial,sans-serif" font-size="18">{name}</text></g>')
    labels=['A cancelled session','Check the signup list','One wrong date','An unanswered message','Make room for drawing','Three tasks, two evenings','Ask one clear question','An ordinary greeting','The conversation replays','A realistic commitment','A fairer rota','A difficult week']
    return f'<figure class="story-figure"><svg viewBox="0 0 600 490" role="img" aria-labelledby="{key}-scene-title {key}-scene-desc"><title id="{key}-scene-title">{e(labels[chapter-1])}</title><desc id="{key}-scene-desc">Alex, Nia and Jules, the recurring fictional characters, beside a drawing table.</desc><path d="M32 425V230a268 210 0 0 1 536 0v195Z" fill="#D8E6EE"/><path d="M55 425V230a245 188 0 0 1 490 0v195Z" fill="#F2F6F9" stroke="#A9C4D3" stroke-width="2"/><rect x="132" y="74" width="336" height="54" rx="7" fill="#19394D"/><text x="300" y="108" text-anchor="middle" fill="white" font-family="CourseSans,Arial,sans-serif" font-size="20">{e(labels[chapter-1])}</text>{"".join(people)}<path d="M65 335h470l24 31H41Z" fill="#D8AC5C" stroke="#19394D" stroke-width="3"/><path d="M78 366v63m444-63v63" stroke="#19394D" stroke-width="10" stroke-linecap="round"/><rect x="240" y="293" width="105" height="44" rx="3" fill="#FFF" stroke="#19394D" stroke-width="2"/><path d="M253 305h63m-63 9h76m-76 9h46" stroke="#A9C4D3" stroke-width="3"/><path d="M370 326l44-40" stroke="#7058A3" stroke-width="7" stroke-linecap="round"/></svg></figure>'

def practice_intro(page, reading=False):
    if page['type'] == 'decision':
        note = 'Choose one option before reading its feedback.' if reading else 'Choose one option, then select Check choice. Read how it fits this situation. You can check the other options too.'
        return f'<p class="decision-instructions">{e(note)}</p>'
    if page['type'] == 'recall':
        note = 'Answer each question in your own words before reading the suggested answer.' if reading else 'Answer each question in your own words. Use the optional response boxes or think through your answers. Then open the suggested answer under each question and check which ideas you included.'
        return paragraphs([note])
    if page['type'] == 'lab':
        return paragraphs(['Work through the five prompts in order. Read the worked response after your first draft, then use the review question to compare.'])
    return ''


def practice(page, reading=False, workbook=False):
    key=page['id'];out=''
    if page['type']=='decision':
        if reading:
            out='<ol class="reading-options">'+''.join(f'<li><strong>{e(o["text"])}</strong><details><summary>Feedback on option {"ABC"[i]}</summary><p>{e(o["feedback"])}</p></details></li>' for i,o in enumerate(page['options']))+'</ol>'
        else:
            options=''.join(f'<label class="option"><input type="radio" name="{key}" value="{i}" required><span><span class="option-letter">{"ABC"[i]}.</span> {e(o["text"])}</span></label>' for i,o in enumerate(page['options']))
            feedback=''.join(f'<div class="feedback" data-feedback="{i}" tabindex="-1" role="group" aria-labelledby="{key}-feedback-{i}" aria-describedby="{key}-feedback-copy-{i}" hidden><strong id="{key}-feedback-{i}">{"ABC"[i]}. {"Strongest choice for this question" if i==page["best"] else "Feedback on this choice"}</strong><p id="{key}-feedback-copy-{i}">{e(o["feedback"])}</p></div>' for i,o in enumerate(page['options']))
            out=f'<form class="decision-form" data-practice="{key}"><fieldset><legend class="sr-only">Choose one option</legend>{options}</fieldset><button class="button primary" type="submit">Check choice</button>{feedback}</form>'
    if page['type']=='recall':
        for i,q in enumerate(page['questions']):
            prompt_id=f'{key}-prompt-{i}'
            out+=f'<section class="recall-question"><h3 id="{prompt_id}">{e(q["prompt"])}</h3>'
            if not reading:
                out+=field('Your response (optional)',f'{key}-r{i}',prompt_id,q["prompt"])
            out+=f'<details><summary>Suggested answer for question {i+1}</summary><p>{e(q["answer"])}</p></details></section>'
    if page['type']=='lab':
        if reading and not workbook:
            out='<ol>'+''.join(f'<li>{e(prompt)}</li>' for prompt in page['fields'])+'</ol>'
        else:
            out=''.join(field(prompt,f'{key}-l{i}',label=f'{i+1}. {prompt}') for i,prompt in enumerate(page['fields']))
        out+=f'<details><summary>Worked response</summary>{paragraphs(page["example"].splitlines())}</details><p class="review-note">{e(page["comparison"])}</p>'
    if not reading and page['type'] in ('recall','lab'):
        out+=f'<button class="button primary" data-tried="{key}" aria-disabled="false">Mark practice as tried</button><p class="practice-status" role="status" data-practice-status></p>'
    return out


def lesson_title(page):
    return 'The situation' if page['type'] == 'story' else page['title']


def lesson_intro(page):
    if page['type'] == 'recall':
        return ''
    return paragraphs(page['paragraphs'])


def writing_note(chapter=False):
    text = 'Writing is optional. Drafts stay in this chapter as you move between lesson pages. Download any draft you want to keep before reloading or leaving the chapter.' if chapter else WRITING_NOTE
    return f'<p class="writing-note">{e(text)}</p>'


def writing_tools():
    return '<div class="response-tools"><button class="button" data-export>Download my responses</button></div>'


def evidence(c):
    links=''.join(f'<li><a href="{e(s["url"])}">{e(s["title"])}</a></li>' for s in c['sources'])
    return f'<details class="evidence"><summary>What this example illustrates and where to read more</summary><p>{e(c["evidence_note"])}</p><ul>{links}</ul><p class="small">Source links checked {COURSE["reviewed"]}.</p></details>'

def document(title,body,prefix='./',extra='',bodyclass='document-page'):
    if bodyclass=='chapter-page':
        footer=f'<footer class="wrap lesson-footer"><a href="{prefix}about.html">Course guidance</a><a href="{prefix}FONT-LICENSE.txt">Font licenses</a></footer>'
    else:
        footer=f'<footer class="wrap"><span class="wordmark">Everyday CBT</span><p>Draft {e(COURSE["version"])} · practitioner review pending.<br>Introductory education. The course does not submit your responses.</p><div><a href="{prefix}about.html">Guidance &amp; sources</a><br><a href="{prefix}FONT-LICENSE.txt">Font licenses</a></div></footer>'
    return Template((ROOT/'site/document.html').read_text()).substitute(title=e(title),body=body,prefix=prefix,extra=extra,bodyclass=bodyclass,footer=footer)

def render_chapter(c,n,output):
    previous=f'<a href="./{COURSE["chapters"][n-2]["slug"]}.html">Previous chapter</a>' if n>1 else ''
    nextlink=f'<a class="button" href="./{COURSE["chapters"][n]["slug"]}.html">Next chapter</a>' if n<12 else '<a class="button" href="../case-final.html">Try the final case</a>'
    checkpoint=next((x for x in COURSE['cases'] if x['after']==n),None)
    checkpoint_link=f'<aside class="checkpoint"><h2>Optional checkpoint</h2><p>Use what you’ve learned so far to work through a new fictional situation.</p><a class="button" href="../{checkpoint["id"]}.html">{e(checkpoint["title"])}</a></aside>' if checkpoint and n<12 else ''
    pages=[]
    for i,p in enumerate(c['pages']):
        key=p['id']
        art=visual(p['diagram'],key) if p.get('diagram') else scene(n,key) if p['type'] in ('story','example') else ''
        writing = p['type'] in ('recall', 'lab')
        title = lesson_title(p)
        body=f'<div class="lesson-copy"><p class="lesson-stage">{STAGES[p["type"]]}</p><h2 id="{key}-heading">{e(title)}</h2>{teaching_copy(p)}{practice_intro(p)}{writing_note(chapter=True) if writing else ""}{practice(p)}{writing_tools() if writing else ""}</div>'
        clip=ROOT/'audio/clips'/f'{key}.m4a'
        audio=f'<audio controls preload="none" src="../audio/clips/{key}.m4a" aria-label="Narration for {e(p["title"])}"></audio>' if clip.exists() else '<p>Recording is being prepared.</p>'
        transcript=f'<details class="recording-transcript"><summary>Read the narration transcript</summary><p>{e(spoken(p))}</p></details>'
        primary = ' primary' if p['type'] in ('story', 'concept', 'example') else ''
        next_control=nextlink if i==7 else f'<button class="button{primary}" data-step="1">Next page</button>'
        transition=checkpoint_link if i==7 else ''
        pages.append(f'<section class="lesson-page" id="p{i+1}" data-page="{i}" data-id="{key}" data-type="{p["type"]}" tabindex="-1" aria-labelledby="{key}-heading"><div class="lesson {"has-art" if art else ""}">{body}{f"<div class=lesson-art>{art}</div>" if art else ""}</div><div class="narration">{audio}<label>Playback speed <select class="audio-rate" aria-label="Playback speed for page {i+1}"><option value="0.8">0.8×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label></div>{transcript}{transition}<nav class="lesson-bottom-controls" aria-label="Page controls"><button class="button" data-step="-1" {"disabled" if i==0 else ""}>Previous page</button>{next_control}</nav></section>')
    nav=''.join(f'<a href="#p{i+1}" data-page-link="{i}" aria-label="Page {i+1}, {e(lesson_title(p))}">{i+1}</a>' for i,p in enumerate(c['pages']))
    options=f'<details class="chapter-options"><summary>Chapter options</summary><div class="chapter-options-panel"><p class="progress-caption" data-chapter-progress></p><a href="../workbook.html#lab-{n}">Open this lab in the workbook</a><a href="../about.html#chapter-sources-{n}">Evidence &amp; further reading</a>{previous}<button class="button" data-print>Print this chapter</button></div></details>'
    body=f'<main id="main" tabindex="-1" class="player wrap" data-chapter="{e(c["slug"])}"><div class="player-heading"><div><p class="eyebrow">Chapter {n} of 12</p><h1>{e(c["title"])}</h1><p class="draft-label">Draft introductory course. Practitioner review pending.</p></div>{options}</div><div class="page-location"><nav class="lesson-nav" aria-label="Lesson pages">{nav}</nav><p id="page-status" role="status">8 lesson pages</p></div><p class="storage-notice" data-progress-status role="status" hidden></p><noscript><style>.lesson-nav, .page-location, .lesson-bottom-controls, .chapter-options, .response-tools, .decision-form, .decision-instructions, .writing-note, [data-tried] {{ display: none }}</style><p class="notice">All pages appear below. Use the <a href="../reading.html#chapter-{n}">reading edition</a> to see every choice and its feedback.</p></noscript>{"".join(pages)}</main>'
    (output/'chapters'/f'{c["slug"]}.html').write_text(document(c['title'],body,'../',bodyclass='chapter-page'))

def case_tasks(case, prefix):
    out = ''
    has_update = len(case['story']) > 2
    for i, (title, prompt, answer) in enumerate(case['tasks'], 1):
        if has_update and i == 5:
            out += f'<details class="new-information"><summary>Read the organiser’s message after tasks 1–4</summary>{paragraphs(case["story"][2:])}</details>'
        key = f'{prefix}-{i}'
        out += f'<section class="case-task"><h3>{i}. {e(title)}</h3><p id="{key}-prompt">{e(prompt)}</p>{field("Your response (optional)",key,key+"-prompt",prompt)}<details><summary>Suggested response for task {i}</summary><p>{e(answer)}</p></details></section>'
    return out


def case_review(case):
    return '<section><h3>Review your first draft</h3><p>Find one place your draft meets these criteria and one place you would revise. This is a self-check.</p><ul>'+''.join(f'<li>{e(x)}</li>' for x in case['rubric'])+'</ul></section>'


def render_case(case):
    body=f'<main id="main" class="wrap document" data-case="{case["id"]}"><p class="eyebrow">Independent practice · about 20–30 minutes</p><h1>{e(case["title"])}</h1><p>Read Rowan’s story and work through the tasks in order. Draft your reasoning before reading each suggested response. More than one approach may fit.</p>{writing_note()}<section class="case-story"><h2>The fictional situation</h2>{paragraphs(case["story"][:2])}</section><h2>Practice tasks</h2>{case_tasks(case,case["id"])}{case_review(case)}<div class="response-tools"><button class="button primary" data-export>Download my responses</button><button class="button" data-print>Print case</button></div><p><a href="./index.html#course">Return to the chapters</a></p></main>'
    return document(case['title'],body)


def render_workbook(output):
    labs = ''.join(f'<li><a href="#lab-{n}">{e(c["pages"][-1]["title"])}</a></li>' for n,c in enumerate(COURSE['chapters'],1))
    cases = ''.join(f'<li><a href="#{case["id"]}">{e(case["title"])}</a></li>' for case in COURSE['cases'])
    body=f'<main id="main" class="wrap document workbook"><h1>Practice workbook</h1><p>Choose a lab to practise one skill or a fictional case to practise several. You can use the fictional examples for every task.</p><p>{e(COURSE["scope"])}</p>{writing_note()}<div id="workbook-tools" class="response-tools" tabindex="-1"><button class="button" data-export>Download all workbook responses</button><button class="button" data-print>Print workbook</button><a href="./workbook.pdf">Download blank workbook PDF</a></div><nav aria-label="Workbook contents"><h2>Chapter labs</h2><ol>{labs}</ol><h2>Independent cases</h2><ul>{cases}</ul></nav>'
    for n,c in enumerate(COURSE['chapters'],1):
        lab=c['pages'][-1]
        body+=f'<section class="workbook-lab" id="lab-{n}"><p class="eyebrow">Chapter {n}</p><h2>{e(lab["title"])}</h2>{paragraphs(lab["paragraphs"])}{practice_intro(lab)}{practice(lab,reading=True,workbook=True)}<p class="screen-only"><a href="#workbook-tools">Go to workbook download and print controls</a></p><p><a href="./chapters/{c["slug"]}.html#p8">Open this lab in the chapter</a></p></section>'
    for case in COURSE['cases']:
        body+=f'<section class="workbook-lab" id="{case["id"]}"><h2>{e(case["title"])}</h2><p>Read Rowan’s story and draft your reasoning before reading each suggested response.</p>{paragraphs(case["story"][:2])}{case_tasks(case,"wb-"+case["id"])}{case_review(case)}</section>'
    body+='<p class="screen-only"><a href="#workbook-tools">Go to workbook download and print controls</a></p></main>'
    (output/'workbook.html').write_text(document('Practice workbook',body))
    contents = ''.join(f'<li><a href="#chapter-{n}">{e(c["title"])}</a></li>' for n,c in enumerate(COURSE['chapters'],1))
    reading=f'<main id="main" class="wrap document reading"><h1>Complete reading edition</h1><p>{e(COURSE["scope"])}</p><p>Read all twelve chapters, including feedback, recall answers and worked lab responses. For recorded narration and interactive decisions, open a chapter from the <a href="./index.html#course">course home</a>.</p><div class="response-tools"><button class="button" data-print>Print reading edition</button><a href="./course.pdf">Download reading edition PDF</a></div><nav aria-label="Reading contents"><h2>Chapters</h2><ol>{contents}</ol></nav>'
    for n,c in enumerate(COURSE['chapters'],1):
        reading+=f'<section class="reading-chapter" id="chapter-{n}"><p class="eyebrow">Chapter {n}</p><h2>{e(c["title"])}</h2>'
        for p in c['pages']:
            title = lesson_title(p)
            reading+=f'<section class="reading-page"><h3>{e(title)}</h3>{lesson_intro(p)}{practice_intro(p,reading=True)}'+(visual(p['diagram'],'read-'+p['id']) if p.get('diagram') else '')+practice(p,reading=True)+'</section>'
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
            if p['type'] in ('story', 'concept', 'example'):
                messages=p['key_messages']
                assert 3<=len(messages)<=4 and all(isinstance(x,str) and x.strip() for x in messages),key+' teaching summaries'
                assert all(len(x.split())<=30 for x in messages),key+' summary too long'
            if p['type']=='decision':assert len(p['options'])==3 and 0<=p['best']<3 and all(o['text'] and o['feedback'] for o in p['options'])
            if p['type']=='recall':assert len(p['questions'])==2 and all(q['prompt'] and q['answer'] for q in p['questions'])
            if p['type']=='lab':assert len(p['fields'])==5 and len(p['example'].splitlines()) == 5 and p['review'] and p['comparison']
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
        cards.append(f'<article class="chapter" id="chapter-{c["slug"]}"><span class="chapter-number">{n:02d}</span><div><h3><a class="chapter-link" data-slug="{c["slug"]}" href="./chapters/{c["slug"]}.html">{e(c["title"])}</a></h3><p class="story">{e(c["story"])}</p><p class="chapter-progress" data-progress="{c["slug"]}">Not yet viewed</p></div></article>')
        render_chapter(c,n,output)
    index=Template((ROOT/'site/template.html').read_text()).substitute(title=e(COURSE['title']),status=e(COURSE['status']),chapters='\n'.join(cards))
    (output/'index.html').write_text(index)
    for case in COURSE['cases']:(output/(case['id']+'.html')).write_text(render_case(case))
    render_workbook(output)
    about=f"""<main id="main" class="wrap document"><h1>Course guidance and sources</h1>
    <p>{e(COURSE['scope'])}</p>
    <h2>Work through a chapter</h2>
    <p>Start with the fictional story and try the first decision. Read or listen to the explanation and worked example, then try the second decision, the recall questions and the lab. Each chapter is estimated to take 20–30 minutes. After chapters 4 and 8 you can try a checkpoint, and after chapter 12 you can try the final case.</p>
    <p>Every exercise works with fictional examples. For optional personal examples, choose a mild everyday situation you are comfortable considering. You can pause or stop. If difficulties persist, worsen or substantially affect daily life, consider support from a qualified professional.</p>
    <h2>Listen or read</h2>
    <p>Use the audio controls or open Read the narration transcript on a lesson page. Audio stops when you move to another page. Feedback and worked answers are written. The <a href="./reading.html">reading edition</a> includes every option and its feedback.</p>
    <h2>Progress and writing</h2>
    <p>The browser saves which pages you viewed, which practices you checked or marked as tried, and the last page you visited. These counts describe activity. Use the feedback and suggested answers to review your reasoning.</p>
    <p>Drafts stay in the current chapter, workbook or case page until you reload or leave. Select Download my responses on that page to keep a copy. The course does not submit your draft.</p>
    <p>Clear saved progress removes this course’s activity record from this browser. The course works even if your browser blocks storage.</p>
    <button class="button" data-clear-progress>Clear saved progress</button><p role="status" data-storage-message></p>
    <h2>Course review status</h2>
    <p>The authors used the sources below to develop this draft. Their publishers have not reviewed or endorsed the course. Technical checks cover the website and synthetic audio. A qualified practitioner review, learner pilot, clinical outcome study and human listening review are still pending.</p>
    <h2>Chapter evidence notes</h2><p>Sources include the UK National Health Service (NHS), the Centre for Clinical Interventions in Western Australia (CCI) and the UK National Institute for Health and Care Excellence (NICE).</p>"""
    for n,c in enumerate(COURSE['chapters'],1):about+=f'<h3 id="chapter-sources-{n}">{n:02d}. {e(c["title"])}</h3>'+evidence(c)
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
