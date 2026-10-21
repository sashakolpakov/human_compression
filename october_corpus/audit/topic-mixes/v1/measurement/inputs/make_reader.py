#!/usr/bin/env python3
"""Make the complete two-page input reader; no factors are evaluated."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
def make():
 p=json.loads((H/'policy.json').read_text());r=json.loads((H/'author_counts.json').read_text())
 labels={'F005':'Complete historical article','U':'Common theory','A1':'Local application','A2':'Exceptional two-orbit application','CODE1':'Main complete program appendix','CODE2':'Exceptional complete program appendix'}
 rows=[]
 for k,d in r['documents'].items():
  m=d['metrics'];vals=[m[v]['NFC']['characters_without_whitespace']for v in p['variants']]
  rows.append(labels[k]+' & '+str(d['pages'])+' & '+' & '.join(f'{v:,}'for v in vals)+r' \\')
 raw=[]
 for category,title in [('programs','Mathematical files'),('drivers','Operational files'),('formal','Scoped formal file')]:
  for name,d in r['raw_files'][category].items():
   short=Path(name).name.replace('_',r'\_');role={'check_coprime.g':'Required finite certificate','check_single_base.py':'Six-coordinate validation','check_exceptional.py':'Exceptional affine validation'}.get(Path(name).name,title)
   if Path(name).name=='check.py':role='Main replay driver' if 'recovery/'in name else 'Additive replay driver'
   elif Path(name).name=='check_integrity.py':role='Integrity controls'
   raw.append(r'\texttt{'+short+'} & '+role+' & '+f"{d['metrics']['NFC']['characters_without_whitespace']:,}"+r' \\')
 return TEMPLATE.replace('@DOCROWS@','\n'.join(rows)).replace('@RAWROWS@','\n'.join(raw))
TEMPLATE=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=24mm]{geometry}
\usepackage{fontspec,booktabs,array,amsmath,hyperref}
\setmainfont{STIXGeneral}\setmonofont{Menlo}[Scale=0.83]
\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Complete measurement inputs for the mix criteria}\\[4pt]
Human Compression project\quad---\quad F005 input audit\end{center}

This packet fixes the text and program boundaries for one complete historical
article: Cunningham and Hubard, \emph{Polytopality criteria for the mix of
polytopes and maniplexes}, arXiv:2506.19334v1, 24 June 2025. All 21 physical pages
are included. The comparison will use the entire common paper, the entire local
application and the entire exceptional-case addition. No part of that addition
is free prior work, and there is no overlap or cross-topic deduction.

\textbf{The primary coordinate was fixed before counting:} NFC characters
without whitespace in the literal, untrimmed PDF extraction. All original and
replacement documents use this same rule. Page footers and the source's arXiv
banner therefore remain in the primary counts. No ratio is evaluated here.

\begin{center}\small
\begin{tabular}{@{}p{64mm}rrrr@{}}\toprule
Whole document & Pages & Raw & Selected & Calibrated\\\midrule
@DOCROWS@
\bottomrule\end{tabular}\end{center}

The last three columns show NFC characters without whitespace. ``Selected''
removes only each isolated physical page footer. ``Calibrated'' additionally
substitutes individually inspected visible glyphs, leaving the same number of
nonspace characters here but sometimes changing their UTF-8 cost. Neither
column changes the primary boundary. The complete machine-readable inventory
records five units, NFC and NFKC, and all three variants: 180 PDF cells across
six documents. The five units are whitespace tokens, alphanumeric units,
characters without whitespace, characters with collapsed whitespace, and
UTF-8 bytes with collapsed whitespace.

\textbf{Scientific scope.} The bound main packet has 35 detailed source rows;
these are not 35 originals. Its additive application settles the literal
claims recorded as R23 and R29 by counterexamples and gives precise rooted
replacement criteria. All three final source problems remain unanswered and
excluded from the recovery claim. Other corrections, qualifications and
retained inputs remain exactly those of the bound scientific records. The
measurement author also authored the mathematics; distinct scientific
acceptance is now bound to both unchanged scientific editions. Distinct
measurement-input review is still required before factors may be calculated.

\textbf{Whole program alternatives.} The two complete printed appendices have
seven pages in total. Their raw alternative consists of the three whole
mathematical files listed on the next page. Printed and raw forms are
alternatives: they must never be added together. Any later conditional
application comparison must declare the whole common theory and all three
mathematical programs already paid. Drivers and partial formal evidence are
inventoried separately, without silently folding them into those programs.

\newpage
\begin{center}{\large Executable boundaries and representation limits}\end{center}
\begin{center}\small
\begin{tabular}{@{}p{54mm}p{71mm}r@{}}\toprule
Whole raw file & Role & NFC nonspace\\\midrule
@RAWROWS@
\bottomrule\end{tabular}\end{center}

The GAP file is a required finite certificate for the eleven-cell and simplex
markings in the coprime-label obstruction. Both Python mathematical files
validate complete written coordinate arguments; they do not replace the
uniform proofs. Full-file inclusion in the two existing appendices is checked
against the literal source bytes, with no line pruning or abbreviated output.
All seven raw files have both normalizations and all five units recorded
(70 cells). The Lean file contains two generic fiber declarations; this is
not an end-to-end formalization of the geometry, finite groups or source.

\textbf{Actual fonts and pages.} The author viewed all 45 scientific and code
pages and 27 exceptional embedded glyph outlines. The source has 23 actual
Type1 font dictionaries and 469 encoded glyph classes. One replacement code
appendix also has a Type1 dictionary with five classes; 18 replacement Type0
dictionaries retain their literal extraction. Nine visually identified source
aliases occur 1,210 times. They affect only the calibrated sensitivity. In
particular a decoded mapsto component is retained as an inspected bar-and-stem
glyph, not reconstructed into a guessed composite mathematical arrow.

The extractor pins \texttt{pypdf 6.13.0} and \texttt{fontTools 4.63.0}. It
checks the returned raw text against ordinary uninstrumented extraction,
records the original font and byte events for every substitution, and keeps
generated line breaks separate from actual glyph events. There is no Form
callback duplication in these inputs. Forty rejection controls exercise the
whole-document boundary, code roles and completeness, forbidden discounts,
source qualifications, literal extraction and glyph substitutions.

\textbf{What the counts do not measure.} Source diagrams on pages 9 and 11
and displayed path relations on page 14 contain graphical information. Their
extractable labels and literal text proxies remain counted; strokes, color
and spatial placement have no established full cost. The historical software,
retained external proofs and full formalization costs are likewise unknown,
not zero. The figures have not been replaced by invented textual equivalents.
The font substitutions are a representation sensitivity, not an estimate of
these missing costs.

The portable replay accepts explicit source and public-artifact roots and
verifies complete PDF, program and scientific-manifest hashes. It exports no
historical article text, font bytes or page images. Optional isolated TeX
rebuilds check the reader and both complete code appendices; the input audit
does not rerun the mathematical GAP or Lean proofs. Whole-source scientific
coverage, measurement-input acceptance and a subsequent numerical comparison
remain separate decisions.
\end{document}
'''
if __name__=='__main__':(H/'input_reader.tex').write_text(make())
