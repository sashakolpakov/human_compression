#!/usr/bin/env python3
"""Recount the published Topic F files and a separately supplied primary PDF."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUT_PIN = '0dfc2fce16d8c532a1cdd9b8f61c1d9391c15099091e795cbba56bde30501620'
REVIEW_PIN = '91ac8430736283e6719bcb3cb4e1245cb2576a38608283b4fd207c1009a0247b'
ADOPTION_PIN = 'f5a71b94d9fe202cd6dfdff92c7ec7002cf490092a31d3d78080e390d2e3053d'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(name):
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts, 'Unsafe mapped path')
    return p


def check_packet(folder, pin):
    manifest = HERE / folder / 'manifest.json'
    need(digest(manifest.read_bytes()) == pin, 'Changed ' + folder + ' manifest')
    for row in read(manifest)['exports']:
        data = (manifest.parent / relative(row['path'])).read_bytes()
        need(len(data) == row['bytes'] and digest(data) == row['sha256'],
             'Changed frozen export ' + row['path'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-pdf', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'Use a fresh output directory')
    check_packet('inputs', INPUT_PIN)
    check_packet('input_review', REVIEW_PIN)
    check_packet('input_adoption', ADOPTION_PIN)
    mapping = read(HERE / 'input_adoption/public_mapping.json')['routes']
    immutable = read(HERE / 'inputs/manifest.json')['immutable_inputs']
    need([{k: r[k] for k in ['path', 'bytes', 'sha256']} for r in mapping] == immutable,
         'Public routes must cover every immutable input in order')
    private = [r for r in mapping if r['public_path'] is None]
    need(len(private) == 1 and private[0]['path'] == 'sources/regular_4pm2025.pdf',
         'Exactly one separately supplied primary PDF')
    args.out.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix='topic-f-inputs-') as tmp:
        study = Path(tmp)
        for row in mapping:
            source = ROOT / relative(row['public_path']) if row['public_path'] else args.source_pdf
            data = source.read_bytes()
            need(len(data) == row['bytes'] and digest(data) == row['sha256'],
                 'Changed input ' + row['path'])
            target = study / relative(row['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        # The frozen independent reviewer checks the original author packet.
        # Only its published exports are copied; no private extraction is exported.
        shutil.copytree(HERE / 'inputs', study / 'topic_F_measurement_inputs')
        runs = [('recount.py', 'recount.json'), ('controls.py', 'controls.json')]
        for script, output in runs:
            subprocess.run([sys.executable, '-B', '-O', str(HERE / 'input_review' / script),
                            '--study-root', str(study), '--packet', str(HERE / 'inputs'),
                            '--out', str(args.out.resolve() / output)], check=True)
    print('PASS: public files and separately supplied primary reproduce the input audit')


if __name__ == '__main__':
    main()
