#!/usr/bin/env python3
"""Two-pass isolated reader build; no source PDFs copied into the build directory."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
from pypdf import PdfReader
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='xelatex');a=p.parse_args()
if a.out.exists():raise ValueError('fresh output directory required')
a.out.mkdir(parents=True);shutil.copy2(R/'input_reader.tex',a.out/'input_reader.tex')
for n in (1,2):
 r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','input_reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'pass{n}.stdout').write_text(r.stdout+r.stderr)
 if r.returncode:raise ValueError('XeLaTeX failure')
log=(a.out/'input_reader.log').read_text();bad=[x for x in log.splitlines()if any(k in x for k in ['Missing character','Overfull','Warning:','! LaTeX'])]
if bad:raise ValueError(bad)
pdf=a.out/'input_reader.pdf';pages=[x.extract_text()or''for x in PdfReader(pdf).pages]
if any(ord(c)<32 and c not in '\n\t\r'or c=='\ufffd'for t in pages for c in t):raise ValueError('unexpected reader glyph')
d={'status':'PASS','pages':len(pages),'tex_sha256':hashlib.sha256((R/'input_reader.tex').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest()for t in pages],'diagnostics':bad}
if (R/'input_reader.pdf').exists():
 old=[x.extract_text()or''for x in PdfReader(R/'input_reader.pdf').pages]
 if old!=pages:raise ValueError('page text differs from frozen reader')
 d['frozen_page_text_equal']=True
(a.out/'render_report.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
