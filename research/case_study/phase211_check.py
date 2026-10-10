#!/usr/bin/env python3
"""Replay exact surface calculations and the separately scoped Lean kernel theorems."""
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
FILES = ['phase211_surface_check.py', 'formal/CoverKernelChains.lean',
         'phase109_cover_families_generalization_model.json', 'phase211_check.py']


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--lean', default='/Users/sasha/.elan/bin/lean')
    parser.add_argument('--packages', type=Path,
                        default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory required')
    out = args.out.resolve()
    out.mkdir(parents=True)
    start = time.monotonic()
    for name in FILES:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    r = subprocess.run([sys.executable, '-O', 'phase211_surface_check.py', '--out', str(out / 'cells')],
                       cwd=out, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    (out / 'cells.log').write_text(r.stdout)
    require(r.returncode == 0, 'surface calculations failed')
    cells = json.loads((out / 'cells/report.json').read_text())
    require(cells['status'] == 'PASS', 'surface status failed')
    require(cells['negative_controls']['wrong_sggi'] == 'nontrivial involutions', 'wrong mutation rejection')
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN'] = 'leanprover/lean4:v4.32.2'
    env['LEAN_PATH'] = ':'.join([str(out)] + [str(args.packages / p / '.lake/build/lib/lean') for p in
        ['mathlib', 'plausible', 'proofwidgets', 'batteries', 'aesop', 'importGraph', 'LeanSearchClient', 'Qq']])
    revision = subprocess.run(['git', '-C', str(args.packages / 'mathlib'), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True, check=True).stdout.strip()
    require(revision == REVISION, 'unexpected mathlib revision')
    source = out / 'formal/CoverKernelChains.lean'
    original = source.read_text()
    require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', original, re.M), 'untrusted Lean source')
    r = subprocess.run([args.lean, '-o', str(out / 'CoverKernelChains.olean'), str(source)],
                       cwd=out, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    (out / 'CoverKernelChains.log').write_text(r.stdout)
    require(r.returncode == 0 and 'sorryAx' not in r.stdout, 'Lean compile failed')
    require(r.stdout.count('depends on axioms:') == 6, 'wrong theorem report count')
    axiom_sets = re.findall(r'depends on axioms:\s*\[([^]]*)\]', r.stdout)
    require(len(axiom_sets) == 6 and all(
        set(x.strip() for x in row.split(',')) <= {'propext', 'Classical.choice', 'Quot.sound'}
        for row in axiom_sets), 'nonstandard theorem axiom')
    old = '(hcop : p.Coprime q)'
    require(original.count(old) == 2, 'changed coprimality mutation sites')
    mutant = out / 'NoncoprimePowers.lean'
    mutant.write_text(original.replace(old, '(hcop : p ≤ q)'))
    r = subprocess.run([args.lean, str(mutant)], cwd=out, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    (out / 'NoncoprimePowers.log').write_text(r.stdout)
    require(r.returncode != 0 and 'error:' in r.stdout, 'false coprime-power generalization accepted')
    report = {'status': 'PASS', 'seconds': round(time.monotonic() - start, 3),
              'inputs': {name: sha(out / name) for name in FILES},
              'mathlib_revision': revision, 'Lean_toolchain': env['ELAN_TOOLCHAIN'],
              'Lean_theorems': 6, 'Lean_axioms': ['propext', 'Classical.choice', 'Quot.sound'],
              'Lean_negative_control': 'Coprimality weakened to mere order: REJECTED',
              'surface_report': cells,
              'artifacts': {name: sha(out / name) for name in ['cells.log', 'CoverKernelChains.log',
                  'NoncoprimePowers.log', 'cells/report.json']},
              'scope': 'Lean proves directed-chain closure, existence of maximal admissible kernels, uniqueness implies greatest, and coprime-power membership/joins. Python checks literal finite surfaces. The homological intersection theorem, surface criterion, cover construction, source-family transport and infinitely many minimal descendants remain separately written proofs.'}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'seconds': report['seconds'], 'out': str(out)}))


if __name__ == '__main__':
    main()
