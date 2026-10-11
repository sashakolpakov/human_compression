"""Portable integrity and finite-validation replay for the written correction."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def need(value, label):
    if not value:
        raise ValueError(label)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output required')
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'manifest.json').read_text())
    for row in manifest['exports']:
        path = root/row['path']
        need(path.is_file() and path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
             'export binding: '+row['path'])
    if args.source is not None:
        need(digest(args.source) == manifest['primary']['sha256'], 'exact source edition hash')
    args.out.mkdir(parents=True)
    reports = {}
    for name in ['literal_s4', 'controls']:
        run = subprocess.run([sys.executable, '-B', '-O', str(root/(name+'.py'))], text=True,
                             capture_output=True, check=True)
        (args.out/(name+'.stdout')).write_text(run.stdout)
        (args.out/(name+'.stderr')).write_text(run.stderr)
        reports[name] = json.loads(run.stdout)
    expected = json.loads((root/'validation.json').read_text())
    need(reports['literal_s4'] == expected, 'exact independently reproducible model report')
    need(reports['controls']['status'] == 'PASS' and len(reports['controls']['controls']) == 4,
         'all controls')
    report = {'status': 'PASS', 'manifest_sha256': digest(root/'manifest.json'),
              'exports': len(manifest['exports']), 'source_verified': args.source is not None,
              'finite_validation': reports,
              'proof_boundary': 'Written elementary Helly and infinite normal-form proofs; finite programs are validation, not the uniform proof.'}
    (args.out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'exports': len(manifest['exports']), 'controls': 4}))

if __name__ == '__main__':
    main()
