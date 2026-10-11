#!/usr/bin/env python3
"""Fresh exact numerical and reader replay from frozen count records."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import pypdf

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError('B5_NUMERICAL_REPLAY_REJECT: ' + message)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--public-root', type=Path, required=True)
    ap.add_argument('--locations', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--xelatex', default='/opt/homebrew/bin/xelatex')
    a = ap.parse_args()
    need(not a.out.exists(), 'fresh output')
    a.out.mkdir(parents=True)
    if (HERE / 'manifest.json').exists():
        for row in json.loads((HERE / 'manifest.json').read_text())['exports']:
            b = (HERE / row['path']).read_bytes()
            need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
                 'frozen export ' + row['path'])
    roots = ['--study-root', str(a.study_root), '--public-root', str(a.public_root)]
    if a.locations:
        roots += ['--locations', str(a.locations)]
    def run(name, arguments):
        p = subprocess.run([sys.executable, '-B', '-O', str(HERE / name)] + arguments,
                           capture_output=True, text=True, timeout=240)
        (a.out / (name + '.log')).write_text(p.stdout + p.stderr)
        need(p.returncode == 0, name + ': ' + p.stderr[-1000:])
    run('compute.py', roots + ['--out', str(a.out / 'calculation')])
    run('build_reader.py', ['--results', str(a.out / 'calculation/results.json'),
                          '--out', str(a.out / 'reader'), '--xelatex', a.xelatex])
    for name in ['results.json', 'comparisons.csv']:
        need((a.out / 'calculation' / name).read_bytes() == (HERE / name).read_bytes(),
             'exact rebuilt ' + name)
    for name in ['measurement.tex', 'whole_costs.svg', 'whole_costs.pdf', 'plot_data.json']:
        need((a.out / 'reader' / name).read_bytes() == (HERE / name).read_bytes(),
             'exact rebuilt ' + name)
    old = [p.extract_text() or '' for p in pypdf.PdfReader(HERE / 'measurement.pdf').pages]
    new = [p.extract_text() or '' for p in pypdf.PdfReader(a.out / 'reader/measurement.pdf').pages]
    need(old == new and len(old) == 2, 'two exact rebuilt reader page texts')
    run('check.py', roots + ['--out', str(a.out / 'check.json')])
    report = dict(status='PASS', exact_generated_files=6, exact_reader_page_texts=2,
                  arithmetic=json.loads((a.out / 'check.json').read_text()),
                  original_source_PDFs_required=False, scientific_programs_executed=False)
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
