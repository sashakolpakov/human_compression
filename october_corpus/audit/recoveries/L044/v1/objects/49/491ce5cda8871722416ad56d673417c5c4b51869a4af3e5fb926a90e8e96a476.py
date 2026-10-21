#!/usr/bin/env python3
"""Operational integrity/replay driver; primitive_certificate.g is required maths."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound(base, entry):
    p = base / entry['path']
    require(p.stat().st_size == entry['bytes'] and sha(p) == entry['sha256'], str(p))
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--study-root', type=Path)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--gap', default='/opt/homebrew/bin/gap')
    ap.add_argument('--pdflatex', default='/opt/homebrew/bin/pdflatex')
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    out = args.out.resolve()
    require(out != here, 'Replay output must be separate from the frozen packet')
    out.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    if (here / 'manifest.json').exists():
        manifest = json.loads((here / 'manifest.json').read_text())
        for entry in manifest['exports']:
            bound(here, entry)
    scope = json.loads((here / 'scope.json').read_text())
    dependencies = json.loads((here / 'dependencies.json').read_text())
    for entry in json.loads((here / 'external_software.json').read_text())['files']:
        bound(Path('/'), entry)
    if args.study_root:
        bound(args.study_root, scope['source'])
        for entry in dependencies['accepted_packets']:
            bound(args.study_root, entry)
        for entry in dependencies['statements']:
            p = bound(args.study_root, entry['file'])
            block = p.read_bytes()[entry['byte_start']:entry['byte_end']]
            require(hashlib.sha256(block).hexdigest() == entry['span_sha256'], 'retained span')
            require(block.decode() == entry['exact_tex'], 'retained literal statement')
        bound(args.study_root, dependencies['finite_engine']['file'])
    run = subprocess.run([args.gap, '-q', str(here / 'primitive_certificate.g')],
                         cwd=out, capture_output=True, text=True, timeout=60)
    (out / 'program.stdout.log').write_text(run.stdout)
    (out / 'program.stderr.log').write_text(run.stderr)
    require(run.returncode == 0 and not run.stderr.strip(), 'GAP diagnostics')
    final = 'PASS_L044_PRIMITIVE_BOUNDARY|residuals=12|integer_cases=39|positive_A5=3'
    require(final in run.stdout and 'Error,' not in run.stdout, 'finite boundary failed')
    cases = re.findall(r'CASE n=(\d+) id=(\d+) order=(\d+) nodes=(\[[^\]]*\]) complete_high_markings=(\d+)', run.stdout)
    require(len(cases) == 13, 'twelve residuals plus one positive control')
    require(all(int(row[4]) == 0 for row in cases[:-1]), 'new high marking found')
    require(cases[-1][0:2] == ('6', '1') and cases[-1][4] == '3', 'positive marking control')
    pages = None
    if args.render:
        from pypdf import PdfReader
        for i in range(2):
            run = subprocess.run([args.pdflatex, '-interaction=nonstopmode', '-halt-on-error',
                                  '-output-directory', str(out), str(here / 'primitive_reduction.tex')],
                                 cwd=here, capture_output=True, text=True, timeout=30)
            (out / f'render{i+1}.log').write_text(run.stdout + run.stderr)
            require(run.returncode == 0, 'TeX rendering failed')
        actual = [(p.extract_text() or '') for p in PdfReader(out / 'primitive_reduction.pdf').pages]
        expected = [(p.extract_text() or '') for p in PdfReader(here / 'primitive_reduction.pdf').pages]
        require(actual == expected, 'rendered page text changed')
        pages = len(actual)
    report = {'status': 'PASS', 'claim': scope['claim'], 'residual_actions': 12,
              'integer_cases': 39, 'positive_A5_markings': 3, 'cases': cases,
              'rendered_pages': pages, 'private_dependencies_checked': bool(args.study_root),
              'whole_L044_recovery': False, 'seconds': time.monotonic() - start}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
