"""Publish exact L091 content routes; no scientific targets or public edits.

The accepted pack codec and prior Archive reader are copied unchanged.  The
resource allowance is the explicit 4 GiB reserve approved for this operation;
the unchanged codec's legacy error string still says 8 GiB.
"""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,shutil,time,subprocess
import pack_codec as codec
P=Path(__file__).resolve().parent;H=P.parent;S=H.parents[1]
R=Path('/Users/sasha/medusa/math_compression')
PREFIX='audit/recoveries/L091/v1';PAPER='papers/recoveries/L091/v1'
ROOT_SHA='3ac722a21723c2a712bfb0f98b3490880a86e74fbcdb0ba26f46cd62fb6b8131'
RESERVE=4*2**30
need=codec.need
def load(p):return json.loads(p.read_text())
def pin(p):n,h=codec.digest_file(p);return dict(path=str(p),bytes=n,sha256=h)
def exact(p,r):need(codec.digest_file(p)==(r['bytes'],r['sha256']),'unchanged exact input '+str(p))
def write_bytes(p,data):
 need(not p.exists(),'fresh publication file')
 need(shutil.disk_usage(p.parent).free>=RESERVE+len(data),'4 GiB reserve before metadata write')
 with p.open('xb') as f:f.write(data)
def write_json(p,value,compact=False):
 text=json.dumps(value,separators=(',',':')) if compact else json.dumps(value,indent=2)
 write_bytes(p,(text+'\n').encode())
def copy_exact(src,dst):
 need(not dst.exists(),'fresh readable publication file')
 need(shutil.disk_usage(dst.parent).free>=RESERVE+src.stat().st_size,'4 GiB reserve before readable copy')
 shutil.copyfile(src,dst)
