from pathlib import Path
import ast, hashlib, json

T = Path('/private/tmp/fi22_subset_relative_replay')
C = Path('/Users/sasha/medusa/human_compression/october_corpus')

def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def check(r):
    assert pin(Path(r['path'])) == r, r['path']

def definitions(s):
    return {n.name: ast.get_source_segment(s, n) for n in ast.parse(s).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

h = json.loads((T/'handoff.json').read_bytes())
for key in ('program', 'controls', 'point_kernel', 'subset_kernel', 'plan', 'source_inverse',
            'controls_inverse', 'read_map', 'invoice', 'artifact_targets', 'archive_manifest', 'archive_plan'):
    check(h[key])
source = Path(h['program']['path']).read_text()
inverse = json.loads(Path(h['source_inverse']['path']).read_bytes())
check(inverse['relative_parent'])
check(inverse['mathematical_parent'])
old = Path(inverse['relative_parent']['path']).read_text()
math_source = Path(inverse['mathematical_parent']['path']).read_text()
assert ''.join(r['old'] for r in inverse['complete_ordered_line_inverse']) == old
assert ''.join(r['new'] for r in inverse['complete_ordered_line_inverse']) == source
actual, parent, relative = definitions(source), definitions(math_source), definitions(old)
for name in h['literal6538_functions']:
    assert actual[name] == parent[name], name
for name in h['literal74b_functions']:
    assert actual[name] == relative[name], name
ci = json.loads(Path(h['controls_inverse']['path']).read_bytes())
controls = Path(h['controls']['path']).read_text()
assert ci['whole_new_controls'] == controls
check(ci['generic_fixture_parent'])
assert definitions(controls)['fixture'] == definitions(Path(ci['generic_fixture_parent']['path']).read_text())['fixture']
plan = json.loads(Path(h['plan']['path']).read_bytes())
closure = {}
for row in plan['reference_map']:
    r = row['original']
    p = C/row['relative']
    actual_pin = pin(p)
    assert (actual_pin['bytes'], actual_pin['sha256']) == (r['bytes'], r['sha256'])
    assert row['relative'] not in closure or closure[row['relative']] == actual_pin
    closure[row['relative']] = actual_pin
assert len(closure) == 28 and len(plan['reference_map']) == 28
assert sum(r['bytes'] for r in closure.values()) == 1523658
assert h['program']['bytes'] + 4 + 2*(1523658 + h['program']['bytes'] + h['plan']['bytes']) == 3172921
assert h['program']['bytes'] + h['point_kernel']['bytes'] + h['subset_kernel']['bytes'] == 37429
assert plan['expected_positive_free_indices'] == [0,2,4,6,7,8,9,11,12,13,14,15]
assert plan['Root_execution_authority_granted'] is False
targets = json.loads(Path(h['artifact_targets']['path']).read_bytes())
installed = []
for row in targets['files']:
    check(row['source'])
    path = C/row['target']
    assert not path.exists(), path
for row in targets['files']:
    path = C/row['target']
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(Path(row['source']['path']).read_bytes())
    result = pin(path)
    assert (result['bytes'], result['sha256']) == (row['source']['bytes'], row['source']['sha256'])
    installed.append(result)
assert plan['program'] == dict(path=targets['files'][0]['target'], bytes=h['program']['bytes'], sha256=h['program']['sha256'])
review = dict(schema='ROOT_REVIEWED_RELATIVE_FI22_SUBSET_REPLAY_SOURCE_V1', root='/root', status='SUPPORTED', blockers=[],
    program=h['program'], controls=h['controls'], plan=h['plan'],
    full_source_controls_new_main_history_IO_and_math_imports_read=True,
    whole_forward_and_reverse_source_inverse_verified=True,
    literal_math_definitions_verified=8, literal_relative_definitions_verified=3,
    unchanged_point_and_subset_kernels_verified=True,
    complete_physical_paths=30, complete_physical_read_upper=3172921,
    namespace_bytes=37429, shared_work_upper=6779507,
    new_control_and_scientific_replay_still_owed=True,
    qualification='Only optional replay of the twelve adopted negative certificates. Exact original classified/model/member/action/global premises retained. No new paid cases, whole original, generation or measurement credit.',
    installed_exact_files=installed)
body = (json.dumps(review, sort_keys=True, separators=(',', ':'))+'\n').encode()
(T/'runtime').mkdir(exist_ok=True)
p = T/'runtime/Root_source_data_review.json'
with p.open('xb') as f:
    f.write(body)
print(json.dumps(dict(status='ROOT_REVIEWED_AND_INSTALLED_EXACT_RELATIVE_REPLAY', review=pin(p), installed_files=len(installed),
    mathematical_Source_activations=0, original_case_calls=0)))
