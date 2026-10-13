#!/usr/bin/env python3
"""Operational replay; string_certificate.g is the required mathematical code."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def bound(base, record):
    p = base / record['path']
    data = p.read_bytes()
    need(len(data) == record['bytes'], f'Byte count: {p}')
    need(hashlib.sha256(data).hexdigest() == record['sha256'], f'Hash: {p}')
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
    need(out != here, 'Use a separate replay output directory')
    out.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    if (here / 'manifest.json').exists():
        for row in json.loads((here / 'manifest.json').read_text())['exports']:
            bound(here, row)
    scope = json.loads((here / 'scope.json').read_text())
    deps = json.loads((here / 'dependencies.json').read_text())
    for row in json.loads((here / 'external_software.json').read_text())['files']:
        bound(Path('/'), row)
    if args.study_root:
        bound(args.study_root, scope['source'])
        for row in deps['accepted_packets']:
            bound(args.study_root, row)
        for row in deps['statements']:
            p = bound(args.study_root, row['file'])
            fragment = p.read_bytes()[row['byte_start']:row['byte_end']]
            need(fragment.decode() == row['exact_tex'], 'Retained exact proof span')
            need(hashlib.sha256(fragment).hexdigest() == row['span_sha256'], 'Retained span hash')
        bound(args.study_root, deps['finite_engine']['file'])
    run = subprocess.run([args.gap, '-q', '-b', str(here / 'string_certificate.g')],
                         cwd=out, capture_output=True, text=True, timeout=60)
    (out / 'program.stdout.log').write_text(run.stdout)
    (out / 'program.stderr.log').write_text(run.stderr)
    need(run.returncode == 0 and not run.stderr.strip(), 'GAP replay diagnostics')
    need('Error,' not in run.stdout, 'GAP error')
    need('PASS_L044_PRIMITIVE_STRINGS|actions=4|integer_cases=38|positive_A5=3|negative_controls=4' in run.stdout,
         'Required finite result or positive control changed')
    need('COUNTEREXAMPLE|order=1344|primitive=true|omissions=[ 192, 192, 192, 96, 168 ]' in run.stdout,
         'Literal counterexample changed')
    rows = re.findall(r'CASE n=(\d+) id=(\d+) order=(\d+) nodes=(\[[^\]]*\]) complete_high_markings=(\d+)', run.stdout)
    need(len(rows) == 5 and all(r[4] == '0' for r in rows[:4]), 'Four empty exhaustive lists')
    need([r[:2] for r in rows] == [('8', '3'), ('8', '5'), ('9', '7'), ('16', '11'), ('6', '1')],
         'Exact action roster')
    need(rows[-1][4] == '3', 'Positive census control')
    pages = None
    if args.render:
        from pypdf import PdfReader
        for i in range(2):
            run = subprocess.run([args.pdflatex, '-interaction=nonstopmode', '-halt-on-error',
                                  '-output-directory', str(out), str(here / 'primitive_strings.tex')],
                                 cwd=here, capture_output=True, text=True, timeout=30)
            (out / f'render{i+1}.log').write_text(run.stdout + run.stderr)
            need(run.returncode == 0, 'TeX build')
        actual = [p.extract_text() or '' for p in PdfReader(out / 'primitive_strings.pdf').pages]
        expected = [p.extract_text() or '' for p in PdfReader(here / 'primitive_strings.pdf').pages]
        need(actual == expected and len(actual) == 2, 'Exact two-page text')
        pages = len(actual)
    report = {'status': 'PASS', 'claim': scope['claim'], 'literal_group_order': 1344,
              'omission_orders': [192, 192, 192, 96, 168], 'counterexample_primitive': True,
              'counterexample_string_orderings': 0, 'residual_primitive_actions': 4,
              'cases': rows, 'integer_comparisons': 38, 'positive_A5_strings': 3,
              'negative_controls': 4, 'IP_tests_used': False, 'centralizer_quotient_pruning_used': False,
              'rendered_pages': pages, 'private_dependencies_checked': bool(args.study_root),
              'whole_L044_recovery': False, 'seconds': time.monotonic() - start}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
