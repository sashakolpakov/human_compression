"""Freeze a finite M11 request without executing its target."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
H=Path(__file__).resolve().parent;P=H.parent;S=P.parents[1];B=S/'algebra/subgroup_atlas'
def pin(p,base=None):
 b=p.read_bytes();return dict(path=str(p.relative_to(base) if base else p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
if (H/'manifest.json').exists() or (H/'request.json').exists():raise RuntimeError('Fresh request only')
data=json.loads((H/'inputs.json').read_text())
registry=json.loads((B/'structural_atoms_v1/registry.json').read_text())
assert data['group_model']==registry['models'][0]
source_parser=B/'structural_labels_pilot_v1/source_join.py'
s=importlib.util.spec_from_file_location('literal_join',source_parser);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
assert data['subgroup_generators']==m.m11_generators((B/'numeric_work/m11_literal02/groups.g').read_text())
numeric=json.loads((B/'numeric_work/m11_literal02/numeric.json').read_text())
assert numeric['group_order']==7920
for script,out in [('small_controls.py','small_controls.json'),('owner_controls.py','owner_controls.json')]:
 p=subprocess.run([sys.executable,str(H/script)],capture_output=True,timeout=15)
 assert p.returncode==0 and not p.stderr
 save(H/out,json.loads(p.stdout))
paths=[H/n for n in ['compute.py','run.py','owner_controls.py','owner_controls.json','small_controls.py','small_controls.json','inputs.json','argument.rst','freeze.py']]
paths += [B/n for n in ['structural_atoms_v1/inputs.json','structural_atoms_v1/registry.json','structural_atoms_v1/manifest.json','structural_atoms_review_v1/manifest.json','structural_atoms_review_v1/review.json','numeric_work/m11_literal02/groups.g','numeric_work/m11_literal02/numeric.json','numeric_review_v1/manifest.json','numeric_review_v1/review.json','numeric_review_v1/comparisons/m11_numeric_comparison.json','structural_labels_pilot_v1/source_join.py']]
paths += [P/'table_application/manifest.json',P/'table_application_root_review/manifest.json',P/'table_application/results.json',P/'character_application_root_review/manifest.json',P/'algorithm_scope_review_adoption/manifest.json',S/'geometry/chiral_atlases/almost_simple_work/acquired_models01/M11.json',Path(sys.executable).resolve()]
req=dict(status='FROZEN_L036_M11_LITERAL_GRAPH_REQUEST_AWAITING_ROOT_REVIEW',source_ids=['L036'],command=[sys.executable,str(H/'compute.py')],deadline_seconds=60,output_cap_bytes=16*2**20,launch_reserve_bytes=4*2**30,emergency_floor_bytes=2*2**30,address_space_bytes=1024*2**20,successor_authorized=False,expected_domain='Acquired M11 model, five maximal classes; all unordered distinct maximal-subgroup pairs',scientific_software_premise='Ordinary Python exact integers and finite permutation/graph operations; no proof-assistant claim',bindings=[pin(p) for p in paths])
save(H/'request.json',req)
save(H/'manifest.json',dict(status=req['status'],target_executed=False,source_ids=['L036'],new_whole_source_credit=0,exports=[pin(p,H) for p in sorted(H.iterdir()) if p.is_file()]))
print(json.dumps(dict(manifest=pin(H/'manifest.json'),request=pin(H/'request.json'),bindings=len(paths),target_executed=False)))
