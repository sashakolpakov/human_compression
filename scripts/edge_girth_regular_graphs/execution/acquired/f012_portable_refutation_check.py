"""Run one packaged refutation with exact native commands and private opens denied."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import psutil

if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
STUDY = Path('/Users/sasha/medusa/research/leemans')
PACKAGE = STUDY/'computation/f012/source_synthesis/package'
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/saved_refutations.py'
CASES = PACKAGE/'data/edge_girth_regular_graphs/saved_refutation_cases.json'


def need(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(2**20), b''):
            digest.update(block)
    return dict(path=str(path), bytes=path.stat().st_size, sha256=digest.hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, required=True)
    parser.add_argument('--case-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256, 'Exact reviewed application')
    application = json.loads(args.case.read_bytes())
    need(set(application) == {'schema', 'selection', 'script', 'cases', 'compiler'},
         'Complete application schema')
    need(application['schema'] == 'F012_ISOLATED_SAVED_REFUTATION_V1', 'Application version')
    need(pin(SCRIPT) == application['script'] and pin(CASES) == application['cases'],
         'Exact prepared portable interface')
    compiler = application['compiler']
    need(Path(compiler['path']).is_absolute() and pin(compiler['path']) == compiler,
         'Actual configured external compiler')
    program = json.loads(CASES.read_bytes())
    manifest_path = PACKAGE/program['runtime_manifest']
    need(pin(manifest_path)['sha256'] == program['runtime_manifest_sha256'],
         'Exact runtime manifest')
    manifest = json.loads(manifest_path.read_bytes())
    case = program['cases'][application['selection']]
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    work = output/'inputs'
    entries = manifest['files']
    aliases = {alias: key for key, entry in entries.items() for alias in entry['aliases']}

    def materialized(key):
        need(key in case['inputs'], 'Closed selected source/data roster')
        return str(work/entries[key]['materialized_path'])

    recipe = manifest['build_recipes'][case['build_recipe']]
    compile_command = [compiler['path']]
    for item in recipe['arguments']:
        if isinstance(item, str):
            compile_command.append(item)
        elif set(item) == {'input'}:
            compile_command.append(materialized(item['input']))
        else:
            need(item == {'output': True}, 'Exact build output marker')
            compile_command.append(str(output/'fresh_rup_checker'))
    check_command = [str(output/'fresh_rup_checker'),
                     materialized(aliases[case['formula']['path']]),
                     materialized(aliases[case['proof']['path']])]
    commands = [compile_command, check_command]
    calls, denied = [], []

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (
                    path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study access denied')
        if event == 'subprocess.Popen':
            index = len(calls)
            need(index < 2 and values[0] == commands[index][0]
                 and list(values[1]) == commands[index] and values[2] is None,
                 'Only the exact compiler and fresh checker commands')
            calls.append(dict(command=list(values[1]), role=('compiler', 'checker')[index]))
        if event in ('os.system', 'os.exec', 'os.fork', 'os.forkpty', 'os.posix_spawn'):
            raise PermissionError('Undeclared process interface')
        if event.startswith('socket.'):
            raise PermissionError('Network forbidden')

    sys.addaudithook(audit)
    forbidden = STUDY/'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError('Private-open positive control failed')
    need(denied == [str(forbidden)], 'Exact positive denial')
    original_popen = subprocess.Popen

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
                self.save()
            except BaseException:
                # Popen's context manager has not yet been entered. A failed
                # identity query or write must not strand the spawned child.
                try:
                    if self.poll() is None:
                        self.kill()
                finally:
                    self.wait(timeout=2)
                raise

        def save(self):
            (output/'native_processes.json').write_text(json.dumps(calls, indent=2)+'\n')

        def __exit__(self, *values):
            try:
                return super().__exit__(*values)
            finally:
                self.record.update(returncode=self.returncode, reaped=self.returncode is not None)
                self.save()

    subprocess.Popen = RecordedPopen
    sys.path[:] = [p for p in sys.path if p and not Path(p).absolute().is_relative_to('/Users/sasha/medusa')]
    sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--cases-sha256', application['cases']['sha256'],
                '--case', application['selection'], '--check', '--compiler', compiler['path'],
                '--out', str(output)]
    try:
        runpy.run_path(str(SCRIPT), run_name='__main__')
    finally:
        subprocess.Popen = original_popen
    result = json.loads((output/'result.json').read_bytes())
    need(result['status'] == 'CHECKED_PORTABLE_EXACT_DOMAIN_REFUTATION'
         and result['exact_dimacs_equal'] and result['solver_calls'] == 0
         and result['proof_production_calls'] == 0, 'Actual saved refutation passed')
    need(len(calls) == 2 and all(x['reaped'] and x['returncode'] == 0 for x in calls),
         'Both declared native commands completed')
    need(denied == [str(forbidden)] and pin(compiler['path']) == compiler,
         'No scientific private fallback and unchanged external compiler')
    report = dict(status='PASS_ISOLATED_PORTABLE_SAVED_REFUTATION', selection=application['selection'],
                  private_open_positive_control=True, scientific_private_open_attempts=0,
                  native_commands=calls, compiler=compiler,
                  isolation_scope='Python study-file opens and direct commands checked; native source is reviewed, not OS file-sandboxed.',
                  source_credit=0, whole_source_credit=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=report['status'], selection=application['selection'])), flush=True)


if __name__ == '__main__':
    main()
