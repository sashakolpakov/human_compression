"""Complete unchanged two-octagon forest checker with its exact direct children."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import psutil

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
STUDY = Path('/Users/sasha/medusa/research/leemans')
PACKAGE = STUDY/'computation/f012/source_synthesis/package'
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/catalogue_inventory_dispatch.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/catalogue_check_modes.json'


def need(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    path = Path(path)
    h = hashlib.sha256()
    with path.open('rb') as source:
        for part in iter(lambda: source.read(1048576), b''):
            h.update(part)
    return dict(path=str(path), bytes=path.stat().st_size, sha256=h.hexdigest())


def normalized_capture(text, enabled):
    if not enabled:
        return text
    lines = text.splitlines(keepends=True)
    need(lines, 'Nonempty actual native capture')
    match = re.fullmatch(r'(SUMMARY COMPLETE NODES [0-9]+ POSITIVES [01] SECONDS )([0-9.e+\-]+)\n', lines[-1])
    need(match is not None, 'Exact complete native summary, not a deadline')
    seconds = float(match[2])
    need(0 <= seconds <= 90, 'Finite bounded native timing')
    lines[-1] = match[1]+'<seconds>\n'
    return ''.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'component', 'script', 'modes', 'compiler', 'expected_report',
        'children', 'authentication_identity_only', 'reference_report', 'scope'}, 'Exact case fields')
    need(case['schema'] == 'F012_ISOLATED_CUBIC_TWO_OCTAGONS_V1' and case['component'] == '49', 'Only atlas 49')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Exact acquired relocation interface')
    modes = json.loads(MODES.read_bytes())
    declaration = modes['components']['49']
    need(declaration['number'] == 49 and len(declaration['inputs']) == 67
         and declaration['materialized_bytes'] == 1174180
         and declaration['entrypoint'] == 'components/cubic_two_octagons/check.py'
         and declaration['authentication_identity_only'] == case['authentication_identity_only']
         and declaration['historical_executable_identities'] == {}, 'Complete mode and documentary complement')
    compiler = case['compiler']
    cp = Path(compiler['path'])
    need(cp.is_absolute() and cp.name == 'clang++' and cp.is_file() and not cp.is_symlink()
         and os.access(cp, os.X_OK) and pin(cp) == compiler, 'Pinned external compiler')
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Exact manifest')
    manifest = json.loads(manifest_path.read_bytes())
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    work, scientific = output/'inputs', output/'scientific'
    entry = work/manifest['files'][declaration['entrypoint']]['materialized_path']
    semantic = [(work/manifest['files'][key]['materialized_path'], manifest['files'][key]) for key in declaration['inputs']]
    locations = dict(PY=sys.executable, P=str(entry.parent), O=str(scientific), S=str(work/'study'))
    schedule = [dict(row, command=[x.format_map(locations) for x in row['command']]) for row in case['children']]
    need(len(schedule) == 41 and sum(x['timeout'] for x in schedule) == 1275
         and [x['name'] for x in schedule[5:14]] == ['target_'+str(i) for i in range(9)], 'All original direct calls')
    calls, denied = [], []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def verify_materialized():
        for path, row in semantic:
            actual = pin(path)
            need(path.is_relative_to(work) and not path.is_symlink()
                 and all(actual[k] == row[k] for k in ('bytes', 'sha256')), 'Whole exact materialized closure')

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 262144, 'Bounded complete direct-child records')
        (output/'finite_processes.json').write_bytes(raw)

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
        i = len(calls)
        need(active is None and 0 <= i < len(schedule), 'Exact finite original sequence')
        row = schedule[i]
        command = row['command']
        if i == 0:
            command = [sys.executable, '-E', '-B', str(SCRIPT), '--root', str(PACKAGE),
                '--modes-sha256', case['modes']['sha256'], '--component', '49', '--legacy-child',
                '--work', str(work), '--outer-output', str(output), '--legacy-output', str(scientific/'inventory.json')]
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPYCACHEPREFIX=str(scientific/'python_cache'))
        environment.pop('PYTHONOPTIMIZE', None)
        if row['environment'] == 'optimized':
            environment['PYTHONOPTIMIZE'] = '1'
        else:
            need(row['environment'] == 'plain', 'Exact original environment mode')
        need(len(values) == 1 and type(values[0]) is list and values[0] == command
             and set(keywords) == {'capture_output', 'input', 'timeout', 'env', 'cwd'}
             and keywords['capture_output'] is True and keywords['input'] is None
             and type(keywords['timeout']) is int and keywords['timeout'] == row['timeout']
             and keywords['env'] == environment and keywords['cwd'] is None,
             'Exact original argv/capture/stdin/timeout/environment/cwd and one acquired relocation')
        need(shutil.which('clang++') == str(cp) and pin(cp) == compiler, 'Pinned inherited compiler')
        verify_materialized()
        active = dict(command=command, environment=environment, row=row, observed=False)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'] and type(result.stdout) is bytes and type(result.stderr) is bytes,
                 'Actual original byte-capture child return')
            need(result.returncode == row['returncode'], 'Exact original success or damage/guard rejection')
            capture = output/'children'
            capture.mkdir(exist_ok=True)
            for suffix, raw in [('stdout', result.stdout), ('stderr', result.stderr)]:
                need(len(raw) <= 2**20, 'Bounded full direct child capture')
                expected = row[suffix]
                need(normalized_capture(raw.decode('utf-8'), suffix == 'stdout' and row['native_seconds_field'])
                     == normalized_capture(expected, suffix == 'stdout' and row['native_seconds_field']),
                     'Whole acquired capture equality except one declared native seconds scalar')
                path = capture/(str(i)+'.'+suffix)
                with path.open('xb') as stream: stream.write(raw)
                calls[-1][suffix] = pin(path)
            save_calls()
            return result
        finally:
            active = None

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path)); raise PermissionError('Private study access denied')
        if event == 'subprocess.Popen':
            need(active is not None and not active['observed'] and len(calls) < 41
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] == active['environment'], 'Only the exact original direct child')
            active['observed'] = True
            row = active['row']
            calls.append(dict(name=row['name'], command=list(values[1]), original_command=row['command'],
                timeout=row['timeout'], environment=row['environment'], cwd=None, capture='bytes',
                environment_sha256=hashlib.sha256(json.dumps(values[3], sort_keys=True).encode()).hexdigest()))
        if event in ('os.system', 'os.exec', 'os.fork', 'os.forkpty', 'os.posix_spawn'):
            raise PermissionError('Undeclared Python process interface')
        if event.startswith('socket.'):
            raise PermissionError('Network denied')
    sys.addaudithook(audit)
    forbidden = STUDY/'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError('Private-open positive control failed')
    need(denied == [str(forbidden)], 'One actual private-open rejection')
    sys.path[:] = [x for x in sys.path if x and not Path(x).absolute().is_relative_to('/Users/sasha/medusa')]
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
            '--component', '49', '--full-check', '--out', str(output),
            '--compiler', str(cp), '--compiler-sha256', compiler['sha256']]
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    need(len(calls) == 41 and all(c.get('reaped') and c.get('returncode') == schedule[i]['returncode']
         for i,c in enumerate(calls)), 'Complete original direct returns')
    result_path = scientific/'report.json'
    actual = json.loads(result_path.read_bytes())
    need(set(actual) == set(case['expected_report']) | {'checks'}
         and {k:v for k,v in actual.items() if k != 'checks'} == case['expected_report'],
         'Whole original scientific report, complete fresh default and no render')
    need(len(actual['checks']) == 41, 'Complete original report child array')
    for i,(row,observed) in enumerate(zip(actual['checks'],calls)):
        need(set(row) == {'name','command','returncode','seconds','stdout','stderr'}
             and row['name'] == observed['name'] and row['command'] == observed['original_command']
             and row['returncode'] == observed['returncode']
             and type(row['seconds']) in (int,float) and 0 <= row['seconds'] <= schedule[i]['timeout']+5,
             'Entire original child row and actual finite duration')
        for suffix in ('stdout','stderr'):
            raw = (scientific/(row['name']+'.'+suffix)).read_bytes()
            need(raw == Path(observed[suffix]['path']).read_bytes()
                 and row[suffix] == dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),
                 'Original report/capture pin and full recorded bytes agree')
    portable_path = output/'portable_report.json'
    portable = json.loads(portable_path.read_bytes())
    expected_substitution = dict(original=schedule[0]['command'],configured=calls[0]['command'])
    need(portable['status'] == 'CHECKED_PORTABLE_CATALOGUE_COMPONENT' and portable['component'] == '49'
         and portable['runtime_inputs'] == 67 and portable['mathematical_predicates_unchanged'] is True
         and portable['historical_payloads_freshly_verified'] is False and portable['historical_executables_run'] is False
         and portable['render'] is False and portable['whole_source_credit'] == 0
         and portable['observed'] == dict(historical_executable_identities=[],compiler_substitutions=[],child_substitutions=[expected_substitution])
         and portable['original_result'] == [pin(result_path)['bytes'],pin(result_path)['sha256']],
         'Truthful acquired relocation and authentication boundary')
    need(json.loads((scientific/'inventory.json').read_bytes()) == case['expected_report']['inventory']
         and json.loads((scientific/'kernel/report.json').read_bytes()) == case['expected_report']['kernel'],
         'Complete original inventory and literal rollback-control results')
    verify_materialized()
    need(denied == [str(forbidden)], 'No parent scientific private reads')
    report = dict(status='PASS_ISOLATED_PORTABLE_CUBIC_TWO_OCTAGONS',component=49,case=case,
        source_inputs=[pin(p) for p,_ in semantic],result=pin(result_path),portable=pin(portable_path),
        finite_processes=pin(output/'finite_processes.json'),actual_direct_children=41,
        unchanged_nested_kernel_calls=2,private_open_positive_control=True,scientific_parent_private_open_attempts=0,
        scientific_source_unchanged=True,whole_original_report_checked=True,scope=case['scope'],whole_source_credit=0,
        qualification='Python parent audit does not survive exec. The acquired relocated inventory child and unchanged kernel child (two nested calls) remain explicit software premises; descendant identities are sampled by the inherited family guard, not asserted fully observed. No full OS sandbox or fresh independent verifier is claimed.')
    with (output/'isolation.json').open('x') as stream: json.dump(report,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(status=report['status'],component=49)),flush=True)


if __name__ == '__main__':
    main()
