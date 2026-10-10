#!/usr/bin/env python3
"""Reproduce L088 in scratch; require a new empty output directory."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', default=shutil.which('gap'))
    args = parser.parse_args()
    if not args.gap:
        parser.error('GAP must be installed or supplied with --gap')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if any(args.output_dir.iterdir()):
        parser.error('--output-dir must be empty; historical reports are never overwritten')
    inputs = ['phase24_L088_seed.json', 'phase24_L088_check.g',
              'phase24_L088_presentation.g', 'phase24_L088_data_check.py']
    hashes = {n: digest(args.inputs/n) for n in inputs}
    query = ('LoadPackage("tomlib");;Print(GAPInfo.Version,"\\n",'
             'PackageInfo("tomlib")[1].Version,"\\n",'
             'Filename(DirectoriesPackageLibrary("tomlib","data"),'
             '"tmjank.tom.gz"),"\\n");QUIT;')
    version = subprocess.run([args.gap, '-q', '-T', '-c', query],
                             text=True, capture_output=True, timeout=30,
                             check=True).stdout.strip().splitlines()
    assert len(version) == 3, version
    software = {'GAP': version[0], 'TomLib': version[1],
                'tomlib_data': 'tomlib/data/tmjank.tom.gz',
                'tomlib_data_sha256': digest(Path(version[2]))}
    outputs = ['phase24_L088_check.log', 'phase24_L088_results.json',
               'phase24_L088_presentation.log', 'phase24_L088_coset_table.json',
               'phase24_L088_run.json', 'phase24_L088_data_check.json']
    with tempfile.TemporaryDirectory(prefix='L088-reproduction-') as temp:
        scratch = Path(temp)
        for n in inputs:
            shutil.copyfile(args.inputs/n, scratch/n)
        runs = []
        for script, marker in [('phase24_L088_check.g', 'L088_ALL_SIX_PASS'),
                               ('phase24_L088_presentation.g', 'PRESENTATION_PASS')]:
            start = time.monotonic()
            proc = subprocess.run([args.gap, '-q', '-T', script], cwd=scratch,
                                  text=True, capture_output=True, timeout=60)
            elapsed = time.monotonic()-start
            text = proc.stdout+proc.stderr
            log = Path(script).with_suffix('.log').name
            (scratch/log).write_text(text)
            if proc.returncode or marker not in text or 'Error,' in text:
                (args.output_dir/log).write_text(text)
                raise RuntimeError(f'{script} failed; see {log}')
            assert digest(scratch/script) == hashes[script]
            runs.append({'script': script, 'sha256': hashes[script],
                         'exit_code': proc.returncode, 'seconds': elapsed,
                         'log': log, 'log_sha256': digest(scratch/log)})
        report = {'status': 'PASS',
                  'date_utc': datetime.now(timezone.utc).isoformat(),
                  'runs': runs, 'software': software,
                  'input_hashes': hashes,
                  'runner_sha256': digest(Path(__file__)),
                  'scope': 'Six explicit markings and exact source presentation; no global classification census.',
                  'scratch_execution': True, 'historical_inputs_unchanged': True}
        (scratch/'phase24_L088_run.json').write_text(json.dumps(report, indent=2)+'\n')
        subprocess.run([sys.executable, 'phase24_L088_data_check.py'],
                       cwd=scratch, check=True, timeout=30)
        for n in inputs:
            assert digest(args.inputs/n) == hashes[n]
        for n in outputs:
            shutil.copyfile(scratch/n, args.output_dir/n)
    print('L088_SCRATCH_REPRODUCTION_PASS', len(outputs), 'outputs')


if __name__ == '__main__':
    main()
