"""Check one complete source supplement against its accepted predecessor."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path, PurePosixPath
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import subprocess

AUD = 'audit/principal-refutations/L115/complete/v1'
BASELINE = 'de093380caee98006f8175ef7f8b4d760ca18b2e'
CANDIDATE_SHA = '63c4ec8b8ba2b429451fbbec09f8149475c4ab52006f26e37d4bc52c4022dce7'
MATH_SHA = '1f7e2e6b2954d60b7af9c5a1a16261a78065d87b2a0828547afcf97a86b91fb3'
PORTABLE_SHA = '4ed33f290c04e0fe9ee06926a12b0b65469adf85be7f12da3bb7974cc8f878ae'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(2**20), b''):
            h.update(chunk)
    return h.hexdigest()


def pin(path, base):
    return dict(path=str(path.relative_to(base)), bytes=path.stat().st_size, sha256=sha(path))


def safe(root, name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.parts and '..' not in p.parts and str(p) == name, 'Safe relative path')
    path = root.joinpath(*p.parts)
    need(not any(x.is_symlink() for x in [path, *path.parents] if x != root.parent), 'No symlink path')
    return path


def bind(root, row):
    path = safe(root, row['path'])
    need(path.is_file() and pin(path, root) == row, 'Exact bytes: ' + row['path'])
    return path


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def changed_paths(root):
    names = set(git(root, 'diff', '--name-only', '-z', BASELINE, '--').decode().split('\0'))
    names |= set(git(root, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
    names.discard('')
    return sorted(names)


def verifier_delta(old):
    tree = ast.parse(old)
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    lines = old.splitlines(keepends=True)
    replacement = '''def check_L115_completion():
    spec=importlib.util.spec_from_file_location('L115_completion',ROOT/'scripts/check_L115_completion.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

def main():
    current = check_L115_completion()
    print(json.dumps(current, sort_keys=True))
    print('PASS: L115 complete source supplement; 98 fully treated originals and 7 remaining.')
    print('Scope: prior accepted science preserved; no new ordinary recovery, principal refutation, measurement or Lean credit.')
'''
    result = ''.join(lines[:main.lineno-1]) + replacement + ''.join(lines[main.end_lineno:])
    before = [ast.dump(n, include_attributes=False) for n in tree.body
              if not isinstance(n, ast.FunctionDef) or n.name != 'main']
    after = [ast.dump(n, include_attributes=False) for n in ast.parse(result).body
             if not isinstance(n, ast.FunctionDef) or n.name not in ['main', 'check_L115_completion']]
    need(before == after, 'Preserve entire predecessor verifier except main dispatch')
    return result


# The semantic function below is copied literally from the reviewed candidate checker.
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





def controls(old, new, admission):
    rejected = []
    for name, mutate in [('extra_recovery', lambda x: x.update(admitted_principal_originals=93)),
                         ('measured_id_removed', lambda x: x['measured_original_ids'].pop()),
                         ('wrong_closed_source', lambda x: x.update(source_complete_refutation_original_ids=['L115'])),
                         ('premature_completion', lambda x: x.update(completion_obligation_originals=0))]:
        bad = copy.deepcopy(new)
        mutate(bad)
        try:
            semantic(old, bad, admission)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Accepted damaged registration')
    return rejected


def manifest_rows(root, params):
    """Retain accepted old rows; hash only declared additions and replacements."""
    old = load(bind(root, params['previous_publication_manifest']))
    rows = {r['file']: r for r in old['files']}
    current = set(git(root, 'ls-files', '-z').decode().split('\0'))
    current.discard('')
    current.discard('provenance/publication_manifest.json')
    need(set(rows) <= current, 'No prior tracked artifact removed')
    for name in changed_paths(root):
        if name == 'provenance/publication_manifest.json':
            continue
        need(name in current, 'Stage all new artifacts before final manifest')
        row = pin(safe(root, name), root)
        rows[name] = dict(file=row['path'], bytes=row['bytes'], sha256=row['sha256'])
    need(set(rows) == current, 'Exact tracked publication paths')
    return {**old, 'files': [rows[name] for name in sorted(rows)]}


def verify(root, require_root=True):
    root = Path(root).resolve()
    a = root / AUD
    params = load(a / 'integration/parameters.json')
    payload = load(a / 'integration/payload_manifest.json')
    need(params['baseline'] == BASELINE and payload['baseline'] == BASELINE, 'Exact accepted predecessor')
    need(git(root, 'merge-base', '--is-ancestor', BASELINE, 'HEAD') == b'', 'Baseline is ancestor')
    for row in payload['files'] + params['preserved'] + params['history']:
        bind(root, row)
    for row in params['integration_files']:
        bind(root, row)
    candidate = a / 'registration/manifest.json'
    need(sha(candidate) == CANDIDATE_SHA, 'Exact reviewed registration candidate')
    for row in load(candidate)['exports']:
        target = row['path'][9:] if row['path'].startswith('proposed/') else AUD + '/registration/' + row['path']
        bind(root, dict(row, path=target))
    old = load(a / 'previous/audit/corpus/latest.json')
    new = load(root / 'audit/corpus/latest.json')
    admission = load(a / 'admission.json')
    semantic(old, new, admission)
    need((root/'scripts/verify_snapshot.py').read_text() == verifier_delta((a/'previous/scripts/verify_snapshot.py').read_text()), 'Exact verifier dispatch change')
    mapping = load(a / 'operational/mapping.json')
    transport = load(a / 'transport.json')
    premises = operational_boundary(mapping, transport)
    need(not any(row['path'].lower().endswith('.md') for row in payload['files']), 'No new public Markdown paths')
    for row in payload['files']:
        need(row['bytes'] == 0 or row['sha256'] not in premises, 'No nonempty documentary or environment premise payload')
    routes = mapping['routes']
    need(mapping['accepted_content_transport'] == pin(a/'transport.json', root) and sha(a/'transport.json') == '18c9b0c7e72ac7da589afb1f2a07b1eefe3f066d412a7bc9a77143f40b19660f', 'Exact root-accepted transport')
    spec = importlib.util.spec_from_file_location('L115_public_codec', a/'pack_codec.py')
    codec = importlib.util.module_from_spec(spec); spec.loader.exec_module(codec)
    decoded = set(); indexed = {}
    for row in routes:
        original = row['original']
        need(original['path'] not in indexed, 'Unique operational source occurrence')
        indexed[original['path']] = row
        if 'public' in row:
            need((row['public']['bytes'], row['public']['sha256']) == (original['bytes'], original['sha256']), 'Exact public operational content')
            bind(root, row['public'])
        elif 'transport_object' in row:
            ref = row['transport_object']; h = ref['sha256']
            if h not in decoded:
                codec.verify(transport['objects'][h], [root]); decoded.add(h)
    def operational_json(original_path):
        need(original_path in indexed, 'Explicit acquired operational input')
        route = indexed[original_path]
        if 'public' in route: return load(bind(root, route['public']))
        need('transport_object' in route, 'Documentary premise cannot supply scientific bytes')
        record = transport['objects'][route['transport_object']['sha256']]
        return json.loads(b''.join(codec.decoded(record, [root])))
    authority = mapping['original_manifest']
    need(authority['sha256'] == PORTABLE_SHA and indexed[authority['path']]['original'] == authority, 'Exact portable authority')
    accepted = operational_json(authority['path'])
    need(accepted['status'] == mapping['original_status'] == 'ACCEPTED_L115_PORTABLE_COMPLETE_SOURCE_TREATMENT', 'Portable acceptance status')
    folder = str(Path(authority['path']).parent)
    expected = operational_json(folder+'/dependencies.json') + [dict(r, path=folder+'/'+r['path']) for r in accepted['exports']] + [authority]
    declared = {}
    for row in expected:
        need(row['path'] not in declared or declared[row['path']] == row, 'Consistent inherited operational aliases')
        declared[row['path']] = row
    need({k:v['original'] for k,v in indexed.items()} == declared, 'Every accepted operational input routed exactly once')
    for digest, status in [(MATH_SHA, 'ACCEPTED_L115_COMPLETE_CORRECTED_SOURCE_TREATMENT'),
                           (PORTABLE_SHA, 'ACCEPTED_L115_PORTABLE_COMPLETE_SOURCE_TREATMENT')]:
        target = next(r['public'] for r in routes if 'public' in r and r['original']['sha256'] == digest)
        need(load(bind(root, target))['status'] == status, 'Retained distinct acceptance')
    allowed = {r['path'] for r in payload['files'] + params['history'] + params['integration_files']}
    allowed |= {AUD+'/integration/parameters.json', AUD+'/integration/payload_manifest.json',
                AUD+'/root_integration.json', 'provenance/publication_manifest.json'}
    for name in changed_paths(root):
        need(name in allowed or name.startswith((AUD+'/registration_review/', AUD+'/integration_checks/')), 'Only declared L115 changes: '+name)
    if require_root:
        gate = load(a / 'root_integration.json')
        need(gate['status'] == 'ROOT_ACCEPTED_L115_COMPLETE_SOURCE_PUBLICATION' and gate['source_ids'] == ['L115'], 'Final root adoption')
        need(gate['source_completion_credit'] == 1 and gate['ordinary_recovery_credit'] == gate['principal_refutation_credit'] == 0, 'Exact root credits')
        for row in gate['bindings']:
            bind(root, row)
        need(gate['payload_manifest'] == pin(a/'integration/payload_manifest.json', root), 'Root binds exact supplement')
        need(gate['parameters'] == pin(a/'integration/parameters.json', root), 'Root binds exact parameters')
        need(gate['candidate_manifest'] == pin(candidate, root), 'Root binds reviewed candidate')
        need(gate['mathematical_acceptance_sha256'] == MATH_SHA and gate['portable_acceptance_sha256'] == PORTABLE_SHA, 'Accepted science retained')
        need(load(root/'provenance/publication_manifest.json') == manifest_rows(root, params), 'Exact tracked manifest; prior metadata preserved')
    return dict(status='PASS_L115_COMPLETE_SOURCE_SUPPLEMENT', fully_treated=98, ordinary_recoveries=92,
                principal_refutations=9, principal_dispositions=101, measured=53, unmeasured_recoveries=39,
                surviving_refuted_sources=3, undisposed_originals=4, outstanding=7,
                exact_payload_files=len(payload['files']), operational_bindings=len(routes), decoded_operational_objects=len(decoded),
                controls=controls(old,new,admission), documentary_controls=boundary_controls(mapping,transport),
                operational_premise_objects=len(premises), final_root_gate_checked=require_root,
                historical_science_replayed=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--preflight', action='store_true')
    args = p.parse_args()
    print(json.dumps(verify(args.repo, not args.preflight), sort_keys=True))
