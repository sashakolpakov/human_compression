#!/usr/bin/env python3
"""Bounded binding, independent diagnostic and native-render replay."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,shutil
from pypdf import PdfReader
R=Path(__file__).resolve().parent

def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((R/n).read_text())
def run(args,cwd=None):
 p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 need(p.returncode==0,p.stdout[-4000:]);return p.stdout

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args()
 need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
 m=read('manifest.json')
 for x in m['exports']:
  p=R/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'export '+x['path'])
 b=read('bindings.json')
 for k in ['reviewed_tex','reviewed_pdf']:need(sha(R/b[k]['path'])==b[k]['sha256'],k)
 if a.study_root:
  for x in b['source']:need(sha(a.study_root/x['path'])==x['sha256'],'source '+x['path'])
 run([sys.executable,'-B','-O',str(R/'independent_matrix_check.py'),'--out',str(a.out/'diagnostic.json')])
 result=json.loads((a.out/'diagnostic.json').read_text());result.pop('elapsed_seconds',None)
 need(result==read('independent_result.json'),'independent matrix results')
 pages=0
 if a.render:
  build=a.out/'native';build.mkdir();shutil.copyfile(R/'reviewed/cubic_generation.tex',build/'cubic_generation.tex')
  for i in range(2):(build/f'run{i}.log').write_text(run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','cubic_generation.tex'],build))
  log=(build/'cubic_generation.log').read_text();need(log.count('Overfull')==1 and 'Overfull \\hbox (4.62306pt too wide) in paragraph at lines 16--23' in log and not any(x in log for x in ['Underfull','LaTeX Warning']),'native diagnostics')
  hashes=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(build/'cubic_generation.pdf').pages]
  need(hashes==b['reviewed_pdf']['page_text_sha256'],'native page texts');pages=len(hashes)
 report={'status':'PASS_BOUNDED_DISTINCT_REVIEW','manifest_sha256':sha(R/'manifest.json'),'exports':len(m['exports']),'source_bindings':len(b['source']) if a.study_root else 0,'field_cases':5,'discriminating_controls':4,'native_page_texts':pages,'whole_L023_acceptance':False,'finite_proof_premise':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
