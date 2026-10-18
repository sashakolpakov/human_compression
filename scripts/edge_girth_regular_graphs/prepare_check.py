"""Materialize one declared checker input set and print commands; execute none."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

RUNTIME_SHA256 = 'e76919bf176912ac7b655a01fd3c4bc051ebb2c1d14db7a94a09658207ff5799'
runtime_path = Path(__file__).with_name('runtime.py')
if runtime_path.is_symlink() or hashlib.sha256(runtime_path.read_bytes()).hexdigest() != RUNTIME_SHA256:
    raise ValueError('Exact acquired transport source')
runtime_spec = importlib.util.spec_from_file_location('f012_declared_transport', runtime_path)
runtime_module = importlib.util.module_from_spec(runtime_spec)
runtime_spec.loader.exec_module(runtime_module)
Runtime, need, regular = runtime_module.Runtime, runtime_module.need, runtime_module.regular


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--modes-sha256', required=True)
    parser.add_argument('--mode', required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--check-output', type=Path, required=True)
    parser.add_argument('--compiler', type=Path)
    args = parser.parse_args()
    raw = regular(args.root, 'data/edge_girth_regular_graphs/execution_modes.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.modes_sha256, 'External mode manifest identity')
    modes = json.loads(raw)
    need(modes['schema'] == 'F012_DECLARED_CHECKER_PREPARATION_MODES_V1', 'Mode schema')
    runtime = Runtime(args.root, modes['runtime_manifest'], modes['runtime_manifest_sha256'])
    mode = modes['modes'][args.mode]
    need(mode['status'] == 'SOURCE_REVIEWED_COMMAND_PREPARED_NOT_REPLAYED', 'Explicit preparation status')
    keys = mode['inputs']
    need(type(keys) is list and keys and len(keys) == len(set(keys)), 'Distinct exact logical inputs')
    need(all(key in runtime.files for key in keys), 'No alias or private input in mode roster')
    auth = mode['authentication_only']
    need(type(auth) is list and len(auth) == len(set(auth)) and set(auth) <= set(keys),
         'Explicit authentication-only subroster')
    for key in keys:
        item = runtime.files[key]
        need(item['role'] != 'provenance_only', 'Old native identities cannot be materialized for execution')
        need(item['role'] != 'unresolved_preserved' or key in auth,
             'Every historical unresolved input needs explicit authentication-only classification')
    work = args.work.absolute()
    result = args.check_output.absolute()
    need(not result.exists() and not result.is_symlink(), 'Fresh checker output')
    if mode['configured_compiler']:
        need(args.compiler is not None and args.compiler.is_absolute(), 'Explicit configured compiler')
    else:
        need(args.compiler is None, 'No compiler for pure Python mode')
    materialized = runtime.materialize(keys, work, allow_unresolved=True)
    need(not result.exists() and not result.is_symlink(), 'Checker output cannot replace a materialized input')
    commands = []
    for declaration in mode['commands']:
        need(declaration['entrypoint'] in keys and runtime.files[declaration['entrypoint']]['role'] == 'source',
             'Exact authenticated Python entrypoint')
        need(mode['python_environment'] in ('isolated', 'ignore_environment_with_exact_local_imports'),
             'Explicit Python import boundary')
        isolation = '-I' if mode['python_environment'] == 'isolated' else '-E'
        command = [sys.executable, isolation, '-B', str(runtime.resolve(declaration['entrypoint'], work))]
        for argument in declaration['arguments']:
            if type(argument) is str:
                need(argument in ('--out', '--input', '--compiler'), 'Exact ordinary flag')
                command.append(argument)
            elif argument == {'output': True}:
                command.append(str(result))
            elif argument == {'compiler': True}:
                need(mode['configured_compiler'], 'Declared compiler argument')
                command.append(str(args.compiler))
            else:
                need(type(argument) is dict and set(argument) == {'input'} and argument['input'] in keys,
                     'Explicit authenticated file argument')
                command.append(str(runtime.resolve(argument['input'], work)))
        commands.append(command)
    report = {'status': 'EXACT_CHECKER_INPUTS_PREPARED_NO_SCIENTIFIC_EXECUTION',
        'mode': args.mode, 'modes_sha256': args.modes_sha256, 'materialization': materialized,
        'commands': commands, 'authentication_only': auth,
        'scientific_scope': mode['scientific_scope'], 'tools': mode['tools'],
        'execution_limits': 'No process launched; apply the separately reviewed bounded owner to these commands.',
        'whole_source_credit': 0}
    with (work/'checker_commands.json').open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
