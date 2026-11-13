"""Full lesson narration; teaching summaries are separate, and hidden answers stay unspoken."""
def spoken(page):
    parts=[page['title'],*page['paragraphs']]
    if page.get('diagram'):
        parts.append(page['diagram']['title'])
        parts.extend(x['label']+'. '+x['detail'] for x in page['diagram']['items'])
    if page['type']=='decision':
        parts.extend(f"Option {letter}. {o['text']}" for letter,o in zip('ABC',page['options']))
        parts.append('Pause here to choose, then check the feedback for your choice.')
    if page['type']=='recall':
        parts.extend(f"Question {i}. {q['prompt']}" for i,q in enumerate(page['questions'],1))
        parts.append('Pause to explain your reasoning before revealing the suggested answers.')
    if page['type']=='lab':
        parts.extend(f"Step {i}. {field}" for i,field in enumerate(page['fields'],1))
        parts.append(page['review'])
        parts.append('Pause here for the lab. You can use the fictional example throughout.')
    return '\n\n'.join(parts)
