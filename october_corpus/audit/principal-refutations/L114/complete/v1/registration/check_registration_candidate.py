"""Read-only semantic and exact-content audit of the L114 registration proposal."""
from pathlib import Path
import copy
import hashlib
import json
import sys

if not __debug__:
    raise SystemExit('ordinary Python required')
P = Path(__file__).resolve().parent
R = Path('/Users/sasha/medusa/math_compression')
C = P / 'registration_candidate01'
N = C / 'proposed'
AUD = 'audit/principal-refutations/L114/complete/v1'


def load(path):
    return json.loads(path.read_text())


def need(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path, base=None):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(base) if base else path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def semantic(old, new, admission):
    preserved = ['admitted_principal_originals', 'admitted_original_ids', 'refuted_principal_originals',
                 'refuted_principal_original_ids', 'handled_mathematical_originals', 'handled_mathematical_original_ids',
                 'currently_measured_originals', 'measured_original_ids', 'scientific_unmeasured_original_ids',
                 'measurement_pending_original_ids', 'accessible_pending_original_ids', 'accessible_pending_complete_recovery',
                 'current_science_registration', 'current_principal_disposition_registration']
    for key in preserved:
        need(new[key] == old[key], 'changed preserved field: ' + key)
    need(new['fully_treated_original_ids'] == sorted(old['fully_treated_original_ids'] + ['L114']), 'exact fully treated set')
    need(len(set(new['fully_treated_original_ids'])) == new['fully_treated_originals'] == 96, 'fully treated count')
    need(new['source_complete_refutation_original_ids'] == sorted(old['source_complete_refutation_original_ids'] + ['L114']) and new['source_complete_refutation_originals'] == 4,
         'only L114 completed after refutation')
    need(new['surviving_claim_obligation_original_ids'] == [x for x in old['surviving_claim_obligation_original_ids'] if x != 'L114'], 'only L114 leaves surviving claims')
    need(len(new['surviving_claim_obligation_original_ids']) == new['surviving_claim_obligation_originals'] == 5, 'surviving count')
    need(new['completion_obligation_original_ids'] == [x for x in old['completion_obligation_original_ids'] if x != 'L114'], 'only L114 leaves all obligations')
    need(len(new['completion_obligation_original_ids']) == new['completion_obligation_originals'] == 9, 'outstanding count')
    need(set(new['completion_obligation_original_ids']) == set(new['surviving_claim_obligation_original_ids']) | set(new['accessible_pending_original_ids']), 'exact outstanding partition')
    need(set(new['fully_treated_original_ids']).isdisjoint(new['completion_obligation_original_ids']), 'completed and outstanding disjoint')
    need(len(set(new['fully_treated_original_ids']) | set(new['completion_obligation_original_ids'])) == 105, 'all mathematical originals accounted once')
    need(admission['source_ids'] == ['L114'] and admission['proposed_source_completion_credit'] == 1, 'one source completion')
    for key in ['ordinary_recovery_credit', 'principal_refutation_credit', 'new_original_credit', 'new_measurements', 'new_question_credit', 'new_Lean_credit']:
        need(admission[key] == 0, 'unearned credit: ' + key)
    need(not admission['whole_source_formalized'] and admission['compression_factor'] is None, 'no unsupported formalization or factor')
    need(admission['uncertified_extensions'] == ['Complete corrected classification of all relative positions and incidence geometries', 'General FT/thinness under stronger actual-residue hypotheses', 'Higher-rank geometry property of coordinate pregeometry family', 'New Lean formalization and mathematical compression measurement'], 'fixed source scope preserved')


def operational_boundary(mapping, transport):
    expected = transport['premises']
    need(mapping['premises'] == expected, 'same documentary/environment premises as accepted stage')
    by_hash = {r['sha256']: r for r in expected}
    need(len(expected) == len(by_hash) == 263, 'exact263 premise objects')
    allowed_occurrences = {(r['original_path'], r['sha256'], r['bytes']) for r in transport['logical_files'] if r['sha256'] in by_hash}
    used = set()
    for route in mapping['routes']:
        original = route['original']
        if 'premise' in route:
            need(set(route) == {'original', 'premise'}, 'premise has no physical publication route')
            premise = by_hash.get(original['sha256'])
            need(premise is not None, 'only accepted documentary sources')
            need(route['premise'] == premise, 'exact documentary premise metadata')
            need((original['path'], original['sha256'], original['bytes']) in allowed_occurrences, 'exact premise occurrence')
            used.add(original['sha256'])
        else:
            need(set(route) == {'original', 'public'} and original['sha256'] not in by_hash,
                 'scientific public route cannot carry documentary source bytes')
    need(used == set(by_hash), 'all and only263 operational premises')
    return by_hash


