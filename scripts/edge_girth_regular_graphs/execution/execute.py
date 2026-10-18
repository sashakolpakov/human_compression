"""Prospective package binding for acquired F012 defaults and bounded ownership.

Source only until separately reviewed and tested. No success or adoption is
implied by preparing a request. Mathematical worker bytes are never rewritten.
"""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys

sys.dont_write_bytecode = True
GIB, MIB = 2**30, 2**20
SELF = Path(__file__).resolve()


def need(value, message):
    if not value:
        raise ValueError(message)


def plain(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'Absolute canonical path')
    for part in (path, *path.parents):
        if os.path.lexists(part):
            need(not part.is_symlink(), 'No operational path aliases: ' + str(part))
    return path


def pin(path):
    path = plain(path)
    h, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(MIB), b''):
            size += len(block)
            h.update(block)
    return dict(path=str(path), bytes=size, sha256=h.hexdigest())


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def read_pinned(path, digest, maximum=4*MIB):
    path = plain(path)
    need(path.stat().st_size <= maximum, 'Bounded metadata')
    data = path.read_bytes()
    need(hashlib.sha256(data).hexdigest() == digest, 'Externally bound metadata identity')
    return json.loads(data)


def within(root, relative):
    rel = PurePosixPath(relative)
    need(type(relative) is str and not rel.is_absolute() and rel.parts
         and str(rel) == relative and all(x not in ('', '.', '..') for x in rel.parts),
         'Canonical package-relative name')
    return plain(root.joinpath(*rel.parts))


def checked(root, record):
    path = within(root, record['relative_path'])
    observed = pin(path)
    need(all(observed[k] == record[k] for k in ('bytes', 'sha256')), 'Exact package source/configuration')
    return path


def plan_at(root, digest):
    path = within(root, 'data/edge_girth_regular_graphs/execution/binding_plan.json')
    plan = read_pinned(path, digest)
    need(plan['schema'] == 'F012_PACKAGE_EXECUTION_BINDING_PLAN_ROLES_V1', 'Known binding plan')
    return path, plan


def slot(value, address):
    need(type(address) is list and bool(address), 'Named nonroot field path')
    current = value
    for key in address[:-1]:
        need((isinstance(current, dict) and type(key) is str and key in current)
             or (isinstance(current, list) and type(key) is int and 0 <= key < len(current)),
             'Exact named field path')
        current = current[key]
    key = address[-1]
    need((isinstance(current, dict) and type(key) is str and key in current)
         or (isinstance(current, list) and type(key) is int and 0 <= key < len(current)),
         'Exact named terminal field')
    return current, key


def environment_value(environment, edit, roles):
    role = edit['role']
    need(role in roles and role in environment['bindings'], 'Declared logical environment role')
    spec, value = roles[role], environment['bindings'][role]
    need(type(value) is dict and value.get('kind') == spec['kind'], 'Typed environment role')
    kind = spec['kind']
    if kind == 'file':
        need(set(value) == {'kind', 'identity'} and type(value['identity']) is dict
             and set(value['identity']) == {'path', 'bytes', 'sha256'}
             and pin(value['identity']['path']) == value['identity'], 'Actual logical file identity')
        path = value['identity']['path']
    elif kind == 'directory':
        need(set(value) == {'kind', 'path'} and plain(value['path']).is_dir(),
             'Ordinary declared environment directory')
        path = value['path']
    else:
        need(kind == 'symlink' and set(value) == {'kind', 'path', 'link', 'target'},
             'Exact declared linker-alias record')
        alias = Path(value['path'])
        need(alias.is_absolute() and '..' not in alias.parts, 'Absolute alias location')
        plain(alias.parent)
        need(alias.is_symlink() and os.readlink(alias) == value['link'] == spec['required_link'],
             'Preserved exact nauty alias/version premise')
        target = environment['bindings'][spec['target_role']]
        need(target['kind'] == 'file' and value['target'] == target['identity']
             and str(alias.resolve(strict=True)) == value['target']['path']
             and pin(value['target']['path']) == value['target'], 'Alias and actual pinned target agree')
        path = value['path']
    if 'directory_role' in spec:
        directory = environment['bindings'][spec['directory_role']]
        need(directory['kind'] == 'directory' and plain(directory['path']).is_dir(),
             'Declared ordinary parent directory')
        expected = Path(directory['path']) / spec['relative_path']
        if kind != 'symlink':
            plain(expected)
        need(path == str(expected), 'Header/library/alias belongs to its named directory')
    need(edit['projection'] in ('pin', 'path'), 'Known logical-role projection')
    if edit['projection'] == 'pin':
        need(kind == 'file', 'Only a file role supplies a full pin')
        return copy.deepcopy(value['identity'])
    return path


