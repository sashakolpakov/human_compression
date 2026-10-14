import hashlib
import json
from pathlib import Path
import shutil

S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013/L041_decorated_distinct'
A=S/'corpus106_L041_decorated_geometry_v2'
O=S/'corpus106_L041_decorated_geometry_independent_review'

def pin(p):
    p=Path(p)
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def write(p,x):
    p.write_text(json.dumps(x,indent=2)+'\n')

if O.exists():
    raise SystemExit('immutable review already exists')
bindings=[]
def bind(p,expected=None):
    got=pin(p)
    if expected is not None and (got['bytes']!=expected['bytes'] or got['sha256']!=expected['sha256']):
        raise ValueError('binding mismatch: '+str(p))
    bindings.append(got)

bind(A/'manifest.json')
if bindings[0]['sha256']!='6f7221a6784c479748786ca2497df0a32f1162cd995e93acb3d9f58dc1665877':
    raise ValueError('wrong author edition')
for x in json.loads((A/'manifest.json').read_text())['exports']:
    bind(A/x['path'],x)
for x in json.loads((A/'dependencies.json').read_text()):
    bind(x['path'],x)
for n in (8,14,15,16,19,20):
    bind(S/f'reboot_20261013/L041_work/source_{n:02}.png')
for name in ('read01.rst','report01.json'):
    bind(S/'reboot_20261013/L041_preliminary_distinct'/name)

O.mkdir()
shutil.copytree(W/'fresh01',O/'fresh01')
for name in ('review.rst','independent_controls.py','independent_controls.json','freeze_review.py'):
    shutil.copy2(W/name,O/name)
write(O/'dependencies.json',bindings)
write(O/'review.json',{
    'status':'ACCEPTED_L041_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY',
    'author':'root','reviewer':'l044_resume',
    'author_manifest':pin(A/'manifest.json'),
    'source':pin(S/'sources/catalogue_L041.pdf'),
    'full_source_pages_read':21,'source_map_rows':28,'numbered_source_statements':20,
    'full_proof_code_and_acquired_interfaces_read':True,
    'source_pages_directly_viewed':[8,14,15,16,19,20],
    'fresh_native_pages_directly_viewed':list(range(1,9)),
    'fresh_session':44906,'fresh_report':pin(W/'fresh01/report.json'),
    'independent_controls':pin(W/'independent_controls.json'),
    'edition_delta':'Only equation renumbering and corresponding references; v1 restoration retained.',
    'reviewer_contribution':'Preliminary full reading and an explicit kernel-index exposition request; no authorship of the new model or program. Final independent controls and complete review.',
    'scope_qualification':'Source page5 generic internal-residue identification used only after actual triple-flag transitivity; no new counterexample inferred.',
    'binding_occurrences':len(bindings),
    'whole_original_credit':0,'public_registration':False,
    'new_question_credit':0,'new_Lean':0,'measurement':None,
    'owned_live_handles':[]
})
exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():
        x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',{'status':'ACCEPTED_L041_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY','exports':exports})
print(json.dumps({'manifest':pin(O/'manifest.json'),'exports':len(exports),'bindings':len(bindings)}))
