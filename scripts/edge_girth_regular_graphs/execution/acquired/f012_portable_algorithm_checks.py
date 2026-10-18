"""Both complete declared algorithm defaults, with exact adjacent imports."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import runpy
import sys

if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
STUDY = Path('/Users/sasha/medusa/research/leemans')
PACKAGE = STUDY/'computation/f012/source_synthesis/package'
PREPARER = PACKAGE/'scripts/edge_girth_regular_graphs/prepare_check.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/execution_modes.json'


def need(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed application case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'preparer', 'modes', 'applications', 'scope'}, 'Complete algorithm case')
    need(case['schema'] == 'F012_TWO_COMPLETE_ALGORITHM_DEFAULTS_V1', 'Fixed paired case')
    need(pin(PREPARER) == case['preparer'] and pin(MODES) == case['modes'], 'Exact acquired preparer and modes')
    modes = json.loads(MODES.read_bytes())
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Exact runtime manifest')
    manifest = json.loads(manifest_path.read_bytes())
    names = ['algorithm_reference', 'printed_algorithm_counterexample']
    need([a['mode'] for a in case['applications']] == names, 'Both full defaults in fixed order')
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output required')
    denied = []

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study access denied')
        if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.fork', 'os.posix_spawn'):
            raise PermissionError('This pure replay cannot launch children')
        if event.startswith('socket.'):
            raise PermissionError('This pure replay cannot use the network')

    sys.addaudithook(audit)
    forbidden = STUDY/'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError('Private-open positive control failed')
    need(denied == [str(forbidden)], 'Exact positive denial')
    sys.path[:] = [x for x in sys.path if x and not Path(x).absolute().is_relative_to(Path('/Users/sasha/medusa'))]
    base_path = list(sys.path)
    output.mkdir()
    results = []
    for selected in case['applications']:
        need(set(selected) == {'mode', 'entrypoint', 'local_imports', 'expected', 'expected_report',
            'normalization', 'scope'}, 'Complete individual application')
        name = selected['mode']
        mode = modes['modes'][name]
        reference = name == 'algorithm_reference'
        expected_environment = 'ignore_environment_with_exact_local_imports' if reference else 'isolated'
        expected_entry = 'components/algorithm/' + ('check_reference.py' if reference else 'check_counterexample_independently.py')
        expected_imports = {'reference': 'components/algorithm/reference.py'} if reference else {}
        need(not mode['configured_compiler'] and mode['python_environment'] == expected_environment
             and len(mode['commands']) == 1 and mode['authentication_only'] == [], 'Declared complete pure mode')
        need(selected['entrypoint'] == mode['commands'][0]['entrypoint'] == expected_entry
             and selected['local_imports'] == expected_imports, 'Exact entrypoint and adjacent import')
        need(selected['normalization'] == ('top_level_seconds_only' if reference else 'none'), 'Only original reference timing varies')
        need(all(module not in sys.modules for module in expected_imports), 'Fresh adjacent module names')
        work = output/(name+'_inputs')
        result = output/name
        sys.argv = [str(PREPARER), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
                    '--mode', name, '--work', str(work), '--check-output', str(result)]
        runpy.run_path(str(PREPARER), run_name='__main__')
        prepared = json.loads((work/'checker_commands.json').read_bytes())
        need(prepared['status'] == 'EXACT_CHECKER_INPUTS_PREPARED_NO_SCIENTIFIC_EXECUTION'
             and prepared['mode'] == name and len(prepared['commands']) == 1
             and prepared['authentication_only'] == []
             and prepared['materialization']['files'] == mode['inputs'], 'Exact complete prepared input roster')
        script = work/manifest['files'][expected_entry]['materialized_path']
        expected_command = [sys.executable, '-E' if reference else '-I', '-B', str(script)]
        expected_command += ['--out', str(result)] if reference else [str(result)]
        need(prepared['commands'] == [expected_command], 'Entire original command and argument interface')
        materialized = [work/manifest['files'][key]['materialized_path'] for key in mode['inputs']]
        before = list(map(pin, materialized))
        for key, actual in zip(mode['inputs'], before):
            declared = manifest['files'][key]
            need(all(actual[k] == declared[k] for k in ('bytes', 'sha256')), 'Exact materialized scientific bytes')
        need(script.is_relative_to(work) and script.is_file() and not script.is_symlink(), 'Materialized original main')
        if reference:
            sys.path.insert(0, str(script.parent))
        try:
            sys.argv = expected_command[3:]
            runpy.run_path(str(script), run_name='__main__')
            for module, key in expected_imports.items():
                actual_module = sys.modules.get(module)
                expected_path = work/manifest['files'][key]['materialized_path']
                need(actual_module is not None and Path(actual_module.__file__).resolve() == expected_path.resolve(),
                     'Actual adjacent import is the exact materialized source')
        finally:
            sys.path[:] = base_path
            for module in expected_imports:
                sys.modules.pop(module, None)
        report_path = result/'report.json'
        raw = report_path.read_bytes()
        actual = json.loads(raw)
        seconds = None
        if reference:
            need(set(actual) == set(selected['expected']) | {'seconds'}, 'All original reference fields')
            seconds = actual['seconds']
            need(type(seconds) in (int, float) and math.isfinite(seconds) and 0 <= seconds <= 60,
                 'Finite bounded actual reference duration')
            comparable = {k: v for k, v in actual.items() if k != 'seconds'}
            comparison_bytes = (json.dumps(comparable, indent=2)+'\n').encode()
        else:
            comparable, comparison_bytes = actual, raw
        need(comparable == selected['expected'], 'Complete original scientific report, not just totals')
        expected_report = selected['expected_report']
        need(len(comparison_bytes) == expected_report['bytes']
             and hashlib.sha256(comparison_bytes).hexdigest() == expected_report['sha256'],
             'Whole exact reference report after only the declared timing removal')
        need(before == list(map(pin, materialized)), 'All selected input bytes unchanged')
        need(denied == [str(forbidden)], 'No scientific private access')
        results.append(dict(mode=name, source_inputs=before, prepared_command=expected_command,
            result=pin(report_path), normalization=selected['normalization'], actual_reference_seconds=seconds,
            complete_report_checked=True, local_imports_checked=expected_imports, scientific_child_calls=0))
    need(len(results) == 2 and [r['mode'] for r in results] == names, 'Both full defaults returned')
    report = dict(status='PASS_ISOLATED_PORTABLE_ALGORITHM_DEFAULTS', case=case, applications=results,
        private_open_positive_control=True, scientific_private_open_attempts=0, children_and_network_denied=True,
        execution='Both unchanged mains via runpy in the -E -B owner child; exact adjacent import only for reference.',
        qualification='No sys.flags.isolated or OS sandbox claim. Original outer mutation/optimization/render controls remain historical premises.',
        source_credit=0, whole_source_credit=0, atlas_increment=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=report['status'], modes=names, whole_source_credit=0)), flush=True)


if __name__ == '__main__':
    main()
