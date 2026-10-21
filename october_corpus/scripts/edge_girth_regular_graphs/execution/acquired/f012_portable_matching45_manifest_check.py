"""Execute one unchanged matching default with its complete declared child list."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import psutil

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
STUDY = Path('/Users/sasha/medusa/research/leemans')
PACKAGE = STUDY/'computation/f012/source_synthesis/package'
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/matching_five_manifest_relocation.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/matching_five_manifest_modes.json'
PLAN = Path(__file__).with_name('f012_matching_process_plan.py')


def need(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            digest.update(block)
    return dict(path=str(path), bytes=path.stat().st_size, sha256=digest.hexdigest())


def configured(plan, locations):
    return [dict(row, command=[x.format_map(locations) for x in row['command']],
        **({'directory':row['directory'].format_map(locations)} if 'directory' in row else {})) for row in plan]


def check_call(row, values, keywords, environment):
    need(len(values) == 1 and type(values[0]) is list and values[0] == row['command'],
         'Exact original child argv and sequence')
    env = dict(environment)
    env.pop('PYTHONOPTIMIZE', None)
    if row['environment'] == 'closed':
        env['ASAN_OPTIONS'] = 'detect_leaks=0:halt_on_error=1'
        env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
    elif row['environment'] == 'optimized':
        env['PYTHONOPTIMIZE'] = '1'
    else:
        need(row['environment'] == 'plain', 'Declared environment')
    need(keywords.get('env') == env and type(keywords.get('timeout')) is int
         and keywords['timeout'] == row['timeout'], 'Original exact environment and timeout')
    if row['capture'] == 'bytes':
        need(set(keywords) == {'capture_output', 'timeout', 'env'}
             and keywords['capture_output'] is True, 'Original byte-capture call')
    else:
        need(row['capture'] == 'files' and set(keywords) == {'stdout', 'stderr', 'timeout', 'env'},
             'Original closed execution file capture')
        for name in ('stdout', 'stderr'):
            stream = keywords[name]
            need(str(getattr(stream, 'name', '')) == row['directory']+'/'+name
                 and getattr(stream, 'mode', None) == 'wb' and not stream.closed,
                 'Exact original open capture file')
    return env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact concrete application')
    case = json.loads(args.case.read_bytes())
    need(case['schema'] == 'F012_ISOLATED_MATCHING_APPLICATION_V1'
         and case['component'] in tuple(map(str, range(38, 46))), 'Eight fixed matching defaults')
    for name, path in [('script', SCRIPT), ('modes', MODES), ('plan', PLAN)]:
        need(pin(path) == case[name], 'Exact acquired adapter and explicit child schedule')
    spec = importlib.util.spec_from_file_location('declared_matching_schedule', PLAN)
    plans = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plans)
    schedule = plans.schedule(case['component'])
    need(schedule == case['children'], 'Literal whole declared schedule')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components'][case['component']]
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Exact runtime manifest')
    manifest = json.loads(manifest_path.read_bytes())
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    work, scientific = output/'inputs', output/'scientific'
    entry = work/manifest['files'][selection['entrypoint']]['materialized_path']
    tools = case['external_environment']

    def check_environment():
        for row in [tools['compiler'], *tools['headers'], tools['library_target']]:
            path = Path(row['path'])
            need(path.is_absolute() and path.is_file() and not path.is_symlink() and pin(path) == row,
                 'Actual explicit external compiler/header/library bytes')
        alias = Path(tools['library_alias']['path'])
        need(alias.is_symlink() and os.readlink(alias) == tools['library_alias']['link']
             and str(alias.resolve()) == tools['library_target']['path'], 'Exact nauty linker alias')
        need(os.access(tools['compiler']['path'], os.X_OK), 'Executable compiler')

    check_environment()
    locations = dict(PY=sys.executable, P=str(entry.parent), S=str(work/'study'),
        O=str(scientific), CXX=tools['compiler']['path'], INCLUDE=tools['include'], LIBRARY=tools['library'])
    expected = configured(schedule, locations)
    calls, denied = [], []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 1048576, 'Bounded complete child identity report')
        (output/'native_processes.json').write_bytes(raw)

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
        need(active is None and len(calls) < len(expected), 'Only the finite original child list')
        row = expected[len(calls)]
        env = check_call(row, values, keywords, os.environ)
        active = dict(command=row['command'], env=env, row=row, observed=False)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Actual audited Popen occurred')
            if row['capture'] == 'bytes':
                need(type(result.stdout) is bytes and type(result.stderr) is bytes, 'Original byte capture')
                capture = output/'children'
                capture.mkdir(exist_ok=True)
                for suffix, raw in [('stdout', result.stdout), ('stderr', result.stderr)]:
                    need(len(raw) <= 1048576, 'Bounded negative/guard capture')
                    path = capture/(str(len(calls)-1)+'.'+suffix)
                    with path.open('xb') as stream:
                        stream.write(raw)
                    calls[-1][suffix] = pin(path)
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
            need(active is not None and not active['observed'] and len(calls) < len(expected)
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] == active['env'], 'Only the exact active original child')
            active['observed'] = True
            calls.append(dict(active['row']))
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
        raise RuntimeError('Private-read positive denial failed')
    need(denied == [str(forbidden)], 'Exactly one positive denial')
    sys.path[:] = [p for p in sys.path if p and not Path(p).absolute().is_relative_to('/Users/sasha/medusa')]
    sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
        '--component', case['component'], '--out', str(output), '--compiler', tools['compiler']['path'],
        '--nauty-include', tools['include'], '--nauty-library', tools['library'], '--full-check']
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    portable = json.loads((output/'portable_report.json').read_bytes())
    result_path = scientific/'report.json'
    result = json.loads(result_path.read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_MATCHING_COMPONENT'
         and portable['component'] == case['component'] and portable['original_report'] == [
             pin(result_path)[k] for k in ('bytes', 'sha256')]
         and portable['mathematical_main_unchanged'] is True
         and portable['recorded_target_mode'] is False
         and portable['historical_payloads_freshly_verified'] is False
         and portable['old_executable_used'] is False, 'Whole actual original report and scope')
    need(set(result) == set(case['expected_report']), 'Complete original report field set')

    def compare(actual, reference, path=()):
        if list(path) in case['timing_fields']:
            need(type(actual) in (float, int) and actual >= 0, 'Actual nonnegative timing')
            return
        if isinstance(reference, dict):
            need(type(actual) is dict and set(actual) == set(reference), 'Whole result object '+str(path))
            for key in reference:
                compare(actual[key], reference[key], (*path, key))
        elif isinstance(reference, list):
            need(type(actual) is list and len(actual) == len(reference), 'Whole result list '+str(path))
            for i, item in enumerate(reference):
                compare(actual[i], item, (*path, i))
        else:
            need(type(actual) is type(reference) and actual == reference, 'Exact expected report field '+str(path))

    compare(result, case['expected_report'])
    need(len(calls) == len(expected) and all(x['reaped'] for x in calls), 'Every declared actual child reaped')
    # The recorded numeric returncode replaces the schedule's textual field.
    for row, expected_row in zip(calls, expected):
        need((row['returncode'] == 0) == (expected_row['returncode'] == 'zero'), 'Exact declared return polarity')
        if row['capture'] == 'files':
            for name in ('stdout', 'stderr'):
                row[name] = pin(Path(row['directory'])/name)
            need(Path(row['stderr']['path']).stat().st_size == 0, 'Original closed-execution clean stderr')
    save_calls()
    check_environment()
    need(denied == [str(forbidden)], 'No parent scientific private fallback')
    record = dict(status='PASS_ISOLATED_PORTABLE_MATCHING_COMPONENT', component=case['component'],
        result=pin(result_path), portable_report=pin(output/'portable_report.json'),
        child_report=pin(output/'native_processes.json'), children=len(calls),
        private_open_positive_control=True, parent_scientific_private_open_attempts=0,
        original_main_and_run_closed_unchanged=True, all_original_controls_retained=True,
        historical_payloads_freshly_verified=False, whole_source_credit=0,
        report_semantics=case['report_semantics'], external_environment=tools,
        isolation='Python parent opens/commands audited. Audit does not survive exec; exact child Python/native/compiler sources and toolchain are trusted-reviewed, not OS file-sandboxed. The unchanged owner bounds and reaps the whole family.')
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=record['status'], component=case['component'])), flush=True)


if __name__ == '__main__':
    main()
