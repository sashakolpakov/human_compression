"""Verify one complete saved tree with private reads and children denied."""
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
SCRIPT = PACKAGE/'scripts/edge_girth_regular_graphs/certificate_checks.py'
MODES = PACKAGE/'data/edge_girth_regular_graphs/tree_certificate_modes.json'


def need(value, message):
    if not value:
        raise ValueError(message)


def pin(path):
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
    need(pin(args.case)['sha256'] == args.case_sha256, 'Reviewed case')
    case = json.loads(args.case.read_bytes())
    need(set(case) == {'schema', 'script', 'modes', 'component', 'expected', 'scope', 'report_semantics'}, 'Exact case fields')
    need(case['schema'] == 'F012_ISOLATED_SAVED_TREE_CASE_V1', 'Case schema')
    need(pin(SCRIPT) == case['script'] and pin(MODES) == case['modes'], 'Reviewed shared interface')
    modes = json.loads(MODES.read_bytes())
    selection = modes['components'][case['component']]
    need(case['component'] == '29' and selection['kind'] == 'saved_tree'
         and selection['number'] == 29, 'Exact child-free saved-tree mode')
    manifest_path = PACKAGE/modes['runtime_manifest']
    need(pin(manifest_path)['sha256'] == modes['runtime_manifest_sha256'], 'Manifest identity')
    output = args.out.absolute()
    need(not output.exists() and not output.is_symlink(), 'Fresh output')
    denied = []

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study read denied')
        if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.fork', 'os.forkpty', 'os.posix_spawn'):
            raise PermissionError('Child processes denied')
        if event.startswith('socket.'):
            raise PermissionError('Network denied')

    sys.addaudithook(audit)
    forbidden = STUDY/'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise RuntimeError('Private-read denial control failed')
    need(denied == [str(forbidden)], 'One positive denial control')
    sys.path[:] = [p for p in sys.path if p and not Path(p).absolute().is_relative_to('/Users/sasha/medusa')]
    sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--modes-sha256', case['modes']['sha256'],
                '--component', case['component'], '--out', str(output), '--full-check']
    runpy.run_path(str(SCRIPT), run_name='__main__')
    portable = json.loads((output/'portable_report.json').read_bytes())
    need(portable['status'] == 'CHECKED_PORTABLE_CERTIFICATE_COMPONENT'
         and portable['component'] == case['component'], 'Complete portable return')
    need(portable['kind'] == 'saved_tree' and portable['compiler_commands'] == []
         and portable['saved_tree_predicates_unchanged'] is True
         and portable['ordinary_sanitized_replayed'] is False
         and portable['historical_payloads_freshly_verified'] is False,
         'Saved-tree scope and truthful historical authentication')
    result_path = output/'scientific'/selection['result_relative']
    need([pin(result_path)['bytes'], pin(result_path)['sha256']] == portable['scientific_result'], 'Result binding')
    result = json.loads(result_path.read_bytes())
    for condition in case['expected']:
        need(set(condition) == {'pointer', 'value'}, 'Literal expected result')
        value = result
        for field in condition['pointer']:
            value = value[field]
        need(value == condition['value'], 'Expected field '+str(condition['pointer']))
    need(denied == [str(forbidden)], 'No scientific private reads')
    record = dict(status='PASS_ISOLATED_PORTABLE_SAVED_TREE', component=case['component'],
                  result=pin(result_path), portable_report=pin(output/'portable_report.json'),
                  private_open_positive_control=True, scientific_private_open_attempts=0,
                  children_and_network_denied=True, whole_source_credit=0,
                  scope=case['scope'],
                  original_report_field_semantics=case['report_semantics'],
                  actually_materialized_inputs=portable['runtime_inputs'],
                  actual_authentication=portable['authentication'],
                  historical_payloads_freshly_verified=portable['historical_payloads_freshly_verified'],
                  isolation='Python -E -B owner child with project import roots removed and audit guards; no claim that sys.flags.isolated is set.')
    with (output/'isolation.json').open('x') as stream:
        json.dump(record, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=record['status'], component=case['component'])), flush=True)


if __name__ == '__main__':
    main()
