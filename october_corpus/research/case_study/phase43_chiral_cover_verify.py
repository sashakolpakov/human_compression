#!/usr/bin/env python3
"""Replay the bound exact finite chiral-cover certificate in a NEW directory.

Stock GAP is trusted; this is not a Lean certificate or conjecture solver.
The historical author's in-place runner is intentionally not used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

SCRIPT_SHA = '59bf1cd96626df42e1e1baed82b88538416f336443c1a4076dfbb5f09bdcc69e'
LOG_SHA = 'dff678f6fc90e78e449585fc87fd8939eaf616240ff9faf3af83b1431235582d'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gap', default='gap')
    parser.add_argument('--input-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    source = (args.input_root/'phase41_chiral_cover_check.g').resolve()
    assert sha(source.read_bytes()) == SCRIPT_SHA, 'Certificate changed'
    executable = shutil.which(args.gap)
    assert executable, 'GAP executable unavailable'
    out = args.output_dir.absolute()
    out.mkdir()  # Refuse an existing output directory.
    command = [executable, '-q', '-b', str(source)]
    start = time.monotonic()
    run = subprocess.run(command, cwd=out, capture_output=True, timeout=600)
    elapsed = time.monotonic()-start
    (out/'stdout.log').write_bytes(run.stdout)
    (out/'stderr.log').write_bytes(run.stderr)
    # The historical Python runner used universal-newline text mode. GAP emits
    # an initial carriage return; preserve the raw log and match that convention.
    canonical = run.stdout.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    (out/'canonical_stdout.log').write_text(canonical)
    status = (run.returncode == 0 and not run.stderr and sha(canonical.encode()) == LOG_SHA
              and sha(source.read_bytes()) == SCRIPT_SHA)
    report = {
        'status': 'PASS' if status else 'FAIL', 'command': command,
        'exit_code': run.returncode, 'elapsed_seconds': elapsed,
        'script_sha256': SCRIPT_SHA, 'stdout_sha256': sha(run.stdout),
        'canonical_stdout_sha256': sha(canonical.encode()),
        'canonicalization': 'UTF-8 decode; CRLF and bare CR replaced by LF, matching historical universal-newline text mode; no other changes.',
        'stderr_sha256': sha(run.stderr),
        'runner_sha256': sha(Path(__file__).read_bytes()),
        'expected_version_in_exact_log': 'GAP 4.15.1',
        'scope': 'Six exact finite groups, actual intersections, mirror and cover maps, duality and a distinguishing word; not a Lean proof or conjecture resolution.',
    }
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if status else 1)


if __name__ == '__main__':
    main()
