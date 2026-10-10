#!/usr/bin/env python3
"""Compile the matrix centralizer core and reject two weakened hypotheses."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
REVISION = '905b95818eb32af7874a58b427f50c1711a5e96c'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--lean', required=True, type=Path)
    ap.add_argument('--packages', required=True, type=Path)
    args = ap.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output required')
    args.out.mkdir(parents=True)
    out = args.out.resolve()
    revision = subprocess.check_output(
        ['git', '-C', str(args.packages / 'mathlib'), 'rev-parse', 'HEAD'], text=True).strip()
    require(revision == REVISION, 'mathlib revision')
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join(str(p / '.lake/build/lib/lean')
                               for p in sorted(args.packages.iterdir()) if p.is_dir())
    source = ROOT / 'phase237_formal/ProjectiveDihedralMatrices.lean'
    original = source.read_text()
    require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', original, re.M),
            'proof escape')
    start = time.monotonic()
    runs = []
    variants = [
        ('matrix_core', original, True),
        ('allow_product_order_two', original.replace('(hlsq : l ^ 2 ≠ 1)',
                                                     '(hlsq : l ^ 2 = 1)'), False),
        ('allow_characteristic_two', original.replace('(h2 : (2 : F) ≠ 0)',
                                                      '(h2 : (2 : F) = 0)'), False),
    ]
    for name, body, expected_pass in variants:
        path = out / (name + '.lean')
        path.write_text(body)
        proc = subprocess.run([str(args.lean), str(path)], env=env, capture_output=True,
                              text=True, timeout=120)
        (out / (name + '.stdout')).write_text(proc.stdout)
        (out / (name + '.stderr')).write_text(proc.stderr)
        require((proc.returncode == 0) == expected_pass, 'unexpected result: ' + name)
        row = {'name': name, 'exit_code': proc.returncode,
               'source_sha256': sha(path), 'expected_pass': expected_pass}
        if expected_pass:
            axioms = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", proc.stdout, re.S)
            require(len(axioms) == 6 and 'sorryAx' not in proc.stdout, 'six proved declarations')
            require('warning:' not in proc.stdout and not proc.stderr, 'unexpected diagnostic')
            for _, names in axioms:
                require(set(n.strip() for n in names.split(',')) <=
                        {'propext', 'Classical.choice', 'Quot.sound'}, 'unexpected axiom')
            row['axiom_reports'] = axioms
        else:
            require('error:' in proc.stdout, 'control must fail elaboration')
        runs.append(row)
    report = {
        'status': 'PASS', 'source_sha256': sha(source),
        'seconds': round(time.monotonic() - start, 3), 'runs': runs,
        'lean_version': subprocess.check_output([str(args.lean), '--version'], text=True).strip(),
        'mathlib_revision': REVISION, 'trusted_cached_dependency_objects': True,
        'scope': 'Actual 2x2 matrix centralizers in split normal forms, including the trace-zero representative. General conjugacy, field descent, PGL quotient interface and classification are not formalized here.',
    }
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
