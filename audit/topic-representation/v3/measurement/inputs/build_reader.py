from pathlib import Path
import json
H=Path(__file__).resolve().parent
c=json.loads((H/'author_counts.json').read_text());d=json.loads((H/'document_map.json').read_text());r=json.loads((H/'raw_file_map.json').read_text())
rows=[]
labels={'F010':'F010 original','L126':'L126 original','U_R':'Complete shared theory','R1':'Complete F010 application','R2':'Complete L126 application','CODE':'Separate full program appendix'}
for key in ['F010','L126','U_R','R1','R2','CODE']:
 x=c['documents'][key];rows.append(f"{labels[key]} & {x['pages']} & {x['variants']['raw_untrimmed']['NFC']['characters_without_whitespace']:,} & {x['variants']['calibrated_selected']['NFC']['characters_without_whitespace']:,} \\\\")
rawrows=[]
for role,label in [('required_finite_certificate','Required finite certificate'),('required_graph_data','Mandatory complete graph data'),('optional_validation','Optional validation programs'),('current_orchestration_driver','Operational helpers'),('partial_formal_evidence','Partial Lean evidence')]:
 xs=[x for x in c['raw_files'].values()if x['role']==role]
 rawrows.append(f"{label} & {len(xs)} & {sum(x['bytes']for x in xs):,} & {sum(x['metrics']['NFC']['characters_without_whitespace']for x in xs):,} \\\\")
text=r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=24mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,tabularx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\emergencystretch}{2em}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\title{Incidence representations: complete measurement inputs}
\author{Human Compression Project}\date{}
\begin{document}\maketitle
This is an input proposal for the accepted two-source scientific edition.
It evaluates no compression factor. Its primary coordinate remains
\textbf{calibrated selected text, NFC, characters without whitespace}, exactly
as in the earlier F010 comparison. Independent input acceptance is still required.

\section*{Every source and every complete paper}
F010 is Díaz Ramos--Molinier--Viruel, \emph{Every finite group is represented
by a finite incidence geometry}, arXiv:2511.02410v2 (16 December 2025).
L126 is Leemans--Stokes--Tranchida, \emph{Groups represented by incidence
geometries}, arXiv:2506.10464v1 (12 June 2025; manuscript dated 13 June).
Both exact 13-page originals are included, with their titles, authors,
references and arXiv identification.

\begin{center}\small
\begin{tabular}{lrrr}\toprule
Complete document & Pages & Raw NFC & Primary NFC\\
 & & nonspace chars & nonspace chars\\\midrule
ROWS
\bottomrule\end{tabular}\end{center}

The written boundary pays the whole 13-page common paper and both whole
applications, including the final reference pages: $13+4+12=29$ replacement
pages. The separate appendix has all 16 pages. With the originals this is
71 physical pages, of which 55 are written source/common/application pages.
There is no discount for inherited proofs, repeated context or bibliography.

The finite-normal-pair encoder and its full proof now belong to the common
paper. Both applications invoke that shared theorem. Neither has an unpaid
sibling-application premise. A later F010 conditional comparison must first
acquire the whole common paper and actual retained classical inputs. A later
L126 conditional comparison must also acquire its complete required graph
certificate and graph data. Optional validation is not a proof prerequisite.

\section*{What is unchanged and what is re-extracted}
Every one of the 30 accepted F010 \emph{source} coordinates is preserved with
its exact font, glyph and furniture evidence. All other current PDFs are
extracted anew, including the changed four-page F010 application. No old
application, common-paper or appendix total is substituted.

For every PDF the packet retains three variants (literal raw, furniture-only
selected, glyph-calibrated selected), NFC and NFKC, and five units: whitespace
tokens, alphanumeric units, nonspace characters, collapsed-whitespace
characters, and collapsed-whitespace UTF-8 bytes. The resulting 180 PDF cells
include 30 inherited cells. The 17 whole raw files supply another 170 cells.
\newpage
\section*{Symmetric programs and retained costs}
Neither original nor either current scientific application/common paper
contains a concrete executable or pseudocode listing. All manuscript listing
masks are therefore explicitly empty. The source's Tits construction and the
new written algorithms are mathematical statements and proofs, so they remain
counted. Programs are excluded from both sides of manuscript comparisons.

The separate appendix contains ten whole mathematical files: one required
finite certificate and nine optional validations. The required certificate
uses the entire 19,326-byte graph JSON. The appendix does not replace that
file with a summary. Printed and raw versions of the same program must never
be added together. All whole-file costs below are an inventory, not a
software-inclusive ratio.

\begin{center}\small
\begin{tabular}{lrrr}\toprule
Whole raw category & Files & Bytes & NFC nonspace\\\midrule
RAWROWS
\bottomrule\end{tabular}\end{center}

The two helpers orchestrate scientific and migration checks. The four Lean
files contain 22 scoped declarations, not a formal proof of either entire
source or of the concrete graph. The mandatory pure-Python certificate
establishes the one explicitly given 896-vertex graph; optional GAP, nauty or
Bliss checks are not its proof premises. All source software, retained
external-proof costs, library costs and full graphic structure remain unknown.
Thus no software-inclusive factor is available and missing cost is not zero.

\section*{Exact extraction and visible symbols}
The parser versions are pypdf 6.13.0 and FontTools 4.63.0. Selected L126 text
removes only the exact running headers/page numbers; its arXiv banner remains.
Own selected PDFs remove only physical page numbers. Every page and reference
line is otherwise retained. The F010 selection and calibration are unchanged,
including the visible right braces encoded as tab characters.

The new L126 audit binds 24 actual font dictionaries and 649 encoded classes,
using dictionary identity, effective encoding and actual embedded outlines.
Eight classes at 28 occurrences calibrate script and blackboard capitals and the
left component of a mapsto symbol. The adjacent arrow is kept separately.
Fifty-eight exceptional source and replacement outlines were directly viewed.
Phi variants and ligatures are retained as actually extracted. The current
own PDFs receive no glyph substitutions. Source diagrams on pages 2, 4, 5
and 12 retain their extracted labels; their complete graphical cost is unknown.

\section*{Scope and independence}
The accepted science preserves six F010 principal blocks and 31 L126
dispositions, including explicit corrections and retained classical inputs.
The finite-field repair, free-basis qualification and chamber-connectivity
condition remain visible. The broader Section 6.2 and Section 8 programmes
are not declared solved. No new question, priority or formalization credit is
claimed. This packet reuses distinct scientific acceptance; its author also
authored the current L126 proof and migration. A separate reviewer must decide
whether these proposed inputs are suitable for numerical comparison.
\end{document}
'''
(H/'input_reader.tex').write_text(text.replace('RAWROWS','\n'.join(rawrows)).replace('ROWS','\n'.join(rows)))
