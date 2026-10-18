"""Exact order-18 package main and its two original optimization rejects."""
import argparse
import hashlib
import json
import math
import ast
import subprocess
import psutil
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


def need(value,message):
    if not value:
        raise ValueError(message)


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def timing_paths():
    return ([['classes', i, 'seconds'] for i in range(27)]
            + [['controls', 'order16_control', i, 'seconds'] for i in range(4)]
            + [['controls', 'order15_positive_search', 'seconds']])


def normalize(report):
    value = json.loads(json.dumps(report))
    for path in timing_paths():
        parent = value
        for key in path[:-1]:
            parent = parent[key]
        seconds = parent[path[-1]]
        need(type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
             'Nonnegative finite original elapsed time at '+str(path))
        parent[path[-1]] = None
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--case',type=Path,required=True)
    parser.add_argument('--case-sha256',required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256,'Exact reviewed application case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema','mode','preparer','modes','entrypoint','expected','scope','timing_paths'},'Complete order18 case')
    need(case['schema'] == 'F012_ISOLATED_ORDER18_CHECK_CASE_V1'
         and case['mode'] == 'order18'
         and case['entrypoint'] == 'components/order18/check_order18.py'
         and case['timing_paths'] == timing_paths(), 'Exact order18 mode and 32 timing fields')
    need(len(case['expected']) == 1 and case['expected'][0]['pointer'] == [],
         'Whole normalized report comparison only')
    need(pin(PREPARER) == case['preparer'] and pin(MODES) == case['modes'],'Exact acquired preparer and modes')
    modes = json.loads(MODES.read_bytes())
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'],'Exact runtime declaration')
    manifest = json.loads(manifest_path.read_bytes())
    mode = modes['modes'][case['mode']]
    need(not mode['configured_compiler'] and mode['python_environment'] == 'isolated'
         and len(mode['commands']) == 1,'Only one declared isolated pure-Python entrypoint')
    need(mode['commands'][0]['entrypoint'] == case['entrypoint'],'Exact selected entrypoint')
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(),'Fresh output required')
    denied = []
    calls = []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 65536, 'Bounded two-child observation')
        (output/'optimization_processes.json').write_bytes(raw)

    class RecordedPopen(original_popen):
        def __init__(self, *values, **keywords):
            super().__init__(*values, **keywords)
            try:
                self.record = calls[-1]
                self.record.update(pid=self.pid, inherited_process_group=os.getpgrp())
                try:
                    self.record['birth'] = psutil.Process(self.pid).create_time()
                except psutil.Error as error:
                    self.record.update(birth=None, birth_observation_error=type(error).__name__)
                save_calls()
            except BaseException:
                try:
                    if self.poll() is None:
                        self.kill()
                finally:
                    self.wait(timeout=2)
                raise

        def __exit__(self, *values):
            try:
                return super().__exit__(*values)
            finally:
                self.record.update(returncode=self.returncode, reaped=self.returncode is not None)
                save_calls()

    def run_guards(script):
        nonlocal active
        tree = ast.parse(script.read_bytes())
        exact_guard = ast.parse('if sys.flags.optimize:raise RuntimeError("Optimized Python is not accepted")').body[0]
        need(isinstance(tree.body[1], ast.Import) and tree.body[1].names[0].name == 'sys'
             and ast.dump(tree.body[2]) == ast.dump(exact_guard),
             'Exact original guard before any scientific imports or main')
        guards = []
        subprocess.Popen = RecordedPopen
        try:
            for label, opts, env in [('argument', ['-O'], None),
                                     ('environment', [], dict(os.environ, PYTHONOPTIMIZE='1'))]:
                forbidden_output = output/('forbidden_'+label+'.json')
                command = [sys.executable, *opts, script.name, '--out', str(forbidden_output)]
                need(not forbidden_output.exists() and active is None, 'Fresh exact optimization control')
                active = dict(command=command, env=env, cwd=str(script.parent), observed=False)
                try:
                    value = original_run(command, cwd=script.parent, env=env, capture_output=True)
                    need(active['observed'], 'Real audited optimization child')
                    (output/(label+'.stdout')).write_bytes(value.stdout)
                    (output/(label+'.stderr')).write_bytes(value.stderr)
                    need(type(value.stdout) is bytes and type(value.stderr) is bytes
                         and value.returncode != 0 and not forbidden_output.exists()
                         and value.stdout == b''
                         and b'RuntimeError: Optimized Python is not accepted' in value.stderr,
                         'Original nonzero/no-output rejection from the exact early guard')
                    calls[-1].update(stdout=pin(output/(label+'.stdout')),
                                     stderr=pin(output/(label+'.stderr')))
                    save_calls()
                    guards.append(dict(name=label, returncode=value.returncode, no_output=True))
                finally:
                    active = None
        finally:
            subprocess.Popen = original_popen
        need(guards == [dict(name=name, returncode=1, no_output=True)
                        for name in ['argument', 'environment']], 'Both complete original controls')
        need(len(calls) == 2 and all(row.get('reaped') and row.get('returncode') == 1 for row in calls),
             'Both actual children returned and reaped')
        (output/'optimization_controls.json').write_text(json.dumps(guards, indent=2)+'\n')

    def audit(event,values):
        if event == 'open' and isinstance(values[0],(str,bytes,os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study access denied')
        if event == 'subprocess.Popen':
            need(active is not None and not active['observed'] and len(calls) < 2
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and str(values[2]) == active['cwd'] and values[3] == active['env'],
                 'Only the two exact original optimization children')
            active['observed'] = True
            calls.append(dict(command=list(values[1]), cwd=active['cwd'],
                              role=('argument','environment')[len(calls)]))
        if event in ('os.system','os.exec','os.fork','os.forkpty','os.posix_spawn'):
            raise PermissionError('Undeclared process interface')
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
    need(denied == [str(forbidden)],'Exact positive denial')
    # The owner starts -E -B. Remove study/project import roots as well;
    # actual isolation is enforced by the audit boundary, not a false claim
    # that this already running process has sys.flags.isolated set.
    sys.path[:] = [x for x in sys.path if x and not Path(x).absolute().is_relative_to(Path('/Users/sasha/medusa'))]
    output.mkdir()
    work = output/'inputs'
    result = output/'result.json'
    sys.argv = [str(PREPARER),'--root',str(PACKAGE),'--modes-sha256',case['modes']['sha256'],
                '--mode',case['mode'],'--work',str(work),'--check-output',str(result)]
    runpy.run_path(str(PREPARER),run_name='__main__')
    prepared = json.loads((work/'checker_commands.json').read_bytes())
    need(prepared['status'] == 'EXACT_CHECKER_INPUTS_PREPARED_NO_SCIENTIFIC_EXECUTION'
         and prepared['mode'] == case['mode'] and len(prepared['commands']) == 1,'One exact prepared command')
    command = prepared['commands'][0]
    need(command[:3] == [sys.executable,'-I','-B'] and command[-2:] == ['--out',str(result)]
         and len(command) == 6,'Exact pure entrypoint argv')
    script = Path(command[3])
    need(script.is_relative_to(work) and script.is_file() and not script.is_symlink(),'Materialized scientific source only')
    need(prepared['materialization']['files'] == mode['inputs'],'Complete selected input roster')
    materialized = [work/manifest['files'][key]['materialized_path'] for key in mode['inputs']]
    before = list(map(pin,materialized))
    run_guards(script)
    sys.argv = command[3:]
    runpy.run_path(str(script),run_name='__main__')
    raw_actual = json.loads(result.read_bytes())
    actual = normalize(raw_actual)
    (output/'normalized_result.json').write_text(json.dumps(actual, indent=2)+'\n')
    for condition in case['expected']:
        need(set(condition) == {'pointer','value'} and type(condition['pointer']) is list,'Literal expected JSON field')
        value = actual
        for field in condition['pointer']:
            value = value[field]
        need(value == condition['value'],'Exact literal result field '+str(condition['pointer']))
    after = list(map(pin,materialized))
    need(before == after,'All materialized scientific input bytes unchanged')
    need(denied == [str(forbidden)],'Scientific replay attempted private access')
    report = dict(status='PASS_ISOLATED_PORTABLE_ORDER18_COMPONENT',mode=case['mode'],
        case=case,source_inputs=before,result=pin(result),private_open_positive_control=True,
        scientific_private_open_attempts=0,undeclared_children_and_network_denied=True,
        optimization_controls=pin(output/'optimization_controls.json'),
        optimization_processes=pin(output/'optimization_processes.json'),
        normalized_result=pin(output/'normalized_result.json'),timing_fields_normalized=32,
        original_main_child_calls=0,actual_optimization_child_calls=2,
        execution='Unchanged script via runpy in -E -B owner child; project import roots removed and audit denial active.',
        source_credit=0,whole_source_credit=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(report,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(status=report['status'],mode=case['mode'],whole_source_credit=0)),flush=True)


if __name__ == '__main__':
    main()
