"""Exact frozen L031 transport; reuse byte-identical published L011 premises."""
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;AUTHOR='corpus106_L031_recovery'
A='audit/recoveries/L031/v1';N='papers/recoveries/L031/v1'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def main(a):
 need(not(HERE/'manifest.json').exists(),'proposal frozen')
 pins={AUTHOR:'f4f522c382d9c24d0d683faaef931ae68e30a71357b9d229a82dda3e135f7c3d',a.root_review_dir:a.root_review_pin}
 reuse={'retained/low_dimension/low_dimension_obstructions.'+ext:'papers/recoveries/L011/v1/low_dimension_obstructions.'+ext for ext in ['tex','pdf']}
 reuse.update({'provenance/L011_author_manifest.json':'audit/recoveries/L011/v1/author/manifest.json','provenance/L011_original_dependencies.json':'audit/recoveries/L011/v1/author/dependencies.json','provenance/L011_original_proof_map.json':'audit/recoveries/L011/v1/author/proof_map.json'})
 for f in (a.repo/'audit/recoveries/L011/v1/root_review').iterdir():
  if f.is_file():reuse['provenance/L011_root_review/'+f.name]=str(f.relative_to(a.repo))
 rows=[];packets=[]
 for directory,pin in pins.items():
  b=a.study/directory;m=load(b/'manifest.json');need(sha(b/'manifest.json')==pin,'accepted packet '+directory)
  for name in ['manifest.json']+[x['path'] for x in m['exports']]:
   p=b/name;need(p.suffix!='.md' and not any(x in Path(name).parts for x in ['sources','private_source','fonts','rasters']),'no source/Markdown transport')
   mode='COPY_FROZEN';dest=(N+'/'+name if p.suffix in ['.tex','.pdf'] else A+'/author/'+name) if directory==AUTHOR else A+'/root_review/'+name
   if directory==AUTHOR and name in reuse:
    dest=reuse[name];mode='EXISTING_PUBLIC';q=a.repo/dest;need(q.stat().st_size==p.stat().st_size and sha(q)==sha(p),'exact existing acquired proof '+dest)
   rows.append(dict(study_path=directory+'/'+name,public_path=dest,bytes=p.stat().st_size,sha256=sha(p),transport=mode,whole_file=True))
  dest=A+('/author/' if directory==AUTHOR else '/root_review/')+'manifest.json'
  packets.append(dict(study_manifest=directory+'/manifest.json',manifest=dict(path=dest,bytes=(b/'manifest.json').stat().st_size,sha256=pin),exports=len(m['exports'])))
 need(len({x['public_path'] for x in rows})==len(rows),'unique actual destinations')
 plan=dict(status='PRIVATE_EXACT_WHOLE_PACKET_TRANSPORT',current_pins=pins,author_directory=AUTHOR,root_review_directory=a.root_review_dir,files=rows,packets=packets,public_dependencies=[],unique_public_files=len(rows),new_public_files=sum(x['transport']=='COPY_FROZEN' for x in rows),new_public_bytes=sum(x['bytes'] for x in rows if x['transport']=='COPY_FROZEN'),reused_existing_public_files=sum(x['transport']=='EXISTING_PUBLIC' for x in rows),source_assets_exported=False,manifest_bytes_unchanged=True,reuse_scope='All 69 author exports and complete distinct review reconstruct exactly; existing L011 native paper/provenance are acquired in full, not free references.')
 (HERE/'copy_plan.json').write_text(json.dumps(plan,indent=2)+'\n');print(json.dumps({k:plan[k] for k in ['unique_public_files','new_public_files','reused_existing_public_files']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);p.add_argument('--root-review-dir',required=True);p.add_argument('--root-review-pin',required=True);main(p.parse_args())
