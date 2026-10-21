from pathlib import Path
import json,subprocess
from pypdf import PdfReader
C=Path(__file__).resolve().parent
for n in [1,2]:
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','completion.tex'],cwd=C,capture_output=True,timeout=30)
 (C/f'completion-pass{n}.stdout').write_bytes(r.stdout);(C/f'completion-pass{n}.stderr').write_bytes(r.stderr)
 if r.returncode:raise ValueError('completion build')
order=json.loads((C/'order.json').read_text());parts=[];page=2
for rel in order:
 count=len(PdfReader(C/(rel+'.pdf')).pages);parts.append(dict(path=rel+'.pdf',pages=count,first_page=page));page+=count
(C/'parts.json').write_text(json.dumps(parts,indent=2)+'\n')
titles=['Source treatment and corrections','The omitted pure-subfield boundary','Prime-subfield residues do not extend','Obstructions to five prescribed constructions','Scalar fields and split families','Field descent and compatible tori','All prescribed torus parameters','Pure subfields and the mixed scalar obstruction','Diagrams of the surviving families','Scalar subspaces give actual geometries','Preliminary source statements','The prime-degree obstruction','Normalizer restrictions and embedded uniqueness','Necessary prime-degree patterns','Realizations of the rank-three patterns','The omitted rank-three torus family','The nonthin geometry over eight elements','The nonthin geometry over thirty-two elements','The earlier algebraic scalar family','Scalar subspaces and central covers','Common elementary Suzuki reductions','The normalizer families','Corrected subfield families']
s=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}\usepackage{pdfpages,hyperref}
\pdfinclusioncopyfonts=1
\begin{document}
\begin{center}{\Large Higher-rank Suzuki geometries}\\[4mm]
{\large Complete source treatment and proofs for L110}\end{center}
This volume treats the fixed twenty-page higher-rank article. The opening
manuscript and claim ledger give the current disposition. Exact earlier
proofs retain their historical scope statements; the separate scalar
geometry supplement proves the stronger conclusion where indicated.
The final papers are reused common theory, with classical premises
explicitly attributed. No new original, principal-refutation count,
Lean formalization or compression measurement is claimed.\par\medskip
\begin{tabular}{rl}
'''
for p,title in zip(parts,titles,strict=True):s+=str(p['first_page'])+' & '+title+r'\\'+'\n'
s+=r'\end{tabular}\newpage'+'\n'
for p in parts:s+='\\includepdf[pages=-]{'+p['path']+'}\n'
s+='\\end{document}\n';(C/'complete.tex').write_text(s)
for n in [1,2]:
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','complete.tex'],cwd=C,capture_output=True,timeout=30)
 (C/f'complete-pass{n}.stdout').write_bytes(r.stdout);(C/f'complete-pass{n}.stderr').write_bytes(r.stderr)
 if r.returncode:raise ValueError('complete build')
if len(PdfReader(C/'complete.pdf').pages)!=page-1:raise ValueError('unexpected cover spill')
print(json.dumps(dict(parts=len(parts),pages=page-1)))
