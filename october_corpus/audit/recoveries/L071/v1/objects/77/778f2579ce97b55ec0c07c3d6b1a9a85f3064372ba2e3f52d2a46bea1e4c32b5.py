#!/usr/bin/env python3
"""Replay the complete census and rebuild the bounded mathematical note."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--source-root', type=Path)
args = parser.parse_args()
packet = Path(__file__).resolve().parent
args.out.mkdir(parents=True, exist_ok=False)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((packet / 'manifest.json').read_text())
for entry in manifest['exports']:
    p = packet / entry['path']
    if p.stat().st_size != entry['bytes'] or sha(p) != entry['sha256']:
        raise ValueError('Export mismatch: ' + entry['path'])
source_checks = 0
if args.source_root:
    for entry in json.loads((packet / 'source_map.json').read_text())['bindings']:
        p = args.source_root / entry['path']
        if sha(p) != entry['sha256']:
            raise ValueError('Source mismatch: ' + entry['path'])
        source_checks += 1

subprocess.run([sys.executable, str(packet / 'check_h3.py'), '--out',
                str(args.out / 'census')], check=True, timeout=60)
got = json.loads((args.out / 'census/report.json').read_text())
retained = json.loads((packet / 'census/report.json').read_text())
for key in retained:
    if key != 'elapsed_seconds' and got[key] != retained[key]:
        raise ValueError('Census mismatch: ' + key)
counts = [(x['rank'], x['count'], x['self_dual'], x['connected'])
          for x in got['rows']]
if counts != [(1,0,0,0), (2,0,0,0), (3,8,1,8), (4,3,0,0),
              (5,0,0,0), (6,0,0,0)]:
    raise ValueError('Unexpected census')

tex = packet / 'disconnected_strings.tex'
for n in range(2):
    run = subprocess.run(['/opt/homebrew/bin/pdflatex', '-halt-on-error',
                          '-interaction=nonstopmode',
                          '-output-directory=' + str(args.out), str(tex)],
                         cwd=packet, capture_output=True, timeout=60)
    (args.out / ('build%d.log' % n)).write_bytes(run.stdout + run.stderr)
    run.check_returncode()
prior = [p.extract_text() for p in PdfReader(packet / 'disconnected_strings.pdf').pages]
fresh = [p.extract_text() for p in PdfReader(args.out / 'disconnected_strings.pdf').pages]
if fresh != prior:
    raise ValueError('Rebuilt document text differs')
report = dict(status='PASS', exports_verified=len(manifest['exports']),
              source_bindings_verified=source_checks, census_replayed=True,
              all_representatives_equal=True, exact_native_pages=len(fresh),
              author_manifest_sha256=sha(packet / 'manifest.json'),
              whole_original_credit=0, new_question_credit=0,
              new_formal_credit=0)
(args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
