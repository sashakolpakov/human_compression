#!/usr/bin/env python3
"""Independent isolated replay and preservation controls for frozen parity mix."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

MANIFEST_SHA = 'ed486ab555336588356b93622fa1cb769d7fbc8a09543dab53c9f99ba10410e0'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    result = {}
    for p in sorted(root.rglob('*')):
        key = str(p.relative_to(root))
        if p.is_symlink():
            result[key] = ['symlink', str(p.readlink())]
        elif p.is_file():
            result[key] = ['file', sha(p)]
        elif p.is_dir():
            result[key] = ['directory']
        else:
            raise RuntimeError('Unexpected file type: ' + key)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--packages', type=Path, required=True)
    ap.add_argument('--lean', required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--full-retained-binding-audit', action='store_true',
                    help='Also check the documentary retained inputs; not needed for public arithmetic.')
    args = ap.parse_args()
    out = args.output_dir.absolute()
    require(not os.path.lexists(out), 'New audit output required')
    root = args.study_root.resolve()
    manifest = root / 'phase146_parity_mix_manifest.json'
    require(sha(manifest) == MANIFEST_SHA, 'Changed frozen author manifest')
    m = json.loads(manifest.read_text())
    entries = {r['path']: r for r in m['exports'] + m['retained_inputs']}
    selected = list(entries) if args.full_retained_binding_audit else m['default_replay_files']
    for name in selected:
        p = root / name
        require(p.is_file() and not p.is_symlink(), 'Missing regular bound input: ' + name)
        require(sha(p) == entries[name]['sha256'] and
                p.stat().st_size == entries[name]['utf8_bytes'], 'Changed bound input: ' + name)
    out.mkdir(parents=True, exist_ok=False)
    stage = out / 'math_compression' / 'research' / 'case_study'
    stage.mkdir(parents=True)
    for name in m['default_replay_files']:
        dst = stage / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, dst)
    require(sum(p.is_file() for p in stage.rglob('*')) == 21, 'Replay closure not exactly21 files')
    baseline = snapshot(stage)
    cases = []
    env = dict(os.environ)
    env['LEAN_PATH'] = '/nonexistent/phase157_deliberately_invalid_inherited_path'

    def run_wrapper(wrapper, output):
        return subprocess.run([sys.executable, '-B', '-O', str(stage / wrapper),
                               '--packages', str(args.packages.resolve()), '--lean', args.lean,
                               '--output-dir', str(output)],
                              cwd=stage, env=env, text=True, capture_output=True, timeout=180)

    fresh = out / 'isolated_build'
    run = run_wrapper('phase146_parity_mix_check.py', fresh)
    (out / 'isolated_stdout.txt').write_text(run.stdout)
    (out / 'isolated_stderr.txt').write_text(run.stderr)
    require(run.returncode == 0 and not run.stderr, 'Isolated compile failed: ' + run.stderr)
    build = json.loads((fresh / 'report.json').read_text())
    require(build['status'] == 'PASS' and len(build['builds']) == 18, 'Incomplete fresh build')
    total = 0
    for row in build['builds']:
        require(row['source_sha256'] == entries['formal/' + row['source']]['sha256'],
                'Unexpected executed source')
        for declaration, axioms in row['axiom_reports'].items():
            require(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}, declaration)
            total += 1
    require(total == 75 and snapshot(stage) == baseline, 'Incomplete proof reports or mutated stage')
    cases.append({'case': 'isolated_21_file_optimized_replay', 'status': 'PASS',
                  'proof_reports': total, 'ambient_LEAN_PATH_replaced': True})

    for number, name in enumerate(['formal/ParityMixTheorem.lean',
                                   'formal/FinIntervalOverlapCancellation.lean',
                                   'formal/dependency_manifest.json']):
        p = stage / name
        original = p.read_bytes()
        p.write_bytes(original + b'\n')
        target = out / ('rejected_mutation_' + str(number))
        run = run_wrapper('phase146_parity_mix_check.py', target)
        p.write_bytes(original)
        require(run.returncode != 0 and 'Frozen ' in run.stderr and
                not os.path.lexists(target) and snapshot(stage) == baseline,
                'Mutation rejection failed: ' + name)
        cases.append({'case': 'mutation_' + name, 'status': 'PASS',
                      'exit_code': run.returncode, 'stderr': run.stderr})

    occupied = out / 'occupied'
    occupied.mkdir()
    regular = occupied / 'regular'
    regular.write_bytes(b'unchanged regular file\n')
    directory = occupied / 'directory'
    directory.mkdir()
    (directory / 'nested').mkdir()
    (directory / 'nested' / 'sentinel').write_bytes(b'unchanged nested contents\n')
    live = occupied / 'live'
    live.symlink_to(regular)
    dangling = occupied / 'dangling'
    dangling.symlink_to(occupied / 'absent')
    occupied_before = snapshot(occupied)
    for wrapper in ['phase146_parity_mix_check.py', 'phase146_parity_mix_controls.py']:
        for target in [regular, directory, live, dangling]:
            run = run_wrapper(wrapper, target)
            require(run.returncode != 0 and 'Fresh ' in run.stderr and
                    snapshot(occupied) == occupied_before and snapshot(stage) == baseline,
                    'Occupied path changed or not rejected')
            cases.append({'case': wrapper + ':' + target.name, 'status': 'PASS',
                          'exit_code': run.returncode, 'stderr': run.stderr})
    require(len(cases) == 12, 'Unexpected case count')
    for name in selected:
        require(sha(root / name) == entries[name]['sha256'], 'Original source changed')
    report = {'status': 'PASS', 'independent_control_program_sha256': sha(Path(__file__)),
              'author_manifest_sha256': MANIFEST_SHA,
              'frozen_input_bindings_checked': len(selected),
              'full_retained_binding_audit': args.full_retained_binding_audit,
              'isolated_source_file_count': 21, 'no_primary_sources_or_manuscripts_in_replay': True,
              'cases': cases, 'case_count': len(cases),
              'all_occupied_and_source_snapshots_unchanged': True,
              'portable_build_report_sha256': sha(fresh / 'report.json'),
              'axiom_reports': {r['source']: r['axiom_reports'] for r in build['builds']},
              'compiler_seconds': sum(r['seconds'] for r in build['builds']),
              'independence_scope': 'Independent input/staging/controls implementation; compiled proof and wrapper are the exact author files, not a second formal proof.'}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'case_count': len(cases),
                      'compiler_seconds': report['compiler_seconds']}, indent=2))


if __name__ == '__main__':
    main()