def origin(p):
 p=Path(p)
 if p.is_relative_to(S):return 'study',str(p.relative_to(S))
 if p.is_relative_to(R):return 'public',str(p.relative_to(R))
 return 'external',str(p)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 start=time.monotonic();need(a.out.is_absolute() and not a.out.exists(),'fresh absolute stage')
 Q=H/'principal_root_review';A=H/'principal_synthesis_v1';root=pin(Q/'manifest.json')
 need(root['sha256']==ROOT_SHA and load(Q/'manifest.json')['status']=='ACCEPTED_COMPLETE_CORRECTED_L091_SOURCE_DISPOSITION','accepted exact L091 disposition')
 inventory=load(P/'inventory01.json');measurement=load(P/'measurement01.json');premises=load(P/'premises.json')
 need(inventory['root_acceptance']==measurement['root']==premises['root']==root,'same accepted closure')
 exact(P/'inventory01.json',measurement['inventory']);exact(P/'premises.json',measurement['premise_inventory'])
 rows=load(Q/'dependencies.json')
 for r in load(Q/'manifest.json')['exports']:rows.append(dict(r,path=str(Q/r['path'])))
 rows.append(root);logical={r['path']:r for r in rows}
 need(len(logical)==len(rows) and rows==inventory['logical_files'],'complete unchanged logical inventory')
 unique=inventory['unique_contents'];reuse=inventory['reuse_candidates']
 prior={r['sha256']:r for r in premises['premises']};measured={r['sha256']:r for r in measurement['objects']}
 need(set(unique)==set(reuse)|set(prior)|set(measured),'all measured exact contents')
 need(not(set(reuse)&set(prior) or set(reuse)&set(measured) or set(prior)&set(measured)),'disjoint routes')
 need(len(prior)==len(premises['premises']) and len(measured)==len(measurement['objects']),'unique route inventories')
 # Includes the compact transport, readable native files and replay reserve.
 bound=measurement['new_stored_bytes']+100*2**20
 need(shutil.disk_usage(a.out.parent).free>=RESERVE+bound,'measured publication fits existing 4 GiB reserve')
 tracked=set(subprocess.run(['git','-C',str(R),'ls-files','-z'],check=True,capture_output=True).stdout.decode().split('\0'))
 public_files={}
 for est in reuse.values():
  files={r['path']:r for r in est['public_files']}
  for seg in est['segments']:
   name=seg['path'];need(name in files and name in tracked,'exact tracked old segment')
   if name in public_files:need(public_files[name]==files[name],'same complete public file')
   else:public_files[name]=files[name];exact(codec.resolve(name,[R]),files[name])
 # No payload has been written until the complete-file reuse audit succeeds.
 need(shutil.disk_usage(a.out.parent).free>=RESERVE+bound,'reserve still available before payload')
 a.out.mkdir();D=a.out/PREFIX;D.mkdir(parents=True)
 writer=codec.Writer(a.out,PREFIX+'/packs',reserve=RESERVE)
 objects={}
 for i,(sha,r) in enumerate(unique.items()):
  if sha in reuse:
   est=reuse[sha]
   rec={k:est[k] for k in ['kind','bytes','sha256','encoding','stored_bytes','stored_sha256','segments']}
   need((rec['bytes'],rec['sha256'])==(r['bytes'],sha),'exact reuse object identity')
   codec.verify(rec,[R]);objects[sha]=rec
  elif sha in prior:
   p=prior[sha];need(p['bytes']==r['bytes'],'exact premise length')
   objects[sha]=dict(kind=p['kind'],sha256=sha,bytes=p['bytes'],exact_locator=p['exact_locator'],reason=p['reason'])
  else:
   est=measured[sha];need(est['bytes']==r['bytes'],'exact measured source length')
   rec=writer.add(r['path'],r,est['encoding']);need(rec['stored_bytes']==est['stored_bytes'],'exact measured stream length')
   objects[sha]=dict(rec,kind='NEW_PACKED_EXACT_CONTENT')
  if i%5000==0:print(json.dumps(dict(objects=i,total=len(unique),seconds=time.monotonic()-start)),flush=True)
 packs=writer.finish();need(sum(r['bytes'] for r in packs)==measurement['new_stored_bytes'],'entire measured new payload')
 routes=[]
 for r in rows:o,n=origin(r['path']);routes.append(dict(origin=o,path=n,original_path=r['path'],bytes=r['bytes'],sha256=r['sha256']))
 transport=dict(status='PRIVATE_L091_EXACT_TRANSPORT_PENDING_DISTINCT_OPERATIONAL_REVIEW',format='L091_SEGMENTED_EXACT_CONTENT_V1',root_acceptance=root,
  author_manifest=pin(A/'manifest.json'),logical_files=routes,objects=objects,packs=packs,existing_public_files=list(public_files.values()),
  premises=premises['premises'],measured_storage=pin(P/'measurement01.json'),premise_inventory=pin(P/'premises.json'),
  new_scientific_targets=0,whole_original_registration_credit=0,mathematical_compression_measurement=None)
 write_json(D/'transport.json',transport,compact=True)
 for n in ['pack_codec.py','prior_transport_reader.py','portable_check.py','codec_controls.py','portable_controls.py','premises.json','selected_inputs.json','native_streams.json']:
  copy_exact(P/n,D/n)
 paper=a.out/PAPER;paper.mkdir(parents=True)
 for r in load(A/'manifest.json')['exports']:
  n=r['path']
  if n.endswith(('.tex','.pdf')) or n in ['claims.json','source_catalogue.json','corrections.json','disposition.rst']:
   src=A/n;exact(src,r);dest=paper/n;dest.parent.mkdir(parents=True,exist_ok=True);copy_exact(src,dest)
 for row in load(P/'selected_inputs.json')['native']:
  for r in row['adjacent_inputs']:
   src=Path(r['path']);exact(src,r);dest=paper/r['relative_to_author']
   if dest.exists():exact(dest,r)
   else:dest.parent.mkdir(parents=True,exist_ok=True);copy_exact(src,dest)
 copy_exact(P/'PUBLICATION.rst',paper/'PUBLICATION.rst')
 write_json(D/'roles.json',dict(author='/root/j3_recovery',mathematical_authority=root,operational_review='pending',
  exact_prior_transport='pack_codec.py, codec_controls.py and the prior Archive reader are unchanged from L070 publication_work.',
  resource_reserve_bytes=RESERVE,legacy_codec_error_text='The unchanged codec says 8 GiB; its explicit numeric reserve argument is 4 GiB.',
  no_public_mutation=True,no_bulk_restore=True,no_new_scientific_target=True))
 exports=[]
 for p in sorted(a.out.rglob('*')):
  if p.is_file():r=pin(p);r['path']=str(p.relative_to(a.out));exports.append(r)
 manifest=dict(status='PRIVATE_L091_PUBLICATION_STAGE_PENDING_OPERATIONAL_REVIEW',exports=exports,root_acceptance=root,new_scientific_targets=0)
 write_json(D/'manifest.json',manifest)
 result=dict(status='STAGED_EXACT_L091_PRIVATE_PAYLOAD',manifest=pin(D/'manifest.json'),transport=pin(D/'transport.json'),
  logical_files=len(rows),unique_objects=len(objects),new_pack_files=len(packs),new_pack_bytes=sum(r['bytes'] for r in packs),
  new_stage_files=len(exports)+1,new_stage_bytes=sum(r['bytes'] for r in exports)+(D/'manifest.json').stat().st_size,
  existing_public_files=len(public_files),explicit_premise_hashes=len(prior),seconds=time.monotonic()-start)
 (P/(a.out.name+'_receipt.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
