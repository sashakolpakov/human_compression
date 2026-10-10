#!/usr/bin/env python3
"""No-clobber exact finite diagnostics for the written odd-prime family proof."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time

root = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--report', type=Path, required=True)
ap.add_argument('--log', type=Path, required=True)
args = ap.parse_args()
assert not args.report.exists() and not args.log.exists(), 'fresh output paths required'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = root / 'phase49_cover_family_check.g'
before = {source: sha(source)}
for name in ['phase41_chiral_cover_manifest.json', 'phase44_cover_poset_manifest.json',
             'phase46_cover_manifest.json', 'phase48_cover_kernel_manifest.json']:
    mf = root / name
    before[mf] = sha(mf)
    for filename, metadata in json.loads(mf.read_text())['files'].items():
        path = root / filename
        assert sha(path) == metadata['sha256'], filename
        before[path] = metadata['sha256']
start = time.monotonic()
with tempfile.TemporaryDirectory(prefix='phase49_cover_family_') as tmp:
    local = Path(tmp) / 'diagnostic.g'
    local.write_bytes(source.read_bytes())
    result = subprocess.run([shutil.which('gap'), '-q', str(local)], cwd=tmp,
                            text=True, capture_output=True, timeout=900)
elapsed = time.monotonic() - start
assert result.returncode == 0 and not result.stderr.strip(), (result.returncode, result.stdout, result.stderr)
assert not re.search(r'FAIL|Error,|Syntax error', result.stdout), result.stdout
flat = re.sub(r'\s+', ' ', result.stdout.replace('\\\n', ''))
rows = re.findall(r'PARAM_PASS \[ (\d+), (\d+), (\d+) \] orders \[ ([\d, ]+) \]', flat)
expected = [(3, 2, 1), (3, 2, 2), (3, 3, 1), (3, 3, 2)] + [(5, 2, k) for k in range(1, 5)]
assert [tuple(map(int, row[:3])) for row in rows] == expected, rows
records = []
for row in rows:
    p, alpha, k = map(int, row[:3]); q = p ** alpha
    orders = list(map(int, row[3].replace(' ', '').split(',')))
    want = [4*p*p*q, 4*p**3*q, 4*p*p*q, 4*p**4*q, 4*p**4*q, 4*p**5*q]
    assert orders == want, (row, want)
    records.append({'p': p, 'alpha': alpha, 'k': k, 'orders_P_R_T_Q_Qdual_H': orders})
version = re.search(r'PASS GAP (\S+) eight exact finite diagnostics; all-parameter theorem is written', flat)
assert version, result.stdout
for path, digest in before.items():
    assert sha(path) == digest, path
args.log.write_text(result.stdout)
report = {'date': '2026-10-10', 'status': 'PASS', 'GAP_version': version.group(1),
          'seconds': elapsed, 'runner_sha256': sha(Path(__file__)),
          'gap_source_sha256': sha(source), 'log_sha256': sha(args.log),
          'cases': records, 'prior_bound_packages_unchanged': True,
          'checks': ['bare source presentation isomorphisms, exact types and IP',
                     'source and R marked dualities', 'normal x coordinate and quotient mirror',
                     'literal Z=[C²,B]=[A²,B]⁻¹, W rank and action table',
                     'exact normal closure and its parabolic intersections',
                     'trivial extension facet embedding and normal kernel character',
                     'actual R/W to T/J marked isomorphism',
                     'Q,Qdual,H exact orders, end IP, injective restrictions and mirror',
                     'distinct degree-p axes and all conjugation/mirror signs'],
          'scope': 'Eight exact finite diagnostics only. The all-parameter conclusion uses the separate written proof.',
          'retained': ['stock GAP exact group algorithms', 'source theorem identifying P for every parameter',
                       'standard geometric recognition in the written proof'],
          'new_Lean_component': False, 'priority_claim': False}
args.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
