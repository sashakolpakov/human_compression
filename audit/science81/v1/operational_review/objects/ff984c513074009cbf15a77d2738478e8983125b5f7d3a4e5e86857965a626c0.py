"""Lossless private payload staging; root retains the public write gate."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
from pathlib import Path
import gzip,hashlib,json,collections
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression';BASE='audit/recoveries/L120/v1';PAPERS='papers/recoveries/L120/v1';O=W/'stage01'
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def need(x,m):
 if not x:raise ValueError(m)
cache={}
def pin(p):
 if p not in cache:
  h=hashlib.sha256();n=0
  with p.open('rb')as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  cache[p]={'bytes':n,'sha256':h.hexdigest()}
 return cache[p]
j=json.loads((W/'closure_resolved.json').read_text());need(not j['issues'],'All exact locators resolved');rows=j['files'];rowmap={(r['origin'],r['path']):r for r in rows}
primary=[
'sources/survey2021.pdf','sources/survey2021.txt','sources/sporadic2022.pdf','sources/sporadic2022.txt',
'reboot_20261013/L120_recovery_work/survey-final.tex',
'reboot_20261013/L120_recovery_work/hypermap_audit/cps2008.pdf','reboot_20261013/L120_recovery_work/hypermap_audit/cps2008.txt',
'reboot_20261013/L120_recovery_work/vicinsky2009.pdf','reboot_20261013/L120_recovery_work/vicinsky2009.txt',
'corpus106_L120_finite_method_independent_review/source_table1.png',
'reboot_20261013/L120_recovery_work/source_views/survey06.png','reboot_20261013/L120_recovery_work/source_views/survey08.png']
for p in primary:
 need(('study',p)in rowmap,'Explicit primary source');rowmap['study',p]['transport']='PRIVATE_PRIMARY_SOURCE_HASH_ONLY'
# Content-addressed public payload lookup is not additional theorem admission.
# It permits reuse of identical already-public bytes without private fallback.
index={};public_indices=[]
keys=['transport','public_path','encoding','stored_bytes','stored_sha256']
for p in sorted((R/'audit/recoveries').glob('*/v1/transport.json')):
 t=json.loads(p.read_text());public_indices.append({'path':str(p.relative_to(R)),**pin(p)})
 for old in t['files']:
  if old['transport'].endswith('HASH_ONLY'):continue
  q=R/old['public_path'];need(q.is_file()and pin(q)=={'bytes':old['stored_bytes'],'sha256':old['stored_sha256']},'Existing public payload '+str(q))
  d={k:old[k]for k in keys};d['transport']='EXISTING_PUBLIC';index.setdefault((old['bytes'],old['sha256']),d)
for r in rows:
 if r['transport'].endswith('HASH_ONLY'):continue
 if r['transport']=='EXISTING_PUBLIC':
  q=R/r['public_path'];need(pin(q)=={'bytes':r['stored_bytes'],'sha256':r['stored_sha256']},'Prior public bytes');index.setdefault((r['bytes'],r['sha256']),{k:r[k]for k in keys})
 elif r['origin']in('public','repo'):
  q=R/r['path']
  if q.is_file()and pin(q)=={k:r[k]for k in('bytes','sha256')}and q.suffix!='.md':index.setdefault((r['bytes'],r['sha256']),{'transport':'EXISTING_PUBLIC','public_path':r['path'],'encoding':'identity','stored_bytes':r['bytes'],'stored_sha256':r['sha256']})
need(not O.exists(),'Fresh staging directory');O.mkdir()
# Actual .gz files first, so raw transcripts can reuse the same stored stream.
ordered=sorted(rows,key=lambda r:(not r['path'].endswith('.gz'),r['origin'],r['path']))
roundtrips=[]
for i,r in enumerate(ordered):
 if r['transport'].endswith('HASH_ONLY'):continue
 ident=(r['bytes'],r['sha256'])
 if ident in index:r.update(index[ident]);continue
 source_origin=r.get('source_origin',r['origin']);source_root=S if source_origin=='study'else R if source_origin in('public','repo')else None
 need(source_root is not None,'Explicit source namespace');p=source_root/r.get('source_path',r['path']);need(p.is_file()and pin(p)=={k:r[k]for k in('bytes','sha256')},'New exact bytes '+str(p));raw=p.read_bytes();ext='.txt'if p.suffix=='.md'else p.suffix
 if r['path'].startswith('corpus106_L120_principal_v2/')and len(Path(r['path']).parts)==2 and ext in('.tex','.pdf'):dest=PAPERS+'/principal/'+p.name
 else:dest=BASE+'/objects/'+r['sha256'][:2]+'/'+r['sha256']+ext
 compressed=len(raw)>64000 and ext not in('.pdf','.png','.gz')
 stored=gzip.compress(raw,mtime=0)if compressed else raw
 if compressed:dest+='.gz'
 q=O/dest;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(stored);need((gzip.decompress(stored)if compressed else stored)==raw,'Lossless round trip')
 d={'transport':'NEW_FROZEN_FILE','public_path':dest,'encoding':'gzip'if compressed else'identity','stored_bytes':len(stored),'stored_sha256':hashlib.sha256(stored).hexdigest()};r.update(d);index[ident]=d
 if ext=='.gz':
  decoded=gzip.decompress(raw);rawident=(len(decoded),hashlib.sha256(decoded).hexdigest());index.setdefault(rawident,{**d,'encoding':'gzip'});roundtrips.append({'gzip_original':{'origin':r['origin'],'path':r['path']},'decoded_bytes':rawident[0],'decoded_sha256':rawident[1],'stored_path':dest})
 if i%500==0:print('STAGED',i,flush=True)
# If a scientific manuscript happened to share earlier bytes, publish a readable
# TeX/PDF entry without changing the logical exact transport.
for name in('survey.tex','survey.pdf'):
 r=rowmap['study','corpus106_L120_principal_v2/'+name];q=O/(PAPERS+'/principal/'+name)
 if not q.exists():q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((S/'corpus106_L120_principal_v2'/name).read_bytes())
unique={r['public_path']:r for r in rows if not r['transport'].endswith('HASH_ONLY')};new=[r for r in unique.values()if r['transport']=='NEW_FROZEN_FILE'];omitted=[{'origin':r['origin'],'path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'reason':r['transport']}for r in rows if r['transport'].endswith('HASH_ONLY')]
exceptions=[];aliases=[];prior_locators=[]
for p in j['predecessors']:
 m=p['metadata'];exceptions.extend(m.get('historical_documentary_exceptions',[]));prior_locators.extend(m.get('relative_locator_resolutions',[]))
 if 'legacy_common_aliases'in m:aliases.append(m['legacy_common_aliases'])
t={'status':'PRIVATE_L120_PAYLOAD_REQUIRES_DISTINCT_OPERATIONAL_REVIEW_AND_ROOT_PUBLICATION','files':rows,'packets':j['packets'],'predecessor_transports':[{k:v for k,v in p.items()if k!='metadata'}for p in j['predecessors']],'byte_reuse_public_indices':public_indices,'primary_sources_hash_only':omitted,'new_primary_source_paths':primary,'historical_documentary_exceptions':exceptions,'legacy_common_aliases':aliases,'inherited_relative_locators':prior_locators,'relative_locator_resolutions':j['relative_locator_resolutions'],'source_assets_exported':False,'private_mathematical_proof_fallback':False,'public_boundary':j['public_boundary'],'logical_files':len(rows),'unique_public_files':len(unique),'new_public_files':len(new),'new_stored_bytes':sum(r['stored_bytes']for r in new),'whole_original_credit':0,'new_measurements':0,'new_question_credit':0,'new_Lean':0,'mathematical_acceptance':{'author':'b5860c241cb773ae005ba412237f5b30220f7c045f5c90e21a35f2f133cc7831','distinct_root_review':'2478f1609c3ff05aec7ca856c44190042bafcaf169b118266a2f9bea40e09543'}}
save(O/BASE/'transport.json',t);save(W/'gzip_reuse.json',roundtrips);save(W/'new_documentary_omissions.json',[r for r in omitted if r['path']in primary]);print(json.dumps({'files':len(rows),'packets':len(j['packets']),'unique':len(unique),'newfiles':len(new),'newbytes':t['new_stored_bytes'],'omitted':len(omitted),'transport':pin(O/BASE/'transport.json')}))
