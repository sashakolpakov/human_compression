#!/usr/bin/env python3
"""Replay phase256 finite diagnostics and five elementary Lean statements.

The quantified surface proof remains written and requires mathematical review.
Primary PDFs are optional external prerequisites, never silently substituted.
"""
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
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
SURFACE_HASH = '728eaceef1048ad8a266b51dcabf217266f07c554474e85fede41f0a5b69e71b'


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
    require(sha(ROOT/'phase211_surface_check.py') == SURFACE_HASH, 'frozen surface dependency')
    copied = ['phase211_surface_check.py', 'phase256_voltage_check.py',
              'phase256_voltage_models.json', 'formal/HomologyCoverAvoidance.lean']
    for name in copied:
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    primary = []
    if args.verify_primary:
        entries = json.loads((ROOT/'phase256_sources.json').read_text())['primary_sources']
        for row in entries:
            require(sha(ROOT/row['path']) == row['sha256'], 'changed primary '+row['id'])
            primary.append(row['id'])
    process = subprocess.run([sys.executable, '-O', 'phase256_voltage_check.py',
                              '--out', 'voltage_report.json'], cwd=out,
                             capture_output=True, text=True, timeout=120)
    (out/'voltage.log').write_text(process.stdout+process.stderr)
    require(process.returncode == 0, 'finite voltage replay')
    voltage = json.loads((out/'voltage_report.json').read_text())
    require(voltage['status'] == 'PASS' and len(voltage['results']) == 5, 'five finite models')
    require([r['order'] for r in voltage['results']] == [32, 96, 96, 216, 120], 'literal group orders')
    require(all(r['prime'] > 4*r['order'] for r in voltage['results']), 'actual large primes')
    require([r['base_odd_surface_criterion'] for r in voltage['results']] ==
            [False, False, False, False, True], 'old one-stage criterion controls')
    require(voltage['results'][-1]['odd_exterior_loop']['closed'] and
            voltage['results'][-1]['odd_exterior_loop']['parity'] == 1,
            'literal nonorientable exterior witness')
    source = (out/'formal/HomologyCoverAvoidance.lean').read_text()
    require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', source, re.M),
            'untrusted Lean declaration')
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN'] = 'leanprover/lean4:v4.32.2'
    env['LEAN_PATH'] = ':'.join([str(out)]+[str(args.packages/p/'.lake/build/lib/lean') for p in
        ['mathlib', 'plausible', 'proofwidgets', 'batteries', 'aesop', 'importGraph', 'LeanSearchClient', 'Qq']])
    revision = subprocess.run(['git', '-C', str(args.packages/'mathlib'), 'rev-parse', 'HEAD'],
                              check=True, capture_output=True, text=True).stdout.strip()
    require(revision == REVISION, 'pinned mathlib revision')
    process = subprocess.run([args.lean, '-o', str(out/'HomologyCoverAvoidance.olean'),
                              'formal/HomologyCoverAvoidance.lean'], cwd=out,
                             env=env, capture_output=True, text=True, timeout=120)
    log = process.stdout+process.stderr
    (out/'HomologyCoverAvoidance.log').write_text(log)
    reports = re.findall(r'depends on axioms:\s*\[([^]]*)\]', log, re.S)
    require(process.returncode == 0 and len(reports) == 5 and 'sorryAx' not in log,
            'five Lean declarations compile')
    require(all(set(x.strip() for x in row.split(',')) <= ALLOWED for row in reports),
            'Lean axiom scope')
    controls = {}
    for name, old, new in [
        ('MissingTransversality', '(hu : u ∉ S)', '(hu : True)'),
        ('NonStrictFieldBound', '(hcard : Fintype.card I < Fintype.card F)',
         '(hcard : Fintype.card I ≤ Fintype.card F)'),
        ('EvenRepetition', '(hp : p % 2 = 1)', '(hp : p % 2 = 0)'),
    ]:
        require(old in source, 'control target '+name)
        (out/(name+'.lean')).write_text(source.replace(old, new))
        process = subprocess.run([args.lean, name+'.lean'], cwd=out, env=env,
                                 capture_output=True, text=True, timeout=120)
        log = process.stdout+process.stderr
        (out/(name+'.log')).write_text(log)
        require(process.returncode != 0 and 'error:' in log, 'incorrect assumption accepted '+name)
        controls[name] = 'REJECTED'
    # A literal input violation must be rejected even under Python -O.
    models = json.loads((out/'phase256_voltage_models.json').read_text())
    models[0]['generators'][3] = models[0]['generators'][0]
    (out/'invalid_marks.json').write_text(json.dumps(models[:1]))
    process = subprocess.run([sys.executable, '-O', 'phase256_voltage_check.py',
                              '--models', 'invalid_marks.json', '--out', 'invalid_result.json'],
                             cwd=out, capture_output=True, text=True, timeout=120)
    log = process.stdout+process.stderr
    (out/'invalid_marks.log').write_text(log)
    require(process.returncode != 0 and 'ValueError: proper string pairs' in log,
            'coincident distant marks control')
    controls['CoincidentMarksUnderOptimization'] = 'REJECTED'
    report = {'status': 'PASS', 'seconds': round(time.monotonic()-start, 3),
              'primary_checked': primary, 'new_Lean_declarations': 5,
              'axioms': sorted(ALLOWED), 'finite_models': 5, 'controls': controls,
              'scope': 'Finite symbolic-voltage diagnostics and five affine/parity Lean interfaces only. The uniform surface argument, homological fiber identification and cover correspondence remain written proof obligations.',
              'artifacts': {str(p.relative_to(out)): sha(p) for p in sorted(out.rglob('*'))
                            if p.is_file() and p.suffix not in ['.olean', '.pyc']}}
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'seconds', 'new_Lean_declarations', 'finite_models', 'controls']}))


if __name__ == '__main__':
    main()
