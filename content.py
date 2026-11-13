"""Author the original Everyday CBT lessons; write the canonical course.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
course = json.loads((ROOT / 'course.json').read_text())
chapters = {c['slug']: c for c in course['chapters']}
NHS = 'https://www.nhs.uk/tests-and-treatments/cognitive-behavioural-therapy-cbt/'
THOUGHTS = 'https://www.nhs.uk/every-mind-matters/mental-wellbeing-tips/self-help-cbt-techniques/reframing-unhelpful-thoughts/'
CCI = 'https://www.cci.health.wa.gov.au/Resources/Looking-After-Yourself/'

def diagram(title, *items, kind='steps'):
    return {'title': title, 'kind': kind, 'items': [{'label': a, 'detail': b} for a,b in items]}

def question(title, prompt, best, *options):
    return {'type': 'decision', 'title': title, 'paragraphs': [prompt], 'best': best,
            'options': [{'text': a, 'feedback': b} for a,b in options]}

def lesson(title, paragraphs, visual):
    return {'type': 'concept', 'title': title, 'paragraphs': paragraphs, 'diagram': visual}

def add(slug, story, first, concepts, example, transfer, recall, lab, sources, limits):
    c=chapters[slug]
    c['pages']=[{'type':'story','title':c['title'],'paragraphs':story},first,*concepts,
                {'type':'example','title':example[0],'paragraphs':example[1]},transfer,
                {'type':'recall','title':'Explain it without looking','paragraphs':['Take a moment to answer in your own words before revealing the suggested reasoning.'],'questions':[{'prompt':a,'answer':b} for a,b in recall]},
                {'type':'lab','title':lab[0],'paragraphs':lab[1],'fields':lab[2],'example':lab[3],'review':lab[4]}]
    c['sources']=[{'title':a,'url':b} for a,b in sources]
    c['evidence_note']=limits
    c['minutes']='20–30 minutes, plus optional field practice'

add('one-event',[
    'Alex, Nia, and Jules meet at a Saturday drawing group. One afternoon the organiser writes: “We need to cancel next week.” There is no explanation in the message.',
    'Alex thinks, “Maybe hardly anyone wanted to come,” feels disappointed, and leaves the group chat unopened. Nia thinks, “I have a free afternoon,” feels relieved, and plans some rest. Jules thinks, “Did I cause a problem?” and sends an apologetic message.',
    'The cancellation is the same. Their interpretations, bodies, feelings, and actions differ. We do not yet know why the organiser cancelled. Begin by describing each person’s experience without deciding whose reaction is justified.'
], question('Start with what is known','Which statement describes an observation rather than an interpretation?',0,
    ('The organiser sent a message cancelling next week’s group.','This describes something that could be checked in the message. It leaves the organiser’s reasons open.'),
    ('The organiser no longer likes the group.','This is a possible explanation, but the message does not establish it. Treat it as an interpretation to examine.'),
    ('Jules must have done something wrong.','This is Jules’s worry presented as a fact. Their distress matters, but it does not establish responsibility.')),
 [lesson('Five parts, one experience',[
    'A situation is a specific event or circumstance. A thought is an interpretation, prediction, memory, or image. An emotion is a feeling such as sadness or anxiety. Bodily sensations include a tight stomach or warmth in the face. Behaviour is what a person does, including withdrawing or asking a question.',
    'These parts influence one another. A racing heart can make a situation feel threatening; leaving can bring relief and change what happens next. The map is a working description, not proof that a thought caused every feeling. Sleep, pain, money, relationships, and other circumstances also matter.'
 ],diagram('Jules’s five-part map',('Situation','Group cancelled'),('Thought','Did I cause this?'),('Feeling','Anxiety'),('Body','Tight stomach'),('Behaviour','Apologetic message'),kind='map')),
 lesson('Make the map specific',[
    '“My week was awful” is too broad to investigate. “At three o’clock I read the cancellation message” gives us a moment to examine. “I feel rejected” can contain both an emotion and an interpretation: sadness is the feeling; “they do not want me there” is the meaning.',
    'A map is a hypothesis you can correct. Ask what the person noticed rather than assigning thoughts to them. The first useful change may be practical: checking whether the session will be rescheduled, arranging rest, or asking for information.'
 ],diagram('Describe before explaining',('Observe','What happened?'),('Ask','What did it mean to them?'),('Separate','Feeling, body, action'),('Revisit','What is still unknown?')))],
 ('A map with room for uncertainty',[
    'Jules writes: Situation: the group was cancelled. Thought: “My request for different materials annoyed the organiser.” Feeling: anxiety. Body: tight stomach. Behaviour: sending an apology before finding out why.',
    'Jules changes “I caused the cancellation” to “I am predicting that my request caused it.” That small wording change preserves the concern while acknowledging uncertainty. It does not require Jules to feel calm or believe that everything is fine.'
 ]),question('Try it in another setting','A colleague walks past without saying hello. You feel hurt. Which next description gives you the most useful starting point?',1,
    ('They deliberately ignored me because they dislike me.','This combines an observation with an untested intention. You can record the possibility without treating it as established.'),
    ('They walked past; I thought they were avoiding me; I felt hurt and stopped approaching them.','This separates the event, interpretation, feeling, and action. You can now examine what is known and what could be checked.'),
    ('I should not feel hurt because it is probably nothing.','This dismisses the feeling and replaces one uncertain explanation with another. Understanding comes before judging the reaction.')),
 [('What distinguishes a thought from an emotion?','A thought carries meaning, such as “I am unwanted.” An emotion names a feeling, such as sadness. Both can be present in the same moment.'),('Why is a five-part map provisional?','It records what is currently understood. The person may remember more, clarify their meaning, or learn new facts. It does not capture every cause.')],
 ('Lab: map one moment',['Use Jules’s cancellation story, or choose a mild everyday situation you are comfortable considering. Keep to one moment. Personal disclosure is optional.'],['What happened that another person could observe?','What thought or image appeared?','Which feelings and bodily sensations were present?','What did the person do next?','What is known, and what remains an interpretation?'],
 'Jules observed a cancellation, predicted personal blame, felt anxious with a tight stomach, and sent an apology. The reason for cancellation is still unknown.',
 'Check that the event and its meaning are separate. You do not need to change a feeling to complete the map.'),
 [('NHS: cognitive behavioural therapy',NHS),('CCI: depression resources — thinking and feeling',CCI+'Depression')],
 'The five-part map is a teaching aid for describing connections. A brief fictional case cannot establish a complete formulation or explain all causes of distress.')

add('patterns',[
    'Alex volunteers to update the drawing group’s non-critical signup list. They check the dates, then check again. For a moment the worry eases. A few minutes later Alex thinks, “What if I missed something?”',
    'After the sixth check, the list is unchanged but Alex has missed a planned break. “I only finished because I kept checking,” Alex concludes. We need to examine what each check achieves now and what it might make harder later.'
],question('Look at the consequence','What information would best help explain the repeated checking?',1,
    ('Whether Alex is a perfectionist by nature.','A label may sound explanatory but does not show how this particular pattern works. Look at triggers and consequences.'),
    ('What happens to the worry immediately after checking, and when doubt returns.','This can reveal a short-term reward and a longer-term cost. The explanation remains a hypothesis to test.'),
    ('Whether the list is perfectly accurate.','Accuracy matters, but it cannot by itself explain why another check feels necessary after no changes. Both task demands and consequences matter.')),
 [lesson('Relief can strengthen a response',[
    'When a behaviour removes something unpleasant, a person may become more likely to repeat it. Psychologists call this negative reinforcement. “Negative” means removal here; it is not a judgment about the person.',
    'Alex’s check briefly removes doubt. The next time doubt appears, another check seems attractive. This does not mean all checking is unhelpful: a proportionate check can prevent an actual error. The question is the function and cost of the extra checks in this context.'
 ],diagram('A possible checking loop',('Trigger','A doubtful thought'),('Action','Check the list again'),('Immediate effect','Brief relief'),('Later effect','Doubt returns'),kind='loop')),
 lesson('Choose a point of influence',[
    'A maintenance cycle describes what may keep a current difficulty going. It is different from a life history explaining how the difficulty began. Several influences can operate at once.',
    'Alex could agree a clear, ordinary checking standard with the organiser, then observe what happens after following it. The aim is to learn, not to ban checking everywhere. Checking instructions for a medical, legal, or safety-critical task would require the proper standards for that task.'
 ],diagram('Useful checking or repeated relief?',('Task requirement','What check is actually needed?'),('Extra repetition','What does another check add?'),('Cost','What else is being lost?'),('Small test','Use an agreed standard')))],
 ('Alex’s first working hypothesis',[
    'Alex records three occasions: after a check, worry falls briefly; later it returns despite no new information. That pattern fits the idea that relief helps maintain the repetition. It does not prove the explanation is complete.',
    'For this ordinary signup list, Alex and the organiser agree to check names against the source once and review changed entries. Alex follows that plan, then records the outcome. If the standard misses important errors, they revise the process rather than declaring the experiment a personal failure.'
 ]),question('A different loop','Nia repeatedly asks a friend whether a short message sounded rude. The reassurance lasts only minutes. What would best clarify the pattern?',2,
    ('Ask the friend to promise the message could not offend anyone.','A stronger promise might bring relief but cannot guarantee every response. It may leave the same need for reassurance in place.'),
    ('Decide that asking for support is always a problem.','Support can be valuable. The relevant question is whether repeated reassurance is providing new information or mainly brief relief.'),
    ('Record the trigger, reassurance, immediate relief, and return of doubt.','This distinguishes a possible maintenance loop from a blanket judgment about support. It also leaves room for a practical communication problem.')),
 [('What does negative reinforcement mean here?','A behaviour becomes more likely because it removes something unpleasant, such as doubt. It does not mean punishment.'),('How does a maintenance explanation differ from an origin story?','It focuses on present triggers and consequences that may sustain a pattern, even when the pattern began for other reasons.')],
 ('Lab: follow the loop',['Use Alex’s signup list. Describe a loop with four parts, then identify one small point that could be investigated.'],['What starts the sequence?','What does Alex do?','What changes immediately?','What happens later, including any cost?','What task-appropriate change could be tested?'],
 'Doubt → extra check → brief relief → renewed doubt and lost break. Agreeing an ordinary checking standard could make an observable, low-stakes test.',
 'Check that your proposed change fits the task. A cycle is a working explanation, not a label for the person.'),
 [('CCI: perfectionism — what keeps it going?',CCI+'Perfectionism'),('CCI: social anxiety — safety behaviours',CCI+'Social-Anxiety')],
 'This example illustrates a possible reinforcement process. Repetitive checking can have different functions; this course does not assess or treat compulsive symptoms.')

add('automatic-thoughts',[
    'Jules notices a wrong date on a poster they helped make. Someone quietly points it out. Jules says, “No problem,” then stays silent for the rest of the session.',
    'Later Jules remembers a sudden image: everyone looking at the poster and shaking their heads. The words were, “I always let people down.” The visible mistake was small; the personal meaning was much larger.'
],question('Ask about the moment','Which question is most likely to uncover the thought linked to Jules’s change in mood?',0,
    ('When you noticed the date, what went through your mind, including any image?','This invites Jules’s own recollection at the specific moment, without supplying a conclusion.'),
    ('You knew they all disliked the poster, didn’t you?','This leads Jules toward an interpretation the questioner has invented. The person’s actual meaning could be different.'),
    ('Why are you always so hard on yourself?','This generalises and may sound blaming. A specific moment is easier to investigate than a judgment about character.')),
 [lesson('A thought can arrive as a picture',[
    'Automatic thoughts often arrive quickly, before someone deliberately reasons through a situation. They can be words, images, or a sense of what will happen. “Everyone judging the poster” is an image carrying the prediction “They see me as unreliable.”',
    'To notice a thought, return to a manageable moment: what happened, when did the feeling shift, and what did it seem to mean? If nothing comes to mind, leave the space open. You do not have to invent a thought to make the model fit.'
 ],diagram('From a moment to its meaning',('Event','Wrong date noticed'),('Image','Everyone shaking heads'),('Meaning','I let people down'),('Response','Shame and silence'))),
 lesson('Name the meaning without endorsing it',[
    '“I am a failure” is a thought, not a diagnosis or a fact established by feeling ashamed. Recording “I had the thought that I am a failure” can help distinguish the experience from the conclusion.',
    'Thinking patterns such as overgeneralising or mind-reading can be useful descriptions. They are not a checklist for proving someone irrational. Start with the exact thought, the context, and the evidence. A real mistake can coexist with a much broader conclusion that needs checking.'
 ],diagram('Keep the scale of the claim visible',('Specific fact','One poster has a wrong date'),('Broad thought','I always let people down'),('Open question','What supports “always”?'),('Possible action','Correct this poster')))],
 ('A more precise record',[
    'Jules initially writes “I felt useless.” They clarify the feeling as shame and the thought as “If I make a visible mistake, people cannot rely on me.” Their shoulders tense, and they stop offering help.',
    'Jules can now address two things: correcting the date and examining the prediction about reliability. The map does not erase the mistake. It prevents one error from silently becoming a complete verdict on their worth.'
 ]),question('Find the thought','Alex says, “I felt anxious before the group because I pictured being unable to speak.” Which part is the automatic thought?',1,
    ('The word anxious.','Anxious names an emotion. It is useful information, but it does not describe the prediction or image.'),
    ('The image of being unable to speak.','An image can carry a prediction just as words can. Ask what Alex believed the image meant or would lead to.'),
    ('The fact that Alex attended the group.','Attending is behaviour. It may be relevant to the map, but it is not the image Alex described.')),
 [('Must an automatic thought be a sentence?','No. It can appear as an image, memory, or prediction. Ask what it means to the person.'),('What should you do if no thought is recalled?','Record what is known and leave uncertainty. Do not manufacture a thought or insist that every bodily reaction has a clear verbal cause.')],
 ('Lab: slow down one moment',['Use Jules’s poster story. Find the smallest specific moment at which the emotion changed.'],['What was happening just before the feeling shifted?','What words or image appeared?','What did that thought imply about Jules or the situation?','Which part is a feeling, and which part is a conclusion?','What practical issue still needs attention?'],
 'The date was pointed out; Jules pictured others shaking their heads; the meaning was “I cannot be relied on.” Shame is the feeling. Correcting the date remains useful.',
 'Use the character’s reported meaning. Avoid inferring a hidden belief without evidence.'),
 [('CCI: depression resources — automatic thoughts and ABC analysis',CCI+'Depression'),('NHS: reframing unhelpful thoughts',THOUGHTS)],
 'Thought monitoring is an introductory observation skill. It is not an instruction to monitor every thought or analyse distress indefinitely.')

add('interpretations',[
    'Jules sends Alex a message asking whether a drawing looks unfinished. Six hours pass without a reply. Jules thinks, “Alex is annoyed with me for asking,” and begins drafting an apology.',
    'There has been no argument. Alex sometimes replies late, but yesterday answered another question quickly. Jules feels hurt and uncertain. We have some relevant information and several missing pieces.'
],question('Choose a fair alternative','Which statement best preserves what Jules knows and does not know?',2,
    ('Alex definitely is not annoyed; everything is fine.','That is reassuring, but still claims access to Alex’s mind. A balanced thought should fit the evidence, including uncertainty.'),
    ('Six hours proves Alex is annoyed.','A delay is observable; the reason is not established. The conclusion is stronger than the available evidence.'),
    ('Alex has not replied. They may be busy or annoyed; I do not yet know why.','This recognises the delay and the uncertainty without demanding a positive conclusion. Jules can choose a practical next step.')),
 [lesson('Evidence is more than a feeling',[
    'A thought record separates the event, the thought, the feeling, evidence supporting the thought, evidence that complicates it, and a balanced response. The aim is a fair account, not winning an argument against yourself.',
    'Jules’s feeling is evidence that the situation matters to Jules. It is not direct evidence of Alex’s intention. A previous argument would be relevant evidence; imagining a frown is not an observed response. Evidence may support part of a thought without supporting its strongest version.'
 ],diagram('Separate the layers',('Observation','No reply for six hours'),('Interpretation','Alex is annoyed'),('Supporting facts','A reply came faster yesterday'),('Complicating facts','Late replies also happen'))),
 lesson('A balanced response can remain uncomfortable',[
    'A balanced response should be believable and specific. “I cannot know the reason from the delay alone” may fit better than “Nobody is ever annoyed with me.” It can include a coping statement: “If there is a disagreement, I can ask about it.”',
    'After reviewing the thought, Jules can choose whether an ordinary follow-up is needed. Repeatedly rewriting a record to reach certainty can become another loop. Set a reasonable stopping point and return to the activity you intended to do.'
 ],diagram('A short thought record',('Name','What am I predicting?'),('Check','What facts fit or complicate it?'),('Balance','What can I fairly conclude?'),('Act','What useful step fits now?')))],
 ('Jules writes a balanced response',[
    'Thought: “Alex is annoyed because I asked.” Supporting fact: Alex replied faster yesterday. Complicating facts: Alex has replied late before; there has been no conflict; Jules has no information about today’s schedule.',
    'Response: “The delay does not tell me why. If I need an answer by tomorrow, I can say when I need it.” Jules still feels some uncertainty. They decide to work on another part of the drawing instead of sending several apologetic messages.'
 ]),question('When the evidence changes','Alex later says, “I was irritated by the repeated requests, and I was busy.” How should Jules update the record?',0,
    ('Acknowledge the irritation and discuss a clearer way to ask, without turning it into “Alex rejects me.”','New evidence should change the account. A specific disagreement can call for communication without establishing a global judgment.'),
    ('Ignore the message because CBT means choosing the positive explanation.','A fair account must include unwelcome evidence. CBT skills should not require denying a real disagreement.'),
    ('Conclude that every future delayed reply means irritation.','One clarified event does not settle the meaning of every future delay. Context still matters.')),
 [('What makes a balanced thought different from reassurance?','It fits the available evidence and admits what is unknown. It does not guarantee the preferred outcome.'),('What if the difficult interpretation is partly supported?','Update it, keep the claim specific, and consider problem-solving or communication. A real problem does not justify every broader conclusion.')],
 ('Lab: write a short thought record',['Use Jules’s unanswered message. Write an initial response before looking at the example.'],['Specific event and initial thought','Feeling and optional intensity in your own terms','Facts supporting the thought','Facts that complicate it or remain unknown','A balanced response and a practical next step'],
 'No reply is certain; annoyance is possible but not established. A fair response admits uncertainty and includes an ordinary deadline-based follow-up if needed.',
 'Does the response acknowledge difficult possibilities? Does the next step serve a practical purpose rather than seek impossible certainty?'),
 [('NHS: reframing unhelpful thoughts',THOUGHTS),('CCI: depression resources — detective work and balanced thoughts',CCI+'Depression')],
 'Thought records are one CBT tool. They are not appropriate for resolving every difficulty, and a plausible alternative is not proof of what another person thinks.')

add('activity',[
    'Nia’s shifts have been tiring. She stops sketching after work and turns down a short walk with Jules. Rest helps on some evenings, but over two weeks her days contain fewer things she enjoys or values.',
    'Nia keeps thinking, “I will start again when I feel motivated.” The days become more empty, and starting feels harder. She wants to investigate this without treating exhaustion as a character flaw.'
],question('Make a manageable start','Which plan gives Nia the clearest, most realistic first experiment?',1,
    ('Fill every evening with activities so there is no time to feel low.','A crowded schedule may ignore exhaustion and be difficult to sustain. More activity is not automatically better.'),
    ('Try ten minutes of sketching after a suitable shift, with a smaller version if energy is low.','This specifies a meaningful activity and respects capacity. Nia can observe what follows without needing motivation to arrive first.'),
    ('Wait until she is certain the activity will improve her mood.','That certainty is unavailable beforehand. A small, feasible experiment can provide information.')),
 [lesson('Action can create an opportunity',[
    'Behavioural activation involves noticing patterns of activity and their consequences, then planning manageable actions that may restore contact with meaningful or rewarding parts of life. Motivation sometimes follows action; it does not always arrive first.',
    'Activities can offer connection, enjoyment, accomplishment, care, or rest. Those experiences may matter even if mood does not improve immediately. Activity planning must fit physical health, responsibilities, resources, and the person’s preferences.'
 ],diagram('A possible withdrawal cycle',('Low energy','Starting feels difficult'),('Withdraw','Cancel valued activities'),('Fewer opportunities','Less connection or satisfaction'),('Harder to begin','Wait for motivation'),kind='loop')),
 lesson('Plan an action you can actually observe',[
    '“Be more active” is vague. “After Tuesday’s early shift, put paper on the table and sketch for ten minutes” specifies a cue and a doable action. A two-minute version can help Nia start without making it an all-or-nothing test.',
    'Record what happened before drawing a conclusion. Did the task fit the available energy? Did it offer any interest or accomplishment? Did transport, pain, cost, or another barrier intervene? Review the plan rather than judging the person.'
 ],diagram('A plan that fits a real day',('Value','Make room for drawing'),('Cue','After an early shift'),('Action','Sketch for ten minutes'),('Adapt','Two minutes if needed')))],
 ('A mixed result is still information',[
    'Nia sketches for six minutes. Her mood does not noticeably change, but she enjoys choosing a colour and wants to finish the drawing another day. She also notices that she had planned it too close to a late shift.',
    'Nia keeps the activity, moves it to a more suitable evening, and protects rest after late shifts. The experiment supports a narrower conclusion than “drawing cures low mood”: a small creative activity can be feasible and worthwhile on some days.'
 ]),question('Review the plan fairly','Jules plans a walk but rain and a care commitment prevent it. What is the most useful review?',2,
    ('The plan proves Jules lacks commitment.','This converts practical barriers into a global judgment and provides little guidance for the next attempt.'),
    ('Double the length of tomorrow’s walk as compensation.','An automatic increase may make the next plan less feasible. There is no exercise debt to repay.'),
    ('Identify the barriers and choose a smaller or differently timed activity that serves the same purpose.','This treats the outcome as information. It preserves the purpose while adapting to circumstances.')),
 [('Why not wait for motivation every time?','A small planned action can create opportunities for interest or connection that waiting may not provide. It is an experiment, not a guarantee.'),('What counts as a useful outcome besides improved mood?','Feasibility, connection, satisfaction, accomplishment, or learning about barriers. Rest can also be a meaningful planned action.')],
 ('Lab: plan one meaningful activity',['Use Nia’s situation or an optional mild everyday example. Choose something affordable, accessible, and compatible with health and responsibilities.'],['What purpose would the activity serve?','What small action, when and where?','What is the smaller version?','What barrier might occur, and how could the plan adapt?','Afterwards: what happened and what will you change?'],
 'Nia chooses drawing for creativity, after an early shift, for ten minutes with a two-minute version. She reviews feasibility and interest as well as mood.',
 'The plan should fit the person’s actual resources. If low mood or fatigue is persistent or substantially affects daily life, consider support from a qualified professional rather than relying on this course.'),
 [('CCI: depression resources — behavioural strategies and activity scheduling',CCI+'Depression'),('NICE NG222: treatment options and individual needs','https://www.nice.org.uk/guidance/ng222/chapter/recommendations')],
 'Behavioural activation is an established treatment approach when delivered appropriately. This brief activity-planning exercise is introductory education; it is not an evaluated treatment programme.')

add('problem-solving',[
    'Alex has agreed to design a poster, update a signup list, and collect supplies before Saturday. There are only two free evenings. “What if everyone thinks I am unreliable?” keeps running through their mind.',
    'There is a practical capacity problem as well as a prediction about other people’s reactions. Arguing with the prediction will not create another evening. Alex needs to decide what can change.'
],question('Define the problem','Which problem statement is specific enough to work on?',0,
    ('Three tasks need doing before Saturday, and I have time for about two.','This identifies a current gap and makes possible solutions visible: change scope, timing, or who does the work.'),
    ('I am incapable of managing my life.','This global judgment does not identify a changeable task. It may be a thought worth examining separately.'),
    ('What if I disappoint everyone forever?','This predicts a broad future outcome. A useful immediate problem statement focuses on the current situation.')),
 [lesson('Separate a current problem from a hypothetical future',[
    'A practical problem has a present situation and some possible action. A hypothetical worry asks what might happen, often without a decision that can be made now. The same concern can contain both.',
    'Alex can estimate the work and contact the organiser. Alex cannot guarantee nobody will ever feel disappointed. Useful problem-solving addresses the actionable part, then leaves room for the uncertainty that remains.'
 ],diagram('Two questions need different responses',('Current problem','Three tasks; two evenings'),('Possible action','Agree priorities or share work'),('Hypothetical worry','Will everyone reject me?'),('Remaining uncertainty','No guarantee of every reaction'))),
 lesson('Generate options before choosing',[
    'Define the goal, list possible approaches, consider costs and feasibility, choose a step, and set a review point. Options can include asking for help, reducing scope, delaying a task, or deciding that a task is not needed.',
    'Problem-solving is not a demand to solve structural problems alone. Some situations require resources, specialist advice, or collective action. A useful step can be identifying who has the authority or support to help.'
 ],diagram('A practical problem-solving sequence',('Define','What needs to be different?'),('Options','What could change?'),('Choose','What is feasible and fair?'),('Review','When will we check?')))],
 ('Alex makes a decision with incomplete certainty',[
    'Alex estimates the poster at one evening, the list at half an evening, and the supplies trip at another. Options include a simpler poster, another volunteer collecting supplies, or a later deadline.',
    'Alex asks the organiser to prioritise. They agree on the simpler poster and share the collection task. Alex still worries about seeming difficult. The practical issue is better specified even though the feeling has not disappeared.'
 ]),question('Choose the next tool','Nia has sent a complete application and cannot change it before next week’s response. She keeps asking, “What if I am rejected?” What fits now?',1,
    ('Rewrite the unavailable application in her mind until she feels certain.','This cannot change the submitted application and may extend the loop without producing a decision.'),
    ('Check once whether a real next step is available, then practise returning attention while accepting the outcome is unknown.','This distinguishes useful preparation from repeated attempts to obtain certainty. A planned review point may help.'),
    ('Assume rejection is impossible because there is nothing more to do.','Lack of an action does not guarantee a preferred result. The skill is making room for uncertainty, not denying it.')),
 [('What makes a problem statement workable?','It identifies a specific current situation and a realistic goal, rather than judging the whole person.'),('Can a practical solution leave anxiety behind?','Yes. A useful action can address the situation while uncertainty or emotion remains. Feeling calm is not a prerequisite for every decision.')],
 ('Lab: choose a practical next step',['Use Alex’s three tasks. Keep the problem within the person’s influence while recognising where help is needed.'],['State the current problem without a character judgment','Describe a realistic goal','List at least three options','Compare effort, resources, consequences, and fairness','Choose a step, who will act, and a review point'],
 'Goal: have essential materials ready by Saturday within two evenings of available time. Options: simplify the poster, share collection, or renegotiate timing. Ask the organiser to agree priorities today.',
 'Check that your plan changes something observable. Identify what remains uncertain rather than adding more planning to chase a guarantee.'),
 [('CCI: worry and rumination — problem-solving',CCI+'Worry-and-Rumination'),('CCI: depression resources — problem solving',CCI+'Depression')],
 'Structured problem-solving is a general skill. Legal, financial, employment, or safeguarding problems may require qualified advice beyond the scope of an introductory course.')

add('experiments',[
    'Jules is unsure which paper size the group needs. “If I ask, the organiser will think I am incompetent,” they predict. Guessing would hide the uncertainty but might produce the wrong order.',
    'Jules wants to investigate the prediction in an ordinary, low-stakes interaction. The question needs to be clear enough that the result can teach them something.'
],question('Make the prediction observable','Which prediction can Jules actually investigate?',2,
    ('The organiser will secretly judge me.','A private judgment cannot be directly observed in this interaction. Choose indicators while recognising that they cannot reveal every hidden thought.'),
    ('Asking will feel completely comfortable.','This is a different prediction about Jules’s feelings. An experiment can still be useful while they feel anxious.'),
    ('If I ask one clear question, the organiser will refuse to answer or explicitly criticise me for asking.','This identifies observable responses. It is a narrower claim than knowing what the organiser privately thinks.')),
 [lesson('An experiment asks a question',[
    'A behavioural experiment compares a prediction with what happens after an action. Specify the situation, the prediction, what you will do, what you will observe, and how different outcomes could be interpreted.',
    'Choose an ordinary, ethical, low-stakes action. Do not manufacture conflict, put someone at risk, or use an experiment to test a dangerous situation. The aim is useful information rather than proving bravery or forcing a preferred result.'
 ],diagram('Before the experiment',('Prediction','One question will bring criticism'),('Action','Ask which paper size is needed'),('Observe','Words and actions in response'),('Interpret','What would each result mean?'))),
 lesson('Mixed outcomes need careful interpretation',[
    'The organiser might answer warmly, answer briefly, ask Jules to check the written instructions, or criticise the repeated question. Each result supports a different, limited conclusion.',
    'A brief answer does not prove warmth or hostility. One friendly interaction does not establish that criticism can never happen. If an awkward result occurs, examine what it shows about the specific situation and how Jules coped. Avoid turning one trial into a verdict on the person.'
 ],diagram('After the experiment',('Record','What actually happened?'),('Compare','What fitted the prediction?'),('Limit','What remains unknown?'),('Revise','What is the next useful question?')))],
 ('Jules gets a brief answer',[
    'Jules asks, “For Saturday’s drawings, should I order A3 or A4?” The organiser replies, “A3, thanks,” then returns to another task. No criticism occurs. Jules still feels tense.',
    'The observable prediction of refusal or explicit criticism was not supported in this trial. Jules cannot conclude that the organiser had no private judgment. They learn that asking a clear question was possible while anxious and obtained the information they needed.'
 ]),question('Review an awkward outcome','In another experiment, a colleague says, “Please check the instructions first next time.” What is the fairest conclusion?',0,
    ('The response identifies a specific expectation; examine whether it was reasonable and what to do next.','This accepts the actual feedback without generalising to “I am incompetent.” The experiment can inform a practical adjustment.'),
    ('The experiment failed, so there is nothing to learn.','An unwelcome result can still provide useful information about the situation, the prediction, and possible responses.'),
    ('This proves every request for clarification will be rejected.','One response cannot establish what every person will do in every context. Keep the conclusion at the scale of the evidence.')),
 [('Why specify an observable prediction?','It makes comparison possible and reduces the temptation to interpret any outcome as proof of a hidden judgment.'),('Does a useful experiment have to disconfirm the prediction?','No. Supporting or mixed evidence can inform an updated understanding, a practical change, or a different question.')],
 ('Lab: design a fair test',['Use Jules’s paper order. You can design the experiment without carrying it out. If choosing your own example, keep it ordinary, voluntary, and safe.'],['What specific prediction will you investigate?','What action, setting, and time?','What observations would support or complicate the prediction?','What could make the result hard to interpret?','What happened, what remains unknown, and what would you revise?'],
 'Ask one clear paper-size question. Record the actual reply. A brief useful answer without explicit criticism complicates the predicted refusal, but does not reveal private thoughts.',
 'Check that the test can teach something even if the result is mixed. Feelings matter, but they are not the only outcome measure.'),
 [('CCI: social anxiety — behavioural experiments',CCI+'Social-Anxiety'),('CCI: perfectionism — testing beliefs',CCI+'Perfectionism')],
 'Behavioural experiments are used across CBT approaches. This lesson illustrates the reasoning process; individual experiments may need adaptation and professional guidance.')

add('approach',[
    'Alex wants to talk to new people at the drawing group. They arrive late, look busy with their phone, and leave before the break. This lowers the immediate chance of an awkward greeting, but also limits the conversations they want.',
    'Alex does not want to deliver a speech. They want a manageable way to practise an ordinary greeting in a group they have chosen to attend.'
],question('Choose a first step','Which first step best fits Alex’s stated goal and current confidence?',1,
    ('Give an unprepared speech to everyone immediately.','A much larger task may not fit the goal or readiness. A useful step can be small and agreed voluntarily.'),
    ('Arrive at the usual time and say hello to one familiar person, then review the experience.','This creates a manageable opportunity for learning and connection. It can be adjusted if it does not fit.'),
    ('Keep avoiding the break until all anxiety has disappeared.','Waiting for no anxiety may leave the same avoidance pattern in place. Alex can consider a manageable step with some discomfort.')),
 [lesson('Avoidance changes what you can learn',[
    'Avoidance can bring short-term relief while reducing opportunities to discover how a situation unfolds or how a person can cope. This is one reason gradual approach is used in CBT for some fears.',
    'Avoiding actual danger can be sensible. A safe everyday social situation is different from harassment, unsafe conditions, or an activity that conflicts with medical advice. Choose the context carefully and keep the person in control.'
 ],diagram('A voluntary approach ladder',('Step 1','Greet a familiar member'),('Step 2','Ask a familiar member a question'),('Step 3','Greet a new member'),('Step 4','Join a short break-time chat'),kind='ladder')),
 lesson('Review learning, not a courage score',[
    'A ladder divides a chosen goal into steps that differ in difficulty. The order is personal, not a ranking imposed by someone else. Repeating, adjusting, or seeking support can be appropriate.',
    'Safety behaviours are actions intended to prevent a feared outcome that may also make it harder to discover what happens without them. Hiding behind a phone may serve that function for Alex. Disability aids, necessary accommodations, and genuine safety precautions should not be removed on that basis. Ask about the function before making changes.'
 ],diagram('What is this action doing?',('Phone as cover','Avoid a possible greeting'),('Useful support','Make participation accessible'),('Question','Does it prevent useful learning?'),('Choice','Adjust only what fits safely')))],
 ('Alex tries one greeting',[
    'Alex chooses to greet a familiar member at the start. Their voice feels shaky. The member says hello and asks about the drawing. Alex stays for two minutes, then returns to their materials.',
    'Alex records that greeting was possible with some anxiety and led to a brief exchange. They decide to repeat the same step once more before considering a new one. They do not need to report zero anxiety or reach the top of a ladder on a fixed schedule.'
 ]),question('Keep the context in view','Nia avoids a group where someone has repeatedly harassed her. What is the most appropriate starting point?',2,
    ('Use the same approach ladder because all avoidance maintains fear.','This ignores evidence of real harm. A general model must not override the actual circumstances.'),
    ('Remove every source of support so the experiment is pure.','Support and accommodations can protect access and safety. Removing them indiscriminately is not a useful learning goal.'),
    ('Consider safety, boundaries, and appropriate support before any decision about returning.','A real threat calls for a contextual response. Nia does not owe the group an exposure exercise.')),
 [('Why can avoidance maintain a fear?','It may reduce immediate discomfort while limiting opportunities to test predictions or learn how to cope.'),('How is an accommodation different from a safety behaviour?','An accommodation may provide necessary access or protection. Function and context matter; the same outward action cannot be classified from appearance alone.')],
 ('Lab: build a voluntary ladder',['Use Alex’s ordinary greeting goal. Designing a fictional ladder is enough. Do not use this exercise for dangerous situations, trauma memories, or severe symptoms without appropriate professional support.'],['What chosen goal would the steps serve?','What is a manageable first step?','What two or three later steps might fit?','Which supports or accommodations should remain?','What learning would you review, and how could you adjust the pace?'],
 'Alex starts with a familiar greeting, later adds a question, and eventually considers a new member. Review observed responses and coping, not whether anxiety vanished.',
 'Each step should remain voluntary and fit the person’s context. A harder step is not automatically a better one.'),
 [('NHS: facing your fears','https://www.nhs.uk/every-mind-matters/mental-wellbeing-tips/self-help-cbt-techniques/facing-your-fears/'),('CCI: social anxiety — avoidance, stepladders, and safety behaviours',CCI+'Social-Anxiety')],
 'This chapter introduces gradual approach in safe everyday situations. It is not an exposure protocol for a diagnosed condition and does not replace individual assessment.')

add('thinking-loops',[
    'After the drawing group, Nia remembers a joke that received little response. She replays it on the bus, at dinner, and while preparing for bed. Each replay asks, “Why did I say that?” but produces no new information.',
    'Nia would like to learn from social mistakes. She also notices that tonight’s analysis is taking time away from rest without reaching a decision.'
],question('Reflection or repetition?','Which question best distinguishes useful reflection from a thinking loop?',0,
    ('Is this producing new information or a specific decision I can act on?','This looks at the function of the thinking. A repeated question without new information may call for a different response.'),
    ('Have I thought about it for exactly the right number of minutes?','Time can be a clue, but there is no universal minute limit that separates helpful and unhelpful thinking.'),
    ('Can I force myself never to think about it again?','Trying to eliminate a thought can create another struggle. The skill is choosing how to respond when it appears.')),
 [lesson('Thinking can become an activity of its own',[
    'Worry often concerns what might happen; rumination often returns to what happened or what it means about oneself. They can overlap. The useful question is whether the thinking helps a decision or keeps circling without one.',
    'A difficult thought returning does not mean the person chose it or failed. Notice its arrival, name the process gently, and consider whether something useful can be done. If there is a practical issue, use a defined problem-solving step.'
 ],diagram('A loop without new information',('Memory','A quiet response to the joke'),('Question','Why am I like this?'),('Replay','Review the same scene'),('Consequence','Less rest; no new facts'),kind='loop')),
 lesson('Return attention without demanding an empty mind',[
    'Nia can acknowledge, “That conversation is back in my mind,” check whether an action is needed, and deliberately return attention to a chosen activity. The thought may remain in the background. The aim is flexible attention rather than thought suppression.',
    'Choose something concrete: notice the feel of a brush, follow a paragraph, or listen to a person speaking. When attention wanders, return again without treating it as a test. If a real repair is needed, decide on one proportionate action rather than rehearsing indefinitely.'
 ],diagram('A different response to the replay',('Notice','The conversation is replaying'),('Check','Is there a useful action?'),('Choose','Act once, or leave it unresolved'),('Return','Attend to the present task')))],
 ('Nia makes one useful distinction',[
    'Nia asks whether the joke contained a hurtful remark that needs an apology. She remembers no such content and has no new information about the quiet response. She writes one brief note to listen more carefully at the next group, then returns to dinner.',
    'The memory returns twice. Nia notices it and returns to the conversation at the table. The exercise is not disproved by the thought returning. The relevant observation is whether Nia can re-engage with the activity she chose.'
 ]),question('When there is an actionable concern','Jules realises they made a specific hurtful remark. Which response fits?',1,
    ('Label every concern as rumination and ignore it.','That could bypass a real responsibility. Distinguish an actionable issue from repetition about the whole self.'),
    ('Decide on a proportionate apology, then notice and redirect repeated self-condemnation.','A practical repair and flexible attention can both be useful. Neither requires a guarantee about the other person’s response.'),
    ('Keep replaying until no shame remains before acting.','Waiting for a feeling to disappear can delay a reasonable action and keep the loop going.')),
 [('How can you distinguish reflection from rumination?','Ask whether the thinking produces new information, a concrete decision, or useful learning. Repeated abstract self-judgment often does not.'),('What if a thought returns after redirecting attention?','Notice it and return again. The goal is flexible engagement, not proving that a thought can never appear.')],
 ('Lab: notice, decide, return',['Use Nia’s joke example or a mild everyday replay. You may stop or use the fictional story if personal reflection becomes uncomfortable.'],['What is the repeated question?','Is there new information or a practical action?','If needed, what one proportionate step fits?','What present activity will receive attention?','What happened when the thought returned?'],
 'Nia identifies a repeated self-judgment without new facts, chooses one listening intention, and returns to dinner. The thought can return without requiring another full analysis.',
 'Check that redirecting attention does not bypass an important practical problem. Avoid judging success by whether the mind stayed blank.'),
 [('CCI: worry and rumination — attention training and uncertainty',CCI+'Worry-and-Rumination')],
 'Attention practices can be useful, but persistent or intrusive thinking may require tailored support. This lesson does not establish the cause of any individual’s repetitive thoughts.')

add('rules',[
    'Jules agrees to bring extra materials, design another poster, and cover a session despite a full week. “If I disappoint someone, I am selfish,” they think. Resentment builds, and they eventually cancel at the last minute.',
    'The same rule appears in several situations. It may once have helped Jules stay connected or avoid conflict. Now its rigid form seems to make honest planning harder.'
],question('Identify the rule','Which statement is a conditional personal rule rather than a specific event or emotion?',2,
    ('Jules agreed to bring extra paper.','This describes an action. A rule would express a broader demand or an if-then assumption.'),
    ('Jules feels resentful.','This names a feeling. It may signal an unmet need, but it is not itself the underlying rule.'),
    ('If I disappoint anyone, it means I am selfish.','This links an event to a broad conclusion about identity. It is a candidate rule to investigate, not a fact to accept.')),
 [lesson('Thoughts can reflect broader assumptions',[
    'An automatic thought belongs to a moment: “I cannot say no to this request.” A conditional assumption expresses a rule: “If I refuse, I will lose people.” A core belief is a broader view of self, others, or the world, such as “I am not worth caring about.”',
    'These are different levels of a possible formulation. Do not assume a core belief simply because a behaviour repeats. Ask the person what the situation means, look for patterns, and remain open to context and alternative explanations.'
 ],diagram('Three levels of a possible pattern',('Moment','I cannot refuse this request'),('Rule','If I refuse, I will lose people'),('Broad belief','My needs do not matter'),('Working hypothesis','Check with the person'))),
 lesson('Make a rule more flexible and test it',[
    'A flexible rule keeps a value without turning it into an impossible demand. Jules values reliability. “I can be considerate and honest about capacity” allows planning, negotiation, and occasional disappointment.',
    'A new sentence does not automatically change a long-standing belief. Look for small experiences that fit or challenge it, and practise acting consistently with it. Some beliefs are connected to difficult histories that deserve more support than a short self-study exercise.'
 ],diagram('Keep the value; soften the demand',('Value','Be considerate and reliable'),('Rigid demand','Never disappoint anyone'),('Flexible guide','Be honest about capacity'),('Small action','Offer what is feasible')))],
 ('Jules tries a different response',[
    'Jules replies, “I can bring the paper, but I cannot cover the session this week.” The organiser finds another volunteer. Jules feels guilty at first, but keeps their feasible commitment.',
    'This experience supports a more flexible possibility: setting one limit can coexist with being helpful. It does not guarantee every person will welcome a boundary. Jules can examine an unfavourable response without deciding their needs are illegitimate.'
 ]),question('Avoid over-interpreting behaviour','Alex hesitates before accepting an invitation. Can you conclude Alex has the core belief “I am unwanted”?',0,
    ('No. Ask what the hesitation means; tiredness, logistics, preference, or several beliefs could fit.','The outward behaviour does not uniquely identify a hidden belief. A formulation needs the person’s own account and context.'),
    ('Yes. Hesitation is enough to reveal the belief.','That assigns a private meaning without evidence and can miss practical explanations.'),
    ('No beliefs can ever influence behaviour.','Beliefs may influence behaviour, but recognising that possibility is different from knowing which belief is present.')),
 [('How does a rule differ from a momentary thought?','A rule applies across situations, often as a should, must, or if-then statement. A thought occurs in a particular moment.'),('What makes a more flexible rule useful?','It is believable, preserves an important value, allows context and limits, and suggests an action that can be tested.')],
 ('Lab: turn a demand into a guide',['Use Jules’s commitments. You can work entirely with this fictional example.'],['What repeated should, must, or if-then rule appears?','What value or need might it be trying to protect?','What are its benefits and costs in this situation?','What more flexible guide fits the evidence?','What small action could test it, and what would you review?'],
 'Rule: never disappoint anyone. Value: care and reliability. Flexible guide: be considerate and honest about capacity. Test: accept one feasible task and decline another respectfully.',
 'A flexible guide should not become another absolute demand to perform perfectly. Leave room for mixed reactions and learning.'),
 [('CCI: depression resources — core beliefs',CCI+'Depression'),('CCI: perfectionism — rules and assumptions',CCI+'Perfectionism'),('CCI: assertiveness',CCI+'Assertiveness')],
 'Core beliefs and assumptions are formulation concepts, not labels to impose on someone. Deeply distressing beliefs may be better explored with a qualified practitioner.')

add('context',[
    'At work, Nia is repeatedly assigned unpopular late shifts despite an agreed rotation. When she asks about it, her manager dismisses the concern. Nia thinks, “I am powerless, so there is no point speaking up.”',
    'The rota provides evidence of a real imbalance. At the same time, “there is no possible action” is a broader conclusion. Nia needs an approach that respects the actual working conditions and the possible costs of challenging them.'
],question('Choose the starting point','What should happen before asking Nia to reinterpret the situation more positively?',1,
    ('Assume the manager must have a good reason.','That invents a reassuring explanation and can minimise the documented imbalance.'),
    ('Acknowledge the evidence and explore Nia’s priorities, safety, support, and practical options.','This keeps the real circumstances central. It also allows specific thoughts to be examined without denying unfairness.'),
    ('Tell Nia that feeling powerless proves she has no choices.','The feeling is understandable but does not by itself establish every possible option. Options may still be limited and costly.')),
 [lesson('Match the tool to the situation',[
    'Different parts of a situation may call for different responses. Check an interpretation when evidence is ambiguous. Use problem-solving for a changeable task. Consider boundaries, support, or appropriate advice for a real interpersonal or structural problem.',
    'CBT skills do not require accepting mistreatment or taking responsibility for another person’s actions. Emotional responses can be understandable signals. A useful formulation includes the environment, power, access to resources, and the costs of each option.'
 ],diagram('Choose a response that fits',('Ambiguous meaning','Examine the interpretation'),('Practical obstacle','Define and solve a problem'),('Unfair treatment','Consider boundaries and support'),('Uncontrollable outcome','Make room for uncertainty'),kind='columns')),
 lesson('Agency can be partial',[
    'Nia may not control the manager’s response. She might control whether to keep a record, consult a trusted representative, request a meeting, or seek other advice. None of those options is automatically safe or available in every workplace.',
    'A specific alternative to “I am powerless” could be “My options are constrained; I can find out what support exists before deciding.” This preserves the constraints and identifies a possible next step. It is not a promise that speaking up will fix the situation.'
 ],diagram('Keep three things separate',('Known facts','The rota departs from the agreement'),('Unknown outcomes','How a challenge will be received'),('Possible influence','Gather information and support'),('Limits','Nia cannot control the manager')))],
 ('A plan with context',[
    'Nia checks the rota and the written agreement, then privately asks a trusted staff representative about options. She considers potential consequences before deciding whether to make a formal request.',
    'Nia also notices the thought “If this is happening, I must deserve it.” The rota does not support that conclusion. Challenging self-blame and addressing the working conditions can proceed together.'
 ]),question('A mixed situation','Jules receives fair criticism about a missed deadline and also a personal insult. Which response best fits?',2,
    ('Reject all feedback because the insult makes every criticism false.','The insult is inappropriate, but the deadline issue may still need a practical response. Separate the claims.'),
    ('Accept the insult as proof that the criticism is accurate.','A personal attack is not established by a specific missed commitment. Keep behaviour, evidence, and identity separate.'),
    ('Address the missed deadline and consider a boundary or support about the insult.','This distinguishes a practical responsibility from unacceptable treatment. Several tools may fit different parts of the same event.')),
 [('Why include the environment in a CBT formulation?','Real demands, resources, discrimination, power, and support affect experiences and options. A thought-only account can miss important causes and constraints.'),('Can checking self-blame and seeking practical support happen together?','Yes. Examining an unsupported personal conclusion does not require denying a real problem or delaying appropriate support.')],
 ('Lab: choose the tool, explain the fit',['Use Nia’s rota example. Consider several responses rather than assuming one tool must solve everything.'],['What facts indicate a real problem?','What interpretation goes beyond those facts?','Which parts are within Nia’s influence?','What practical support or advice might be appropriate?','What first step fits Nia’s priorities and possible risks?'],
 'The rota supports an imbalance, not the conclusion that Nia deserves it. Gathering records and privately checking available support may be a first step, subject to her circumstances.',
 'Does the plan respect actual constraints? Do not treat a person’s inability to change a structural problem as a failure to use CBT.'),
 [('CCI: assertiveness — communication and boundaries',CCI+'Assertiveness'),('NHS: what CBT involves',NHS)],
 'The fictional workplace example teaches tool selection, not employment advice. Practical and professional support may be essential; no outcome is guaranteed.')

add('continuing',[
    'Several weeks later, Alex has used clearer checking standards and small social steps. Then a busy week disrupts sleep and routines. Alex notices the signup list being checked repeatedly again.',
    '“I am back at the beginning,” they think. But Alex now notices the pattern earlier, can explain part of the loop, and knows a response that has helped before. A returning difficulty and losing all learning are not the same event.'
],question('Read the setback carefully','Which conclusion best fits the information?',0,
    ('The pattern has returned under strain; Alex can use what they have learned and reassess what support is needed.','This acknowledges the difficulty without erasing previous learning. The next step can be specific and manageable.'),
    ('Any returning worry proves the course has failed.','A single recurrence does not establish that no learning occurred. This course is not a treatment with a promised symptom outcome.'),
    ('Ignore the checking because progress means nothing can go wrong now.','That dismisses new information. A useful maintenance plan includes noticing and responding to changes.')),
 [lesson('Make a personal learning summary',[
    'A maintenance plan records what you have learned about a pattern, early signs that it is intensifying, small responses that fit, and sources of support. It should be short enough to use when things are difficult.',
    'Alex’s early signs include repeated checks without new information, missed breaks, and the thought “I must be completely certain.” Their first response might be to revisit the agreed checking standard, simplify an overloaded day, and speak to someone supportive.'
 ],diagram('A usable maintenance plan',('Notice','My early warning signs'),('Respond','One familiar, feasible skill'),('Review','What changed; what is needed?'),('Support','Who or what can help?'))),
 lesson('Review patterns without turning life into a test',[
    'Progress can include noticing earlier, choosing a more workable action, asking for support, or recovering from a difficult day more flexibly. A course score or streak cannot capture all of that.',
    'Plan a brief revisit after using a skill and another at a useful later point. Adjust the timing to your circumstances. If difficulties persist, worsen, or substantially affect daily life, consider support from a qualified professional. You do not have to complete more exercises before asking.'
 ],diagram('Respond to a difficult week',('Describe','What has changed?'),('Scale down','What is feasible today?'),('Use learning','Which skill fits this pattern?'),('Seek support','What help is needed now?')))],
 ('Alex’s one-page plan',[
    'Pattern: doubt followed by extra checking and short relief. Early signs: three returns to an unchanged list and a skipped break. First steps: check the actual task standard, pause the extra work, and review the week’s capacity.',
    'Support: ask the organiser to clarify priorities; contact a qualified practitioner if the pattern becomes persistent or substantially disruptive. Review: after the next ordinary task, record what happened and update the plan. The plan guides a response; it does not promise that doubt will disappear.'
 ]),question('Bring the skills together','After a stressful week, Nia has less energy and starts replaying a conversation. What is the best next step?',1,
    ('Complete every worksheet immediately to catch up.','An overloaded response may ignore current capacity. Choose the tool that fits the immediate pattern.'),
    ('Map the current situation, choose one feasible response, and consider whether more support is needed.','This combines observation, tool selection, and context. It does not require starting the entire course again.'),
    ('Use thought challenging for every feeling regardless of the cause.','Different problems call for different responses. Rest, practical help, or attention shifting may fit better.')),
 [('What should a maintenance plan contain?','A short description of the pattern, early signs, feasible responses, a review point, and sources of support.'),('What can show learning even when a difficulty returns?','Earlier recognition, more specific understanding, a more flexible action, or seeking useful support. Absence of all difficult feelings is not the standard.')],
 ('Lab: a plan for the next difficult week',['Use Alex’s pattern, or create an optional personal summary. Keep it brief and realistic. Then try the final case to practise choosing tools without a chapter label.'],['What pattern and trigger do you want to recognise?','What two early signs are observable?','What small first response has a clear purpose?','Who or what could provide support?','When will you review, and what would tell you more help is needed?'],
 'Alex notices repeated checks and missed breaks, revisits the task standard, reviews capacity, and seeks support if disruption persists. They review after the next ordinary task.',
 'Use this as a flexible guide. A return of difficulty is information, not a moral failure or a requirement to cope alone.'),
 [('CCI: depression resources — self management',CCI+'Depression'),('CCI: worry and rumination — self management plan',CCI+'Worry-and-Rumination'),('NHS: cognitive behavioural therapy',NHS)],
 'Maintenance planning supports continuing learning. This course has not been tested for prevention of relapse or for clinical outcomes; recurrent symptoms deserve appropriate assessment and support.')

course['cases']=[
 {'id':'case-pattern','title':'Checkpoint 1: the unread invitation','after':4,
  'story':['Rowan receives an invitation to a community book group. They think, “I will have nothing useful to say,” feel tense, and leave it unanswered. Not replying brings relief that evening. A week later Rowan feels more isolated and believes they would not fit in.'],
  'tasks':[('Map the moment','Separate the event, thought, emotion, body information, and behaviour. What is missing?','Event: invitation. Thought: nothing useful to say. Feeling: tension or anxiety; bodily sensations were not specified. Behaviour: no reply. Ask rather than invent the missing bodily details.'),('Explain a possible cycle','How might the short-term consequence relate to what happens later?','Avoiding the reply brings relief but prevents new information and a possible connection. Later isolation may strengthen the initial prediction. This is a hypothesis, not proof of the only cause.'),('Write a balanced account','What can Rowan fairly conclude from the available facts?','The invitation does not establish how a visit would go. Rowan can acknowledge uncertainty and consider a small information-gathering step if participation fits their interests.')],
  'rubric':['Event and interpretation are separate.','The cycle includes immediate and later consequences.','Missing information stays open rather than being invented.']},
 {'id':'case-experiment','title':'Checkpoint 2: asking at the library','after':8,
  'story':['Rowan wants to ask a librarian whether a beginner book group is suitable. They predict, “The librarian will laugh or say my question is stupid.” Rowan usually asks a friend to speak for them. The library is an ordinary setting they have safely visited before.'],
  'tasks':[('Design the experiment','Specify one action and observable outcomes. What support should remain?','Rowan could choose to ask one clear suitability question. Observe words and actions, not hidden opinions. Preserve any communication accommodations; consider voluntarily changing only the friend speaking on their behalf if that fits Rowan’s needs.'),('Interpret a brief response','The librarian says, “Yes, beginners are welcome,” then turns to another visitor. What follows?','The predicted explicit ridicule did not occur in this trial. A brief answer does not establish a private opinion. Rowan obtained information while possibly still anxious.'),('Interpret an awkward response','Instead the librarian says, “It is on the sign.” How would your conclusion change?','This may be unhelpful or brusque, but it is not identical to explicit ridicule. Note the exact response, consider its limits, and decide whether another source of information or a different next step is useful.')],
  'rubric':['The prediction is observable.','Support and access needs are respected.','Both favourable and awkward results permit specific learning.']},
 {'id':'case-final','title':'Final case: the first book-group session','after':12,
  'story':['Rowan attends the group and answers one question briefly. Another participant interrupts twice. Afterwards the organiser thanks Rowan for coming. At home Rowan thinks, “Nobody wants me there,” replays the interruptions, and decides never to return.','Rowan also has a genuine scheduling problem: the next meeting overlaps a regular care commitment. They feel tired and have stopped a short reading routine they used to enjoy.','New information arrives: the organiser says interruptions have affected other participants too and proposes a turn-taking format. The organiser cannot change the next meeting’s time.'],
  'tasks':[('Map without mind-reading','Separate observations, interpretations, feelings, actions, and unknowns.','Observations include two interruptions and thanks from the organiser. “Nobody wants me” is broader than the evidence. Fatigue is reported; ask about other bodily and emotional experiences rather than inventing them.'),('Identify a possible loop','What might withdrawal and repeated analysis accomplish now and cost later?','Withdrawal may offer relief while limiting connection and new information. Replaying without new facts may take time from rest. Neither explanation removes the real interruptions or care commitment.'),('Choose tools that fit','Select responses for the interpretation, interruptions, scheduling, and reduced activity.','Examine the global rejection thought; consider a boundary or organiser support about interruptions; problem-solve the scheduling constraint; consider a manageable reading activity if Rowan values it. Do not treat every issue as a thinking error.'),('Design one small experiment','Choose a voluntary action with an observable prediction and an interpretation plan.','If Rowan wants to return and timing permits, they might try one short contribution under the turn-taking format and observe whether they finish. Success is not guaranteed; keeping participation accessible and respecting care responsibilities matters.'),('Update with new information','What should change after the organiser’s message?','The interruption pattern affecting others complicates the personal-rejection account and supports a practical format issue. The scheduling problem remains real. Rowan need not deny either fact.'),('Plan for a difficult week','Write an early sign, one feasible response, and a source of support.','An early sign could be repeated replay replacing rest. A response could be one practical decision and a return to a chosen activity. Support might include a trusted person or professional help if difficulties persist or substantially interfere.')],
  'rubric':['Reasoning stays specific to the evidence.','Several tools are matched to distinct problems.','The experiment is voluntary, safe, and observable.','New facts revise the account.','The maintenance plan recognises capacity and support.']}
]
course.update({'title':'Everyday CBT','version':'0.1.0','status':'Draft course · practitioner review pending','reviewed':'2026-11-13','scope':'Introductory CBT skills education for adults. Not diagnosis, individual treatment, or professional clinical training. No practitioner review or learner pilot has taken place.','characters':[{'name':'Alex','description':'A volunteer who wants to contribute without getting trapped in repeated checking.'},{'name':'Nia','description':'A shift worker making room for creativity, rest, and fair treatment.'},{'name':'Jules','description':'A drawing-group member practising clearer requests and realistic commitments.'}]})
for number,c in enumerate(course['chapters'],1):
    assert 'pages' in c,c['slug']
    for i,page in enumerate(c['pages'],1):page['id']=f'c{number:02d}p{i:02d}'
(ROOT/'course.json').write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n')
print(f"Authored {len(course['chapters'])} chapters, {sum(len(c['pages']) for c in course['chapters'])} lesson pages, and {len(course['cases'])} cases")
