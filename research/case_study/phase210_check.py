#!/usr/bin/env python3
"""Fresh review replay for the Hermitian conjectural statement and transport leg."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

RETAINED = {
    'hermitian_unital_proof.md': '173c11ff6cb45bcea3dd9351b887cf92610244aed1b9f7285a8897ce59313528',
    'formal/ResidueConnectivity.lean': 'dbf265ba13d766b74f5577f8d61269e1deffe58c628cc2afa859103fe0593c69',
    'sources/older_L092_gwdg.pdf': 'f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403',
    'sources/older_L092_gwdg.txt': '8bca71ed69b045cc32a16af9ef712fa1e5bec7cecc571e1dd6437cb14ed16901',
    'phase199_export.json': '8c80fa904dfa730f58bad84c2b83d81250e7626004198849799c7c1467639a3d',
    'phase186_hermitian_residue_diameters.md': '038ae271e11db84a299627fcb06d87c568678c0105ae1aa2b66da7fc105f1d3e',
    'formal/dependency_manifest.json': '4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3'
}
NAMES = ['special_unitary_iff_gram', 'norm_fixed', 'preserves_norm', 'transport_maps',
         'transport_unitary', 'unitary_eq_transport', 'exists_unique_unitary_transport',
         'upper_unitary', 'lower_unitary', 'upper_difference_isotropic',
         'lower_difference_isotropic', 'upper_move_nontrivial', 'lower_move_nontrivial']


def need(ok, message):
    if not ok:
        raise RuntimeError('PHASE210_REJECT ' + message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--lean', type=Path, default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    ap.add_argument('--packages', type=Path, default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--gap', type=Path, default=Path('/opt/homebrew/bin/gap'))
    a = ap.parse_args()
    base = Path(__file__).resolve().parent
    out = a.output_dir.resolve()
    need(not out.exists() and not out.is_symlink(), 'fresh output directory')
    for name, digest in RETAINED.items():
        need(sha(base / name) == digest, 'retained input ' + name)
    new_inputs = ['phase210_formal/HermitianPlaneTransport.lean', 'phase210_unitary_check.g',
                  'phase210_norm_shell_transport.md', 'phase210_check.py']
    new_hashes = {name: sha(base / name) for name in new_inputs}
    deps = []
    for d in json.loads((base / 'formal/dependency_manifest.json').read_text())['packages']:
        p = a.packages / d['name']
        rev = subprocess.check_output(['git', '-C', str(p), 'rev-parse', 'HEAD'], text=True).strip()
        need(rev == d['rev'], 'dependency revision ' + d['name'])
        need(subprocess.run(['git', '-C', str(p), 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
             'dependency source clean ' + d['name'])
        deps.append(dict(name=d['name'], revision=rev))
    out.mkdir(parents=True)
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(str(p / '.lake/build/lib/lean') for p in a.packages.iterdir()
                                     if (p / '.lake/build/lib/lean').is_dir())

    def run(label, command, reject=False):
        r = subprocess.run(list(map(str, command)), cwd=out, env=env, text=True,
                           capture_output=True, timeout=240)
        (out / (label + '.stdout')).write_text(r.stdout)
        (out / (label + '.stderr')).write_text(r.stderr)
        need(r.returncode != 0 if reject else r.returncode == 0,
             label + ' unexpected exit status: ' + (r.stdout + r.stderr)[-1500:])
        return r.stdout + r.stderr

    formal = []
    for source, expected in [
            ('phase210_formal/HermitianPlaneTransport.lean',
             ['HumanCompression.HermitianPlane.' + n for n in NAMES]),
            ('formal/ResidueConnectivity.lean', ['LeemansConnectivity.connected_of_generating_moves'])]:
        dest = out / Path(source).name
        shutil.copyfile(base / source, dest)
        need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', dest.read_text(), re.M),
             'no proof holes or extra axioms')
        log = run(dest.stem, [a.lean, '-o', dest.with_suffix('.olean'), dest])
        reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)
        need([n for n, _ in reports] == expected, 'exact formal declarations')
        need(all(set(re.findall(r'[\w.]+', values)) <= {'propext', 'Classical.choice', 'Quot.sound'}
                 for _, values in reports), 'standard axioms only')
        need('error:' not in log and 'sorryAx' not in log and 'warning:' not in log, 'clean compilation')
        formal.append(dict(source=source, source_sha256=sha(dest), declarations=expected,
                           object_sha256=sha(dest.with_suffix('.olean'))))
    native = run('native_literal', [a.gap, '-q', '-b', base / 'phase210_unitary_check.g'])
    need('PHASE210_LITERAL_AND_UNITARY_PASS' in native and 'Error' not in native and 'Warning' not in native,
         'complete native check')
    rows = [json.loads(s) for s in native.splitlines() if s.startswith('{')]
    need([r['q'] for r in rows] == [2, 3, 4, 5], 'finite parameter range')
    for r in rows:
        q = r['q']
        need(r['unitary_action_order'] == q**3 * (q**3 + 1) * (q*q - 1) and
             r['chamber_stabilizer'] == 1 and r['ordered_pair_stabilizer'] == q*q - 1 and
             r['norm_shell'] == r['root_orbit'] == q*(q*q-1) and
             r['transport_pairs'] == (q*(q*q-1))**2, 'unitary chamber and transport action')
    controls = []
    lean_source = (base / 'phase210_formal/HermitianPlaneTransport.lean').read_text()
    mutations = [
        ('zero_norm_allowed',
         'theorem transport_maps (σ : K ≃+* K) (v w : K × K) (hv : norm σ v ≠ 0) :',
         'theorem transport_maps (σ : K ≃+* K) (v w : K × K) (hv : True) :'),
        ('wrong_transport_sign',
         '(w.1 * σ v.1 - σ w.1 * v.1) / k,',
         '(w.1 * σ v.1 + σ w.1 * v.1) / k,')]
    for label, old, new in mutations:
        need(lean_source.count(old) == 1, 'unique Lean mutation site')
        dest = out / (label + '.lean')
        dest.write_text(lean_source.replace(old, new, 1))
        log = run(label, [a.lean, dest], reject=True)
        need('error:' in log, 'semantic Lean mutation rejection')
        controls.append(dict(name=label, kind='Lean', rejected=True))
    gap_source = (base / 'phase210_unitary_check.g').read_text()
    mutations = [
        ('wrong_literal_flag_incidence',
         'function(i,f)return i in f[2] and i<>f[1];end',
         'function(i,f)return i=f[1];end'),
        ('wrong_shell_sign',
         'norm2:=v->v[1]*v[2]^q+v[1]^q*v[2];',
         'norm2:=v->v[1]*v[2]^q-v[1]^q*v[2];')]
    for label, old, new in mutations:
        need(gap_source.count(old) == 1, 'unique GAP mutation site')
        dest = out / (label + '.g')
        dest.write_text(gap_source.replace(old, new, 1))
        log = run(label, [a.gap, '-q', '-b', dest], reject=True)
        need('PHASE210_FAIL' in log, 'finite semantic mutation rejection')
        controls.append(dict(name=label, kind='GAP', rejected=True))
    for name, digest in RETAINED.items():
        need(sha(base / name) == digest, 'retained input preserved')
    need(new_hashes == {name: sha(base / name) for name in new_inputs}, 'new input stability')
    report = dict(status='PASS_HERMITIAN_REVIEW_AND_UNIFORM_TRANSPORT_REPLAY',
                  retained_inputs=RETAINED, new_inputs=new_hashes, dependency_revisions=deps,
                  lean_binary_sha256=sha(a.lean.resolve()), cached_dependency_objects_remain_trusted=True,
                  formal=formal, new_formal_declarations=13, retained_formal_declarations=1,
                  literal_models=rows, explicit_transport_pairs=sum(r['transport_pairs'] for r in rows),
                  controls=controls, legacy_full_written_proof_review='ACCEPTED',
                  new_formal_supplement_semantic_review='PENDING_SEPARATE_ROOT_REVIEW',
                  complete_conjecture_formalization=False,
                  source_formulation_answered='L092 Conjecture1, q>2; proof also covers q=2',
                  historical_priority_established=False, additional_conjecture_count=0,
                  whole_source_admissions=0, compression_ratio=None)
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PHASE210_REPLAY_PASS')


if __name__ == '__main__':
    main()
