"""Read-only semantic and exact-content audit of the L115 registration proposal."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import subprocess
from pypdf import PdfReader
import pack_codec as codec
from prior_transport_reader import Archive

if not __debug__:
    raise SystemExit('ordinary Python required')
P = Path(__file__).resolve().parent
R = Path('/Users/sasha/medusa/math_compression')
C = P / 'registration_candidate02'
N = C / 'proposed'
AUD = 'audit/principal-refutations/L115/complete/v1'


def load(path):
    return json.loads(path.read_text())


def need(ok, message):
    if not ok:
        raise ValueError(message)


def pin(path, base=None):
    size, digest = codec.digest_file(path)
    return dict(path=str(path.relative_to(base) if base else path), bytes=size, sha256=digest)


def semantic(old, new, admission):
    preserved = ['admitted_principal_originals', 'admitted_original_ids', 'refuted_principal_originals',
                 'refuted_principal_original_ids', 'handled_mathematical_originals', 'handled_mathematical_original_ids',
                 'currently_measured_originals', 'measured_original_ids', 'scientific_unmeasured_original_ids',
                 'measurement_pending_original_ids', 'accessible_pending_original_ids', 'accessible_pending_complete_recovery',
                 'current_science_registration', 'current_principal_disposition_registration']
    for key in preserved:
        need(new[key] == old[key], 'changed preserved field: ' + key)
    need(new['fully_treated_original_ids'] == sorted(old['fully_treated_original_ids'] + ['L115']), 'exact fully treated set')
    need(len(set(new['fully_treated_original_ids'])) == new['fully_treated_originals'] == 98, 'fully treated count')
    need(new['source_complete_refutation_original_ids'] == sorted(old['source_complete_refutation_original_ids'] + ['L115']) and new['source_complete_refutation_originals'] == 6,
         'only L115 completed after refutation')
    need(new['surviving_claim_obligation_original_ids'] == [x for x in old['surviving_claim_obligation_original_ids'] if x != 'L115'], 'only L115 leaves surviving claims')
    need(len(new['surviving_claim_obligation_original_ids']) == new['surviving_claim_obligation_originals'] == 3, 'surviving count')
    need(new['completion_obligation_original_ids'] == [x for x in old['completion_obligation_original_ids'] if x != 'L115'], 'only L115 leaves all obligations')
    need(len(new['completion_obligation_original_ids']) == new['completion_obligation_originals'] == 7, 'outstanding count')
    need(set(new['completion_obligation_original_ids']) == set(new['surviving_claim_obligation_original_ids']) | set(new['accessible_pending_original_ids']), 'exact outstanding partition')
    need(set(new['fully_treated_original_ids']).isdisjoint(new['completion_obligation_original_ids']), 'completed and outstanding disjoint')
    need(len(set(new['fully_treated_original_ids']) | set(new['completion_obligation_original_ids'])) == 105, 'all mathematical originals accounted once')
    need(admission['source_ids'] == ['L115'] and admission['proposed_source_completion_credit'] == 1, 'one source completion')
    for key in ['ordinary_recovery_credit', 'principal_refutation_credit', 'new_original_credit', 'new_measurements', 'new_question_credit', 'new_Lean_credit']:
        need(admission[key] == 0, 'unearned credit: ' + key)
    need(not admission['whole_source_formalized'] and admission['compression_factor'] is None, 'no unsupported formalization or factor')
    need(admission['unresolved_asserted_claims'] == [] and admission['source_claim_rows'] == 70, 'all 70 asserted-source dispositions')
    need(admission['complete_proof_collection']['physical_pages'] == 36 and admission['complete_proof_collection']['manuscripts'] == 8, 'eight complete manuscripts, 36 pages')


def operational_boundary(mapping, transport):
    expected = transport['premises']
    need(mapping['premises'] == expected, 'same documentary/environment premises as accepted stage')
    by_hash = {r['sha256']: r for r in expected}
    need(len(expected) == len(by_hash) == 2583, 'exact2583 premise objects')
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
            need((original['path'], original['sha256'], original['bytes']) not in allowed_occurrences,
                 'exact documentary occurrence cannot have a physical publication route')
            need(original['sha256'] not in by_hash or original['bytes'] == 0,
                 'only independently generated empty operational logs may share documentary content')
            if 'transport_object' in route:
                need(set(route) == {'original', 'transport_object'}, 'one exact scientific transport route')
                ref = route['transport_object']
                need(set(ref) == {'transport', 'sha256', 'bytes'}, 'complete content-addressed route')
                need(ref['transport'] == mapping['accepted_content_transport'], 'same accepted content transport')
                need((ref['bytes'], ref['sha256']) == (original['bytes'], original['sha256']), 'same exact decoded content')
                obj = transport['objects'].get(ref['sha256'])
                need(obj is not None and obj['kind'] in ['NEW_PACKED_EXACT_CONTENT', 'EXISTING_PUBLIC'], 'existing accessible scientific payload')
                need((obj['bytes'], obj['sha256']) == (ref['bytes'], ref['sha256']), 'exact transport object identity')
            else:
                need(set(route) == {'original', 'public'}, 'one physical public route')
    need(used == set(by_hash), 'all and only2583 operational premises')
    return by_hash


def boundary_controls(mapping, transport):
    rejected = []
    for name in ['missing_source_premise', 'source_given_public_route', 'changed_source_locator', 'changed_transport_pin', 'changed_object_hash', 'source_as_object', 'two_routes']:
        bad = copy.deepcopy(mapping)
        if name == 'missing_source_premise':
            bad['premises'].pop()
        elif name == 'source_given_public_route':
            row = next(r for r in bad['routes'] if 'premise' in r)
            row['public'] = dict(path='forbidden.pdf', bytes=row['original']['bytes'], sha256=row['original']['sha256'])
            del row['premise']
        elif name == 'changed_source_locator':
            row = next(r for r in bad['routes'] if 'premise' in r)
            row['original']['path'] += '.changed'
        else:
            row = next(r for r in bad['routes'] if 'transport_object' in r)
            if name == 'changed_transport_pin': row['transport_object']['transport'] = dict(row['transport_object']['transport'], sha256='0' * 64)
            elif name == 'changed_object_hash': row['transport_object']['sha256'] = '0' * 64
            elif name == 'source_as_object':
                row = next(r for r in bad['routes'] if 'premise' in r and r['original']['bytes'] > 0)
                row['transport_object'] = dict(transport=bad['accepted_content_transport'], sha256=row['original']['sha256'], bytes=row['original']['bytes'])
                del row['premise']
            else: row['public'] = dict(path='also.json', bytes=0, sha256='0' * 64)
        try:
            operational_boundary(bad, transport)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted changed documentary boundary')
    return rejected


def main():
    need(len(sys.argv) == 1, 'no unbound inputs')
    need(subprocess.check_output(['git', '-C', str(R), 'rev-parse', 'HEAD'], text=True).strip() == 'de093380caee98006f8175ef7f8b4d760ca18b2e', 'exact accepted predecessor')
    need(not subprocess.check_output(['git', '-C', str(R), 'status', '--porcelain']).strip(), 'public predecessor untouched')
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
            need(before['original_id'] == after['original_id'] == 'L115', 'no other source changed')
            need({k: v for k, v in after.items() if k not in ['current_source_completion', 'next_obligation']} ==
                 {k: v for k, v in before.items() if k != 'next_obligation'}, 'only additive source completion and next obligation')
            changed.append('L115')
    need(changed == ['L115'], 'exact one source entry changed')
    native_old = load(R / 'papers/catalogue_principal_refutations.json')
    native_new = load(N / 'papers/catalogue_principal_refutations.json')
    need(native_old['original_ids'] == native_new['original_ids'] and len(native_old['entries']) == len(native_new['entries']), 'no duplicate original or native principal entry')
    for before, after in zip(native_old['entries'], native_new['entries']):
        if before != after:
            need(before['source_ids'] == after['source_ids'] == ['L115'], 'only L115 native supplement')
            need({k: v for k, v in after.items() if k != 'source_completion'} == before, 'principal native entry unchanged')
    changed_global = {k for k in old.keys() | new.keys() if old.get(k) != new.get(k)}
    declared = set(load(C / 'machine_delta.json')) | {'snapshot', 'previous_snapshot', 'active_catalogue', 'current_source_completion_registration'}
    need(changed_global == declared, 'exact global machine delta only')
    mapping = load(N / AUD / 'operational/mapping.json')
    transport = load(P / 'stage02' / AUD / 'transport.json')
    premise_by_hash = operational_boundary(mapping, transport)
    routes = mapping['routes']
    transport_pin = pin(P / 'stage02' / AUD / 'transport.json', P / 'stage02')
    need(mapping['accepted_content_transport'] == transport_pin and transport_pin['sha256'] == '18c9b0c7e72ac7da589afb1f2a07b1eefe3f066d412a7bc9a77143f40b19660f', 'root-accepted exact transport')
    archive = Archive(P / 'stage02', R, transport)
    def public_path(record):
        codec.relative(record['path'])
        candidates = [base / record['path'] for base in [N, P / 'stage02', R] if (base / record['path']).is_file()]
        need(candidates, 'available declared public file')
        for path in candidates:
            need(codec.digest_file(path) == (record['bytes'], record['sha256']), 'identical public overlay bytes')
        return candidates[0]
    verified = set()
    for row in routes:
        need(pin(Path(row['original']['path'])) == row['original'], 'unchanged accepted operational evidence')
        if 'premise' in row:
            continue
        if 'transport_object' in row:
            ref = row['transport_object']; h = ref['sha256']
            if h not in verified:
                obj = archive.objects[h]
                codec.verify(obj, [R] if obj['kind'] == 'EXISTING_PUBLIC' else [P / 'stage02'])
                verified.add(h)
        else:
            need((row['public']['bytes'], row['public']['sha256']) == (row['original']['bytes'], row['original']['sha256']), 'physical route preserves exact original content')
            public_path(row['public'])
    original_manifest = mapping['original_manifest']
    need(original_manifest['sha256'] == '4ed33f290c04e0fe9ee06926a12b0b65469adf85be7f12da3bb7974cc8f878ae', 'root operational authority')
    authority = load(Path(original_manifest['path']))
    need(authority['status'] == mapping['original_status'] == 'ACCEPTED_L115_PORTABLE_COMPLETE_SOURCE_TREATMENT', 'root acceptance status')
    expected = load(Path(original_manifest['path']).parent / 'dependencies.json') + [dict(r, path=str(Path(original_manifest['path']).parent / r['path'])) for r in authority['exports']] + [original_manifest]
    bound = {}
    for row in expected:
        need(row['path'] not in bound or bound[row['path']] == row, 'consistent root aliases'); bound[row['path']] = row
    need(len(routes) == len({row['original']['path'] for row in routes}) and {row['original']['path']: row['original'] for row in routes} == bound, 'every operational dependency acquired exactly once')
    for key in ['mathematical_acceptance', 'portable_acceptance', 'operational_mapping', 'stage_manifest', 'transport', 'portable_checker', 'source_claim_ledger']:
        public_path(admission[key])
    need(load(public_path(admission['source_claim_ledger']))['unresolved_asserted_claims'] == [], 'same accepted complete claim ledger')
    manuscripts = admission['manuscripts']; total = reused = 0
    need(len(manuscripts) == len({r['id'] for r in manuscripts}) == 8, 'eight unique whole manuscripts')
    for row in manuscripts:
        public_path(row['tex']); pdf = public_path(row['pdf'])
        pages = len(PdfReader(pdf).pages); need(pages == row['physical_pages'], 'actual complete native pages'); total += pages
        if row['existing_principal_manuscript_reused']:
            need(row['id'] == 'L115-scalar_subspaces' and pages == 4, 'only previously counted principal proof'); reused += pages
            before = next(e for e in native_old['entries'] if e['source_ids'] == ['L115'])
            for kind in ['tex', 'pdf']: need(pin(R / before[kind])['sha256'] == row[kind]['sha256'], 'principal proof exact bytes retained')
    need(total == 36 and reused == 4 and admission['complete_proof_collection']['additional_manuscript_pages'] == 32 and not admission['complete_proof_collection']['merged_volume_claimed'], 'complete collection without duplicate principal charge or fabricated merged PDF')
    public_path(admission['complete_proof_collection']['manifest'])
    need(not list(N.rglob('*.md')), 'new Markdown files remain private')
    for path in N.rglob('*'):
        if path.is_file():
            need(path.stat().st_size == 0 or pin(path)['sha256'] not in premise_by_hash, 'nonempty source documentary bytes must not be published')
    for row in load(C / 'narrative_changes.json'):
        need(pin(R / row['path'], R) == row['before'] and pin(N / row['path'], N) == row['after'], 'exact narrative delta')
    damaged = []
    for name, mutate in [('extra_recovery', lambda x: x.update(admitted_principal_originals=93)),
                         ('measured_id_removed', lambda x: x['measured_original_ids'].pop()),
                         ('wrong_closed_source', lambda x: x.update(source_complete_refutation_original_ids=['L115'])),
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
    print(json.dumps(dict(status='PASS_L115_REGISTRATION_CANDIDATE', fully_treated=98, ordinary_recoveries=92,
        principal_refutations=9, principal_dispositions=101, measured=53, unmeasured_recoveries=39,
        surviving_refuted_sources=3, undisposed_originals=4, outstanding=7, operational_bindings=len(routes), decoded_operational_objects=len(verified), complete_proof_pages=total, complete_manuscripts=len(manuscripts),
        damage_controls=damaged, documentary_controls=boundary_controls(mapping, transport), operational_premise_objects=2583, public_mutations=0)))


if __name__ == '__main__':
    main()
