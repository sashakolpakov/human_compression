"""Build the input-boundary reader; no ratios or source assets."""
from pathlib import Path
import argparse,json,subprocess,re
H=Path(__file__).resolve().parent
load=lambda n:json.loads((H/n).read_text())
def esc(s):
 for a,b in [('&',r'\&'),('_',r'\_'),('%',r'\%')]:s=s.replace(a,b)
 return s
def reader():
 p=load('policy.json');c=load('author_counts.json');d=c['documents'];m=p['primary']['metric'];rows=[]
 for src,app in p['source_to_application'].items():
  v=d[src]['metrics']['calibrated_selected']['NFC'][m];w=d[app]['metrics']['calibrated_selected']['NFC'][m]
  rows.append(f'{src} & {d[src]["pages"]} & {v:,} & {app} & {d[app]["pages"]} & {w:,}'+r'\\')
 newrows=[]
 for key in ['L121','A9']:
  for v,label in [('raw_untrimmed','raw, complete'),('raw_selected','raw, selected'),('calibrated_selected','calibrated')]:
   for n in ['NFC','NFKC']:
    q=d[key]['metrics'][v][n];newrows.append(f'{key} & {label} & {n} & '+' & '.join(f'{q[k]:,}'for k in p['metrics'])+r'\\')
 raw=load('precount/raw_inventory.json')['files'];roles={}
 for x in raw:
  role='Required programs/data'if x['mathematical_premise']else('Old auxiliaries'if x['role']=='inherited_auxiliary'else('Operational runners'if 'driver'in x['role']or x['role']=='operational_validation_runner'else'Partial formal files'))
  if role not in roles:roles[role]=[0,0]
  roles[role][0]+=1;roles[role][1]+=x['file']['bytes']
 rr='\n'.join(f'{k} & {v[0]} & {v[1]:,}'+r'\\'for k,v in roles.items())
 return r'''\documentclass[10pt]{article}
\usepackage[a4paper,margin=19mm]{geometry}
\usepackage{lmodern,booktabs,array,hyperref}

\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Adding L121 to the complete A input boundary}\\[4pt]
Full manuscripts and complete file inventories\end{center}
The primary coordinate remains calibrated selected PDF text, NFC, characters
excluding whitespace. This document records inputs; it calculates no factor.
All five units, both Unicode normalizations and the raw complete, raw selected
and calibrated selected variants remain available.

The boundary contains nine complete sources (131 pages), the whole unchanged
common paper (23 pages), all nine complete applications (56 pages), and the
three old program appendices (30 pages): 22 PDFs and 240 physical pages.
Title, abstract, proof text, references, addresses and extractable figure labels
are included. Selected text removes only exact running furniture.

\begin{center}\begin{tabular}{lrrlrr}\toprule
Source & Pages & Characters & Application & Pages & Characters\\\midrule
'''+ '\n'.join(rows)+r'''
\midrule
\multicolumn{3}{l}{Whole common paper, U} & & 23 & '''+f'{d["U"]["metrics"]["calibrated_selected"]["NFC"][m]:,}'+r'''\\
\bottomrule\end{tabular}\end{center}
All 600 earlier PDF cells and 300 earlier raw-file cells are preserved exactly.
The two new PDFs add 60 cells and fifteen complete files add 150 cells, giving
660 PDF cells and 450 raw-file cells. A cell is one metric, normalization and
selection coordinate; these are not counts of papers or results.

Any later whole written comparison pays all of U and all nine applications.
Any later individual comparison assumes the whole common paper and the declared
required computational/data and retained mathematical premises have already
been acquired. L121 uses no sibling application as a premise. These acquisition
conditions do not make the program or external-proof cost zero.

\begin{center}\begin{tabular}{lrr}\toprule
Complete raw inventory & Files & Exact bytes\\\midrule
'''+rr+r'''
\bottomrule\end{tabular}\end{center}
The nine new required files are eight complete programs and
\texttt{model\_data.json}; \texttt{cubic\_relation/check.py} is a required coordinate
calculation. Four other new runners are operational. All 45 contents differ,
so there is no within-topic duplicate-content discount.

The old appendices represent only the eleven old computational files.
No printed appendix represents the entire enlarged required collection.
There is no complete printed-code factor and no software-inclusive factor.
Historical source software, including L121's Magma work, remains unpriced.
\newpage
\begin{center}{\large The two new PDF sensitivities}\end{center}
\begin{center}\scriptsize\setlength{\tabcolsep}{3.7pt}
\begin{tabular}{lllrrrrr}\toprule
PDF & Selection & Norm. & Tokens & Alphanum. & Nonspace & Collapsed & UTF-8\\\midrule
'''+ '\n'.join(newrows)+r'''
\bottomrule\end{tabular}\end{center}
``Tokens'' counts whitespace-separated tokens. ``Alphanum.'' counts maximal
Unicode letter/number runs. ``Nonspace'' counts characters excluding whitespace.
The last two columns count characters and UTF-8 bytes after whitespace collapse.
Full exact text hashes accompany the numerical vectors.

The new source is the retained twelve-page author PDF of \emph{Two families of
locally toroidal regular 4-hypertopes arising from toroids}, by Fernandes,
Leemans, Piedade and Ivi\'c Weiss. Its complete eleven-page application is
\emph{Period lattices and locally toroidal hypertopes}. Both entire PDFs were
freshly inspected for running furniture, formula extraction and executable
listings. Neither contains an executable listing; no new code mask is applied.
Mathematical algorithm prose, presentation relators and software references remain.

The actual-font audit reconciles 36 Type1 font dictionaries and 871 encoded
glyph classes. Eighty-eight exceptional classes were viewed as embedded outlines.
There are 18 source and 51 application repair occurrences, in 17 classes.
Each binds its exact dictionary, encoding, byte, text event, page and context.
Six source private-use bracket pieces become their visible Unicode bracket
components. Printable sum, brace, script-letter and blackboard-letter aliases
are repaired locally. The mapsto tail remains a separate component from its
adjacent arrow. Ordinary ligatures and printed line hyphens are preserved;
NFKC is a separate sensitivity.

The source's vector diagrams on pages 5--7 retain extracted labels. Their
edges, layout and geometric content are not priced. All earlier limitations,
including L035's raster material, remain explicit. This is extracted text,
not a complete visible-text or graphic-cost claim. No source PDF, primary body
text, font stream or raster is distributed in the input packet.

The accepted corrected L121 contract has 27 source dispositions; the previous
102 dispositions remain unchanged. They do not create extra originals or
question credit. The six new Lean declarations establish countermodel relations
and two nonconsequences only; they do not formalize the group orders, infinite
families or geometry. Earlier partial-formal scopes are unchanged.

The scientific acceptance chain and fixed precount protocol are bound separately
from the completed input report. Independent input acceptance is a separate
step before numerical comparison. The preserved precount policy records that
no new counts had been evaluated at its earlier freeze; the additive completion
receipt records the present count stage.
\end{document}
'''
def build(out,engine):
 out.mkdir(parents=True,exist_ok=False);tex=reader();(out/'reader.tex').write_text(tex)
 for _ in range(2):
  r=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  if r.returncode:raise RuntimeError(r.stdout)
 log=(out/'reader.log').read_text();diag=[x for x in log.splitlines()if any(t in x for t in ['Overfull','LaTeX Warning','Missing character','Undefined control'])]
 if diag:raise ValueError(diag)
 return dict(diagnostics=diag)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--xelatex',default='xelatex');v=a.parse_args();print(json.dumps(build(v.out,v.xelatex)))
