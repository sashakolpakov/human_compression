"""Exact F002 transport, reusing only identical already-public projective files."""
from pathlib import Path
import argparse,hashlib,json
P=Path(__file__).resolve().parent
A='corpus106_F002_recovery_v1';R='corpus106_F002_independent_review';D='corpus106_F002_root_adoption'
AUD='audit/recoveries/F002/v1';N='papers/recoveries/F002/v1'
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(a):
 need(not(P/'manifest.json').exists(),'immutable proposal')
 pins={A:'591169a4e8e2625a2c85b217a59c13758554ffd85cbd5624bf048e01e6b667a9',R:'da2627c396da681b4c210dfff3501706ecd80c06b46519332da8874adcc89824',a.adoption_directory:a.adoption_pin}
 rows=[];packets=[]
 for directory,pin in pins.items():
  base=a.study/directory;m=json.loads((base/'manifest.json').read_text());need(sha(base/'manifest.json')==pin,'manifest '+directory)
  tag='author' if directory==A else 'independent_review' if directory==R else 'root_adoption'
  for name in ['manifest.json']+[x['path'] for x in m['exports']]:
   q=base/name;need(q.suffix!='.md' and not any(x in Path(name).parts for x in ['sources','fonts','rasters','private_source']),'no primary assets')
   dest=AUD+'/'+tag+'/'+name;kind='COPY_FROZEN'
   if directory==A and name.startswith('retained/projective/'):
    dest=name.removeprefix('retained/projective/');kind='EXISTING_PUBLIC'
    need((a.repo/dest).is_file() and sha(a.repo/dest)==sha(q),'exact existing dependency '+dest)
   elif directory==A and name in ['marked_search.tex','marked_search.pdf','degree_eleven.tex','degree_eleven.pdf']:
    dest=N+'/'+name
   rows.append(dict(study_path=directory+'/'+name,public_path=dest,bytes=q.stat().st_size,sha256=sha(q),transport=kind,whole_file=True))
  packets.append(dict(study_manifest=directory+'/manifest.json',manifest=dict(path=AUD+'/'+tag+'/manifest.json',bytes=(base/'manifest.json').stat().st_size,sha256=pin),exports=len(m['exports'])))
 need(len({x['study_path']for x in rows})==len(rows),'logical uniqueness')
 destinations={}
 for r in rows:
  if r['public_path'] in destinations:need(destinations[r['public_path']]==(r['bytes'],r['sha256']),'shared bytes')
  destinations[r['public_path']]=(r['bytes'],r['sha256'])
 new=[r for r in rows if r['transport']=='COPY_FROZEN']; reused=[r for r in rows if r['transport']=='EXISTING_PUBLIC']
 need(len(reused)==380,'full inherited closure')
 data=dict(status='PRIVATE_EXACT_WHOLE_PACKET_TRANSPORT',current_pins=pins,author_directory=A,independent_review_directory=R,root_review_directory=a.adoption_directory,files=rows,packets=packets,public_dependencies=[dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])for r in reused],unique_public_files=len(destinations),new_public_files=len(new),new_public_bytes=sum(r['bytes']for r in new),reused_existing_public_files=len(reused),source_assets_exported=False,manifest_bytes_unchanged=True,reuse_scope='All author, distinct-review and root-adoption exports reconstruct exactly. The complete 380-file projective closure uses identical current public routes; it is acquired, not omitted. No private proof fallback.')
 (P/'copy_plan.json').write_text(json.dumps(data,indent=2)+'\n');print({k:data[k]for k in ['unique_public_files','new_public_files','reused_existing_public_files']})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);p.add_argument('--adoption-directory',default=D);p.add_argument('--adoption-pin',required=True);main(p.parse_args())
