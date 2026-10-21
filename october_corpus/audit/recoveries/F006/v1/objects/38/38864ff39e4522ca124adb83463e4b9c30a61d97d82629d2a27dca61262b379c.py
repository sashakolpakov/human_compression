"""Assess exact parser warnings in three completed F006 validation runs.

No search or finite validation is repeated. Original strict receipts are read
unchanged. The assessment has no whole-source or mathematical priority credit.
"""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re

EXPECTED_STDERR = (
    'Syntax warning: Unbound global variable in validate.g:28\n'
    '  typ:=List([1..rank-1],j->Order(t[j]*t[j+1]));;Add(types,typ);\n'
    '                                 ^\n'
    'Syntax warning: Unbound global variable in validate.g:28\n'
    '  typ:=List([1..rank-1],j->Order(t[j]*t[j+1]));;Add(types,typ);\n'
    '                                      ^\n'
).encode()
SCRIPT_SHA = '05bbf05eee8b81fe9c8a7dc60d0808e53dfda0c8661df5907132fe90af6bb66f'
CODE_SHA = '9f6245c95a19b18865397fe358f696746b06e80abb1ea9fad950ccc41f03bc96'
CHECKS_SHA = '64a06cd9b11f04b747a41ab00ef5034a4d0cb0b894a0260a91cff68657c34509'
CASES = {
    'F4': ('F006_F4_restored01', 10, 9, 1152),
    'H4': ('F006_H4_restored01', 13, 112, 11776),
    'E7': ('F006_E7_inner_restart01', 21, 8970, 4694016),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path.resolve()), bytes=len(data), sha256=digest(data))


def check_pin(record):
    need(pin(Path(record['path'])) == record, 'unchanged evidence pin')


def literal(text, prefix):
    need(text.count(prefix) == 1, 'unique literal: ' + prefix)
    start = text.index(prefix) + len(prefix)
    while text[start].isspace():
        start += 1
    need(text[start] == '[', 'list literal')
    depth = 0
    for end in range(start, len(text)):
        if text[end] == '[':
            depth += 1
        elif text[end] == ']':
            depth -= 1
            if depth == 0:
                return text[start:end + 1]
    raise ValueError('unterminated literal')


def assess_values(name, report, stderr, stdout, code, rows):
    _, limit, total, pairs = CASES[name]
    need(report['name'] == name and report['status'] == 'FAILED_NO_CERTIFICATE', 'original strict status')
    need(report['returncode'] == 0 and report['complete_marker'] is True and report['unchanged'] is True,
         'terminal execution')
    need(report['all_subset_intersections_checked'] is False, 'preserve original strict decision')
    need(report['rank_limit'] == limit and report['recorded_tuples'] == total, 'original scope')
    need(report['whole_original_credit'] == 0, 'no source credit')
    need(stderr == EXPECTED_STDERR, 'exact two harmless parser warnings')
    need(digest(code) == CODE_SHA, 'reviewed full validator')
    need(stdout.count('COMPLETE_EXCEPTIONAL_ROW_VALIDATION') == 1, 'unique completion')
    summary = re.findall(r'VALIDATED_MODEL (\w+) TUPLES (\d+) SUBSET_PAIRS (\d+)', stdout)
    need(summary == [(name, str(total), str(pairs))], 'exact tuple and subset totals')
    observed = [(int(k), ast.literal_eval(v)) for k, v in
                re.findall(r'VERIFIED_RANK\s+(\d+)\s+(\[[^\]]*\])', stdout)]
    need(observed == [(r[0], r[1:]) for r in rows], 'all validated ranks equal census')
    type_ranks = list(map(int, re.findall(r'VERIFIED_TYPE_COUNTS\s+(\d+)\s+', stdout)))
    need(type_ranks == list(range(1, limit + 1)), 'all type lists')
    for row in rows:
        k = row[0]
        types = ast.literal_eval(literal(stdout, f'VERIFIED_TYPE_COUNTS {k} '))
        need(all(isinstance(t, list) and len(t) == 2 and isinstance(t[0], list)
                 and len(t[0]) == max(k - 1, 0) and all(type(v) is int and v >= 2 for v in t[0])
                 and type(t[1]) is int and t[1] > 0 for t in types), 'valid type records')
        need(sum(t[1] for t in types) == row[1], 'type totals')
        need(sum(t[1] for t in types if all(v > 2 for v in t[0])) == row[4], 'connected type totals')
    need(sum(r[1] for r in rows) == total and sum(r[1] * 4 ** r[0] for r in rows) == pairs,
         'independently summed subset totals')


