from pathlib import Path
import json, subprocess
from pypdf import PdfReader

C=Path(__file__).resolve().parent

def build(stem):
    for n in (1,2):
        r=subprocess.run(['/opt/homebrew/bin/pdflatex','-recorder','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=C,capture_output=True,timeout=30)
        (C/f'{stem}-pass{n}.stdout').write_bytes(r.stdout)
        (C/f'{stem}-pass{n}.stderr').write_bytes(r.stderr)
        if r.returncode: raise ValueError('failed TeX build '+stem)
    log=(C/(stem+'.log')).read_text()
    if 'Overfull' in log or 'undefined' in log: raise ValueError('new document warning '+stem)

build('completion')
order=json.loads((C/'order.json').read_text())
parts=[];page=2
for part in order:
    count=len(PdfReader(C/(part['path']+'.pdf')).pages)
    parts.append(dict(path=part['path']+'.pdf',title=part['title'],pages=count,first_page=page))
    page+=count
(C/'parts.json').write_text(json.dumps(parts,indent=2)+'\n')
s=r'''\documentclass[11pt]{article}
\usepackage[margin=27mm]{geometry}\usepackage{pdfpages,hyperref}
\pdfinclusioncopyfonts=1
\begin{document}
\begin{center}{\Large Rank two projective geometries}\\[4mm]
{\large Complete source treatment and shared proofs for L063 and L064}\end{center}
The published Part II article and the retained appendix are separately
registered originals. Their individual claim ledgers accompany this
volume. The opening manuscript identifies every correction and the
classical premises; the following papers contain the full proofs.
The omitted affine family and all previously accepted components are
reused without repeating their acquisition. Earlier scope statements
inside those exact components retain their historical wording; the
opening manuscript records their completed source joins. No new
principal-refutation count, compression ratio or Lean verification is
claimed.\par\medskip
\small\begin{tabular}{rp{.84\textwidth}}
'''
for p in parts:s+=str(p['first_page'])+' & '+p['title']+r'\\'+'\n'
s+=r'\end{tabular}\newpage'+'\n'
for p in parts:s+='\\includepdf[pages=-]{'+p['path']+'}\n'
s+='\\end{document}\n'
(C/'complete.tex').write_text(s)
build('complete')
if len(PdfReader(C/'complete.pdf').pages)!=page-1:raise ValueError('cover spill')
print(json.dumps(dict(parts=len(parts),pages=page-1)))
