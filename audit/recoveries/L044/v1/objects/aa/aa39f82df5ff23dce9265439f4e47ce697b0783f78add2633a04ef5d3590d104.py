#!/usr/bin/env python3
"""Bounded exact example review, with independently authored coordinate checks."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
from coordinate_check import run as coordinate_run
H=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise ValueError(m)
def bind(p,r):
 b=p.read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'binding '+str(p))
def run(study,out,gap):
 if(H/'manifest.json').exists():
  for r in read(H/'manifest.json')['exports']:bind(H/r['path'],r)
 bs=read(H/'bindings.json')
 for r in bs.values():bind(study/r['path'],r)
 am=study/bs['author']['path'];author=read(am)
 for r in author['exports']:bind(am.parent/r['path'],r)
 r=read(H/'review.json');need(r['status']=='ACCEPTED_BOUNDED_ORBIT_CUT_DIAGNOSTIC'and not r['reviewer_was_author'],'review scope and distinct role')
 need(not r['full_source_theorem_refuted']and not r['full_L044_accepted']and r['new_original_credit']==r['new_question_credit']==r['new_formal_declarations']==0 and r['ratio']is None,'strict bounded conclusion')
 coordinates=coordinate_run();need(coordinates['intersection_pairs']==256 and len(coordinates['controls'])==6,'independent full small verification')
 out.mkdir(parents=True,exist_ok=False);gap_result=None
 if gap:
  cp=out/'author_export_copy';cp.mkdir()
  for x in author['exports']:shutil.copyfile(am.parent/x['path'],cp/x['path'])
  shutil.copyfile(am,cp/'manifest.json')
  p=subprocess.run(['/opt/homebrew/bin/gap','-q','check.g'],cwd=cp,capture_output=True,text=True,timeout=60)
  (out/'author_stdout.log').write_text(p.stdout);(out/'author_stderr.log').write_text(p.stderr)
  need(p.returncode==0 and not p.stderr.strip()and 'PASS_BOUNDED_ORBIT_CUT_OBSTRUCTION'in p.stdout and 'Error'not in p.stdout,'copied small GAP replay')
  need(p.stdout.replace('\r','')==(am.parent/'execution.stdout.log').read_text().replace('\r',''),'exact author stdout')
  gap_result=dict(status='PASS',stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),stderr_empty=True)
 report=dict(status='PASS_DISTINCT_BOUNDED_ORBIT_CUT_REVIEW',author_exports=len(author['exports']),independent_coordinates=coordinates,author_copied_GAP=gap_result,no_large_census=True,no_source_theorem_refutation=True)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--gap',action='store_true');a=p.parse_args();print(json.dumps(run(a.study_root,a.out,a.gap),indent=2))
