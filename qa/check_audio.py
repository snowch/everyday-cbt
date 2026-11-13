"""Verify script hashes, decode every recording, and reject silent/truncated files."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.narration_text import spoken
course=json.loads((ROOT/'course.json').read_text())
manifest=json.loads((ROOT/'audio/manifest.json').read_text())
text={p['id']:spoken(p) for c in course['chapters'] for p in c['pages']}
assert len(manifest['clips'])==96 and set(text)=={r['id'] for r in manifest['clips']}
seconds=0
for record in manifest['clips']:
    path=ROOT/record['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
    assert hashlib.sha256(text[record['id']].encode()).hexdigest()==record['text_sha256']
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','s16le','-ac','1','-ar','24000','-'])
    import array
    samples=array.array('h');samples.frombytes(raw)
    assert len(samples)>24000*3,path
    assert max(abs(x) for x in samples)>1000,path
    duration=len(samples)/24000
    assert abs(duration-record['seconds'])<.2,path
    words=len(text[record['id']].split())
    assert 60<words/duration*60<260,(path,words/duration*60)
    seconds+=duration
print(json.dumps({'clips':96,'decoded':96,'minutes':round(seconds/60,1),'silent_files':0,'script_hashes':'match','encoded_hashes':'match','review_limit':'Technical checks only; no ASR screen or human listening review.'},indent=2))
