#!/usr/bin/env python3
"""Public F010 replay: unchanged reviewer checks, fresh Lean, four controls.

Adapted from the frozen phase188 driver. Only the selected F010 inputs are
required; private primary files and unrelated L059 artifacts are excluded.
The full private author checkpoint was checked at root admission.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

REQUIRED_AUTHOR = {
    'phase177_finite_pair_representation.md',
    'phase177_F010_contract.json',
    'phase177_hexagon_check.g',
    'formal/CompletedHexagonCounterexample.lean',
}

PINS = {
    'phase188_export.json': 'b9aa21d11f4bc1e21587b00f9e3529ec0a405decbcf71e4568d2257418b8ccf1',
    'phase177_finite_pair_representation.md': '21926d47460a75d0752f374579378fd2ffd56026fcdda6084863b0bdef033889',
    'phase177_F010_contract.json': 'a280f9903d130e36914923aeb0c2492103d876c2a6585ea1e48addfedb8aa8c1',
    'phase177_export.json': 'c1032decb72e86aa9f5d56189937b043a6bdbb3478e6de4ec6935463572fb9c9',
    'phase188_gadget_check.g': 'ecc53867c3bfedd2d69d03483dd2228d31a29917341732eb3563fd352353ae6d',
    'phase177_hexagon_check.g': 'f8a3ef275cef467e99d622228b518225b25e25d7e6c3dbd374229d0948327985',
    'formal/CompletedHexagonCounterexample.lean': '1a0d0ab0bf16537dbd9a35701c1f98336f8cf08513552a08fc1fd5648f272eb2',
    'formal/dependency_manifest.json': '4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3',
}


def require(test, message):
    if not test:
        raise RuntimeError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', default='gap')
    parser.add_argument('--lean', default='lean')
    parser.add_argument('--packages', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), 'fresh output directory required')
    for name, expected in PINS.items():
        require(digest(root / name) == expected, 'changed input: ' + name)
    manifest = json.loads((root / 'phase177_export.json').read_text())
    require({row['path'] for row in manifest['exports']} >= REQUIRED_AUTHOR, 'missing author bindings')
    for row in manifest['exports']:
        if row['path'] not in REQUIRED_AUTHOR:
            continue
        file = root / row['path']
        require(digest(file) == row['sha256'] and file.stat().st_size == row['bytes'], 'author binding: ' + row['path'])
    dependencies = json.loads((root / 'formal/dependency_manifest.json').read_text())
    checked = []
    gap_query = 'LoadPackage("grape");;Print(GAPInfo.Version,"\\n",PackageInfo("grape")[1].Version,"\\n");QUIT;'
    gap_info = subprocess.run([args.gap, '-q', '-T', '-c', gap_query], capture_output=True, text=True, timeout=30)
    gap_lines = gap_info.stdout.strip().splitlines()
    require(gap_info.returncode == 0 and not gap_info.stderr.strip() and len(gap_lines) == 2, 'invalid GAP/GRAPE environment')
    for item in dependencies['packages']:
        folder = args.packages / item['name']
        revision = subprocess.check_output(['git', '-C', str(folder), 'rev-parse', 'HEAD'], text=True).strip()
        require(revision == item['rev'], 'wrong dependency revision')
        require(subprocess.run(['git', '-C', str(folder), 'diff', '--quiet', 'HEAD', '--']).returncode == 0,
                'changed tracked dependency source')
        checked.append({'name': item['name'], 'revision': revision})
    out.mkdir(parents=True)
    env = dict(os.environ)
    env['ELAN_TOOLCHAIN'] = dependencies['lean']
    env['LEAN_PATH'] = os.pathsep.join(str(args.packages / p['name'] / '.lake/build/lib/lean')
                                      for p in dependencies['packages']
                                      if (args.packages / p['name'] / '.lake/build/lib/lean').is_dir())
    version = subprocess.check_output([args.lean, '--version'], text=True, env=env).strip()
    require(re.search(r'\bversion 4\.32\.2(?:,|\s)', version), 'wrong Lean compiler')
    graph = (root / 'phase188_gadget_check.g').read_text()
    hexagon = (root / 'phase177_hexagon_check.g').read_text()
    lean = (root / 'formal/CompletedHexagonCounterexample.lean').read_text()
    scenarios = [
        ('gadgets', 'g', graph, 'PHASE188_BOUNDED_GADGET_REVIEW_PASS', None),
        ('hexagon', 'g', hexagon, 'PHASE177_HEXAGON_CHECK_COMPLETE', None),
        ('lean', 'lean', lean, 'cyclic_three_has_no_nontrivial_involution', None),
    ]
    mutations = [
        ('unrigid_cleaning_tail', 'g', graph,
         'Add(edges,[base+2*M+3,base+2*M]);', '', 'restriction pair mismatch'),
        ('collapsed_arrow_labels', 'g', graph,
         'k:=Position(els,els[y]/els[x]);', 'k:=2;', 'uncolored arrow rigidity'),
        ('printed_wrong_hexagon_kernel', 'g', hexagon,
         'P177Hexagon([0..5],[12,6]);;', 'P177Hexagon([0..5],[12,3]);;', 'Assertion failure'),
        ('wrong_tip_reflection', 'lean', lean,
         '| .inr i => .inr (-i - 1)', '| .inr i => .inr (-i)', 'error:'),
    ]
    for name, extension, text, old, new, expected in mutations:
        require(text.count(old) == 1, 'mutation anchor: ' + name)
        marker = ('PHASE188_BOUNDED_GADGET_REVIEW_PASS' if text is graph else
                  'PHASE177_HEXAGON_CHECK_COMPLETE' if text is hexagon else None)
        mutant = text.replace(old, new)
        if name == 'collapsed_arrow_labels':
            # Remove only the size expectation to reach the actual rigidity
            # check; minimum degree, triangle-freeness and connectivity stay.
            count = 'result.n=(q^3+9*q^2-8*q)/2'
            require(mutant.count(count) == 1, 'size-control anchor')
            mutant = mutant.replace(count, 'true')
        scenarios.append((name, extension, mutant, marker, expected))

    def run(scenario):
        name, extension, text, marker, rejection = scenario
        file = out / (name + '.' + extension)
        file.write_text(text)
        command = ([args.gap, '-q', '-T', str(file)] if extension == 'g' else
                   [args.lean, '-o', str(out / (name + '.olean')), str(file)])
        start = time.monotonic()
        proc = subprocess.run(command, cwd=out, env=env, capture_output=True, text=True, timeout=600)
        log = proc.stdout + proc.stderr
        (out / (name + '.log')).write_text(log)
        if rejection is None:
            require(proc.returncode == 0 and marker in log and not re.search(r'Error,|error:|warning:', log), 'positive failure: ' + name)
        else:
            require(rejection in log and (marker is None or marker not in log), 'mutation not rejected: ' + name)
        if name == 'lean':
            reports = re.findall(r"'MathCompression\.CompletedHexagonCounterexample\.([^']+)' depends on axioms: \[([^]]*)\]", log)
            require(len(reports) == 4, 'incomplete Lean axiom report')
            require(all({x.strip() for x in used.split(',') if x.strip()} <=
                        {'propext', 'Classical.choice', 'Quot.sound'} for _, used in reports), 'unexpected axiom')
        return {'scenario': name, 'status': 'PASS', 'rejection': rejection, 'return_code': proc.returncode,
                'seconds': time.monotonic() - start, 'log_sha256': sha256(log.encode()).hexdigest()}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, scenarios))
    for name, expected in PINS.items():
        require(digest(root / name) == expected, 'input changed during replay')
    report = {'status': 'PASS', 'inputs': PINS, 'driver_sha256': digest(Path(__file__)),
              'Lean': version, 'GAP': gap_lines[0], 'GRAPE': gap_lines[1],
              'dependency_revisions': checked, 'runs': results,
              'bounded_cleaning_and_completion_graphs': 25, 'normal_pair_examples': 7,
              'normal_pair_completions_checked': 4, 'symmetric_family_parameters': [2, 3, 4, 5],
              'new_Lean_scope': 'Existing local completed-hexagon reflection certificate freshly compiled; no universal gadget theorem formalized.',
              'trust': 'Written universal proofs; GAP/GRAPE exact finite algorithms; Lean kernel and pinned cached dependency objects.',
              'L059_census_replayed': False, 'new_open_conjecture_solution': False,
              'private_primary_required': False, 'fresh_public_replay': True,
              'binding_scope': 'Selected F010 author sources, exact independent gadget program and frozen manifests. Primary texts were checked at admission; no unrelated L059 source or certificate is needed.'}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PHASE193_F010_PUBLIC_CHECKS_PASS')


if __name__ == '__main__':
    main()
