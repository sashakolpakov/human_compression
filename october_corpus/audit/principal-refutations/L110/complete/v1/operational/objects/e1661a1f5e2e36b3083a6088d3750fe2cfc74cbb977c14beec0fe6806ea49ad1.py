from pathlib import Path
import json,subprocess,time
from pypdf import PdfReader
C=Path(__file__).resolve().parent
stems=['completion','realizations']
runs=[]
for rel in stems:
 p=C/rel
 for n in [1,2]:
  cmd=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',p.name+'.tex'];r=subprocess.run(cmd,cwd=p.parent,capture_output=True,timeout=30)
  p.with_name(p.name+'-pass'+str(n)+'.stdout').write_bytes(r.stdout);p.with_name(p.name+'-pass'+str(n)+'.stderr').write_bytes(r.stderr)
  if r.returncode:raise ValueError('build failed '+rel)
  runs.append(dict(stem=rel,pass_number=n,returncode=r.returncode))
order=['completion','proofs/preliminary','proofs/prime_degree','proofs/restrictions','proofs/patterns','realizations','proofs/principal','proofs/markings','proofs/nonthin8','proofs/nonthin32','proofs/local_rank','proofs/standard_subfields','proofs/scalar_subspaces','proofs/common_preliminaries','proofs/normalizer_families','proofs/subfield_families']
parts=[];page=2
for rel in order:
 n=len(PdfReader(C/(rel+'.pdf')).pages)
 parts.append(dict(path=rel+'.pdf',pages=n,first_page=page));page+=n
(C/'parts.json').write_text(json.dumps(parts,indent=2)+'\n')
head=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{pdfpages,hyperref}
\pdfinclusioncopyfonts=1
\begin{document}
\begin{center}{\Large Rank-three Suzuki geometries}\\[5mm]
{\large Complete proofs and source disposition for L114}\end{center}
This volume treats the fixed 1999 article, pp.~43--63. It preserves exact
accepted proof texts. Historical progress statements inside those notes
are superseded by the opening treatment and its current claim ledger.
The final five notes provide explicitly reused common theory. Their
classical structural premises remain attributed; separate L115 numerical
and diagram tables are not imported as proved inputs.\par\medskip
\begin{tabular}{rl}
'''
titles={'completion': 'Results, corrections and source disposition', 'preliminary': 'Preliminary source statements and corrections', 'prime_degree': 'The obstruction in prime field degree', 'restrictions': 'Maximal intersections in torus normalizers', 'patterns': 'Necessary patterns for prime split-torus order', 'realizations': 'Realizations and obstructions for the displayed patterns', 'principal': 'Compatible tori and the omitted geometry', 'markings': 'Eight additional retained markings', 'nonthin8': 'A nonthin geometry over the field of eight elements', 'nonthin32': 'A nonthin geometry over the field of thirty-two elements', 'local_rank': 'Scalar subspaces and unbounded algebraic local rank', 'standard_subfields': 'Standard subfields and the missing boundary', 'scalar_subspaces': 'Scalar subspaces in rank-two Suzuki geometries', 'common_preliminaries': 'Common elementary Suzuki reductions', 'normalizer_families': 'The rank-two normalizer families', 'subfield_families': 'Subfield families and the corrected classification'}
for row in parts:
 title=titles[Path(row['path']).stem]
 title=title.replace('_',' ')
 head+=str(row['first_page'])+' & '+title+r'\\'+'\n'
head+=r'''\end{tabular}
\par\medskip No new original, principal refutation, Lean result or compression
measurement is counted by this assembly. A complete corrected classification
of all Suzuki geometries is not claimed.
\newpage
'''
for row in parts:head+='\\includepdf[pages=-]{'+row['path']+'}\n'
head+='\\end{document}\n';(C/'complete.tex').write_text(head)
for n in [1,2]:
 r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','complete.tex'],cwd=C,capture_output=True,timeout=30)
 (C/('complete-pass'+str(n)+'.stdout')).write_bytes(r.stdout);(C/('complete-pass'+str(n)+'.stderr')).write_bytes(r.stderr)
 if r.returncode:raise ValueError('complete build')
(C/'build_report.json').write_text(json.dumps(dict(runs=runs,pages=len(PdfReader(C/'complete.pdf').pages)),indent=2)+'\n')
print(json.dumps(dict(parts=len(parts),pages=page-1)))