def assess_case(study, name):
    run_name, limit, total, pairs = CASES[name]
    work = study / 'reboot_20261013'
    source = work / run_name
    dest = work / 'F006_other_full_IP01' / name
    report = json.loads((dest / 'report.json').read_text())
    inp = json.loads((dest / 'input.json').read_text())
    need(inp['pins'] == report['pins'], 'original input and terminal pins agree')
    for p in report['pins']:
        check_pin(p)
    need(digest((work / 'validate_F006_rows.py').read_bytes()) == SCRIPT_SHA, 'reviewed driver')
    need(digest((dest / 'checks.g').read_bytes()) == CHECKS_SHA, 'reviewed full IP function')
    need((dest / 'model.g').read_bytes() == (study / 'corpus106_F006_exceptional_work' / (name + '_model.g')).read_bytes(),
         'exact original Coxeter model')
    src_report = json.loads((source / 'report.json').read_text())
    need(src_report['status'] == 'EXITED' and src_report['returncode'] == 0
         and src_report['complete_marker'] is True and src_report['unchanged'] is True, 'complete original census')
    need((source / 'stderr.log').read_bytes() == b'', 'clean original census stderr')
    for p in src_report['pins']:
        q = study / 'corpus106_F006_exceptional_work' / p['path']
        need(digest(q.read_bytes()) == p['sha256'], 'census input hash')
        if 'bytes' in p:
            need(q.stat().st_size == p['bytes'], 'census input length')
    raw = (source / 'stdout.log').read_text()
    need(raw.count('COMPLETE_EXHAUSTION') == 1, 'complete source search')
    pattern = (r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)'
               r'\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)')
    rows = [list(map(int, x)) for x in re.findall(pattern, raw)]
    need([r[0] for r in rows] == list(range(1, limit + 1)) and rows == inp['counts'], 'complete original ranks')
    for r in rows:
        _, n, sd, dual, cn, cs, cd = r
        need(0 <= cs <= sd <= n and cs <= cn <= n and 2 * dual == n + sd and 2 * cd == cn + cs,
             'duality arithmetic')
    reconstructed = 'ivs:=' + literal(raw, 'INVOLUTIONS_LITERAL ') + ';;\nrecordedIds:=[];;\n'
    for r in rows:
        reconstructed += f'recordedIds[{r[0]}]:=' + literal(raw, f'COMPLETE_MARKS_RANK_{r[0]} ') + ';;\n'
    reconstructed += 'reportedCounts:=' + json.dumps([r[1:] for r in rows]) + ';;\n'
    reconstructed += 'innerAction:=' + ('true' if name == 'E7' else 'false') + ';;\n'
    need((dest / 'records.g').read_text() == reconstructed, 'every original literal tuple preserved')
    stderr = (dest / 'stderr.log').read_bytes()
    stdout = (dest / 'stdout.log').read_text()
    code = (dest / 'validate.g').read_bytes()
    assess_values(name, report, stderr, stdout, code, rows)
    paths = [dest / x for x in ['report.json', 'input.json', 'stdout.log', 'stderr.log']]
    paths += [Path(p['path']) for p in report['pins']]
    paths += [study / 'corpus106_F006_exceptional_work' / p['path'] for p in src_report['pins']]
    evidence = {str(p.resolve()): pin(p) for p in paths}
    result = dict(name=name, status='ACCEPTED_EXACT_WARNINGS_AND_COMPLETE_VALIDATION',
                  original_strict_status=report['status'], tuples=total, subset_pairs=pairs,
                  ranks=limit, all_literal_records_preserved=True, exact_warning_count=2,
                  unchanged_pins=len(report['pins']), execution_repeated=False,
                  bindings=list(evidence.values()), whole_original_credit=0)
    return result, (name, report, stderr, stdout, code, rows)


def controls(values):
    tests = []
    def reject(label, index, change):
        args = list(copy.deepcopy(values))
        args[index] = change(args[index])
        try:
            assess_values(*args)
        except (ValueError, KeyError, TypeError, SyntaxError):
            tests.append(label)
        else:
            raise ValueError('mutation was accepted: ' + label)
    reject('nonzero process exit', 1, lambda r: dict(r, returncode=1))
    reject('timeout status', 1, lambda r: dict(r, status='TIMEOUT_NO_CERTIFICATE'))
    reject('changed input flag', 1, lambda r: dict(r, unchanged=False))
    reject('rewritten old decision', 1, lambda r: dict(r, all_subset_intersections_checked=True))
    reject('extra stderr error', 2, lambda b: b + b'Error, failure\n')
    reject('different warned variable', 2, lambda b: b.replace(b't[j]', b'x[j]'))
    reject('missing warning', 2, lambda b: b'')
    reject('missing completion', 3, lambda s: s.replace('COMPLETE_EXCEPTIONAL_ROW_VALIDATION', ''))
    reject('duplicate completion', 3, lambda s: s + 'COMPLETE_EXCEPTIONAL_ROW_VALIDATION\n')
    reject('missing zero rank', 3, lambda s: s.replace('VERIFIED_RANK 1 ', 'OMITTED_RANK 1 '))
    reject('altered full-IP code', 4, lambda b: b.replace(b'FullIP(t)', b'true'))
    reject('incorrect expected count', 5, lambda rows: [[r[0], r[1] + 1] + r[2:] if r[0] == 3 else r for r in rows])
    altered_pin = dict(values[1]['pins'][0], sha256='0' * 64)
    try:
        check_pin(altered_pin)
    except ValueError:
        tests.append('damaged evidence hash')
    else:
        raise ValueError('damaged evidence hash was accepted')
    return tests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--draft-two-only', action='store_true')
    args = ap.parse_args()
    need(__debug__, 'optimized Python is not permitted')
    args.out.mkdir(parents=True, exist_ok=False)
    results = []
    for name in (['F4', 'H4'] if args.draft_two_only else list(CASES)):
        result, values = assess_case(args.study.resolve(), name)
        results.append(result)
    bad = controls(values)
    report = dict(status=('DRAFT_TWO_CASES_ONLY' if args.draft_two_only else 'ACCEPTED_SEPARATE_EXACT_WARNING_ASSESSMENT'),
                  accepted=not args.draft_two_only,
                  assessor='publication_recovery', cases=results, negative_controls=bad,
                  tuple_total=sum(r['tuples'] for r in results), subset_pair_total=sum(r['subset_pairs'] for r in results),
                  whole_original_credit=0, new_question_credit=0, new_formal_credit=0,
                  finite_executions_repeated=0)
    (args.out / 'assessment.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