def case_value(root, route, environment, roles):
    if route['case_template'] is None:
        need(not route['named_case_edits'], 'No implicit case edits')
        return None
    path = checked(root, route['case_template'])
    original = json.loads(path.read_bytes())
    value = copy.deepcopy(original)
    seen = set()
    for edit in route['named_case_edits']:
        marker = tuple(edit['address'])
        need(marker not in seen, 'Unique named case edit')
        need(not any(marker[:len(old)] == old or old[:len(marker)] == marker for old in seen),
             'No nested overlapping edits')
        seen.add(marker)
        parent, key = slot(value, edit['address'])
        need(parent[key] == edit['old'], 'Exact predecessor field')
        if edit['kind'] == 'package_pin':
            replacement = pin(within(root, edit['relative_path']))
            need(all(replacement[k] == edit['old'][k] for k in ('bytes', 'sha256')),
                 'Only package pin path changes')
        else:
            need(edit['kind'] == 'environment', 'Known typed environment edit')
            replacement = environment_value(environment, edit, roles)
        parent[key] = copy.deepcopy(replacement)
    inverse = copy.deepcopy(value)
    for edit in reversed(route['named_case_edits']):
        parent, key = slot(inverse, edit['address'])
        parent[key] = copy.deepcopy(edit['old'])
    need(inverse == original, 'Whole case inverse; every expectation and scientific selector retained')
    return value


def selected_parts(root, route, value):
    """Read declared manifests, not graph/certificate contents or project code."""
    declarations = []
    if value is not None and 'modes' in value:
        table = read_pinned(value['modes']['path'], value['modes']['sha256'])
        if 'component' in value:
            selections = [table['components'][value['component']]]
        elif 'mode' in value:
            selections = [table['modes'][value['mode']]]
        else:
            need('applications' in value, 'Known multi-mode application')
            selections = [table['modes'][x['mode']] for x in value['applications']]
        declarations.append((table, selections))
    else:
        record = route['worker_global_bindings']['CASES']
        table = read_pinned(within(root, record['relative_path']), record['expected']['sha256'])
        selection = table['transport'] if value is None else table['cases'][value['selection']]
        declarations.append((table, [selection]))
    records = []
    for table, selections in declarations:
        path = within(root, table['runtime_manifest'])
        manifest = read_pinned(path, table['runtime_manifest_sha256'], 16*MIB)
        for selection in selections:
            for key in selection['inputs']:
                entry = manifest['files'][key]
                need(entry['object'] is not None, 'Actual selected scientific bytes required')
                for part in manifest['objects'][entry['object']]['parts']:
                    records.append(dict(path=str(within(root, part['relative_path'])),
                        bytes=part['bytes'], sha256=part['sha256']))
    return records


def inputs_for(root, plan_path, plan, route, environment_pin, environment, work, case):
    rows = [pin(plan_path), environment_pin, pin(SELF), pin(checked(root, plan['environment_generator']))]
    for record in plan['acquired_sources'] + plan['package_sources'] + plan['package_manifests']:
        rows.append(pin(checked(root, record)))
    if route['case_template'] is not None:
        rows.append(pin(checked(root, route['case_template'])))
        rows.append(pin(work / 'case.json'))
    for edit in route['named_case_edits']:
        if edit['kind'] == 'environment':
            environment_value(environment, edit, plan['environment_roles'])
            value = environment['bindings'][edit['role']]
            if value['kind'] == 'file':
                rows.append(value['identity'])
            elif value['kind'] == 'symlink':
                rows.append(value['target'])
    for row in environment['extra_input_pins']:
        need(set(row) == {'path', 'bytes', 'sha256'} and pin(row['path']) == row,
             'Explicit additional Python/tool environment pin')
        rows.append(row)
    rows.extend(selected_parts(root, route, case))
    unique = {}
    for row in rows:
        path = row['path']
        need(path not in unique or unique[path] == row, 'No conflicting input identities')
        unique[path] = row
    return [unique[path] for path in sorted(unique)]


