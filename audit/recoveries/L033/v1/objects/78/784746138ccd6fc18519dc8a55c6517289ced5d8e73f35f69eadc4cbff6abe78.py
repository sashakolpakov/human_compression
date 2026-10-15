import sys
if sys.flags.optimize: raise SystemExit('optimized execution unsupported')
from pathlib import Path
import argparse,json,subprocess,time,os,hashlib
def pin(p):
    b=p.read_bytes(); return {'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p=argparse.ArgumentParser();p.add_argument('--driver',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--marker',required=True);p.add_argument('--seconds',type=int,default=120);a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic();cmd=['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(a.driver.resolve())]
report={'status':'RUNNING','command':cmd,'seconds_cap':a.seconds,'inputs':[pin(Path(__file__)),pin(a.driver)],'marker':a.marker,'whole_original_credit':0}
(a.out/'active.json').write_text(json.dumps(report,indent=2)+'\n')
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
with (a.out/'stdout').open('wb') as so,(a.out/'stderr').open('wb') as se:
    try:
        r=subprocess.run(cmd,stdout=so,stderr=se,timeout=a.seconds,env=env); report['returncode']=r.returncode
        text=(a.out/'stdout').read_text();err=(a.out/'stderr').read_text()
        report['status']='PASS' if r.returncode==0 and a.marker in text and not err.strip() and not any(x in text for x in ['Syntax warning','Error,','Error:']) else 'FAIL'
    except subprocess.TimeoutExpired:report['status']='TIMEOUT_NO_CERTIFICATE'
report['seconds']=time.monotonic()-start;report['outputs']=[pin(a.out/x) for x in ['stdout','stderr']]
(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'active.json').write_text(json.dumps({'status':'TERMINAL','report':pin(a.out/'report.json')},indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','seconds']}),flush=True)
if report['status']!='PASS': raise SystemExit(1)
