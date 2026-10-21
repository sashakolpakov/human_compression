#!/usr/bin/env python3
"""Replay the reviewed L092 calculations without private primary publications.

The mathematical programs are unchanged. This adapter checks their frozen
bindings and the single previously documented public navigation substitution.
Uniform mathematical proofs and source attribution require written review.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
FREEZES = {
    'phase186_export.json': 'cbbb953e5565ef1dd36286fe245c12c81fd1f854be5d887a544361055d97a24b',
    'phase199_export.json': '8c80fa904dfa730f58bad84c2b83d81250e7626004198849799c7c1467639a3d',
}
PRIMARY = {
    'sources/older_L092_gwdg.pdf', 'sources/older_L102_gwdg.pdf',
    'sources/phase183_kantor_homogeneousdes.pdf',
}
PUBLIC_UNITAL = '03eca23e35735b204ce53f60f7035545d8750bdacf89e8478124d57c8247ef70'
MATHLIB = '905b95818eb32af7874a58b427f50c1711a5e96c'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', type=Path, required=True)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--packages', type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), 'fresh output directory required')
    rows = {}
    for name, expected in FREEZES.items():
        require(digest(ROOT / name) == expected, 'freeze changed: ' + name)
        manifest = json.loads((ROOT / name).read_text())
        for row in manifest['exports'] + manifest['retained_inputs']:
            previous = rows.setdefault(row['path'], row)
            require(previous['sha256'] == row['sha256'] and previous['bytes'] == row['bytes'],
                    'inconsistent frozen bindings: ' + row['path'])
    require({name for name in rows if name.startswith('sources/')} == PRIMARY,
            'unexpected excluded primary input')
    adapter_hash = digest(Path(__file__))

    def verify():
        for name, expected in FREEZES.items():
            require(digest(ROOT / name) == expected, 'freeze changed: ' + name)
        for name, row in rows.items():
            if name in PRIMARY:
                continue
            path = ROOT / name
            if name == 'hermitian_unital_proof.md':
                require(digest(path) == PUBLIC_UNITAL, 'public unital text changed')
                old = b'](sources/van_nypelseer_forward_openalex.json)'
                new = b'[van_nypelseer_forward_openalex.json](sources/README.md)'
                require(path.read_bytes().count(new) == 1, 'unital navigation site changed')
                original = path.read_bytes().replace(new,
                    b'[van_nypelseer_forward_openalex.json' + old)
                require(len(original) == row['bytes'] and
                        hashlib.sha256(original).hexdigest() == row['sha256'],
                        'unital mathematical text differs from the author binding')
            else:
                require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
                        'frozen input changed: ' + name)
        require(digest(Path(__file__)) == adapter_hash, 'public adapter changed during replay')

    verify()
    lean = args.lean.absolute()
    packages = args.packages.absolute()
    lean_version = subprocess.check_output([str(lean), '--version'], text=True).strip()
    require('version 4.32.2,' in lean_version, 'Lean 4.32.2 required')
    revision = subprocess.check_output(['git', '-C', str(packages / 'mathlib'),
        'rev-parse', 'HEAD'], text=True).strip()
    require(revision == MATHLIB, 'pinned mathlib revision required')
    tracked = subprocess.check_output(['git', '-C', str(packages / 'mathlib'),
        'status', '--porcelain', '--untracked-files=no'], text=True)
    require(not tracked.strip(), 'mathlib tracked sources changed')
    out.mkdir(parents=True)
    environment = dict(os.environ)
    environment.pop('PYTHONOPTIMIZE', None)

    def command(label, argv, marker=None, rejection=False):
        r = subprocess.run(argv, cwd=ROOT, env=environment, text=True,
                           capture_output=True, timeout=300)
        log = r.stdout + r.stderr
        (out / (label + '.log')).write_text(log)
        if rejection:
            require('Error,' in log and (not marker or marker not in log),
                    label + ': altered incidence was not rejected')
        else:
            require(r.returncode == 0 and 'Error,' not in log, label + ': execution failed')
            require(not marker or marker in log, label + ': acceptance marker missing')
        return log

    command('author_replay', [sys.executable, '-B', str(ROOT / 'phase186_check.py'),
        '--out', str(out / 'author'), '--gap', str(args.gap.absolute()),
        '--lean', str(lean), '--packages', str(packages)])
    command('literal_hermitian', [str(args.gap.absolute()), '-q', '-b',
        str(ROOT / 'phase199_hermitian_literal.g')], 'P199_LITERAL_HERMITIAN_PASS')
    command('retained_mathieu_fibers', [str(args.gap.absolute()), '-q', '-b',
        str(ROOT / 'phase182_mathieu_fibers.g')], 'P182_MATHIEU_EXTENSION_FIBERS_PASS')
    paths = json.loads(command('path_length', [sys.executable, '-B',
        str(ROOT / 'phase199_path_length.py')]))
    require(paths['status'] == 'PASS', 'path-length counterexample failed')
    original = (ROOT / 'phase199_hermitian_literal.g').read_text()
    anchor = 'return x in flag[2] and x<>flag[1];'
    require(original.count(anchor) == 1, 'incidence mutation anchor changed')
    mutant = out / 'wrong_flag_incidence.g'
    mutant.write_text(original.replace(anchor, 'return not x in flag[2] and x<>flag[1];'))
    command('wrong_flag_incidence', [str(args.gap.absolute()), '-q', '-b', str(mutant)],
            'P199_LITERAL_HERMITIAN_PASS', rejection=True)
    author = json.loads((out / 'author/phase186_build.json').read_text())
    witness_path = out / 'author/phase186_witt_witness.json'
    witness = json.loads(witness_path.read_text())
    expected_witness = json.loads((ROOT / 'phase186_export.json').read_text())[
        'replay']['artifact_hashes']['phase186_witt_witness.json']
    require(digest(witness_path) == expected_witness, 'fresh Witt witness differs')
    versions = {key: witness[key] for key in ('gap_version', 'design_version', 'grape_version')}
    require(versions == dict(gap_version='4.15.1', design_version='1.8.2', grape_version='4.9.3'),
            'reviewed GAP/DESIGN/GRAPE versions required')
    reports = {}
    for module, count in [('DeletedLineFourResidue', 7), ('WittDerivedPlanes', 9),
                          ('CyclicBiplaneDelta', 6)]:
        source = ROOT / 'formal' / (module + '.lean')
        staged = out / 'author/formal' / (module + '.lean')
        require(source.read_bytes() == staged.read_bytes(), 'staged Lean source differs')
        log = (out / 'author' / (module + '.log')).read_text()
        lists = re.findall(r'depends on axioms:\s*\[([^]]*)\]', log)
        require(len(lists) == count, 'wrong axiom-report count: ' + module)
        axioms = {a.strip() for names in lists for a in names.split(',') if a.strip()}
        require(axioms <= {'propext', 'Classical.choice', 'Quot.sound'},
                'unexpected axiom: ' + module)
        reports[module] = dict(declarations=count, axioms=sorted(axioms),
            source_sha256=digest(source), log_sha256=digest(out / 'author' / (module + '.log')))
    verify()
    report = dict(status='PASS', public_adapter='phase208', adapter_sha256=adapter_hash,
        frozen_manifests=FREEZES, distributed_bindings_verified=len(rows) - len(PRIMARY),
        excluded_primary_bindings=sorted(PRIMARY), primary_PDFs_required_for_execution=False,
        unital_public_change='Previously recorded navigation link only; original proof bytes recovered and checked.',
        Lean_version=lean_version, compiler_sha256=digest(lean), mathlib_revision=revision,
        dependency_trust='Pinned tracked mathlib sources checked clean; existing dependency oleans not rebuilt.',
        versions=versions, exact_Witt_witness_byte_identical=True, finite_Witt_designs=5,
        derived_coordinate_isomorphisms=3, Lean=reports,
        root_coset_Hermitian_q=author['Hermitian_root_coset_parameters'],
        independent_literal_Hermitian_q=[3, 4, 5], independent_path_length=paths,
        author_Lean_negative_controls=author['Lean_negative_controls'],
        Python_witness_validation=json.loads((out / 'author/phase186_validation.json').read_text()),
        independent_source_incidence_mutation='REJECTED',
        retained_Mathieu_fibers_freshly_passed=True, new_open_conjecture_credit=0,
        scope='Fresh finite calculations and scoped formal proofs. Uniform theorems, source comparison and full-group completeness are not Lean-certified.')
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PHASE208_PUBLIC_REPLAY_PASS', digest(out / 'report.json'))


if __name__ == '__main__':
    main()
