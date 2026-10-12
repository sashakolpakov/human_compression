"""Restore all three exact F002 packets using only mapped public files."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
P=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def safe(n):
 q=PurePosixPath(n);need(not q.is_absolute()and'..'not in q.parts,'safe path');return q
def bound(p,r):need(p.stat().st_size==r['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],'binding '+str(p))
def main(a):
 need(not a.out.exists(),'fresh replay directory');a.out.mkdir(parents=True);study=a.out/'logical_study';study.mkdir();plan=load(P/'copy_plan.json')
 for r in plan['files']:
  src=a.repo/safe(r['public_path']);bound(src,r);dst=study/safe(r['study_path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for packet in plan['packets']:
  p=study/safe(packet['study_manifest']);m=load(p);need(len(m['exports'])==packet['exports'],'full packet');
  for r in m['exports']:bound(p.parent/safe(r['path']),r)
 author=study/plan['author_directory'];review=study/plan['independent_review_directory']
 cmd=[sys.executable,'-B','-O',str(author/'check.py'),'--out',str(a.out/'author_replay')]
 if a.render:cmd.append('--render')
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(a.out/'author.stdout').write_text(p.stdout);(a.out/'author.stderr').write_text(p.stderr);need(p.returncode==0,'complete public-only author replay '+p.stderr)
 r=load(a.out/'author_replay/report.json');need((r['exports'],r['retained_whole_files'],r['even_involutions'],r['full_subset_IP_checks'])==(414,380,18315,132),'whole census')
 need(r['transitive_markings_by_rank']=={'3':130,'4':2,'5':0}and r['source_bindings']is None,'exact portable scope')
 if a.render:need([x['pages']for x in r['render']]==[2,2],'whole new manuscripts')
 p=subprocess.run([sys.executable,'-B','-O',str(review/'check.py'),'--author',str(author),'--out',str(a.out/'distinct_replay')],capture_output=True,text=True,timeout=60)
 (a.out/'distinct.stdout').write_text(p.stdout);(a.out/'distinct.stderr').write_text(p.stderr);need(p.returncode==0,'distinct portable replay '+p.stderr)
 rr=load(a.out/'distinct_replay/report.json');need(rr['review_exports']==18 and len(rr['independent_controls'])==8,'complete distinct review')
 adoption=load(study/plan['root_review_directory']/'adoption.json');need(adoption['original_id']=='F002'and adoption['whole_original_credit']==1,'root scientific adoption')
 report=dict(status='PASS_PUBLIC_ONLY_COMPLETE_PACKET_REPLAY',logical_files=len(plan['files']),complete_packets=3,reused_public_files=380,author=r,distinct=rr,native_pages=4 if a.render else 0,required_new_finite_census_repeated=True,old_projective_computations_repeated=False,primary_assets_restored=False,private_study_fallback=False,new_measurements=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['author','distinct']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--render',action='store_true');main(p.parse_args())
