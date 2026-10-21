"""Public-only exact L017 reconstruction, finite replay and all native builds."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def bound(p,x):need(p.stat().st_size==x['bytes']and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],'exact bytes '+str(p))
def safe(n):
 p=PurePosixPath(n);need(not p.is_absolute()and'..'not in p.parts,'safe path');return p
def main(a):
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);study=a.out/'logical_study';study.mkdir();plan=load(HERE/'copy_plan.json')
 for x in plan['files']:
  src=a.repo/safe(x['public_path']);bound(src,x);dst=study/safe(x['study_path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for x in plan['packets']:
  p=study/safe(x['study_manifest']);m=load(p);need(len(m['exports'])==x['exports'],'whole packet')
  for y in m['exports']:bound(p.parent/safe(y['path']),y)
 cmd=[sys.executable,'-B','-O',str(study/plan['author_directory']/'check.py'),'--out',str(a.out/'author_replay')]
 if a.render:cmd.append('--render')
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=120);(a.out/'author_stdout.txt').write_text(p.stdout+p.stderr);need(p.returncode==0,'public-only author replay: '+p.stdout+p.stderr)
 r=load(a.out/'author_replay/report.json');need((r['whole_export_bindings'],r['exact_inherited_files'],r['source_dispositions'],r['named_source_results'],r['fresh_finite_outputs'],r['actual_full_automorphism_certificates'])==(93,40,53,13,17,6),'whole accepted scope')
 need(len(r['negative_controls'])==14 and r['source_marking_q7_exhaustion']==336 and r['q7_representatives']==7 and not r['exact_primary_bound'],'exact finite scope/no source fallback')
 need(r['new_scientific_credit']==r['new_questions']==r['new_lean']==0 and r['ratios']is None,'no inferred new credits')
 if a.render:need([x['pages']for x in r['native']]==[6,4,3,3],'all whole native pages')
 review=load(study/plan['root_review_directory']/'review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY'and review['source_id']=='L017'and review['remaining_principal']==[],'later whole acceptance')
 result=dict(status='PASS_PUBLIC_ONLY_COMPLETE_PACKET_REPLAY',logical_files=len(plan['files']),complete_packets=2,reused_public_files=plan['reused_existing_public_files'],author=r,root_scientific_status=review['status'],native_pages=16 if a.render else 0,finite_computations_repeated=True,unchanged_predecessor_computations_repeated=False,primary_assets_restored=False,private_study_fallback=False,new_measurements=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='author'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');main(p.parse_args())
