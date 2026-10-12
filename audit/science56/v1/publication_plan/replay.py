"""Rebuild exact L102 logical packets from public routes; no new mathematical run."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def need(t,m):
 if not t:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(name):
 p=PurePosixPath(name);need(not p.is_absolute()and '..'not in p.parts and str(p)==name,'safe path');return p
def main(a):
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 plan=load(HERE/'copy_plan.json')
 for r in plan['files']:
  src=a.repo/safe(r['public_path']);need(src.stat().st_size==r['bytes']and sha(src)==r['sha256'],'exact public payload')
  dst=a.out/'packets'/safe(r['packet'])/safe(r['logical_path']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for p in plan['packets']:
  d=a.out/'packets'/p['id'];m=load(d/'manifest.json');need(len(m['exports'])==p['exports'],'whole packet')
  for e in m['exports']:need((d/e['path']).stat().st_size==e['bytes']and sha(d/e['path'])==e['sha256'],'exact logical file')
 d=a.out/'packets/L102_author';cmd=[sys.executable,'-B','-O',str(d/'check.py'),'--out',str(a.out/'bounded')]
 if a.render:cmd.append('--render')
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=60);(a.out/'author_stdout.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'bounded author replay')
 accepted=load(a.out/'packets/L102_review/review.json')
 need(accepted['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY'and accepted['source_items']==35 and accepted['new_question_credit']==accepted['new_Lean']==0,'distinct root scope')
 report=dict(status='PASS_PUBLIC_ROUTE_RECONSTRUCTION',files=47,packets=2,author=load(a.out/'bounded/report.json'),source_programs_rerun=False,extraction_or_Lean_rerun=False,root_scientific_review=accepted['status'])
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');main(p.parse_args())
