"""One fresh reviewer replay; retained per-child caps and an outer deadline."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,subprocess,time,os,signal,argparse
W=Path(__file__).resolve().parent;H=W.parent;P=H/'cubic_example_v1'
def read(p):return json.loads(p.read_text())
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def pin(p):
 p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def need(v,m):
 if not v:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author-sha',required=True);a=ap.parse_args()
 need(pin(P/'manifest.json')['sha256']==a.author_sha,'exact final manifest')
 O=W/'execution01';F=W/'fresh01';need(not O.exists()and not F.exists(),'fresh')
 deps={r['path']:r for r in read(P/'dependencies.json')}
 for r in read(P/'manifest.json')['exports']:
  p=P/r['path'];q=pin(p);need(q['bytes']==r['bytes']and q['sha256']==r['sha256'],'exact export');deps[q['path']]=q
 for p in [P/'manifest.json',Path(__file__).resolve(),Path(sys.executable)]:deps[str(p.resolve())]=pin(p)
 for r in deps.values():need(pin(Path(r['path']))==r,'exact dependency')
 O.mkdir();cmd=[sys.executable,str(P/'check.py'),'--out',str(F),'--render'];inputs=[deps[k]for k in sorted(deps)]
 save(O/'inputs.json',inputs);save(O/'active.json',dict(command=cmd,cap_seconds=180,author_sha256=a.author_sha,inputs=inputs))
 start=time.monotonic();deadline=False;error=None;code=None
 with (O/'stdout').open('wb')as so,(O/'stderr').open('wb')as se:
  try:
   proc=subprocess.Popen(cmd,stdout=so,stderr=se,stdin=subprocess.DEVNULL,start_new_session=True)
   try:code=proc.wait(timeout=180)
   except subprocess.TimeoutExpired:
    deadline=True;os.killpg(proc.pid,signal.SIGKILL);code=proc.wait()
  except OSError as e:error=repr(e)
 try:unchanged=all(pin(Path(r['path']))==r for r in inputs)
 except OSError:unchanged=False
 clean=(O/'stderr').stat().st_size==0;passed=code==0 and not deadline and error is None and unchanged and clean
 outputs=[pin(p)for root in[O,F]if root.exists()for p in sorted(root.rglob('*'))if p.is_file()]
 receipt=dict(status='CLEAN_FINITE_RETURN'if passed else'FAILED_NO_CERTIFICATE',command=cmd,cap_seconds=180,returncode=code,deadline=deadline,error=error,seconds=time.monotonic()-start,inputs_unchanged=unchanged,stderr_empty=clean,outputs=outputs,target_census=False,whole_original_credit=0)
 save(O/'receipt.json',receipt);print(json.dumps({k:v for k,v in receipt.items()if k!='outputs'}));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
