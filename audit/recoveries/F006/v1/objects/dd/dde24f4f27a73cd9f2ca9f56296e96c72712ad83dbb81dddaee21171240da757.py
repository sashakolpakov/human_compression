from pathlib import Path
import argparse,hashlib,json,subprocess,time
p=argparse.ArgumentParser()
p.add_argument('--model',choices=['Test','E6','E7','E8','Co3','D8'],required=True)
p.add_argument('--out',type=Path,required=True)
p.add_argument('--seconds',type=int,default=1800)
a=p.parse_args();W=Path(__file__).resolve().parent
a.out.mkdir(parents=True,exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pins=[{'path':n,'sha256':sha(W/n)}for n in ['enumerate.g',a.model+'_model.g','run.py']]
cmd=['/opt/homebrew/bin/gap','-q','-b','-c',f'modelFile:="{a.model}_model.g";Read("enumerate.g");']
t=time.monotonic()
with(a.out/'stdout.log').open('wb')as so,(a.out/'stderr.log').open('wb')as se:
    q=subprocess.Popen(cmd,cwd=W,stdout=so,stderr=se)
    (a.out/'pid').write_text(str(q.pid)+'\n')
    try:rc=q.wait(timeout=a.seconds);status='EXITED'
    except subprocess.TimeoutExpired:q.kill();q.wait();rc=None;status='TIMEOUT_NO_CERTIFICATE'
with(a.out/'stdout.log').open('rb')as f:
    f.seek(max(0,(a.out/'stdout.log').stat().st_size-10000))
    complete=b'COMPLETE_EXHAUSTION'in f.read()
r={'status':status,'returncode':rc,'seconds':time.monotonic()-t,'complete_marker':complete,
   'pins':pins,'unchanged':all(sha(W/x['path'])==x['sha256']for x in pins),
   'whole_original_credit':0,'distinct_review_pending':True}
(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

