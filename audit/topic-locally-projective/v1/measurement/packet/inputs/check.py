#!/usr/bin/env python3
"""Portable bounded input, control and optional reader reproduction."""
from pathlib import Path
from types import SimpleNamespace
import argparse,json,subprocess
import pypdf
import extract_inputs as E
from controls import checks
from build_reader import build

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 E.need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 if (E.HERE/'manifest.json').exists():
  for r in E.load('manifest.json')['exports']:E.bound(r,E.HERE)
 result,_=E.replay(a);E.need(result==E.load('author_counts.json'),'all bound input integers and text hashes reproduced')
 control=checks(a.study_root);E.need(control==E.load('author_controls.json'),'all input/control results reproduced')
 tex=build(result);E.need(tex==(E.HERE/'input_reader.tex').read_text(),'exact integer reader generated');(a.out/'input_reader.tex').write_text(tex)
 render=None
 if a.render:
  for n in [1,2]:
   q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','input_reader.tex'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   (a.out/f'render_pass{n}.txt').write_text(q.stdout);E.need(q.returncode==0,'complete reader render')
  log=(a.out/'input_reader.log').read_text();diagnostics=[s for s in log.splitlines() if any(w in s for w in ['Overfull','Underfull','Missing character','LaTeX Warning','Package fontspec Warning'])];E.need(not diagnostics,'reader diagnostics empty')
  texts=lambda p:[page.extract_text() for page in pypdf.PdfReader(p).pages]
  old=texts(E.HERE/'input_reader.pdf');new=texts(a.out/'input_reader.pdf');E.need(old==new,'every reader page text identical')
  render=dict(pages=len(new),diagnostics=[],page_text_sha256=[E.sha(x.encode()) for x in new])
 for n,obj in [('counts.json',result),('controls.json',control),('report.json',dict(status='PASS',pdf_metric_cells=210,raw_metric_cells=100,semantic_controls=control['semantic_negative_controls'],reader_reproduced=True,render=render,ratio=None,scientific_computation_repeated=False))]:(a.out/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS: 310 complete input cells,25 semantic controls,exact input reader; no ratios.')
if __name__=='__main__':main()
