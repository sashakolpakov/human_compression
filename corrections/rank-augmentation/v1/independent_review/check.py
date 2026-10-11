#!/usr/bin/env python3
"""Distinct GAP calculation and direct Lean compilation of the L020 obstruction.

No author implementation is imported. The written input C-property and source
hypotheses were separately read; Lean proves only the actual output defect.
"""
import argparse, hashlib, json, os, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WRITTEN = '95447aed8d01e873306eb55b463b13ab037c709a752ffcb3bcca172c70534bfd'
FORMAL = '0ccc90e1df556584071527d0b1271d26379e60e1a5839133e274ba7013dcf57e'

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def packet(path, pin):
    need(sha(path / 'manifest.json') == pin, 'wrong frozen packet')
    for row in json.loads((path / 'manifest.json').read_text())['exports']:
        name = Path(row['path'])
        need(not name.is_absolute() and '..' not in name.parts, 'unsafe export')
        f = path / name
        need(f.stat().st_size == row['bytes'] and sha(f) == row['sha256'], 'changed export ' + str(name))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--written', type=Path, required=True)
    p.add_argument('--formal', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--gap', default='/opt/homebrew/bin/gap')
    p.add_argument('--lean', default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    p.add_argument('--packages', type=Path, default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    a = p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'use a fresh output directory')
    a.out.mkdir(parents=True)
    packet(a.written, WRITTEN)
    packet(a.formal, FORMAL)
    code = (ROOT / 'distinct.g').read_text()
    # GAP and Schreier chains replace the author's explicit Python parabolics.
    result = subprocess.run([a.gap, '-q', '-b', '--quitonbreak'], input=code,
                            capture_output=True, text=True, timeout=120)
    (a.out / 'gap.stdout').write_text(result.stdout)
    (a.out / 'gap.stderr').write_text(result.stderr)
    need(result.returncode == 0 and not result.stderr, 'distinct GAP calculation failed')
    line = ''.join(result.stdout.split())
    expected = 'PASS_L020_DISTINCT_GAP:degree=18;old-order=6402373705728000;old-IP=64;tree-edges=17;H=48;B=6;intersection=48;old-type=[6,90];new-type=[4,3,90]'
    need(line == expected, 'incomplete or wrong mathematical output')
    pins = json.loads((a.formal / 'dependency_manifest.json').read_text())
    libraries = []
    for item in pins['packages']:
        d = a.packages / item['name']
        rev = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
        need(rev == item['rev'], 'wrong dependency revision')
        need(subprocess.run(['git', '-C', d, 'diff', '--quiet', 'HEAD', '--']).returncode == 0, 'changed dependency source')
        lib = d / '.lake/build/lib/lean'
        if lib.is_dir():
            libraries.append(str(lib))
    version = subprocess.run([a.lean, '--version'], capture_output=True, text=True, check=True).stdout
    need('version 4.32.2,' in version, 'wrong Lean version')
    source = (a.formal / 'RankAugmentationObstruction.lean').read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b', source), 'unpermitted placeholder or evaluator')
    local = a.out / 'RankAugmentationObstruction.lean'
    local.write_text(source)
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(libraries)
    env.pop('LEAN_SRC_PATH', None)
    result = subprocess.run([a.lean, '-o', 'RankAugmentationObstruction.olean', local.name], cwd=a.out,
                            env=env, capture_output=True, text=True, timeout=120)
    (a.out / 'lean.stdout').write_text(result.stdout)
    (a.out / 'lean.stderr').write_text(result.stderr)
    need(result.returncode == 0 and 'warning:' not in result.stdout + result.stderr, 'direct Lean compilation failed')
    declarations = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", result.stdout, re.S)
    need([name for name, _ in declarations] == json.loads((a.formal / 'scope.json').read_text())['declarations'], 'formal inventory changed')
    need(all(set(re.findall(r'[A-Za-z][\w.]*', ax)) <= {'propext', 'Classical.choice', 'Quot.sound'} for _, ax in declarations), 'nonstandard axioms')
    report = dict(status='PASS_DISTINCT_ROOT', written_manifest=WRITTEN, formal_manifest=FORMAL,
                  author_program_imports=False, old_group_order=6402373705728000, old_IP_pairs=64,
                  tree_edges=17, middle_group_order=6, first_end_order=48,
                  last_end_order=6402373705728000, end_intersection_order=48,
                  exact_disjoint_label_witness=True, formal_declarations=[n for n, _ in declarations],
                  standard_axioms_only=True, cached_dependencies_trusted=True,
                  input_C_property_formalized=False, source_hypotheses_formalized=False,
                  full_L020_recovery=False, original_admissions_added=0, new_question_credit=0)
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
