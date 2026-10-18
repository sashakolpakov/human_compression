"""Run the unchanged positive-witness checker with its two exact recorded children."""
import argparse
import gzip
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
PREPARER = PACKAGE/'scripts/edge_girth_regular_graphs/prepare_check.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/execution_modes.json'


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed application case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'mode', 'preparer', 'modes', 'entrypoint', 'compiler',
                       'expected', 'stdin_bytes', 'scope'}, 'Complete positive-check case')
    need(case['schema'] == 'F012_ISOLATED_POSITIVE_CHECK_V1' and case['mode'] == 'positive_graphs',
         'Only the complete original positive checker')
    need(pin(PREPARER) == case['preparer'] and pin(MODES) == case['modes'],
         'Exact acquired preparer and modes')
    modes = json.loads(MODES.read_bytes())
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Exact runtime declaration')
    manifest = json.loads(manifest_path.read_bytes())
    mode = modes['modes'][case['mode']]
    need(mode['configured_compiler'] and mode['python_environment'] == 'isolated'
         and len(mode['commands']) == 1 and len(mode['inputs']) == 18
         and mode['commands'][0]['entrypoint'] == case['entrypoint'] == 'components/positive/check.py',
         'One exact compiler-using positive entrypoint and complete input roster')
    compiler = case['compiler']
    cp = Path(compiler['path'])
    need(cp.is_absolute() and cp.name == 'clang++' and cp.is_file() and not cp.is_symlink()
         and os.access(cp, os.X_OK) and pin(cp) == compiler, 'Exact external compiler bytes')
    need(case['stdin_bytes'] == 16592658, 'Exact original positive input length')
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    work = output/'inputs'
    scientific = output/'scientific'
    entry = work/manifest['files'][case['entrypoint']]['materialized_path']
    semantic = [(work/manifest['files'][key]['materialized_path'], manifest['files'][key])
                for key in mode['inputs']]
    calls, denied = [], []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def verify_materialized():
        for path, row in semantic:
            need(path.is_relative_to(work) and not path.is_symlink()
                 and all(pin(path)[k] == row[k] for k in ('bytes', 'sha256')),
                 'Complete exact materialized input bytes')

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 65536, 'Bounded two-child observation')
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
        index = len(calls)
        need(active is None and index in (0, 1), 'Only the two original nonnested calls')
        exe = scientific/'verify_egr_witnesses'
        command = ([compiler['path'], '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic',
                    str(entry.parent/'verify_egr_witnesses.cpp'), '-o', str(exe)]
                   if index == 0 else [str(exe)])
        fields = {'capture_output', 'text', 'timeout'} | ({'input'} if index == 1 else set())
        need(len(values) == 1 and type(values[0]) is list and values[0] == command
             and set(keywords) == fields and keywords['capture_output'] is True
             and keywords['text'] is True and type(keywords['timeout']) is int
             and keywords['timeout'] == (60, 120)[index],
             'Exact original argv, text capture, inherited cwd/env, stdin policy and timeout')
        verify_materialized()
        need(pin(cp) == compiler, 'Compiler remains unchanged')
        if index == 1:
            need(type(keywords['input']) is str and len(keywords['input'].encode('utf-8')) == case['stdin_bytes']
                 and keywords['input'].encode('utf-8') == gzip.decompress((entry.parent/'witnesses.input.gz').read_bytes()),
                 'Whole actual native stdin equals the exact materialized compressed input')
        active = dict(command=command, observed=False)
        try:
            returned = original_run(*values, **keywords)
            need(active['observed'], 'Actual original Popen occurred')
            need(type(returned.stdout) is str and type(returned.stderr) is str, 'Original text=True returns')
            capture = output/'children'
            capture.mkdir(exist_ok=True)
            streams = [('stdout', returned.stdout), ('stderr', returned.stderr)]
            if index == 1:
                streams.append(('stdin', keywords['input']))
            for suffix, text in streams:
                raw = text.encode('utf-8')
                need(len(raw) <= 32*2**20, 'Bounded exact UTF-8 text capture')
                p = capture/(str(index)+'.'+suffix)
                with p.open('xb') as stream:
                    stream.write(raw)
                calls[-1][suffix] = pin(p)
            save_calls()
            return returned
        finally:
            active = None

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            p = Path(os.path.abspath(os.fsdecode(values[0])))
            if p.is_relative_to(STUDY) and not (p.is_relative_to(PACKAGE) or p.is_relative_to(output)):
                denied.append(str(p))
                raise PermissionError('Private study access denied')
        if event == 'subprocess.Popen':
            need(active is not None and not active['observed'] and len(calls) < 2
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] is None,
                 'Only the two exact original children with inherited cwd and environment')
            active['observed'] = True
            calls.append(dict(command=list(values[1]), cwd=None, env=None, text=True,
                              role=('compile', 'positive')[len(calls)], timeout=(60, 120)[len(calls)]))
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
        raise AssertionError('Private-open positive control failed')
    need(denied == [str(forbidden)], 'Exact positive denial')
    sys.path[:] = [x for x in sys.path if x and not Path(x).absolute().is_relative_to('/Users/sasha/medusa')]
    output.mkdir()
    sys.argv = [str(PREPARER), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
                '--mode', case['mode'], '--work', str(work), '--check-output', str(scientific),
                '--compiler', compiler['path']]
    runpy.run_path(str(PREPARER), run_name='__main__')
    prepared = json.loads((work/'checker_commands.json').read_bytes())
    command = [sys.executable, '-I', '-B', str(entry), '--out', str(scientific), '--compiler', compiler['path']]
    need(prepared['status'] == 'EXACT_CHECKER_INPUTS_PREPARED_NO_SCIENTIFIC_EXECUTION'
         and prepared['mode'] == case['mode'] and prepared['commands'] == [command]
         and prepared['materialization']['files'] == mode['inputs'], 'Exact original prepared command and full roster')
    verify_materialized()
    before = [pin(p) for p, _ in semantic]
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        sys.argv = command[3:]
        runpy.run_path(str(entry), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    need(len(calls) == 2 and all(c.get('reaped') and c.get('returncode') == 0 for c in calls),
         'Both complete original child returns')
    for index, stem in enumerate(('compile', 'positive')):
        for suffix in ('stdout', 'stderr'):
            need((scientific/(stem+'.'+suffix)).read_bytes() == Path(calls[index][suffix]['path']).read_bytes(),
                 'Complete original and recorded capture equality')
    result_path = scientific/'report.json'
    actual = json.loads(result_path.read_bytes())
    need(actual == case['expected'], 'Whole original report equality without normalization')
    verify_materialized()
    need(before == [pin(p) for p, _ in semantic] and denied == [str(forbidden)],
         'Source preservation and no scientific private reads')
    report = dict(status='PASS_ISOLATED_PORTABLE_POSITIVE_COMPONENT', component=1, case=case,
                  source_inputs=before, result=pin(result_path), finite_processes=pin(output/'finite_processes.json'),
                  private_open_positive_control=True, scientific_private_open_attempts=0,
                  exact_children_and_network_denial=True, actual_children=2,
                  whole_original_report_equal=True, scientific_source_unchanged=True,
                  scope=case['scope'], source_credit=0, whole_source_credit=0,
                  qualification='Parent Python audit only; it does not survive exec. Compiler/toolchain and unchanged native verifier remain explicit software premises. Text captures are UTF-8 encodings, not raw pipe bytes.')
    with (output/'isolation.json').open('x') as stream:
        json.dump(report, stream, indent=2); stream.write('\n')
    print(json.dumps(dict(status=report['status'], component=1)), flush=True)


if __name__ == '__main__':
    main()
