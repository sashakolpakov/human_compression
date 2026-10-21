"""Exact packet/direct-acquisition integrity; not a mathematical proof oracle."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not an accepted checker mode')
from pathlib import Path
import hashlib
import json
import argparse

def need(condition, message):
    if not condition:
        raise ValueError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, default=Path('/Users/sasha/medusa/research/leemans'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    checked = []
    def verify(root, item):
        p = root / item['path']
        need(p.is_file(), 'Missing pinned file: ' + str(p))
        raw = p.read_bytes()
        need(len(raw) == item['bytes'], 'Size mismatch: ' + str(p))
        need(hashlib.sha256(raw).hexdigest() == item['sha256'], 'Hash mismatch: ' + str(p))
        checked.append(str(p))
    manifest = json.loads((here / 'manifest.json').read_text())
    for item in manifest['exports']:
        verify(here, item)
    dep = json.loads((here / 'dependencies.json').read_text())
    for item in dep['bindings']:
        need(item['root'] == 'private_study', 'Unexpected root')
        verify(args.study, item)
        if item['path'].endswith('/manifest.json'):
            p = args.study / item['path']
            child = json.loads(p.read_text())
            for exp in child.get('exports', []):
                verify(p.parent, exp)
    routes = json.loads((here / 'claim_routes.json').read_text())
    need(routes['original'] == 'L044', 'Wrong original')
    need(not manifest['whole_original_accepted'], 'Author packet must not self-admit')
    result = {'status': 'PASS', 'integrity_checks': len(checked),
              'unique_files': len(set(checked)),
              'scope': 'Own exports, direct dependency pins and every direct acquired manifest export. No new finite enumeration; not a substitute for recursive publication transport or full mathematical review.'}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
