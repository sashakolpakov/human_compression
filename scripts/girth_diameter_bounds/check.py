"""Replay the saved local refutations and the one order-95 graph; never solve.

The manifest hash must come from the reviewed publication record. Historical
absolute paths in provenance are documentary and are never used as input paths.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('Run ordinary Python, without -O')
sys.dont_write_bytecode = True
import argparse
import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/girth_diameter_bounds'
SCRIPTS = ROOT / 'scripts/girth_diameter_bounds'
PREFIXES = ('data/girth_diameter_bounds/', 'papers/girth_diameter_bounds/',
            'scripts/girth_diameter_bounds/')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def local(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and not p.is_absolute()
            and '..' not in p.parts and str(p) == name
            and name.startswith(PREFIXES), 'relative component path')
    path = ROOT / name
    require(not any(x.is_symlink() for x in (path, *path.parents)), 'no input symlinks')
    require(path.is_file() and path.resolve().is_relative_to(ROOT), 'local regular input')
    return path


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def function_ast(path, name):
    rows = [n for n in ast.parse(path.read_text()).body
            if isinstance(n, ast.FunctionDef) and n.name == name]
    require(len(rows) == 1, 'unique function')
    return ast.dump(rows[0], include_attributes=False)


def authenticate(expected):
    path = DATA / 'manifest.json'
    require(len(expected) == 64 and digest(path) == expected, 'external manifest hash')
    manifest = json.loads(path.read_text())
    require(manifest['schema'] == 'GIRTH_DIAMETER_ORDER95_COMPONENT_V1', 'manifest schema')
    rows = manifest['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'unique file roster')
    for row in rows:
        p = local(row['path'])
        require(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'],
                'exact component input: ' + row['path'])
    require('scripts/girth_diameter_bounds/check.py' in names, 'entrypoint bound')
    require(function_ast(SCRIPTS / 'check_positive.py', 'graph_properties') ==
            function_ast(SCRIPTS / 'reference_positive_check.py', 'graph_properties'),
            'unchanged acquired positive predicate')
    return manifest


def coverage():
    catalogue = json.loads((DATA / 'cases.json').read_text())
    require(catalogue['schema'] == 'GIRTH_DIAMETER_LOCAL_CERTIFICATES_V1', 'case schema')
    cases = catalogue['cases']
    require(len(cases) == 27 and len({c['id'] for c in cases}) == 27, '27 distinct cases')
    partition = json.loads((DATA / 'hole_pattern_partition.json').read_text())
    expected_ids = set()
    cells = [10*i+j for i in range(1, 4) for j in range(1, 4)]
    for occupied, count in ((6, 10), (5, 17)):
        n = 9-occupied
        universe = {tuple(x) for x in itertools.combinations(cells, n) if 11 in x}
        seen = set()
        group = next(g for g in partition['groups'] if g['occupied_cells'] == occupied)
        require(len(group['partition']) == count, 'orbit representative count')
        for row in group['partition']:
            holes = row['representative']
            orbit = set()
            images = {}
            for a, b in itertools.product((0, 1), repeat=2):
                def swap(x, bit):
                    return 5-x if bit and x in (2, 3) else x
                image = tuple(sorted(10*swap(x//10, a)+swap(x%10, b) for x in holes))
                images[f'{a}{b}'] = list(image)
                orbit.add(image)
            require(images == row['images'] and orbit == set(map(tuple, row['orbit'])),
                    'all literal C2 x C2 images')
            require(orbit <= universe and not orbit & seen, 'disjoint valid hole orbit')
            seen |= orbit
            case = next(c for c in cases if c['id'] == row['id'])
            require(case['holes'] == [[x//10, x%10] for x in holes], 'case representative')
            expected_ids.add(row['id'])
        require(seen == universe, 'complete distinguished-hole cover')
    require(expected_ids == {c['id'] for c in cases}, 'exact case coverage')
    require(sum(c['accepted_additions'] for c in cases) == 43029, 'retained proof total')
    return cases


def run_small(command, out, stem, seconds):
    so, se = out / (stem + '.stdout'), out / (stem + '.stderr')
    with so.open('xb') as stdout, se.open('xb') as stderr:
        result = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=seconds)
    require(result.returncode == 0, stem + ' return code')
    require(so.stat().st_size <= 65536 and se.stat().st_size == 0, stem + ' clean small output')
    return so.read_text()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest-sha256', required=True)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--metadata-only', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    manifest = authenticate(args.manifest_sha256)
    cases = coverage()
    if args.metadata_only:
        require(args.out is None, 'metadata mode writes no output')
        print(json.dumps({'status': 'PASS_COMPONENT_METADATA', 'files': len(manifest['files']),
                          'cases': len(cases), 'solver_calls': 0}))
        return
    require(args.out is not None and args.out.is_absolute(), 'absolute fresh external output')
    out = args.out
    require(not out.exists() and out.parent.is_dir()
            and not out.resolve().is_relative_to(ROOT)
            and not ROOT.is_relative_to(out.resolve())
            and not any(p.is_symlink() for p in (out, *out.parents)),
            'output outside checkout, no symlinks or overlap')
    compiler = shutil.which('c++')
    require(compiler is not None, 'C++17 compiler c++')
    out.mkdir()
    source = SCRIPTS / 'vendor/f012/certificate_backends/rup/root_units_active.cpp'
    binary = out / 'root_units_active'
    compile_command = [compiler, '-std=c++17', '-O2', str(source), '-o', str(binary)]
    run_small(compile_command, out, 'compile', 60)
    cnf = load_module('portable_exact_layer_formula',
                      SCRIPTS / 'vendor/f009/six_layer_certificates/cnf.py')
    results = []
    for case in cases:
        formula, variables = cnf.build(case['holes'])
        directory = DATA / 'certificates' / case['id']
        require((directory / 'formula.cnf').read_bytes() == formula.dimacs().encode(),
                case['id'] + ' exact complete DIMACS')
        require((directory / 'variables.json').read_bytes() ==
                (json.dumps(variables, indent=2) + '\n').encode(),
                case['id'] + ' exact primary-variable map')
        require(formula.variables == case['variables'] and len(formula.clauses) == case['clauses'],
                case['id'] + ' dimensions')
        command = [str(binary), str(directory / 'formula.cnf'), str(directory / 'proof.drat')]
        actual = json.loads(run_small(command, out, case['id'], 110))
        require(actual['status'] == 'CHECKED_ROOT_UNIT_ACTIVE_FALLBACK_RUP_REFUTATION'
                and actual['variables'] == case['variables']
                and actual['input_clauses'] == case['clauses']
                and type(actual['additions']) is int
                and actual['additions'] == case['accepted_additions'] >= 1,
                case['id'] + ' full RUP refutation ending in the original empty clause')
        results.append({'id': case['id'], 'holes': case['holes'], 'checker_result': actual,
                        'exact_dimacs_rebuilt': True, 'exact_variable_map_rebuilt': True})
        print(json.dumps({'checked': case['id'], 'additions': actual['additions']}), flush=True)
    positive = load_module('portable_exact_positive', SCRIPTS / 'check_positive.py')
    require(positive.nx.__version__ == '3.6.1', 'declared NetworkX 3.6.1')
    _, properties = positive.graph_properties((DATA / 'n95_k4_g5_d22.g6').read_bytes())
    require(properties == [95, 4, 4, 5, 22, 0], 'literal positive graph properties')
    authenticate(args.manifest_sha256)
    report = {'status': 'PASS_GIRTH_DIAMETER_ORDER95_PORTABLE_COMPONENT',
              'manifest_sha256': args.manifest_sha256, 'cases': results,
              'positive_properties': properties, 'compile_command': compile_command,
              'checker_sha256': digest(binary), 'networkx_version': positive.nx.__version__,
              'input_files': len(manifest['files']), 'inputs_unchanged': True,
              'solver_calls': 0, 'search_cache_reads': 0, 'whole_original_credit': 0,
              'scope': '27 local refutations and one positive graph; hand proofs remain explicit mathematical premises.',
              'seconds': time.monotonic() - start}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'cases': len(results),
                      'positive_properties': properties}), flush=True)


if __name__ == '__main__':
    main()
