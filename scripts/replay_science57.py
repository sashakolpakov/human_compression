"""Reconstruct exact F011 packets and rebuild the eight native pages privately."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    out = args.out.resolve()
    if out.exists() or out.is_relative_to(repo):
        raise ValueError('Use a fresh private output directory outside the repository.')
    rows = json.loads((repo / 'audit/science57/v1/copy_plan.json').read_text())['files']
    for row in rows:
        source = repo / row['public_path']
        raw = source.read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('Changed payload: ' + row['public_path'])
        destination = out / row['packet'] / row['logical_path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    subprocess.run([sys.executable, '-B', '-O', str(out/'author/check.py'),
                    '--out', str(out/'render'), '--render'], check=True)
    print(json.dumps(dict(status='PASS_PUBLIC_F011_RECONSTRUCTION', files=len(rows),
                          pages=8, new_Lean=0, conjecture_credit=0)))


if __name__ == '__main__':
    main()
