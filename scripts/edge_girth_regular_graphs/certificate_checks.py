"""Exact saved-tree verification and unchanged small native classifications.

The default is source declaration only. Execution requires a separately reviewed
process/resource owner. Historical producer agreement is never reported by the
saved-tree mode, which instead verifies the complete literal branching tree.
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from types import SimpleNamespace
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
HELPER_SHA = 'ca8fa9e004a736b539dd29551086e03e94867e23a25605bd5b9a4efeef8f205b'
helper = Path(__file__).with_name('finite_checks_relocation.py')
if helper.is_symlink() or hashlib.sha256(helper.read_bytes()).hexdigest() != HELPER_SHA:
    raise ValueError('Exact relocated finite interface')
spec = importlib.util.spec_from_file_location('f012_certificate_finite', helper)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
R, need = F.R, F.need
AUTH_TREE, PATHS = F.adapted_tree, F.install_paths


def statement_sha(node):
    return hashlib.sha256(F.structure(node).encode()).hexdigest()


def certificate_tree(raw, case):
    tree = AUTH_TREE(raw, case)
    if case['kind'] == 'unchanged_native':
        need(not case.get('omitted_main_statements'), 'Native mathematical main unchanged')
        return tree
    need(case['kind'] == 'saved_tree' and case['number'] == 29,
         'Only the explicitly reviewed saved-tree interface')
    original = copy.deepcopy(tree)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    saved = copy.deepcopy(main.body)
    removed = case['omitted_main_statements']
    ids = [r['index'] for r in removed]
    need(ids == [19, 20, 21, 22, 23, 38, 39], 'Exact producer/guard/render statement boundary')
    for row in removed:
        node = main.body[row['index']]
        need(node.lineno == row['line'] and statement_sha(node) == row['sha256'],
             'Unchanged removed statement')
    declaration = case['report_statement']
    need(declaration['index'] == 40 and statement_sha(main.body[40]) == declaration['sha256'],
         'Exact original report statement')
    report = main.body[40]
    need(isinstance(report, ast.Assign) and isinstance(report.value, ast.Dict), 'Literal report dictionary')
    changes = case['report_replacements']
    need(changes == {
        'status': dict(old='PASS_GIRTH_SIX_ORDER30_CLASSIFICATION', key='status', value='PASS_SAVED_GIRTH_SIX_ORDER30_CLASSIFICATION'),
        'ordinary_sanitized_agree': dict(old=True, key='native_producers_replayed', value=False),
        'optimization_guards': dict(old=2, key='optimization_guards', value=0)},
        'Truthful saved-only report changes')
    found = set()
    for i, key in enumerate(report.value.keys):
        if isinstance(key, ast.Constant) and key.value in changes:
            row = changes[key.value]
            val = report.value.values[i]
            need(isinstance(val, ast.Constant) and type(val.value) is type(row['old'])
                 and val.value == row['old'], 'Exact original report field')
            found.add(key.value)
            report.value.keys[i] = ast.copy_location(ast.Constant(row['key']), key)
            report.value.values[i] = ast.copy_location(ast.Constant(row['value']), val)
    need(found == set(changes), 'Every declared report field present')
    main.body = [n for i, n in enumerate(main.body) if i not in ids]
    # Restore only the named removals/report statement, preserving the actual
    # transformed remainder. Equality rules out edits to scientific clauses.
    reverse = copy.deepcopy(tree)
    reverse_main = next(n for n in reverse.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    kept = iter(reverse_main.body)
    reverse_main.body = [copy.deepcopy(saved[i]) if i in ids else next(kept) for i in range(len(saved))]
    reverse_main.body[40] = copy.deepcopy(saved[40])
    need(F.structure(reverse) == F.structure(original), 'All saved mathematical predicates and control statements preserved')
    need(not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and isinstance(n.func.value, ast.Name) and n.func.value.id == 'subprocess'
                 for n in ast.walk(tree)), 'Saved-tree mode has no subprocess calls')
    return ast.fix_missing_locations(tree)


def run(rt, work, case, output, compiler, compiler_sha):
    observations = []
    before = None
    if case['kind'] == 'unchanged_native':
        need(compiler is not None and compiler.is_absolute() and compiler.is_file()
             and not compiler.is_symlink() and os.access(compiler, os.X_OK), 'Explicit regular compiler executable')
        before = R.digest(compiler)
        need(before[1] == compiler_sha, 'Externally pinned compiler bytes')
    else:
        need(compiler is None and compiler_sha is None, 'Saved-tree mode does not accept a compiler')

    def install(module, runtime, materialized, declaration, out):
        PATHS(module, runtime, materialized, declaration, out)
        if case['kind'] != 'unchanged_native':
            return
        need(module.subprocess is subprocess, 'Original module-local subprocess binding')

        def native_run(command, *args, **kwargs):
            argv = [str(x) for x in command]
            if argv and argv[0] == 'clang++':
                original = list(argv)
                need('-std=c++17' in argv and argv.count('-o') == 1,
                     'Original source-build invocation')
                declared = {str(rt.resolve(key, work)) for key in case['source_build']['sources']}
                need({x for x in argv if x.endswith('.cpp')} == declared,
                     'Every compiled source is an exact declared input')
                argv[0] = str(compiler)
                observations.append(dict(original=original, configured=argv))
            # All flags, native arguments, input bytes, timeout and environment
            # remain supplied by the original checker. The owner handles the
            # process family; this adapter adds no executor or retry.
            return subprocess.run(argv, *args, **kwargs)

        module.subprocess = SimpleNamespace(run=native_run)

    old_tree, old_paths = F.adapted_tree, F.install_paths
    try:
        F.adapted_tree, F.install_paths = certificate_tree, install
        result, authentication = F.run_original(rt, work, case, output)
    finally:
        F.adapted_tree, F.install_paths = old_tree, old_paths
    if before is not None:
        need(R.digest(compiler) == before and len(observations) == 2,
             'Unchanged compiler and both original ordinary/sanitized builds')
    return result, authentication, observations


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--modes-sha256', required=True)
    p.add_argument('--component', required=True, choices=['26', '29'])
    p.add_argument('--out', type=Path)
    p.add_argument('--compiler', type=Path)
    p.add_argument('--compiler-sha256')
    p.add_argument('--full-check', action='store_true')
    a = p.parse_args()
    raw = R.regular(a.root, 'data/edge_girth_regular_graphs/tree_certificate_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == a.modes_sha256, 'Externally reviewed exact modes')
    modes = json.loads(raw)
    need(modes['schema'] == 'F012_PORTABLE_TREE_CERTIFICATES_V1', 'Mode schema')
    rt = R.Runtime(a.root, modes['runtime_manifest'], modes['runtime_manifest_sha256'])
    case = modes['components'][a.component]
    certificate_tree(rt.read(case['entrypoint']), case)
    if not a.full_check:
        print(json.dumps(dict(status='SOURCE_DECLARED_NOT_EXECUTED', case=case, whole_source_credit=0), indent=2))
        return
    need(a.out is not None and not a.out.exists() and not a.out.is_symlink(), 'Fresh output')
    out = a.out.absolute()
    rt.verify(case['inputs'])
    out.mkdir()
    work = out/'inputs'
    rt.materialize(case['inputs'], work)
    result, auth, commands = run(rt, work, case, out, a.compiler, a.compiler_sha256)
    for key in case['inputs']:
        rt.resolve(key, work)
    rt.verify(case['inputs'])
    report = dict(status='CHECKED_PORTABLE_CERTIFICATE_COMPONENT', component=a.component, kind=case['kind'],
        scientific_result=R.digest(result), runtime_inputs=len(case['inputs']), authentication=auth,
        historical_payloads_freshly_verified=False, historical_binary_used=False,
        compiler_commands=commands, saved_tree_predicates_unchanged=case['kind'] == 'saved_tree',
        ordinary_sanitized_replayed=case['kind'] == 'unchanged_native', render=False, whole_source_credit=0)
    (out/'portable_report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], component=a.component, whole_source_credit=0)))


if __name__ == '__main__':
    main()
