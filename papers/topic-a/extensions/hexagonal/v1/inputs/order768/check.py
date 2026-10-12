#!/usr/bin/env python3
"""Replay the isolated universal group, local groups and all intersections."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, time
HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    if (HERE / 'manifest.json').exists():
        for entry in json.loads((HERE / 'manifest.json').read_text())['exports']:
            path = HERE / entry['path']
            need(path.stat().st_size == entry['bytes'] and
                 hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'],
                 'frozen export ' + entry['path'])
    shutil.copyfile(HERE / 'verify.g', args.out / 'verify.g')
    started = time.monotonic()
    result = subprocess.run(['/opt/homebrew/bin/gap', '-q', '-T', 'verify.g'],
                            cwd=args.out, capture_output=True, text=True, timeout=45)
    (args.out / 'stdout.log').write_text(result.stdout)
    (args.out / 'stderr.log').write_text(result.stderr)
    need(result.returncode == 0 and not result.stderr and
         'PASS_768_AND_GENUS4' in result.stdout, 'exact finite calculation')
    pages = None
    if args.render:
        from pypdf import PdfReader
        shutil.copyfile(HERE / 'order768.tex', args.out / 'order768.tex')
        for i in [1, 2]:
            run = subprocess.run(['/opt/homebrew/bin/pdflatex', '-interaction=nonstopmode',
                                  '-halt-on-error', 'order768.tex'], cwd=args.out,
                                 capture_output=True, text=True, timeout=30)
            (args.out / f'tex{i}.log').write_text(run.stdout + run.stderr)
            need(run.returncode == 0, 'TeX build')
        text = (args.out / 'order768.log').read_text()
        need(not any(x in text for x in ['Overfull', 'Underfull', 'LaTeX Warning',
                                         'Missing character']), 'clean TeX')
        pdf = PdfReader(args.out / 'order768.pdf')
        pages = len(pdf.pages)
        if (HERE / 'order768.pdf').exists():
            old = PdfReader(HERE / 'order768.pdf')
            need([p.extract_text() for p in pdf.pages] ==
                 [p.extract_text() for p in old.pages], 'exact rebuilt page text')
    report = dict(status='PASS', universal_order=768, facet_order=128,
                  vertex_figure_order=48, all_intersection_pairs=256,
                  vertex_figure_f_vector=[4,12,6], euler_characteristic=-2,
                  nonorientable=True, genus=4, new_Lean=0, whole_original_credit=0,
                  rendered_pages=pages, seconds=time.monotonic()-started)
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
