#!/usr/bin/env python3
"""Replay only the elementary Lean portion of the proposed general cover proof.

The geometric filling argument is a written proof using retained primary
theorems. A PASS here does not certify that argument or settle the conjecture.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent
REVISION = '905b95818eb32af7874a58b427f50c1711a5e96c'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


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
    parser.add_argument('--verify-primary', action='store_true',
                        help='also require and hash the eight separately acquired primary PDFs')
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory required')
    out = args.out.resolve()
    out.mkdir(parents=True)
    start = time.monotonic()
    bindings = json.loads((ROOT / 'phase216_sources.json').read_text())
    checked_primary = []
    if args.verify_primary:
        for entry in bindings['sources']:
            require(sha(ROOT / entry['path']) == entry['sha256'], 'changed primary: ' + entry['id'])
            checked_primary.append(entry['id'])
        require(sha(ROOT / 'phase211_export.json') == bindings['frozen211_manifest_sha256'],
                'changed frozen211 manifest')
    require(sha(ROOT / 'formal/CoverKernelChains.lean') ==
            bindings['frozen211_lean_sha256'],
            'changed frozen211 Lean dependency')
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN'] = 'leanprover/lean4:v4.32.2'
    env['LEAN_PATH'] = ':'.join([str(out)] + [str(args.packages / p / '.lake/build/lib/lean') for p in
        ['mathlib', 'plausible', 'proofwidgets', 'batteries', 'aesop', 'importGraph', 'LeanSearchClient', 'Qq']])
    revision = subprocess.run(['git', '-C', str(args.packages / 'mathlib'), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True, check=True).stdout.strip()
    require(revision == REVISION, 'unexpected mathlib revision')
    reports = {}
    for name, count in [('CoverKernelChains', 6), ('CoverKernelGeneration', 5)]:
        source = ROOT / 'formal' / (name + '.lean')
        original = source.read_text()
        require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', original, re.M),
                'untrusted source in ' + name)
        target = out / (name + '.lean')
        shutil.copyfile(source, target)
        r = subprocess.run([args.lean, '-o', str(out / (name + '.olean')), str(target)],
                           cwd=out, env=env, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=180)
        (out / (name + '.log')).write_text(r.stdout)
        require(r.returncode == 0 and 'sorryAx' not in r.stdout, name + ' compile failed')
        rows = re.findall(r'depends on axioms:\s*\[([^]]*)\]', r.stdout)
        require(len(rows) == count and all(
            set(x.strip() for x in row.split(',')) <= ALLOWED for row in rows),
            'unexpected theorem or axiom set in ' + name)
        reports[name] = {'theorems': count, 'source_sha256': sha(target),
                         'log_sha256': sha(out / (name + '.log'))}
    original = (out / 'CoverKernelGeneration.lean').read_text()
    mutations = [
        ('OverlappingCoordinates', '(hdisj : Disjoint I J)', '(hdisj : True)'),
        ('UnseparatedPoints',
         '(hsep : ∀ x y, (∀ i, coord i x = coord i y) → x = y)', '(hsep : True)'),
        ('NonconsecutivePowers', 'w ^ (m + 1) ∈ B', 'w ^ (m + 2) ∈ B'),
    ]
    controls = {}
    for name, old, new in mutations:
        require(original.count(old) == 1, 'unexpected mutation location for ' + name)
        mutant = out / (name + '.lean')
        mutant.write_text(original.replace(old, new))
        r = subprocess.run([args.lean, str(mutant)], cwd=out, env=env, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        (out / (name + '.log')).write_text(r.stdout)
        require(r.returncode != 0 and 'error:' in r.stdout, 'mutation accepted: ' + name)
        controls[name] = {'status': 'REJECTED', 'log_sha256': sha(out / (name + '.log'))}
    report = {
        'status': 'PASS', 'seconds': round(time.monotonic() - start, 3),
        'mathlib_revision': revision, 'Lean_toolchain': env['ELAN_TOOLCHAIN'],
        'theorems': reports, 'negative_controls': controls,
        'verified_primary_PDFs': checked_primary,
        'inputs': {name: sha(ROOT / name) for name in [
            'phase216_check.py', 'phase216_sources.json', 'phase216_general_covers.md',
            'phase216_geometric_filling.md', 'formal/CoverKernelChains.lean',
            'formal/CoverKernelGeneration.lean']},
        'scope': 'Five new elementary Lean theorems use the frozen211 definitions. '
                 'Normal generation and consecutive-power supply remain explicit hypotheses. '
                 'The cubical geometry, the retained geometric theorems, and the complete '
                 'polytope-cover argument are not certified by this runner.'
    }
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'seconds': report['seconds'], 'out': str(out)}))


if __name__ == '__main__':
    main()
