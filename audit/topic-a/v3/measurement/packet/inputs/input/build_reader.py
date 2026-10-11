#!/usr/bin/env python3
"""Build the concise complete-boundary reader; no ratio calculation."""
from pathlib import Path
import json,argparse,subprocess,shutil,hashlib,re
from pypdf import PdfReader
H=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((H/n).read_text())
def esc(s):
 for a,b in [('\\',r'\textbackslash{}'),('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#'),('^',r'\textasciicircum{}')]:s=s.replace(a,b)
 return s

def make():
 p=load('policy.json');c=load('author_counts.json')['documents'];spec=load('input_spec.json');titles=load('source_scope.json')['source_titles']
 n=lambda k:format(c[k]['metrics'][p['primary']['variant']][p['primary']['normalization']][p['primary']['metric']],',')
 title=lambda k:esc(titles[k]).replace(r'2\textasciicircum{}n p',r'$2^np$').replace(r'2\textasciicircum{}n',r'$2^n$')
 source_rows='\n'.join(f"{k} & {title(k)} & {spec[k]['pages']} & {n(k)} \\\\" for k in p['source_ids'])
 ownnames={'U':'Complete common theory','A1':'Two-power orders','A2':'Three-generator hypertopes','A3':'Square sections and free extensions','A4':'Common two-group quotient','A5':'High-type two-groups','A6':'Order-1024 markings','A7':'Prescribed diagram symmetries','A8':'Mixed-prime polyhedra'}
 own_rows='\n'.join(f"{k} & {ownnames[k]} & {spec[k]['pages']} & {n(k)} \\\\"for k in ownnames)
 code_rows='\n'.join(f"{label} & {spec[k]['pages']} & {n(k)} \\\\"for k,label in [('CODE_A','Two-group computation (four whole files)'),('CODE_AFFINE','Affine computation (six whole files)'),('CODE_DIAGRAM','Diagram computation (one whole file)')])
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,tabularx,array}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\newcolumntype{L}{>{\raggedright\arraybackslash}X}
\begin{document}
\begin{center}\large\textbf{Supported kernels, translation lattices\newline and finite marked quotients}\par
\normalsize Proposed complete measurement inputs\end{center}
The boundary compares eight already admitted originals with one complete common
paper and eight complete applications. The new common paper replaces the declared
duplicated arguments; no previous common manuscript is a free premise. All source
contracts and their corrections remain. This packet records lengths, not compression
factors, and awaits an independent input review.

The primary coordinate preserves the current A and Affine convention: calibrated,
furniture-selected NFC text, counting non-whitespace characters. Raw-untrimmed and
raw-selected text, NFC and NFKC, and five units are all retained (30 coordinates per
PDF). The tables show the primary coordinate only. Only exact page furniture is
removed; titles, proofs, complete tables, bibliographies and wrappers are charged.

\small
\begin{tabularx}{\textwidth}{@{}lLrr@{}}\toprule
Original & Complete source title & Pages & Characters\\\midrule
'''+source_rows+r'''
\bottomrule\end{tabularx}\par

\begin{tabularx}{\textwidth}{@{}lLrr@{}}\toprule
Paper & Complete replacement & Pages & Characters\\\midrule
'''+own_rows+r'''
\bottomrule\end{tabularx}\par
\normalsize
All 119 source pages and all 68 replacement scientific pages are included. The 240
source coordinates and 48 collapsed-text hashes reproduce the prior accepted inputs
exactly. Source visible-glyph mappings are reused with their exact PDF, font and
context bindings; this is not a new full source-outline audit.
\newpage
\textbf{Complete computational and other inputs}

All three appendices are measured in full, adding 30 pages. The eleven whole
computational files include the phase78 presentation data and mathematical replay
driver. These are required proof inputs, not free output tables. Their printed and
raw-file lengths are alternative representations, never two additive copies.

\small
\begin{tabularx}{\textwidth}{@{}Lrr@{}}\toprule
Complete appendix & Pages & Characters\\\midrule
'''+code_rows+r'''
\bottomrule\end{tabularx}\par
\normalsize
The separate raw inventory also contains all three inherited affine auxiliary
scripts, the two current packet drivers and all fourteen unchanged Lean
modules. The latter provide only their declared partial formal results: the new
arbitrary-parabolic theorem and complete applications are not formalized by them.
There is no new theorem, source, question or formal credit from this measurement.

\textbf{Symmetric manuscript boundary.}
The eight originals and the nine scientific replacement papers contain no unmatched
executable listing under the bound listing screen. Mathematical proof and algorithm
prose remain included. Separate executable appendices and raw software are fully
inventoried. No software-inclusive factor is justified by this inventory: the complete
historical software boundary and external library/database costs are unknown.
A future application comparison must identify the whole common paper and every
actual required computational or retained mathematical premise already acquired;
optional checking is not silently made a theorem premise.

\textbf{What is and is not measured.}
Twenty PDFs, comprising 217 physical pages, produce 600 metric cells; thirty complete
raw files produce 300 more. All eleven program/data files are verified in the full
TeX and printed appendices. Inclusion alone ignores whitespace and the printing
wrap markers; the measured PDF text retains them. The new PDFs have no inferred
glyph substitutions: all extracted controls/private-use/replacement characters are
checked, and all font dictionary, encoding, ToUnicode and embedded-stream identities
are bound.

The old source-page and glyph reviews and the exact unified-paper visual receipts
are explicitly reused. No fresh review of all 217 pages, execution of GAP, or Lean
compilation is claimed. L035 has raster-only scientific labels on pages 9, 10, 12
and 22; the image on page 22 is clipped by the page boundary. Their full visible
text cost, all diagram structure, retained external proofs, and installed software
and databases remain unknown, not zero.

The scientific boundary is the author freeze \texttt{3a51b6f9} and distinct root
review \texttt{f81a0294}. Exact source editions, hashes and full reproduction
instructions are in the accompanying JSON and README. This proposal changes no
published factor and exports no primary text or page raster.
\end{document}
'''

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 if a.out.exists():raise ValueError('fresh output required')
 a.out.mkdir(parents=True);tex=make();(a.out/'input_reader.tex').write_text(tex)
 for i in(1,2):
  r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','input_reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'xelatex{i}.stdout').write_text(r.stdout+r.stderr)
  if r.returncode:raise ValueError('reader render failed')
 log=(a.out/'input_reader.log').read_text();diagnostics=[x for x in log.splitlines()if any(t in x for t in ('Overfull','Underfull','Missing character','LaTeX Warning','Package fontspec Warning'))]
 if diagnostics:raise ValueError(diagnostics)
 texts=[x.extract_text()or''for x in PdfReader(a.out/'input_reader.pdf').pages]
 if len(texts)!=2:raise ValueError('expected two complete reader pages')
 if(H/'input_reader.pdf').exists():
  old=[x.extract_text()or''for x in PdfReader(H/'input_reader.pdf').pages]
  if old!=texts:raise ValueError('frozen reader page texts differ')
 report=dict(status='PASS',pages=len(texts),diagnostics=diagnostics,tex_sha256=sha(tex.encode()),pdf_sha256=sha((a.out/'input_reader.pdf').read_bytes()),page_text_sha256=[sha(t.encode())for t in texts],all_page_text_sha256=sha('\n'.join(texts).encode()),factors_calculated=False)
 (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS two-page input reader, no diagnostics or factors')
if __name__=='__main__':main()
