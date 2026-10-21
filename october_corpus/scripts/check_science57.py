"""Check the additive F011 admission without changing earlier measurements."""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

AUDIT = 'audit/science57/v1'
SCIENCE = 'audit/recoveries/F011/v1'


def need(value, message):
    if not value:
        raise ValueError('SCIENCE57: ' + message)


def load(path):
    return json.loads(path.read_text())


def bind(root, row):
    path = PurePosixPath(row['path'])
    need(not path.is_absolute() and '..' not in path.parts, 'safe relative path')
    raw = (root / path).read_bytes()
    need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
         'file binding ' + row['path'])


def verify(root, require_root=True):
    root = Path(root).resolve()
    history = load(root / AUDIT / 'history_routes.json')['routes']
    for row in history.values():
        bind(root, row)
    old = load(root / history['audit/corpus/latest.json']['path'])
    current = load(root / 'audit/corpus/latest.json')
    need((current['originals'], current['admitted_principal_originals'],
          current['currently_measured_originals'], current['accessible_pending_complete_recovery'],
          current['editorial_originals']) == (106, 57, 53, 48, 1), 'fixed corpus partition')
    admitted = current['admitted_original_ids']
    pending = current['accessible_pending_original_ids']
    need(len(admitted) == len(set(admitted)) == 57 and
         set(admitted) == set(old['admitted_original_ids']) | {'F011'}, 'one new original')
    need(len(pending) == len(set(pending)) == 48 and
         set(pending) == set(old['accessible_pending_original_ids']) - {'F011'}, 'pending subtraction')
    need(set(admitted).isdisjoint(pending) and
         set(admitted) | set(pending) | {'L022'} == set(current['active_original_ids']), 'disjoint partition')
    for key in ['measured_original_ids', 'added_measurements', 'current_topic_replacements',
                'historical_admitted_ids', 'active_original_ids', 'archived_original_ids',
                'editorial_original_ids', 'editorial_factor', 'source_retrieval_in_scope',
                'all_original_proofs_recovered', 'all_conjectures_resolved']:
        need(current[key] == old[key], 'unchanged boundary ' + key)
    need(current['measurement_pending_original_ids'] == current['scientific_unmeasured_original_ids'] ==
         ['F011', 'L024', 'L102', 'N014'], 'four unmeasured originals')
    for key in ['active_catalogue', 'snapshot', 'current_science_registration']:
        bind(root, current[key])
    need(load(root / current['snapshot']['path']) == {k: v for k, v in current.items() if k != 'snapshot'},
         'exact current snapshot')
    need(current['added_admissions'] == old['added_admissions'] + [current['current_science_registration']],
         'one appended registration')
    bind(root, old['active_catalogue'])
    oldcat = load(root / old['active_catalogue']['path'])
    cat = load(root / current['active_catalogue']['path'])
    before = {r['original_id']: r for r in oldcat['entries']}
    after = {r['original_id']: r for r in cat['entries']}
    need(len(cat['entries']) == len(after) == 106 and before.keys() == after.keys(), 'same original IDs')
    need(all(before[k] == after[k] for k in before if k != 'F011'), '105 other records exact')
    for key in before['F011']:
        if key not in ['current_principal_recovery', 'next_obligation']:
            need(before['F011'][key] == after['F011'][key], 'fixed F011 source identity/history')
    recovery = after['F011']['current_principal_recovery']
    need(recovery['historical_admission_evidence'] == before['F011']['current_principal_recovery'] and
         recovery['principal_contract_admitted'] and not recovery['measured'] and
         recovery['compression_factor'] is None, 'corrected recovery, unmeasured')
    reg = load(root / current['current_science_registration']['path'])
    need(reg['source_ids'] == ['F011'] and reg['principal_originals_added'] == 1 and
         reg['previous_registration'] == old['current_science_registration'] and
         reg['measurement_originals_added'] == reg['new_question_credit'] == reg['new_Lean_declarations'] == 0,
         'registration roles and counts')
    need(len(reg['admissions']) == 1 and recovery['latest_admission_references'] == reg['admissions'],
         'one bound admission')
    bind(root, reg['admissions'][0])
    admission = load(root / reg['admissions'][0]['path'])
    need(admission['source_ids'] == ['F011'] and admission['physical_pages'] == [4, 4] and
         admission['source_routes'] == 22 and admission['source_pages'] == 10 and
         not admission['measured'] and not admission['comparison_topic_created'] and
         not admission['whole_source_formalized'] and not admission['theorem_sets_equivalent'] and
         admission['compression_factor'] is admission['software_inclusive_factor'] is None and
         admission['new_question_credit'] == admission['new_Lean_declarations'] == 0 and
         admission['required_mathematical_programs'] == [] and admission['source_software_cost'] is None,
         'complete corrected scientific scope')
    for key in ['author_manifest', 'distinct_root_review_manifest', 'source_contract', 'program_roles']:
        bind(root, admission[key])
    review = load(root / SCIENCE / 'root_review/review.json')
    need(review['status'] == 'ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and
         review['distinct_review'] and review['reviewer'] == 'root' and
         review['mathematical_author'] == 'enumeration_volume', 'distinct mathematical review')
    contract = load(root / admission['source_contract']['path'])
    need(contract['unresolved_principal'] == [] and len(contract['rows']) == 22 and
         contract['source_conjecture_status'] == 'RECORDED_UNANSWERED_NO_CURRENT_STATUS_CLAIM',
         'principal proof completion is not conjecture resolution')
    plan = load(root / AUDIT / 'copy_plan.json')['files']
    need(len(plan) == len({r['public_path'] for r in plan}) == 18, '18 complete payload files')
    for row in plan:
        bind(root, dict(path=row['public_path'], bytes=row['bytes'], sha256=row['sha256']))
        need(not row['public_path'].endswith('.md'), 'no public Markdown')
    for role, exports in [('author', 13), ('root_review', 3)]:
        manifest = load(root / SCIENCE / role / 'manifest.json')
        mapped = {r['logical_path']: r for r in plan if r['packet'] == role}
        need(len(manifest['exports']) == exports and
             set(mapped) == {'manifest.json'} | {r['path'] for r in manifest['exports']}, 'whole packet closure')
        for row in manifest['exports']:
            need(all(row[k] == mapped[row['path']][k] for k in ['bytes', 'sha256']), 'frozen payload identity')
    papers = load(root / 'papers/latest_catalogue.json')
    oldpapers = load(root / history['papers/latest_catalogue.json']['path'])
    for key in oldpapers:
        if key not in ['active_source_catalogue', 'corrected_unmeasured_scientific_catalogue']:
            need(papers[key] == oldpapers[key], 'old papers and measured boundary unchanged')
    need(papers['active_source_catalogue'] == current['active_catalogue'], 'catalogue agreement')
    bind(root, papers['corrected_unmeasured_scientific_catalogue'])
    scientific = load(root / papers['corrected_unmeasured_scientific_catalogue']['path'])
    oldscientific = load(root / history['papers/catalogue_corrected_unmeasured.json']['path'])
    need(scientific['entries'][:-2] == oldscientific['entries'] and
         scientific['acquired_dependencies'] == oldscientific['acquired_dependencies'] and
         scientific['original_ids'] == oldscientific['original_ids'] + ['F011'] and
         scientific['existing_comparison_topic_count'] == 19 and scientific['new_measurements'] == 0,
         'two additive documents, no measurements')
    from pypdf import PdfReader
    for row, identity in zip(scientific['entries'][-2:], ['F011_U', 'F011_A']):
        need(row['id'] == identity and row['source_ids'] == ['F011'] and row['compiler'] == 'pdflatex' and
             row['physical_pages'] == len(PdfReader(root / row['pdf']).pages) == 4 and
             row['admission'] == reg['admissions'][0] and row['compression_factor'] is None,
             'whole native document')
        need(re.search(r'\\title\{([^{}]+)\}', (root / row['tex']).read_text()).group(1) == row['title'],
             'literal title')
    def functions(path):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(path.read_text()).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name != 'main'}
    old_functions = functions(root / history['scripts/verify_snapshot.py']['path'])
    now_functions = functions(root / 'scripts/verify_snapshot.py')
    need(len(old_functions) == 139 and all(now_functions.get(k) == v for k, v in old_functions.items()),
         'all139 earlier verifier functions exact')
    readme = (root / 'README.rst').read_text()
    need('57 accessible originals' in readme and '48 await mathematical recovery' in readme and
         'four (N014, L024, L102 and F011)' in readme, 'reader counts')
    protocol = (root / 'audit/protocol.tex').read_text()
    need('106=57' in protocol and 'recoveries}+48' in protocol, 'protocol counts')
    links = 0
    for name in ['README.rst', 'audit/completion.rst', 'papers/recoveries/F011/v1/PUBLICATION.rst']:
        for target in re.findall(r'<([^<>\n]+)>`_', (root / name).read_text()):
            if re.match(r'\w+://', target):
                continue
            need((root / Path(name).parent / target).exists(), 'reader link ' + target)
            links += 1
    if require_root:
        gate = load(root / AUDIT / 'root_integration.json')
        need(gate['status'] == 'ROOT_ACCEPTED_SCIENCE57_PUBLICATION' and gate['source_ids'] == ['F011'],
             'root integration acceptance')
        required = set(history) | {AUDIT+'/new_original_registration.json', AUDIT+'/copy_plan.json',
                                  SCIENCE+'/admission.json', 'scripts/check_science57.py',
                                  'scripts/check_science57_history.py', 'scripts/replay_science57.py'}
        need(required <= {r['path'] for r in gate['bindings']}, 'complete integration bindings')
        for row in gate['bindings']:
            bind(root, row)
    return dict(status='PASS_SCIENCE57', counts=dict(active=106, corrected_recoveries=57, measured=53,
                unmeasured=4, mathematical_pending=48, editorial=1), payload_files=18,
                old_verifier_functions=139, other_originals_preserved=105, checked_links=links,
                new_factors=0, new_question_credit=0, new_Lean=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--before-root', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.repo, require_root=not args.before_root), indent=2))
