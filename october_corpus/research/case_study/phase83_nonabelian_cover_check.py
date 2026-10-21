#!/usr/bin/env python3
"""Replay the original-cell certificate and compile its narrowly scoped Lean proof.

Uses only distributed study files, pinned package checkouts and their existing
compiled libraries. Output must be new; no GAP simplifier is a proof input.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
MODEL_HASH = '0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338'


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closure(gens):
    identity = tuple(range(1, 129))
    elements, seen = [identity], {identity}
    for a in elements:
        for b in gens:
            product = tuple(b[i-1] for i in a)
            if product not in seen:
                elements.append(product)
                seen.add(product)
    return seen


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packages', type=Path, required=True)
    ap.add_argument('--lean', default='lean')
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(), 'New output directory required')
    names = ['phase66_coprime_cover_permutation_model.json', 'phase83_word_elimination.py',
             'phase83_word_elimination.json', 'phase83_generate_lean.py',
             'formal/OddKernelWord.lean', 'formal/dependency_manifest.json']
    before = {name: sha(ROOT / name) for name in names}
    require(before[names[0]] == MODEL_HASH, 'Reviewed coset model changed')
    model = json.loads((ROOT / names[0]).read_text())
    generators = [tuple(g) for g in model['generators']]
    require(model['degree'] == 128 and len(generators) == 4, 'Wrong model degree')
    require(all(sorted(g) == list(range(1, 129)) for g in generators), 'Invalid permutation')
    require(all(all(g[g[i]-1] == i+1 for i in range(128)) for g in generators), 'Marks not involutions')
    group = closure(generators)
    medial = closure(generators[1:3])
    require(len(group) == 1024 and len(medial) == 8, 'Wrong marked group order')
    require({g for g in group if g[0] == 1} == medial, 'C is not the full stabilizer')
    require({g[0] for g in group} == set(range(1, 129)), 'Nontransitive model')
    point = 1
    for letter in model['z_word_1based']:
        require(type(letter) is int and 1 <= letter <= 4, 'Invalid z word')
        point = generators[letter-1][point-1]
    require(point == 40, 'Wrong distinguished defect coset')
    base = (1, generators[3][0], generators[0][0], generators[0][generators[3][0]-1])
    quads = {tuple(g[i-1] for i in base) for g in group}
    require(len(quads) == 1024 and base == (1, 2, 39, 77), 'Wrong cell orbit')
    lean_source = (ROOT / 'formal/OddKernelWord.lean').read_text()
    cell_block = lean_source.split('def requiredCells :', 1)[1].split(']\n', 1)[0]
    cells = [tuple(map(int, cell)) for cell in re.findall(r'\((\d+), (\d+), (\d+), (\d+)\)', cell_block)]
    require(len(cells) == len(set(cells)) == 35, 'Wrong formal cell list')
    require(set(cells) <= quads, 'A formal cell is outside the actual orbit')
    require(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',
                          re.sub(r'/\-.*?\-/', '', lean_source, flags=re.S)), 'Unapproved Lean proof construct')

    dependency_file = ROOT / 'formal/dependency_manifest.json'
    dependencies = json.loads(dependency_file.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, 'Lean executable unavailable')
    env = dict(os.environ)
    env['ELAN_TOOLCHAIN'] = dependencies['lean']
    version = subprocess.check_output([lean, '--version'], env=env, text=True).strip()
    expected = dependencies['lean'].split(':')[-1].removeprefix('v')
    require(re.search(r'\bversion ' + re.escape(expected) + r'(?:,|\s|\))', version), 'Wrong Lean version')
    checked, libraries = [], []
    for item in dependencies['packages']:
        checkout = args.packages.resolve() / item['name']
        rev = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
        require(rev == item['rev'], 'Wrong package revision: ' + item['name'])
        require(subprocess.run(['git', '-C', str(checkout), 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
                'Tracked package changes: ' + item['name'])
        library = checkout / '.lake/build/lib/lean'
        if library.is_dir():
            libraries.append(library)
        checked.append(dict(name=item['name'], revision=rev, tracked_files_clean=True,
                            compiled_library_present=library.is_dir()))
    env['LEAN_PATH'] = os.pathsep.join(map(str, libraries))
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    for script, target in [('phase83_word_elimination.py', 'phase83_word_elimination.json'),
                           ('phase83_generate_lean.py', 'OddKernelWord.lean')]:
        proc = subprocess.run([sys.executable, '-O', str(ROOT / script), '--output', str(output / target)],
                              capture_output=True, text=True, timeout=120)
        (output / (script + '.log')).write_text(proc.stdout + proc.stderr)
        require(proc.returncode == 0 and not proc.stderr.strip(), 'Regeneration failed: ' + script)
        original = ROOT / ('formal/' + target if target.endswith('.lean') else target)
        require((output / target).read_bytes() == original.read_bytes(), 'Regenerated artifact differs: ' + target)
    result = subprocess.run([lean, '-o', str(output / 'OddKernelWord.olean'), str(output / 'OddKernelWord.lean')],
                            cwd=output, env=env, capture_output=True, text=True, timeout=120)
    (output / 'build.log').write_text(result.stdout + result.stderr)
    require(result.returncode == 0 and not result.stderr.strip() and
            not re.search(r'sorryAx|native_decide|warning:|error:', result.stdout), 'Lean compilation failed')
    declarations = {'defect_square', 'defect_trivial_of_odd_card'}
    reports = re.findall(r"'MathCompression\.OddKernelWord\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]", result.stdout)
    require(len(reports) == 2 and {name for name, _ in reports} == declarations, 'Incomplete axiom report')
    axioms = {name: sorted({a.strip() for a in values.split(',') if a.strip()}) for name, values in reports}
    require(all(set(values) <= {'propext', 'Classical.choice', 'Quot.sound'} for values in axioms.values()),
            'Unapproved axiom')
    require(before == {name: sha(ROOT / name) for name in names}, 'Bound input changed during replay')
    cert = json.loads((output / 'phase83_word_elimination.json').read_text())
    report = dict(status='PASS', date='2026-10-10', runner_sha256=sha(Path(__file__)),
                  seconds=time.monotonic()-started, input_sha256=before,
                  coset_degree=128, group_order=1024, stabilizer_order=8, cell_orbit_size=1024,
                  formal_cells=35, formal_cells_in_actual_orbit=True, defect_point=40,
                  trace_eliminations=len(cert['steps']), lean_eliminations=34,
                  regenerated_trace_identical=True, regenerated_lean_identical=True,
                  lean=version, dependency_checks=checked, axiom_reports=axioms,
                  build_log_sha256=sha(output / 'build.log'),
                  trust_boundary='Pinned package revisions and tracked-file cleanliness checked. Existing compiled dependency objects remain trusted build inputs.',
                  formal_scope='35 literal noncommutative cell relations imply (t1^-1*t40)^2=1; finite odd cardinality implies t1=t40.',
                  written_scope='Sylow normalization, local intersection criterion, universal presentation, and transport from every Gamma2 parameter to the fixed coset action.',
                  exclusions=['formalization of Sylow or polytope recognition', 'free-product decomposition',
                              'noninjective ends', 'even or mixed kernels', 'unrestricted minimal-cover uniqueness',
                              'historical priority or current-open-conjecture resolution'])
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
