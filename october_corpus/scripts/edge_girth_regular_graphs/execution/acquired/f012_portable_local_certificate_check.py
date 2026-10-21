"""Run one finite package check retaining exactly two optimization-guard children."""
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


def guard_source(raw, policy, expected_sha256):
    """Check the actual child source before either real Popen."""
    need(hashlib.sha256(raw).hexdigest() == expected_sha256, 'Exact child source')
    tree = ast.parse(raw)
    body = tree.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    imports = []
    while body and isinstance(body[0], (ast.Import, ast.ImportFrom)):
        node, body = body[0], body[1:]
        imports.extend([a.name for a in node.names] if isinstance(node, ast.Import) else [node.module])
    need(imports == policy['guard']['only_prior_imports'], 'Exact standard-library prefix')
    wanted = ast.parse("if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):\n"
                       "    raise RuntimeError('Optimized Python is not accepted')").body[0]
    need(body and ast.dump(body[0]) == ast.dump(wanted), 'First executable guard before scientific imports')
    need(hashlib.sha256(ast.dump(body[0]).encode()).hexdigest() == policy['guard']['ast_sha256'],
         'Bound guard AST')
    loops = [n for n in ast.walk(tree) if isinstance(n, ast.For)
             and n.lineno == policy['exact_child_loop']['line']]
    need(len(loops) == 1 and hashlib.sha256(ast.dump(loops[0]).encode()).hexdigest()
         == policy['exact_child_loop']['ast_sha256'], 'Unchanged complete optimization loop')


def checked_call(index, values, keywords, entry, environment):
    """Pure exact-boundary check; the real subprocess.run still executes."""
    need(index in (0, 1), 'Exactly two optimization controls')
    command = [sys.executable] + (['-O'] if index == 0 else []) + [str(entry)]
    env = dict(environment)
    need(not env.get('PYTHONOPTIMIZE'), 'Ordinary parent environment')
    if index == 1:
        env['PYTHONOPTIMIZE'] = '1'
    need(len(values) == 1 and type(values[0]) is list and values[0] == command,
         'Exact original optimization argv and order')
    need(set(keywords) == {'env', 'capture_output', 'text', 'timeout'}
         and keywords['capture_output'] is True and keywords['text'] is True
         and type(keywords['timeout']) is int and keywords['timeout'] == 5
         and type(keywords['env']) is dict and keywords['env'] == env,
         'Exact original environment/capture/text/timeout semantics')
    return command, env


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
    need(case['component'] in ('32', '33', '34'), 'Reviewed finite-child modes')
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
    calls, denied = [], []
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

    def exact_run(*values, **keywords):
        nonlocal active
        need(active is None, 'No nested process request')
        command, env = checked_call(len(calls), values, keywords, entry, os.environ)
        raw = entry.read_bytes()
        need(len(raw) == entry_info['bytes'], 'Exact materialized child source length')
        guard_source(raw, policy, selection['source_sha256'])
        active = dict(command=command, env=env, observed=False)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Real audited Popen occurred')
            calls[-1].update(stdout_sha256=hashlib.sha256(result.stdout.encode()).hexdigest(),
                             stderr_sha256=hashlib.sha256(result.stderr.encode()).hexdigest(),
                             stderr_bytes=len(result.stderr.encode()))
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
            need(active is not None and not active['observed'] and len(calls) < 2
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] == active['env'],
                 'Only the active exact original subprocess.run child')
            active['observed'] = True
            calls.append(dict(command=list(values[1]), role=('argument', 'environment')[len(calls)]))
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
    need(len(calls) == 2 and all(x['reaped'] and x['returncode'] != 0 for x in calls),
         'Both real optimization rejections completed and reaped')
    for call in calls:
        stderr = (output/'scientific'/('guard_'+call['role']+'.stderr')).read_bytes()
        need(len(stderr) == call['stderr_bytes'] and hashlib.sha256(stderr).hexdigest() == call['stderr_sha256']
             and b'Optimized Python is not accepted' in stderr, 'Original retained child stderr')
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
