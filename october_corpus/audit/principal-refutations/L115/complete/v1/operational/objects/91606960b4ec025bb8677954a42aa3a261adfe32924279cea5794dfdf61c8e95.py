from pathlib import Path
import json,sys,collections
P=Path(__file__).resolve().parent;Z=P.parent;S=Z.parents[1];R=Path('/Users/sasha/medusa/math_compression')
def load(p):return json.loads(p.read_text())
root=Z/'principal_root_review';m=load(root/'manifest.json');rows=load(root/'dependencies.json')+[dict(r,path=str(root/r['path']))for r in m['exports']]
prior={}
for q in [S/'geometry/suzuki_incidence/publication_work/premise_candidates.json',S/'algebra/subgroup_atlas/publication_work/premises02.json']:
 if q.exists():
  z=load(q)
  for x in z.get('premises',[]):prior[x['sha256']]=x
premises=[];unmatched=[]
for r in rows:
 old=prior.get(r['sha256']);p=Path(r['path']);suffix=p.suffix.lower()
 if old:
  kind='PINNED_ENVIRONMENT_OR_LIBRARY_PREMISE'if 'ENVIRONMENT'in old['kind']else 'ORIGINAL_SOURCE_DOCUMENTARY_PREMISE';reason=old['reason']
 elif not p.is_relative_to(S)and not p.is_relative_to(R)and (str(p).startswith('/opt/homebrew/')or str(p).startswith('/Users/sasha/.venvs/')):
  kind='PINNED_ENVIRONMENT_OR_LIBRARY_PREMISE';reason='Acquired executable or installed library; explicit software premise, not project output.'
 elif '/sources/'in str(p) or (suffix in ['.png','.pdf','.txt','.text']and any(t in str(p)for t in ['/source_pages/','/source-page','/source-observation','/source_native/','/native_source','/source/','/source_text.txt','/source.pdf','/source.txt'])):
  kind='ORIGINAL_SOURCE_DOCUMENTARY_PREMISE';reason='Original paper, extraction or native source view; separately cited documentary input, not project proof.'
 elif suffix in ['.png','.txt','.pdf']and (p.name.startswith(('source-','source_','source35_detail','source10','source11','source12')) and not p.name.startswith('source_joins')):
  kind='ORIGINAL_SOURCE_DOCUMENTARY_PREMISE';reason='Exact separately named original-source view or extraction; no project proof or derived table omitted.'
 else:
  if suffix in ['.png','.pdf','.txt','.text']and any(w in str(p).lower()for w in ['source','emis','page','original']):unmatched.append(r)
  continue
 premises.append(dict(r,kind=kind,reason=reason))
result=dict(author_sha256='8c15732e2041adc45ba02f88119c6823673e33272ae2c5526ab3d7dbe83cacf9',premises=premises,documentary_count=sum(r['kind']=='ORIGINAL_SOURCE_DOCUMENTARY_PREMISE'for r in premises),environment_count=sum(r['kind']=='PINNED_ENVIRONMENT_OR_LIBRARY_PREMISE'for r in premises))
(P/'premise_candidates.json').write_text(json.dumps(result,indent=2)+'\n');(P/'premise_unmatched.json').write_text(json.dumps(unmatched,indent=2)+'\n')
print(json.dumps(dict(rows=len(rows),premises=len(premises),unmatched=len(unmatched))))
