#!/usr/bin/env python3
"""Replay finite witnesses and explicitly scoped Lean interfaces for phase239."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent
REVISION = '905b95818eb32af7874a58b427f50c1711a5e96c'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
FROZEN = {
    'phase211_surface_check.py': '728eaceef1048ad8a266b51dcabf217266f07c554474e85fede41f0a5b69e71b',
    'phase224_pyramid_flags.py': '5833616bed65485a89cbd1d03dd4558b92e8bc3984fd565b1344275195411a1f',
    'formal/CoprimePullback.lean': '4eb20ee7eb85943eab4100b565146a8cd938e4f3c2055b66c6fbbdfa3f68987c',
    'formal/CoverKernelChains.lean': '64cdb792746b651ec755af4f61b9548470fb0812f1f479b5f4eaceac4b99d572',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--gap', default='/opt/homebrew/bin/gap')
    parser.add_argument('--lean', default='/Users/sasha/.elan/bin/lean')
    parser.add_argument('--packages', type=Path,
                        default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory required')
    out = args.out.resolve()
    out.mkdir(parents=True)
    start = time.monotonic()
    for name, expected in FROZEN.items():
        require(sha(ROOT/name) == expected, 'changed frozen dependency: '+name)
    files = list(FROZEN) + ['phase239_pyramid_layers.py', 'phase239_pyramid_groups.g',
                            'formal/PyramidKernelTransport.lean']
    for name in files:
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    import phase239_pyramid_layers as layers
    import phase224_pyramid_flags as literal
    import phase211_surface_check as surfaces
    model = layers.orientation_model()
    (out/'orientation_model.json').write_text(json.dumps(model, indent=2)+'\n')
    (out/'orientation_input.g').write_text(layers.gap_input(model))
    bridges = [layers.verify_literal_bridge(n, literal) for n in [3, 5]]
    saved = layers.SHIFTS[0]
    layers.SHIFTS[0] = (0, 0)
    try:
        layers.verify_literal_bridge(3, literal)
    except ValueError as error:
        shift_control = str(error)
    else:
        raise RuntimeError('incorrect affine reflection accepted')
    finally:
        layers.SHIFTS[0] = saved
    require(shift_control == 'four adjacency intertwinings', 'unexpected affine control failure')
    process = subprocess.run([args.gap, '-q', 'phase239_pyramid_groups.g'],
                             cwd=out, text=True, capture_output=True, timeout=180)
    log = process.stdout+process.stderr
    (out/'groups.log').write_text(log)
    require(process.returncode == 0 and 'Error' not in log, 'fixed group replay')
    groups = json.loads(process.stdout[process.stdout.index('{'):])
    require(groups['status'] == 'PASS' and groups['D_generators'] == layers.D_GENERATORS,
            'common marked quotient between group and surface computations')
    d_model = {'name': 'Pyramid_D3840', 'degree': 10, 'generators': layers.D_GENERATORS}
    cells = surfaces.analyze(d_model, True)
    require(cells['cells'] == [3840, 7680, 3200] and cells['middle_order'] == 6,
            'literal cells of D')
    require(cells['orientable'] and cells['Euler_characteristic'] == -640 and
            cells['H1_dimension_odd'] == cells['H1_dimension_two'] == 642,
            'uniform homology dimension')
    require([len(x['complement_components']) for x in cells['pairs']] == [1, 1, 1] and
            [x['complement_components'][0]['size'] for x in cells['pairs']] == [2704, 3199, 3199],
            'three connected complements')
    require(cells['all_odd_prime_criterion'] and cells['prime_two_criterion'], 'surface hypotheses')
    (out/'surface_certificate.json').write_text(json.dumps(cells, indent=2)+'\n')
    env = os.environ.copy()
    env['ELAN_TOOLCHAIN'] = 'leanprover/lean4:v4.32.2'
    env['LEAN_PATH'] = ':'.join([str(out)] + [str(args.packages/p/'.lake/build/lib/lean')
        for p in ['mathlib', 'plausible', 'proofwidgets', 'batteries', 'aesop',
                  'importGraph', 'LeanSearchClient', 'Qq']])
    revision = subprocess.run(['git', '-C', str(args.packages/'mathlib'), 'rev-parse', 'HEAD'],
                              text=True, capture_output=True, check=True).stdout.strip()
    require(revision == REVISION, 'pinned mathlib revision')
    lean_reports = {}
    for name, count in [('CoprimePullback', 3), ('CoverKernelChains', 6),
                        ('PyramidKernelTransport', 4)]:
        source = out/'formal'/(name+'.lean')
        require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s', source.read_text(), re.M),
                'untrusted Lean declaration')
        process = subprocess.run([args.lean, '-o', str(out/(name+'.olean')), str(source)],
                                 cwd=out, env=env, text=True, capture_output=True, timeout=180)
        log = process.stdout+process.stderr
        (out/(name+'.log')).write_text(log)
        reports = re.findall(r'depends on axioms:\s*\[([^]]*)\]', log, re.S)
        require(process.returncode == 0 and 'sorryAx' not in log and len(reports) == count,
                'Lean compile and statement count: '+name)
        require(all(set(x.strip() for x in row.split(',')) <= ALLOWED for row in reports),
                'Lean axiom scope')
        lean_reports[name] = {'theorems': count, 'source_sha256': sha(source),
                              'log_sha256': sha(out/(name+'.log'))}
    source = (out/'formal/PyramidKernelTransport.lean').read_text()
    controls = {}
    for name, old, new in [
        ('CoincidentSupports', '(hab : a ≠ b)', '(hab : True)'),
        ('TrivialModulus', '(hn : 2 ≤ n)', '(hn : 1 ≤ n)'),
        ('MissingInjectivity', '(hker : ∀ x ∈ T, rho x = 1 → x = 1)', '(hker : True)'),
    ]:
        mutant = out/(name+'.lean')
        require(old in source, 'mutation target')
        mutant.write_text(source.replace(old, new))
        process = subprocess.run([args.lean, str(mutant)], cwd=out, env=env,
                                 text=True, capture_output=True, timeout=180)
        log = process.stdout+process.stderr
        (out/(name+'.log')).write_text(log)
        require(process.returncode != 0 and 'error:' in log, 'invalid proof assumption accepted')
        controls[name] = 'REJECTED'
    report = {
        'status': 'PASS', 'seconds': round(time.monotonic()-start, 3),
        'literal_bridges': bridges, 'groups': groups,
        'surface': {key: cells[key] for key in ['order', 'cells', 'middle_order',
                    'orientable', 'Euler_characteristic', 'H1_dimension_odd']},
        'Lean': lean_reports, 'Lean_controls': controls,
        'finite_controls': {'incorrect_r0_translation': shift_control,
                            'omitted_middle_center_condition': 'REJECTED'},
        'scope': 'Finite witnesses plus thirteen scoped Lean statements. The uniform affine/layer proof, surface topology, and retained 2022 non-C classification are written inputs; no general finite-cover conjecture is certified.',
        'artifacts': {str(p.relative_to(out)): sha(p) for p in sorted(out.rglob('*'))
                      if p.is_file() and p.suffix != '.olean'},
    }
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
