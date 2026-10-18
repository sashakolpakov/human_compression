"""Preserved catalogue/forest interfaces with explicit historical boundaries.

Default invocation only describes source. No historical executable is used.
The one legacy child entry executes its unchanged main under path relocation.
"""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from types import ModuleType, SimpleNamespace

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
helper=Path(__file__).with_name('native_checks.py')
if helper.is_symlink() or hashlib.sha256(helper.read_bytes()).hexdigest()!='8e9415e7398c664510abfd98a677c31f27681c47c4553233b6916645b3f30129':
    raise ValueError('Exact shared native relocation interface')
spec=importlib.util.spec_from_file_location('f012_catalogue_native',helper)
N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
F,R,need=N.F,N.R,N.need
AUTH_TREE=F.adapted_tree


def adapted_tree(raw,case):
    tree=AUTH_TREE(raw,case)
    original=ast.parse(raw)
    loops={(v.lineno,v.col_offset):v for v in ast.walk(original)if isinstance(v,ast.For)}
    modified={(v.lineno,v.col_offset):v for v in ast.walk(tree)if isinstance(v,ast.For)}
    for row in case['authentication_counters']:
        pos=(row['line'],row['column']);node=loops[pos].body[-1]
        need(isinstance(node,ast.AugAssign) and isinstance(node.op,ast.Add)
             and isinstance(node.target,ast.Name) and node.target.id==row['name']
             and isinstance(node.value,ast.Constant) and type(node.value.value)is int
             and node.value.value==1,'Exact metadata counter, not mathematical work')
        need(len(modified[pos].body)==1,'Exact inherited authentication replacement')
        modified[pos].body.append(copy.deepcopy(node))
    return ast.fix_missing_locations(tree)


def legacy_child(rt,case,work,output,target):
    need(case['number']==49 and target==output/'scientific/inventory.json'
         and not target.exists() and work==output/'inputs','One exact saved-inventory child result')
    key=case['relocated_child'];need(key in case['inputs'],'Declared child source')
    entry=rt.resolve(key,work);raw=entry.read_bytes();tree=ast.parse(raw)
    last=tree.body[-1]
    need(isinstance(last,ast.If) and F.structure(last.test)==F.structure(ast.parse("__name__ == '__main__'",mode='eval').body),
         'Exact original guarded child entry')
    module=ModuleType('f012_path_relocated_certificate');module.__file__=str(entry)
    module.__package__=None
    sys.path.insert(0,str(entry.parent))
    # First retain definitions under a non-main name; then execute the exact
    # original main guard/body after installing module-local Path relocation.
    exec(compile(tree,str(entry),'exec'),module.__dict__)
    N.install(module,rt,work,case,output)
    sys.argv=[str(entry),str(target)];module.__name__='__main__'
    exec(compile(ast.Module(body=[copy.deepcopy(last)],type_ignores=[]),str(entry),'exec'),module.__dict__)
    rt.resolve(key,work)


