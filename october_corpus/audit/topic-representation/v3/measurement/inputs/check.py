#!/usr/bin/env python3
from pathlib import Path
import argparse,json,os,shutil,subprocess
import pypdf
from extract_inputs import replay,load,H
from font_tools import need,sha
from controls import controls

def render(out,xelatex):
 target=out/'reader';target.mkdir();shutil.copyfile(H/'input_reader.tex',target/'input_reader.tex');logs=[]
 for i in range(2):
  r=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','input_reader.tex'],cwd=target,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(target/f'pass{i+1}.stdout').write_text(r.stdout);need(r.returncode==0,'reader render');logs.append(r.stdout)
 log=(target/'input_reader.log').read_text(errors='replace');warnings=[x for x in log.splitlines()if any(y in x for y in ['Overfull','Undefined','LaTeX Warning','Missing character','Underfull'])];need(not warnings,'reader diagnostic '+str(warnings))
 pages=[x.extract_text()or''for x in pypdf.PdfReader(target/'input_reader.pdf').pages];old=[x.extract_text()or''for x in pypdf.PdfReader(H/'input_reader.pdf').pages];need(pages==old and len(pages)==2,'all two frozen reader pages');return dict(pages=2,diagnostics=warnings,matched_exact_page_text=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh replay directory');a.out.mkdir(parents=True)
 result,cache=replay(a);need(result==load('author_counts.json'),'all180PDF/170raw cells and36PDF/34raw hashes match frozen author counts');mutations=controls(a,cache);report=dict(status='PASS_AUTHOR_COMPLETE_INPUT_REPLAY_NOT_ACCEPTANCE',PDF_cells=180,new_PDF_cells=150,inherited_source_cells=30,raw_cells=170,controls=mutations,ratios=None)
 if a.render:report['render']=render(a.out,a.xelatex)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=report['status'],PDF_cells=180,raw_cells=170,controls=len(mutations),render=report.get('render'))))
