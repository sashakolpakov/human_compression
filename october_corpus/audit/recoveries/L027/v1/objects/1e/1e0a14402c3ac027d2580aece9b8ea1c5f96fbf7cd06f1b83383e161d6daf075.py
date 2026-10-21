import hashlib
import json
from pathlib import Path
import shutil

S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013/L027_rank_four_distinct'
A=S/'corpus106_L027_rank_four_v1'
O=S/'corpus106_L027_rank_four_independent_review'

def pin(p):
    p=Path(p);b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):
    p.write_text(json.dumps(x,indent=2)+'\n')

if O.exists():
    raise SystemExit('immutable review already exists')
bindings=[]
def bind(p,expected=None):
    got=pin(p)
    if expected is not None and (got['bytes']!=expected['bytes'] or got['sha256']!=expected['sha256']):
        raise ValueError('binding mismatch '+str(p))
    bindings.append(got)
bind(A/'manifest.json')
if bindings[0]['sha256']!='45b3229778ed49c181123218eb02f85fb91cefc98cd447659a4af95eeeeb8ffd':
    raise ValueError('wrong author edition')
for x in json.loads((A/'manifest.json').read_text())['exports']:
    bind(A/x['path'],x)
for x in json.loads((A/'dependencies.json').read_text()):
    bind(x['path'],x)
O.mkdir()
shutil.copytree(W/'fresh01',O/'fresh01')
for name in ('review.rst','reversal_control.g','reversal_control.json','freeze_review.py'):
    shutil.copy2(W/name,O/name)
for i in range(1,5):
    shutil.copy2(W/f'source-{i:02}.png',O/f'source-{i:02}.png')
write(O/'dependencies.json',bindings)
write(O/'review.json',dict(
    status='ACCEPTED_L027_RANK_FOUR_COMPONENT',
    author='root',reviewer='l044_resume',
    author_manifest=pin(A/'manifest.json'),
    source=pin(S/'sources/psl3_chiral2022.pdf'),
    source_pages_read=list(range(1,8)),source_pages_directly_viewed=[4,5,6,7],
    full_proof_code_and_acquired_interfaces_read=True,
    fresh_native_pages_directly_viewed=[1,2,3,4],
    fresh_session=15604,fresh_report=pin(W/'fresh01/report.json'),
    independent_control=pin(W/'reversal_control.json'),
    reviewer_contribution='None to author mathematics or code; independently written supplementary intertwiner control during distinct review.',
    scope='Theorem 1.1 and complete Section 3 only; other L027 principal clauses remain outside this component.',
    binding_occurrences=len(bindings),
    whole_original_credit=0,public_registration=False,new_question_credit=0,
    new_Lean=0,measurement=None,owned_live_handles=[]))
exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():
        x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',dict(status='ACCEPTED_L027_RANK_FOUR_COMPONENT',exports=exports))
print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),bindings=len(bindings))))
