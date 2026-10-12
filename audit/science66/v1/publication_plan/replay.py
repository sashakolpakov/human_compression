"""Public-only exact packet reconstruction and accepted bounded author replay."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def bound(p,x):need(p.stat().st_size==x['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],'exact bytes '+str(p))
def safe(n):
 p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts,'safe path');return p
def main(a):
 need(not a.out.exists(),'fresh public-only output');a.out.mkdir(parents=True);study=a.out/'logical_study';study.mkdir();plan=load(HERE/'copy_plan.json')
 for x in plan['files']:
  src=a.repo/safe(x['public_path']);bound(src,x);dst=study/safe(x['study_path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for x in plan['public_dependencies']:bound(a.repo/safe(x['path']),x)
 for x in plan['packets']:
  p=study/safe(x['study_manifest']);m=load(p);need(len(m['exports'])==x['exports'],'full packet')
  for y in m['exports']:bound(p.parent/safe(y['path']),y)
 cmd=[sys.executable,'-B','-O',str(study/'corpus106_L023_complete_candidate/check.py'),'--out',str(a.out/'author_replay')]
 if a.render:cmd.append('--render')
 if a.programs:cmd.append('--programs')
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(a.out/'author_stdout.txt').write_text(p.stdout+p.stderr);need(p.returncode==0,'portable author replay')
 r=load(a.out/'author_replay/report.json');need((r['exports'],r['exact_component_copies'],r['source_dispositions'],r['finite_table_rows'],r['whole_program_files'])==(89,76,70,12,12),'complete exact contract')
 need(len(r['controls'])==15 and not r['whole_original_adopted'] and r['new_question_credit']==0 and r['new_factor'] is None,'historical author status/controls')
 if a.render:need(r['native_pages']==19,'all native pages')
 if a.programs:need(r['required_finite_replays']==['polynomial','geometry'],'both required programs')
 review=load(study/'corpus106_L023_complete_root_review/review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['source_id']=='L023','later distinct root acceptance')
 result=dict(status='PASS_PUBLIC_ONLY_COMPLETE_PACKET_REPLAY',logical_files=len(plan['files']),complete_packets=2,author=r,root_scientific_status=review['status'],native_pages=19 if a.render else 0,required_finite_replays=a.programs,primary_assets_restored=False,private_study_fallback=False,new_measurements=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--programs',action='store_true');main(p.parse_args())
