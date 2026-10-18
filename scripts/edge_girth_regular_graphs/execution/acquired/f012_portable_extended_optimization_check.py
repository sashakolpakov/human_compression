"""Run modes 35/47/48 with all exact original optimization-guard children."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys
import subprocess
import psutil

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
STUDY = Path('/Users/sasha/medusa/research/leemans')
PACKAGE = STUDY/'computation/f012/source_synthesis/package'
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/finite_checks_relocation.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/finite_check_modes.json'


def need(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for part in iter(lambda: source.read(1048576), b''):
            h.update(part)
    return dict(path=str(path), bytes=path.stat().st_size, sha256=h.hexdigest())


def guard_source(component, child, sources, policy):
    """Only parse exact materialized sources; never execute a guard as a fixture."""
    trees = {}
    need(set(sources) == set(policy['sources']), 'Exact child source closure')
    for name, raw in sources.items():
        declared = policy['sources'][name]
        need(len(raw) == declared['bytes'] and hashlib.sha256(raw).hexdigest() == declared['sha256'],
             'Exact materialized child source')
        trees[name] = ast.parse(raw)
    entry_tree = trees['check.py']
    loops = [n for n in ast.walk(entry_tree) if isinstance(n, ast.For)
             and n.lineno == policy['exact_child_loop']['line']]
    need(len(loops) == 1 and hashlib.sha256(ast.dump(loops[0]).encode()).hexdigest()
         == policy['exact_child_loop']['ast_sha256'], 'Unchanged entire optimization loop')
    if component == '35':
        need(child == 'check.py' and set(trees) == {'check.py', 'local_model.py'}, 'One imported early guard')
        prefix = ast.parse('import argparse,json,hashlib,subprocess,shutil,os,sys\n'
                           'from pathlib import Path\nfrom local_model import *').body
        need([ast.dump(x) for x in entry_tree.body[:3]] == [ast.dump(x) for x in prefix],
             'Entry reaches exact adjacent import before any scientific statement')
        prefix = ast.parse("import itertools,collections,math,sys,os\n"
                           "if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):\n"
                           "    raise RuntimeError('Optimized Python is not accepted')").body
        actual = trees['local_model.py'].body[:2]
    else:
        need(component in ('47', '48') and child in trees, 'Declared direct guarded script')
        prefix = ast.parse("import sys\nif sys.flags.optimize:\n"
                           "    raise SystemExit('optimized execution unsupported')").body
        actual = trees[child].body[:2]
    need([ast.dump(x) for x in actual] == [ast.dump(x) for x in prefix],
         'Exact early guard before scientific imports, argument parsing or file reads')


def child_plan(component, index, entry, output):
    count = 4 if component == '48' else 2
    need(component in ('35', '47', '48') and type(index) is int and 0 <= index < count,
         'Exact declared child count and selector')
    script = 'model_controls.py' if component == '48' and index >= 2 else 'check.py'
    envopt = bool(index % 2)
    role = 'environment' if envopt else 'argument'
    command = [sys.executable] + ([] if envopt else ['-O']) + [str(entry.parent/script)]
    target = None
    if component != '35':
        name = ('optimized'+str(envopt) if component == '47'
                else 'optimized_'+script+str(envopt))
        target = output/'scientific'/name
        if script == 'check.py':
            command += ['--study', str(output/'inputs/study'), '--out', str(target)]
    return dict(command=command, script=script, role=role, envopt=envopt,
                target=str(target) if target is not None else None,
                text=component == '35', timeout=5 if component == '35' else 10)


def checked_call(component, index, values, keywords, entry, output, environment):
    """Pure exact-boundary check; the real subprocess.run still executes."""
    plan = child_plan(component, index, entry, output)
    command = plan['command']
    env = dict(environment)
    need(not env.get('PYTHONOPTIMIZE'), 'Ordinary parent environment')
    if component != '35':
        env.pop('PYTHONOPTIMIZE', None)
    if plan['envopt']:
        env['PYTHONOPTIMIZE'] = '1'
    need(len(values) == 1 and type(values[0]) is list and values[0] == command,
         'Exact original optimization argv and order')
    fields = {'env', 'capture_output', 'timeout'} | ({'text'} if plan['text'] else set())
    need(set(keywords) == fields and keywords['capture_output'] is True
         and (not plan['text'] or keywords['text'] is True)
         and type(keywords['timeout']) is int and keywords['timeout'] == plan['timeout']
         and type(keywords['env']) is dict and keywords['env'] == env,
         'Exact original environment/capture/text/timeout semantics')
    return plan, env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Reviewed case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'script', 'modes', 'component', 'expected', 'scope', 'optimization_scope'}, 'Exact case fields')
    need(case['schema'] == 'F012_ISOLATED_FINITE_OPTIMIZATION_CASE_V1', 'Case schema')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Reviewed shared interface')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components'][case['component']]
    need(case['component'] in ('35', '47', '48'), 'Reviewed finite-child modes')
    need(selection['child_scope'] == 'Original optimized-Python rejection controls only; no compiler.',
         'Original child declaration retained')
    scope_path = Path(case['optimization_scope']['path'])
    need(pin(scope_path) == case['optimization_scope'], 'Exact reviewed source/child scope')
    scope = json.loads(scope_path.read_bytes())
    policies = [x for x in scope['cases'] if str(x['number']) == case['component']]
    need(len(policies) == 1, 'Unique reviewed child source')
    policy = policies[0]
    need(policy['entrypoint'] == selection['entrypoint']
         and policy['original_source']['sha256'] == selection['source_sha256'], 'Original mode/source join')
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Manifest identity')
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    manifest = json.loads(manifest_path.read_bytes())
    entry_info = manifest['files'][selection['entrypoint']]
    entry = output/'inputs'/entry_info['materialized_path']
    need(entry.is_relative_to(output/'inputs') and '..' not in entry.parts, 'Exact child input path')
    child_count = 4 if case['component'] == '48' else 2
    expected_sources = {'check.py': selection['entrypoint']}
    expected_sources.update({Path(key).name: key for key in selection['adjacent_modules'].values()})
    need(set(policy['sources']) == set(expected_sources), 'Exact original adjacent source roster')
    for name, key in expected_sources.items():
        info = manifest['files'][key]
        need(key in selection['inputs'] and policy['sources'][name]['key'] == key
             and all(policy['sources'][name][x] == info[x] for x in ('bytes', 'sha256'))
             and output/'inputs'/info['materialized_path'] == entry.parent/name,
             'Exact adjacent materialization/source binding')
    calls, denied = [], []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 65536, 'Bounded optimization-child observation')
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

    def exact_run(*values, **keywords):
        nonlocal active
        need(active is None, 'No nested process request')
        plan, env = checked_call(case['component'], len(calls), values, keywords, entry, output, os.environ)
        sources = {name: (entry.parent/name).read_bytes() for name in expected_sources}
        guard_source(case['component'], plan['script'], sources, policy)
        active = dict(command=plan['command'], env=env, observed=False, plan=plan)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Real audited Popen occurred')
            raw_out = result.stdout.encode() if plan['text'] else result.stdout
            raw_err = result.stderr.encode() if plan['text'] else result.stderr
            need(type(raw_out) is bytes and type(raw_err) is bytes, 'Original capture types')
            capture = output/'optimization_children'
            capture.mkdir(exist_ok=True)
            stem = str(len(calls)-1)
            for suffix, raw in [('stdout', raw_out), ('stderr', raw_err)]:
                need(len(raw) <= 65536, 'Bounded guard capture')
                with (capture/(stem+'.'+suffix)).open('xb') as stream:
                    stream.write(raw)
            calls[-1].update(stdout=pin(capture/(stem+'.stdout')), stderr=pin(capture/(stem+'.stderr')))
            save_calls()
            return result
        finally:
            active = None

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study read denied')
        if event == 'subprocess.Popen':
            need(active is not None and not active['observed'] and len(calls) < child_count
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] == active['env'],
                 'Only the active exact original subprocess.run child')
            active['observed'] = True
            calls.append(dict(command=list(values[1]), role=active['plan']['role'],
                              script=active['plan']['script'], target=active['plan']['target']))
        if event in ('os.system', 'os.exec', 'os.fork', 'os.forkpty', 'os.posix_spawn'):
            raise PermissionError('Undeclared process interface')
        if event.startswith('socket.'):
            raise PermissionError('Network denied')

    sys.addaudithook(audit)
    forbidden = STUDY/'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise RuntimeError('Private-read denial control failed')
    need(denied == [str(forbidden)], 'One positive denial control')
    sys.path[:] = [p for p in sys.path if p and not Path(p).absolute().is_relative_to('/Users/sasha/medusa')]
    sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
                '--component', case['component'], '--out', str(output), '--full-check']
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    portable = json.loads((output/'portable_report.json').read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_FINITE_COMPONENT'
         and portable['component'] == case['component'], 'Complete portable return')
    result_path = output/'scientific'/selection['result_relative']
    need([pin(result_path)['bytes'], pin(result_path)['sha256']] == portable['original_result'], 'Result binding')
    result = json.loads(result_path.read_bytes())
    for condition in case['expected']:
        need(set(condition) == {'pointer', 'value'}, 'Literal expected result')
        value = result
        for field in condition['pointer']:
            value = value[field]
        need(value == condition['value'], 'Expected field '+str(condition['pointer']))
    need(denied == [str(forbidden)], 'No scientific private reads')
    need(len(calls) == child_count and all(x['reaped'] and x['returncode'] != 0 for x in calls),
         'All original real optimization rejections completed and reaped')
    for call in calls:
        stderr = Path(call['stderr']['path']).read_bytes()
        need(pin(Path(call['stderr']['path'])) == call['stderr'], 'Actual retained child stderr')
        marker = b'Optimized Python is not accepted' if case['component'] == '35' else b'optimized execution unsupported'
        need(marker in stderr, 'Original optimization rejection marker')
        if case['component'] == '35':
            need((output/'scientific'/('guard_'+call['role']+'.stderr')).read_bytes() == stderr,
                 'Original retained guard file equals actual capture')
        else:
            need(not Path(call['target']).exists(), 'Original forbidden child output stays absent')
    record = dict(status='PASS_ISOLATED_PORTABLE_FINITE_OPTIMIZATION_COMPONENT', component=case['component'],
                  result=pin(result_path), portable_report=pin(output/'portable_report.json'),
                  private_open_positive_control=True, scientific_private_open_attempts=0,
                  optimization_children=calls, all_other_children_and_network_denied=True,
                  child_boundary='Parent audit does not survive exec; exact original early guard precedes all scientific imports and reads.',
                  reported_binding_counts='Historical row identities; actual materialized input count and authentication dispositions are in portable_report.',
                  historical_new_row_fields_are_not_fresh_credit=True, whole_source_credit=0,
                  scope=case['scope'],
                  isolation='Python -E -B owner child with project import roots removed and audit guards; no claim that sys.flags.isolated is set.')
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=record['status'], component=case['component'])), flush=True)


if __name__ == '__main__':
    main()
