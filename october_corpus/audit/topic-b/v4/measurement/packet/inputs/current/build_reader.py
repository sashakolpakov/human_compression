"""Human-readable complete input boundary, not a ratio report."""
from pathlib import Path
import json,subprocess,re
import pypdf
H=Path(__file__).resolve().parent

def load(n):return json.loads((H/n).read_text())
def reader():
 c=load('author_counts.json');rows=[]
 labels={'L047':'Complete L047 original','U_B6':'Complete new common theory','B6':'Complete new application','CODE6':'Separate complete program appendix'}
 for k,label in labels.items():
  d=c['documents'][k];rows.append(f"{label} & {d['pages']} & {d['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']:,} & {d['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']:,} \\\\")
 return r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=23mm]{geometry}
\usepackage{booktabs,array,hyperref}
\setlength{\parskip}{5pt}\setlength{\parindent}{0pt}
\title{Adding transitive string C-groups to Topic B\\Complete measurement inputs}
\author{Input proposal; distinct count review pending}\date{12 October 2026}
\begin{document}\maketitle
This packet prepares a six-original manuscript comparison. It contains no
compression factor and makes no new scientific or question claim. The corrected
L047 principal contract has separate scientific review and root adoption;
measurement acceptance is a separate step.

\textbf{The complete boundary.}
The five existing originals are N001, N003, N008, L030 and L040. L047 is added
as B6. Every existing source and replacement observation stays exact. N001
remains the complete literal authored rendering, not an acquired original PDF.
The other five originals use their fixed complete PDFs. L040 retains its
identification cover in the primary, with its accepted direct article-only
sensitivity preserved.

The replacement has two complete common papers: the existing sixteen-page
\emph{Forest coordinates and relative generation} and the ten-page
\emph{String separators, normal modules and transitive rank}. It retains all
five existing applications and adds the complete three-page
\emph{Transitive string C-groups: the complete half-degree bound}.
Both whole common papers are acquired once within Topic B; no unused passage
is deducted merely because the new proof avoids an older argument. The full
finite-neighbor proof is already written in the new common paper. Its archived
two-page predecessor is provenance, not a second manuscript charge.

\textbf{Fixed units.}
The primary remains raw, untrimmed NFC characters without whitespace, selected
before new counts. All thirty coordinates are retained: raw untrimmed, raw
selected and calibrated selected text; NFC and NFKC; and five units
(whitespace tokens, alphanumeric units, nonspace characters, collapsed-space
characters and collapsed-space UTF-8 bytes). Titles, proof prose, tables,
references and qualifications remain within the complete manuscripts.

\begin{center}\small
\begin{tabular}{@{}p{65mm}rrr@{}}\toprule
New complete document & Pages & Raw primary & Calibrated\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
The calibrated column is the selected NFC nonspace sensitivity, not a preferred
replacement for the fixed raw primary. The program appendix is an inventory
representation and is excluded from both manuscript sides.

\newpage
\textbf{Matched software treatment.}
L047 names Magma computations and a primitive-group catalogue function, but
contains no complete executable listing. Its full source and all new scientific
pages were read and visually checked. The replacement likewise keeps its
mathematical algorithms as prose; executable code is in separate appendices.
The accepted listing screen for the older five originals and their current
applications is reused without a new exclusion or extraction.

There are ten whole mathematical files: four inherited files and six additional
required finite inputs. Of the old four, two supply required or auxiliary finite
premises and two are optional validations. All six additional files are required:
the four new complete searches, the inherited finite-neighbor search, and its
exact action roster. A file called \texttt{run.g} is therefore a mathematical
input, not merely an operational launcher. No additional stored data are
consumed by these files. Their recorded results and complete logs are
reproducible execution receipts; GAP algorithms and catalogue completeness
remain retained premises.

The two seven-page appendices print all ten files in full. The whole raw files
are an alternative representation, never an added second charge. Five
operational drivers and two inherited Lean modules are inventoried separately;
the latter contain fourteen partial declarations and zero new declarations.
Four archived independent-audit tools are separately identified as provenance.
No complete source formalization is claimed.

Optional validation is excluded on both sides. Required finite certificates
retain their mathematical role, so a future manuscript-length ratio will not be
a complete executable-proof cost. Source-side software, complete external
proofs and complete graphics have unknown cost, not zero. No software-inclusive
scalar is available. Any conditional comparison must first acquire both whole
common papers and every required dependency.

\textbf{Glyphs and graphics.}
The new source and new replacement use actual font dictionaries and encoded
glyph events. Eight private outline panels cover 85 distinct embedded classes.
Twenty-three alias classes give 314 individually bound repairs: two source
epsilon events and 312 symbols in the new common paper. Repairs affect only
the calibrated sensitivity. A mapsto tail stays separate from adjacent arrow
components. The standard unembedded font used in the source's arXiv banner
stays literal; no embedded-outline claim is made for it. Three code-wrap
symbols also stay literal in every measured variant; the hook's extraction is
a representation limitation. They are ignored only in the separate test that
each complete raw file is printed.

Table values are retained as text. Table rules, layout and other graphics have
no invented text equivalent. The entire source Table 3 remains counted, including
its 23 finer reports that are ancillary to the accepted principal contract.
Source Conjecture 1.1 was already resolved in L044; this packet claims no new
question solution.

\textbf{Review and reproducibility.}
The proposal preserves 360 previous document cells, 30 article-only sensitivity
cells and 80 raw-file cells. It adds 120 document cells and 90 raw-file cells.
The resulting main boundary has 450 PDF cells and 30 literal-rendering cells,
with 170 raw-file cells separately inventoried. All fifteen PDFs contain 134
pages; no original PDF is invented for N001. The input author wrote the older
B common theory and distinctly reviewed L047 science. Those roles are disclosed;
new metric acceptance must come from a different reviewer. Replay extracts
inputs and rebuilds this reader without rerunning finite searches or Lean.
\end{document}
'''
def build(out,engine):
 out.mkdir(parents=True,exist_ok=True);(out/'reader.tex').write_text(reader())
 logs=[]
 for i in range(2):
  p=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error','reader.tex'],cwd=out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/f'build{i}.log').write_text(p.stdout);logs.append(p.stdout)
  if p.returncode:raise ValueError(p.stdout[-4000:])
 defects=[line for line in logs[-1].splitlines()if any(x in line for x in ['Overfull','Missing character','LaTeX Warning:'])]
 if defects:raise ValueError(str(defects))
 pages=len(pypdf.PdfReader(out/'reader.pdf').pages)
 if pages!=2:raise ValueError(f'Expected two reader pages, got {pages}')
 return dict(pages=pages,diagnostics=defects)
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');v=a.parse_args();print(build(v.out,v.xelatex))
