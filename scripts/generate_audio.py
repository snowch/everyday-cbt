"""Generate recorded Kokoro af_heart narration. Run in an audio-production venv."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from narration_text import spoken
ROOT=Path(__file__).resolve().parents[1]

def render(task):
    key,text,models,working=task
    import numpy as np
    import soundfile as sf
    import onnxruntime as ort
    from kokoro_onnx import Kokoro
    global ENGINE
    if 'ENGINE' not in globals():
        options=ort.SessionOptions()
        options.intra_op_num_threads=2
        options.inter_op_num_threads=1
        session=ort.InferenceSession(str(Path(models)/'kokoro-v1.0.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
        ENGINE=Kokoro.from_session(session,str(Path(models)/'voices-v1.0.bin'))
    target=ROOT/'audio/clips'/f'{key}.m4a'
    fingerprint=hashlib.sha256(text.encode()).hexdigest()
    marker=Path(working)/f'{key}.json'
    if target.exists() and marker.exists() and json.loads(marker.read_text())['text_sha256']==fingerprint:
        return json.loads(marker.read_text())
    blocks=[]
    for paragraph in text.split('\n\n'):
        samples,rate=ENGINE.create(paragraph.replace('CBT','C B T'),voice='af_heart',speed=1.0,lang='en-us')
        blocks.extend([samples,np.zeros(int(rate*.45),dtype=np.float32)])
    wav=Path(working)/f'{key}.wav'
    sf.write(wav,np.concatenate(blocks),rate)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ac','1','-ar','24000','-c:a','aac','-b:a','96k',str(target)],check=True)
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(target)]))
    record={'id':key,'file':f'audio/clips/{key}.m4a','text_sha256':fingerprint,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'seconds':round(duration,3)}
    marker.write_text(json.dumps(record))
    print(f'{key}: {duration:.1f}s',flush=True)
    return record

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--models',required=True)
    parser.add_argument('--working',required=True)
    parser.add_argument('--workers',type=int,default=2)
    args=parser.parse_args()
    models=Path(args.models)
    hashes={'kokoro-v1.0.onnx':'beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a','voices-v1.0.bin':'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d'}
    for name,sha in hashes.items():assert hashlib.sha256((models/name).read_bytes()).hexdigest()==sha,name
    Path(args.working).mkdir(parents=True,exist_ok=True)
    (ROOT/'audio/clips').mkdir(parents=True,exist_ok=True)
    course=json.loads((ROOT/'course.json').read_text())
    tasks=[(p['id'],spoken(p),args.models,args.working) for c in course['chapters'] for p in c['pages']]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:records=list(pool.map(render,tasks))
    (ROOT/'audio/manifest.json').write_text(json.dumps({'voice':'af_heart','speed':1.0,'clips':records},indent=2)+'\n')
    provenance={'engine':'Kokoro-82M v1.0 via kokoro-onnx 0.6.1','voice':'af_heart','speed':1.0,'model_release':'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/','model_sha256':hashes,'clip_count':len(records),'seconds':round(sum(r['seconds'] for r in records),1),'review':'Generated from visible lesson text. Technical decoding checks only; no independent ASR screen or human listening review. Hidden feedback, recall answers, and worked lab suggestions are text-only.'}
    (ROOT/'production/narration.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print('Finished',len(records),'clips',flush=True)
