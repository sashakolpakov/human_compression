import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
w = Path(__file__).resolve().parent
p = w / 'enumerate.g'
receipt = {'status': 'RUNNING', 'source_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
           'deadline_seconds': 45, 'scope': 'bounded critical degree10 diagnostic; no incomplete classification credit'}
(w / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
start = time.monotonic()
try:
    result = subprocess.run(['/opt/homebrew/bin/gap', '-q', '-T', str(p)], cwd=w,
                            capture_output=True, timeout=45)
    (w / 'stdout.log').write_bytes(result.stdout)
    (w / 'stderr.log').write_bytes(result.stderr)
    good = result.returncode == 0 and not result.stderr and result.stdout.count(b'COMPLETE_FRACTURED_CRITICAL_SYMMETRIC') == 1
    receipt.update(status='COMPLETE_DIAGNOSTIC' if good else 'FAILED_NO_CERTIFICATE', returncode=result.returncode)
except subprocess.TimeoutExpired as exc:
    (w / 'stdout.log').write_bytes(exc.stdout or b'')
    (w / 'stderr.log').write_bytes(exc.stderr or b'')
    receipt['status'] = 'TIMEOUT_NO_CERTIFICATE'
receipt['seconds'] = time.monotonic() - start
(w / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
