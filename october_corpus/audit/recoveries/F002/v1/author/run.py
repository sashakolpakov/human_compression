from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--degree', type=int, required=True)
parser.add_argument('--rank', type=int, default=5)
parser.add_argument('--seconds', type=int, default=600)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
args.out.mkdir(parents=True, exist_ok=False)
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pins = [{'path': n, 'sha256': digest(root / n)}
        for n in ['enumerate_even.g', 'run.py']]
command = ['/opt/homebrew/bin/gap', '-q', '-b', '-c',
           'degree:=%d;rankLimit:=%d;Read("enumerate_even.g");' %
           (args.degree, args.rank)]
start = time.monotonic()
with (args.out / 'stdout.log').open('wb') as out, (args.out / 'stderr.log').open('wb') as err:
    proc = subprocess.Popen(command, cwd=root, stdout=out, stderr=err)
    (args.out / 'pid').write_text(str(proc.pid) + '\n')
    try:
        rc = proc.wait(timeout=args.seconds)
        status = 'EXITED'
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        rc = None
        status = 'TIMEOUT_NO_CERTIFICATE'
data = (args.out / 'stdout.log').read_bytes()
report = {'status': status, 'returncode': rc,
          'seconds': time.monotonic() - start,
          'complete_marker': b'COMPLETE_EXHAUSTION' in data,
          'degree': args.degree, 'rank_limit': args.rank,
          'pins': pins, 'command': command,
          'unchanged': all(digest(root / p['path']) == p['sha256'] for p in pins),
          'whole_original_credit': 0, 'distinct_review_pending': True}
(args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
