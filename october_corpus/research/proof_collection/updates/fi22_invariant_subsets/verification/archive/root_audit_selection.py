from pathlib import Path, PurePosixPath
import hashlib, json

T = Path('/private/tmp/fi22_invariant_subset_export')
W = Path('/Users/sasha/medusa/human_compression/october_corpus')

def pin(path):
    body = path.read_bytes()
    return dict(path=str(path), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())

def check(ref):
    assert pin(Path(ref['path'])) == ref, ref['path']

handoff = json.loads((T / 'handoff.json').read_bytes())
for key in ('program', 'verifier', 'plan', 'manifest', 'scope', 'input_maps', 'invoice'):
    check(handoff[key])
plan = json.loads(Path(handoff['plan']['path']).read_bytes())
manifest = json.loads(Path(handoff['manifest']['path']).read_bytes())
scope = json.loads(Path(handoff['scope']['path']).read_bytes())
maps = json.loads(Path(handoff['input_maps']['path']).read_bytes())
destinations = {}
for row in plan['payloads']:
    target = row['target']
    p = PurePosixPath(target)
    assert not p.is_absolute() and '..' not in p.parts and str(p) == target
    assert target not in destinations
    check(row['source'])
    destinations[target] = row['source']
    for alias in row['originals']:
        assert (alias['bytes'], alias['sha256']) == (row['source']['bytes'], row['source']['sha256'])
for row in plan['existing_public_reuses']:
    check(dict(row, path=str(W / row['path'])))
    assert row['path'] not in destinations
    destinations[row['path']] = row
assert len(plan['payloads']) == 90 and len(plan['existing_public_reuses']) == 25
assert sum(r['source']['bytes'] for r in plan['payloads']) == 1194805
assert len(manifest['files']) == 113 and len(manifest['original_to_relative']) == 200
listed = {r['path']: r for r in manifest['files']}
assert len(listed) == len(manifest['files'])
for target, row in listed.items():
    source = destinations[target]
    assert (source['bytes'], source['sha256']) == (row['bytes'], row['sha256'])
aliases = {}
for row in manifest['original_to_relative']:
    original, target = row['original'], row['relative']
    source = listed[target]
    assert (original['bytes'], original['sha256']) == (source['bytes'], source['sha256'])
    key = (original['path'], original['bytes'], original['sha256'])
    assert key not in aliases or aliases[key] == target
    aliases[key] = target
def mapped(ref):
    target = aliases[(ref['path'], ref['bytes'], ref['sha256'])]
    row = listed[target]
    assert (row['bytes'], row['sha256']) == (ref['bytes'], ref['sha256'])
    return target
retention_count = 0
for ref in scope['immutable_source_preservations']:
    check(ref)
    mapped(ref)
    retention = json.loads(Path(ref['path']).read_bytes())
    rows = retention.get('files', retention.get('rows'))
    assert isinstance(rows, list)
    for row in rows:
        check(row['retained'])
        assert mapped(row['original']) == mapped(row['retained'])
        retention_count += 1
assert retention_count == 86
assert len(maps['fixed_inputs']) == 22
for row in maps['fixed_inputs']:
    check(row['original'])
    assert mapped(row['original']) == row['relative']
assert sum(row['existing_public_reuse'] for row in maps['fixed_inputs']) == 18
check(scope['actual_adoption'])
assert mapped(scope['actual_adoption']) == maps['adopted_receipt']
adoption = json.loads(Path(scope['actual_adoption']['path']).read_bytes())
assert adoption['adopted'] is True
assert scope['programme'] == dict(complete_originals=102, new_complete_original_credit=0,
    pending=['F004', 'F009', 'L026'], total_originals=105)
assert scope['new_nongenerating_components'] == 12
assert scope['combined_nongenerating_components'] == 17700
assert scope['unresolved_components'] == 28896
facts = scope['exact_new_facts']
assert len(facts) == 12 and sum(x['invariant_points'] for x in facts) == 3009
assert sum(x['strict_positive_rotation_edges'] for x in facts) == 6018
assert all(x['strict_positive_rotation_edges'] == 2*x['invariant_points'] for x in facts)
assert all(manifest[k] == 0 for k in ('whole_original_credit', 'conjecture_credit', 'Lean_credit', 'compression_credit'))
assert manifest['scientific_replay_status'] == 'NOT_ACQUIRED_BY_THIS_EXPORT'
assert not (T / 'stage').exists()
value = dict(schema='ROOT_REVIEWED_FI22_NG12_PUBLIC_ARCHIVE_SELECTION_V1', root='/root',
    status='SUPPORTED', blockers=[], program=handoff['program'], verifier=handoff['verifier'],
    plan=handoff['plan'], manifest=handoff['manifest'], complete_retention_rows=86,
    complete_fixed_inputs=22, payload_files=90, reused_public_files=25,
    complete_original_mappings=200, all_whole_selected_sources_checked=True,
    mathematical_replay_acquired_by_copy=False, file_copy_only=True,
    whole_original_credit=0, reviewed_scope=scope)
body = (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()
(T / 'runtime').mkdir(exist_ok=True)
out = T / 'runtime/Root_selection_review.json'
with out.open('xb') as f:
    f.write(body)
print(json.dumps(dict(status='ROOT_FULL_ARCHIVE_SELECTION_SUPPORTED', review=pin(out),
    payload_files=90, reused_public_files=25, original_mappings=200, retention_rows=86)))
