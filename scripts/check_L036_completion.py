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
import json
import subprocess

AUD = 'audit/principal-refutations/L036/complete/v1'
BASELINE = 'c5cd1ca228ee69ccdcd6cbd32956dbf895afa74f'
CANDIDATE_SHA = 'fcdfac6156704ee1832cc214f2b83941bd196fae623716de61762c6ae6f1e80a'
MATH_SHA = 'b19a2543b1d33ebc1d317c719a4151a20fc3c601fbc5808cb0c82ca46335e5b9'
PORTABLE_SHA = 'fcd3b2518f6ff70a03c497ac6e478d705baceaa39dc16a5deedd65ca4b01f2d7'


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
    replacement = '''def check_L036_completion():
    spec=importlib.util.spec_from_file_location('L036_completion',ROOT/'scripts/check_L036_completion.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

def main():
    current = check_L036_completion()
    print(json.dumps(current, sort_keys=True))
    print('PASS: L036 complete source supplement; 94 fully treated originals and 11 remaining.')
    print('Scope: prior accepted science preserved; no new ordinary recovery, principal refutation, measurement or Lean credit.')
'''
    result = ''.join(lines[:main.lineno-1]) + replacement + ''.join(lines[main.end_lineno:])
    before = [ast.dump(n, include_attributes=False) for n in tree.body
              if not isinstance(n, ast.FunctionDef) or n.name != 'main']
    after = [ast.dump(n, include_attributes=False) for n in ast.parse(result).body
             if not isinstance(n, ast.FunctionDef) or n.name not in ['main', 'check_L036_completion']]
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
    need(new['fully_treated_original_ids'] == sorted(old['fully_treated_original_ids'] + ['L036']), 'exact fully treated set')
    need(len(set(new['fully_treated_original_ids'])) == new['fully_treated_originals'] == 94, 'fully treated count')
    need(new['source_complete_refutation_original_ids'] == sorted(old['source_complete_refutation_original_ids'] + ['L036']) and new['source_complete_refutation_originals'] == 3,
         'only L036 completed after refutation')
    need(new['surviving_claim_obligation_original_ids'] == [x for x in old['surviving_claim_obligation_original_ids'] if x != 'L036'], 'only L036 leaves surviving claims')
    need(len(new['surviving_claim_obligation_original_ids']) == new['surviving_claim_obligation_originals'] == 6, 'surviving count')
    need(new['completion_obligation_original_ids'] == [x for x in old['completion_obligation_original_ids'] if x != 'L036'], 'only L036 leaves all obligations')
    need(len(new['completion_obligation_original_ids']) == new['completion_obligation_originals'] == 11, 'outstanding count')
    need(set(new['completion_obligation_original_ids']) == set(new['surviving_claim_obligation_original_ids']) | set(new['accessible_pending_original_ids']), 'exact outstanding partition')
    need(set(new['fully_treated_original_ids']).isdisjoint(new['completion_obligation_original_ids']), 'completed and outstanding disjoint')
    need(len(set(new['fully_treated_original_ids']) | set(new['completion_obligation_original_ids'])) == 105, 'all mathematical originals accounted once')
    need(admission['source_ids'] == ['L036'] and admission['proposed_source_completion_credit'] == 1, 'one source completion')
    for key in ['ordinary_recovery_credit', 'principal_refutation_credit', 'new_original_credit', 'new_measurements', 'new_question_credit', 'new_Lean_credit']:
        need(admission[key] == 0, 'unearned credit: ' + key)
    need(not admission['whole_source_formalized'] and admission['compression_factor'] is None, 'no unsupported formalization or factor')
    need(admission['uncertified_extensions'] == ['Contents and completeness of external downloadable representative files', 'Higher-rank extension proposed as future work', 'Historical timings and a claimed speedup, not independently benchmarked', 'General formal verification in Lean and compression measurement'], 'fixed source scope preserved')



def operational_boundary(mapping, transport):
    expected = transport['premises']
    need(mapping['premises'] == expected, 'same documentary/environment premises as accepted stage')
    by_hash = {r['sha256']: r for r in expected}
    need(len(expected) == len(by_hash) == 218, 'exact218 premise objects')
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
    need(used == set(by_hash), 'all and only218 operational premises')
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


def controls(old, new, admission):
    rejected = []
    for name, mutate in [('extra_recovery', lambda x: x.update(admitted_principal_originals=92)),
                         ('measured_id_removed', lambda x: x['measured_original_ids'].pop()),
                         ('wrong_closed_source', lambda x: x.update(source_complete_refutation_original_ids=['L036'])),
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
    for row in payload['files']:
        need(row['sha256'] not in premises, 'No documentary or environment premise payload')
    routes = mapping['routes']
    for row in routes:
        if 'public' in row:
            bind(root, row['public'])
    for digest, status in [(MATH_SHA, 'ACCEPTED_L036_COMPLETE_CORRECTED_SOURCE_TREATMENT'),
                           (PORTABLE_SHA, 'ACCEPTED_L036_PORTABLE_COMPLETE_SOURCE_TREATMENT')]:
        target = next(r['public'] for r in routes if 'public' in r and r['original']['sha256'] == digest)
        need(load(bind(root, target))['status'] == status, 'Retained distinct acceptance')
    allowed = {r['path'] for r in payload['files'] + params['history'] + params['integration_files']}
    allowed |= {AUD+'/integration/parameters.json', AUD+'/integration/payload_manifest.json',
                AUD+'/root_integration.json', 'provenance/publication_manifest.json'}
    for name in changed_paths(root):
        need(name in allowed or name.startswith((AUD+'/registration_review/', AUD+'/integration_checks/')), 'Only declared L036 changes: '+name)
    if require_root:
        gate = load(a / 'root_integration.json')
        need(gate['status'] == 'ROOT_ACCEPTED_L036_COMPLETE_SOURCE_PUBLICATION' and gate['source_ids'] == ['L036'], 'Final root adoption')
        need(gate['source_completion_credit'] == 1 and gate['ordinary_recovery_credit'] == gate['principal_refutation_credit'] == 0, 'Exact root credits')
        for row in gate['bindings']:
            bind(root, row)
        need(gate['payload_manifest'] == pin(a/'integration/payload_manifest.json', root), 'Root binds exact supplement')
        need(gate['parameters'] == pin(a/'integration/parameters.json', root), 'Root binds exact parameters')
        need(gate['candidate_manifest'] == pin(candidate, root), 'Root binds reviewed candidate')
        need(gate['mathematical_acceptance_sha256'] == MATH_SHA and gate['portable_acceptance_sha256'] == PORTABLE_SHA, 'Accepted science retained')
        need(load(root/'provenance/publication_manifest.json') == manifest_rows(root, params), 'Exact tracked manifest; prior metadata preserved')
    return dict(status='PASS_L036_COMPLETE_SOURCE_SUPPLEMENT', fully_treated=94, ordinary_recoveries=91,
                principal_refutations=9, principal_dispositions=100, measured=53, unmeasured_recoveries=38,
                surviving_refuted_sources=6, undisposed_originals=5, outstanding=11,
                exact_payload_files=len(payload['files']), operational_bindings=len(routes),
                controls=controls(old,new,admission), documentary_controls=boundary_controls(mapping,transport),
                operational_premise_objects=len(premises), final_root_gate_checked=require_root,
                historical_science_replayed=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--preflight', action='store_true')
    args = p.parse_args()
    print(json.dumps(verify(args.repo, not args.preflight), sort_keys=True))
