#!/usr/bin/env python3
"""Independent replay and adverse-input controls for the frozen public wrapper."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

EXPECTED = '3042fca2289085c469a41e210e06b6beda68620ace46cbf9ba94ec7cdf2c6a56'
NAME = 'phase75_eleven_source_verify.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    root, output = args.input_root.resolve(), args.output_dir.absolute()
    require(not os.path.lexists(output) and not os.path.lexists(args.report), 'Fresh paths required')
    wrapper = root / NAME
    require(digest(wrapper) == EXPECTED, 'Unexpected wrapper')
    # Run the outer wrapper under optimization. Its require checks must survive;
    # code review separately establishes PYTHONOPTIMIZE=0 for the exact child.
    env = dict(os.environ)
    env['PYTHONOPTIMIZE'] = '1'
    command = [sys.executable, '-O', str(wrapper), '--input-root', str(root),
               '--output-dir', str(output), '--run-petrial']
    result = subprocess.run(command, capture_output=True, env=env)
    require(result.returncode == 0 and not result.stderr, repr(result.stderr))
    replay = json.loads((output / 'report.json').read_text())
    require(replay['status'] == 'PASS_STRUCTURAL_AND_FINITE_CONTROLS', 'Replay failed')
    require(len(replay['bound_inputs']) == 29, 'Input inventory changed')
    require(replay['controls_sha256'] == 'fd3426fb348d4414fbcfb64af5b9432e65ad6f56f0cc05907250a4c5b02394ba', 'Controls changed')
    require(replay['contract_rows'] == 87 and replay['old_proof_spans_unchanged'] == 73 and
            replay['old_proof_spans_only_approved_erratum'] == 6 and
            replay['whole_old_sections_unchanged'] == 19 and replay['all_five_programs_byte_exact'], 'Structural counts changed')
    require(not replay['primary_source_spans_checked_by_this_runner'] and
            not replay['mathematical_proof_text_checked_by_this_runner'] and
            not replay['earlier_GAP_programs_reexecuted'], 'Scope changed')
    controls = json.loads((output / 'petrial_results.json').read_text())
    require(controls['summary'] == {'examples': 7, 'nonfaithful_petrial_actions': 2,
                                  'original_chambers': 188, 'thin_petrials': 4}, 'Finite summary changed')
    before = {p.name: digest(p) for p in output.iterdir() if p.is_file()}
    rejected = subprocess.run(command, capture_output=True, env=env)
    require(rejected.returncode != 0 and b'Refusing existing output directory' in rejected.stderr,
            'Existing directory was not rejected')
    require(before == {p.name: digest(p) for p in output.iterdir() if p.is_file()}, 'Replay overwritten')
    adverse = []
    # Every mutation is made to a byte-copy in an isolated temporary tree.
    with tempfile.TemporaryDirectory(prefix='phase77_mutation_') as td:
        temporary = Path(td)
        for name in [NAME, *replay['bound_inputs']]:
            (temporary / name).write_bytes((root / name).read_bytes())
        # The isolated tree deliberately contains no private primary captures.
        require(not (temporary / 'sources').exists(), 'Unexpected private source tree')
        mutations = [
            ('phase65_petrial_integration_manuscript.md', b'Manifest mismatch'),
            ('phase70_petrial_integration_recent_audit.md', b'Manifest mismatch'),
            ('phase37_compress_twogroups_census.g', b'Program differs from embedded source'),
        ]
        for index, (name, expected_error) in enumerate(mutations):
            copied = temporary / name
            original = copied.read_bytes()
            copied.write_bytes(original + b'\n')
            destination = temporary / ('adverse_' + str(index))
            test = subprocess.run([sys.executable, '-O', str(temporary / NAME),
                                   '--input-root', str(temporary), '--output-dir', str(destination)],
                                  capture_output=True, env=env)
            require(test.returncode != 0 and expected_error in test.stderr, 'Mutation accepted: ' + name)
            require(not destination.exists(), 'Output created before input rejection')
            adverse.append({'mutated_copy': name, 'rejected': True,
                            'expected_error': expected_error.decode(), 'output_created': False})
            copied.write_bytes(original)
        isolated = temporary / 'valid_without_private_sources'
        valid = subprocess.run([sys.executable, '-O', str(temporary / NAME), '--output-dir', str(isolated)],
                               capture_output=True, env=env)
        require(valid.returncode == 0 and not valid.stderr, 'Public-only isolated run failed')
        require(json.loads((isolated / 'report.json').read_text())['status'] == 'PASS_STRUCTURAL', 'Bad isolated report')
    for name, expected in replay['bound_inputs'].items():
        require(digest(root / name) == expected, 'Original input modified: ' + name)
    require(digest(wrapper) == EXPECTED, 'Wrapper changed')
    report = {'date': '2026-10-10', 'status': 'PASS', 'checker_sha256': digest(Path(__file__)),
              'wrapper_sha256': EXPECTED, 'input_root': str(root),
              'replay': replay, 'finite_summary': controls['summary'],
              'replay_artifact_hashes': before, 'no_clobber': True,
              'adverse_inputs': adverse, 'isolated_public_only_structure_pass': True,
              'outer_optimized_interpreter': True,
              'child_assertion_enabling': 'verified by full wrapper code review; PYTHONOPTIMIZE=0',
              'public_or_frozen_inputs_modified': False, 'old_GAP_reexecuted': False,
              'mathematical_review_inherited': 'phase70 frozen proof review'}
    with args.report.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'report_sha256': digest(args.report),
                      'control_seconds': replay['control_seconds']}, indent=2))


if __name__ == '__main__':
    main()
