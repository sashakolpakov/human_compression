#!/usr/bin/env python3
"""Rebuild the complete overview and check actual SVG/PDF cost bars.

Author validation only. The numerical and scientific inputs have separate
acceptances; a distinct overview reviewer must check this consolidation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

from pypdf import PdfReader
import build
import geometry_checks as geometry

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--public-root', type=Path)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--xelatex', default='xelatex')
    args = parser.parse_args()
    build.need(not args.out.exists(), 'Use a fresh output directory.')
    if (ROOT / 'manifest.json').exists():
        for row in build.load(ROOT / 'manifest.json')['exports']:
            p = Path(row['path'])
            build.need(not p.is_absolute() and '..' not in p.parts, 'Unsafe export path.')
            raw = (ROOT / p).read_bytes()
            build.need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'Changed frozen export.')
    protocol, data = build.inputs()
    build.need(build.make(data) == build.load(ROOT / 'results.json'), 'Written comparisons or inventories changed.')
    if args.public_root:
        for row in protocol['inputs'].values():
            raw = subprocess.check_output(['git', 'show', protocol['baseline_commit'] + ':' + row['public_path']], cwd=args.public_root) if row.get('committed_baseline') else (args.public_root / row['public_path']).read_bytes()
            build.need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'Public input differs.')
        catalogues = {}
        for key, row in protocol['external_catalogue_bindings'].items():
            raw = (args.public_root / row['path']).read_bytes()
            build.need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'Complete catalogue changed.')
            catalogues[key] = json.loads(raw)
        old = {r['original_id']: r for r in catalogues['previous']['entries']}
        new = {r['original_id']: r for r in catalogues['current']['entries']}
        build.need(set(old) == set(new) and len(old) == 106 and
                   all(old[k] == new[k] for k in old if k not in ['L014', 'L007']), 'Unrelated accessible original changed.')
    args.out.mkdir(parents=True)
    command = [sys.executable, '-B', '-O', str(ROOT / 'build.py'), '--out', str((args.out / 'rebuilt').resolve())]
    if args.render:
        command += ['--render', '--xelatex', args.xelatex]
    run = subprocess.run(command, capture_output=True)
    (args.out / 'build.log').write_bytes(run.stdout + run.stderr)
    build.need(run.returncode == 0, 'Fresh overview build failed.')
    names = ['results.json', 'topics.csv', 'applications.csv', 'program_inventory.csv', 'plot_data.json', 'summary.tex']
    names += [k + '.svg' for k in ['whole_topics', 'conditional_1', 'conditional_2']]
    for name in names:
        build.need((ROOT / name).read_bytes() == (args.out / 'rebuilt' / name).read_bytes(), 'Rebuilt output differs: ' + name)
    bars = 0
    for key, spec in build.load(ROOT / 'plot_data.json').items():
        expected, height = geometry.expected_geometry(spec)
        geometry.compare_geometry(geometry.svg_rectangles((ROOT / (key + '.svg')).read_text()), expected)
        rectangles, height = geometry.pdf_rectangles(ROOT / (key + '.pdf'))
        geometry.compare_pdf(rectangles, height, expected, 3 if key == 'whole_topics' else 2)
        bars += len(expected)
    build.need(bars == 182, 'Complete chart components changed.')
    if args.render:
        text = lambda p: [page.extract_text() for page in PdfReader(p).pages]
        build.need(text(ROOT / 'summary.pdf') == text(args.out / 'rebuilt/summary.pdf') and
                   len(text(ROOT / 'summary.pdf')) == 6, 'Full reader page text changed.')
    build.dump(args.out / 'report.json', dict(status='PASS_AUTHOR_OVERVIEW43', originals=43, topics=19,
                written_and_conditional_comparisons=62, actual_SVG_bars=182, actual_PDF_bars=182,
                reader_pages=6 if args.render else None, complete_catalogues_checked=bool(args.public_root),
                fresh_scientific_or_numerical_input_replay=False, independently_reviewed=False))
    print('PASS: 43 originals,62 written/conditional comparisons,182 actual bars per format.')


if __name__ == '__main__':
    main()
