#!/usr/bin/env python3
"""Compile the exact coprime pullback generation certificate with pinned dependencies.

Adapted from the reviewed phase68 compilation interface. Only the named,
hash-bound source is admitted; existing outputs are never overwritten.
Dependency source checkouts are read only. Compiled dependencies are trusted.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

SOURCE = 'CoprimePullback.lean'
SOURCE_SHA = '4eb20ee7eb85943eab4100b565146a8cd938e4f3c2055b66c6fbbdfa3f68987c'
DEPENDENCY_SHA = '4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3'
DECLARATIONS = {'snd_kernel_mem', 'eq_fiberProduct_of_coprime', 'closure_paired_generators'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packages', type=Path, required=True)
    parser.add_argument('--lean', default='lean')
    parser.add_argument('--source-dir', type=Path,
                        default=Path(__file__).resolve().parent / 'formal')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.absolute()
    require(not output.exists() and not output.is_symlink(), 'Fresh output directory required')
    source = args.source_dir.resolve() / SOURCE
    dependency_file = source.parent / 'dependency_manifest.json'
    require(sha(source) == SOURCE_SHA, 'Frozen source changed')
    require(sha(dependency_file) == DEPENDENCY_SHA, 'Frozen dependency manifest changed')
    require(not re.search(r'\b(sorry|admit|axiom)\b', source.read_text()),
            'Unproved declaration or placeholder in source')
    dependencies = json.loads(dependency_file.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, 'Lean executable not found')
    env = dict(os.environ)
    env['ELAN_TOOLCHAIN'] = dependencies['lean']
    version = subprocess.check_output([lean, '--version'], env=env, text=True).strip()
    expected = dependencies['lean'].split(':')[-1].removeprefix('v')
    require(re.search(r'\bversion ' + re.escape(expected) + r'(?:,|\s|\))', version),
            'Unexpected Lean version')
    checked, libraries = [], []
    for item in dependencies['packages']:
        checkout = args.packages.resolve() / item['name']
        revision = subprocess.check_output(
            ['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
        require(revision == item['rev'], 'Wrong dependency revision: ' + item['name'])
        clean = subprocess.run(['git', '-C', str(checkout), 'diff', '--quiet', 'HEAD', '--'])
        require(clean.returncode == 0, 'Tracked dependency changed: ' + item['name'])
        library = checkout / '.lake/build/lib/lean'
        if library.is_dir():
            libraries.append(library)
        checked.append(dict(name=item['name'], revision=revision,
                            tracked_files_clean=True, compiled_library_present=library.is_dir()))
    env['LEAN_PATH'] = os.pathsep.join(map(str, libraries))
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    run = subprocess.run([lean, '-o', str(output / SOURCE.replace('.lean', '.olean')), str(source)],
                         cwd=source.parent, env=env, capture_output=True, text=True, timeout=120)
    elapsed = time.monotonic() - started
    (output / 'build.log').write_text(run.stdout + run.stderr)
    require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
    require(not re.search(r'sorryAx|native_decide|warning:|error:', run.stdout),
            'Unexpected compiler diagnostic or trust axiom')
    reports = re.findall(
        r"'MathCompression\.CoprimePullback\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]",
        run.stdout)
    require(len(reports) == len(DECLARATIONS) and {n for n, _ in reports} == DECLARATIONS,
            'Missing or duplicate axiom report')
    axioms = {}
    for name, text in reports:
        names = {v.strip() for v in text.split(',') if v.strip()}
        require(names <= {'propext', 'Classical.choice', 'Quot.sound'}, 'Unexpected axioms')
        axioms[name] = sorted(names)
    require(sha(source) == SOURCE_SHA and sha(dependency_file) == DEPENDENCY_SHA,
            'Frozen input changed during execution')
    report = dict(
        status='PASS', date='2026-10-10', source=SOURCE, source_sha256=SOURCE_SHA,
        runner_sha256=sha(Path(__file__)), dependency_manifest_sha256=DEPENDENCY_SHA,
        lean=version, seconds=elapsed, dependencies=checked, axiom_reports=axioms,
        build_log_sha256=sha(output / 'build.log'), exit_code=run.returncode,
        stdout=run.stdout, stderr=run.stderr,
        trust_boundary='Pinned dependency revisions and tracked-file cleanliness checked; '
                       'existing compiled dependency objects remain trusted build inputs.',
        scope='Complete coprime subdirect fiber-product theorem, kernel isolation, and paired-generator closure corollary; classical group reasoning.',
        exclusions=['intersection property of a particular cover', 'all-parabolic geometric specialization', 'source presentation recognition', 'historical priority or open-conjecture claim'],
        native_evaluation_axioms=False, unproved_placeholders=False)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', declarations=len(axioms), seconds=elapsed,
                          output=str(output)), indent=2))


if __name__ == '__main__':
    main()
