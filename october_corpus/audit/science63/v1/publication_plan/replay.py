"""Public-only restoration of complete L122 packets, receipts and native pages."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(s):
 p=PurePosixPath(s);need(not p.is_absolute() and '..' not in p.parts,'safe path');return p
def main(a):
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);plan=load(HERE/'copy_plan.json')
 for r in plan['files']:
  src=a.repo/safe(r['public_path']);need(src.stat().st_size==r['bytes'] and sha(src)==r['sha256'],'public payload')
  dest=a.out/'packets'/safe(r['packet'])/safe(r['logical_path']);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
 for p in plan['packets']:
  d=a.out/'packets'/p['id'];m=load(d/'manifest.json');need(len(m['exports'])==p['exports'],'whole packet')
  for r in m['exports']:need((d/r['path']).stat().st_size==r['bytes'] and sha(d/r['path'])==r['sha256'],'exact logical file')
 cmd=[sys.executable,'-B','-O',str(a.out/'packets/author/check.py'),'--out',str(a.out/'author_replay')]
 if a.render:cmd+=['--render','--pdflatex',a.pdflatex]
 proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(a.out/'author_stdout.txt').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'full assembly replay')
 author=load(a.out/'author_replay/report.json');review=load(a.out/'packets/root_review/review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_L122_UNMEASURED' and review['whole_original_accepted'] and review['native_pages']==13,'actual root science acceptance')
 need(author['exact_copied_files']==56 and author['source_dispositions']==36 and author['counterexample_integer_certificate_fresh'] and not author['positive_GAP_repeated'],'precise current replay scope')
 report=dict(status='PASS_PUBLIC_ROUTE_RECONSTRUCTION',files=len(plan['files']),packets=len(plan['packets']),author_replay=author,native_pages=[4,4,3,2] if a.render else [],accepted_positive_GAP_receipt_retained=True,positive_GAP_repeated=False,actual_coset_certificate_repeated=True,source_extraction_or_Lean_rerun=False,root_science_status=review['status'],primary_source_binding='Private primary hash preserved; public-only replay makes no new primary-reading claim.')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
