#!/usr/bin/env python3
"""Replay the finite matrix witness and the general Lean quotient argument."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def need(ok, message):
    if not ok:
        raise RuntimeError('P212_REPLAY_REJECT ' + message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--gap', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--packages', type=Path, required=True)
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    out = args.out.resolve()
    need(not out.exists() and not out.is_symlink(), 'fresh output directory')
    names = ['phase212_n11_obstruction.md', 'phase212_n11_matrices.g',
             'phase212_binary_field_check.py', 'phase212_check.py',
             'phase212_formal/SimpleQuotientObstruction.lean',
             'formal/dependency_manifest.json']
    hashes = {name: sha(base / name) for name in names}
    deps = json.loads((base / 'formal/dependency_manifest.json').read_text())
    checked, libraries = [], []
    for item in deps['packages']:
        path = args.packages.resolve() / item['name']
        rev = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
        need(rev == item['rev'], 'dependency revision ' + item['name'])
        need(subprocess.run(['git', '-C', str(path), 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
             'dependency tracked sources clean ' + item['name'])
        checked.append(dict(name=item['name'], revision=rev))
        if (path / '.lake/build/lib/lean').is_dir():
            libraries.append(str(path / '.lake/build/lib/lean'))
    lean_version = subprocess.check_output([args.lean, '--version'], text=True).strip()
    need('version 4.32.2,' in lean_version, 'Lean version')
    gap_version = subprocess.check_output([args.gap, '-q', '-b', '-c',
                                           'Print(GAPInfo.Version,\"\\n\");QUIT_GAP(0);'], text=True).strip()
    need(gap_version == '4.15.1', 'GAP version')
    out.mkdir(parents=True)
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(libraries)
    runs = []

    def run(label, command, reject=False):
        p = subprocess.run(list(map(str, command)), cwd=out, env=env, text=True,
                           capture_output=True, timeout=240)
        (out / (label + '.stdout')).write_text(p.stdout)
        (out / (label + '.stderr')).write_text(p.stderr)
        need(p.returncode != 0 if reject else p.returncode == 0,
             label + ' exit code: ' + (p.stdout + p.stderr)[-1600:])
        runs.append(dict(label=label, exit_code=p.returncode,
                         stdout_sha256=sha(out / (label + '.stdout')),
                         stderr_sha256=sha(out / (label + '.stderr'))))
        return p.stdout + p.stderr

    binary = json.loads(run('binary', [sys.executable, '-B', '-O', base / names[2]]))
    need(binary['status'] == 'P212_BINARY_FIELD_PASS', 'independent arithmetic')
    native = run('matrices', [args.gap, '-q', '-b', base / names[1]])
    expected_lines = [
        'P212_LITERAL_RELATORS_PASS 45',
        'P212_ENDPOINT_REFLECTION_MEMBER 1 signed 1',
        'P212_ENDPOINT_REFLECTION_MEMBER 2 signed 1',
        'P212_MIDDLE_QUOTIENT_BOUND 22 outside_rotation33',
        'P212_MIDDLE_RESTRICTION_ORDER 22528',
        'P212_SP4_IMAGE 1124799322521600 simple true',
        'P212_SIGNED_IMAGE_ORDER 2249598645043200',
        'P212_LITERAL_MATRIX_CERTIFICATE_PASS']
    need(all(native.count(line) == 1 for line in expected_lines), 'complete literal group certificate')
    need(not re.search(r'Error|Warning|Syntax error|P212_FAIL', native), 'clean GAP run')
    source = base / names[4]
    text = source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', text, re.M), 'no proof holes')
    copy = out / source.name
    shutil.copyfile(source, copy)
    formal = run('quotients', [args.lean, '-o', copy.with_suffix('.olean'), copy])
    declarations = ['centerless_of_simple', 'simple_factor_nontrivial_of_adjacent_product',
                    'surviving_adjacent_product_separates_simple_factor',
                    'trivial_of_coprime_index', 'trivial_binary_character_index_three',
                    'injective_of_simple_nontrivial', 'kernel_second_eq_one',
                    'second_eq_of_image_eq', 'intersection_witness_survives']
    reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", formal)
    namespace = 'HumanCompression.SimpleQuotientObstruction.'
    need([name for name, _ in reports] == [namespace + name for name in declarations],
         'exact formal declarations')
    need(all(set(re.findall(r'[\w.]+', axioms)) <= {'propext', 'Classical.choice', 'Quot.sound'}
             for _, axioms in reports), 'standard axioms only')
    need(not re.search(r'warning:|error:|sorryAx', formal), 'clean Lean build')
    controls = []
    for mutant in ['identity-witness', 'wrong-field']:
        log = run(mutant, [sys.executable, '-B', '-O', base / names[2], '--mutant', mutant], True)
        need('P212_BINARY_REJECT' in log, 'arithmetic mutation rejection')
        controls.append(dict(name=mutant, rejected=True))
    changes = [
        ('even-index-character', '(hindex : D.index = 3)', '(hindex : D.index = 2)'),
        ('trivial-adjacent-product',
         '(hab : f (c, a) * f (c, b) ≠ 1) : ∃ s : S, f (1, s) ≠ 1 := by',
         '(hab : True) : ∃ s : S, f (1, s) ≠ 1 := by')]
    for label, old, new in changes:
        need(text.count(old) == 1, 'unique formal mutation site')
        path = out / (label + '.lean')
        path.write_text(text.replace(old, new, 1))
        log = run(label, [args.lean, path], True)
        need('error:' in log, 'formal mutation rejection')
        controls.append(dict(name=label, rejected=True))
    gap_text = (base / names[1]).read_text()
    old = 'List(P5gens,g->g*(33826,33827))'
    need(gap_text.count(old) == 1, 'unique sign mutation site')
    path = out / 'forgotten_sign.g'
    path.write_text(gap_text.replace(old, 'List(P5gens,g->g)', 1))
    log = run('forgotten_sign', [args.gap, '-q', '-b', path], True)
    need('P212_FAIL rank5 signed image bound' in log, 'central sign matters')
    controls.append(dict(name='forgotten_sign', rejected=True))
    need(hashes == {name: sha(base / name) for name in names}, 'input stability')
    report = dict(status='P212_MATRIX_AND_QUOTIENT_REPLAY_PASS', inputs=hashes,
                  dependency_revisions=checked, lean=lean_version, gap=gap_version,
                  lean_binary_sha256=sha(args.lean.resolve()),
                  cached_dependency_objects_remain_trusted=True,
                  binary_arithmetic=binary, formal_declarations=[n for n, _ in reports],
                  formal_object_sha256=sha(copy.with_suffix('.olean')),
                  unsigned_group_order=1124799322521600,
                  signed_group_order=2249598645043200,
                  endpoint_signed_memberships=[1, 2],
                  controls=controls, runs=runs,
                  universal_upper_certificate='separate phase214 component',
                  full_conjecture_lean_certificate=False,
                  historical_priority_established=False, source_edition='arXiv:2505.09505v1')
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('P212_MATRIX_AND_QUOTIENT_REPLAY_PASS')


if __name__ == '__main__':
    main()
