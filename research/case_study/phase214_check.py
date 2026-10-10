#!/usr/bin/env python3
"""Replay the literal n=11 presentation's three index upper certificates.

ACE is not required.  The compressed tables are untrusted naming oracles:
the separate C++ checker has to derive every non-tree transition.
All checks use explicit failures and remain active under python -O.
"""
import argparse
import gzip
import hashlib
import json
import pathlib
import shutil
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(args, *, timeout, expected=0):
    started = time.monotonic()
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    require(result.returncode == expected,
            f"command returned {result.returncode}, expected {expected}: {args}\n"
            f"{result.stdout}\n{result.stderr}")
    return dict(stdout=result.stdout, stderr=result.stderr,
                returncode=result.returncode,
                elapsed_seconds=round(time.monotonic() - started, 6))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=pathlib.Path, required=True)
    options = ap.parse_args()
    require(not options.out.exists() and not options.out.is_symlink(),
            'output directory must be fresh, not an existing path or symlink')
    out = options.out.resolve()
    require(not out.exists(), 'output directory must be fresh')
    out.mkdir(parents=True)
    metadata = json.loads((ROOT / 'phase214_tables.json').read_text())
    cpp = ROOT / 'phase214_table_deduction.cpp'
    require(digest(cpp.read_bytes()) == metadata['checker_sha256'],
            'checker source binding mismatch')
    compiler = shutil.which('c++')
    require(compiler is not None, 'a C++17 compiler is required')
    compiler_version = run([compiler, '--version'], timeout=10)
    binary = out / 'table_deduction'
    compile_report = run([compiler, '-O3', '-std=c++17', str(cpp),
                          '-o', str(binary)], timeout=120)
    reports = []
    for item in metadata['tables']:
        packed = (ROOT / item['path']).read_bytes()
        require(digest(packed) == item['gzip_sha256'], 'compressed binding mismatch')
        raw = gzip.decompress(packed)
        require(len(raw) == item['raw_bytes'], 'raw size mismatch')
        require(digest(raw) == item['raw_sha256'], 'raw binding mismatch')
        table = out / f"table{item['rank']}.txt"
        table.write_bytes(raw)
        result = run([str(binary), str(table)], timeout=180)
        expected = (f"COMPLETE index_upper_bound={item['index_upper_bound']} "
                    f"rank={item['rank']} label=11\n")
        require(result['stdout'] == expected, 'unexpected successful checker output')
        reports.append(dict(rank=item['rank'],
                            index_upper_bound=item['index_upper_bound'],
                            raw_sha256=item['raw_sha256'], **result))
    # This is a perfectly valid permutation representation of EVERY relator,
    # with the facet fixing the sole point.  It is not an index upper proof.
    collapsed = out / 'control_collapsed_one_point.txt'
    collapsed.write_text('1 5\n1 1 1 1 1\n')
    negative1 = run([str(binary), str(collapsed)], timeout=10, expected=2)
    require(negative1['stdout'] == 'INCOMPLETE known=4 total=5\n',
            'one-point lower-bound-only control was not rejected correctly')
    # Alter the defining root-facet loop in the smallest certificate.
    raw3 = (out / 'table3.txt').read_text().splitlines()
    row = raw3[1].split()
    row[0] = '2'
    raw3[1] = ' '.join(row)
    altered = out / 'control_altered_facet.txt'
    altered.write_text('\n'.join(raw3) + '\n')
    negative2 = run([str(binary), str(altered)], timeout=10, expected=1)
    require('deduction disagrees with oracle' in negative2['stderr'],
            'altered facet control was not rejected for the intended reason')
    bounds = {'rank2': 22}
    for item in metadata['tables']:
        d = item['rank']
        bounds[f'rank{d}'] = bounds[f'rank{d-1}'] * item['index_upper_bound']
    require(bounds == {'rank2': 22, 'rank3': 22528, 'rank4': 2147481600,
                       'rank5': 2249598645043200}, 'upper-bound arithmetic mismatch')
    report = dict(status='PASS', scope='literal presentation index upper bounds only',
                  label=11, checker_sha256=metadata['checker_sha256'],
                  tables_metadata_sha256=digest((ROOT / 'phase214_tables.json').read_bytes()),
                  compiler=compiler, compiler_version=compiler_version,
                  compilation=compile_report, tables=reports, order_upper_bounds=bounds,
                  controls={'valid_collapsed_representation': negative1,
                            'altered_facet_loop': negative2},
                  exclusions=['No matrix image computation in this driver.',
                              'No universal-group identification from an upper bound alone.',
                              'No claim that the conjecture is currently open.',
                              'No Lean verification of the table-deduction program.'])
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'order_upper_bounds': bounds,
                      'negative_controls': 2, 'report': str(out / 'report.json')}))


if __name__ == '__main__':
    main()