def write_json(path, value):
    with path.open('xb') as stream:
        stream.write(canonical(value))


def prepare(args):
    root, work = plain(args.root), plain(args.work)
    need(SELF == within(root, 'scripts/edge_girth_regular_graphs/execution/execute.py'),
         'Run the installed binding from the assembled package')
    need(not os.path.lexists(work) and work.parent.is_dir(), 'Fresh external working directory')
    need(not work.is_relative_to(root) and not root.is_relative_to(work), 'Outputs outside package')
    plan_path, plan = plan_at(root, args.plan_sha256)
    need(args.route in plan['routes'], 'One exact declared route')
    route = plan['routes'][args.route]
    env_path = plain(args.environment)
    environment = read_pinned(env_path, args.environment_sha256)
    need(environment['schema'] == 'F012_PACKAGE_ENVIRONMENT_ROLES_V1'
         and environment['platform'] == plan['supported_owner_platform'] == 'darwin',
         'Current acquired libproc ownership supports Darwin only')
    need(type(environment['bindings']) is dict and type(environment['extra_input_pins']) is list,
         'Explicit environment configuration')
    need(environment['plan_sha256'] == pin(plan_path)['sha256']
         and set(environment['bindings']) == set(plan['environment_roles']),
         'Environment is bound to this plan and exact logical roles')
    case = case_value(root, route, environment, plan['environment_roles'])
    work.mkdir()
    if case is not None:
        write_json(work / 'case.json', case)
    config = dict(schema='F012_PACKAGE_BOUND_RUN_V1', root=str(root), work=str(work),
        plan=pin(plan_path), environment=pin(env_path), route=args.route,
        case=None if case is None else pin(work / 'case.json'),
        admission=dict(available_ram_bytes=max(4*GIB, route['limits']['family_rss_cap_bytes']+2*GIB),
                       free_disk_bytes=max(5*GIB, route['limits']['reserve_bytes']+route['limits']['growth_cap_bytes']+MIB)),
        whole_original_credit=0, source_and_runtime_acceptance=None)
    write_json(work / 'run_config.json', config)
    config_pin = pin(work / 'run_config.json')
    rows = inputs_for(root, plan_path, plan, route, pin(env_path), environment, work, case)
    rows.append(config_pin)
    request = dict(schema='LOCAL_SMALL_PYTHON_CHECK_V1', execution_id='F012_PACKAGE_'+args.route,
        program=str(SELF), supervisor=str(SELF), guard=str(within(root, plan['guard']['relative_path'])),
        argv=[sys.executable, '-E', '-B', str(SELF), '--worker', '--run-config', config_pin['path'],
              '--run-config-sha256', config_pin['sha256'], '--out', str(work/'returned')],
        inputs=sorted(rows, key=lambda x:x['path']), readonly_symlinks=[],
        output_roots=[str(work/'returned')], execution=str(work/'execution'), limits=route['limits'],
        scope='Complete declared original default and exact acquired report comparisons; no whole-original credit.',
        provenance=dict(binding_config=config_pin, source_and_runtime_acceptance=None))
    write_json(work / 'request.json', request)
    print(json.dumps(dict(status='PREPARED_ONLY_NO_SCIENTIFIC_EXECUTION', request=pin(work/'request.json'),
                         config=config_pin, scientific_calls=0)))


