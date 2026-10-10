#!/usr/bin/env python3
"""Replay the independently reviewed elementary packet, not the geometric proof.

Requires the frozen phase216 export and its fourteen files, the frozen
CoverKernelChains.lean dependency, pinned Lean and mathlib. Primary PDFs
are optional and are checked only with --verify-primary. See the review
for the separate, complete written mathematical assessment.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
AUTHOR_SHA = 'daba2e40dc03b5c7f6067e9ea938ff4e408d82d45e412b4ff9b72e70b0269f13'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bindings(primary):
    path = ROOT / 'phase216_export.json'
    require(sha(path) == AUTHOR_SHA, 'changed author manifest')
    manifest = json.loads(path.read_text())
    checks = dict(manifest['files'])
    checks['formal/CoverKernelChains.lean'] = manifest['frozen_dependencies']['formal/CoverKernelChains.lean']
    if primary:
        checks.update(manifest['external_primary_references'])
        checks['phase211_export.json'] = manifest['frozen_dependencies']['phase211_export.json']
    for name, expected in checks.items():
        require((ROOT / name).stat().st_size == expected['bytes'] and
                sha(ROOT / name) == expected['sha256'], 'changed bound input: ' + name)
    return {name: expected['sha256'] for name, expected in checks.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--lean', default='/Users/sasha/.elan/bin/lean')
    parser.add_argument('--packages', type=Path,
                        default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    parser.add_argument('--verify-primary', action='store_true')
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory required')
    before = bindings(args.verify_primary)
    out = args.out.resolve()
    out.mkdir(parents=True)
    start = time.monotonic()
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    cmd = [sys.executable, '-B', '-O', str(ROOT / 'phase216_check.py'),
           '--out', str(out / 'formal'), '--lean', args.lean,
           '--packages', str(args.packages)]
    if args.verify_primary:
        cmd.append('--verify-primary')
    result = subprocess.run(cmd, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=240)
    (out / 'author_stdout.log').write_text(result.stdout)
    require(result.returncode == 0, 'author replay failed; see author_stdout.log')
    report = json.loads((out / 'formal/report.json').read_text())
    require(report['status'] == 'PASS', 'author report did not pass')
    for name, count in [('CoverKernelChains', 6), ('CoverKernelGeneration', 5)]:
        require(report['theorems'][name]['theorems'] == count, 'wrong theorem count')
        log = out / 'formal' / (name + '.log')
        require(sha(log) == report['theorems'][name]['log_sha256'], 'formal log not bound')
        text = log.read_text()
        rows = re.findall(r'depends on axioms:\s*\[([^]]*)\]', text)
        require(len(rows) == count and 'sorryAx' not in text, 'invalid formal output')
        require(all(set(x.strip() for x in row.split(',')) <= ALLOWED for row in rows),
                'nonstandard axiom detected')
    require(set(report['negative_controls']) == {
        'OverlappingCoordinates', 'UnseparatedPoints', 'NonconsecutivePowers'},
        'incorrect altered-proof controls')
    for name, record in report['negative_controls'].items():
        log = out / 'formal' / (name + '.log')
        require(record['status'] == 'REJECTED' and sha(log) == record['log_sha256'] and
                'error:' in log.read_text(), 'altered-proof control failed: ' + name)
    for name, digest in report['inputs'].items():
        require(name in before and before[name] == digest, 'unbound author report input: ' + name)
    control = subprocess.run([sys.executable, '-B', '-O', str(ROOT / 'phase222_hypothesis_controls.py'),
                              '--out', str(out / 'hypothesis_controls.json')],
                             env=env, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=30)
    (out / 'controls_stdout.log').write_text(control.stdout)
    require(control.returncode == 0, 'independent countermodels failed')
    models = json.loads((out / 'hypothesis_controls.json').read_text())
    require(models['status'] == 'PASS' and len(models) == 6, 'incorrect countermodel report')
    require(before == bindings(args.verify_primary), 'input changed during replay')
    contract = json.loads((ROOT / 'phase222_source_contract.json').read_text())
    require(contract['author_manifest']['sha256'] == AUTHOR_SHA and
            len(contract['clauses']) == 20 and len(contract['sources']) == 8,
            'wrong review contract')
    answer = {
        'status': 'PASS', 'date': '2026-10-10',
        'seconds': round(time.monotonic() - start, 3),
        'author_manifest_sha256': AUTHOR_SHA,
        'author_files_bound': 14, 'source_contract_clauses': 20,
        'verified_primary_PDFs': report['verified_primary_PDFs'],
        'formal_theorems': {'new': 5, 'retained': 6, 'axioms': sorted(ALLOWED)},
        'altered_proof_controls_rejected': 3,
        'independent_hypothesis_countermodels': 4,
        'frozen_inputs_verified_before_and_after': before,
        'review_inputs': {name: sha(ROOT / name) for name in [
            'phase222_general_cover_review.md', 'phase222_source_contract.json',
            'phase222_hypothesis_controls.py', 'phase222_check.py']},
        'artifacts': {str(path.relative_to(out)): sha(path) for path in
                      sorted(out.rglob('*')) if path.is_file() and path.suffix in ('.json', '.log')},
        'scope': 'Executable acceptance covers only the explicitly conditional elementary Lean '
                 'statements and hypothesis countermodels. The complete general cover theorem '
                 'is accepted by the separate written review; its geometric proof is not formalized.'
    }
    (out / 'report.json').write_text(json.dumps(answer, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'seconds': answer['seconds'],
                      'new_Lean': 5, 'retained_Lean': 6, 'countermodels': 4}))


if __name__ == '__main__':
    main()
