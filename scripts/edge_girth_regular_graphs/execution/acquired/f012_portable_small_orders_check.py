"""Replay atlas7 with its one original finite Python child and all controls."""
import argparse
import hashlib
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
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/finite_checks_relocation.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/finite_check_modes.json'


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


def checked_call(index, values, keywords, entry, scientific, environment):
    need(index == 0, 'One original finite_small child only')
    command = [sys.executable, str(entry.parent/'finite_small.py'),
               '--input', str(entry.parent/'input'), '--out', str(scientific/'census')]
    need(len(values) == 1 and type(values[0]) is list and values[0] == command,
         'Exact original finite_small argv and order')
    need(set(keywords) == {'capture_output', 'text', 'timeout'}
         and keywords['capture_output'] is True and keywords['text'] is True
         and type(keywords['timeout']) is int and keywords['timeout'] == 240,
         'Original capture/text/240-second timeout and inherited environment')
    need(not environment.get('PYTHONOPTIMIZE') and not environment.get('PYTHONPATH')
         and not environment.get('PYTHONHOME') and environment.get('PYTHONDONTWRITEBYTECODE') == '1',
         'Ordinary fixed interpreter environment; inherited adapter disables bytecode')
    return command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed application')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'script', 'modes', 'component', 'expected',
                       'expected_census_files', 'scope', 'report_semantics'}, 'Exact case fields')
    need(case['schema'] == 'F012_ISOLATED_SMALL_ORDERS_V1' and case['component'] == '7',
         'Only atlas7 complete small-order classification')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Unchanged shared interface')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components']['7']
    need(selection['number'] == 7 and selection['entrypoint'] == 'components/small_orders/check.py'
         and selection['child_scope'] == 'One unchanged finite_small.py replay (240s original timeout), no compiler.',
         'Original finite classifier and complete declared input scope')
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Exact runtime manifest')
    manifest = json.loads(manifest_path.read_bytes())
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    scientific = output/'scientific'
    work = output/'inputs'
    entry = work/manifest['files'][selection['entrypoint']]['materialized_path']
    need(entry.is_relative_to(work) and '..' not in entry.parts, 'Exact materialized entry')
    semantic = [(work/manifest['files'][key]['materialized_path'], manifest['files'][key])
                for key in selection['inputs']]
    calls, denied = [], []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def verify_materialized():
        for path, row in semantic:
            actual = pin(path)
            need(not path.is_symlink() and all(actual[k] == row[k] for k in ('bytes', 'sha256')),
                 'Exact entire materialized scientific input roster')

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 65536, 'Bounded one-child observation')
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
        need(active is None, 'No nested process request')
        command = checked_call(len(calls), values, keywords, entry, scientific, os.environ)
        verify_materialized()
        active = dict(command=command, observed=False)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Actual original Popen occurred')
            need(type(result.stdout) is str and type(result.stderr) is str, 'Original text capture')
            capture = output/'children'
            capture.mkdir()
            for suffix, raw in [('stdout', result.stdout.encode()), ('stderr', result.stderr.encode())]:
                need(len(raw) <= 1048576, 'Bounded retained child capture')
                path = capture/('0.'+suffix)
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
            need(active is not None and not active['observed'] and not calls
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] is None,
                 'Only exact original inherited-environment child')
            active['observed'] = True
            calls.append(dict(command=list(values[1]), role='finite_small', timeout=240))
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
        raise RuntimeError('Private-read positive control failed')
    need(denied == [str(forbidden)], 'Exactly one positive denial')
    sys.path[:] = [p for p in sys.path if p and not Path(p).absolute().is_relative_to('/Users/sasha/medusa')]
    sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
                '--component', '7', '--out', str(output), '--full-check']
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    portable = json.loads((output/'portable_report.json').read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_FINITE_COMPONENT' and portable['component'] == '7',
         'Whole portable route completed')
    result_path = scientific/selection['result_relative']
    need([pin(result_path)['bytes'], pin(result_path)['sha256']] == portable['original_result'], 'Report binding')
    result = json.loads(result_path.read_bytes())
    need(type(result.get('seconds')) in (int, float) and 0 <= result['seconds'] <= 300, 'Actual bounded elapsed time')
    need({k:v for k,v in result.items() if k != 'seconds'} == case['expected'],
         'Whole original report; only measured seconds vary, render is unrequested')
    expected = case['expected_census_files']
    need(len(expected) == 16 and {p.name for p in (scientific/'census').iterdir()} == set(expected),
         'All15 original base certificates and whole census report')
    for name, row in expected.items():
        need(Path(name).name == name, 'Literal expected child filename')
        got = pin(scientific/'census'/name)
        need(all(got[k] == row[k] for k in ('bytes', 'sha256')), 'Exact deterministic original census bytes')
    need(len(calls) == 1 and calls[0]['reaped'] and calls[0]['returncode'] == 0, 'Original child completed/reaped')
    for suffix in ('stdout', 'stderr'):
        row = calls[0][suffix]
        path = Path(row['path'])
        need(pin(path) == row and path.read_bytes() == (scientific/suffix).read_bytes(), 'Exact original retained capture')
    verify_materialized()
    need(denied == [str(forbidden)], 'No parent scientific private fallback')
    record = dict(status='PASS_ISOLATED_PORTABLE_SMALL_ORDERS', component='7',
        result=pin(result_path), portable_report=pin(output/'portable_report.json'), children=calls,
        private_open_positive_control=True, parent_scientific_private_open_attempts=0,
        all_other_parent_children_and_network_denied=True,
        child_boundary='The parent audit does not survive exec. The exact unchanged child and adjacent source are trusted-reviewed: only declared input and output paths, stdlib imports, no process/network call. This is not an OS file sandbox.',
        actual_materialized_inputs=len(semantic), original_report_field_semantics=case['report_semantics'],
        scope=case['scope'], whole_source_credit=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2); stream.write('\n')
    print(json.dumps(dict(status=record['status'], component='7')), flush=True)


if __name__ == '__main__':
    main()
