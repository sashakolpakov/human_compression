"""Assess completed comparisons without erasing their original strict receipts.

Only the two exact, understood GAP parser warnings are allowed. This does not
reclassify a timeout, incomplete run, changed input, or any other diagnostic.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re

S = Path(__file__).resolve().parent.parent
CODE = 'f4562c7f03482b1c7ec5d734423040765aae0d29fb25dcf05d673be9807df3fc'
WARNINGS = 'edd645381693fb60d0d91c46d87f8b4c94b89ada3d8de6e69382356aa6826dce'
NAMES = {'M11', 'M12', 'J1', 'M22', 'J2', 'M23', 'HS', 'M24', 'McL', 'Tits', 'He', 'J3'}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate(receipt, stdout, stderr, code):
    name = receipt['name']
    need(name in NAMES, 'named source classification')
    need(receipt['returncode'] == 0 and receipt['complete_marker'] is True and
         receipt['unchanged'] is True, 'normal complete unchanged execution')
    need(receipt['status'] in ('EXITED', 'FAILED_NO_CERTIFICATE'), 'no interrupted execution')
    need(digest(code) == CODE, 'exact reviewed comparison program')
    need(stderr == b'' or digest(stderr) == WARNINGS, 'no unknown diagnostic')
    trailer = re.findall(r'COMPLETE_SOURCE_ORBIT_BIJECTION (\w+) CLASSES (\d+)', stdout)
    need(trailer == [(name, str(receipt['source_markings']))], 'one exact completed bijection')
    matches = [tuple(map(int, x)) for x in
               re.findall(r'SOURCE_MATCH\s+(\d+)\s+LEAF\s+\[\s*(\d+)\s*,\s*(\d+)\s*\]\s+TRANSPORTER', stdout)]
    need([x[0] for x in matches] == list(range(1, receipt['source_markings'] + 1)),
         'every source marking in order')
    need(len({x[1:] for x in matches}) == len(matches), 'distinct target leaves')
    need(all(x[1] > 0 and x[2] > 0 for x in matches), 'positive leaf coordinates')
    return matches


def main(args):
    args.out.mkdir(parents=True, exist_ok=False)
    reports = []
    for name in sorted(NAMES):
        p = args.run / name
        receipt = json.loads((p / 'report.json').read_text())
        stdout = (p / 'stdout.log').read_text()
        stderr = (p / 'stderr.log').read_bytes()
        code = (p / 'compare.g').read_bytes()
        matches = validate(receipt, stdout, stderr, code)
        for pin in receipt['pins']:
            path = Path(pin['path'])
            if not path.is_absolute():
                path = S / path
            need(digest(path.read_bytes()) == pin['sha256'], 'unchanged execution pin')
        rows = []
        for rel in ('report.json', 'stdout.log', 'stderr.log', 'compare.g', 'records.g', 'source.g'):
            path = p / rel
            rows.append(dict(path=str(path.resolve()), bytes=path.stat().st_size,
                             sha256=digest(path.read_bytes())))
        reports.append(dict(name=name, status='COMPLETE_BIJECTION_PENDING_DISTINCT_REVIEW',
                            original_strict_status=receipt['status'], source_markings=len(matches),
                            exact_known_warnings=stderr != b'', execution_bindings=rows,
                            pins_checked=len(receipt['pins']), long_execution_repeated=False))
    # Controls exercise the operational boundary, not the group-theoretic proof.
    p = args.run / 'M12'
    receipt = json.loads((p / 'report.json').read_text())
    stdout = (p / 'stdout.log').read_text()
    stderr = (p / 'stderr.log').read_bytes()
    code = (p / 'compare.g').read_bytes()
    controls = []
    for key, value in [('returncode', 1), ('complete_marker', False),
                       ('unchanged', False), ('status', 'TIMEOUT_NO_CERTIFICATE'),
                       ('source_markings', receipt['source_markings'] + 1)]:
        bad = copy.deepcopy(receipt)
        bad[key] = value
        try:
            validate(bad, stdout, stderr, code)
        except ValueError:
            controls.append(key)
        else:
            raise ValueError('invalid receipt accepted: ' + key)
    for name, badout, baderr, badcode in [
        ('unknown diagnostic', stdout, stderr + b'Error: unexpected failure\n', code),
        ('changed program', stdout, stderr, code + b'\n'),
        ('missing completion', stdout.replace('COMPLETE_SOURCE_ORBIT_BIJECTION', 'INCOMPLETE'), stderr, code),
        ('missing marking', stdout.replace('SOURCE_MATCH 1 LEAF', 'OMITTED_MATCH 1 LEAF'), stderr, code),
    ]:
        try:
            validate(receipt, badout, baderr, badcode)
        except ValueError:
            controls.append(name)
        else:
            raise ValueError('invalid control accepted: ' + name)
    need(sum(r['source_markings'] for r in reports) == 6047, 'whole auxiliary archive')
    result = dict(status='AUTHOR_ASSESSMENT_COMPLETE_PENDING_DISTINCT_REVIEW',
                  groups=12, source_markings=6047, reports=reports, controls=controls,
                  original_receipts_unchanged=True, native_searches_repeated=0,
                  warning_semantics='h and transporter are globals assigned before every lambda evaluation. GAP parses the enclosing if statement before executing those assignments. Exact GAP reference79.10-1 and the full comparison program are separate review inputs.',
                  whole_original_credit=0)
    (args.out / 'assessment.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'reports'}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    main(p.parse_args())
