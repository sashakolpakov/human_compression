"""One isolated replay of the packaged seventy-domain transport certificate."""
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
PACKAGE = STUDY / 'computation/f012/source_synthesis/package'
SCRIPT = PACKAGE / 'scripts/edge_girth_regular_graphs/saved_refutations.py'
CASES = PACKAGE / 'data/edge_girth_regular_graphs/saved_refutation_cases.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--script-sha256', required=True)
    parser.add_argument('--cases-sha256', required=True)
    args = parser.parse_args()
    output = args.out.absolute()
    if output.exists() or output.is_symlink():
        raise ValueError('Fresh output required')
    for path, expected in ((SCRIPT, args.script_sha256), (CASES, args.cases_sha256)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Changed declared portable input')
    denied = []

    def audit(event, values):
        if event == 'open' and isinstance(values[0], (str, bytes, os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(values[0])))
            if path.is_relative_to(STUDY) and not (
                    path.is_relative_to(PACKAGE) or path.is_relative_to(output)):
                denied.append(str(path))
                raise PermissionError('Private study access denied')
        if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.fork', 'os.posix_spawn'):
            raise PermissionError('This pure transport replay cannot launch children')
        if event.startswith('socket.'):
            raise PermissionError('This replay cannot use the network')

    sys.addaudithook(audit)
    forbidden = STUDY / 'reboot_20261013/CURRENT.json'
    try:
        forbidden.read_bytes()
    except PermissionError:
        pass
    else:
        raise AssertionError('Private-open positive control failed')
    if denied != [str(forbidden)]:
        raise AssertionError('Unexpected denial control')
    sys.argv = [str(SCRIPT), '--root', str(PACKAGE), '--cases-sha256', args.cases_sha256,
                '--case', 't6_transport', '--reconstruct', '--out', str(output)]
    runpy.run_path(str(SCRIPT), run_name='__main__')
    result = json.loads((output / 'result.json').read_text())
    if not (result['status'] == 'CHECKED_PORTABLE_SEVENTY_DOMAIN_TRANSPORTS'
            and result['domains'] == result['exact_models_rebuilt'] == 70
            and len(result['representatives']) == 24
            and result['nauty_calls'] == result['solver_calls'] == result['proof_reads'] == 0):
        raise AssertionError('Exact transport scope did not pass')
    if denied != [str(forbidden)]:
        raise AssertionError('Scientific replay attempted private access')
    report = dict(status='PASS_ISOLATED_PORTABLE_SEVENTY_DOMAIN_TRANSPORT',
                  private_open_positive_control=True, scientific_private_open_attempts=0,
                  children_and_network_denied=True, domains=70, representatives=24,
                  source_credit=0, whole_source_credit=0)
    with (output / 'isolation.json').open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
