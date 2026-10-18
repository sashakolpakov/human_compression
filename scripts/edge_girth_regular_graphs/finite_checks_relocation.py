"""Relocate preserved finite/DAG checkers with exact authentication-site adapters.

The default only describes a mode. Full execution requires a separately reviewed
resource/process owner. No generator, rendering or alternate target flags exist.
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True
RUNTIME_SHA256 = 'e76919bf176912ac7b655a01fd3c4bc051ebb2c1d14db7a94a09658207ff5799'
transport = Path(__file__).with_name('runtime.py')
if transport.is_symlink() or hashlib.sha256(transport.read_bytes()).hexdigest() != RUNTIME_SHA256:
    raise ValueError('Exact package transport source')
spec = importlib.util.spec_from_file_location('f012_finite_transport', transport)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
need = R.need


def structure(node):
    return ast.dump(node, include_attributes=False)


def body_hash(body):
    return hashlib.sha256(structure(ast.Module(body=body, type_ignores=[])).encode()).hexdigest()


def adapted_tree(raw, case):
    """Replace only the declared authentication For bodies, then reverse-check."""
    need(hashlib.sha256(raw).hexdigest() == case['source_sha256'], 'Exact original source')
    original = ast.parse(raw)
    tree = copy.deepcopy(original)
    nodes = {(n.lineno, n.col_offset): n for n in ast.walk(tree) if isinstance(n, ast.For)}
    seen = set()
    originals = {}
    for site in case['authentication_sites']:
        position = (site['line'], site['column'])
        need(position in nodes and position not in seen, 'Unique exact authentication site')
        seen.add(position)
        node = nodes[position]
        need(isinstance(node.target, ast.Name) and node.target.id == site['row_variable']
             and structure(node.iter) == site['iterator_ast']
             and body_hash(node.body) == site['body_sha256'], 'Unchanged authentication body/iterator')
        originals[position] = node.body
        replacement = ast.Expr(value=ast.Call(func=ast.Name(id='_portable_authentication', ctx=ast.Load()),
            args=[ast.Constant(value=site['id']), ast.Name(id=node.target.id, ctx=ast.Load())], keywords=[]))
        node.body = [ast.copy_location(replacement, node.body[0])]
    # The reverse comparison binds every scientific expression, branch, loop,
    # import, helper and control outside these individually displayed bodies.
    restored = copy.deepcopy(tree)
    for node in ast.walk(restored):
        if isinstance(node, ast.For) and (node.lineno, node.col_offset) in originals:
            node.body = copy.deepcopy(originals[node.lineno, node.col_offset])
    need(structure(restored) == structure(original), 'No change outside authentication bodies')
    return ast.fix_missing_locations(tree)


def original_table(rt, work, declaration):
    value = json.loads(rt.resolve(declaration['key'], work).read_bytes())
    for key in declaration['pointer']:
        need(isinstance(value, dict) and key in value, 'Declared JSON table pointer')
        value = value[key]
    need(isinstance(value, list), 'Authentication table is a literal list')
    return value


def row_path(row, table):
    need(isinstance(row, dict) and {'path', 'bytes', 'sha256'} <= set(row), 'Original hash row')
    q = Path(row['path'])
    need('..' not in q.parts, 'No parent traversal in original locator')
    if table['base'] == 'absolute':
        need(q.is_absolute(), 'Absolute authentication locator')
        return str(q)
    need(not q.is_absolute(), 'Relative authentication locator')
    if table['base'] == 'roots':
        need(row['root'] in table['roots'], 'Explicit original root name')
        return str(Path(table['roots'][row['root']])/q)
    return str(Path(table['base'])/q)


def authentication(rt, work, case):
    """Authenticate real selected files; report exact old identity-only rows."""
    selected = set(case['inputs'])
    tables = {name: original_table(rt, work, table)
              for name, table in case['authentication_tables'].items()}
    paths = {}
    expected_only = {}
    aliases = {a: k for k, v in rt.files.items() for a in v['aliases']}
    for name, rows in tables.items():
        missing = []
        for i, row in enumerate(rows):
            path = row_path(row, case['authentication_tables'][name])
            key = aliases.get(path)
            if key in selected:
                item = rt.files[key]
                need(all(item[k] == row[k] for k in ('bytes', 'sha256')), 'Real input/table identity')
            else:
                missing.append(i)
            paths[name, i] = (path, key)
        expected_only[name] = missing
    need(case['authentication_identity_only'] == expected_only,
         'Exact declared complement of materialized mathematical inputs')
    sequences = {}
    covered = []
    for site in case['authentication_sites']:
        rows = [(name, i, row) for name in site['tables'] for i, row in enumerate(tables[name])]
        need(site['id'] not in sequences, 'Unique authentication site identifier')
        sequences[site['id']] = rows
        covered.extend((name, i) for name, i, _ in rows)
    need(len(covered) == len(set(covered)) and set(covered) == set(paths),
         'Every original authentication row has exactly one declared visit')
    positions = dict.fromkeys(sequences, 0)
    observed = dict(real_inputs=set(), identity_only=[])

    def check(site, row):
        need(site in sequences and positions[site] < len(sequences[site]), 'Declared row visit')
        name, i, expected = sequences[site][positions[site]]
        need(row == expected, 'Literal original authentication row and order')
        path, key = paths[name, i]
        if i in expected_only[name]:
            observed['identity_only'].append(dict(table=name, index=i, original_path=path,
                bytes=row['bytes'], sha256=row['sha256']))
        else:
            rt.resolve(key, work)
            observed['real_inputs'].add(key)
        positions[site] += 1

    def finish():
        need(all(positions[k] == len(v) for k, v in sequences.items()),
             'All original authentication loops actually completed')
        return dict(real_inputs=sorted(observed['real_inputs']),
                    identity_only=observed['identity_only'], visits=sum(positions.values()))
    return check, finish


def install_paths(module, rt, work, case, output):
    need(work == output/'inputs', 'Exact materialized tree inside this fresh output')
    roots = [(Path(old), work/new) for old, new in case['root_relocations'].items()]
    roots.sort(key=lambda pair: len(pair[0].parts), reverse=True)

    def relocated(value='.'):
        q = Path(value)
        need('..' not in q.parts, 'No undeclared parent traversal')
        if q.is_absolute():
            # The output may itself be inside the old study root. Already
            # relocated inputs and fresh outputs must not be relocated twice.
            if q.is_relative_to(output):
                return q
            for old, new in roots:
                if q.is_relative_to(old):
                    # Only a fresh materialized tree is addressed. Missing
                    # files fail normally; the private root is never opened.
                    return new/q.relative_to(old)
        return q

    if 'Path' in module.__dict__:
        module.Path = relocated
    if 'pathlib' in module.__dict__:
        # Only the legacy module's binding changes, never global pathlib.
        module.pathlib = SimpleNamespace(Path=relocated)
    dynamic = case['dynamic_imports']
    if dynamic:
        original = importlib.util.spec_from_file_location
        def load_spec(name, location, *args, **kwargs):
            need(not args and not kwargs and str(location) in dynamic,
                 'Only the exact declared cross-component Python import')
            key = dynamic[str(location)]
            need(key in case['inputs'], 'Declared imported source is materialized')
            return original(name, rt.resolve(key, work))
        module.importlib = SimpleNamespace(util=SimpleNamespace(
            spec_from_file_location=load_spec, module_from_spec=importlib.util.module_from_spec))


def run_original(rt, work, case, output):
    entry = rt.resolve(case['entrypoint'], work)
    tree = adapted_tree(entry.read_bytes(), case)
    adjacent = case['adjacent_modules']
    need(all(name not in sys.modules for name in adjacent), 'Fresh adjacent scientific imports')
    sys.path.insert(0, str(entry.parent))
    module = ModuleType('f012_original_finite_check')
    module.__file__ = str(entry)
    module.__package__ = None
    exec(compile(tree, str(entry), 'exec'), module.__dict__)
    for name, key in adjacent.items():
        need(name in sys.modules and Path(sys.modules[name].__file__).resolve() == rt.resolve(key, work),
             'Exact adjacent imported-source identity')
    check, finish = authentication(rt, work, case)
    module._portable_authentication = check
    install_paths(module, rt, work, case, output)
    scientific = output/'scientific'
    if case['output_kind'] == 'file':
        scientific.mkdir()
    result = scientific/case['result_relative']
    variables = dict(study=str(work/'study'), result=str(result), output=str(scientific),
                     component=str(entry.parent))
    argv = [str(entry)]
    for argument in case['arguments']:
        if isinstance(argument, str):
            argv.append(argument)
        else:
            need(set(argument) == {'variable'} and argument['variable'] in variables,
                 'Declared invocation parameter')
            argv.append(variables[argument['variable']])
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.argv = argv
    module.main()
    observations = finish()
    report = json.loads(result.read_bytes())
    need(report['status'] == case['expected_status'], 'Complete unchanged mathematical result')
    return result, observations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--modes-sha256', required=True)
    parser.add_argument('--component', required=True)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--full-check', action='store_true')
    args = parser.parse_args()
    raw = R.regular(args.root, 'data/edge_girth_regular_graphs/finite_check_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.modes_sha256, 'Externally reviewed mode declaration')
    modes = json.loads(raw)
    need(modes['schema'] == 'F012_PORTABLE_FINITE_CHECKS_V1', 'Finite mode schema')
    rt = R.Runtime(args.root, modes['runtime_manifest'], modes['runtime_manifest_sha256'])
    case = modes['components'][args.component]
    # Source transformation can be checked without importing a scientific module.
    adapted_tree(rt.read(case['entrypoint']), case)
    if not args.full_check:
        print(json.dumps(dict(status='DECLARED_FINITE_CHECK_NOT_EXECUTED', component=args.component,
            case=case, whole_source_credit=0), indent=2))
        return
    need(args.out is not None and not args.out.exists() and not args.out.is_symlink(), 'Fresh output')
    output = args.out.absolute()
    rt.verify(case['inputs'])
    output.mkdir()
    work = output/'inputs'
    rt.materialize(case['inputs'], work)
    result, observed = run_original(rt, work, case, output)
    for key in case['inputs']:
        rt.resolve(key, work)
    rt.verify(case['inputs'])
    report = dict(status='CHECKED_PORTABLE_FINITE_COMPONENT', component=args.component,
        original_result=R.digest(result), runtime_inputs=len(case['inputs']),
        authentication=observed, historical_payloads_freshly_verified=False,
        authentication_bodies_only_changed=True, scientific_ast_unchanged=True,
        render=False, generate=False, whole_source_credit=0)
    (output/'portable_report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], component=args.component, whole_source_credit=0)))


if __name__ == '__main__':
    main()
