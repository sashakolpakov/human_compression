"""Assemble accepted private publication stages and complete operational reviews.

This copies into a fresh private directory only. It creates no admissions,
catalogue changes or gates. The final configuration must name every exact
accepted handoff; unresolved or absent reviews fail before staging.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path,PurePosixPath
import argparse,gzip,hashlib,json,shutil,subprocess
W=Path(__file__).resolve().parent;S=W.parents[1];R=Path('/Users/sasha/medusa/math_compression')
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,root=None):return dict(path=str(p.relative_to(root))if root else str(p),bytes=p.stat().st_size,sha256=sha(p))
def save(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2)+'\n')
def safe(root,name):
 q=PurePosixPath(name);need(not q.is_absolute()and'..'not in q.parts,'Safe relative path');p=(root/q).resolve();need(p.is_relative_to(root.resolve()),'No escape');return p
def checked(p,r):need(p.is_file()and p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'Exact input '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();config=load(a.config);O=a.out.resolve()
 need(O.is_relative_to(W)and not O.exists(),'Fresh private bundle output');need(config['baseline']=='ade9feeb7f8feaffa8f773932d57a50e60cb64c2','Exact shared baseline');need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==config['baseline'],'Current baseline')
 tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0'))
 ids=[i for p in config['packages']for i in p['source_ids']];need(len(ids)==len(set(ids)),'Separate source dispositions')
 sources={};known={};docs={};package_data=[]
 def add(source,name):
  source=source.resolve();safe(O,name);identity=source.stat().st_size,sha(source)
  if name in sources:need((sources[name].stat().st_size,sha(sources[name]))==identity,'No conflicting stages')
  else:sources[name]=source
  known.setdefault(identity,dict(path=name,bytes=identity[0],sha256=identity[1],encoding='identity',decoded_bytes=identity[0],decoded_sha256=identity[1]))
 for c in config['packages']:
  work=S/c['work'];ready=work/'ready.json';checked(ready,c['ready']);stage=work/c['stage'];mp=work/c['stage_manifest'];checked(mp,c['stage_manifest_pin']);manifest=load(mp)
  proposal=work/c['proposal'];checked(proposal,c['proposal_pin'])
  for r in manifest['files']:
   p=safe(stage,r['path']);checked(p,r);add(p,r['path']);q=R/r['path'];need(not q.exists()or q.read_bytes()==p.read_bytes(),'No public replacement '+r['path'])
  if c.get('transport'):
   t=load(stage/c['transport'])
   for r in t['files']:
    identity=r['bytes'],r['sha256']
    if r['transport'].endswith('HASH_ONLY'):docs[identity]=r;continue
    p=stage/r['public_path']
    if not p.exists():
     p=R/r['public_path'];need(r['public_path']in tracked,'Tracked public reuse');checked(p,dict(bytes=r['stored_bytes'],sha256=r['stored_sha256']))
    known.setdefault(identity,dict(path=r['public_path'],bytes=r['stored_bytes'],sha256=r['stored_sha256'],encoding=r['encoding'],decoded_bytes=r['bytes'],decoded_sha256=r['sha256']))
  op=S/c['operational_review']['packet'];checked(op/'manifest.json',c['operational_review']);om=load(op/'manifest.json');need(om['status']==c['operational_review']['status'],'Accepted operation status')
  inputs={op/'manifest.json'};missing_docs={}
  for r in om['exports']:p=safe(op,r['path']);checked(p,r);inputs.add(p)
  for name in ['dependencies.json','bindings.json']:
   p=op/name
   if not p.exists():continue
   d=load(p);rows=d if isinstance(d,list)else d.get('bindings',[])
   if isinstance(rows,dict):rows=list(rows.values())
   for r in rows:
    if not isinstance(r,dict)or not isinstance(r.get('path'),str)or'sha256'not in r:continue
    name=Path(r['path']);ns=r.get('namespace','study');choices=[name]if name.is_absolute()else[(R if ns in ['repo','public']else S)/name,op/name,work/name]
    matches=[q for q in choices if q.is_file()and sha(q)==r['sha256']and q.stat().st_size==r.get('bytes',q.stat().st_size)]
    if not matches and (r.get('bytes'),r['sha256'])in docs:
     d=docs[r['bytes'],r['sha256']];missing_docs[str(name)]={k:d[k]for k in ['origin','path','bytes','sha256']};continue
    need(matches,'Exact operational dependency '+str(name));inputs.add(matches[0].resolve())
  package_data.append((c,op,om,inputs,missing_docs))
 # Every potentially failing acquisition has been checked before writing.
 O.mkdir();ST=O/'stage';ST.mkdir();AUD=config['audit_base'];maps=[]
 for name,p in sources.items():q=safe(ST,name);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 for c,op,om,inputs,missing_docs in package_data:
  mapping={};excluded=dict(missing_docs);logical=lambda p:str(p.relative_to(S))if p.is_relative_to(S)else str(p)
  for p in sorted(inputs):
   identity=p.stat().st_size,sha(p);key=logical(p)
   if identity in docs:excluded[key]={k:docs[identity][k]for k in ['origin','path','bytes','sha256']};continue
   if identity in known:mapping[key]=known[identity];continue
   name=f"{AUD}/operational/{c['id']}/objects/{sha(p)}{p.suffix}";q=safe(ST,name);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);mapping[key]=dict(pin(q,ST),encoding='identity',decoded_bytes=identity[0],decoded_sha256=identity[1]);known[identity]=mapping[key]
  record=dict(status='EXACT_ACCEPTED_OPERATIONAL_REVIEW',package_id=c['id'],source_ids=c['source_ids'],manifest=mapping[logical(op/'manifest.json')],review=mapping[logical(op/'review.json')],original_manifest_sha256=c['operational_review']['sha256'],original_status=om['status'],bindings=mapping,hash_only_bindings=excluded,mathematical_review_role_unchanged=True)
  dest=ST/AUD/'operational'/c['id']/'mapping.json';save(dest,record);maps.append(pin(dest,ST))
 # Decode each relocated operational dependency independently and check identity.
 for r in maps:
  m=load(ST/r['path'])
  for x in m['bindings'].values():
   p=ST/x['path'];p=p if p.exists()else R/x['path'];checked(p,x);raw=p.read_bytes();raw=gzip.decompress(raw)if x.get('encoding')=='gzip'else raw;need(len(raw)==x['decoded_bytes']and hashlib.sha256(raw).hexdigest()==x['decoded_sha256'],'Exact operational relocation')
 save(O/'accepted_bundle.json',dict(status='PRIVATE_ACCEPTED_PAYLOAD_BUNDLE_NO_REGISTRATION',baseline=config['baseline'],audit_base=AUD,packages=config['packages'],source_ids=ids,operational_reviews=maps,ordinary_recovery_ids=[i for p in config['packages']if p['kind']=='ordinary_recovery'for i in p['source_ids']],principal_refutation_ids=[i for p in config['packages']if p['kind']=='principal_statement_refuted'for i in p['source_ids']],public_writes=False))
 save(O/'stage_manifest.json',dict(status='EXACT_COMBINED_PRIVATE_STAGE',files=[pin(p,ST)for p in sorted(ST.rglob('*'))if p.is_file()],public_writes=False))
 print(json.dumps(dict(status='PRIVATE_BUNDLE_STAGED',sources=ids,stage_files=len(load(O/'stage_manifest.json')['files']),public_writes=False)))
if __name__=='__main__':main()