def load_config(path, digest):
    config = read_pinned(path, digest)
    need(set(config) == {'schema', 'root', 'work', 'plan', 'environment', 'route', 'case',
         'admission', 'whole_original_credit', 'source_and_runtime_acceptance'}
         and config['schema'] == 'F012_PACKAGE_BOUND_RUN_V1'
         and config['whole_original_credit'] == 0 and config['source_and_runtime_acceptance'] is None,
         'Exact unadopted run configuration schema')
    root, work = plain(config['root']), plain(config['work'])
    need(not work.is_relative_to(root) and not root.is_relative_to(work), 'Separate package and work roots')
    plan_path, plan = plan_at(root, config['plan']['sha256'])
    need(pin(plan_path) == config['plan'], 'Exact actual plan path')
    environment = read_pinned(config['environment']['path'], config['environment']['sha256'])
    need(pin(config['environment']['path']) == config['environment'], 'Exact environment bytes')
    need(environment['schema'] == 'F012_PACKAGE_ENVIRONMENT_ROLES_V1'
         and environment['platform'] == plan['supported_owner_platform'] == 'darwin',
         'Explicit supported environment; no cross-platform promise')
    route = plan['routes'][config['route']]
    need(environment['plan_sha256'] == pin(plan_path)['sha256']
         and set(environment['bindings']) == set(plan['environment_roles']),
         'Environment is bound to this plan and exact logical roles')
    case = case_value(root, route, environment, plan['environment_roles'])
    if case is None:
        need(config['case'] is None, 'No extra case')
    else:
        need(config['case']['path'] == str(work/'case.json')
             and pin(work/'case.json') == config['case']
             and (work/'case.json').read_bytes() == canonical(case), 'Exact relocated case, no expectation changes')
    return config, root, work, plan_path, plan, route, environment, case


def namespace(path, name):
    value = {'__name__': name, '__file__': str(path), '__builtins__': __builtins__}
    exec(compile(path.read_bytes(), str(path), 'exec'), value)
    return value