def historical_identities(rt,case,work):
    """Only declared provenance rows, never substitutes for mathematical data."""
    result={}
    for key,row in case['historical_executable_identities'].items():
        need(case['number']==9 and key not in case['inputs'],'Only declared historical executables')
        item=rt.files[key]
        need(item['role']=='provenance_only' and item['object'] is None
             and set(row)=={'bytes','sha256'} and all(item[k]==row[k]for k in row),
             'Exact non-payload historical identity')
        relative=R.relative(item['materialized_path'])
        path=str(work.joinpath(*relative))
        need(path not in result,'Distinct historical executable paths')
        result[path]=(key,row)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True);p.add_argument('--modes-sha256',required=True)
    p.add_argument('--component',choices=['4','9','49'],required=True)
    p.add_argument('--out',type=Path);p.add_argument('--compiler',type=Path);p.add_argument('--compiler-sha256')
    p.add_argument('--full-check',action='store_true');p.add_argument('--legacy-child',action='store_true')
    p.add_argument('--work',type=Path);p.add_argument('--outer-output',type=Path);p.add_argument('--legacy-output',type=Path)
    a=p.parse_args()
    raw=R.regular(a.root,'data/edge_girth_regular_graphs/catalogue_check_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==a.modes_sha256,'Externally reviewed catalogue modes')
    modes=json.loads(raw);need(modes['schema']=='F012_PORTABLE_CATALOGUE_CHECKS_V1','Mode schema')
    rt=R.Runtime(a.root,modes['runtime_manifest'],modes['runtime_manifest_sha256']);case=modes['components'][a.component]
    if a.legacy_child:
        need(not a.full_check and a.out is None and a.compiler is None and a.compiler_sha256 is None
             and all(v is not None and v.is_absolute()for v in(a.work,a.outer_output,a.legacy_output)),
             'Exact inherited child mode arguments')
        legacy_child(rt,case,a.work,a.outer_output,a.legacy_output);return
    need(a.work is None and a.outer_output is None and a.legacy_output is None,'No stray child parameters')
    adapted_tree(rt.read(case['entrypoint']),case)
    if not a.full_check:
        print(json.dumps(dict(status='CATALOGUE_SOURCE_DECLARED_NOT_EXECUTED',case=case,whole_source_credit=0),indent=2));return
    need(a.out is not None and not a.out.exists()and not a.out.is_symlink(),'Fresh output')
    compiler=a.compiler
    need(compiler is not None and compiler.is_absolute()and compiler.name=='clang++'
         and compiler.is_file()and not compiler.is_symlink()and os.access(compiler,os.X_OK),'Explicit regular clang++')
    before=R.digest(compiler);need(before[1]==a.compiler_sha256,'Externally pinned compiler')
    output=a.out.absolute();rt.verify(case['inputs']);output.mkdir();work=output/'inputs';rt.materialize(case['inputs'],work)
    observed=dict(historical_executable_identities=[],compiler_substitutions=[],child_substitutions=[])
    need(all(name not in sys.modules for name in case['late_modules']),
         'Fresh delayed adjacent mathematical imports')

    def install(module,runtime,materialized,declaration,out):
        N.install(module,runtime,materialized,declaration,out)
        history=historical_identities(rt,case,work)
        need(not(set(history)&{str(rt.resolve(k,work))for k in case['inputs']}),'Historical binaries are disjoint from mathematical input payloads')
        if history:
            need(case['number']==9 and hasattr(module,'sha'),'Only cubic historical-executable identity interface')
            original_sha=module.sha
            def sha(path):
                key=str(Path(path))
                if key not in history:return original_sha(path)
                logical,row=history[key]
                observed['historical_executable_identities'].append(dict(key=logical,bytes=row['bytes'],sha256=row['sha256']))
                return row['sha256']
            module.sha=sha
        need(module.subprocess is subprocess,'Unchanged module-local subprocess interface')
        original_run=subprocess.run
        def run(command,*args,**kwargs):
            argv=[str(x)for x in command]
            if argv and argv[0]=='/usr/bin/clang++':
                need(case['number']==9,'Only the declared cubic absolute compiler call')
                old=list(argv);argv[0]=str(compiler);observed['compiler_substitutions'].append(dict(original=old,configured=argv))
            if case['number']==49 and len(argv)==3 and argv[:2]==[sys.executable,str(rt.resolve(case['relocated_child'],work))]:
                target=Path(argv[2]);need(target==out/'scientific/inventory.json','Exact original inventory child output')
                old=list(argv);argv=[sys.executable,'-E','-B',str(Path(__file__).absolute()),'--root',str(a.root),
                    '--modes-sha256',a.modes_sha256,'--component','49','--legacy-child','--work',str(work),
                    '--outer-output',str(out),'--legacy-output',str(target)]
                observed['child_substitutions'].append(dict(original=old,configured=argv))
            # An actual subprocess remains an actual subprocess, with the same
            # capture/input/env/timeout semantics. No synthetic process result.
            return original_run(argv,*args,**kwargs)
        module.subprocess=SimpleNamespace(run=run,TimeoutExpired=subprocess.TimeoutExpired)

    old_path,old_tree,old_install=os.environ.get('PATH'),F.adapted_tree,F.install_paths
    try:
        os.environ['PATH']=str(compiler.parent)+(os.pathsep+old_path if old_path else'')
        need(shutil.which('clang++')==str(compiler),'Selected compiler for unchanged PATH calls')
        F.adapted_tree,F.install_paths=adapted_tree,install
        result,authentication=F.run_original(rt,work,case,output)
    finally:
        F.adapted_tree,F.install_paths=old_tree,old_install
        if old_path is None:os.environ.pop('PATH',None)
        else:os.environ['PATH']=old_path
    need(R.digest(compiler)==before,'Compiler unchanged')
    for name,key in case['late_modules'].items():
        need(name in sys.modules and Path(sys.modules[name].__file__).resolve()==rt.resolve(key,work),
             'Exact delayed adjacent mathematical source')
    if case['number']==49:need(len(observed['child_substitutions'])==1,'One actual relocated inventory child')
    if case['number']==9:
        need(len(observed['compiler_substitutions'])==1 and {r['key']for r in observed['historical_executable_identities']}==set(case['historical_executable_identities']),
             'Exact compiler and all declared historical executable identity consumers')
    for key in case['inputs']:rt.resolve(key,work)
    rt.verify(case['inputs'])
    report=dict(status='CHECKED_PORTABLE_CATALOGUE_COMPONENT',component=a.component,original_result=R.digest(result),
        runtime_inputs=len(case['inputs']),authentication=authentication,observed=observed,
        mathematical_predicates_unchanged=True,historical_payloads_freshly_verified=False,
        historical_executables_run=False,render=False,scope=case['mathematical_scope'],whole_source_credit=0)
    (output/'portable_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],component=a.component,whole_source_credit=0)))


if __name__=='__main__':main()
