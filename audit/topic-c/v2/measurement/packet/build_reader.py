#!/usr/bin/env python3
"""Render Topic C's measured boundary without inventing L108's source cost."""
import argparse,json,hashlib,os,subprocess,tempfile,re
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'topic-c-measurement-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,default=HERE/'results.json');ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 if a.out.exists() or a.out.is_symlink():raise ValueError('fresh render output')
 a.out.mkdir(parents=True);data=json.loads(a.results.read_text());p=data['primary']
 if p['overall_factor'] is not None or p['unknown_source']!='L108':raise ValueError('missing original source remains unknown')
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'human-compression-topic-c-v2'})
 fig,ax=plt.subplots(figsize=(8.5,3.1),layout='constrained');new=[p['common_theory']]+[r['application_cost'] for r in p['per_result']]+[p['complete_printed_program_cost']]
 bars=ax.bar([i+.16 for i in range(6)],new,width=.32,color='#235a85',label='Complete common paper, applications and appendix')
 oldpairs=[(i+1,r['source_cost']) for i,r in enumerate(p['per_result']) if r['source_cost'] is not None];old=ax.bar([i-.16 for i,v in oldpairs],[v for i,v in oldpairs],width=.32,color='#a06736',label='Complete source PDFs')
 for collection in [bars,old]:
  for b in collection:ax.text(b.get_x()+b.get_width()/2,b.get_height()+470,f'{int(b.get_height()):,}',ha='center',fontsize=8)
 ax.text(2.84,850,'unknown',ha='center',fontsize=8);ax.set_xticks(range(6),['Common\nU_C','L088 / C1','N013 / C2','L108 / C3','F014 / C4','Required\nCODE']);ax.set_ylim(0,35500);ax.set_ylabel('NFC characters, excluding whitespace');ax.spines[['top','right']].set_visible(False);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.2);ax.legend(loc='upper right',frameon=False,fontsize=8)
 for ext in ['svg','pdf','png']:fig.savefig(a.out/('costs.'+ext),dpi=150,facecolor='white')
 plt.close(fig)
 table='\n'.join(f"{r['source']} / {r['application']} & "+('unknown' if r['source_cost'] is None else f"{r['source_cost']:,}")+f" & {r['application_cost']:,} & "+('unknown' if r['factor'] is None else f"{r['factor']:.3f}")+r'\\' for r in p['per_result'])
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}
\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}{\Large Topic C: common theory, applications and required code}\\[4pt]
Human Compression project\end{center}
The common paper \emph{Changes of chamber generators and binary translation
groups} supports four complete applications: Janko geometries (C1), halving
generalized cubes (C2), Petrials and faithful chamber actions (C3), and regular
polyhedra with equal adjacent parameters (C4). The fixed source contracts
are L088, N013, L108 and F014. Their forty-row scope table includes the
recorded qualifications, retained statements and exclusions; this
measurement does not expand that scope.

\paragraph{The whole-topic written comparison.}
The whole common theory costs \textbf{27,131} characters and the four complete
applications cost \textbf{44,146}. The written denominator is therefore
\textbf{71,277}. Three available source PDFs cost 60,256. If $x$ is the unknown
original-PDF cost of L108, the written comparison is
\[R_C^{\mathrm{written}}=\frac{x+60\,256}{71\,277}.\]
The two required programs are also counted in full. Their complete printed
appendix costs \textbf{8,799}, giving the separately reported comparison
\[R_C^{\mathrm{with\ programs}}=\frac{x+60\,256}{80\,076}.\]
Neither comparison has a numerical value until $x$ is known. C3's 10,071
characters remain in both denominators. Its browser text does not replace
the missing original PDF.

\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
\noindent The unit is NFC characters without whitespace in complete extracted
PDF text, after the exact furniture exclusions and visible-glyph corrections.
All unique front matter and references remain charged.

