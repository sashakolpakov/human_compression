from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
S=Path('/Users/sasha/medusa/research/leemans')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
if(P/'manifest.json').exists():raise ValueError('Frozen packet already exists')
put(P/'dependencies.json',[pin(S/'sources/catalogue_L036.pdf'),pin(S/'reboot_20261013/L036_work/source.txt')])
put(P/'scope.json',dict(status='AUTHOR_COMPLETE_REQUIRES_DISTINCT_REVIEW',author='root',source='L036, Algorithm3.1, physical pages4 and5',proof_pages=2,
 claims=['Inverse image of a subgroup image is its product with the action kernel.','Printed arbitrary-group algorithm fails for C2 x C2.','Retaining the original subgroup gives completeness for every finite group under the source equivalence.'],
 borrowed=['Source subgroup-orbit method and automorphism equivalence.','Elementary kernel identity, orbit-stabilizer theorem and coset-incidence facts.'],
 new=['Diagnosis and repair of the arbitrary-group scope; explicit order4 example.'],
 unchanged_simple_group_scope=True,whole_source_credit=0,principal_refutation_delta=0,new_Lean=0,measurement=None,all_two_native_pages_viewed=True))
names=['scope.tex','scope.pdf','example.py','example.json','scope.json','dependencies.json','final-01.png','final-02.png','build1.stdout','build1.stderr','build2.stdout','build2.stderr','freeze.py']
exports=[]
for name in names:
 r=pin(P/name);r['path']=name;exports.append(r)
put(P/'manifest.json',dict(status='AUTHOR_L036_COSET_ACTION_SCOPE_CORRECTION_AWAITING_REVIEW',exports=exports))
print(json.dumps(pin(P/'manifest.json')))
