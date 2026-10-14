import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path
import argparse,hashlib,json,subprocess,time
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=int,required=True);p.add_argument('--cwd',type=Path,required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
if a.command and a.command[0]=='--':a.command=a.command[1:]
assert a.command and not a.out.exists() and a.out.parent.is_dir()
a.out.mkdir();start=time.monotonic();record=dict(status='RUNNING',command=a.command,cwd=str(a.cwd.resolve()),cap=a.seconds)
(a.out/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
try:
 r=subprocess.run(a.command,cwd=a.cwd,capture_output=True,timeout=a.seconds);code,stdout,stderr=r.returncode,r.stdout,r.stderr;status='TERMINAL_PASS'if code==0 else'TERMINAL_FAILURE'
except subprocess.TimeoutExpired as e:code,stdout,stderr=None,e.stdout or b'',e.stderr or b'';status='EXTERNAL_DEADLINE'
except OSError as e:code,stdout,stderr=None,b'',str(e).encode();status='LAUNCH_FAILURE'
def pin(p):
 b=p.read_bytes();return dict(path=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
(a.out/'stdout').write_bytes(stdout);(a.out/'stderr').write_bytes(stderr)
record.update(status=status,returncode=code,seconds=time.monotonic()-start,stdout=pin(a.out/'stdout'),stderr=pin(a.out/'stderr'))
(a.out/'receipt.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));sys.exit(0 if status=='TERMINAL_PASS'else 1)
