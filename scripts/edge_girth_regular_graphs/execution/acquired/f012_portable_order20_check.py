"""Run the unchanged order20 route with its exact six original child calls."""
import argparse
import ast
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
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/certificate_checks.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/tree_certificate_modes.json'


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


def guard_source(raw, source_sha):
    """Parse the actual unchanged child; do not replace or simulate its guard."""
    need(hashlib.sha256(raw).hexdigest() == source_sha, 'Exact original child source')
    prefix = ast.parse("import argparse\nimport hashlib\nimport itertools\nimport json\n"
                       "import os\nfrom pathlib import Path\nimport shutil\nimport subprocess\nimport sys\n"
                       "if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):\n"
                       "    raise RuntimeError('Optimized Python is not accepted')\n").body
    body = ast.parse(raw).body
    need([ast.dump(n) for n in body[:len(prefix)]] == [ast.dump(n) for n in prefix],
         'Exact early guard before NetworkX, scientific input reads and argument parsing')


def child_plan(index, entry, scientific, compiler):
    need(type(index) is int and 0 <= index < 6, 'Only the six original calls')
    if index < 4:
        mode = 'ordinary' if index < 2 else 'sanitized'
        binary = scientific/mode
        if index % 2 == 0:
            flags = ['-O2'] if mode == 'ordinary' else [
                '-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
            command = [compiler, '-std=c++17', '-Wall', '-Wextra', '-pedantic',
                       *flags, str(entry.parent/'root20.cpp'), '-o', str(binary)]
            role, timeout = 'compiler', 30
        else:
            command, role, timeout = [str(binary)], 'native', 50
        return dict(command=command, role=role, name=mode, timeout=timeout)
    name = 'argument' if index == 4 else 'environment'
    command = [sys.executable] + (['-O'] if index == 4 else []) + [str(entry)]
    return dict(command=command, role='optimization', name=name, timeout=5)


def checked_call(index, values, keywords, entry, scientific, compiler, environment):
    """Pure call-policy check. Original subprocess.run executes after this check."""
    plan = child_plan(index, entry, scientific, compiler)
    env = dict(environment)
    need(not env.get('PYTHONOPTIMIZE'), 'Ordinary parent environment')
    env['ASAN_OPTIONS'] = 'detect_leaks=0:halt_on_error=1'
    env['UBSAN_OPTIONS'] = 'halt_on_error=1'
    if index == 5:
        env['PYTHONOPTIMIZE'] = '1'
    need(len(values) == 1 and type(values[0]) is list and values[0] == plan['command'],
         'Exact original configured argv and call order')
    need(set(keywords) == {'capture_output', 'text', 'env', 'timeout'}
         and keywords['capture_output'] is True and keywords['text'] is True
         and type(keywords['env']) is dict and keywords['env'] == env
         and type(keywords['timeout']) is int and keywords['timeout'] == plan['timeout'],
         'Original capture, environment and per-call timeout unchanged')
    return plan, env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed application')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'script', 'modes', 'component', 'compiler',
                       'expected', 'scope', 'report_semantics'}, 'Exact application schema')
    need(case['schema'] == 'F012_ISOLATED_ORDER20_NATIVE_V1' and case['component'] == '26',
         'Only the original quartic girth-five order20 route')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Unchanged shared interface')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components']['26']
    need(selection['number'] == 26 and selection['kind'] == 'unchanged_native'
         and not selection.get('omitted_main_statements'), 'All original mathematical statements retained')
    compiler = case['compiler']
    cp = Path(compiler['path'])
    need(cp.is_absolute() and cp.is_file() and not cp.is_symlink() and os.access(cp, os.X_OK)
         and pin(cp) == compiler, 'Exact explicit external compiler')
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Runtime manifest identity')
    manifest = json.loads(manifest_path.read_bytes())
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    scientific = output/'scientific'
    entry = output/'inputs'/manifest['files'][selection['entrypoint']]['materialized_path']
    need(entry.is_relative_to(output/'inputs') and '..' not in entry.parts, 'Exact materialized entry')
    cpp_key = 'components/quartic_girth_five/root20.cpp'
    cpp_info = manifest['files'][cpp_key]
    need(selection['source_build']['sources'] == [cpp_key]
         and selection['source_build']['local_headers'] == []
         and cpp_key in selection['inputs']
         and output/'inputs'/cpp_info['materialized_path'] == entry.parent/'root20.cpp',
         'Exact compiled source and no undeclared local headers')
    calls, denied = [], []
    active = None
    original_run, original_popen = subprocess.run, subprocess.Popen

    def save_calls():
        raw = (json.dumps(calls, indent=2)+'\n').encode()
        need(len(raw) <= 65536, 'Bounded child identity report')
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
        need(active is None, 'No nested Python process request')
        plan, env = checked_call(len(calls), values, keywords, entry, scientific,
                                 compiler['path'], os.environ)
        guard_source(entry.read_bytes(), selection['source_sha256'])
        cpp = pin(entry.parent/'root20.cpp')
        need(all(cpp[k] == cpp_info[k] for k in ('bytes', 'sha256')), 'Unchanged native source')
        active = dict(command=plan['command'], env=env, observed=False, plan=plan)
        try:
            result = original_run(*values, **keywords)
            need(active['observed'], 'Actual audited Popen occurred')
            need(type(result.stdout) is str and type(result.stderr) is str, 'Original text capture')
            capture = output/'children'
            capture.mkdir(exist_ok=True)
            stem = str(len(calls)-1)
            for suffix, raw in [('stdout', result.stdout.encode()), ('stderr', result.stderr.encode())]:
                need(len(raw) <= 1048576, 'Bounded retained child capture')
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
            need(active is not None and not active['observed'] and len(calls) < 6
                 and values[0] == active['command'][0] and list(values[1]) == active['command']
                 and values[2] is None and values[3] == active['env'],
                 'Only the exact active original subprocess.run call')
            active['observed'] = True
            calls.append(dict(command=list(values[1]), role=active['plan']['role'],
                              name=active['plan']['name'], timeout=active['plan']['timeout']))
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
                '--component', '26', '--out', str(output), '--compiler', compiler['path'],
                '--compiler-sha256', compiler['sha256'], '--full-check']
    subprocess.run, subprocess.Popen = exact_run, RecordedPopen
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.run, subprocess.Popen = original_run, original_popen
    portable = json.loads((output/'portable_report.json').read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_CERTIFICATE_COMPONENT'
         and portable['component'] == '26' and portable['kind'] == 'unchanged_native'
         and portable['ordinary_sanitized_replayed'] is True
         and portable['historical_binary_used'] is False
         and portable['historical_payloads_freshly_verified'] is False
         and portable['saved_tree_predicates_unchanged'] is False and portable['render'] is False,
         'Exact native scientific scope')
    result_path = scientific/selection['result_relative']
    need([pin(result_path)['bytes'], pin(result_path)['sha256']] == portable['scientific_result'],
         'Whole actual report binding')
    need(json.loads(result_path.read_bytes()) == case['expected'], 'Whole original expected report')
    need(len(calls) == 6 and all(c['reaped'] for c in calls)
         and all(c['returncode'] == 0 for c in calls[:4])
         and all(c['returncode'] != 0 for c in calls[4:]), 'All six actual calls returned and reaped')
    compiled = portable['compiler_commands']
    need(len(compiled) == 2, 'Both original builds observed')
    for row, index in zip(compiled, (0, 2)):
        configured = child_plan(index, entry, scientific, compiler['path'])['command']
        need(row == dict(original=['clang++', *configured[1:]], configured=configured),
             'Only original compiler argv[0] substituted')
    for i, call in enumerate(calls):
        for suffix in ('stdout', 'stderr'):
            captured = Path(call[suffix]['path'])
            need(pin(captured) == call[suffix], 'Retained actual capture unchanged')
            if i < 4:
                stem = ('compile_' if i % 2 == 0 else '') + call['name']
                need((scientific/(stem+'.'+suffix)).read_bytes() == captured.read_bytes(),
                     'Original native capture equals actual child capture')
            elif suffix == 'stderr':
                need(b'Optimized Python is not accepted' in captured.read_bytes()
                     and (scientific/('guard_'+call['name']+'.stderr')).read_bytes() == captured.read_bytes(),
                     'Original actual optimization rejection retained')
    need(denied == [str(forbidden)] and pin(cp) == compiler,
         'No scientific private fallback; external compiler unchanged')
    record = dict(status='PASS_ISOLATED_PORTABLE_ORDER20_NATIVE', component='26',
        result=pin(result_path), portable_report=pin(output/'portable_report.json'),
        private_open_positive_control=True, scientific_private_open_attempts=0,
        children=calls, compiler=compiler, actually_materialized_inputs=portable['runtime_inputs'],
        actual_authentication=portable['authentication'], whole_source_credit=0,
        scope=case['scope'], original_report_field_semantics=case['report_semantics'],
        isolation='Python study opens/direct commands are checked. Compiler toolchain descendants and native code are trusted-reviewed, not OS file-sandboxed; inherited owner bounds and reaps the entire group.',
        guard_boundary='Parent audit does not survive exec; exact original guard precedes NetworkX and all scientific reads.')
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=record['status'], component='26')), flush=True)


if __name__ == '__main__':
    main()
