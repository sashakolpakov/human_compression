#!/usr/bin/env python3
"""Recount public G documents with the two separately supplied original PDFs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PINS = {
    'original_inputs': '79ee51fdfcd4eb9526015863af2abc588fd257d6eed8dcecc4b96a79ebc8173b',
    'inputs': 'c46e1742d44138d9a63af86ae2ee9dd9d1498d0b4ca0d75cf1fd19a022af978d',
    'input_review': '4bd02d9322aa41b6f6ea09ec68c10428b07bf079288048ef416f1d7e7f737d80',
    'input_adoption': '26fefb9a3b596a7ed8ceb0792a99afe0e39f01e3cb1483225ce04d8e69d8fbbb',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(name):
    path = Path(name)
    need(not path.is_absolute() and '..' not in path.parts, 'Unsafe mapped path')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--linear-source-pdf', type=Path, required=True)
    parser.add_argument('--steiner-source-pdf', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'Use a fresh output directory')
    out = args.out.resolve()
    need(not out.is_relative_to(ROOT), 'Output must be outside the publication checkout')
    for folder, pin in PINS.items():
        manifest = HERE / folder / 'manifest.json'
        need(digest(manifest.read_bytes()) == pin, 'Changed frozen packet ' + folder)
        for row in read(manifest)['exports']:
            data = (manifest.parent / relative(row['path'])).read_bytes()
            need(len(data) == row['bytes'] and digest(data) == row['sha256'],
                 'Changed frozen export ' + row['path'])
    mapping = read(HERE / 'recount_mapping.json')['routes']
    need(len({r['private_path'] for r in mapping}) == len(mapping) == 35,
         'Complete distinct recount inputs required')
    originals = {'L009': args.linear_source_pdf, 'L092': args.steiner_source_pdf}
    private = [r for r in mapping if r['public_path'] is None]
    need(len(private) == 2 and {r['source_id'] for r in private} == set(originals),
         'Exactly two separately supplied original PDFs required')
    with tempfile.TemporaryDirectory(prefix='topic-g-inputs-') as tmp:
        study = Path(tmp)
        for row in mapping:
            source = ROOT / relative(row['public_path']) if row['public_path'] else originals[row['source_id']]
            data = source.read_bytes()
            need(len(data) == row['bytes'] and digest(data) == row['sha256'],
                 'Changed recount input ' + row['private_path'])
            target = study / relative(row['private_path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        out.mkdir(parents=True)
        command = [sys.executable, '-B', '-O', str(HERE / 'input_review/check.py'),
                   '--study-root', str(study), '--public-root', str(ROOT),
                   '--packet', str(HERE / 'inputs'), '--original', str(HERE / 'original_inputs'),
                   '--out', str(out / 'independent_recount.json')]
        with (out / 'stdout.log').open('w') as stdout, (out / 'stderr.log').open('w') as stderr:
            result = subprocess.run(command, stdout=stdout, stderr=stderr)
        need(result.returncode == 0, 'Independent recount failed; inspect the preserved logs')
        report = read(out / 'independent_recount.json')
        need(report['status'] == 'PASS_INDEPENDENT_TOPIC_G_INPUT_REVIEW' and
             report['pdf_metric_cells'] == 180 and report['raw_metric_cells'] == 220 and
             len(report['independent_controls']) == 21,
             'Independent recount did not cover all accepted inputs')
    summary = {'status': 'PASS_PUBLIC_INPUT_ADAPTER', 'public_files': 33,
               'separately_supplied_originals': 2, 'pdf_metric_cells': 180,
               'raw_metric_cells': 220, 'independent_controls': 21,
               'primary_copies_removed': True, 'primary_material_exported': False,
               'independent_report': 'independent_recount.json',
               'report_sha256': digest((out / 'independent_recount.json').read_bytes()),
               'GAP_or_Lean_replay': False, 'new_source_credit': 0, 'new_question_credit': 0}
    (out / 'report.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