\paragraph{Conditional application comparisons.}
After acquiring the \emph{whole common theory and both complete required
programs}, the local comparison is the complete source paper divided by its
complete application. Both whole-topic denominators pay the common theory once; the program-inclusive one also pays the full appendix once.
\begin{center}\begin{tabular}{lrrr}\toprule
Source / application & Source & Application & Conditional factor\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
\newpage
\paragraph{The code is counted once, in a declared representation.}
Both GAP files are required mathematical programs and are charged in full.
The primary representation is their four-page printed appendix, including
its headings and printed glyphs. An alternative uses the complete raw files:
4,458 and 4,783 bytes, with 4,084 and 4,239 NFC nonspace characters.
The alternative replaces the appendix; it is never added to it.
\begin{center}\begin{tabular}{p{.64\linewidth}r}\toprule
Denominator representation & NFC nonspace cost\\\midrule
Common paper and four applications only & 71,277\\
Written topic plus printed program appendix & 80,076\\
Written topic plus both raw programs (alternative) & 79,600\\\bottomrule
\end{tabular}\end{center}
All three numerators remain $x+60\,256$. The written comparison is presented
first, followed by the required-program-inclusive comparison. The printed
appendix is the primary representation of the program cost, not a replacement
for the written comparison.
The raw-file metrics are summed file by file; no program or diagnostic
portion is pruned. There is no cross-topic discount on the common theory.

\paragraph{What was measured.}
The source inputs are three complete physical PDFs, totaling 33 pages.
The new side consists of the complete 27-page scientific edition and the
four-page required-program appendix. Only exact running furniture and
navigation are excluded. Font-aware glyph replacements precede Unicode
normalization; no semantic correction, dehyphenation, formula reordering or
coalescing of printed delimiter pieces is performed.

The machine-readable record contains all five length units under NFC and
NFKC, for raw untrimmed, raw selected and calibrated selected text. Each of
these thirty coordinates has the same full denominator boundary and the
three declared program representations. Exact conditional fractions appear
in the CSV and JSON files. The primary coordinate is the calibrated NFC
nonspace count used on page one.

\paragraph{Scope and retained work.}
The Janko application keeps the accepted figure/label qualification. The
halving application retains its qualified statement and excludes the
specified external-classification comparison and unused semiregular
isomorphism. For L108, the unconditional faithful-action assertion is
replaced by the exact kernel criterion. F014 uses the fixed first edition
and corrected left-action convention; its higher-rank Conjecture 3.7 belongs
to the separate question track.

The TomLib subgroup catalogue, group and coset algorithms, Danzer and
Pellicer constructions, Coxeter classifications and other stated classical
inputs remain attributed and retained. Their expanded proof and catalogue
costs are unknown, as are unextracted graphical and formula-layout costs.
The extracted-text comparison is not a measurement of total research effort
or minimum mathematical complexity.

\paragraph{Verification and use.}
The independently accepted input audit matches 270 PDF metric cells,
54 normalized-text hashes and 20 complete raw-program cells. It checks the
embedded fonts and visible glyph conventions. This numerical packet reuses
that acceptance and computes only sums, exact fractions and CSV records;
it does not repeat the source, GAP or Lean proof work. The 16 scoped Lean
declarations and other validation infrastructure remain separately
inventoried, without a claim that every application is fully formalized.

Reproduce the arithmetic with \texttt{compute.py --out /fresh/directory};
\texttt{check.py} verifies the complete boundary, both code representations,
all coordinate records and corruption controls. No primary-source text or
images are distributed. Independent arithmetic and reader review is separate
from this author calculation. No source or question credit is added.
\end{document}
'''.replace('@PAIRS@',table)
 (a.out/'measurement.tex').write_text(tex)
 for i in range(2):
  proc=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','measurement.tex'],cwd=a.out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(a.out/f'pass{i+1}.log').write_text(proc.stdout)
  if proc.returncode:raise ValueError(proc.stdout[-2200:])
 log=(a.out/'measurement.log').read_text();bad=[l for l in log.splitlines() if re.search('Overfull|Missing character|LaTeX Warning',l)]
 pdf=PdfReader(a.out/'measurement.pdf');texts=[p.extract_text() or '' for p in pdf.pages];badglyph=[(i+1,ord(c)) for i,t in enumerate(texts) for c in t if (ord(c)<32 and c not in '\t\n\r') or c=='\ufffd' or 0xe000<=ord(c)<=0xf8ff]
 if bad or badglyph:raise ValueError(str((bad,badglyph)))
 report=dict(status='PASS_RENDER_AND_TEXT_SCAN',pages=len(pdf.pages),diagnostics=bad,bad_glyphs=badglyph,page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in texts],results_sha256=hashlib.sha256(a.results.read_bytes()).hexdigest(),visual_review=False)
 (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
