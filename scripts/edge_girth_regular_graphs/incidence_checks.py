"""Original incidence classifications with explicit portable authentication.

No saved-result shortcut: complete native census, coverage and literal positive
checks remain. Default invocation describes source only.
"""
import argparse
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
helper = Path(__file__).with_name('native_checks.py')
if helper.is_symlink() or hashlib.sha256(helper.read_bytes()).hexdigest() != '8e9415e7398c664510abfd98a677c31f27681c47c4553233b6916645b3f30129':
    raise ValueError('Exact shared native relocation interface')
spec = importlib.util.spec_from_file_location('f012_incidence_native', helper)
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
F, R, need = N.F, N.R, N.need
ROW_PATH = F.row_path


def row_path(row, table):
    if table.get('path_field') == 'absolute_path':
        need('path' not in row and {'absolute_path', 'bytes', 'sha256'} <= set(row)
             and table['base'] == 'absolute', 'Exact original incidence identity row')
        translated = dict(row)
        translated['path'] = translated.pop('absolute_path')
        return ROW_PATH(translated, table)
    return ROW_PATH(row, table)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--modes-sha256', required=True)
    p.add_argument('--component', required=True, choices=['5', '6'])
    p.add_argument('--out', type=Path)
    p.add_argument('--compiler', type=Path)
    p.add_argument('--compiler-sha256')
    p.add_argument('--full-check', action='store_true')
    a = p.parse_args()
    raw = R.regular(a.root, 'data/edge_girth_regular_graphs/incidence_check_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == a.modes_sha256, 'Externally reviewed incidence modes')
    modes = json.loads(raw)
    need(modes['schema'] == 'F012_PORTABLE_INCIDENCE_CHECKS_V1', 'Mode schema')
    rt = R.Runtime(a.root, modes['runtime_manifest'], modes['runtime_manifest_sha256'])
    case = modes['components'][a.component]
    F.adapted_tree(rt.read(case['entrypoint']), case)
    if not a.full_check:
        print(json.dumps(dict(status='INCIDENCE_SOURCE_DECLARED_NOT_EXECUTED', case=case, whole_source_credit=0), indent=2))
        return
    need(a.out is not None and not a.out.exists() and not a.out.is_symlink(), 'Fresh output')
    compiler = a.compiler
    need(compiler is not None and compiler.is_absolute() and compiler.name == 'clang++'
         and compiler.is_file() and not compiler.is_symlink() and os.access(compiler, os.X_OK),
         'Explicit regular clang++ executable')
    before = R.digest(compiler)
    need(before[1] == a.compiler_sha256, 'Externally pinned compiler')
    out = a.out.absolute()
    rt.verify(case['inputs']); out.mkdir(); work = out/'inputs'
    rt.materialize(case['inputs'], work)
    old_path, old_installer, old_row = os.environ.get('PATH'), F.install_paths, F.row_path
    try:
        os.environ['PATH'] = str(compiler.parent)+(os.pathsep+old_path if old_path else '')
        need(shutil.which('clang++') == str(compiler), 'Explicit compiler selection')
        F.install_paths, F.row_path = N.install, row_path
        result, auth = F.run_original(rt, work, case, out)
    finally:
        F.install_paths, F.row_path = old_installer, old_row
        if old_path is None:os.environ.pop('PATH', None)
        else:os.environ['PATH'] = old_path
    need(R.digest(compiler) == before, 'Compiler bytes unchanged')
    for key in case['inputs']:rt.resolve(key, work)
    rt.verify(case['inputs'])
    report = dict(status='CHECKED_PORTABLE_INCIDENCE_COMPONENT', component=a.component,
        original_result=R.digest(result), runtime_inputs=len(case['inputs']), authentication=auth,
        compiler=dict(path=str(compiler), bytes=before[0], sha256=before[1]),
        mathematical_ast_unchanged=True, native_arguments_unchanged=True,
        historical_payloads_freshly_verified=False, historical_native_binaries_used=False,
        saved_output_acceptance_only=False, optional_render=False, optional_sanitize=False,
        whole_source_credit=0)
    (out/'portable_report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], component=a.component, whole_source_credit=0)))


if __name__ == '__main__':main()
