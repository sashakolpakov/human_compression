#!/usr/bin/env python3
"""Public replay of the accepted L012 packet, without redistributing primary texts."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
PINS = {
    'phase250_manifest.json': '27f605517f1fec35aef62ec181229d5ed2b8f73aeda09f5cd0ccd9a1af44c62e',
    'phase254_manifest.json': 'b075f2b957b557a15bd04e5c3b2451c3012c2c947faf3808c12d96438466372b',
}
OMITTED_BUILD_PRODUCT = 'phase254_replay/author/PeriodSignObstruction.olean'


def need(ok, message):
    if not ok:
        raise RuntimeError('PHASE259_REJECT ' + message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(row):
    name = pathlib.PurePosixPath(row['path'])
    need(not name.is_absolute() and '..' not in name.parts, 'relative artifact')
    path = ROOT / name
    need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'binding ' + str(name))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ['out', 'gap', 'lean', 'packages']:
        parser.add_argument('--' + flag, type=pathlib.Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh raw output')
    out = args.out.resolve()
    need(not out.exists(), 'fresh resolved output')
    out.mkdir(parents=True)
    checked = 0
    for name, expected in PINS.items():
        need(sha(ROOT / name) == expected, 'frozen manifest ' + name)
        manifest = json.loads((ROOT / name).read_bytes())
        for row in manifest['exports']:
            if row['path'] == OMITTED_BUILD_PRODUCT:
                continue
            binding(row)
            checked += 1
        for row in manifest['retained_bindings']:
            if not row['path'].startswith('sources/'):
                binding(row)
    start = time.monotonic()
    executions = []

    def run(label, command):
        before = time.monotonic()
        result = subprocess.run([str(x) for x in command], cwd=ROOT,
                                text=True, capture_output=True, timeout=300)
        for suffix, text in [('stdout', result.stdout), ('stderr', result.stderr)]:
            (out / (label + '.' + suffix)).write_text(text)
        executions.append(dict(label=label, exit_code=result.returncode,
                               seconds=round(time.monotonic() - before, 3),
                               stdout_sha256=sha(out / (label + '.stdout')),
                               stderr_sha256=sha(out / (label + '.stderr'))))
        need(result.returncode == 0, label)
        return result

    run('author', [sys.executable, '-B', '-O', ROOT / 'phase250_check.py',
                  '--out', out / 'author', '--gap', args.gap,
                  '--lean', args.lean, '--packages', args.packages])
    author = json.loads((out / 'author/report.json').read_bytes())
    need(author['status'] == 'PASS' and not author['primary_checked'], 'public author replay')
    need(len(author['axiom_reports']) == 3, 'three formal declarations')
    run('independent_affine', [sys.executable, '-B', '-O', ROOT / 'phase254_independent_affine.py',
                               '--out', out / 'independent_affine.json'])
    affine = json.loads((out / 'independent_affine.json').read_bytes())
    need(affine['status'] == 'PASS' and len(affine['models']) == 18
         and affine['bad_period']['intersection_failures'], 'independent quotients and negative control')
    result = run('independent_presentations', [args.gap, '-q', '-T', ROOT / 'phase254_source_presentations.g'])
    need(result.stdout.count('IP64 deletions8 PASS') == 6
         and 'PHASE254_PRESENTATIONS_PASS' in result.stdout
         and 'Error' not in result.stdout + result.stderr, 'six literal source presentations')
    report = dict(status='PASS', seconds=round(time.monotonic() - start, 3),
                  manifest_bindings=PINS, frozen_exports_checked=checked,
                  omitted_cached_build_product=OMITTED_BUILD_PRODUCT,
                  primary_texts_checked=False, executions=executions,
                  source_rows=33, proof_spans=14, independent_affine_models=18,
                  independent_literal_presentations=6, lean_declarations=3,
                  scope='Fresh public author and independent computational replay. Primary reading and mathematical acceptance remain the frozen phase254 review and root acceptance; primary files are not distributed.',
                  trust=author['limits'] + ['Pinned cached Lean dependency objects remain trusted.'])
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', seconds=report['seconds'], report=str(out / 'report.json'))))


if __name__ == '__main__':
    main()
