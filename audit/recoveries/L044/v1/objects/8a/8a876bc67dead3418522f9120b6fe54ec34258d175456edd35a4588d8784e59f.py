"""Fresh exhaustive replay. Supply one previously nonexistent output directory."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

def require(condition,message):
    if not condition: raise RuntimeError(message)

def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

require(sys.flags.optimize==0,"Run without Python optimization")
require(len(sys.argv)==2,"Usage: python3 check.py NEW_OUTPUT_DIRECTORY")
src=Path(__file__).resolve().parent
out=Path(sys.argv[1]).resolve()
require(not out.exists(),"Output directory must be new")
files=[src/x for x in ['model.g','enumeration.g','run.g','check.py']]
inputs=[pin(p) for p in files]
out.mkdir(parents=True)
for p in files: shutil.copyfile(p,out/p.name)
report=dict(status="RUNNING",inputs=inputs,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),cap_seconds=240)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
try:
    with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
        proc=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b','run.g'],cwd=out,stdout=stdout,stderr=stderr)
        report['pid']=proc.pid
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        code=proc.wait(timeout=240)
    require(code==0,"GAP did not exit successfully")
    log=(out/'stdout.log').read_text()
    require(not (out/'stderr.log').read_bytes(),"GAP stderr is not empty")
    require('CONTROLS_PASS' in log and 'ALL_SIX_PATTERNS_COMPLETE' in log,"Missing completion marker")
    require('Error' not in log and 'NODE_CAP_NOT_EXHAUSTION' not in log,"Incomplete census")
    data=json.loads((out/'census.json').read_text())
    expected=[
        [1,[1,6,76,76,32,0],0,0],
        [2,[1,6,76,76,528,0],0,0],
        [3,[1,6,76,76,32,0],0,0],
        [4,[1,6,76,76,528,5376],5376,0],
        [5,[1,6,76,76,528,0],0,0],
        [6,[1,6,76,76,528,2912],2912,0]]
    require(data['model']==[1024,344064,239],"Model mismatch")
    require(data['rows']==expected,"Exhausted census differs from recorded table")
    require((data['reference_calls'],data['reference_pairs'])==(20478,5413998),"Full-subset reference differs")
    require([pin(p) for p in files]==inputs,"Source changed during replay")
    report.update(status="PASS",census=data,whole_original_credit=0)
except BaseException as exc:
    if 'proc' in locals() and proc.poll() is None:
        proc.kill();proc.wait()
    report.update(status="FAILED_NO_CERTIFICATE",error=str(exc),whole_original_credit=0)
    raise
finally:
    report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    report['outputs']=[pin(out/x) for x in ['stdout.log','stderr.log','census.json'] if (out/x).exists()]
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
