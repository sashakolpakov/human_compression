"""Whole immutable L017 transport with exact existing L023 acquisition."""
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;AUTHOR='corpus106_L017_recovery';REVIEW='corpus106_L017_complete_root_review'
A='audit/recoveries/L017/v1';N='papers/recoveries/L017/v1'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def main(a):
 need(not(HERE/'manifest.json').exists(),'proposal frozen')
 pins={AUTHOR:'80b951a401196484342b9f2778f587c5e129978681aa878490de2eba300b66a3',REVIEW:'c08fca2b12bd6ef8f1e9a73b09718bad16bbc3a152857895c52c5293e22a7bc3'}
 old=load(a.repo/'audit/science66/v1/publication_plan/copy_plan.json')
 existing={x['study_path']:x['public_path']for x in old['files']}
 prefixes={'odd_completion':'components/odd_completion','odd_review':'components/odd_completion_review','equations':'components/polynomial','equations_review':'components/polynomial_review'}
 rows=[];packets=[]
 for directory,pin in pins.items():
  b=a.study/directory;m=load(b/'manifest.json');need(sha(b/'manifest.json')==pin,'accepted packet '+directory)
  for name in ['manifest.json']+[x['path']for x in m['exports']]:
   p=b/name;need(p.suffix!='.md' and not any(x in Path(name).parts for x in ['sources','private_source','fonts','rasters']),'no primary/Markdown export')
   mode='COPY_FROZEN';dest=(N+'/'+name if p.suffix in ['.tex','.pdf']else A+'/author/'+name)if directory==AUTHOR else A+'/root_review/'+name
   if directory==AUTHOR and name.startswith('accepted_inputs/'):
    parts=Path(name).parts;kind=parts[1];tail='/'.join(parts[2:])
    key=('corpus106_L023_complete_root_review/'+tail if kind=='whole_L023_review' else 'corpus106_L023_complete_candidate/'+prefixes[kind]+'/'+tail)
    dest=existing[key];q=a.repo/dest;need(q.stat().st_size==p.stat().st_size and sha(q)==sha(p),'exact reused '+name);mode='EXISTING_PUBLIC'
   rows.append(dict(study_path=directory+'/'+name,public_path=dest,bytes=p.stat().st_size,sha256=sha(p),transport=mode,whole_file=True))
  packets.append(dict(study_manifest=directory+'/manifest.json',manifest=dict(path=A+('/author/'if directory==AUTHOR else'/root_review/')+'manifest.json',bytes=(b/'manifest.json').stat().st_size,sha256=pin),exports=len(m['exports'])))
 need(len(set(x['public_path']for x in rows))==len(rows),'unique destinations')
 d=dict(status='PRIVATE_EXACT_WHOLE_PACKET_TRANSPORT',current_pins=pins,author_directory=AUTHOR,root_review_directory=REVIEW,files=rows,packets=packets,public_dependencies=[],unique_public_files=len(rows),new_public_files=sum(x['transport']=='COPY_FROZEN'for x in rows),new_public_bytes=sum(x['bytes']for x in rows if x['transport']=='COPY_FROZEN'),reused_existing_public_files=sum(x['transport']=='EXISTING_PUBLIC'for x in rows),source_assets_exported=False,manifest_bytes_unchanged=True,reuse_scope='All 93 author exports and complete root review reconstruct exactly. Both whole L023 three-page proofs and exact associated reviews are acquired at existing byte-identical routes; no free dependency or predecessor census rerun.')
 (HERE/'copy_plan.json').write_text(json.dumps(d,indent=2)+'\n');print({k:d[k]for k in ['unique_public_files','new_public_files','reused_existing_public_files']})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
