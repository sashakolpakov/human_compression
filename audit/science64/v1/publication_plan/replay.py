"""Public-only restoration of the exact L015 accepted packets and native pages."""
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
 if a.optional:cmd+=['--optional']
 proc=subprocess.run(cmd,capture_output=True,text=True,timeout=180);(a.out/'author_stdout.txt').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'full accepted packet replay')
 author=load(a.out/'author_replay/report.json');review=load(a.out/'packets/root_review/review.json')
 need(review['decision']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['original']=='L015' and review['whole_native_pages']==[4,6,4] and review['author_manifest_sha256']==sha(a.out/'packets/author/manifest.json'),'actual root science acceptance')
 need(author['exports']==21 and author['source_rows']==45 and author['whole_common_copies']==2 and len(author['semantic_negative_controls'])==12 and author['external_bindings']==0,'precise current replay scope')
 if a.render:need([x['pages'] for x in author['native_documents']]==[4,6,4],'all native pages')
 report=dict(status='PASS_PUBLIC_ROUTE_RECONSTRUCTION',files=len(plan['files']),packets=len(plan['packets']),author_replay=author,native_pages=[4,6,4] if a.render else [],required_finite_programs=0,optional_diagnostic_repeated=a.optional,source_extraction_or_Lean_rerun=False,root_science_status=review['decision'],primary_source_binding='Private primary hash preserved; public-only replay makes no new primary-reading claim.')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--optional',action='store_true');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
