"""Run prepared models serially; timeouts and missing markers give no census."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
S = Path(__file__).resolve().parent.parent
W = S / 'corpus106_L071_remaining_censuses_work'
queue = json.loads((W / 'queue.json').read_text())
a.out.mkdir(parents=True, exist_ok=False)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(W / 'enumerate.g') == queue['engine_sha256']
records = []
for row in queue['models']:
    name = row['name']
    out = a.out / name
    out.mkdir()
    paths = [Path(__file__), W / 'queue.json', W / 'enumerate.g', W / row['model']]
    if name == 'J3':
        paths.extend([W / 'J3.g1', W / 'J3.g2'])
    pins = [{'path': str(path), 'sha256': sha(path)} for path in paths]
    assert sha(W / row['model']) == row['model_sha256']
    cmd = ['/opt/homebrew/bin/gap', '-q', '-b', '-c',
           f'modelFile:="{row["model"]}";Read("enumerate.g");']
    start = time.monotonic()
    with (out / 'stdout.log').open('wb') as so, (out / 'stderr.log').open('wb') as se:
        child = subprocess.Popen(cmd, cwd=W, stdout=so, stderr=se)
        (out / 'pid').write_text(str(child.pid) + '\n')
        current = {'name': name, 'pid': child.pid, 'owner': 'root',
                   'seconds_limit': row['seconds_limit'], 'output': str(out),
                   'started_utc': datetime.now(timezone.utc).isoformat()}
        (a.out / 'current_job.json').write_text(json.dumps(current, indent=2) + '\n')
        print(json.dumps({'started': name, 'pid': child.pid}), flush=True)
        try:
            rc = child.wait(timeout=row['seconds_limit'])
            status = 'EXITED'
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
            rc = None
            status = 'TIMEOUT_NO_CERTIFICATE'
    with (out / 'stdout.log').open('rb') as stream:
        stream.seek(max(0, (out / 'stdout.log').stat().st_size - 10000))
        complete = b'COMPLETE_EXHAUSTION' in stream.read()
    unchanged = all(sha(Path(pin['path'])) == pin['sha256'] for pin in pins)
    if status == 'EXITED' and not (rc == 0 and complete and unchanged):
        status = 'FAILED_NO_CERTIFICATE'
    report = {'name': name, 'status': status, 'returncode': rc,
              'seconds': time.monotonic() - start, 'seconds_limit': row['seconds_limit'],
              'complete_marker': complete, 'pins': pins, 'unchanged': unchanged,
              'source_counts_used_to_direct_or_stop_search': False,
              'whole_original_credit': 0, 'distinct_review_pending': True}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    records.append(report)
    (a.out / 'batch_progress.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'pins'}), flush=True)
(a.out / 'current_job.json').write_text(json.dumps({'status': 'BATCH_TERMINAL',
    'completed': sum(r['status'] == 'EXITED' for r in records), 'total': len(records)}, indent=2) + '\n')
