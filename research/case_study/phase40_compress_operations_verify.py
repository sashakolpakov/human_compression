#!/usr/bin/env python3
"""Replay both complete Compress_C appendices without overwriting old evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', default=shutil.which('gap'))
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error('output directory must not exist; historical evidence is preserved')
    if not args.gap:
        parser.error('GAP is required')
    names = ['phase40_compress_operations_check.g',
             'phase40_compress_operations_exhaustive.g']
    manuscript = args.inputs / 'phase40_compress_operations_manuscript.md'
    blocks = re.findall(r'^```gap\n(.*?)^```', manuscript.read_text(), re.M | re.S)
    assert blocks == [(args.inputs / n).read_text() for n in names], 'embedded code differs'
    hashes = {n: digest(args.inputs / n) for n in names + [manuscript.name]}
    query = ('LoadPackage("tomlib");;Print(GAPInfo.Version,"\\n",'
             'PackageInfo("tomlib")[1].Version,"\\n",'
             'Filename(DirectoriesPackageLibrary("tomlib","data"),'
             '"tmjank.tom.gz"),"\\n");QUIT;')
    proc = subprocess.run([args.gap, '-q', '-T', '-c', query],
                          capture_output=True, text=True, timeout=30, check=True)
    versions = proc.stdout.strip().splitlines()
    assert len(versions) == 3 and not proc.stderr, (proc.stdout, proc.stderr)
    software = {'GAP': versions[0], 'TomLib': versions[1],
                'J1_data_name': 'tomlib/data/tmjank.tom.gz',
                'J1_data_sha256': digest(Path(versions[2]))}
    args.output_dir.mkdir(parents=True)
    logs = []
    runs = []
    with tempfile.TemporaryDirectory(prefix='compress-C-complete-') as tmp:
        scratch = Path(tmp)
        for n in names:
            shutil.copyfile(args.inputs / n, scratch / n)
        for n, marker in zip(names, ['COMPRESS_C_J1_PASS', 'COMPRESS_C_EXHAUSTIVE_PASS']):
            logpath = args.output_dir / Path(n).with_suffix('.log').name
            start = time.monotonic()
            with logpath.open('w') as stream:
                proc = subprocess.run([args.gap, '-q', '-T', n], cwd=scratch,
                                      stdout=stream, stderr=subprocess.STDOUT, timeout=900)
            elapsed = time.monotonic() - start
            log = logpath.read_text()
            assert proc.returncode == 0 and 'Error,' not in log, f'failed: {logpath}'
            assert log.rstrip().endswith(marker), f'missing completion: {logpath}'
            assert digest(scratch / n) == hashes[n]
            logs.append(log)
            runs.append({'script': n, 'sha256': hashes[n], 'exit_code': proc.returncode,
                         'seconds': elapsed, 'log': logpath.name,
                         'log_sha256': digest(logpath)})
        classfile = 'phase40_compress_operations_exhaustive_classes.json'
        classes = json.loads((scratch / classfile).read_text())
        assert len(classes[0]) == 6 and classes[1] == [] and len(classes[2]) == 6
        assert len({tuple(p) for p in classes[2]}) == 6
        shutil.copyfile(scratch / classfile, args.output_dir / classfile)
    assert all(digest(args.inputs / n) == h for n, h in hashes.items())
    positive = re.findall(r'^GEOMETRY (\d) .* IP_MEETS 256 HELLY_ROWS 16 PASS$', logs[0], re.M)
    negative = re.findall(r'^NEGATIVE (\d) IP_FAILURES 8 PANELS .* PASS$', logs[0], re.M)
    assert positive == list('123456') and negative == list('12')
    local = [[int(v) for v in row] for row in re.findall(
        r'^LOCAL (\d) MAXIMAL (\d+) ORDER (\d+) ORBITS (\d+) REGULAR (\d+)$', logs[1], re.M)]
    assert len(local) == 14
    assert sum(row[3] for row in local if row[0] == 3) == 245
    assert sum(row[3] for row in local if row[0] == 4) == 1476
    assert sum(row[4] for row in local if row[0] == 3) == 95
    assert sum(row[4] for row in local if row[0] == 4) == 15
    stages = [[int(v) for v in row] for row in re.findall(
        r'^STAGE_TOTAL (\d) TESTED (\d+) ACCEPTED (\d+)$', logs[1], re.M)]
    assert stages == [[4, 100016, 40], [5, 21352, 0]], stages
    report = {
        'status': 'PASS', 'input_hashes': hashes,
        'runner_sha256': digest(Path(__file__)), 'software': software, 'runs': runs,
        'embedded_executables_byte_identical': True,
        'construction': {'geometries': 6, 'marked_meets': 1536, 'global_typed_Helly_rows': 96,
                         'negative_controls': 2, 'source_presentation_index': 1463,
                         'source_presentation_group_order': 175560},
        'census': {'local_rows': local, 'stage_totals': stages,
                   'global_local_triple_classes': 70, 'global_local_quadruple_classes': 15,
                   'rank4_conjugacy_and_type_classes': 6, 'rank5_classes_in_all_subgroups': 0,
                   'classes_sha256': digest(args.output_dir / classfile),
                   'classification_up_to': 'inner conjugation and arbitrary type permutation; distinct parabolic multisets exclude further isomorphism merging',
                   'higher_rank_exclusion': 'regular thin residually connected geometries via actual rank5 residues; not all C-group markings'},
        'retained_inputs': ['complete TomLib J1 subgroup catalogue and permutation model',
                            'GAP exact group, conjugacy, orbit and coset algorithms',
                            'finite Coxeter[3,5] order120 for source-presentation upper bound'],
        'prior_geometry_records_read': False,
        'source_geometry_classification_used_as_premise': False,
        'historical_inputs_unchanged': True,
        'uniform_all_group_and_parameter_theorems': 'written proofs; finite census does not substitute for them',
    }
    (args.output_dir / 'phase40_compress_operations_verify.json').write_text(
        json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('COMPRESS_C_COMPLETE_REPLAY_PASS')


if __name__ == '__main__':
    main()
