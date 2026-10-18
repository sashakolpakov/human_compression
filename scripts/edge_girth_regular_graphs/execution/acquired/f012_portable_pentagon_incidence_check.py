"""Replay atlas6 with its eight exact original compiler/native/Python calls."""
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
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/incidence_checks.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/incidence_check_modes.json'


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


NAMES = ('compile', 'edge_controls', 'census10', 'coverage10',
         'census12', 'coverage12', 'canonical_controls', 'positives')
TIMEOUTS = (60, 60, 180, 90, 180, 90, 60, 60)


def checked_call(index, values, keywords, entry, scientific, compiler, environment):
    need(type(index) is int and 0 <= index < 8, 'Only the eight original calls')
    here = entry.parent
    binary = scientific/'medial5'
    if index == 0:
        command = ['clang++', '-std=c++17', '-pedantic-errors', '-O2',
                   str(here/'medial5.cpp'), '-o', str(binary)]
    elif index == 1:
        command = [str(binary), '--controls']
    elif index in (2, 4):
        command = [str(binary)]
    elif index in (3, 5):
        n = 10 if index == 3 else 12
        command = [sys.executable, str(here/'base_cover5.py'),
                   str(here/('base'+str(n)+'.txt')), str(scientific/('coverage'+str(n)+'.json'))]
    elif index == 6:
        command = [sys.executable, str(here/'controls5.py'), str(scientific/'canonical_controls.json')]
    else:
        command = [sys.executable, str(here/'verify_medial5.py'),
            '--base10', str(here/'base10.txt'), '--base12', str(here/'base12.txt'),
            '--result10', str(scientific/'census10.stdout'), '--result12', str(scientific/'census12.stdout'),
            '--source', str(here/'source_match5.json'), '--output', str(scientific/'positive_report.json')]
    need(len(values) == 1 and type(values[0]) is list and values[0] == command,
         'Exact unchanged original argv and eight-call order')
    need(set(keywords) == {'input', 'capture_output', 'timeout', 'cwd'}
         and keywords['capture_output'] is True and keywords['cwd'] is None
         and type(keywords['timeout']) is int and keywords['timeout'] == TIMEOUTS[index],
         'Original byte capture, inherited environment/cwd and exact per-call timeout')
    if index in (2, 4):
        n = 10 if index == 2 else 12
        need(type(keywords['input']) is bytes
             and keywords['input'] == (here/('base'+str(n)+'.txt')).read_bytes(),
             'Exact complete original native stdin bytes')
    else:
        need(keywords['input'] is None, 'Original explicit empty input')
    need(not environment.get('PYTHONOPTIMIZE') and not environment.get('PYTHONPATH')
         and not environment.get('PYTHONHOME') and environment.get('PYTHONDONTWRITEBYTECODE') == '1',
         'Fixed ordinary interpreter environment inherited by Python children')
    need(shutil.which('clang++') == compiler['path'] and pin(compiler['path']) == compiler,
         'Inherited PATH resolves the exact explicit compiler; argv is unchanged')
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
                       'expected_reports', 'scope', 'report_semantics'}, 'Exact case fields')
    need(case['schema'] == 'F012_ISOLATED_PENTAGON_INCIDENCE_V1' and case['component'] == '6',
         'Only atlas6 complete pentagon-incidence classification')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Unchanged shared interface')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components']['6']
    need(selection['number'] == 6 and selection['entrypoint'] == 'components/pentagon_incidence/check.py'
         and selection['python_children'] == ['components/pentagon_incidence/base_cover5.py',
            'components/pentagon_incidence/controls5.py', 'components/pentagon_incidence/verify_medial5.py']
         and selection['optional_flags_exposed'] == [], 'Complete original default child scope')
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
        need(len(raw) <= 65536, 'Bounded eight-child observation')
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
        command = checked_call(len(calls), values, keywords, entry, scientific, compiler, os.environ)
        verify_materialized()
        active = dict(command=command, observed=False)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Actual original Popen occurred')
            need(type(result.stdout) is bytes and type(result.stderr) is bytes, 'Original byte capture')
            capture = output/'children'
            capture.mkdir(exist_ok=True)
            for suffix, raw in [('stdout', result.stdout), ('stderr', result.stderr)]:
                need(len(raw) <= 1048576, 'Bounded retained child capture')
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
            need(active is not None and not active['observed'] and len(calls) < 8
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] is None,
                 'Only exact original inherited-environment child')
            active['observed'] = True
            index = len(calls)
            role = 'compiler' if index == 0 else 'native' if index in (1, 2, 4) else 'python'
            calls.append(dict(command=list(values[1]), role=role, name=NAMES[index], timeout=TIMEOUTS[index]))
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
                '--component', '6', '--out', str(output), '--compiler', compiler['path'],
                '--compiler-sha256', compiler['sha256'], '--full-check']
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    portable = json.loads((output/'portable_report.json').read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_INCIDENCE_COMPONENT' and portable['component'] == '6'
         and portable['mathematical_ast_unchanged'] is True
         and portable['native_arguments_unchanged'] is True
         and portable['historical_native_binaries_used'] is False
         and portable['saved_output_acceptance_only'] is False
         and portable['optional_render'] is False and portable['optional_sanitize'] is False,
         'Whole unchanged incidence route completed with truthful scope')
    result_path = scientific/selection['result_relative']
    need([pin(result_path)['bytes'], pin(result_path)['sha256']] == portable['original_result'], 'Report binding')
    need(json.loads(result_path.read_bytes()) == case['expected'], 'Entire original report equality')
    need(len(calls) == 8 and all(c['reaped'] and c['returncode'] == 0 for c in calls),
         'All eight original children completed/reaped')
    for i, call in enumerate(calls):
        for suffix in ('stdout', 'stderr'):
            captured = Path(call[suffix]['path'])
            target = scientific/(NAMES[i]+'.'+suffix)
            need(pin(captured) == call[suffix] and captured.read_bytes() == target.read_bytes(),
                 'Exact original retained byte capture')
    for n in (10, 12):
        name = 'census'+str(n)+'.stdout'
        need((scientific/name).read_bytes() == (entry.parent/name).read_bytes(),
             'Both complete original native census byte streams reproduced')
    expected_reports = case['expected_reports']
    need(set(expected_reports) == {'coverage10.json', 'coverage12.json',
                                   'canonical_controls.json', 'positive_report.json'},
         'All four original child report files')
    for name, expected in expected_reports.items():
        value = json.loads((scientific/name).read_bytes())
        excluded = expected['excluded_fields']
        need(excluded == ([] if name == 'positive_report.json' else ['seconds']),
             'Only original measured elapsed fields vary')
        if excluded:
            need(type(value.get('seconds')) in (int, float) and 0 <= value['seconds'] <= 840,
                 'Actual bounded child elapsed time')
        normalized = {k:v for k,v in value.items() if k not in excluded}
        raw = (json.dumps(normalized, sort_keys=True, separators=(',', ':'))+'\n').encode()
        need(len(raw) == expected['bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'],
             'Whole original child report including every coverage row/positive array')
    verify_materialized()
    need(denied == [str(forbidden)] and pin(cp) == compiler,
         'No parent scientific private fallback; compiler bytes unchanged')
    record = dict(status='PASS_ISOLATED_PORTABLE_PENTAGON_INCIDENCE', component='6',
        result=pin(result_path), portable_report=pin(output/'portable_report.json'), children=calls,
        private_open_positive_control=True, parent_scientific_private_open_attempts=0,
        all_other_parent_children_and_network_denied=True, compiler=compiler,
        child_boundary='The parent audit does not survive exec. The exact native/Python sources and external compiler toolchain are trusted-reviewed, not OS file-sandboxed. Original Python children read declared adjacent inputs and outputs, use stdlib, and start no descendants; native reads stdin and writes stdout/stderr. The owner bounds and reaps the entire group.',
        actual_materialized_inputs=len(semantic), original_report_field_semantics=case['report_semantics'],
        scope=case['scope'], whole_source_credit=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2); stream.write('\n')
    print(json.dumps(dict(status=record['status'], component='6')), flush=True)



if __name__ == '__main__':
    main()
