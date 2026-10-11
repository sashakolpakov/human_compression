#!/usr/bin/env python3
"""Bounded evidence/coverage check; not a proof assistant for the prose."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
OLD = r'\(\mathbb F_{16}\)\emph{/F4}'
NEW = r'\(\mathbb F_{16}^{*}/\mathbb F_4^{*}\)'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def safe(root, relative):
    path = Path(relative)
    need(not path.is_absolute() and '..' not in path.parts, 'unsafe relative path')
    result = root / path
    need(not result.is_symlink(), 'symlinked evidence')
    need(result.resolve().is_relative_to(root.resolve()), 'evidence escapes root')
    return result


def check_binding(root, row):
    data = safe(root, row['path']).read_bytes()
    need(len(data) == row['bytes'] and digest(data) == row['sha256'],
         'changed bound file: ' + row['path'])


def check_contract(scope, readings, expected_rows):
    rows = [row for row in scope['rows'] if row['source'] == 'L092']
    need(rows == expected_rows, 'L092 source rows or qualifications changed')
    need(len(rows) == 35 and len({row['id'] for row in rows}) == 35,
         'incomplete L092 row coverage')
    need([row['id'] for row in readings] == [row['id'] for row in rows],
         'reading-note coverage mismatch')
    for note, row in zip(readings, rows):
        need(note['source_locator'] == row['source_locator'] and
             note['author_status'] == row['status'] and
             note['proof_spans'] == row['new_proof_spans'], 'changed reading interface')
        need(bool(note['review_note'].strip()), 'missing mathematical reading note')
    need(scope['new_source_credit'] == 0 and scope['new_question_credit'] == 0
         and scope['ratio'] is None, 'new credit or ratio introduced')
    need(scope['intake_closed'] is True, 'closed-intake boundary lost')
    return sorted({span for row in rows for span in row['new_proof_spans']})


def check_literal_change(old, new):
    need(old.count(OLD) == 1, 'unexpected original quotient occurrence')
    need(new == old.replace(OLD, NEW), 'notation delta is not the exact accepted repair')


def check_scope_delta(old, new):
    a, b = copy.deepcopy(old), copy.deepcopy(new)
    for data in (a, b):
        row = data['proof_spans']['LinearBases']
        for key in ('bytes', 'sha256'):
            row.pop(key)
    need(a == b, 'scope delta changes more than the LinearBases text binding')


def rejection(name, callback):
    try:
        callback()
    except (ValueError, KeyError, IndexError):
        return {'name': name, 'rejected': True}
    raise ValueError('control was accepted: ' + name)


def audit(args):
    evidence = read_json(HERE / 'bindings.json')
    roots = {'author': args.author, 'delta': args.delta,
             'program_review': args.program_review}
    if args.study:
        roots['study'] = args.study
    if args.repository:
        roots['repository'] = args.repository
    checked, omitted = [], []
    for origin, rows in evidence.items():
        if origin not in roots:
            omitted.append(origin)
            continue
        for row in rows:
            check_binding(roots[origin], row)
            checked.append(origin + ':' + row['path'])
    base_manifest = read_json(args.author / 'manifest.json')
    for row in base_manifest['exports']:
        check_binding(args.author, row)
    delta_manifest = read_json(args.delta / 'manifest.json')
    for row in delta_manifest['exports']:
        check_binding(args.delta, row)
    old = read_json(args.author / 'scope.json')
    new = read_json(args.delta / 'scope.json')
    check_scope_delta(old, new)
    old_tex = (args.author / 'sections/linear-bases.tex').read_text()
    new_tex = (args.delta / 'sections/linear-bases.tex').read_text()
    check_literal_change(old_tex, new_tex)
    old_pages = [p.extract_text() or '' for p in PdfReader(args.author / 'steiner-geometries.pdf').pages]
    new_pages = [p.extract_text() or '' for p in PdfReader(args.delta / 'steiner-geometries.pdf').pages]
    need(len(old_pages) == len(new_pages) == 22, 'Steiner page count changed')
    changed_pages = [i + 1 for i, (a, b) in enumerate(zip(old_pages, new_pages)) if a != b]
    need(changed_pages == [4], 'notation repair changed other extracted pages')
    notes = read_json(HERE / 'proof_reading.json')['rows']
    expected = [row for row in old['rows'] if row['source'] == 'L092']
    spans = check_contract(new, notes, expected)
    for name in spans:
        row = new['proof_spans'][name]
        path = safe(args.delta, row['path'])
        if not path.exists():
            path = safe(args.author, row['path'])
        text = path.read_text()
        begin = text.index(row['start_anchor']) if row['start_anchor'] else 0
        end = (text.index(row['end_anchor'], begin + len(row['start_anchor'] or ''))
               if row['end_anchor'] else len(text))
        data = text[begin:end].encode()
        need(len(data) == row['bytes'] and digest(data) == row['sha256'],
             'changed proof span: ' + name)
    # These are scope/integrity controls, not numerical counterexamples.
    controls = []
    bad = copy.deepcopy(new)
    bad['rows'] = [r for r in bad['rows'] if r['id'] != 'L092.T11']
    controls.append(rejection('omitted principal classification clause',
                              lambda: check_contract(bad, notes, expected)))
    bad = copy.deepcopy(new)
    next(r for r in bad['rows'] if r['id'] == 'L092.Pasini.names')['status'] = 'recovered'
    controls.append(rejection('excluded named-geometry identification promoted',
                              lambda: check_contract(bad, notes, expected)))
    bad = copy.deepcopy(new)
    next(r for r in bad['rows'] if r['id'] == 'L092.T2')['status'] = 'recovered'
    controls.append(rejection('retained classification promoted to an internal proof',
                              lambda: check_contract(bad, notes, expected)))
    bad = copy.deepcopy(new)
    bad['new_question_credit'] = 1
    controls.append(rejection('prior unital answer recounted',
                              lambda: check_contract(bad, notes, expected)))
    controls.append(rejection('multiplicative quotient repair omitted',
                              lambda: check_literal_change(old_tex, old_tex)))
    controls.append(rejection('additional theorem text changed in the notation repair',
                              lambda: check_literal_change(old_tex, new_tex + '\n')))
    bad = copy.deepcopy(new)
    next(r for r in bad['rows'] if r['id'] == 'L092.L5')['new_proof_spans'] = ['S1']
    controls.append(rejection('subline connectivity proof interface weakened',
                              lambda: check_scope_delta(old, bad)))
    return {'status': 'PASS', 'verified_file_bindings': checked,
            'optional_binding_roots_not_supplied': omitted,
            'unchanged_author_exports': len(base_manifest['exports']),
            'delta_exports': len(delta_manifest['exports']),
            'source_rows': 35, 'proof_spans': len(spans),
            'exact_one_notation_replacement': True,
            'pdf_pages': 22, 'changed_extracted_pages': changed_pages,
            'all_source_rows_unchanged': True, 'controls': controls,
            'scope': 'Evidence integrity and exact review scope only. Written proofs were read by the reviewer; no source extraction, GAP execution, Lean compilation or mechanized proof is claimed by this check.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author', type=Path, required=True)
    ap.add_argument('--delta', type=Path, required=True)
    ap.add_argument('--program-review', type=Path, required=True)
    ap.add_argument('--study', type=Path, help='optional acquired primary and prior private bindings')
    ap.add_argument('--repository', type=Path, help='optional prior public admission bindings')
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'output must be fresh')
    result = audit(a)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'source_rows', 'proof_spans', 'unchanged_author_exports')}))


if __name__ == '__main__':
    main()
