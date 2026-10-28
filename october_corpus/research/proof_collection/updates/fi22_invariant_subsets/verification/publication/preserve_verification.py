from pathlib import Path
import hashlib, json, os

T = Path('/private/tmp/fi22_invariant_subset_export')
F = Path('/private/tmp/l026_invariant_subsets/full_proper_cap')
W = Path('/Users/sasha/medusa/human_compression/october_corpus')
S = Path('/Users/sasha/medusa/research/leemans')
base = Path('research/proof_collection/updates/fi22_invariant_subsets')
M = S / 'maintenance/intake'
files, mappings = {}, []
copied = read_bytes = 0

def pin(path, body):
    return dict(path=str(path), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())

def put(path, body):
    global copied
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        assert path.read_bytes() == body, path
    else:
        with path.open('xb') as f:
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
        copied += len(body)

def add(source, target):
    global read_bytes
    assert source.is_file() and source.resolve(strict=True) == source
    body = source.read_bytes()
    read_bytes += len(body)
    assert read_bytes < 16*2**20
    original = pin(source, body)
    put(W / target, body)
    value = dict(path=str(target), bytes=len(body), sha256=original['sha256'], role='archived_evidence')
    assert str(target) not in files or files[str(target)] == value
    files[str(target)] = value
    mappings.append(dict(original=original, relative=str(target)))
    return original

# The exact completed copy/integrity calls and independent selection review.
for name in ('root_audit_selection.py', 'export_plan.json', 'Root_release.json', 'read_invoice.json',
             'independent_review/independent_review.json', 'independent_review/observations.json',
             'runtime/Root_selection_review.json', 'runtime/Root_selection_audit_actual_capture.json',
             'runtime/Root_release_actual_capture.json'):
    target = base / 'verification/archive' / name.removeprefix('runtime/')
    add(T / name, target)
for step in ('stage', 'finalize_stage', 'install', 'finalize_install', 'integrity'):
    cap = T / ('runtime/' + step + '_actual_capture.json')
    assert json.loads(cap.read_bytes())['actual_tool']['exit_code'] == 0
    add(cap, base / ('verification/archive/' + step + '_actual_capture.json'))
    for name in ('receipt.json', 'started.json', 'stdout.log', 'stderr.log'):
        add(T / ('runtime/' + step + '_guard') / name, base / ('verification/archive/' + step) / name)

# The independently reviewed, actually published compact intake journal.
journal_preservation = M / 'progress/intake_overview/evidence/fi22_invariant_subsets/preservation.json'
jp = json.loads(journal_preservation.read_bytes())
current = M / 'progress/current_intake_verified_exports.json'
current_body = current.read_bytes()
assert pin(current, current_body) == jp['current']
assert jp['current']['sha256'] == 'c27e93b809230fbfaf54e58cd2d6e0d6f17500a08bd75b0373a9119e97856b07'
add(current, base / 'verification/journal/current_intake.json')
add(journal_preservation, base / 'verification/journal/preservation.json')
for row in jp['rows']:
    source = Path(row['retained']['path'])
    body = source.read_bytes()
    assert pin(source, body) == row['retained']
    target = Path('data/proof_objects/sha256') / row['retained']['sha256']
    add(source, target)
    mappings.append(dict(original=row['original'], relative=str(target)))

# One larger finite search, without any mathematical credit for its cap miss.
names = ('worker.py', 'subset_kernel.py', 'controls.py', 'ARGUMENT.rst', 'plan.json',
         'resume_free_index_0001.json', 'resume_provenance.json', 'source_inverse.json',
         'read_and_work_invoice.json', 'Root_gate.json', 'Root_review.json',
         'independent_review/independent_review.json', 'independent_review/observations.json',
         'runtime/Root_source_data_review.json', 'runtime/Root_source_data_audit_actual_capture.json',
         'runtime/Root_gate_failed_path_actual_capture.json', 'runtime/controls_actual_capture.json',
         'runtime/singleton_proposal_actual_capture.json',
         'instances/free_index_0001/output/result.json',
         'instances/free_index_0001/output/records.json',
         'instances/free_index_0001/output/checkpoint.json')
search_rows = []
dest = M / 'l026_fi22_neighborhood_orbits/operations/triangle_quotients/invariant_subsets/full_subset_search/evidence'
expanded = list(names)
for step in ('control_guard', 'singleton_proposal_guard'):
    expanded += ['runtime/' + step + '/' + name for name in ('receipt.json', 'started.json', 'stdout.log', 'stderr.log')]
for name in expanded:
    source = F / name
    original = add(source, base / 'verification/subset_search' / name.removeprefix('runtime/'))
    body = source.read_bytes()
    retained = dest / 'objects' / original['sha256']
    put(retained, body)
    search_rows.append(dict(original=original, retained=pin(retained, body)))
search_preservation = dict(schema='ROOT_CLOSED_L026_FULL_SUBSET_FINITE_SEARCH_V1', root='/root',
    files=search_rows, selected_free_indices=[1], closed_hints=0, cap_misses_unpaid=[1],
    prior_completed_edges_retained=586, mathematical_credit=0,
    qualification='The exact bounded search reached cap3509. No proper invariant set, generation, absence, or manuscript conclusion follows.')
put(dest / 'preservation.json', (json.dumps(search_preservation, sort_keys=True, separators=(',', ':'))+'\n').encode())
add(dest / 'preservation.json', base / 'verification/subset_search/preservation.json')

manifest = dict(schema='CURATED_PORTABLE_PROOF_PACKET_MANIFEST_V1', packet='fi22_invariant_subsets_actual_publication',
    files=list(files.values()), original_to_relative=mappings, proof_banks=[], packed_members=[],
    scientific_replay_status='METADATA_AND_FINITE_SEARCH_EVIDENCE_ONLY', whole_original_credit=0,
    conjecture_credit=0, Lean_credit=0, compression_credit=0,
    qualification='Authenticates actual archive checks, journal CAS, and one unpaid finite search; the separate mathematical replay remains owed.')
out = W / base / 'verification/manifest.json'
put(out, (json.dumps(manifest, sort_keys=True, separators=(',', ':'))+'\n').encode())
print(json.dumps(dict(status='PUBLIC_VERIFICATION_EVIDENCE_PRESERVED', manifest=pin(out, out.read_bytes()),
    files=len(files), original_mappings=len(mappings), read_bytes=read_bytes, new_bytes=copied,
    preserved_search=pin(dest/'preservation.json', (dest/'preservation.json').read_bytes()),
    scientific_calls=0, whole_original_credit=0)))
