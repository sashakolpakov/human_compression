from pathlib import Path
import subprocess,time,json,hashlib
D=Path(__file__).resolve().parent;out=D/'independent01';out.mkdir(exist_ok=False)
cmd=['/opt/homebrew/bin/gap','-q','-b','-T',str(D/'independent.g')]
t=time.monotonic();r=subprocess.run(cmd,cwd=D,capture_output=True,timeout=150)
(out/'stdout').write_bytes(r.stdout);(out/'stderr').write_bytes(r.stderr)
status='PASS'if r.returncode==0 and not r.stderr and b'PASS_INDEPENDENT_RANK_TWO 'in r.stdout else'FAILED'
x=dict(status=status,command=cmd,returncode=r.returncode,seconds=time.monotonic()-t,stdout_sha256=hashlib.sha256(r.stdout).hexdigest(),stderr_sha256=hashlib.sha256(r.stderr).hexdigest(),no_full_geometry_census=True)
(out/'receipt.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x));print(r.stdout.decode()[-1500:]);raise SystemExit(0 if status=='PASS'else 1)
