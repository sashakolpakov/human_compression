#!/usr/bin/env python3
"""Independent isolated replay and interface controls for frozen phase105."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

MANIFEST = 'phase105_odd_cover_separation_manifest.json'
MANIFEST_SHA = '751538c486b332aec54437dd49e17d84b76ecddacedbc83fb2ddfc6373301628'
RUNNER = 'phase105_odd_cover_separation_check.py'
SOURCE = 'formal/OddCoverSeparation.lean'
DEPENDENCY = 'formal/dependency_manifest.json'


def require(value, message):
    if not value:
        raise RuntimeError(message)


def binding(path):
    data = path.read_bytes()
    return dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--packages', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    args = parser.parse_args()
    root = args.study_root.resolve()
    out = args.output_dir.absolute()
    require(not os.path.lexists(out), 'New review output required')
    require(binding(root / MANIFEST)['sha256'] == MANIFEST_SHA, 'Author manifest changed')
    manifest = json.loads((root / MANIFEST).read_text())
    retained = {**manifest['files'], **manifest['retained_inputs']}
    for name, expected in retained.items():
        require(binding(root / name) == expected, 'Author binding changed: ' + name)
    originals = {name: binding(root / name) for name in [*retained, MANIFEST]}
    require(set(manifest['export_allowlist']) == set(manifest['files']) | {MANIFEST},
            'Author allowlist differs')
    out.mkdir(parents=False)
    isolated = out / 'isolated'
    (isolated / 'formal').mkdir(parents=True)
    for name in [RUNNER, SOURCE, DEPENDENCY]:
        shutil.copyfile(root / name, isolated / name)
    isolated_inputs = {name: binding(isolated / name) for name in [RUNNER, SOURCE, DEPENDENCY]}

    def run(target):
        argv = [sys.executable, '-O', str(isolated / RUNNER),
                '--packages', str(args.packages.resolve()),
                '--lean', str(args.lean.resolve()), '--output-dir', str(target)]
        result = subprocess.run(argv, cwd=out, capture_output=True, text=True, timeout=150)
        return result, argv

    build = out / 'build'
    result, argv = run(build)
    (out / 'wrapper.stdout.txt').write_text(result.stdout)
    (out / 'wrapper.stderr.txt').write_text(result.stderr)
    require(result.returncode == 0, result.stdout + result.stderr)
    require(not result.stderr, 'Independent replay stderr')
    replay = json.loads((build / 'report.json').read_text())
    require(replay['status'] == 'PASS' and len(replay['axiom_reports']) == 6, 'Six claims not compiled')
    require((build / 'build.log').read_bytes() == (root / 'phase105_odd_cover_separation_build.log').read_bytes(),
            'Compiler axiom output differs')
    initial_outputs = {p.name: binding(p) for p in build.iterdir() if p.is_file()}
    controls = []
    occupied_file = out / 'occupied-file'
    occupied_file.write_text('preserve\n')
    missing = out / 'missing-target'
    occupied_link = out / 'occupied-link'
    occupied_link.symlink_to(missing)
    for kind, target in [('populated-directory', build), ('file', occupied_file),
                         ('dangling-symlink', occupied_link)]:
        result, _ = run(target)
        require(result.returncode != 0 and 'Fresh output directory required' in result.stderr,
                'No-clobber rejection failed: ' + kind)
        controls.append(dict(kind=kind, returncode=result.returncode,
                             stderr=result.stderr, rejected=True))
    require(occupied_file.read_text() == 'preserve\n', 'Occupied file changed')
    require(occupied_link.is_symlink() and not missing.exists(), 'Occupied link changed')
    require(initial_outputs == {p.name: binding(p) for p in build.iterdir() if p.is_file()},
            'Successful build was overwritten')
    for name, label, error in [(SOURCE, 'source', 'Frozen source changed'),
                               (DEPENDENCY, 'dependency', 'Frozen dependency manifest changed')]:
        target = isolated / name
        original = target.read_bytes()
        target.write_bytes(original + b'\n')
        rejected_output = out / ('rejected-' + label)
        try:
            result, _ = run(rejected_output)
            require(result.returncode != 0 and error in result.stderr, 'Mutation not rejected')
            require(not os.path.lexists(rejected_output), 'Mutation created output')
            controls.append(dict(kind=label + '-mutation', returncode=result.returncode,
                                 stderr=result.stderr, rejected=True, output_absent=True))
        finally:
            target.write_bytes(original)
    require(isolated_inputs == {name: binding(isolated / name) for name in isolated_inputs},
            'Isolated frozen inputs changed')
    require(originals == {name: binding(root / name) for name in originals},
            'Original author inputs changed')
    report = dict(status='PASS', date='2026-10-10', author_manifest_sha256=MANIFEST_SHA,
                  review_runner=binding(Path(__file__)), reviewed_inputs=originals,
                  isolated_inputs=isolated_inputs, original_inputs_unchanged=True,
                  isolated_inputs_restored=True, full_compiler_replay=replay,
                  exact_original_compiler_log=True, optimized_python=True,
                  replay_command=argv, compiler_seconds=replay['seconds'],
                  no_clobber_cases=3, mutation_cases=2, controls=controls,
                  successful_build_files_preserved=initial_outputs,
                  portability='Only the exact runner, Lean source and dependency manifest were copied; compilation from an unrelated working directory succeeded using explicit external pinned packages and Lean.',
                  trust_boundary=replay['trust_boundary'],
                  mathematical_review_separate=True, public_files_modified=False)
    with (out / 'review.json').open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(status='PASS', seconds=replay['seconds'], declarations=6,
                          no_clobber=3, mutations=2, report=binding(out / 'review.json')), indent=2))


if __name__ == '__main__':
    main()
