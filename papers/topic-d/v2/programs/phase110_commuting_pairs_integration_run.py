#!/usr/bin/env python3
"""Replay only the new complete L066 computation, preserving old certificates."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PREFIX = 'phase110_commuting_pairs_integration_'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def binding(path):
    return dict(path=path.name, bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir = args.output_dir.resolve()
    need(not args.output_dir.exists(), 'Refusing existing output directory')
    gap = shutil.which('gap')
    need(gap is not None, 'GAP executable unavailable')
    args.output_dir.mkdir(parents=True)
    started = time.monotonic()
    finite = ROOT/(PREFIX+'finite.g')
    formula = ROOT/(PREFIX+'formula.py')
    commands = [[gap, '-q', str(finite)],
                [sys.executable, '-O', str(formula), '--output',
                 str(args.output_dir/'formula.json')]]
    for name, command in zip(['finite', 'formula'], commands):
        result = subprocess.run(command, cwd=args.output_dir, capture_output=True, text=True)
        (args.output_dir/(name+'.log')).write_text(result.stdout)
        (args.output_dir/(name+'.stderr')).write_text(result.stderr)
        need(result.returncode == 0 and not result.stderr.strip(), name+' process failed')
        if name == 'finite':
            need(result.stdout.rstrip().endswith('PASS'), 'GAP did not finish its full census')
            need('Error' not in result.stdout and 'Syntax warning' not in result.stdout,
                 'GAP error/warning in stdout')
    text = (args.output_dir/'finite.log').read_text()
    fields = ['group_order','automorphism_order','involutions','commuting_pairs',
              'symmetric_conjugacy_orbits','automorphism_pair_orbits','middle_orbits',
              'generating_triples','IP_survivors','census_IP_meets','explicit_IP_meets']
    summaries = [dict(zip(fields,map(int,line.split('|')[1:])))
                 for line in text.splitlines() if line.startswith('SUMMARY|')]
    need(len(summaries) == 2, 'Missing census summary')
    expected = [[720,1440,75,495,9,5,80,2,2,128,128],
                [360,1440,45,90,2,1,8,0,0,0,0]]
    need([list(row.values()) for row in summaries] == expected, 'Census summary mismatch')
    fibers = [[int(x) for x in line.split('|')[1:]]
              for line in text.splitlines() if line.startswith('FIBER|')]
    survivors = []
    for line in text.splitlines():
        if line.startswith('SURVIVOR|'):
            _, group, index, typ, triple = line.split('|')
            survivors.append(dict(group_order=int(group),source_pair_index=int(index),
                                  type=json.loads(typ),permutations=json.loads(triple)))
    arithmetic = json.loads((args.output_dir/'formula.json').read_text())
    need(arithmetic['status'] == 'PASS' and arithmetic['printed_rows'] == 14,
         'Arithmetic controls incomplete')
    report = dict(status='PASS',scope='Full degree-six endpoints and all regular polyhedra; optional finite arithmetic controls',
                  summaries=summaries,fibers=fibers,survivors=survivors,
                  all_census_IP_meets=128,all_explicit_IP_meets=128,
                  formula_controls=arithmetic,inputs=[binding(finite),binding(formula)],
                  runner=binding(Path(__file__)),
                  outputs=[binding(args.output_dir/x) for x in
                           ['finite.log','finite.stderr','formula.log','formula.stderr','formula.json']],
                  gap_version=next(line.split('|')[1] for line in text.splitlines()
                                   if line.startswith('VERSION|')),
                  elapsed_seconds=round(time.monotonic()-started,6),
                  old_mathematical_certificates_rerun=False,
                  independent_review=False,ratio=None)
    (args.output_dir/'replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
