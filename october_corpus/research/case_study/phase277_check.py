#!/usr/bin/env python3
"""Replay the finite obstruction and three order-theoretic Lean statements."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REVISION = '905b95818eb32af7874a58b427f50c1711a5e96c'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--lean', default='/Users/sasha/.elan/bin/lean')
    parser.add_argument('--packages', type=Path,
                        default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    parser.add_argument('--verify-primary', action='store_true')
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory required')
    out = args.out.resolve()
    out.mkdir(parents=True)
    start = time.monotonic()
    source_ledger = json.loads((ROOT/'phase277_sources.json').read_text())
    for row in source_ledger['prior_project_inputs']:
        require(sha(ROOT/row['path']) == row['sha256'], 'frozen dependency '+row['path'])
    primary = []
    if args.verify_primary:
        for row in source_ledger['primary_sources']:
            require(sha(ROOT/row['path']) == row['sha256'], 'primary '+row['id'])
            primary.append(row['id'])
    for name in ['phase277_obstruction_check.py', 'formal/IntervalMinimalCoverLifting.lean']:
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    process = subprocess.run([sys.executable, '-O', 'phase277_obstruction_check.py',
                              '--out', 'obstruction_report.json'], cwd=out,
                             capture_output=True, text=True, timeout=120)
    (out/'obstruction.log').write_text(process.stdout + process.stderr)
    require(process.returncode == 0, 'finite obstruction replay')
    finite = json.loads((out/'obstruction_report.json').read_text())
    require(finite['status'] == 'PASS' and finite['cover_IP_pairs_checked'] == 1024,
            'complete finite scope')
    source = (out/'formal/IntervalMinimalCoverLifting.lean').read_text()
    require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', source, re.M),
            'untrusted Lean declaration')
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN'] = 'leanprover/lean4:v4.32.2'
    env['LEAN_PATH'] = ':'.join([str(out)] + [str(args.packages/p/'.lake/build/lib/lean') for p in
        ['mathlib', 'plausible', 'proofwidgets', 'batteries', 'aesop', 'importGraph', 'LeanSearchClient', 'Qq']])
    revision = subprocess.run(['git', '-C', str(args.packages/'mathlib'), 'rev-parse', 'HEAD'],
                              check=True, capture_output=True, text=True).stdout.strip()
    require(revision == REVISION, 'pinned mathlib revision')
    process = subprocess.run([args.lean, '-o', str(out/'IntervalMinimalCoverLifting.olean'),
                              'formal/IntervalMinimalCoverLifting.lean'], cwd=out,
                             env=env, capture_output=True, text=True, timeout=120)
    log = process.stdout + process.stderr
    (out/'IntervalMinimalCoverLifting.log').write_text(log)
    require(process.returncode == 0 and log.count('does not depend on any axioms') == 3
            and 'sorryAx' not in log and 'warning:' not in log, 'three Lean declarations')
    controls = {}
    for name, old, new in [
        ('ReversedDescent', '(hrm : r ≤ m)', '(hrm : m ≤ r)'),
        ('MissingLocalAdmissibility', '(hm : Q (f m))', '(hm : True)'),
    ]:
        require(old in source, 'control target '+name)
        (out/(name+'.lean')).write_text(source.replace(old, new))
        process = subprocess.run([args.lean, name+'.lean'], cwd=out, env=env,
                                 capture_output=True, text=True, timeout=120)
        log = process.stdout + process.stderr
        (out/(name+'.log')).write_text(log)
        require(process.returncode != 0 and 'error:' in log, 'invalid hypothesis accepted '+name)
        controls[name] = 'REJECTED'
    process = subprocess.run([sys.executable, '-O', 'phase277_obstruction_check.py',
                              '--remove-identification', '--out', 'invalid.json'], cwd=out,
                             capture_output=True, text=True, timeout=120)
    log = process.stdout + process.stderr
    (out/'removed_identification.log').write_text(log)
    require(process.returncode != 0 and 'nontrivial separated intersection' in log,
            'removed central identification control')
    controls['RemovedCentralIdentificationUnderOptimization'] = 'REJECTED'
    report = {'status': 'PASS', 'seconds': round(time.monotonic()-start, 3),
              'primary_checked': primary, 'new_Lean_declarations': 3, 'axioms': [],
              'controls': controls, 'base_order': finite['base_order'],
              'cover_order': finite['cover_order'],
              'scope': 'Three order-theoretic statements and one complete finite obstruction model. The interval extension theorem and actual-polytope corollary remain written arguments with explicit prior inputs.',
              'artifacts': {str(p.relative_to(out)): sha(p) for p in sorted(out.rglob('*'))
                            if p.is_file() and p.suffix not in ['.olean', '.pyc']}}
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'seconds', 'new_Lean_declarations', 'controls']}))


if __name__ == '__main__':
    main()
