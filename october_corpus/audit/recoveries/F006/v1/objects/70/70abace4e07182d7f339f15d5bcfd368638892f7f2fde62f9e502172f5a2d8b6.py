from pathlib import Path
import argparse,subprocess,json,hashlib,time
p=argparse.ArgumentParser();p.add_argument('--model',choices=['F4','H4','E6','E7','E8'],required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=int,default=1800);a=p.parse_args()
R=Path(__file__).resolve().parent;a.out.mkdir(exist_ok=False,parents=True)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=[{'path':n,'sha256':h(R/n)}for n in ['enumerate_inner_progress.g',a.model+'_model.g',a.model+'_model.json','build_models.py','run_inner_progress.py']]
cmd=['/opt/homebrew/bin/gap','-q','-b','-c','modelFile:="'+a.model+'_model.g";Read("enumerate_inner_progress.g");']
with (a.out/'stdout.log').open('wb')as out,(a.out/'stderr.log').open('wb')as err:
    t=time.monotonic();proc=subprocess.Popen(cmd,cwd=R,stdout=out,stderr=err);(a.out/'pid').write_text(str(proc.pid)+'\n')
    try:rc=proc.wait(timeout=a.seconds);status='EXITED'
    except subprocess.TimeoutExpired:proc.kill();proc.wait();rc=None;status='TIMEOUT_NO_CERTIFICATE'
data=(a.out/'stdout.log').read_bytes()
r={'status':status,'returncode':rc,'seconds':time.monotonic()-t,'complete_marker':b'COMPLETE_EXHAUSTION' in data,'pins':pins,'model':a.model,'command':cmd,'unchanged':all(h(R/x['path'])==x['sha256']for x in pins),'whole_original_credit':0,'distinct_review_pending':True}
(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
