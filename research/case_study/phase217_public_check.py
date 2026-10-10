#!/usr/bin/env python3
"""Replay both reviewed components of the label-eleven counterexample."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def need(ok, message):
    if not ok:
        raise RuntimeError('P217_REJECT ' + message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--gap', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--packages', type=Path, required=True)
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    # Check the caller's actual path before following a possibly dangling link.
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output path')
    out = args.out.absolute()
    manifests = {
        'phase212_export.json': '2c461355cccb9962149010720d7c620f5e32a829e7a50549e654b8ef261a5cae',
        'phase214_manifest.json': 'f50d16fc1339b27cd1daccd641829dc470b74b92bd595687c754e6d36b115b4c'}
    bound = {}
    for name, expected in manifests.items():
        need(sha(base / name) == expected, 'manifest ' + name)
        for row in json.loads((base / name).read_text())['exports']:
            need(sha(base / row['path']) == row['sha256'], 'artifact ' + row['path'])
            bound[row['path']] = row['sha256']
    out.mkdir(parents=True)
    commands = [
        [sys.executable, '-B', '-O', base / 'phase214_check.py', '--out', out / 'upper'],
        [sys.executable, '-B', '-O', base / 'phase212_check.py', '--out', out / 'matrices',
         '--gap', args.gap, '--lean', args.lean, '--packages', args.packages]]
    for label, command in zip(['upper', 'matrices'], commands):
        p = subprocess.run(list(map(str, command)), capture_output=True, text=True, timeout=900)
        (out / (label + '.stdout')).write_text(p.stdout)
        (out / (label + '.stderr')).write_text(p.stderr)
        need(p.returncode == 0, label + ': ' + (p.stdout + p.stderr)[-1500:])
    upper = json.loads((out / 'upper/report.json').read_text())
    matrix = json.loads((out / 'matrices/report.json').read_text())
    need(upper['status'] == 'PASS', 'upper certificate status')
    need(matrix['status'] == 'P212_MATRIX_AND_QUOTIENT_REPLAY_PASS', 'matrix certificate status')
    need(matrix['signed_group_order'] == 2249598645043200, 'matching signed order')
    need(bound == {name: sha(base / name) for name in bound}, 'frozen input stability')
    report = dict(status='P217_COMBINED_PUBLIC_REPLAY_PASS', manifests=manifests,
                  bound_artifacts=len(bound), unsigned_order=matrix['unsigned_group_order'],
                  signed_order=matrix['signed_group_order'],
                  upper_report_sha256=sha(out / 'upper/report.json'),
                  matrix_report_sha256=sha(out / 'matrices/report.json'),
                  formal_declarations=len(matrix['formal_declarations']),
                  whole_theorem_formalized=False, historical_priority_established=False)
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('P217_COMBINED_PUBLIC_REPLAY_PASS')


if __name__ == '__main__':
    main()
