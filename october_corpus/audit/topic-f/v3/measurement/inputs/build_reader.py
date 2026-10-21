#!/usr/bin/env python3
"""Complete input boundary reader, no factor calculation."""
import argparse,subprocess
from pathlib import Path
from extract_inputs import load
from font_tools import need

def text():
 a=load('author_counts.json');p=load('policy.json');v={k:f"{r['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']:,}" for k,r in a['documents'].items()}
 s=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=26mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\setlength{\emergencystretch}{2em}
\title{Odd-prime kernels: complete measurement inputs}
\author{Human Compression project}\date{Expanded Topic F; input proposal only}
\begin{document}\maketitle\raggedright
This boundary compares two complete originals with one complete common paper
and two complete applications. It preserves 25 L014 and 38 L007 scientific
source dispositions. It computes input lengths, not compression factors.

\textbf{L014:} Hou, Feng, Leemans and Qu, \emph{String C-groups of order
$4p^m$}, arXiv:2407.10388v1, 15 July 2024, twelve pages.
\textbf{L007:} Kong, Feng, Hou, Leemans and Qu, \emph{Chiral 3-polytopes of
order $2p^m$}, accepted 19 January 2026, DOI 10.26493/1855-3974.3716.b64,
twenty-two pages. Every physical source page is included, with its title,
abstract, formulas, tables, bibliography and contact information.

\begin{center}\begin{tabular}{@{}lrr@{}}\toprule
Complete document & Pages & Raw NFC characters\\\midrule
Original L014 &12&@L014@\\Original L007 &22&@L007@\\
Common paper U &7&@U@\\L014 application A1 &5&@A1@\\
L007 application A2 &6&@A2@\\Complete program appendix &9&@CODE@\\\bottomrule
\end{tabular}\end{center}
Characters here mean non-whitespace characters in the untrimmed extraction.
This primary coordinate was fixed before extraction. The six PDFs occupy 61
pages. No old common paper, application or program is an unpaid premise.

A later written comparison must pay U+A1+A2 in full: eighteen pages, including
reference-only endings. A separate program-inclusive comparison adds the
whole nine-page appendix. The alternative raw representation instead adds all
nine complete program files, @PROGRAM_BYTES@ bytes. These representations
must not be added together. Each conditional source/application comparison
requires prior acquisition of the entire U and all nine declared programs;
its remaining local cost is all of A1 or all of A2.

\textbf{Programme roles.} All nine files are finite validation, not premises
of uniform theorems. They include the three inherited L014 checks, two current
carry and regular-family checks, two exploratory scans, and two inherited
central-lift checks. Complete files are retained even when they are diagnostic.
The appendix's nine full \texttt{VerbatimInput} directives and a text-inclusion
check account for every file once. Continuation marks are removed only in that
printing check; every printed mark remains in every measured coordinate.

\newpage
\section*{Literal extraction and visible glyphs}
All five established units are recorded under NFC and NFKC for untrimmed text,
selected text and calibrated selected text: 180 PDF cells. Source L014's arXiv
banner and L007's 22 accepted-manuscript watermarks remain in the raw primary.
The selected variants remove exact page furniture only: repeated running
headers, those watermarks and isolated replacement page numbers. They preserve
source content, original hyphens and extraction spacing.

The original PDF byte events resolve to 1,140 used classes across 50 actual
font dictionaries. Dictionary identity, effective encoding, font stream and
outline evidence are bound separately. Sixty-three mathematical and icon
outlines were freshly inspected. Thirty-seven classes receive 780
occurrence-bound sensitivity repairs, covering mathematical alphabets,
parentheses, brackets, bracket pieces, sums, products, tildes and one mapsto
component class. The latter uses the declared arrow proxy for that component;
the adjoining arrow is still counted.

Two licence icons and four horizontal-brace component classes in L007 stay
literal encoded proxies. Their visual structure is not reconstructed as text.
The source logos, table rules, formula placement and full graphical complexity
remain unknown, not zero. Ordinary variable font styling is not re-encoded.
The four replacement PDFs retain their Unicode Type0 text unchanged; no
Type1 source-outline claim is made for those fonts.

The PDF visitor emits one duplicate, fontless watermark callback on every
L007 page. The narrowly bound helper ignores that duplicate only for metadata
alignment. The returned extraction is byte-for-byte the unchanged standard
\texttt{pypdf} text, and the actual PDF stream still contains each watermark
once. No mathematical source character is dropped by this repair.

\section*{Complete scope and separate costs}
Four complete operational drivers total @DRIVER_BYTES@ bytes, and three complete
Lean files total @LEAN_BYTES@ bytes. Together with the nine programs these yield
160 raw metric cells. The twelve scoped declarations comprise nine reused and
three new generic statements. No particular source construction, complete
classification or geometric correspondence is formally proved by these files.
These operational and formal costs are separate from paper/program comparisons.

The corrected scientific boundary preserves the full L014 contract and all
L007 parameter ranges. In L007's Remark 1.3 the fourth regular family exists
exactly for $p=3$; the Section 6 quotient argument is repaired. These corrections
do not rewrite the measured primary. The previously written cyclic lift is
charged in U and has a distinct fresh root adjudication. No new question or
historical-priority claim is made.

Complete external proofs of the retained Cunningham--Pellicer, Huppert,
Schmidt/Iwasawa and classical inputs remain unpriced. Scientific acceptance
is reused, with all 61 page views bound; six source formula/icon pages were
re-viewed for calibration. The measurement author was the scientific reviewer,
with the inherited lift role disclosed. A distinct input audit is still required.
No mathematical program or Lean theorem is rerun by this measurement packet.
\end{document}
'''
 for k,x in v.items():s=s.replace('@'+k+'@',x)
 for key,cat in [('PROGRAM_BYTES','programs'),('DRIVER_BYTES','operational_drivers'),('LEAN_BYTES','formal_files')]:s=s.replace('@'+key+'@',f"{sum(r['bytes'] for r in p[cat]):,}")
 return s
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True);(a.out/'reader.tex').write_text(text())
 for i in range(2):
  q=subprocess.run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','reader.tex'],cwd=a.out,capture_output=True);(a.out/f'render{i}.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'reader render')
 diag=[s for s in (a.out/'reader.log').read_text().splitlines() if any(k in s for k in ['Missing character','Overfull','Underfull','LaTeX Warning','Font Warning'])];need(not diag,'clean reader diagnostics');print('PASS input reader')
