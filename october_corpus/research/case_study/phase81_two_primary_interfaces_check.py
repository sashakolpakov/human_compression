#!/usr/bin/env python3
"""Independent wrapper/interface checks; expects a completed fresh phase80 replay.

Does not rerun GAP and does not prove the written parameter reductions.
Every rejection is tested through the optimized Python CLI on isolated copies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

RUNNER = 'phase80_two_primary_verify.py'
RUNNER_SHA = '448ca96943d25673fccc2f942f60a728cff68ae87a37c1ce78b8de9a7fdd5df2'
REVIEWS = {
 'phase73_2primary_cover_recent_audit_manifest.json': '2b814f3464b0d49da03f03e5e6dfc5cf1923ff400f449a4c943b94ff61ec07e1',
 'phase74_coprime_cover_recent_audit_manifest.json': '749d3f79c57f255b1e62bf9c702232658623e4fe58487255f606c31d9bd59a0a',
}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def require(value, message):
    if not value: raise ValueError(message)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-root', type=Path, required=True)
    p.add_argument('--private-root', type=Path, required=True)
    p.add_argument('--replay-dir', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    args = p.parse_args()
    require(not args.report.exists() and not args.report.is_symlink(), 'New report required')
    root = args.input_root
    bound = dict(REVIEWS)
    for name, expected in REVIEWS.items():
        require(sha(root / name) == expected, 'Review manifest changed')
        for name, entry in json.loads((root / name).read_text())['files'].items():
            require(name == Path(name).name, 'Nested path')
            require(name not in bound or bound[name] == entry['sha256'], 'Conflicting bindings')
            bound[name] = entry['sha256']
    require(len(bound) == 33, '33 reviewed original inputs')
    bound[RUNNER] = RUNNER_SHA
    for name, expected in bound.items():
        require(sha(root / name) == expected, 'Public input changed: ' + name)
        require(sha(args.private_root / name) == expected, 'Private/public mismatch: ' + name)
    report_path = args.replay_dir / 'report.json'
    replay = json.loads(report_path.read_text())
    require(replay['status'] == 'PASS' and replay['runner_sha256'] == RUNNER_SHA, 'Fresh replay failed')
    require(replay['bound_inputs'] == {k:v for k,v in bound.items() if k != RUNNER}, 'Replay bindings')
    require(replay['all_bound_inputs_and_executed_copies_unchanged'], 'Replay changed input')
    require(len(replay['runs']) == 3 and all(r['passed'] for r in replay['runs']), 'Three GAP replays')
    for row in replay['runs']:
        require(sha(args.replay_dir / row['program']) == bound[row['program']], 'Executed source copy')
        for stream in ('stdout', 'stderr'):
            require(sha(args.replay_dir / (row['program'] + '.' + stream + '.log')) == row[stream + '_sha256'], 'Raw stream hash')
    for name, expected in replay['expected_log_sha256'].items():
        require(sha(args.replay_dir / name) == expected, 'Prior canonical log mismatch')
    require(all(replay['exact_prior_log_matches'].values()), 'Prior log comparison')
    require(replay['GAP_version'] == '4.15.1', 'GAP version')
    require(replay['integer_model']['sparse_sum'] == {'1':-2, '40':2}, 'Exact integer sum')

    mutations = [
        'phase58_2primary_cover_theorem.md', 'phase66_coprime_cover_theorem.md',
        'phase58_2primary_cover_check.g', 'phase58_2primary_cover_extension_check.g',
        'phase66_coprime_cover_check.g', 'phase66_coprime_cover_permutation_model.json',
        'phase66_coprime_cover_coefficients.json', 'phase73_2primary_cover_recent_audit.md',
        'phase74_coprime_cover_recent_audit.md', *REVIEWS,
    ]
    checks = []
    with tempfile.TemporaryDirectory(prefix='phase81-rejection-', dir='/private/tmp') as temporary:
        temp = Path(temporary)
        for index, name in enumerate(mutations):
            case = temp / str(index)
            case.mkdir()
            for filename in bound: shutil.copyfile(root / filename, case / filename)
            (case / name).write_bytes((case / name).read_bytes() + b'\n')
            output = temp / ('output-' + str(index))
            run = subprocess.run([sys.executable, '-O', str(case / RUNNER), '--output-dir', str(output)], capture_output=True)
            message = (run.stdout + run.stderr).decode()
            require(run.returncode != 0 and 'changed:' in message and not output.exists(), 'Mutation accepted: ' + name)
            checks.append(dict(kind='bound_input_mutation', input=name, exit_code=run.returncode, output_created=False))
        # Neither a directory, an ordinary file, nor a dangling symlink may be replaced.
        for kind in ('directory', 'file', 'dangling_symlink'):
            output = temp / ('existing-' + kind)
            if kind == 'directory':
                output.mkdir(); (output / 'sentinel').write_bytes(b'preserve')
            elif kind == 'file': output.write_bytes(b'preserve')
            else: output.symlink_to(temp / 'never-created')
            run = subprocess.run([sys.executable, '-O', str(root / RUNNER), '--output-dir', str(output)], capture_output=True)
            require(run.returncode != 0 and b'output path exists' in run.stderr, 'Existing path accepted')
            require((output.is_dir() and (output / 'sentinel').read_bytes() == b'preserve') if kind == 'directory'
                    else output.read_bytes() == b'preserve' if kind == 'file'
                    else output.is_symlink() and output.readlink() == temp / 'never-created', 'Existing path altered')
            checks.append(dict(kind='no_clobber_' + kind, exit_code=run.returncode, existing_path_preserved=True))
    for name, expected in bound.items():
        require(sha(root / name) == sha(args.private_root / name) == expected, 'Original changed during audit')
    result = dict(status='PASS', runner_sha256=RUNNER_SHA, bound_originals=len(bound)-1,
                  public_private_byte_identity=True, optimized_python_rejections=checks,
                  independent_fresh_replay_report_sha256=sha(report_path),
                  independent_fresh_replay_seconds=sum(row['elapsed_seconds'] for row in replay['runs']),
                  canonical_log_sha256=replay['expected_log_sha256'],
                  isolated_replay_scope='33 bound inputs plus unchanged wrapper; no other private inputs',
                  all_originals_unchanged=True, new_mathematical_or_Lean_claim=False)
    args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
if __name__ == '__main__': main()
