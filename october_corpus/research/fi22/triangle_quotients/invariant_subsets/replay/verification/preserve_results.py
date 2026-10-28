from pathlib import Path
import hashlib, json, os

T = Path('/private/tmp/fi22_subset_relative_replay')
C = Path('/Users/sasha/medusa/human_compression/october_corpus')
S = Path('/Users/sasha/medusa/research/leemans/maintenance/intake/l026_fi22_neighborhood_orbits/operations/triangle_quotients/invariant_subsets/relative_replay/evidence')
base = Path('research/fi22/triangle_quotients/invariant_subsets/replay')

def pin(p, b=None):
    if b is None:
        b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def put(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        assert p.read_bytes() == b, p
    else:
        with p.open('xb') as f:
            f.write(b)
            f.flush()
            os.fsync(f.fileno())

peer = json.loads((T/'independent_review/independent_review.json').read_bytes())
assert peer['status'] == 'SUPPORTED_STATIC_SOURCE_DATA_AND_ACTUAL_GENERIC_CONTROLS'
assert peer['blockers'] == []
for name in ('final_controls', 'replay'):
    cap = json.loads((T/('runtime/'+name+'_actual_capture.json')).read_bytes())
    assert cap['actual_tool']['exit_code'] == 0
    assert json.loads((T/('runtime/'+name+'_guard/receipt.json')).read_bytes())['status'] == 'PASS'
controls = json.loads((T/'runtime/final_controls_guard/stdout.log').read_bytes())
assert controls['status'] == 'PASS' and controls['controls'] == 9
assert controls['program']['sha256'] == 'e0b299b5a484de58e9904f6024e80583abac0f2c57c1c4ff2bcf4ecb8d68d38a'
result = json.loads((T/'runtime/replay_guard/stdout.log').read_bytes())
assert result['status'] == 'VERIFIED_ADOPTED_ORIGINAL_ROTATION_SUBSETS'
assert result['verified_count'] == 12 and result['actual_checked_points'] == 3009
assert result['actual_positive_rotation_edges'] == 6018
assert result['actual_original_machine_path_reads'] == 0
assert result['resources']['physical_read_bytes'] == 3172921
assert result['resources']['physical_paths'] == 30
assert result['resources']['work_units'] == 6536655
assert result['resources']['peak_RSS'] < 128*2**20
rows, files, originals = [], {}, []

def retained(source, target):
    body = source.read_bytes()
    r = pin(source, body)
    p = S/'objects'/r['sha256']
    put(p, body)
    rows.append(dict(original=r, retained=pin(p, body)))
    put(C/target, body)
    current = dict(path=str(target), bytes=r['bytes'], sha256=r['sha256'], role='archived_evidence')
    assert str(target) not in files or files[str(target)] == current
    files[str(target)] = current
    originals.append(dict(original=r, relative=str(target)))

target_table = json.loads((T/'control_io/artifact_targets_magic.json').read_bytes())
for row in target_table['files']:
    assert pin(Path(row['source']['path'])) == row['source']
    retained(Path(row['source']['path']), Path(row['target']))
plan = json.loads((T/'plan.json').read_bytes())
for row in plan['reference_map']:
    p = C/row['relative']
    r = pin(p)
    assert (r['bytes'], r['sha256']) == (row['original']['bytes'], row['original']['sha256'])
    files[row['relative']] = dict(r, path=row['relative'], role='mathematical_data')
    originals.append(row)

names = ['root_audit_install.py', 'preserve_results.py', 'handoff.json', 'control_io/handoff_with_magic.json',
    'control_io/artifact_targets_magic.json', 'independent_review/independent_review.json',
    'independent_review/observations.json', 'independent_review/final_controls_observation.json',
    'runtime/Root_source_data_review.json', 'runtime/Root_audit_install_actual_capture.json',
    'runtime/Root_final_control_reporting_review.json',
    'runtime/Root_peer_status_spelling_check_failure_actual_capture.json']
for name in ('controls', 'final_controls', 'replay'):
    names.append('runtime/'+name+'_actual_capture.json')
    names += ['runtime/'+name+'_guard/'+tail for tail in ('receipt.json', 'started.json', 'stdout.log', 'stderr.log')]
for name in ('controls.py', 'first_calls.json', 'README.rst'):
    names.append('runtime/previous_installed/'+name)
for name in names:
    retained(T/name, base/'verification'/name.removeprefix('runtime/'))

preservation = dict(schema='ROOT_CLOSED_ACTUAL_RELATIVE_FI22_SUBSET_REPLAY_V1', root='/root',
    status='VERIFIED_ADOPTED_ORIGINAL_ROTATION_SUBSETS', files=rows, replayed_count=12,
    checked_points=3009, checked_positive_edges=6018, original_machine_paths_opened=0,
    new_paid_original_or_case_credit=0,
    metadata_status_assertion_note='The first pre-run metadata check used the shorthand SUPPORTED instead of the peer exact longer label. Its failed call is preserved. The complete pinned peer had no blockers; the actual arithmetic and final controls passed under their own exact identities. No failed metadata check is reported as passed.')
p = S/'preservation.json'
put(p, (json.dumps(preservation, sort_keys=True, separators=(',', ':'))+'\n').encode())
retained(p, base/'verification/preservation.json')
manifest = dict(schema='CURATED_PORTABLE_PROOF_PACKET_MANIFEST_V1', packet='fi22_relative_adopted_subset_replay',
    files=list(files.values()), original_to_relative=originals, packed_members=[], proof_banks=[],
    scientific_replay_status='ACTUAL_TWELVE_ADOPTED_SUBSET_REPLAY_PASSED', whole_original_credit=0,
    conjecture_credit=0, Lean_credit=0, compression_credit=0,
    qualification='Exact finite point closure replay, with all original model/action/membership/classification and geometry premises retained. No new adopted case or manuscript result.')
p = C/base/'manifest.json'
put(p, (json.dumps(manifest, sort_keys=True, separators=(',', ':'))+'\n').encode())
print(json.dumps(dict(status='ACTUAL_RELATIVE_REPLAY_AND_EVIDENCE_PRESERVED', manifest=pin(p),
    files=len(files), original_mappings=len(originals), S_preservation=pin(S/'preservation.json'),
    scientific_calls_in_this_copy=0, verified_count=12, checked_positive_edges=6018)))
