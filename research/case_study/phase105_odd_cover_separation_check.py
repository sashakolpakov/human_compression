#!/usr/bin/env python3
"""Compile the exact odd-cover separation certificate with pinned dependencies.

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

SOURCE = 'OddCoverSeparation.lean'
SOURCE_SHA = '3ae3d89b561edf9b5e536863383405b4476b692ada4cc95ac1b5cbc9d0aadec1'
DEPENDENCY_SHA = '4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3'
DECLARATIONS = {
    'kernelMap_surjective', 'kernel_card_dvd', 'odd_kernel_of_quotient',
    'no_even_kernel_factor', 'no_double_cover_factor',
    'exists_maximal_admissible_kernel',
}


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
        r"'MathCompression\.OddCoverSeparation\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]",
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
        scope='Kernel-cardinality divisibility and odd-degree inheritance under surjective '
              'maps over a common base; exclusion of even-kernel factors; finite maximal '
              'admissible normal kernel for an explicit arbitrary predicate.',
        exclusions=['construction of an odd-degree polytopal cover',
                    'intersection property or family transport',
                    'formal definition of polytopes or cover/quotient correspondence',
                    'historical novelty or open-conjecture status'],
        native_evaluation_axioms=False, unproved_placeholders=False)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', declarations=len(axioms), seconds=elapsed,
                          output=str(output)), indent=2))


if __name__ == '__main__':
    main()
