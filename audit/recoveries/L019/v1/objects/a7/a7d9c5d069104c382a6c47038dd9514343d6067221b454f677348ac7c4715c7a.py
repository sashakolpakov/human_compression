import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
a=argparse.ArgumentParser();a.add_argument('n',type=int);a.add_argument('--seconds',type=int,default=120);a.add_argument('--name',default='run01');args=a.parse_args()
w=Path(__file__).resolve().parent;o=w/f'n{args.n}_{args.name}';o.mkdir(exist_ok=False)
(o/'parameters.g').write_text(f'n:={args.n};;\n')
(o/'enumerate.g').write_bytes((w/'enumerate.g').read_bytes())
r={'status':'RUNNING','scope':'critical-wing finite diagnostic, no theorem credit yet','n':args.n,'deadline_seconds':args.seconds,'files':{x:hashlib.sha256((o/x).read_bytes()).hexdigest() for x in ['parameters.g','enumerate.g']}}
(o/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');t=time.monotonic()
with (o/'stdout.log').open('wb') as out,(o/'stderr.log').open('wb') as err:
 try:
  p=subprocess.run(['/opt/homebrew/bin/gap','-q','-T','enumerate.g'],cwd=o,stdout=out,stderr=err,timeout=args.seconds)
  r['returncode']=p.returncode;r['status']='TERMINAL_PENDING_CHECK'
 except subprocess.TimeoutExpired:r['status']='TIMEOUT_NO_CERTIFICATE'
r['seconds']=time.monotonic()-t
b=(o/'stdout.log').read_bytes();e=(o/'stderr.log').read_bytes()
if r['status']=='TERMINAL_PENDING_CHECK':r['status']='COMPLETE_DIAGNOSTIC' if r['returncode']==0 and not e and b.count(b'COMPLETE_ANCHORED_CRITICAL_WINGS')==1 else 'FAILED_NO_CERTIFICATE'
r['stdout_sha256']=hashlib.sha256(b).hexdigest();r['stderr_bytes']=len(e)
(o/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));print(b.decode()[-1800:])