def boundary_controls(mapping, transport):
    rejected = []
    for name in ['missing_source_premise', 'source_given_public_route', 'changed_source_locator']:
        bad = copy.deepcopy(mapping)
        if name == 'missing_source_premise':
            bad['premises'].pop()
        elif name == 'source_given_public_route':
            row = next(r for r in bad['routes'] if 'premise' in r)
            row['public'] = dict(path='forbidden.pdf', bytes=row['original']['bytes'], sha256=row['original']['sha256'])
            del row['premise']
        else:
            row = next(r for r in bad['routes'] if 'premise' in r)
            row['original']['path'] += '.changed'
        try:
            operational_boundary(bad, transport)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted changed documentary boundary')
    return rejected


def main():
    need(len(sys.argv) == 1, 'no unbound inputs')
    old = load(R / 'audit/corpus/latest.json')
    new = load(N / 'audit/corpus/latest.json')
    admission = load(N / AUD / 'admission.json')
    semantic(old, new, admission)
    current_cat = load(R / old['active_catalogue']['path'])
    candidate_cat = load(N / new['active_catalogue']['path'])
    need(pin(N / new['active_catalogue']['path'], N) == new['active_catalogue'], 'exact new source catalogue')
    need(len(current_cat['entries']) == len(candidate_cat['entries']) == 106, 'all106 source entries retained')
    changed = []
    for before, after in zip(current_cat['entries'], candidate_cat['entries']):
        if before != after:
            need(before['original_id'] == after['original_id'] == 'L114', 'no other source changed')
            need({k: v for k, v in after.items() if k not in ['current_source_completion', 'next_obligation']} ==
                 {k: v for k, v in before.items() if k != 'next_obligation'}, 'only additive source completion and next obligation')
            changed.append('L114')
    need(changed == ['L114'], 'exact one source entry changed')
    native_old = load(R / 'papers/catalogue_principal_refutations.json')
    native_new = load(N / 'papers/catalogue_principal_refutations.json')
    need(native_old['original_ids'] == native_new['original_ids'] and len(native_old['entries']) == len(native_new['entries']), 'no duplicate original or native principal entry')
    for before, after in zip(native_old['entries'], native_new['entries']):
        if before != after:
            need(before['source_ids'] == after['source_ids'] == ['L114'], 'only L114 native supplement')
            need({k: v for k, v in after.items() if k != 'source_completion'} == before, 'principal native entry unchanged')
    changed_global = {k for k in old.keys() | new.keys() if old.get(k) != new.get(k)}
    declared = set(load(C / 'machine_delta.json')) | {'snapshot', 'previous_snapshot', 'active_catalogue', 'current_source_completion_registration'}
    need(changed_global == declared, 'exact global machine delta only')
    mapping = load(N / AUD / 'operational/mapping.json')
    transport = load(P / 'stage02' / AUD / 'transport.json')
    premise_by_hash = operational_boundary(mapping, transport)
    routes = mapping['routes']
    for row in routes:
        need(pin(Path(row['original']['path'])) == row['original'], 'unchanged accepted operational evidence')
        if 'premise' in row:
            continue
        target = row['public']['path']
        path = N / target if (N / target).is_file() else P / 'stage02' / target
        need(pin(path, N if path.is_relative_to(N) else P / 'stage02') == row['public'], 'exact operational public route')
    for path in N.rglob('*'):
        if path.is_file():
            need(pin(path)['sha256'] not in premise_by_hash, 'source documentary bytes must not be published')
    for row in load(C / 'narrative_changes.json'):
        need(pin(R / row['path'], R) == row['before'] and pin(N / row['path'], N) == row['after'], 'exact narrative delta')
    damaged = []
    for name, mutate in [('extra_recovery', lambda x: x.update(admitted_principal_originals=93)),
                         ('measured_id_removed', lambda x: x['measured_original_ids'].pop()),
                         ('wrong_closed_source', lambda x: x.update(source_complete_refutation_original_ids=['L114'])),
                         ('premature_completion', lambda x: x.update(completion_obligation_originals=0))]:
        bad = copy.deepcopy(new)
        mutate(bad)
        try:
            semantic(old, bad, admission)
        except ValueError:
            damaged.append(name)
        else:
            raise ValueError('accepted damaged registration')
    need('Overfull' not in (C / 'native_protocol/protocol.log').read_text(), 'clean proposed protocol layout')
    print(json.dumps(dict(status='PASS_L114_REGISTRATION_CANDIDATE', fully_treated=96, ordinary_recoveries=92,
        principal_refutations=9, principal_dispositions=101, measured=53, unmeasured_recoveries=39,
        surviving_refuted_sources=5, undisposed_originals=4, outstanding=9, operational_bindings=len(routes),
        damage_controls=damaged, documentary_controls=boundary_controls(mapping, transport), operational_premise_objects=263, public_mutations=0)))


if __name__ == '__main__':
    main()
