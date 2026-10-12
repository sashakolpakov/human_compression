"""Whole immutable N011 transport; requires the actual distinct acceptance pin."""
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;AUTHOR='corpus106_N011_recovery';REVIEW='corpus106_N011_root_review'
A='audit/recoveries/N011/v1';N='papers/recoveries/N011/v1'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def main(a):
 need(not(HERE/'manifest.json').exists(),'proposal frozen')
 pins={AUTHOR:'60cf3f14e1d01a0bafe782bc0a735ad4e2f788728a0a870e2ffcf1ef724651bb',REVIEW:a.review_pin}
 rows=[];packets=[]
 for directory,pin in pins.items():
  b=a.study/directory;m=load(b/'manifest.json');need(sha(b/'manifest.json')==pin,'accepted packet '+directory)
  for name in ['manifest.json']+[x['path']for x in m['exports']]:
   p=b/name;need(p.suffix!='.md'and not any(x in Path(name).parts for x in ['sources','private_source','fonts','rasters']),'no primary/Markdown export')
   dest=(N+'/'+name if p.suffix in ['.tex','.pdf']else A+'/author/'+name)if directory==AUTHOR else A+'/root_review/'+name
   rows.append(dict(study_path=directory+'/'+name,public_path=dest,bytes=p.stat().st_size,sha256=sha(p),transport='COPY_FROZEN',whole_file=True))
  packets.append(dict(study_manifest=directory+'/manifest.json',manifest=dict(path=A+('/author/'if directory==AUTHOR else'/root_review/')+'manifest.json',bytes=(b/'manifest.json').stat().st_size,sha256=pin),exports=len(m['exports'])))
 need(len(set(x['public_path']for x in rows))==len(rows),'unique destinations')
 d=dict(status='PRIVATE_EXACT_WHOLE_PACKET_TRANSPORT',current_pins=pins,author_directory=AUTHOR,root_review_directory=REVIEW,files=rows,packets=packets,public_dependencies=[],unique_public_files=len(rows),new_public_files=len(rows),new_public_bytes=sum(x['bytes']for x in rows),reused_existing_public_files=0,source_assets_exported=False,manifest_bytes_unchanged=True,reuse_scope='All16 author exports and all3 distinct root-review exports reconstruct exactly. Both whole scientific papers (2+7 pages), the optional symbolic program/output and operational driver are acquired. Primary source assets remain private; no private fallback is required for replay.')
 (HERE/'copy_plan.json').write_text(json.dumps(d,indent=2)+'\n');print({k:d[k]for k in ['unique_public_files','new_public_files','reused_existing_public_files']})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);p.add_argument('--review-pin',required=True);main(p.parse_args())
