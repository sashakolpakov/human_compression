"""Bounded packet replay; the uniform proofs require mathematical review."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--render', action='store_true')
    p.add_argument('--examples', action='store_true')
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    count = 0
    if (ROOT/'manifest.json').exists():
        for r in json.loads((ROOT/'manifest.json').read_text())['exports']:
            data = (ROOT/r['path']).read_bytes()
            need(len(data) == r['bytes'] and hashlib.sha256(data).hexdigest() == r['sha256'], r['path'])
            count += 1
    render = None
    if a.render:
        from pypdf import PdfReader
        w = a.out/'render'
        w.mkdir()
        shutil.copyfile(ROOT/'cages_and_planes.tex', w/'cages_and_planes.tex')
        for i in range(2):
            run = subprocess.run(['/opt/homebrew/bin/pdflatex', '-halt-on-error',
                                  '-interaction=nonstopmode', 'cages_and_planes.tex'],
                                 cwd=w, capture_output=True, timeout=45)
            (a.out/f'pass{i}.log').write_bytes(run.stdout+run.stderr)
            need(run.returncode == 0, 'native build')
        log = (w/'cages_and_planes.log').read_text()
        need(not any(s in log for s in ['Overfull', 'undefined', 'LaTeX Warning:']), 'native diagnostics')
        old = [p.extract_text() for p in PdfReader(ROOT/'cages_and_planes.pdf').pages]
        new = [p.extract_text() for p in PdfReader(w/'cages_and_planes.pdf').pages]
        need(new == old and len(new) == 5, 'whole page texts')
        render = dict(pages=5, all_page_texts_equal=True)
    examples = None
    if a.examples:
        spec = importlib.util.spec_from_file_location('optional_examples', ROOT/'check_examples.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        examples = module.run()
        (a.out/'examples.json').write_text(json.dumps(examples, indent=2)+'\n')
    report = dict(status='PASS_BOUNDED_THEORY_REPLAY', frozen_exports=count,
                  render=render, optional_examples=len(examples['cases']) if examples else None,
                  mathematical_proof_automated=False, finite_census_run=False,
                  new_original_credit=0, new_question_credit=0, new_Lean_declarations=0)
    (a.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
