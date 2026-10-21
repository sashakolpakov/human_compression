"""Private F001 transport inventory with explicit acquired proof boundaries."""
from pathlib import Path
import argparse, hashlib, json
S=Path(__file__).resolve().parents[2]; R=S.parents[1]/'math_compression'
def need(ok,s):
 if not ok: raise ValueError(s)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 need(not a.out.exists(),'fresh inventory required')
 existing={}
 for p in sorted((R/'audit/recoveries').glob('*/v*/transport.json')):
  for row in json.loads(p.read_text()).get('files',[]):
   if 'public_path' in row: existing.setdefault((row['bytes'],row['sha256']),row)
 # L031 predates the generic transport format. Index its existing complete
 # author packet and readable native documents directly, without copying.
 for base in ['audit/recoveries/L031/v1','papers/recoveries/L031/v1']:
  for p in sorted((R/base).rglob('*')):
   if p.is_file():
    key=(p.stat().st_size,sha(p));existing.setdefault(key,dict(public_path=str(p.relative_to(R)),encoding='identity',stored_bytes=key[0],stored_sha256=key[1]))
 files={};packets=[]
 def add(relative,expected=None,role='explicit required binding'):
  p=(S/relative).resolve();need(p.is_relative_to(S) and p.is_file(),'missing/outside '+relative);need(p.suffix!='.md','working Markdown is not public evidence')
  row=files.get(relative)
  if row is None:
   row=dict(origin='study',path=relative,bytes=p.stat().st_size,sha256=sha(p),role=role)
   if relative.startswith('sources/'):row['transport']='PRIVATE_PRIMARY_SOURCE_HASH_ONLY'
   elif (row['bytes'],row['sha256']) in existing:
    old=existing[(row['bytes'],row['sha256'])];q=(R/old['public_path']).resolve();need(q.is_relative_to(R.resolve()) and q.stat().st_size==old['stored_bytes'] and sha(q)==old['stored_sha256'],'changed public evidence')
    row.update(transport='EXISTING_PUBLIC',**{k:old[k] for k in ['public_path','encoding','stored_bytes','stored_sha256']})
   else:row['transport']='NEW_FROZEN_FILE'
   files[relative]=row
  if expected:need(row['sha256']==expected['sha256'] and ('bytes' not in expected or row['bytes']==expected['bytes']),'changed pin '+relative)
 def packet(name,read_bindings=False):
  add(name+'/manifest.json',role='whole frozen acquired edition');m=json.loads((S/name/'manifest.json').read_text())
  for row in m['exports']:
   q=Path(row['path']);need(not q.is_absolute() and '..' not in q.parts,'export escapes');add(name+'/'+row['path'],row,'complete manifest export')
  packets.append(dict(origin='study',path=name+'/manifest.json',sha256=sha(S/name/'manifest.json'),exports=len(m['exports'])))
  if read_bindings:
   for filename in ['dependencies.json','bindings.json']:
    p=S/name/filename
    if p.exists():
     for row in json.loads(p.read_text()).get('bindings',[]):add(row['path'],row)
 acquired=json.loads((S/'corpus106_F001_principal_v1/dependencies.json').read_text())['required_acquired_manifests']
 names=['corpus106_F001_principal_v1']+[str(Path(p).parent) for p in acquired]+['corpus106_F006_Dn_v2','corpus106_F006_Dn_independent_review','corpus106_F006_complete_root_adoption']
 missing=[]
 if a.whole_review:
  need((S/a.whole_review/'manifest.json').is_file(),'whole review not frozen');names.append(a.whole_review)
 else:missing=['F001 complete principal review/adoption by root']
 for name in names:packet(name,name.startswith('corpus106_F001'))
 # The distinct mixed review records its full checked selection, including
 # exact S5/S6 proof/program/receipt interfaces. Preserve this selection;
 # do not recursively enlarge historical manifests inside F006's edition.
 for row in json.loads((S/'corpus106_F001_mixed_bound_root_review/integrity.json').read_text())['checks']:add(row['path'],row,'mixed review checked acquired selection')
 for row in json.loads((S/'corpus106_F001_rank_bound_v1/provenance.json').read_text())['source_bindings']:add(row['path'],row,'auxiliary source binding')
 rows=sorted(files.values(),key=lambda r:r['path'])
 result=dict(status='PRIVATE_F001_TRANSPORT_INVENTORY_NOT_ADMISSION',files=rows,packets=packets,logical_files=len(rows),missing_final_reviews=missing,primary_sources_hash_only=[r['path'] for r in rows if r['transport'].endswith('HASH_ONLY')],new_uncompressed_bytes=sum(r['bytes'] for r in rows if r['transport']=='NEW_FROZEN_FILE'),source_assets_exported=False,whole_original_credit=0,
  acquired_boundary='Entire F001 components/reviews; complete L031/L037 and Dn selected editions. Inner historical manifests do not expand their containing edition. Exact required S5/S6 interfaces remain present. F006 whole adoption is acceptance provenance, not a claim that all Coxeter censuses are F001 premises.',
  correction='Source arbitrary-subgroup Lemma4.1 is separately refuted; principal Theorem1.1 recovered. No whole-source theorem-set equivalence or conjecture/Lean/factor claim.')
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['files','packets']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--whole-review');main(p.parse_args())