def worker(args):
    config, root, work, _, plan, route, environment, case = load_config(args.run_config, args.run_config_sha256)
    need(plain(args.out) == work/'returned' and not os.path.lexists(args.out), 'Exact fresh scientific output')
    for key in ('PYTHONOPTIMIZE', 'PYTHONPATH', 'PYTHONHOME'):
        os.environ.pop(key, None)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    compiler = None if case is None else case.get('compiler', case.get('external_environment', {}).get('compiler'))
    if compiler:
        os.environ['PATH'] = str(Path(compiler['path']).parent) + os.pathsep + os.environ.get('PATH', '')
    acquired = checked(root, route['worker'])
    source = acquired.read_text()
    tree = ast.parse(source)
    expressions = {n.targets[0].id: ast.get_source_segment(source, n.value) for n in tree.body
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
    ns = namespace(acquired, 'acquired_f012_worker')
    for key, binding in route['worker_global_bindings'].items():
        need(expressions.get(key) == binding['original_expression'], 'Exact original global binding expression')
        if binding['kind'] == 'package_root':
            ns[key] = root
        else:
            path = within(root, binding['relative_path'])
            expected = binding.get('expected', binding)
            need(all(pin(path)[k] == expected[k] for k in ('bytes','sha256')), 'Unchanged bound interface/helper')
            ns[key] = path
    # exec used a single namespace: every original function keeps these globals.
    need(ns['main'].__globals__ is ns, 'Original worker code and private rebound namespace')
    sys.argv = [str(acquired), '--out', str(args.out)]
    if case is not None:
        sys.argv += ['--case', config['case']['path'], '--case-sha256', config['case']['sha256']]
    sys.argv += route['extra_arguments']
    ns['main']()


def owner(args):
    need(sys.platform == 'darwin', 'Acquired targeted group observer is Darwin/libproc-specific')
    request = read_pinned(args.request, args.request_sha256)
    record = request['provenance']['binding_config']
    need(pin(record['path']) == record, 'Exact prepared run configuration')
    config, root, work, plan_path, plan, route, environment, case = load_config(record['path'], record['sha256'])
    need(SELF == within(root, 'scripts/edge_girth_regular_graphs/execution/execute.py'),
         'Execution binding installed at its declared package location')
    need(Path(args.request) == work/'request.json', 'Exact prepared request location')
    expected_inputs = inputs_for(root, plan_path, plan, route, config['environment'], environment, work, case)
    expected_inputs.append(record)
    expected_inputs.sort(key=lambda x:x['path'])
    need(request['inputs'] == expected_inputs and request['readonly_symlinks'] == [], 'Complete selected byte closure; no historical receipt dependency')
    need(request['program'] == request['supervisor'] == str(SELF)
         and request['guard'] == str(within(root, plan['guard']['relative_path']))
         and request['argv'] == [sys.executable, '-E', '-B', str(SELF), '--worker', '--run-config', record['path'],
             '--run-config-sha256', record['sha256'], '--out', str(work/'returned')]
         and request['output_roots'] == [str(work/'returned')]
         and request['execution'] == str(work/'execution') and request['limits'] == route['limits'],
         'Exact bounded route invocation')
    common_path = checked(root, plan['owner'])
    guard_path = checked(root, plan['guard'])
    ns = namespace(common_path, 'acquired_f012_owner')
    need(ns['GUARD_SHA'] == plan['guard']['sha256'], 'Original accepted guard unchanged')
    ns.update(S=work, SELF=SELF, GUARD=guard_path, PACKAGE_ROOT=root,
        READ_ROOTS=(root, work.parent, *tuple(sorted({Path(x['path']).parent for x in expected_inputs if not Path(x['path']).is_relative_to(root) and not Path(x['path']).is_relative_to(work)}, key=str))),
        WRITE_ROOTS=(work.parent,), INHERITED_ALIASES=set(), EXPECTED_LIMITS=route['limits'])
    original = common_path.read_text()
    node = next(n for n in ast.parse(original).body if isinstance(n, ast.FunctionDef) and n.name == 'preflight')
    text = ast.get_source_segment(original, node)
    substitutions = [
        ("need(type(limits['phase_seconds']) in (int, float) and 0 < limits['phase_seconds'] <= 120, 'at most 120 seconds')", "need(limits == EXPECTED_LIMITS, 'Exact acquired route profile')"),
        ("need(type(limits['family_rss_cap_bytes']) is int and 0 < limits['family_rss_cap_bytes'] <= 512*MIB, 'at most 512 MiB family RSS')", "need(type(limits['family_rss_cap_bytes']) is int and limits['family_rss_cap_bytes'] == EXPECTED_LIMITS['family_rss_cap_bytes'], 'Exact route RSS')"),
        ("need(type(limits['growth_cap_bytes']) is int and 65536 <= limits['growth_cap_bytes'] <= 8*MIB, '64 KiB to 8 MiB including receipts')", "need(type(limits['growth_cap_bytes']) is int and limits['growth_cap_bytes'] == EXPECTED_LIMITS['growth_cap_bytes'], 'Exact route growth')"),
        ("program = path_value(r['program'], (S,))", "program = path_value(r['program'], (PACKAGE_ROOT,))")]
    selected = text
    for old, new in substitutions:
        need(selected.count(old) == 1, 'One exact operational preflight substitution')
        selected = selected.replace(old, new)
    inverse = selected
    for old, new in reversed(substitutions):
        need(inverse.count(new) == 1, 'Unique inverse substitution')
        inverse = inverse.replace(new, old)
    need(inverse == text, 'Complete preflight source inverse')
    exec(compile(selected, str(SELF), 'exec'), ns)
    observed = ns['resources']()
    admission = dict(available_ram_bytes=max(4*GIB, route['limits']['family_rss_cap_bytes']+2*GIB),
        free_disk_bytes=max(5*GIB, route['limits']['reserve_bytes']+route['limits']['growth_cap_bytes']+MIB))
    need(config['admission'] == admission and all(observed[k] >= v for k,v in admission.items()),
         'Prospective exclusive launch admission; no cap change')
    # Original run, guard, receipt accounting, cleanup and targeted reaping.
    # Only preflight bindings/profile and filesystem base changed above.
    return ns['run'](args.request, args.preflight)


def main():
    need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE'), 'Ordinary Python required')
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--prepare', action='store_true')
    action.add_argument('--worker', action='store_true')
    action.add_argument('--request', type=Path)
    for name in ('root', 'work', 'environment', 'run-config', 'out'):
        parser.add_argument('--'+name, type=Path)
    for name in ('plan-sha256', 'environment-sha256', 'route', 'run-config-sha256', 'request-sha256'):
        parser.add_argument('--'+name)
    parser.add_argument('--preflight', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        return prepare(args)
    if args.worker:
        return worker(args)
    return owner(args)


if __name__ == '__main__':
    raise SystemExit(main())
