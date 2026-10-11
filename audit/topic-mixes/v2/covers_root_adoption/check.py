#!/usr/bin/env python3
"""Bind the accepted L016 science and its exact scope; no mathematical replay."""
from pathlib import Path
import argparse
import hashlib
import json


def need(value, message):
    if not value:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet(path, pin, expected=None):
    need(sha(path / 'manifest.json') == pin, 'Exact accepted manifest: ' + str(path))
    rows = load(path / 'manifest.json')['exports']
    if expected is not None:
        need(len(rows) == expected, 'Complete accepted export count')
    names = set()
    for row in rows:
        rel = Path(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in names, 'Unique safe export')
        names.add(str(rel)); f = path / rel
        need(f.stat().st_size == row['bytes'] and sha(f) == row['sha256'], 'Changed accepted export: ' + str(rel))
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--public-root', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); root = args.study_root
    need(not args.out.exists(), 'Use a fresh output file')
    a = root / 'topic_Mix_L016_recovery'; r = root / 'topic_Mix_L016_independent_review'
    counts = {
        'author': packet(a, 'a1398f54debff3981d1606cb1055060b4abc75ae51f056a00c46a03c7821401a', 41),
        'distinct_review': packet(r, 'ebe16e59f738086a8e6333baa5da00809df920b2e83865720f4b22855695e9a8', 58),
        'root_diagnostic': packet(root / 'topic_Mix_L016_root_thin_diagnostic',
            '4950c88b3260b9ac8e1dd14de8f006ec4bca4a291b8f0f4f8a96c6f43f6a1767')}
    scope = load(a / 'scope.json'); review = load(r / 'review.json')
    need(review['status'] == 'ACCEPTED_UNCHANGED_FOR_DECLARED_CORRECTED_PRINCIPAL_CONTRACT' and
         review['requested_author_corrections'] == [] and review['science_author'] != review['reviewer'] and
         review['prior_role_disclosure'], 'Full distinct scientific acceptance')
    for row in scope['external_bindings']:
        f = root / row['path']
        need(f.stat().st_size == row['bytes'] and sha(f) == row['sha256'], 'Retained input changed')
    for row in scope['proof_contexts']:
        text = (a / row['path']).read_text()[row['start']:row['end']]
        need(hashlib.sha256(text.encode()).hexdigest() == row['sha256'], 'Written proof context changed')
    scientific = load(r / 'source_math_review.json')
    ids = [q['id'] for q in scope['source_rows']]
    need(len(ids) == len(set(ids)) == 19 and ids == [q['id'] for q in scientific['rows']] and
         scientific['complete_source_text_read'] and scientific['proof_contexts_read'] == len(scope['proof_contexts']) == 20,
         'Full source and written scope')
    dispositions = {q['id']: q for q in scope['source_rows']}
    for key, expected in [('B3', 'disproved_literal_auxiliary_with_repair'),
                          ('B5', 'qualified_unused_background'),
                          ('A1', 'ancillary_not_rederived'), ('A3', 'ancillary_not_rederived'),
                          ('Q1', 'excluded_unanswered_or_omitted')]:
        need(dispositions[key]['disposition'] == expected, 'Preserve explicit source qualification')
    need([q['role'] for q in scope['programs']] ==
         ['required finite premise', 'optional validation', 'optional validation'], 'Preserve required and optional programs')
    need(not scope['end_to_end_Lean'] and sum(len(q['declarations']) for q in scope['formal']) == 6,
         'Partial six-declaration Lean evidence')
    for name in ['reports/author/report.json', 'reports/copied/report.json']:
        run = load(r / name)
        need(run['status'] == 'PASS' and run['required_programs'] == 1 and run['optional_validation_programs'] == 2 and
             run['formal_declarations'] == 6 and run['new_formal_declarations'] == 4 and
             len(run['program_mutations_rejected']) == 6 and len(run['formal_mutations_rejected']) == 3 and
             run['whole_program_inclusion'] and not run['full_Lean'] and
             [q['pages'] for q in run['renders']] == [4, 6, 3] and
             all(q['per_page_text_equal'] for q in run['renders']), 'Full accepted replay evidence')
    independent = load(r / 'reports/independent/report.json')
    need(independent['status'] == 'PASS' and independent['all_subset_intersections'] == 1024 and
         independent['source_universal_order'] == 96 and len(independent['scope_controls']) == 8,
         'Distinct finite checks and scope controls')
    cost = scope['whole_topic_cost_policy']
    need(cost['full_existing_Mixes_common'] and cost['full_new_common_and_application'] and
         cost['no_cross_topic_discount'] and cost['optional_validation_symmetric'] and
         cost['source_historical_GAP_and_Atlas_cost'] is None, 'Complete common dependency and symmetric policy')
    old = root / 'topic_Mix_F005_recovery/fiber_intersections.pdf'
    public = args.public_root / 'papers/topic-mixes/v1/packet/fiber_intersections.pdf'
    need(old.read_bytes() == public.read_bytes(), 'Existing whole Mixes common paper must be the accepted public one')
    result = dict(status='PASS_ROOT_L016_SCIENTIFIC_ADOPTION_BINDINGS', accepted_packet_exports=counts,
                  source_dispositions=19, written_proof_contexts=20, required_programs=1,
                  optional_validation_programs=2, generic_Lean_declarations=6,
                  new_generic_Lean_declarations=4, full_source_formalized=False,
                  prior_whole_Mixes_common_retained=True, scientific_review_reused=True,
                  fresh_mathematical_program_or_Lean_run=False, source_registration=False,
                  ratios_computed=False, new_conjecture_credit=0)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
