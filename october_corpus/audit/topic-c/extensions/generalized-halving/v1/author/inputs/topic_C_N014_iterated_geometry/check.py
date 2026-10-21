#!/usr/bin/env python3
"""Portable bindings/render and optional coordinate checks; not theorem proving."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from pypdf import PdfReader
from check_coordinates import run


def need(b, m):
    if not b:
        raise ValueError(m)


def signature(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--study-root', type=Path)
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--pdflatex', default='/opt/homebrew/bin/pdflatex')
    a = ap.parse_args()
    here = Path(__file__).resolve().parent
    a.out.mkdir(parents=True, exist_ok=False)
    count = 0
    if (here/'manifest.json').exists():
        for row in json.loads((here/'manifest.json').read_text())['exports']:
            need(signature(here/row['path']) == {k: row[k] for k in ['bytes','sha256']},
                 'export '+row['path'])
            count += 1
    bindings = json.loads((here/'dependencies.json').read_text())
    if a.study_root:
        for row in bindings['study_inputs']:
            need(signature(a.study_root/row['path']) ==
                 {k: row[k] for k in ['bytes','sha256']}, 'dependency '+row['path'])
    scope = json.loads((here/'scope.json').read_text())
    need(scope['new_original_credit'] == scope['new_conjecture_credit'] == 0,
         'no new credit')
    need(scope['measurement'] is None and not scope['whole_source_acceptance'],
         'bounded nonnumerical scope')
    need(scope['required_new_finite_programs'] == [] and scope['new_Lean'] == [],
         'purely written proof')
    rows = json.loads((here/'source_map.json').read_text())['rows']
    need(len(rows) == len({r['id'] for r in rows}) == 14, 'fourteen distinct source items')
    computed = run()
    need(computed == json.loads((here/'coordinate_report.json').read_text()),
         'optional coordinate replay')
    reference = json.loads((here/'render_reference.json').read_text())
    def check_pdf(path):
        pages = PdfReader(path).pages
        need(len(pages) == reference['pages'] == 7, 'whole seven-page proof')
        need([hashlib.sha256(x.extract_text().encode()).hexdigest() for x in pages]
             == reference['page_text_sha256'], 'exact page text')
    check_pdf(here/'iterated_geometry.pdf')
    if a.render:
        build = a.out/'render'
        build.mkdir()
        for i in [1,2]:
            p = subprocess.run([a.pdflatex,'-interaction=nonstopmode',
                                '-halt-on-error','-output-directory='+str(build),
                                str(here/'iterated_geometry.tex')],
                               cwd=here, text=True, capture_output=True)
            (build/f'pass{i}.log').write_text(p.stdout+p.stderr)
            need(p.returncode == 0, 'TeX build')
        log = (build/'pass2.log').read_text()
        need(not any(x in log for x in ['undefined','Overfull','Underfull']),
             'clean final TeX')
        check_pdf(build/'iterated_geometry.pdf')
    report = dict(status='PASS', exports_verified=count,
                  study_bindings_verified=len(bindings['study_inputs']) if a.study_root else 0,
                  source_items=len(rows), exact_pdf_pages=7,
                  optional_diagrams=len(computed['diagrams']),
                  optional_lattice_cases=len(computed['lattice_cases']),
                  controls=len(computed['controls']),rendered=a.render,
                  uniform_proof_basis='written mathematical review, not this program',
                  whole_source_acceptance=False)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
