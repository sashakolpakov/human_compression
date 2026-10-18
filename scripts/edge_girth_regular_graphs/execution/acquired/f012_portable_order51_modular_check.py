"""Full declared order-51 modular certificate check; positional directory output."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys

if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
STUDY = Path('/Users/sasha/medusa/research/leemans')
PACKAGE = STUDY/'computation/f012/source_synthesis/package'
PREPARER = PACKAGE/'scripts/edge_girth_regular_graphs/prepare_check.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/execution_modes.json'


def need(value,message):
    if not value:
        raise ValueError(message)


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--case',type=Path,required=True)
    parser.add_argument('--case-sha256',required=True)
    args = parser.parse_args()
    need(pin(args.case)['sha256'] == args.case_sha256,'Exact reviewed application case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema','mode','preparer','modes','entrypoint','expected','scope'},'Complete pure-check case')
    need(case['schema'] == 'F012_ISOLATED_PURE_CHECK_CASE_V1','Exact case schema')
    need(case['mode'] == 'order51_modular_certificates','Exact reviewed modular-certificate mode')
    need(pin(PREPARER) == case['preparer'] and pin(MODES) == case['modes'],'Exact acquired preparer and modes')
    modes = json.loads(MODES.read_bytes())
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'],'Exact runtime declaration')
    manifest = json.loads(manifest_path.read_bytes())
    mode = modes['modes'][case['mode']]
    need(not mode['configured_compiler'] and mode['python_environment'] == 'isolated'
         and len(mode['commands']) == 1,'Only one declared isolated pure-Python entrypoint')
    need(mode['commands'][0]['entrypoint'] == case['entrypoint'],'Exact selected entrypoint')
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(),'Fresh output required')
    denied = []
    def audit(event,values):
        if event == 'open' and isinstance(values[0],(str,bytes,os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study access denied')
        if event in ('subprocess.Popen','os.system','os.exec','os.fork','os.posix_spawn'):
            raise PermissionError('This pure replay cannot launch children')
        if event.startswith('socket.'):
            raise PermissionError('This pure replay cannot use the network')
    sys.addaudithook(audit)
    forbidden = STUDY/'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError('Private-open positive control failed')
    need(denied == [str(forbidden)],'Exact positive denial')
    # The owner starts -E -B. Remove study/project import roots as well;
    # actual isolation is enforced by the audit boundary, not a false claim
    # that this already running process has sys.flags.isolated set.
    sys.path[:] = [x for x in sys.path if x and not Path(x).absolute().is_relative_to(Path('/Users/sasha/medusa'))]
    output.mkdir()
    work = output/'inputs'
    result = output/'spectral'
    scientific_report = result/'report.json'
    sys.argv = [str(PREPARER),'--root',str(PACKAGE),'--modes-sha256',case['modes']['sha256'],
                '--mode',case['mode'],'--work',str(work),'--check-output',str(result)]
    runpy.run_path(str(PREPARER),run_name='__main__')
    prepared = json.loads((work/'checker_commands.json').read_bytes())
    need(prepared['status'] == 'EXACT_CHECKER_INPUTS_PREPARED_NO_SCIENTIFIC_EXECUTION'
         and prepared['mode'] == case['mode'] and len(prepared['commands']) == 1,'One exact prepared command')
    command = prepared['commands'][0]
    need(command[:3] == [sys.executable,'-I','-B'] and command[-1:] == [str(result)]
         and len(command) == 5,'Exact positional modular-certificate argv')
    script = Path(command[3])
    need(script.is_relative_to(work) and script.is_file() and not script.is_symlink(),'Materialized scientific source only')
    need(prepared['materialization']['files'] == mode['inputs'],'Complete selected input roster')
    materialized = [work/manifest['files'][key]['materialized_path'] for key in mode['inputs']]
    before = list(map(pin,materialized))
    sys.argv = command[3:]
    runpy.run_path(str(script),run_name='__main__')
    actual = json.loads(scientific_report.read_bytes())
    for condition in case['expected']:
        need(set(condition) == {'pointer','value'} and type(condition['pointer']) is list,'Literal expected JSON field')
        value = actual
        for field in condition['pointer']:
            value = value[field]
        need(value == condition['value'],'Exact literal result field '+str(condition['pointer']))
    after = list(map(pin,materialized))
    need(before == after,'All materialized scientific input bytes unchanged')
    need(denied == [str(forbidden)],'Scientific replay attempted private access')
    report = dict(status='PASS_ISOLATED_PORTABLE_PYTHON_COMPONENT',mode=case['mode'],
        case=case,source_inputs=before,result=pin(scientific_report),private_open_positive_control=True,
        scientific_private_open_attempts=0,children_and_network_denied=True,
        execution='Unchanged script via runpy in -E -B owner child; project import roots removed and audit denial active.',
        source_credit=0,whole_source_credit=0)
    with (output/'isolation.json').open('x') as stream:
        json.dump(report,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(status=report['status'],mode=case['mode'],whole_source_credit=0)),flush=True)


if __name__ == '__main__':
    main()
