"""Lossless private L041 transport, with tracked public reuse only."""
import sys
if sys.flags.optimize: raise RuntimeError('Unoptimized Python required')
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression'
B='audit/recoveries/L041/v1';P='papers/recoveries/L041/v1'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();O=a.out.resolve()
need(not O.exists(),'Fresh stage');j=load(W/'closure_initial.json');need(not j['issues'],'Complete exact closure')
tracked=set(subprocess.check_output(['git','-C',str(R),'ls-files','-z']).decode().split('\0'))
index={};indices=[]
for p in sorted((R/'audit/recoveries').glob('*/v1/transport.json')):
 indices.append(dict(path=str(p.relative_to(R)),**pin(p)))
 for r in load(p)['files']:
  if 'public_path'in r and r['public_path']in tracked:
   index.setdefault((r['bytes'],r['sha256']),{k:r[k]for k in ['public_path','encoding','stored_bytes','stored_sha256']})
rows=j['files'];docs=[];runtime=[]
docnames=['sources/catalogue_L041.pdf','sources/hypertopes_accepted2016.pdf','sources/hypertopes_accepted2016.txt']
docnames += [f'reboot_20261013/L041_work/source_{i:02}.png'for i in [8,14,15,16,19,20]]
docnames += [f'reboot_20261013/L052_general_distinct/source_native/source-15-{i:02}.png'for i in range(1,5)]
native={f'corpus106_L041_decorated_geometry_v2/{name}':f'{P}/decorated-points/{name}'for name in ['decorated_points.tex','decorated_points.pdf','tetrahedra_section.tex']}
for r in rows:
 if r['origin']=='runtime':
  need(r['transport']=='RUNTIME_IDENTITY_HASH_ONLY','Declared runtime identity');runtime.append(dict(origin=r['origin'],path=r['path'],bytes=r['bytes'],sha256=r['sha256'],reason=r['transport']));continue
 if r['origin']=='study'and r['path']in docnames:
  r['transport']='DOCUMENTARY_ASSET_HASH_ONLY';docs.append(dict(origin=r['origin'],path=r['path'],bytes=r['bytes'],sha256=r['sha256'],reason=r['transport']))
 if r['origin']=='public':
  need(r['path']in tracked,'Tracked literal public dependency');index[r['bytes'],r['sha256']]=dict(public_path=r['path'],encoding='identity',stored_bytes=r['bytes'],stored_sha256=r['sha256'])
need(len(docs)==13 and len(runtime)==1,'Exact declared exclusions')
O.mkdir(parents=True);new={};reused={}
for r in sorted(rows,key=lambda r:(0 if r['origin']=='study'and r['path']in native else 1,r['origin'],r['path'])):
 if r['transport'].endswith('HASH_ONLY'):continue
 ident=r['bytes'],r['sha256'];preferred=native.get(r['path'])if r['origin']=='study'else None
 if not preferred and ident in new:r.update(new[ident]);continue
 if not preferred and ident in index:
  z=index[ident];q=R/z['public_path'];need(z['public_path']in tracked and pin(q)==dict(bytes=z['stored_bytes'],sha256=z['stored_sha256']),'Exact Git-tracked reuse')
  reused[z['public_path']]=dict(path=z['public_path'],bytes=z['stored_bytes'],sha256=z['stored_sha256']);r.update(z,transport='EXISTING_PUBLIC');continue
 q=(S if r['origin']=='study'else R)/r['path'];raw=q.read_bytes();need(pin(q)==dict(bytes=r['bytes'],sha256=r['sha256']),'Exact source bytes')
 ext=q.suffix;ext='.txt'if ext=='.md'else'.bin'if ext=='.pyc'else ext
 dest=preferred or f"{B}/objects/{r['sha256'][:2]}/{r['sha256']}{ext}"
 compressed=not preferred and len(raw)>64000 and ext not in ['.pdf','.png','.gz']
 data=gzip.compress(raw,mtime=0)if compressed else raw
 if compressed:dest+='.gz'
 need((gzip.decompress(data)if compressed else data)==raw,'Lossless object')
 p=O/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 z=dict(transport='NEW_FROZEN_FILE',public_path=dest,encoding='gzip'if compressed else'identity',stored_bytes=len(data),stored_sha256=hashlib.sha256(data).hexdigest());new[ident]=z;r.update(z)
policy=dict(documentary_assets=docs,runtime_identities=runtime,
 runtime_treatment='The exact original Python executable is a historical execution identity, not a scientific payload. It is not redistributed or required to have the same hash on another platform. Replay uses the caller ordinary Python 3 with pypdf plus pdflatex and Ghostscript; original programs are byte-identical. No private runtime or original-document fallback exists.',
 historical_absolute_roots=dict(study=str(S)+'/',public=str(R)+'/'),entry_roots=load(W/'entry_roots.json'),
 principal_review_pending=j['review_pending'],collection_boundary=j['collection_boundary'],logical_files=len(rows),private_packets=len(j['packets']),complete_private_exports=sum(p['exports']for p in j['packets']))
T=dict(status='PRIVATE_L041_TRANSPORT_NOT_PUBLIC_ADMISSION',files=rows,packets=j['packets'],**policy,
 public_reuse_indices=indices,tracked_public_reuse=list(reused.values()),baseline=j['baseline'],
 whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0)
save(O/B/'transport.json',T);save(O/B/'portable_policy.json',policy)
save(W/(O.name+'_summary.json'),dict(logical=len(rows),packets=len(j['packets']),exports=policy['complete_private_exports'],new_files=len({r['public_path']for r in rows if r['transport']=='NEW_FROZEN_FILE'}),reused=len(reused),documentary=13,runtime=1,transport=pin(O/B/'transport.json'),policy=pin(O/B/'portable_policy.json')))
print(json.dumps(load(W/(O.name+'_summary.json'))))
