"""Check the F001/N012 registration, scope, provenance and public evidence."""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import json

AUD = 'audit/science76/v1'
IDS = ['F001', 'N012']
TRANSPORT = {
    'F001': ('1d75ccdbdb7c351549893de0b0825d14b477d2d90d6a19868d40149904d0ec58', 520, 436, 19, 5),
    'N012': ('0bddf32d1440ea9e74ae0b9fcecd3fc8ca60ba47300d999236b6f41c1490be94', 239, 170, 18, 49),
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(root, name):
    return json.loads((root / name).read_text())


def bind(root, row):
    p = root / row['path']
    need(not Path(row['path']).is_absolute() and p.resolve().is_relative_to(root.resolve()), 'binding escapes public repository')
    need(p.is_file() and sha(p) == row.get('stored_sha256', row['sha256']), 'public binding changed: ' + row['path'])
    size = row.get('stored_bytes', row.get('bytes'))
    if size is not None:
        need(p.stat().st_size == size, 'public binding size changed')


def unique(values, expected, label):
    need(len(values) == len(set(values)) and set(values) == set(expected), label)


def semantics(current, old, admissions, scopes):
    unique(current['admitted_original_ids'], old['admitted_original_ids'] + IDS, 'only two unique recoveries added')
    need(len(current['admitted_original_ids']) == current['admitted_principal_originals'] == 76, '76 recoveries')
    unique(current['accessible_pending_original_ids'], set(old['accessible_pending_original_ids']) - set(IDS), 'only two pending removed')
    need(len(current['accessible_pending_original_ids']) == current['accessible_pending_complete_recovery'] == 28, '28 pending')
    unique(current['handled_mathematical_original_ids'], old['handled_mathematical_original_ids'] + IDS, 'two handled originals added')
    need(len(current['handled_mathematical_original_ids']) == current['handled_mathematical_originals'] == 77, '77 handled')
    for key in ('measurement_pending_original_ids', 'scientific_unmeasured_original_ids'):
        unique(current[key], old[key] + IDS, 'only two unmeasured originals added')
        need(len(current[key]) == 23, '23 unmeasured')
    for key in ('active_original_ids', 'archived_original_ids', 'measured_original_ids', 'added_measurements', 'current_topic_replacements', 'editorial_original_ids', 'refuted_principal_originals', 'refuted_principal_original_ids', 'principal_refutation_admissions', 'all_mathematical_originals_handled', 'all_original_proofs_recovered', 'all_conjectures_resolved', 'current_principal_disposition_registration'):
        need(current[key] == old[key], 'unchanged corpus, measurement or refutation: ' + key)
    need(current['currently_measured_originals'] == 53 and current['originals'] == 106 and current['editorial_originals'] == 1, 'fixed corpus')
    for orig in IDS:
        a = admissions[orig]
        need(a['source_ids'] == [orig] and a['principal_originals_added'] == 1 and a['whole_original_credit'] == 0, 'individual proposal awaits common root gate')
        need(a['complete_principal_contract_recovered'] and not a['all_original_assertions_claimed'], 'complete principal contract with explicit limitations')
        need(a['compression_factor'] is a['software_inclusive_factor'] is None and a['new_question_credit'] == a['new_Lean_declarations'] == a['new_measurements'] == 0 and not a['whole_source_formalized'] and not a['measured'], 'no new numerical, question or formal claim')
    f, n = admissions['F001'], admissions['N012']
    need(f['literal_principal_theorem_recovered'] and not n['literal_principal_theorem_recovered'], 'literal F001; corrected N012 principal scope')
    need(set(f['component_acceptance']) == {'odd_existence', 'negative_reflections', 'mixed_involutions', 'principal', 'auxiliary_correction'}, 'F001 component list')
    for name, chain in f['component_acceptance'].items():
        need(set(chain) == ({'author', 'distinct_review', 'root_adoption'} if name in ('odd_existence', 'negative_reflections') else {'author', 'distinct_review'}), 'F001 exact component review chain')
    need(set(n['component_acceptance']) == {'complete'} and set(n['component_acceptance']['complete']) == {'author', 'root_whole_review', 'distinct_component_reviews_acquired'} and n['component_acceptance']['complete']['distinct_component_reviews_acquired'], 'N012 whole assembly and distinct component reviews')
    for stem in ('integral', 'central_quotients', 'finite_H', 'quotient_completion'):
        need('corpus106_N012_' + stem + '_independent_review' in n['complete_acquired_proofs'] and 'corpus106_N012_' + stem + '_root_adoption' in n['complete_acquired_proofs'], 'N012 each new component reviewed and adopted')
    unique([r['id'] for r in scopes['F001']['rows']], ['P1', 'P1.E5', 'P1.E34', 'P1.EU', 'P1.B235', 'P1.B2U', 'P1.O345', 'P1.OU', 'P1.Q3', 'P1.LOW', 'A1', 'R1', 'Q1', 'E1'], 'F001 exact fourteen source routes')
    unique([r['id'] for r in scopes['N012']['rows']], ['N012.T2.2.1', 'N012.T3.2.1', 'N012.T3.2.2', 'N012.T3.3.1', 'N012.C3.3.1', 'N012.T4.2.1', 'N012.T4.2.2', 'N012.C4.2.1', 'N012.C4.2.2', 'N012.C4.2.3', 'N012.T4.3.1', 'N012.C4.3.1'], 'N012 twelve exact numbered claims')
    need(len(scopes['N012']['classification_tables']) == 2 and [len(t['rows']) for t in scopes['N012']['classification_tables']] == [6, 6], 'both complete N012 tables')
    need(f['finite_positive_subset_pairs'] == 4096 and f['q3_prefix_counts'] == [2, 13, 121, 20, 2] and f['q3_generating_markings'] == 0 and f['mixed_exact_identities'] == 53 and f['mixed_normalized_transitive_pairs'] == 16, 'F001 actual finite evidence')
    need(f['principal_immediate_pages'] == 20 and f['separate_auxiliary_correction_pages'] == 2 and f['physical_pages'] == 22 and 'Literal Lemma4.1 is false' in f['auxiliary_correction'], 'F001 principal and auxiliary scopes remain separate')
    need(n['physical_pages'] == 30 and n['new_physical_pages'] == 21 and n['reused_physical_pages'] == 9 and n['integral_exact_records'] == 57 and n['finite_H_polynomial_identities'] == 42 and n['finite_H_prime_word_length'] == 131, 'N012 exact evidence and inventory')
    need(n['corrected_numbered_claim'] == 'Corollary 4.2.1: full-centre quotient is PSL when e is even and the index-two extension when e is odd; type [4p,n] survives in both cases.', 'N012 centre correction required')


def verify(root, require_root=True):
    root = Path(root).resolve()
    history = load(root, AUD + '/history_routes.json')['routes']
    for row in history.values():
        bind(root, row)
    old = load(root, history['audit/corpus/latest.json']['path'])
    current = load(root, 'audit/corpus/latest.json')
    ads = {o: load(root, 'audit/recoveries/' + o + '/v1/admission.json') for o in IDS}
    scopes = {o: load(root, 'audit/recoveries/' + o + '/v1/scope_routes.json') for o in IDS}
    semantics(current, old, ads, scopes)
    for key in ('active_catalogue', 'snapshot', 'current_science_registration'):
        bind(root, current[key])
    need(load(root, current['snapshot']['path']) == {k: v for k, v in current.items() if k != 'snapshot'}, 'exact current snapshot')
    cat = load(root, current['active_catalogue']['path'])
    oldcat = load(root, old['active_catalogue']['path'])
    need(len(cat['entries']) == len(oldcat['entries']) == 106, 'fixed original catalogue')
    for before, after in zip(oldcat['entries'], cat['entries']):
        orig = before['original_id']
        if orig not in IDS:
            need(before == after, 'another original changed')
        else:
            need(set(before) == set(after), 'original schema unchanged')
            for key in set(before) - {'current_principal_recovery', 'next_obligation'}:
                need(before[key] == after[key], 'original historical data changed')
            recovery = after['current_principal_recovery']
            need(recovery['historical_admission_evidence'] == before['current_principal_recovery'] and recovery['principal_contract_admitted'] and not recovery['measured'] and recovery['literal_principal_theorem_recovered'] == ads[orig]['literal_principal_theorem_recovered'], 'recovery contract and historical evidence')
    reg = load(root, current['current_science_registration']['path'])
    need(reg['source_ids'] == IDS and reg['previous_registration'] == old['current_science_registration'] and reg['principal_originals_added'] == 2 and reg['measurement_originals_added'] == reg['new_question_credit'] == reg['new_Lean_declarations'] == reg['comparison_topics_added'] == 0 and reg['compression_factor'] is None and not reg['whole_source_formalized'], 'two-original registration with exact predecessor')
    need(len(reg['admissions']) == 2 and [r['path'] for r in reg['admissions']] == ['audit/recoveries/' + o + '/v1/admission.json' for o in IDS], 'exact admission pair')
    for row in reg['admissions']:
        bind(root, row)
    payload_counts = {}
    for orig in IDS:
        a = ads[orig]
        rec = 'audit/recoveries/' + orig + '/v1'
        for chain in a['component_acceptance'].values():
            for row in chain.values():
                if isinstance(row, dict):
                    bind(root, row)
        for key in ('source_routes', 'source_map', 'portable_report', 'portable_checker', 'portable_review', 'portable_transport'):
            bind(root, a[key])
        for row in load(root, a['portable_review']['path'])['bindings'].values():
            bind(root, row)
        for row in a['complete_acquired_proofs'].values():
            bind(root, row)
        if orig == 'N012':
            bind(root, a['editorial_delta'])
            bind(root, a['editorial_diff'])
        for entry in a['new_native_manuscripts']:
            bind(root, entry['tex'])
            bind(root, entry['pdf'])
        t = load(root, rec + '/transport.json')
        digest, logical, payloads, packets, sources = TRANSPORT[orig]
        need(sha(root / (rec + '/transport.json')) == a['portable_transport']['sha256'] == digest and t['logical_files'] == logical and len(t['packets']) == packets, 'complete exact transport')
        public = {r['public_path']: r for r in t['files'] if 'public_path' in r}
        for path, row in public.items():
            bind(root, dict(row, path=path))
        need(len(public) == payloads and len(t['files']) == logical and sum('public_path' not in r for r in t['files']) == sources and not t['private_mathematical_proof_fallback'], 'all mathematical payloads public; exact primary-source exceptions')
        payload_counts[orig] = len(public)
        replay = load(root, a['portable_report']['path'])
        need(replay['transport_sha256'] == digest and replay['logical_records'] == logical and replay['distinct_payloads'] == payloads and replay['acquired_packets'] == packets and not replay['source_content_reread'] and replay['whole_original_credit'] == 0, 'exact public restoration report')
        if orig == 'F001':
            need(replay['status'] == 'PASS_PUBLIC_F001_RESTORATION_AND_FINITE_PREMISES' and not replay['private_proof_fallback'] and replay['restored_files'] == 515 and replay['acquired_exports'] == 444 and [r['component'] for r in replay['checks']] == ['odd_existence', 'reflection_bound', 'mixed_bound', 'principal', 'rank_bound'] and all(r['report']['status'] == 'PASS' for r in replay['checks']), 'all five F001 mathematical/native checks')
        else:
            need(replay['status'] == 'PASS_PUBLIC_N012_RESTORATION_AND_CERTIFICATES' and not replay['private_runtime_fallback'] and not replay['retained_programs_patched'] and replay['restored_files'] == 190 and replay['acquired_exports'] == 160 and replay['principal_claims'] == replay['table_rows'] == 12 and replay['exact_editorial_diff'] and replay['integral']['displayed_matrix_and_orbit_records'] == 57 and replay['finite_H_polynomial_identities'] == 42 and replay['prime_word']['word_length'] == 131 and replay['prime_word']['status'] == 'PASS', 'all N012 claim routes and literal certificates')
    previous = load(root, history['papers/catalogue_corrected_unmeasured.json']['path'])
    native = load(root, 'papers/catalogue_corrected_unmeasured.json')
    need(native['entries'][:-12] == previous['entries'] and native['original_ids'] == previous['original_ids'] + IDS and native['existing_comparison_topic_count'] == 19 and native['new_measurements'] == 0, 'prior manuscripts and measurements unchanged')
    need([e['physical_pages'] for e in native['entries'][-12:]] == [2, 6, 4, 8, 2, 3, 5, 2, 7, 4, 6, 3], 'twelve complete immediate proof documents')
    expected_native = [p for o in IDS for p in ads[o]['new_native_manuscripts']]
    for actual, expected in zip(native['entries'][-12:], expected_native):
        need(actual['id'] == expected['id'] and actual['tex'] == expected['tex']['path'] and actual['pdf'] == expected['pdf']['path'] and not actual['measured'] and actual['compression_factor'] is None, 'exact native routes without a measurement')
    paper = load(root, 'papers/latest_catalogue.json')
    oldpaper = load(root, history['papers/latest_catalogue.json']['path'])
    need(set(paper) == set(oldpaper), 'prior paper routing schema')
    for k in set(oldpaper) - {'status', 'active_source_catalogue', 'corrected_unmeasured_scientific_catalogue'}:
        need(paper[k] == oldpaper[k], 'prior paper routing changed')
    need(paper['active_source_catalogue'] == current['active_catalogue'], 'current paper routing')
    bind(root, paper['corrected_unmeasured_scientific_catalogue'])
    oldtree = ast.parse((root / history['scripts/verify_snapshot.py']['path']).read_text())
    newtree = ast.parse((root / 'scripts/verify_snapshot.py').read_text())
    def functions(tree):
        return {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name != 'main'}
    oldf, newf = functions(oldtree), functions(newtree)
    need(all(newf.get(k) == v for k, v in oldf.items()), 'old verifier functions changed')
    added = {'check_previous_science76', 'check_science76'}
    need(set(newf) - set(oldf) == added, 'only two new verifier functions')
    def preserved_nodes(tree, exclusions):
        return [ast.dump(n, include_attributes=False) for n in tree.body if not (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in exclusions)]
    need(preserved_nodes(oldtree, {'main'}) == preserved_nodes(newtree, {'main'} | added), 'all other top-level code preserved')
    controls = []
    edits = [
        ('duplicate original', lambda c, a, s: c['admitted_original_ids'].append('F001')),
        ('extra pending removed', lambda c, a, s: c['accessible_pending_original_ids'].pop()),
        ('invent factor', lambda c, a, s: a['F001'].update(compression_factor=2)),
        ('auxiliary overclaim', lambda c, a, s: a['F001'].update(all_original_assertions_claimed=True)),
        ('missing F001 route', lambda c, a, s: s['F001']['rows'].pop()),
        ('missing N012 route', lambda c, a, s: s['N012']['rows'].pop()),
        ('missing table row', lambda c, a, s: s['N012']['classification_tables'][0]['rows'].pop()),
        ('missing mixed review', lambda c, a, s: a['F001']['component_acceptance']['mixed_involutions'].pop('distinct_review')),
        ('missing quotient review', lambda c, a, s: a['N012']['complete_acquired_proofs'].pop('corpus106_N012_quotient_completion_independent_review')),
        ('uncorrected N012', lambda c, a, s: a['N012'].update(literal_principal_theorem_recovered=True)),
        ('lost centre correction', lambda c, a, s: a['N012'].update(corrected_numbered_claim='none')),
    ]
    for label, edit in edits:
        c, a, s = copy.deepcopy((current, ads, scopes))
        edit(c, a, s)
        try:
            semantics(c, old, a, s)
        except (ValueError, KeyError):
            controls.append(label)
        else:
            raise ValueError('invalid registration accepted: ' + label)
    if require_root:
        gate = load(root, AUD + '/root_integration.json')
        need(gate['status'] == 'ROOT_ACCEPTED_SCIENCE76_PUBLICATION' and gate['source_ids'] == IDS and gate['whole_original_credit'] == 2 and gate['new_question_credit'] == gate['new_Lean_declarations'] == gate['new_measurements'] == 0 and gate['compression_factor'] is None, 'root publication gate supplies exact final credit')
        for row in gate['bindings']:
            bind(root, row)
        need(load(root, AUD + '/registration_review/review.json')['status'] == 'ACCEPTED_F001_N012_REGISTRATION', 'distinct registration review')
    return dict(status='PASS_SCIENCE76_PUBLICATION', counts=dict(active=106, corrected_recoveries=76, refuted=1, handled=77, measured=53, unmeasured=23, mathematical_pending=28, editorial=1, archived=55, comparison_topics=19), source_ids=IDS, old_verifier_functions_preserved=len(oldf), public_payloads=payload_counts, controls=controls)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--preflight', action='store_true')
    a = p.parse_args()
    print(json.dumps(verify(a.repo, require_root=not a.preflight)))
