import sys
if sys.flags.optimize:raise RuntimeError('Normal Python is required')
from pathlib import Path
import json,hashlib,shutil
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');W=S/'reboot_20261013/L033_euclidean_work';O=S/'corpus106_L033_period_adapter_v1'
def need(b,m):
 if not b:raise ValueError(m)
def h(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not O.exists(),'fresh packet')
D={};aliases=[]
def add(p):D[str(p)]=dict(path=str(p),**h(p))
A=R/'audit/topic-c/extensions/generalized-halving/v1';P=R/'papers/topic-c/extensions/generalized-halving/v1';C=R/'papers/topic-c/v2'
for sub in ['author','independent_review','root_adoption']:
 base=A/sub;add(base/'manifest.json');m=json.loads((base/'manifest.json').read_text())
 for x in m['exports']:
  rel=Path(x['path']);poss=[base/rel,P/rel]
  if rel.parts[0]=='old_common':poss.append(C/Path(*rel.parts[1:]))
  poss += [p.with_suffix('.txt') for p in list(poss) if p.suffix=='.md']
  ps=[p for p in poss if p.is_file() and h(p)=={k:x[k]for k in ['bytes','sha256']}]
  need(bool(ps),'missing exact export '+str(base/rel));p=ps[0];add(p)
  if p!=base/rel:aliases.append(dict(logical=str(base/rel),actual=str(p),sha256=x['sha256']))
for p in [A/'admission.json',P/'PUBLICATION.rst',R/'audit/science55/v1/root_integration.json',S/'sources/catalogue_L033.pdf',S/'sources/catalogue_L033.txt']:add(p)
O.mkdir()
for old,new in [('period_adapter.tex','period_adapter.tex'),('period_adapter.pdf','period_adapter.pdf'),('adapter_check.py','check.py'),('freeze_adapter.py','freeze.py')]:shutil.copyfile(W/old,O/new)
(O/'dependencies.json').write_text(json.dumps(list(D.values()),indent=2)+'\n');(O/'acquired_locator_map.json').write_text(json.dumps(aliases,indent=2)+'\n')
source=dict(original='L033',fixed_source=str(S/'sources/catalogue_L033.pdf'),physical_page=11,claims=[dict(types=['affine B3','affine A3'],source_vector='(2s,0,0)',domain='s>=2',acquired_parameters=dict(k=1,t='2s'),period='2s Z^3'),dict(types=['affine B3','affine A3'],source_vector='(s,s,0)',domain='s>=2',acquired_parameters=dict(k=2,t='s'),period='s D3'),dict(types=['affine B3','affine A3'],source_vector='(2s,2s,2s)',domain='s>=1',acquired_parameters=dict(k=3,t='2s'),period='2s (2Z^3+Z1)')],exhaustion='Source-attributed Ens classification retained; not independently rederived by this adapter',proof_inputs='Complete accepted generalized-halving affine and actual-incidence proofs with their retained classical cubic toroid input')
(O/'source_map.json').write_text(json.dumps(source,indent=2)+'\n')
scope=dict(status='AUTHOR_COMPONENT_REVIEW_PENDING',author='l044_resume',root_role='Assigned exact existing-family interface; no new mathematical proof step supplied',new_contribution='Literal period and marking correspondence with source domains',inherited='Full previously accepted affine and geometric halving proofs; their original authorship retained',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
(O/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
M=dict(schema='human-compression-author-v1',status='AUTHOR_PERIOD_ADAPTER_REVIEW_PENDING',exports=[dict(path=p.name,**h(p)) for p in sorted(O.iterdir())if p.is_file()]);(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n')
print(json.dumps(dict(path=str(O/'manifest.json'),sha256=h(O/'manifest.json')['sha256'],exports=len(M['exports']),dependencies=len(D),aliases=len(aliases))))
