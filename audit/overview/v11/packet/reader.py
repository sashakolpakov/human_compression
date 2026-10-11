"""Compact additive reader; displays only carried, currently available factors."""
from pathlib import Path
from build import read

def render_text(r):
 rows=[]
 for t in r['topics']:
  value=t['written']['decimal']if t['written']is not None else r'\textemdash'
  status='unchanged'if t['written']is not None else 'held'
  rows.append(f"{t['topic']} & {t['source_count']} & {value} & {status} \\\\")
 table='\n'.join(rows)
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,booktabs,array,hyperref}
\setmainfont{STIXGeneral}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\begin{document}
\begin{center}{\Large Current comparison: listing correction}\\[4pt]
An additive qualification of published overview v10\end{center}
Three whole-topic factors and three conditional factors are withdrawn from the current comparison. Their source manuscripts contain concrete program or search-pseudocode blocks while corresponding replacement programs were excluded as separate files. The old costs and fractions are retained as historical observations; the affected current factors are null. No manuscript has been remeasured and no new fraction has been calculated.
\begin{center}\small\begin{tabular}{lll}\toprule
Whole topic held & Conditional row held & Source listing location\\\midrule
Chamber & L008 & Section 5, physical pages 8--10\\
ChiralEnumeration & L028 & Section 4.2, physical pages 9--12\\
Operations & N006 & Theorem 5.3 proof, physical page 20\\\bottomrule
\end{tabular}\end{center}
These blocks implement proof computations or algorithms; they are not relabeled optional validation. Calling a program required does not justify counting its executable text only in the source. Surrounding proof, mathematical algorithm prose, presentations and numerical tables remain mathematical content. No entire source section is deleted or discounted here.

The final bounded listing audit covers the eighteen non-F topic boundaries; the separately accepted expanded-F screen is reused. It identifies 16 available whole-topic factors and 40 available conditional factors. The unaffected N016, N005 and N007 conditional rows remain available after acquisition of their entire common theory and actual required premises. Holding a topic sum does not automatically invalidate an unaffected local source/application comparison.

All 19 topic records and all 43 original records remain in the current JSON and CSV tables. The programme still has 43 admitted recoveries among 106 accessible originals, with 63 pending; the 55 archived originals are unchanged. This is a numerical-boundary correction, not withdrawal of accepted mathematics or a change in source credit.

\textbf{Current graphs.} \href{whole_topics.pdf}{Whole topics},
\href{conditional_1.pdf}{conditional rows 1--22} and
\href{conditional_2.pdf}{conditional rows 23--43} retain complete observed source/common/application bars for available rows. A held row has no numeric bars and reads ``awaiting matched code boundary''. Previous v10 plots remain historical and must be read with this correction; they are not current unqualified comparison plots.

\textbf{Repair boundary.} A later edition may identify exact matching executable-block masks on both sides and recount without dropping surrounding mathematics. A complete software-inclusive comparison would instead require matched source and replacement software inventories. Neither repair is performed here. Unknown original software costs, external proofs and graphics remain unknown. Every optional-validation or software-inclusive factor remains null.
\newpage
\section*{Complete current topic table}
All displayed values below are copied from v10. They compare complete manuscript costs under each row's published extraction convention; they do not estimate minimum proof complexity. Whole common theory remains fully charged once within each topic. There is no free overlap with another topic and no pooled factor.
\begin{center}\small\begin{tabular}{lrrl}\toprule
Topic & Originals & Current written factor & Status\\\midrule
'''+table+r'''
\bottomrule\end{tabular}\end{center}
\textbf{Full tables.} \href{topics.csv}{topics.csv} contains all 19 topic records;
\href{applications.csv}{applications.csv} contains all 43 conditional records.
Each has distinct current and historical factor columns. A current null is not a zero. Full old common, application, source and declared program costs remain unchanged in the data. The complete original v10 results and tables are retained under \texttt{inputs/}.

A conditional factor always assumes the whole common theory and declared required dependencies have already been acquired. Optional validation is not a mathematical prerequisite. No change in a factor's current availability removes a required finite certificate, mandatory data file or classical premise from its proof.

\textbf{Screening limits.} The listing audit concerns the counted PDF text and two complete authored browser renderings, together with available replacement TeX. It does not certify unseen editions or unextracted raster contents. It reviewed actual candidate contexts and eight source pages containing listings, rather than inferring absence from a keyword search alone. It is not a fresh review of all mathematical proofs or all 1,003 PDF pages. Expanded F retains its earlier distinct accepted screen.

\textbf{Verification.} The portable checker binds the published v10 observations and final audit, reproduces the 19/43 current records, verifies unchanged source costs and program roles, and checks every actual SVG/PDF bar. Corruption controls reject restored held factors, bars on held rows, altered costs, free common theory, lost required-program roles and invented software-inclusive values. No source extraction, GAP or Lean calculation is performed.
\end{document}
'''
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);x=a.parse_args();x.out.mkdir(parents=True,exist_ok=True);(x.out/'reader.tex').write_text(render_text(read('results.json')))
