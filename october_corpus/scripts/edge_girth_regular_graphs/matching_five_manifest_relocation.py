"""Prepared relocation for unchanged matching-forest component checkers.

Default is metadata only. The full-check action requires a separately reviewed
process/resource owner. Recorded-target and render modes are not exposed here.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True

RUNTIME_SHA256 = 'e76919bf176912ac7b655a01fd3c4bc051ebb2c1d14db7a94a09658207ff5799'
source = Path(__file__).with_name('runtime.py')
if source.is_symlink() or hashlib.sha256(source.read_bytes()).hexdigest() != RUNTIME_SHA256:
    raise ValueError('Exact package transport source')
spec = importlib.util.spec_from_file_location('f012_matching_transport',source)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
need = R.need


def import_original(rt,work,case):
    entrypoint = rt.resolve(case['entrypoint'],work)
    directory = entrypoint.parent
    # The legacy files use adjacent absolute module names. One component is
    # executed per fresh process; no old cached module may supply an import.
    for name in case['adjacent_modules']:
        need(name not in sys.modules,'Fresh adjacent scientific module: '+name)
    sys.path.insert(0,str(directory))
    spec = importlib.util.spec_from_file_location('f012_original_matching_check',entrypoint)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name,key in case['adjacent_modules'].items():
        need(name in sys.modules and Path(sys.modules[name].__file__).resolve() == rt.resolve(key,work),
             'Exact adjacent module imported from the materialized source')
    return module


def install_adapters(module,rt,work,case,output,compiler,include,library):
    """Change only path/authentication and configured compiler invocation."""
    original_pin = module.pin
    original_execute = module.execute
    component_dir = rt.resolve(case['entrypoint'],work).parent
    study = work/'study'
    need(study.is_dir(),'Explicit package-relative study layout')
    original_study = Path(case['original_study'])
    original_component = Path(case['original_component'])
    auth = {}
    allowed = {(table,index) for table,indices in case['authentication_identity_only'].items() for index in indices}
    need(sum(map(len,case['authentication_identity_only'].values())) == len(allowed),'Distinct authentication row selectors')
    seen = set()
    for name,base in (('bindings',study),('exports',component_dir)):
        rows = json.loads(rt.resolve(case[name],work).read_bytes())
        if name == 'exports':
            rows = rows['exports']
        for index,row in enumerate(rows):
            need({'path','bytes','sha256'} <= set(row),'Exact original authentication row')
            relative = Path(row['path'])
            need(not relative.is_absolute() and '..' not in relative.parts,'Literal relative authentication locator')
            current = (base/relative).absolute()
            old_base = original_study if name == 'bindings' else original_component
            old = str(old_base/relative)
            identity = dict(bytes=row['bytes'],sha256=row['sha256'])
            if current in auth:
                need(auth[current]['identity'] == identity,'Consistent duplicate authentication identity')
            row_id = (name,index)
            seen.add(row_id)
            previous = auth.get(current,{}).get('row_ids',set())
            auth[current] = dict(identity=identity,original=old,kind=name,row_ids=previous|{row_id})
    # Some component37 history locators are authenticated by verify_history.
    for table_index,key in enumerate(case['additional_authentication_tables']):
        path = rt.resolve(key,work)
        for index,row in enumerate(json.loads(path.read_bytes())):
            if row['kind'] == 'supplied_software_hash':
                continue
            relative = Path(row['local_path'])
            need(not relative.is_absolute() and '..' not in relative.parts,'Literal historical local path')
            current = (component_dir/relative).absolute()
            identity = {k:row[k] for k in ('bytes','sha256')}
            if current in auth:
                need(auth[current]['identity'] == identity,'History/export identity agreement')
            row_id = ('history'+str(table_index),index)
            seen.add(row_id)
            previous = auth.get(current,{}).get('row_ids',set())
            auth[current] = dict(identity=identity,original=str(original_component/relative),kind='history',row_ids=previous|{row_id})
    actual = {rt.resolve(key,work).absolute():key for key in case['inputs']}
    need(allowed <= seen,'Every declared historical boundary names an actual authentication row')
    need(allowed == {i for q,row in auth.items() if q not in actual for i in row['row_ids']},
         'Exact authentication-only complement of all real materialized inputs')
    observations = dict(authenticated_materialized=set(),historical_identity_only={},compiler_commands=[])

    def portable_path(value='.'):
        q = Path(value)
        # A fresh output can itself lie under the old study root. Preserve
        # materialized inputs and output arguments before consulting old aliases.
        if q.is_absolute() and q.is_relative_to(output):
            return q
        if q.is_absolute() and (q.is_relative_to(original_study) or any(
                q.is_relative_to(Path(root)) for root in case['other_original_roots'])):
            # Only a declared alias with real preserved bytes may become a
            # data path. Missing historical binaries never get a fake file.
            key,_ = rt.entry(str(q))
            need(key in case['inputs'],'Explicit semantic absolute-path input')
            return rt.resolve(key,work)
        return q

    def portable_pin(value):
        q = Path(value).absolute()
        if q in actual:
            result = original_pin(q)
            item = rt.files[actual[q]]
            need(all(result[k] == item[k] for k in ('bytes','sha256')),'Fresh runtime input hash')
            observations['authenticated_materialized'].add(actual[q])
            return result
        if q in auth:
            declared = auth[q]
            need(declared['row_ids'] <= allowed,
                 'Exact reviewed non-runtime authentication boundary')
            observations['historical_identity_only'][declared['original']] = declared['identity']
            result = dict(declared['identity'])
            if case['pin_includes_path']:
                result['path'] = str(q)
            return result
        need(q.is_relative_to(output),'Undeclared pin is not a new execution output')
        return original_pin(q)

    def portable_execute(command,out,inputs,seconds,expected_report=None):
        argv = [str(x) for x in command]
        if argv and argv[0] == 'clang++':
            need(argv.count('-I/opt/homebrew/include') == argv.count('-L/opt/homebrew/lib') == 1
                 and all(flag in argv for flag in ('-std=c++17','-DWORDSIZE=64','-lnauty')),
                 'Exact existing nauty64 compiler invocation')
            before = list(argv)
            argv[0] = str(compiler)
            argv[argv.index('-I/opt/homebrew/include')] = '-I'+str(include)
            argv[argv.index('-L/opt/homebrew/lib')] = '-L'+str(library)
            need(len(argv)==len(before),'Only three existing compiler arguments substituted')
            observations['compiler_commands'].append(dict(original=before,configured=argv))
        # All native/Python scientific arguments, inputs, timeouts, reports and
        # original run_closed receipt checks are forwarded without alteration.
        return original_execute(argv,out,inputs,seconds,expected_report)

    module.Path = portable_path
    module.pin = portable_pin
    module.execute = portable_execute
    return study,observations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--modes-sha256',required=True)
    parser.add_argument('--component',required=True)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--compiler',type=Path)
    parser.add_argument('--nauty-include',type=Path)
    parser.add_argument('--nauty-library',type=Path)
    parser.add_argument('--full-check',action='store_true')
    args = parser.parse_args()
    raw = R.regular(args.root,'data/edge_girth_regular_graphs/matching_five_manifest_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.modes_sha256,'Exact external matching-mode declaration')
    modes = json.loads(raw)
    need(modes['schema'] == 'F012_PORTABLE_MATCHING_CHECKS_V1','Matching-mode schema')
    rt = R.Runtime(args.root,modes['runtime_manifest'],modes['runtime_manifest_sha256'])
    case = modes['components'][args.component]
    if not args.full_check:
        print(json.dumps(dict(status='DECLARED_MATCHING_CHECK_NOT_EXECUTED',component=args.component,
            case=case,whole_source_credit=0),indent=2))
        return
    need(args.out is not None and not args.out.exists() and not args.out.is_symlink(),'Fresh component output')
    for path in (args.compiler,args.nauty_include,args.nauty_library):
        need(path is not None and path.is_absolute(),'Explicit compiler and compatible nauty64 environment')
    output = args.out.absolute()
    rt.verify(case['inputs'])
    output.mkdir()
    work = output/'inputs'
    rt.materialize(case['inputs'],work)
    module = import_original(rt,work,case)
    scientific = output/'scientific'
    study,observations = install_adapters(module,rt,work,case,output,
        args.compiler,args.nauty_include,args.nauty_library)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.argv = [str(rt.resolve(case['entrypoint'],work)),'--study',str(study),'--out',str(scientific)]
    # No render, sanitizer-option or recorded-target option is implicitly added.
    # Any bounded controls the original default requires remain unchanged.
    module.main()
    result = json.loads((scientific/'report.json').read_bytes())
    need(result['status'] == case['expected_status'],'Entire original scientific main completed')
    for key in case['inputs']:
        rt.resolve(key,work)
    rt.verify(case['inputs'])
    report = dict(status='CHECKED_PORTABLE_MATCHING_COMPONENT',component=args.component,
        original_report=R.digest(scientific/'report.json'),runtime_inputs=len(case['inputs']),
        fresh_runtime_pin_queries=sorted(observations['authenticated_materialized']),
        historical_identity_queries=observations['historical_identity_only'],
        historical_payloads_freshly_verified=False,old_executable_used=False,
        compiler_substitutions=observations['compiler_commands'],
        mathematical_main_unchanged=True,recorded_target_mode=False,
        whole_source_credit=0)
    (output/'portable_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],component=args.component,whole_source_credit=0)))


if __name__ == '__main__':
    main()
