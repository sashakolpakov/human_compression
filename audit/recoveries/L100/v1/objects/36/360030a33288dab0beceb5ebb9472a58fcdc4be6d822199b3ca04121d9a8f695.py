"""Rehash this operational packet and run only its bounded no-target controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
if not __debug__:
    raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode = True
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    for row in json.loads((here / 'manifest.json').read_text())['exports']:
        data = (here / row['path']).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise SystemExit('changed operational export: ' + row['path'])
    subprocess.run([sys.executable, str(here / 'controls.py'), '--out', str(args.out)], check=True, timeout=55)
if __name__ == '__main__':
    main()
