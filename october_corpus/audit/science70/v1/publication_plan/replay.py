"""Reconstruct complete accepted N011 packets from only their public routes."""
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
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(a.out/'author_stdout.txt').write_text(p.stdout+p.stderr);need(p.returncode==0,'public-only author replay: '+p.stdout+p.stderr)
 r=load(a.out/'author_replay/report.json');need((r['frozen_exports'],r['source_dispositions'],r['source_table_rows'],r['native_pages'])==(16,57,12,9),'whole accepted scope')
 need(len(r['controls'])==12 and r['required_finite_premises']==0 and r['optional_symbolic_checks']==105,'actual optional and operational replay')
 scope=load(study/plan['author_directory']/'scope.json');need(scope['new_original_credit']==scope['new_conjecture_credit']==scope['new_lean']==scope['new_measurement']==0,'no inferred credit')
 if a.render:need([x['pages']for x in r['renders']]==[2,7],'all whole native pages')
 review=load(study/plan['root_review_directory']/'review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY'and review['author_manifest_sha256']==plan['current_pins'][plan['author_directory']],'later whole acceptance')
 result=dict(status='PASS_PUBLIC_ONLY_COMPLETE_PACKET_REPLAY',logical_files=len(plan['files']),complete_packets=2,reused_public_files=0,author=r,root_scientific_status=review['status'],native_pages=9 if a.render else 0,required_finite_searches_repeated=False,optional_symbolic_validation_repeated=True,primary_assets_restored=False,private_study_fallback=False,new_measurements=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='author'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');main(p.parse_args())
