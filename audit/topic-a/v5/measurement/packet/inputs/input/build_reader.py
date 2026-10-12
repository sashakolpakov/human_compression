"""Readable complete input boundary; no factors or source bodies."""
from pathlib import Path
import argparse,json,subprocess
H=Path(__file__).resolve().parent
load=lambda n:json.loads((H/n).read_text())
def esc(s):return s.replace('_',r'\_').replace('&',r'\&')
def reader():
 p=load('policy.json');c=load('author_counts.json');d=c['documents'];m=p['primary']['metric']
 def value(k):return d[k]['metrics']['calibrated_selected']['NFC'][m]
 rows=[]
 for src,app in p['source_to_application'].items():
  parts=p['application_documents'][app];rows.append(f'{src} & {d[src]["pages"]} & {value(src):,} & {app} & {sum(d[k]["pages"]for k in parts)} & {sum(value(k)for k in parts):,}'+r'\\')
 common='\n'.join(f'{esc(k)} & {d[k]["pages"]} & {value(k):,}'+r'\\'for k in p['common_documents'])
 roles={}
 for r in c['raw_files_measured'].values():
  q=roles.setdefault(r['accounting_class'],[0,0]);q[0]+=1;q[1]+=r['bytes']
 labels={'required_program':'Required programs','required_data':'Required mathematical data','optional_validation':'Optional validation','operational':'Operational files','partial_formal':'Partial formal files','output_receipt':'Output receipts'}
 rr='\n'.join(f'{labels.get(k,esc(k))} & {v[0]} & {v[1]:,}'+r'\\'for k,v in roles.items())
 newrows=[]
 for key in load('input_spec.json'):
  for v,label in [('raw_untrimmed','complete'),('raw_selected','selected'),('calibrated_selected','calibrated')]:
   for n in ['NFC','NFKC']:
    q=d[key]['metrics'][v][n];newrows.append(f'{esc(key)} & {label} & {n} & '+' & '.join(f'{q[k]:,}'for k in p['metrics'])+r'\\')
 return r'''\documentclass[10pt]{article}
\usepackage[a4paper,margin=18mm]{geometry}
\usepackage{lmodern,booktabs,array,hyperref}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Ten-source A: complete measurement inputs}\\[4pt]
Native manuscripts, calibrated extraction and whole-file inventory\end{center}
The primary coordinate remains calibrated selected PDF text, NFC, characters
excluding whitespace. This packet records inputs only; it calculates no factor.
The five units, two normalizations and three extraction variants give thirty
coordinates for each complete PDF.

The written boundary is ten full sources (152 pages), three complete common
papers (23+14+4 pages), and ten complete applications (63 pages). The additional
three inherited program appendices have 30 pages. Thus the input inventory has
29 native PDFs and 286 physical pages. Title, abstract, body, proofs, tables,
references, addresses and extracted figure labels remain included. Selected
text removes only exact running furniture.

\begin{center}\begin{tabular}{lrrlrr}\toprule
Source & Pages & Characters & Application & Pages & Characters\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
\begin{center}\begin{tabular}{lrr}\toprule
Complete common component & Pages & Characters\\\midrule
'''+common+r'''
\bottomrule\end{tabular}\end{center}
The first eight application PDFs and all their coordinates remain unchanged.
The former eleven-page L121 application is replaced by its complete one-page
adapter; its moved proof is paid in the fourteen-page common supplement.
The L003 application includes all four native companions, of 7, 4, 4 and 2 pages.
The four-page shared structural proof is also part of common acquisition.
The convenience concatenated PDFs are not counted in addition to their parts.

A subsequent whole written comparison must pay all 41 common pages and all
63 application pages. A conditional source/application comparison assumes the
whole common theory and all 99 required program/data contents already acquired,
with retained external mathematical premises explicit. It does not make those
costs zero. No sibling application is a free proof premise.

Exactly 630 inherited PDF cells and 450 inherited whole-file cells are retained.
Eight new native PDFs add 240 PDF cells; 158 new contents add 1,580 raw cells.
The complete vectors contain 870 PDF cells and 2,030 raw cells. These coordinate
counts are not numbers of originals, results or formalized theorems.
\newpage
\begin{center}{\large Evidence, file roles and limits}\end{center}
\begin{center}\begin{tabular}{lrr}\toprule
Disjoint whole-content class & Contents & Exact bytes\\\midrule
'''+rr+r'''
\bottomrule\end{tabular}\end{center}
The 253 declared file occurrences comprise 203 distinct complete contents.
Identical complete bytes are shared only within this topic. All occurrence
roles and paths remain in the inventory. A saved image consumed by a structural
proof is required data even when it also has an output role; overlapping role
labels are not summed as disjoint costs. The disjoint classes above use the
explicit frozen role policy, rather than inference from file names or prose.
The 28 required programs and 71 required data contents remain proof premises;
the five optional validation contents are not silently promoted or substituted.
Operational files, partial formal evidence and output receipts remain disclosed.

The three old printed appendices cover only the former eleven-file computational
subset. They are partial historical representations, not a complete printed
appendix for the enlarged collection. Raw inventories are separate disclosures;
there is no printed-code or software-inclusive factor. Unknown historical
software and external proof-library, catalogue and graphic costs remain unknown.

All 57 pages of the eight new PDFs were visually screened for executable
listings, running furniture and extraction issues. There are no executable
listings to exclude. Mathematical proof and algorithm prose, presentation words,
complete tables and software references remain. The other 21 PDFs inherit their
prior screen only because the complete PDF bytes are identical. This preserves
the symmetric manuscript-only program boundary.

The new actual-font audit aligns 104 Type1 dictionaries and 1,743 encoded
classes. Two hundred twenty-one exceptional outline classes were directly
viewed. The 26 Type0 dictionaries in new replacement PDFs retain their Unicode
extraction with dictionary metadata and page inspection; no Type0 outline
decoding claim is made. Fifty mathematical classes require 462 occurrence-bound
repairs. Each repair binds dictionary, encoding, byte, event, page and context.
Both visible TAB-encoded braces are retained as braces. A mapsto component is
kept separate from its adjacent arrow; generated whitespace is never repaired.

L003 contributes 32 drawing-font classes and 423 actual graphic occurrences.
Their literal extracted aliases are retained, including control characters,
letters and arrow-like codes. LCIRCLE nodes, LINE/XYDASH strokes and half-arrow
components are explicitly tagged as drawing material, not linguistic or
mathematical transcription. Every extracted figure label remains. These values
measure extraction representation length; they do not price geometric structure.
The raw complete and raw selected variants expose this convention. Full graphic
complexity and unextracted visible image text remain unknown, not zero.

The fixed source is the complete 21-page \emph{Hexagonal extensions of toroidal
maps and hypermaps}, by Maria Elisa Fernandes, Dimitri Leemans and Asia Ivi\'c
Weiss. The accepted corrected contract preserves its explicit order, nonsplitting,
local-period and word qualifications. The diagram-(5) experimental flag-
transitivity statement and source questions do not acquire a new solution claim.
Existing partial formal evidence is separately inventoried, not full-source
formalization. This input authorship does not create source or theorem credit.
\newpage
\begin{center}{\large The eight new PDF sensitivity vectors}\end{center}
\begin{center}\scriptsize\setlength{\tabcolsep}{3.2pt}\renewcommand{\arraystretch}{1.04}
\begin{tabular}{lllrrrrr}\toprule
PDF & Selection & Norm. & Tokens & Alphanum. & Nonspace & Collapsed & UTF-8\\\midrule
'''+ '\n'.join(newrows)+r'''
\bottomrule\end{tabular}\end{center}
\small
Tokens are whitespace-separated units; alphanumeric units are maximal Unicode
letter/number runs. Nonspace counts all non-whitespace characters. The last two
columns use whitespace-collapsed text. Exact normalized and collapsed text hashes
accompany the full vectors. No line-hyphen or ordinary-ligature rewriting is
performed; NFC and NFKC remain separate sensitivities.

The pre-count policy and subsequent event/mask freeze preceded all new scoring.
Their earlier pending status is preserved as chronology; the completion receipt
records the completed author input stage. Distinct full-input acceptance is
required before comparison. Primary PDFs, full source text, embedded font bytes
and rasters stay private; scripts, bounded event metadata and counts are exported.
\end{document}
'''
def build(out,engine):
 out.mkdir(parents=True,exist_ok=False);(out/'reader.tex').write_text(reader())
 for _ in range(2):
  r=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  if r.returncode:raise RuntimeError(r.stdout)
 log=(out/'reader.log').read_text();diag=[x for x in log.splitlines()if any(t in x for t in ['Overfull','LaTeX Warning','Missing character','Undefined control'])]
 if diag:raise ValueError(diag)
 return dict(diagnostics=diag)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--xelatex',default='xelatex');v=a.parse_args();print(json.dumps(build(v.out,v.xelatex)))
