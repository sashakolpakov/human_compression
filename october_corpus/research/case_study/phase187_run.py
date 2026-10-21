#!/usr/bin/env python3
"""Replay the geometric obstruction, negative controls and limited Lean components."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    a = ap.parse_args()
    root = Path(__file__).resolve().parent
    out = a.output_dir.absolute()
    lean = a.lean.absolute()
    require(not out.exists() and not out.is_symlink(), 'fresh output directory required')
    out.mkdir(parents=True)
    code = root / 'phase187_parallel_gluing_check.py'
    source = root / 'phase187_formal/SimultaneousMatching.lean'
    written = root / 'phase187_parallel_gluing.md'
    bindings = {str(p.relative_to(root)): sha(p) for p in [code, source, written]}
    result = subprocess.run([sys.executable, '-B', '-O', str(code), '--output', str(out / 'geometry.json')],
                            capture_output=True, text=True, timeout=120)
    (out / 'geometry.log').write_text(result.stdout + result.stderr)
    require(result.returncode == 0 and 'PHASE187_PARALLEL_GLUING_PASS' in result.stdout,
            'literal geometry replay failed')
    controls = []
    for name, old, new, expected in [
        ('globally_compatible_matching', 'beta = (e, s, compose(aa, t))', 'beta = alpha',
         'global lift must be obstructed'),
        ('duplicate_line_shadows', '[[1, 2, 5, 6], [0, 3, 4, 7]],',
         '[[0, 1, 4, 5], [2, 3, 6, 7]],', 'property O: distinct line shadows'),
    ]:
        text = code.read_text()
        require(text.count(old) == 1, 'nonunique mutation anchor')
        path = out / (name + '.py')
        path.write_text(text.replace(old, new))
        r = subprocess.run([sys.executable, '-B', '-O', str(path), '--output', str(out / (name + '.json'))],
                           capture_output=True, text=True, timeout=120)
        (out / (name + '.log')).write_text(r.stdout + r.stderr)
        require(r.returncode != 0 and expected in r.stderr and not (out / (name + '.json')).exists(),
                'negative control did not fail closed: ' + name)
        controls.append({'name': name, 'rejected': True, 'reason': expected})
    formal = out / 'formal'
    formal.mkdir()
    staged = formal / source.name
    shutil.copy2(source, staged)
    require(sha(staged) == sha(source), 'fresh Lean stage differs')
    r = subprocess.run([str(lean), '-o', str(formal / 'SimultaneousMatching.olean'), str(staged)],
                       capture_output=True, text=True, cwd=formal, timeout=120)
    body = r.stdout + r.stderr
    (out / 'lean.log').write_text(body)
    require(r.returncode == 0 and 'sorryAx' not in body and 'error:' not in body
            and body.count("'SimultaneousMatching.") == 12, 'fresh Lean component build failed')
    # Changing the third coset to the identity-containing subgroup creates a
    # common element. The former theorem must therefore stop compiling.
    text = source.read_text()
    old = 'def shifted (x : Klein) : Prop := x = a ∨ x = b'
    new = 'def shifted (x : Klein) : Prop := x = one ∨ x = b'
    require(text.count(old) == 1, 'nonunique Lean mutation anchor')
    altered = formal / 'AlteredCoset.lean'
    altered.write_text(text.replace(old, new))
    r = subprocess.run([str(lean), str(altered)], capture_output=True, text=True, cwd=formal, timeout=120)
    (out / 'lean_altered_coset.log').write_text(r.stdout + r.stderr)
    require(r.returncode != 0 and 'error:' in r.stdout + r.stderr,
            'changed formal obstruction was not rejected')
    controls.append({'name': 'altered_formal_coset', 'rejected': True,
                     'reason': 'the false intersection/coset declarations do not compile'})
    for name, h in bindings.items():
        require(sha(root / name) == h, 'bound source changed during replay')
    version = subprocess.run([str(lean), '--version'], capture_output=True, text=True, check=True).stdout.strip()
    report = {'status': 'PASS', 'source_hashes': bindings, 'geometry': json.loads((out / 'geometry.json').read_text()),
              'negative_controls': controls, 'Lean': {'version': version, 'compiler_sha256': sha(lean),
                'declarations': 12, 'fresh_source_compile': True, 'imports': ['Std'],
                'axioms_observed': ['Classical.choice', 'propext'],
                'scope': 'common-image/coherent-family equivalence and the finite Klein-group coset obstruction',
                'full_incidence_geometry_formalized': False},
              'whole_source_principal_credit': 0, 'open_conjecture_credit': 0}
    (out / 'replay.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PHASE187_REPLAY_PASS', sha(out / 'replay.json'))


if __name__ == '__main__':
    main()
