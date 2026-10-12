"""Public-only exact L018 reconstruction; optional full search and native builds."""
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
 cmd=[sys.executable,'-B','-O',str(study/plan['author_directory']/'check.py'),'--out',str(a.out/'author_replay'),'--validate']
 if a.render:cmd.append('--render')
 if a.programs:cmd.append('--programs')
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=7200 if a.programs else 180);(a.out/'author_stdout.txt').write_text(p.stdout+p.stderr);need(p.returncode==0,'public-only author replay: '+p.stdout+p.stderr)
 r=load(a.out/'author_replay/report.json');need((r['exports'],r['source_rows'],r['square_cases'],r['rectangle_cases'],r['case_routes'])==(50,36,103,11126,11229),'whole accepted scope')
 need(len(r['controls'])==9 and len(r['compiled_whole_programs'])==5,'all complete programs and controls')
 scope=load(study/plan['author_directory']/'scope.json');need(scope['new_original_credit']==scope['new_questions_answered']==scope['new_lean']==scope['new_factors']==0,'no inferred new credits')
 if a.render:need([x['pages']for x in r['native']]==[5,3],'all whole native pages')
 need(r['saved_receipts_reused']==(not a.programs),'actual finite replay mode')
 if a.programs:need(r['fresh_exhaustive_unique_cases']==11210,'actual finite executions')
 else:need(r['fresh_exhaustive_unique_cases']==0,'no unclaimed full rerun')
 review=load(study/plan['root_review_directory']/'review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY'and review['source_id']=='L018'and review['remaining_principal']==[],'later whole acceptance')
 result=dict(status='PASS_PUBLIC_ONLY_COMPLETE_PACKET_REPLAY',logical_files=len(plan['files']),complete_packets=2,reused_public_files=0,author=r,root_scientific_status=review['status'],native_pages=8 if a.render else 0,finite_computations_repeated=a.programs,saved_finite_receipts_used=not a.programs,ordinary_compiler_validation_repeated=True,unchanged_predecessor_computations_repeated=False,primary_assets_restored=False,private_study_fallback=False,new_measurements=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='author'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--programs',action='store_true');main(p.parse_args())
