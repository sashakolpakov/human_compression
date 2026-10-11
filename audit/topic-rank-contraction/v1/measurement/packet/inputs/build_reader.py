#!/usr/bin/env python3
"""Fresh two-pass input-reader build; never executes the mathematical programs."""
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess
from pypdf import PdfReader
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='xelatex');p.add_argument('--compare',action='store_true');a=p.parse_args()
if a.out.exists():raise ValueError('fresh output required')
a.out.mkdir(parents=True);shutil.copy2(H/'reader.tex',a.out/'reader.tex')
for i in range(2):
 q=subprocess.run([a.xelatex,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode','reader.tex'],cwd=a.out,capture_output=True,text=True,timeout=90)
 (a.out/f'render{i}.stdout').write_text(q.stdout);(a.out/f'render{i}.stderr').write_text(q.stderr)
 if q.returncode or 'Output written on' not in q.stdout:raise ValueError('reader build failed')
diag=[l for l in(a.out/'reader.log').read_text().splitlines()if any(x in l for x in ['Overfull','Missing character','Warning:'])]
if diag:raise ValueError(diag)
texts=[page.extract_text()or''for page in PdfReader(a.out/'reader.pdf').pages]
if len(texts)!=2:raise ValueError('reader must have two complete pages')
if a.compare and texts!=[page.extract_text()or''for page in PdfReader(H/'reader.pdf').pages]:raise ValueError('exact reader page text')
r=dict(status='PASS',pages=len(texts),diagnostics=diag,page_text_sha256=[hashlib.sha256(t.encode()).hexdigest()for t in texts],page_text_compared=a.compare)
(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
