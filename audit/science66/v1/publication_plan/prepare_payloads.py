"""Exact complete L023 transport; no private primary or public mutation."""
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
AUTHOR='corpus106_L023_complete_candidate';REVIEW='corpus106_L023_complete_root_review'
A='audit/recoveries/L023/v1';N='papers/recoveries/L023/v1'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 need(not(HERE/'manifest.json').exists(),'proposal frozen')
 pins={AUTHOR:'369c7a7bea1e2836b949de6cc82dbd02834254c353310ed6cdf5e49cd7902450',REVIEW:a.root_review_pin}
 rows=[];packets=[]
 for directory,pin in pins.items():
  base=a.study/directory;m=load(base/'manifest.json');need(sha(base/'manifest.json')==pin,'accepted packet')
  for name in ['manifest.json']+[x['path'] for x in m['exports']]:
   p=base/name;need(p.suffix!='.md' and not any(x in p.relative_to(base).parts for x in ['sources','private_source','fonts','rasters']),'no primary/Markdown')
   dest=(N+'/'+name if p.suffix in ['.tex','.pdf'] else A+'/author/'+name) if directory==AUTHOR else A+'/root_review/'+name
   rows.append(dict(study_path=directory+'/'+name,public_path=dest,bytes=p.stat().st_size,sha256=sha(p),transport='COPY_FROZEN',whole_file=True))
  dest=A+('/author/' if directory==AUTHOR else '/root_review/')+'manifest.json'
  packets.append(dict(study_manifest=directory+'/manifest.json',manifest=dict(path=dest,bytes=(base/'manifest.json').stat().st_size,sha256=pin),exports=len(m['exports'])))
 # Historical L015 answer is already public; bind exact full theorem and accepted
 # manifest locations, without treating them as new completion proof premises.
 index={}
 for x in load(a.repo/'provenance/publication_manifest.json')['files']:
  if x.get('sha256'):index.setdefault(x['sha256'],[]).append(x['file'])
 historical=[]
 for x in load(a.study/AUTHOR/'historical_question.json')['bindings']:
  candidates=sorted(index.get(x['sha256'],[]),key=lambda n:('/previous/' in n or 'publication_plan' in n,len(n),n))
  need(candidates,'historical accepted result already public');n=candidates[0];p=a.repo/n
  need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'actual historical public bytes')
  historical.append(dict(study_path=x['path'],path=n,bytes=x['bytes'],sha256=x['sha256'],role='HISTORICAL_ANSWER_ONLY_NOT_CURRENT_PROOF_PREMISE'))
 plan=dict(status='PRIVATE_EXACT_WHOLE_PACKET_TRANSPORT',current_pins=pins,files=rows,packets=packets,public_dependencies=historical,unique_public_files=len(rows),new_public_files=len(rows),new_public_bytes=sum(x['bytes'] for x in rows),reused_existing_public_files=0,source_assets_exported=False,manifest_bytes_unchanged=True)
 (HERE/'copy_plan.json').write_text(json.dumps(plan,indent=2)+'\n');print('payloads',len(rows))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);p.add_argument('--root-review-pin',required=True);main(p.parse_args())
