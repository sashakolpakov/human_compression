"""Replay atlas 19 with all 18 original text-mode compiler/native calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
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
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/native_checks.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/native_check_modes.json'


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


NAMES = ('compile_ordinary', 'compile_sanitized') + tuple(
    'order'+str(n)+'_'+mode for n in range(15, 21) for mode in ('ordinary', 'sanitized')) + (
    'unsupported_order', 'bad_class', 'negative_cap', 'timeout_control')


def normalized_rows(text):
    rows = [json.loads(line) for line in text.splitlines()]
    for row in rows:
        need(type(row.get('seconds')) in (int, float) and 0 <= row['seconds'] <= 60,
             'Original measured native time is bounded')
    return [{k:v for k,v in row.items() if k != 'seconds'} for row in rows]


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def checked_call(index, values, keywords, entry, scientific, compiler, environment, expected_inputs):
    need(type(index) is int and 0 <= index < 18, 'Only the 18 original calls')
    if index < 2:
        mode = ('ordinary', 'sanitized')[index]
        flags = ['-O2'] if index == 0 else ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
        command = ['clang++', '-std=c++17', *flags, '-Wall', '-Wextra', '-pedantic',
                   str(entry.parent/'cycle_search_positive.cpp'), '-o', str(scientific/mode)]
        expected_input = None
    else:
        mode = ('ordinary', 'sanitized')[(index-2)%2] if index < 14 else 'ordinary'
        command = [str(scientific/mode)]
        n = 15+(index-2)//2 if index < 14 else 20
        raw = (scientific/('order'+str(n)+'.input')).read_bytes()
        expected = expected_inputs[str(n)]
        need(len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'],
             'Whole freshly generated inventory equals the acquired literal input')
        expected_input = raw.decode('ascii')
        if 14 <= index < 17:
            row = expected_input.splitlines()[0].split()
            position, value = ((1, '22'), (7, '0'), (18, '-1'))[index-14]
            row[position] = value
            expected_input = ' '.join(row)+'\n'
        elif index == 17:
            rows = [json.loads(line) for line in (scientific/'order20_ordinary.stdout').read_text().splitlines()]
            hard = max(rows, key=lambda row: row['nodes'])['case']
            lines = expected_input.splitlines()
            need(type(hard) is int and 0 <= hard < len(lines), 'Actual maximum-node case index')
            row = lines[hard].split()
            need(int(row[0]) == hard, 'Original ordered case identity')
            row[-1] = str(0.000000001)
            expected_input = ' '.join(row)+'\n'
    need(len(values) == 1 and type(values[0]) is list and values[0] == command,
         'Exact original compiler/native argv and 18-call order')
    need(set(keywords) == {'input', 'text', 'capture_output', 'timeout'}
         and keywords['text'] is True and keywords['capture_output'] is True
         and type(keywords['timeout']) is int and keywords['timeout'] == 60,
         'Original text capture and 60-second timeout; no cwd or environment override')
    need(keywords['input'] == expected_input
         and (keywords['input'] is None if index < 2 else type(keywords['input']) is str),
         'Exact original compiler None or native string input')
    need(not environment.get('PYTHONOPTIMIZE') and not environment.get('PYTHONPATH')
         and not environment.get('PYTHONHOME') and environment.get('PYTHONDONTWRITEBYTECODE') == '1',
         'Fixed ordinary Python environment')
    need(shutil.which('clang++') == compiler['path'] and pin(compiler['path']) == compiler,
         'Inherited PATH selects the exact external compiler')
    return command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed application')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'script', 'modes', 'component', 'compiler', 'expected',
                       'expected_inputs', 'expected_calls', 'expected_source_report', 'scope', 'report_semantics'}, 'Exact case fields')
    need(case['schema'] == 'F012_ISOLATED_NATIVE_ATLAS19_V1' and case['component'] == '19',
         'Only atlas 19 complete original order-20 classification')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Unchanged shared interface')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components']['19']
    need(selection['number'] == 19 and selection['entrypoint'] == 'components/order20/check_order20.py'
         and selection['authentication_sites'] == [] and selection['authentication_tables'] == {}
         and selection['authentication_identity_only'] == {}, 'Original source with no removed authentication body')
    need(set(case['expected_inputs']) == {str(n) for n in range(15, 21)}
         and [r['name'] for r in case['expected_calls']] == list(NAMES), 'Full six inventories and 18 calls')
    compiler = case['compiler']
    cp = Path(compiler['path'])
    need(cp.is_absolute() and cp.name == 'clang++' and cp.is_file() and not cp.is_symlink()
         and os.access(cp, os.X_OK) and pin(cp) == compiler, 'Exact external regular compiler')
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
        need(len(raw) <= 65536, 'Bounded 18-child observation')
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
        command = checked_call(len(calls), values, keywords, entry, scientific, compiler, os.environ, case['expected_inputs'])
        verify_materialized()
        active = dict(command=command, observed=False)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Actual original Popen occurred')
            need(type(result.stdout) is str and type(result.stderr) is str, 'Original text=True capture')
            capture = output/'children'
            capture.mkdir(exist_ok=True)
            streams = [('stdout', result.stdout), ('stderr', result.stderr)]
            if keywords['input'] is not None:
                streams.append(('stdin', keywords['input']))
            for suffix, captured_text in streams:
                raw = captured_text.encode('utf-8')
                need(len(raw) <= 1048576, 'Bounded UTF-8 representation of actual text capture/input')
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
            need(active is not None and not active['observed'] and len(calls) < 18
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] is None,
                 'Only exact original inherited-environment child')
            active['observed'] = True
            index = len(calls)
            role = 'compiler' if index < 2 else 'native'
            calls.append(dict(command=list(values[1]), role=role, name=NAMES[index], timeout=60,
                              text_capture=True, observation_encoding='utf-8'))
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
                '--component', '19', '--out', str(output), '--compiler', compiler['path'],
                '--compiler-sha256', compiler['sha256'], '--full-check']
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    portable = json.loads((output/'portable_report.json').read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_NATIVE_COMPONENT' and portable['component'] == '19'
         and portable['original_scientific_ast_unchanged'] is True
         and portable['native_arguments_unchanged'] is True
         and portable['historical_native_binaries_used'] is False
         and portable['saved_output_acceptance_only'] is False and portable['render'] is False,
         'Full unchanged native route completed')
    result_path = scientific/selection['result_relative']
    need([pin(result_path)['bytes'], pin(result_path)['sha256']] == portable['original_result'], 'Report binding')
    need(json.loads(result_path.read_bytes()) == case['expected'], 'Entire original report equality')
    need(len(calls) == 18 and all(c['reaped'] for c in calls), 'All original children completed and reaped')
    receipts = json.loads((scientific/'receipts.json').read_bytes())
    need(len(receipts) == 18, 'Every original child receipt retained')
    for i, (call, expected, receipt) in enumerate(zip(calls, case['expected_calls'], receipts)):
        need(call['returncode'] == expected['returncode'] == receipt['returncode']
             and receipt['label'] == NAMES[i] and receipt['command'] == call['command']
             and type(receipt['seconds']) in (int, float) and 0 <= receipt['seconds'] <= 1140,
             'Exact original receipt identity and expected return status')
        for suffix in ('stdout', 'stderr'):
            captured = Path(call[suffix]['path'])
            target = scientific/(NAMES[i]+'.'+suffix)
            need(pin(captured) == call[suffix] and captured.read_bytes() == target.read_text().encode('utf-8'),
                 'Complete actual text captures equal original retained text')
        text = (scientific/(NAMES[i]+'.stdout')).read_text()
        value = normalized_rows(text) if expected['stdout_kind'] == 'native_json_lines' else text
        raw = canonical(value)
        need(len(raw) == expected['stdout']['bytes'] and hashlib.sha256(raw).hexdigest() == expected['stdout']['sha256'],
             'Whole expected stdout; only original native measured seconds excluded')
        need((scientific/(NAMES[i]+'.stderr')).read_text() == expected['stderr'], 'Exact original diagnostic text')
    value = json.loads((scientific/'source_report.json').read_bytes())
    raw = canonical(value)
    need(len(raw) == case['expected_source_report']['bytes']
         and hashlib.sha256(raw).hexdigest() == case['expected_source_report']['sha256'],
         'All seven complete source invariant records')
    verify_materialized()
    need(denied == [str(forbidden)] and pin(cp) == compiler,
         'No parent scientific private fallback; compiler bytes unchanged')
    record = dict(status='PASS_ISOLATED_PORTABLE_NATIVE_ATLAS19', component='19',
        result=pin(result_path), portable_report=pin(output/'portable_report.json'), children=calls,
        private_open_positive_control=True, parent_scientific_private_open_attempts=0,
        all_other_parent_children_and_network_denied=True, compiler=compiler,
        child_boundary='The parent audit does not survive exec. The exact source-built native programs read stdin and write stdout/stderr; they and the external compiler/headers/SDK/sanitizer runtimes are trusted-reviewed, not OS file-sandboxed. No original Python child or native descendant is declared. The owner bounds and reaps the group.',
        capture_semantics='Original text=True CompletedProcess is returned unchanged. Observation files encode its actual Unicode text and stdin as UTF-8; these are not claimed as raw pipe bytes.',
        actual_materialized_inputs=len(semantic), original_report_field_semantics=case['report_semantics'],
        scope=case['scope'], whole_source_credit=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2); stream.write('\n')
    print(json.dumps(dict(status=record['status'], component='19')), flush=True)



if __name__ == '__main__':
    main()
