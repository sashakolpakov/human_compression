#!/usr/bin/env python3
"""Reviewer semantic replay and two independent non-vacuity controls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

AUTHOR_HASH = '2fd04abbd8610404fefa5dec7ff486489256d387e536ec2f73e368ebe2d76031'


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--gap', default='gap')
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), 'fresh output directory required')
    source = (root / 'phase179_livingstone_check.g').read_bytes()
    require(sha256(source).hexdigest() == AUTHOR_HASH and source.endswith(b'QUIT;\n'), 'author binding')
    reviewer = root / 'phase184_source_predicate_review.g'
    out.mkdir(parents=True)
    families = out / 'author_families.g'
    families.write_bytes(source[:-6])
    scenarios = [
        ('positive', '', None),
        ('wrong_P_colour', '''OriginalIncident184:=Incident179;;
Incident179:=function(mode,i,j,x,y)
 if mode=2 and i=2 and j=4 then return y in x[2];fi;
 return OriginalIncident184(mode,i,j,x,y);
end;;
''', 'literal source predicate disagreement'),
        ('remove_repair', '''RepairedIncident179:=function(mode,i,j,x,y)
 return Incident179(mode,i,j,x,y);
end;;
''', 'algebraic induced-quadruple repair'),
    ]

    def run(scenario):
        name, change, expected = scenario
        script = out / (name + '.g')
        script.write_text('Read(' + json.dumps(str(families)) + ');;\n' + change +
                          'Read(' + json.dumps(str(reviewer)) + ');;\n')
        start = time.monotonic()
        proc = subprocess.run([args.gap, '-q', '-T', str(script)], capture_output=True, text=True, timeout=300)
        log = proc.stdout + proc.stderr
        (out / (name + '.log')).write_text(log)
        marker = 'PHASE184_SEMANTIC_SOURCE_REVIEW_PASS'
        if expected is None:
            require(proc.returncode == 0 and marker in log and 'warning' not in log and 'Error,' not in log,
                    'positive semantic review failed')
            require(log.count('REVIEWER_SOURCE_RELATION') == 12, 'missing semantic relation')
            require('[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5 ]' in log, 'unexpected extension counts')
        else:
            require(marker not in log and expected in log, 'review control was not rejected: ' + name)
        return {'scenario': name, 'expected_rejection': expected, 'result': 'PASS',
                'exit_code': proc.returncode, 'seconds': time.monotonic() - start,
                'log_sha256': sha256(log.encode()).hexdigest()}

    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(run, scenarios))
    report = {'status': 'PASS', 'author_sha256': AUTHOR_HASH,
              'reviewer_sha256': sha256(reviewer.read_bytes()).hexdigest(), 'runs': records,
              'scope': 'Independent source-predicate and all-neighbour semantic check; author graph/object construction retained. Two reviewer-designed mutations occur after the complete unmodified author computation.'}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PHASE184_REVIEW_SEMANTICS_AND_CONTROLS_PASS')


if __name__ == '__main__':
    main()
