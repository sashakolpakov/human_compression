#!/usr/bin/env python3
"""Recount the published representation topic with its separately supplied source PDF."""
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
    'inputs':'122820fac69c94d484444a88b4318fa7ae1a588770c4378737af7d457a037af1',
    'input_review':'d9b130046c95f625946762a4414fc294d2366e5bed3803aae783bb43967b69f3',
    'input_adoption':'c6cd89907ac02b7384fb887e93e3d4f941dcab2f963cc9156341cbeb5b2a24c5',
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
    parser.add_argument('--source-pdf', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'Use a fresh output directory')
    out = args.out.resolve()
    need(not out.is_relative_to(ROOT), 'Output must be outside the publication checkout')
    for folder, pin in PINS.items():
        manifest = HERE/folder/'manifest.json'
        need(digest(manifest.read_bytes())==pin, 'Changed frozen packet '+folder)
        for row in read(manifest)['exports']:
            data = (manifest.parent/relative(row['path'])).read_bytes()
            need(len(data)==row['bytes'] and digest(data)==row['sha256'],
                 'Changed frozen export '+row['path'])
    mapping = read(HERE/'recount_mapping.json')['routes']
    need(len({r['private_path'] for r in mapping})==len(mapping)==17,
         'Complete distinct recount inputs required')
    originals = [r for r in mapping if r['public_path'] is None]
    need(len(originals)==1 and originals[0]['source_id']=='F010',
         'Exactly one separately supplied source PDF required')
    with tempfile.TemporaryDirectory(prefix='representation-inputs-') as tmp:
        study = Path(tmp)
        for row in mapping:
            source = ROOT/relative(row['public_path']) if row['public_path'] else args.source_pdf
            data = source.read_bytes()
            need(len(data)==row['bytes'] and digest(data)==row['sha256'],
                 'Changed recount input '+row['private_path'])
            target = study/relative(row['private_path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        out.mkdir(parents=True)
        command = [sys.executable, '-B', '-O', str(HERE/'input_review/check.py'),
                   '--study-root', str(study), '--packet', str(HERE/'inputs'),
                   '--public-root', str(ROOT), '--out', str(out/'independent_recount.json')]
        with (out/'stdout.log').open('w') as stdout, (out/'stderr.log').open('w') as stderr:
            result = subprocess.run(command, stdout=stdout, stderr=stderr)
        need(result.returncode==0, 'Independent recount failed; inspect the preserved logs')
        report = read(out/'independent_recount.json')
        need(report['status']=='ACCEPTED_INDEPENDENT_MEASUREMENT_INPUT_REVIEW' and
             report['pdf_metric_cells']==120 and report['raw_metric_cells']==60 and
             report['controls_rejected']==30,
             'Independent recount did not cover all accepted inputs')
        archived = read(HERE/'input_review/independent_replay.json')
        need({k:v for k,v in report.items() if k!='elapsed_seconds'}==
             {k:v for k,v in archived.items() if k!='elapsed_seconds'},
             'Independent recount differs from the accepted evidence')
    summary = {'status':'PASS_PUBLIC_REPRESENTATION_INPUT_ADAPTER',
               'public_files':16, 'separately_supplied_originals':1,
               'pdf_metric_cells':120, 'raw_metric_cells':60, 'independent_controls':30,
               'primary_copies_removed':True, 'primary_material_exported':False,
               'matches_archived_recount_except_elapsed_time':True,
               'independent_report':'independent_recount.json',
               'report_sha256':digest((out/'independent_recount.json').read_bytes()),
               'GAP_or_Lean_replay':False, 'new_source_credit':0, 'new_question_credit':0}
    (out/'report.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
