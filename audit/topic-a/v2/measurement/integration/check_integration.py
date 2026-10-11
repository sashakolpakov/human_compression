#!/usr/bin/env python3
"""Read-only bounded review of the public numerical integration.

No census, Lean proof, or complete document recount is run here. In-memory
semantic controls bypass file bindings deliberately; real bindings are tested
separately, and the complete unchanged checker function is executed first.
"""
from pathlib import Path
import ast
import copy
from hashlib import sha256
import importlib.util
import json
import subprocess

PUBLIC = Path('/Users/sasha/medusa/math_compression')
STUDY = Path('/Users/sasha/medusa/research/leemans')
HERE = Path(__file__).resolve().parent
BASE = '6641c356b39ea9ca650542a41869b7811fdfc0ff'
PREFIX = 'audit/topic-a/v2/measurement/'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def binding(path):
    data = (PUBLIC/path).read_bytes()
    return dict(path=path, bytes=len(data), sha256=sha256(data).hexdigest())

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

def main():
    old = subprocess.run(['git', 'show', BASE+':scripts/verify_snapshot.py'],
                         cwd=PUBLIC, capture_output=True, check=True).stdout.decode()
    new = (PUBLIC/'scripts/verify_snapshot.py').read_text()
    functions = lambda text: {n.name:ast.dump(n, include_attributes=False)
                             for n in ast.parse(text).body
                             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    before, after = functions(old), functions(new)
    unchanged = [name for name in before if name != 'main']
    need(all(before[name] == after[name] for name in unchanged),
         'An existing verification function changed')
    need(set(after)-set(before) == {'check_topic_a_measurement'}, 'Unexpected checker additions')
    # The main function is read manually: one new call between the existing
    # Topic E measurement and graph checks, plus clarified reporting strings.
    checker = module(PUBLIC/'scripts/verify_snapshot.py', 'bounded_topic_a_verifier')
    actual = checker.check_topic_a_measurement()
    need(actual == (420,300), 'Unexpected verified dimensions')
    original_load, original_bindings = checker.load, checker.check_bindings
    values = {name:original_load(PREFIX+name) for name in
              ['admission.json','input_spec.json','results.json','accepted_current_recount.json']}
    controls = []
    coordinate = lambda x: x['results.json']['factors']['NFC']['calibrated_selected']['characters_without_whitespace']
    cases = [
        ('omit umbrella from total', lambda x: coordinate(x)['costs'].__setitem__('full_written_papers', coordinate(x)['costs']['six_applications'])),
        ('charge printed program twice', lambda x: coordinate(x)['costs'].__setitem__('full_program_inclusive', coordinate(x)['costs']['full_program_inclusive']+coordinate(x)['costs']['complete_printed_program_appendix'])),
        ('remove one whole program', lambda x: x['input_spec.json']['required_programs'].pop()),
        ('remove explicit conditional prepayment', lambda x: coordinate(x)['conditional_applications'][0].__setitem__('given', 'No common costs needed.')),
        ('assign missing image text zero', lambda x: x['results.json'].__setitem__('missing_visible_text_cost',0)),
        ('change a denominator', lambda x: coordinate(x)['written_topic'].__setitem__('denominator',1)),
        ('remove source and application together', lambda x: (x['results.json']['documents'].pop('A6'),x['accepted_current_recount.json']['documents'].pop('A6'))),
    ]
    try:
        # These mutations intentionally test the arithmetic and scope logic
        # after hash verification, without changing any public byte.
        checker.check_bindings = lambda rows: None
        for label, mutate in cases:
            current = copy.deepcopy(values)
            mutate(current)
            checker.load = lambda path: current[path.removeprefix(PREFIX)]
            try:
                checker.check_topic_a_measurement()
            except ValueError as error:
                controls.append(dict(control=label, result='REJECTED', reason=str(error)))
            else:
                raise ValueError('Semantic control accepted: '+label)
    finally:
        checker.load, checker.check_bindings = original_load, original_bindings
    row = copy.deepcopy(values['admission.json']['artifacts'][0])
    row['sha256'] = '0'*64
    try:
        checker.check_bindings([row])
    except ValueError as error:
        controls.append(dict(control='wrong actual artifact digest', result='REJECTED', reason=str(error)))
    else:
        raise ValueError('Changed artifact digest accepted')
    extract = module(PUBLIC/PREFIX/'extract_inputs.py', 'bounded_topic_a_extractor')
    row = copy.deepcopy(values['input_spec.json']['sources']['L032'])
    row['included_spans'][0]['start'] = 1
    try:
        extract.document(STUDY, 'L032', row)
    except ValueError as error:
        need('complete-document scope' in str(error), 'Unexpected source-boundary failure')
        controls.append(dict(control='replace full source by proper text span', result='REJECTED', reason=str(error)))
    else:
        raise ValueError('Partial source span accepted')
    report = dict(status='PASS_BOUNDED_INDEPENDENT_INTEGRATION_CHECK', baseline_commit=BASE,
                  checker=binding('scripts/verify_snapshot.py'),
                  unchanged_existing_functions=unchanged,
                  verified_recorded_metric_cells=420, verified_fractions=300,
                  negative_controls=controls,
                  full_census_or_Lean_rerun=False,
                  full_independent_pdf_recount=False,
                  primary_scope='Complete-document extractable text under the admitted main-result contracts; missing image text and other unmeasured costs remain unknown.',
                  mutations='In memory only; no public files changed.')
    (HERE/'checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], unchanged_functions=len(unchanged),
                         controls=len(controls), cells=420, fractions=300)))

if __name__ == '__main__':
    main()
