"""Restore exact F008 logical packets and optionally build all15 native pages."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(s):
 p=PurePosixPath(s);need(not p.is_absolute() and '..'not in p.parts,'safe path');return p
def main(a):
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 plan=load(HERE/'copy_plan.json')
 for r in plan['files']:
  src=a.repo/safe(r['public_path']);need(src.stat().st_size==r['bytes'] and sha(src)==r['sha256'],'public payload')
  dest=a.out/'packets'/safe(r['packet'])/safe(r['logical_path']);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
 for p in plan['packets']:
  d=a.out/'packets'/p['id'];m=load(d/'manifest.json')
  need(len(m['exports'])==p['exports'],'whole packet')
  for r in m['exports']:need((d/r['path']).stat().st_size==r['bytes'] and sha(d/r['path'])==r['sha256'],'logical bytes')
 author=a.out/'packets/author'
 proc=subprocess.run([sys.executable,'-B','-O',str(author/'check.py'),'--out',str(a.out/'bindings')],capture_output=True,text=True,timeout=60)
 (a.out/'binding_stdout.txt').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'author bounded bindings')
 review=load(a.out/'packets/root_review/review.json');need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['source_rows']==36 and not review['all_literal_source_assertions_reproved'],'actual root scope')
 pages=[]
 if a.render:
  from pypdf import PdfReader
  for row in load(HERE/'native_catalogue.json')['new_documents']:
   stem=Path(row['tex']).stem;folder=a.out/'native'/stem;folder.mkdir(parents=True)
   shutil.copyfile(a.repo/row['tex'],folder/(stem+'.tex'))
   for i in range(2):
    p=subprocess.run([a.pdflatex,'-halt-on-error','-interaction=nonstopmode',stem+'.tex'],cwd=folder,capture_output=True,text=True,timeout=60)
    (folder/f'pass{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'native pdfLaTeX')
   log=(folder/(stem+'.log')).read_text();need(not any(s in log for s in ['Overfull','undefined','LaTeX Warning:']),'native diagnostics')
   now=[p.extract_text() or '' for p in PdfReader(folder/(stem+'.pdf')).pages]
   old=[p.extract_text() or '' for p in PdfReader(a.repo/row['pdf']).pages]
   need(now==old and len(now)==row['physical_pages'],'exact native whole page text')
   pages.append(dict(id=row['id'],pages=len(now),exact_page_text=True))
 report=dict(status='PASS_PUBLIC_ROUTE_RECONSTRUCTION',files=len(plan['files']),packets=len(plan['packets']),author=load(a.out/'bindings/report.json'),native_pages=pages,mathematical_programs_rerun=False,source_extraction_or_Lean_rerun=False,root_science_status=review['status'])
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
