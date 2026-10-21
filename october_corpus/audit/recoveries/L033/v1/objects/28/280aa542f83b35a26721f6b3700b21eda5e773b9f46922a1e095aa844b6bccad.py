from pathlib import Path
import json,subprocess,time,hashlib
W=Path(__file__).resolve().parent;O=W/'independent02'
if O.exists():raise RuntimeError('fresh output')
O.mkdir();cmd=['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(W/'independent02.g')];t=time.monotonic()
try:
 p=subprocess.run(cmd,capture_output=True,timeout=90);code,stdout,stderr=p.returncode,p.stdout,p.stderr
except subprocess.TimeoutExpired as exc:
 code,stdout,stderr=None,exc.stdout or b'',exc.stderr or b''
(O/'stdout').write_bytes(stdout);(O/'stderr').write_bytes(stderr)
r=dict(command=cmd,cap_seconds=90,returncode=code,seconds=time.monotonic()-t,stdout_sha256=hashlib.sha256(stdout).hexdigest(),stderr_sha256=hashlib.sha256(stderr).hexdigest(),driver_sha256=hashlib.sha256((W/'independent02.g').read_bytes()).hexdigest())
(O/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
if code!=0 or stderr or b'PASS_INDEPENDENT_GROUP_CERTIFICATES'not in stdout:raise RuntimeError('independent certificate check failed')
print(stdout.decode());print(json.dumps(r))
