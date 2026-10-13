import json,subprocess,time,hashlib
from pathlib import Path
w=Path(__file__).resolve().parent;p=w/'enumerate.g';b=p.read_bytes();start=time.monotonic()
r={'source_sha256':hashlib.sha256(b).hexdigest(),'deadline_seconds':45,'status':'RUNNING','scope':'new critical-rank diagnostic only'}
(w/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
try:
 q=subprocess.run(['gap','-q','-T',str(p)],cwd=w,capture_output=True,timeout=45)
 (w/'stdout.log').write_bytes(q.stdout);(w/'stderr.log').write_bytes(q.stderr)
 r.update(returncode=q.returncode,seconds=time.monotonic()-start,status='COMPLETE_DIAGNOSTIC'if q.returncode==0 and not q.stderr and q.stdout.count(b'COMPLETE_ANCHORED_CRITICAL_SYMMETRIC')==1 else'FAILED_NO_CERTIFICATE')
except subprocess.TimeoutExpired as e:
 (w/'stdout.log').write_bytes(e.stdout or b'');(w/'stderr.log').write_bytes(e.stderr or b'');r.update(status='TIMEOUT_NO_CERTIFICATE',seconds=time.monotonic()-start)
(w/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
