#!/usr/bin/env python3
"""Compile the four connectivity declarations under pinned Lean dependencies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import sys

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(condition, message):
    if not condition:
        raise RuntimeError('PHASE268_REJECT ' + message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['out', 'lean', 'packages']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output')
    out = args.out.resolve()
    need(not out.exists(), 'fresh resolved output')
    out.mkdir(parents=True)
    start = time.monotonic()
    source = ROOT / 'phase268_formal/GraphClones.lean'
    text = source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', text, re.M),
         'no proof holes or new axioms')
    pins_path = ROOT / 'formal/dependency_manifest.json'
    pins = json.loads(pins_path.read_text())
    dependencies = []
    for item in pins['packages']:
        path = args.packages / item['name']
        rev = subprocess.check_output(['git', '-C', path, 'rev-parse', 'HEAD'], text=True).strip()
        need(rev == item['rev'] and subprocess.run(
            ['git', '-C', path, 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
            'pinned clean package ' + item['name'])
        dependencies.append(dict(name=item['name'], revision=rev))
    version = subprocess.check_output([args.lean, '--version'], text=True).strip()
    need('version 4.32.2,' in version, 'Lean version')
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(str(p / '.lake/build/lib/lean')
        for p in args.packages.iterdir() if (p / '.lake/build/lib/lean').is_dir())
    copied = out / source.name
    copied.write_text(text)
    result = subprocess.run([str(args.lean), '-o', str(out / 'GraphClones.olean'),
                             str(copied)], cwd=out, env=env, text=True,
                            capture_output=True, timeout=180)
    (out / 'formal.stdout').write_text(result.stdout)
    (out / 'formal.stderr').write_text(result.stderr)
    need(result.returncode == 0 and not re.search(r'error:|warning:|sorryAx',
         result.stdout + result.stderr), 'fresh Lean compile')
    expected = ['lift_fixed_fiber', 'same_fiber_reachable', 'lift_reachability', 'preserves_connectedness']
    declarations = re.findall(r"'([^']+)' does not depend on any axioms", result.stdout)
    need(declarations == ['GraphClones.' + x for x in expected], 'four axiom-free declarations')
    author_pin = '99c2a317d3c9c6a2ba37265b61245f6e3c7a4256af901975c7f01d6623a8e976'
    manifest_path = ROOT / 'phase265_cloning_manifest.json'
    need(sha(manifest_path) == author_pin, 'frozen clone author manifest')
    manifest = json.loads(manifest_path.read_text())
    for row in manifest['exports']:
        path = ROOT / row['path']
        need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'frozen author file')
    executions = []
    for label, filename in [('author', 'phase265_gonality_two_check.py'), ('independent', 'phase268_independent.py')]:
        tick = time.monotonic()
        run = subprocess.run([sys.executable, '-B', '-O', str(ROOT / filename),
                              '--out', str(out / (label + '.json'))], cwd=out,
                             capture_output=True, text=True, timeout=180)
        (out / (label + '.stdout')).write_text(run.stdout)
        (out / (label + '.stderr')).write_text(run.stderr)
        need(run.returncode == 0 and not run.stderr, label + ' replay')
        data = json.loads((out / (label + '.json')).read_text())
        need(data['status'] == 'PASS', label + ' success')
        executions.append(dict(label=label, seconds=round(time.monotonic()-tick, 3)))
    # The neighbor hypothesis matters: cloning a single isolated base vertex
    # produces two disconnected vertices although the one-vertex base is connected.
    from phase268_independent import reaches
    need(reaches([set()]) == {0} and reaches([set(), set()]) == {0}, 'isolated-vertex control')
    report = dict(status='PASS', seconds=round(time.monotonic()-start, 3),
        source_sha256=sha(source), checker_sha256=sha(Path(__file__)),
        dependency_manifest_sha256=sha(pins_path), lean_version=version,
        dependencies=dependencies, axiom_free_declarations=declarations, exit_code=result.returncode,
        semantic_hypothesis_controls=1, executions=executions, trusted_cached_dependency_objects=True,
        scope='Four actual graph-relation path proofs; literal a=2 and independent a=1,2,3 geometries. Incidence identification, uniform cloning theorem and source application remain written.')
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
