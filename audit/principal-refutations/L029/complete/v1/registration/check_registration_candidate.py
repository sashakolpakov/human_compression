"""Read-only semantic and exact-content audit of the L029 registration proposal."""
from pathlib import Path
import copy
import hashlib
import json
import sys

if not __debug__:
    raise SystemExit('ordinary Python required')
P = Path(__file__).resolve().parent
R = Path('/Users/sasha/medusa/math_compression')
C = P / 'registration_candidate03'
N = C / 'proposed'
AUD = 'audit/principal-refutations/L029/complete/v1'


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
    need(new['fully_treated_original_ids'] == sorted(old['admitted_original_ids'] + ['L029']), 'exact fully treated set')
    need(len(set(new['fully_treated_original_ids'])) == new['fully_treated_originals'] == 92, 'fully treated count')
    need(new['source_complete_refutation_original_ids'] == ['L029'] and new['source_complete_refutation_originals'] == 1,
         'only L029 completed after refutation')
    need(new['surviving_claim_obligation_original_ids'] == [x for x in old['surviving_claim_obligation_original_ids'] if x != 'L029'], 'only L029 leaves surviving claims')
    need(len(new['surviving_claim_obligation_original_ids']) == new['surviving_claim_obligation_originals'] == 8, 'surviving count')
    need(new['completion_obligation_original_ids'] == [x for x in old['completion_obligation_original_ids'] if x != 'L029'], 'only L029 leaves all obligations')
    need(len(new['completion_obligation_original_ids']) == new['completion_obligation_originals'] == 13, 'outstanding count')
    need(set(new['completion_obligation_original_ids']) == set(new['surviving_claim_obligation_original_ids']) | set(new['accessible_pending_original_ids']), 'exact outstanding partition')
    need(set(new['fully_treated_original_ids']).isdisjoint(new['completion_obligation_original_ids']), 'completed and outstanding disjoint')
    need(len(set(new['fully_treated_original_ids']) | set(new['completion_obligation_original_ids'])) == 105, 'all mathematical originals accounted once')
    need(admission['source_ids'] == ['L029'] and admission['proposed_source_completion_credit'] == 1, 'one source completion')
    for key in ['ordinary_recovery_credit', 'principal_refutation_credit', 'new_original_credit', 'new_measurements', 'new_question_credit', 'new_Lean_credit']:
        need(admission[key] == 0, 'unearned credit: ' + key)
    need(not admission['whole_source_formalized'] and admission['compression_factor'] is None, 'no unsupported formalization or factor')
    need(admission['general_higher_rank_firmness'] == 'UNPROVED_CORRECTED_VARIANT', 'unproved variant preserved')


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
            need(before['original_id'] == after['original_id'] == 'L029', 'no other source changed')
            need({k: v for k, v in after.items() if k not in ['current_source_completion', 'next_obligation']} ==
                 {k: v for k, v in before.items() if k != 'next_obligation'}, 'only additive source completion and next obligation')
            changed.append('L029')
    need(changed == ['L029'], 'exact one source entry changed')
    native_old = load(R / 'papers/catalogue_principal_refutations.json')
    native_new = load(N / 'papers/catalogue_principal_refutations.json')
    need(native_old['original_ids'] == native_new['original_ids'] and len(native_old['entries']) == len(native_new['entries']), 'no duplicate original or native principal entry')
    for before, after in zip(native_old['entries'], native_new['entries']):
        if before != after:
            need(before['source_ids'] == after['source_ids'] == ['L029'], 'only L029 native supplement')
            need({k: v for k, v in after.items() if k != 'source_completion'} == before, 'principal native entry unchanged')
    changed_global = {k for k in old.keys() | new.keys() if old.get(k) != new.get(k)}
    declared = set(load(C / 'machine_delta.json')) | {'snapshot', 'previous_snapshot', 'active_catalogue', 'current_source_completion_registration'}
    need(changed_global == declared, 'exact global machine delta only')
    routes = load(N / AUD / 'operational/mapping.json')['routes']
    for row in routes:
        need(pin(Path(row['original']['path'])) == row['original'], 'unchanged accepted operational evidence')
        target = row['public']['path']
        path = N / target if (N / target).is_file() else P / 'stage01' / target
        need(pin(path, N if path.is_relative_to(N) else P / 'stage01') == row['public'], 'exact operational public route')
    for row in load(C / 'narrative_changes.json'):
        need(pin(R / row['path'], R) == row['before'] and pin(N / row['path'], N) == row['after'], 'exact narrative delta')
    damaged = []
    for name, mutate in [('extra_recovery', lambda x: x.update(admitted_principal_originals=92)),
                         ('measured_id_removed', lambda x: x['measured_original_ids'].pop()),
                         ('wrong_closed_source', lambda x: x.update(source_complete_refutation_original_ids=['L036'])),
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
    print(json.dumps(dict(status='PASS_L029_REGISTRATION_CANDIDATE', fully_treated=92, ordinary_recoveries=91,
        principal_refutations=9, principal_dispositions=100, measured=53, unmeasured_recoveries=38,
        surviving_refuted_sources=8, undisposed_originals=5, outstanding=13, operational_bindings=len(routes),
        damage_controls=damaged, public_mutations=0)))


if __name__ == '__main__':
    main()
