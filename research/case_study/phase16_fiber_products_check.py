#!/usr/bin/env python3
"""Run and bind exact finite-presentation diagnostics; no source PDF needed."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gap', default=shutil.which('gap'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not args.gap:
        parser.error('GAP is required; use --gap /path/to/gap')
    here = Path(__file__).resolve().parent
    output = args.output or here / 'phase16_fiber_products_check.json'
    script = here / 'phase16_fiber_products_check.g'
    run = subprocess.run([args.gap, '-q', str(script)], capture_output=True,
                         text=True, timeout=180)
    log = output.with_suffix('.log')
    log.write_text(run.stdout + run.stderr)
    assert run.returncode == 0 and 'Error' not in run.stdout + run.stderr
    pattern = (r'PASS parameters=\[([\d, ]+)\] rank=(\d+) order=(\d+)'
               r' kernel=(\d+) maps=(\d+) meets=(\d+)')
    cases = []
    for match in re.finditer(pattern, run.stdout):
        ns = [int(x) for x in match[1].split(',')]
        rank, order, kernel, maps, meets = map(int, match.groups()[1:])
        assert rank == len(ns) + 2
        assert order == 2**(sum(ns) - 3*(rank - 3))
        assert kernel == 2**sum(n - 5 for n in ns)
        assert maps == 2**rank and meets == maps**2
        cases.append(dict(parameters=ns, rank=rank, order=order,
                          kernel_order=kernel, maps=maps, meets=meets))
    assert [x['parameters'] for x in cases] == [
        [5], [6], [7], [5,6], [6,6], [5,7], [6,5,6], [5,6,5]]
    assert 'PASS all presentation, local-group, Boolean-map, IP and kernel checks' in run.stdout
    version = subprocess.run([args.gap, '-q', '-c', 'Print(GAPInfo.Version);QUIT;'],
                             capture_output=True, text=True, timeout=20).stdout.strip()
    report = dict(status='PASS', scope='Eight exact finite-presentation diagnostics only',
                  gap_version=version, cases=cases,
                  total_maps=sum(x['maps'] for x in cases),
                  total_meets=sum(x['meets'] for x in cases),
                  input_sha256={p.name: digest(p) for p in [script, Path(__file__),
                      here / 'phase16_fiber_products.md']}, log_sha256=digest(log))
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'total_maps', 'total_meets']}))


if __name__ == '__main__':
    main()
