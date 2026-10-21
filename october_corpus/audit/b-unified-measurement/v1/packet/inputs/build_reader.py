#!/usr/bin/env python3
"""Reproduce the one-page input boundary, not a mathematical measurement input."""
from pathlib import Path
import argparse,json,re,shutil,subprocess,unicodedata
from pypdf import PdfReader
from extract_inputs import need,sha,save
H=Path(__file__).resolve().parent
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh reader output');a.out.mkdir(parents=True);shutil.copy2(H/'reader.tex',a.out/'reader.tex')
 for n in [1,2]:
  r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(a.out/f'pass{n}.log').write_text(r.stdout);need(r.returncode==0,'successful complete XeLaTeX run')
 log=(a.out/'reader.log').read_text();diagnostics=[line for line in log.splitlines() if any(s in line for s in ['Missing character:','Overfull','Underfull','LaTeX Warning:','Package fontspec Warning:'])];need(not diagnostics,'reader diagnostics '+str(diagnostics))
 pages=[p.extract_text() or '' for p in PdfReader(a.out/'reader.pdf').pages];expected=[p.extract_text() or '' for p in PdfReader(H/'reader.pdf').pages];need(pages==expected and len(pages)==1,'complete exact one-page reader text')
 need(not any(unicodedata.category(c)=='Co' or c=='\ufffd' or (unicodedata.category(c)=='Cc' and c not in '\n\t\r') for c in ''.join(pages)),'reader glyph scan')
 save(a.out/'report.json',dict(status='PASS',pages=1,diagnostics=diagnostics,exact_page_text=True,text_sha256=sha('\n'.join(pages).encode()),measurement_input=False))
 print('PASS complete one-page boundary reader; no ratios.')
