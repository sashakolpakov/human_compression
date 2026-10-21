#!/usr/bin/env python3
"""Compile the six polynomial declarations under pinned Lean dependencies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(condition, message):
    if not condition:
        raise RuntimeError('PHASE266_REJECT ' + message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['out', 'lean', 'packages']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output')
    out = args.out.resolve()
    need(not out.exists(), 'fresh resolved output')
    out.mkdir(parents=True)
    start = time.monotonic()
    source = ROOT / 'phase266_formal/PrimitiveSquarePolynomial.lean'
    text = source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', text, re.M),
         'no proof holes or new axioms')
    pins_path = ROOT / 'formal/dependency_manifest.json'
    pins = json.loads(pins_path.read_text())
    dependencies = []
    for item in pins['packages']:
        path = args.packages / item['name']
        rev = subprocess.check_output(['git', '-C', path, 'rev-parse', 'HEAD'], text=True).strip()
        need(rev == item['rev'] and subprocess.run(
            ['git', '-C', path, 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
            'pinned clean package ' + item['name'])
        dependencies.append(dict(name=item['name'], revision=rev))
    version = subprocess.check_output([args.lean, '--version'], text=True).strip()
    need('version 4.32.2,' in version, 'Lean version')
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(str(p / '.lake/build/lib/lean')
        for p in args.packages.iterdir() if (p / '.lake/build/lib/lean').is_dir())
    copied = out / source.name
    copied.write_text(text)
    result = subprocess.run([str(args.lean), '-o', str(out / 'PrimitiveSquarePolynomial.olean'),
                             str(copied)], cwd=out, env=env, text=True,
                            capture_output=True, timeout=180)
    (out / 'formal.stdout').write_text(result.stdout)
    (out / 'formal.stderr').write_text(result.stderr)
    need(result.returncode == 0 and not re.search(r'error:|warning:|sorryAx',
         result.stdout + result.stderr), 'fresh Lean compile')
    axioms = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", result.stdout)
    expected = ['evaluated_polynomial', 'evaluated_derivative', 'trace_identity',
                'bezout_identity', 'distinct_parameters_no_shared_root', 'no_common_derivative_root']
    need([x[0] for x in axioms] == ['PrimitiveSquarePolynomial.' + x for x in expected],
         'exact declarations')
    need(all(set(re.findall(r'[\w.]+', x)) <= {'propext', 'Classical.choice', 'Quot.sound'}
             for _, x in axioms), 'standard axioms only')
    # Actual counterexamples to dropping the essential hypotheses.
    def f(s, x, p):
        return ((s - 4) * (x*x + 1)**2 - 4*s*x*x) % p
    def d(s, x, p):
        return (4*x*((s - 4)*x*x - s - 4)) % p
    need(f(0, 2, 5) == d(0, 2, 5) == 0, 's=0 repeated-root control')
    need(f(4, 0, 5) == d(4, 0, 5) == 0, 's=4 repeated-root control')
    need(f(0, 1, 2) == f(1, 1, 2) == 0, 'characteristic-two shared-root control')
    need(f(1, 0, 5) != 0, 'zero trace-variable control')
    report = dict(status='PASS', seconds=round(time.monotonic()-start, 3),
        source_sha256=sha(source), checker_sha256=sha(Path(__file__)),
        dependency_manifest_sha256=sha(pins_path), lean_version=version,
        dependencies=dependencies, axiom_reports=axioms, exit_code=result.returncode,
        semantic_hypothesis_controls=4, trusted_cached_dependency_objects=True,
        scope='Six actual polynomial declarations only; no norm, primitive-character, Weil, finite-reduction or full conjecture formalization.')
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
