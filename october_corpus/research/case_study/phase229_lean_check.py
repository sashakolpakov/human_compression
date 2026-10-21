#!/usr/bin/env python3
"""Fresh Lean replay of the all-period displacement argument."""
import argparse, hashlib, json, os, re, subprocess, time
from pathlib import Path
BASE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok: raise RuntimeError('P229_REJECT ' + message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--packages', type=Path, required=True)
    a = ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh output directory')
    a.out.mkdir(parents=True)
    manifest = BASE / 'formal/dependency_manifest.json'
    deps = json.loads(manifest.read_text())
    revisions = []
    for item in deps['packages']:
        p = a.packages / item['name']
        revision = subprocess.check_output(['git', '-C', str(p), 'rev-parse', 'HEAD'], text=True).strip()
        need(revision == item['rev'], 'dependency revision ' + item['name'])
        need(subprocess.run(['git', '-C', str(p), 'diff', '--quiet', 'HEAD', '--']).returncode == 0, 'modified dependency ' + item['name'])
        revisions.append({'name': item['name'], 'revision': revision})
    version = subprocess.check_output([a.lean, '--version'], text=True).strip()
    need('version 4.32.2,' in version, 'Lean version')
    source = BASE / 'phase229_formal/BinaryDihedralDisplacements.lean'
    text = source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', text, re.M), 'proof placeholder')
    libraries = [str(p / '.lake/build/lib/lean') for p in sorted(a.packages.iterdir()) if (p / '.lake/build/lib/lean').is_dir()]
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(libraries))
    start = time.monotonic()
    r = subprocess.run([a.lean, source], cwd=BASE, env=env, text=True, capture_output=True, timeout=180)
    (a.out / 'BinaryDihedralDisplacements.stdout').write_text(r.stdout)
    (a.out / 'BinaryDihedralDisplacements.stderr').write_text(r.stderr)
    need(r.returncode == 0, 'compiler failure ' + r.stdout + r.stderr)
    need(not re.search(r'warning:|error:|sorryAx', r.stdout + r.stderr), 'unclean build')
    reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", r.stdout)
    expected = ['displacements_commute', 'displacement_conjugation', 'displacement_closure_commutative', 'finite_period_involutions', 'finite_displacement_closure_commutative']
    need([k.rsplit('.', 1)[-1] for k, _ in reports] == expected, 'declaration census')
    need(all(set(re.findall(r'[\w.]+', v)) <= {'propext', 'Quot.sound', 'Classical.choice'} for _, v in reports), 'axiom boundary')
    report = {'status': 'P229_FORMAL_REPLAY_PASS', 'sha256': digest(source), 'exit_code': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr, 'seconds': time.monotonic()-start, 'lean': version, 'lean_sha256': digest(a.lean.resolve()), 'dependencies': revisions, 'dependency_manifest_sha256': digest(manifest), 'trusted_cached_dependency_objects': True, 'native_decide_used': False, 'declarations': [k for k, _ in reports], 'scope': 'All-period commutativity, conjugation identity, subgroup commutativity and exact finite-period adapter. No complete formalization of the semidirect group, order bound or regular polytope.'}
    (a.out / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print('P229_FORMAL_REPLAY_PASS')
if __name__ == '__main__': main()
