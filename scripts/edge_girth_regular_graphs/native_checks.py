"""Relocate unchanged finite native classifications; source declaration by default.

These modes retain the original searches and controls. They are not saved-report
acceptance modes. An external bounded owner must authorize every actual replay.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
HELPER_SHA = 'ca8fa9e004a736b539dd29551086e03e94867e23a25605bd5b9a4efeef8f205b'
helper = Path(__file__).with_name('finite_checks_relocation.py')
if helper.is_symlink() or hashlib.sha256(helper.read_bytes()).hexdigest() != HELPER_SHA:
    raise ValueError('Exact relocated finite interface')
spec = importlib.util.spec_from_file_location('f012_native_finite', helper)
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
R, need = F.R, F.need
PATHS = F.install_paths


def install(module, rt, work, case, output):
    # The acquired helper accepts exactly declared import locations. These
    # original callers construct some locations from --study, so permit the
    # corresponding already-materialized spelling as well as the old spelling.
    declaration = copy.deepcopy(case)
    for original, key in case['dynamic_imports'].items():
        need(key in case['inputs'], 'Imported code is an exact semantic input')
        translated = str(rt.resolve(key, work))
        if translated in declaration['dynamic_imports']:
            need(declaration['dynamic_imports'][translated] == key, 'No import-location collision')
        declaration['dynamic_imports'][translated] = key
    PATHS(module, rt, work, declaration, output)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--modes-sha256', required=True)
    p.add_argument('--component', required=True, choices=['18', '19', '20', '21', '22', '23'])
    p.add_argument('--out', type=Path)
    p.add_argument('--compiler', type=Path)
    p.add_argument('--compiler-sha256')
    p.add_argument('--full-check', action='store_true')
    a = p.parse_args()
    raw = R.regular(a.root, 'data/edge_girth_regular_graphs/native_check_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == a.modes_sha256, 'Externally reviewed native modes')
    modes = json.loads(raw)
    need(modes['schema'] == 'F012_PORTABLE_NATIVE_CHECKS_V1', 'Mode schema')
    rt = R.Runtime(a.root, modes['runtime_manifest'], modes['runtime_manifest_sha256'])
    case = modes['components'][a.component]
    F.adapted_tree(rt.read(case['entrypoint']), case)
    if not a.full_check:
        print(json.dumps(dict(status='NATIVE_SOURCE_DECLARED_NOT_EXECUTED', case=case, whole_source_credit=0), indent=2))
        return
    need(a.out is not None and not a.out.exists() and not a.out.is_symlink(), 'Fresh output')
    compiler = a.compiler
    need(compiler is not None and compiler.is_absolute() and compiler.name == 'clang++'
         and compiler.is_file() and not compiler.is_symlink() and os.access(compiler, os.X_OK),
         'Explicit regular clang++ executable for all original calls')
    before = R.digest(compiler)
    need(before[1] == a.compiler_sha256, 'Externally pinned compiler')
    out = a.out.absolute()
    rt.verify(case['inputs'])
    out.mkdir()
    work = out/'inputs'
    rt.materialize(case['inputs'], work)
    old_path = os.environ.get('PATH')
    old_installer = F.install_paths
    try:
        # This also reaches the original interval_controls.py child in mode21.
        # No compiler/native argument, code, timeout or control is rewritten.
        os.environ['PATH'] = str(compiler.parent)+(os.pathsep+old_path if old_path else '')
        need(shutil.which('clang++') == str(compiler), 'Every PATH compiler call selects the pinned file')
        F.install_paths = install
        result, auth = F.run_original(rt, work, case, out)
    finally:
        F.install_paths = old_installer
        if old_path is None:
            os.environ.pop('PATH', None)
        else:
            os.environ['PATH'] = old_path
    need(R.digest(compiler) == before, 'Compiler bytes unchanged after the complete replay')
    for key in case['inputs']:
        rt.resolve(key, work)
    rt.verify(case['inputs'])
    report = dict(status='CHECKED_PORTABLE_NATIVE_COMPONENT', component=a.component,
        original_result=R.digest(result), runtime_inputs=len(case['inputs']), authentication=auth,
        compiler=dict(path=str(compiler), bytes=before[0], sha256=before[1]),
        original_scientific_ast_unchanged=True, native_arguments_unchanged=True,
        compiler_selection='Only PATH prefix selects the explicit pinned clang++; original child arguments are unchanged.',
        historical_payloads_freshly_verified=False, historical_native_binaries_used=False,
        saved_output_acceptance_only=False, render=False, whole_source_credit=0)
    (out/'portable_report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], component=a.component, whole_source_credit=0)))


if __name__ == '__main__':
    main()
