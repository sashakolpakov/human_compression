#!/usr/bin/env python3
"""Render a concise explanation of the complete Topic B acquisition boundary."""
import argparse,json,os,shutil,subprocess,tempfile,re,hashlib
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'topic-b-dependency-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 if a.out.exists() or a.out.is_symlink():raise ValueError('fresh render output')
 a.out.mkdir(parents=True);d=json.loads((a.packet/'view_data.json').read_text());p=d['measurement']['primary'];metric='characters_without_whitespace'
 val=lambda row:row['NFC'][metric]
 rows=d['acquisition']['stages'];new=[val(r['new_cost']) for r in rows];cum=[val(r['cumulative_cost']) for r in rows]
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'topic-b-dependency-reader'})
 fig,axes=plt.subplots(1,2,figsize=(9,3),layout='constrained')
 ax=axes[0];bars=ax.bar([i+.18 for i in range(5)],new,width=.34,color='#235a85',label='Complete new paper')
 known=[(i+1,r['source_cost']) for i,r in enumerate(p['per_result']) if r['source_cost'] is not None]
 old=ax.bar([i-.18 for i,v in known],[v for i,v in known],width=.34,color='#a06736',label='Complete source paper')
 for collection in [bars,old]:
  for b in collection:ax.text(b.get_x()+b.get_width()/2,b.get_height()+450,f'{int(b.get_height()):,}',ha='center',fontsize=7)
 ax.text(.82,900,'unknown',ha='center',fontsize=7);ax.set_xticks(range(5),['U_B','N001\nB1','N003\nB2','N008\nB3','L030\nB4']);ax.set_ylim(0,28500);ax.set_title('Whole papers');ax.legend(fontsize=7,frameon=False,loc='upper left');ax.set_ylabel('NFC characters, excluding whitespace')
 ax=axes[1];ax.plot(range(5),cum,'o-',color='#235a85');ax.set_xticks(range(5),['U_B','+ B1','+ B2','+ B3','+ B4']);ax.set_ylim(0,70000);ax.set_title('Acquire each new passage once')
 for i,v in enumerate(cum):ax.annotate(f'{v:,}',(i,v),xytext=(0,8),textcoords='offset points',ha='center',fontsize=8)
 ax.text(.04,.05,'No numerical historical curve:\nN001 remains unknown.',transform=ax.transAxes,fontsize=8)
 for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 for ext in ['svg','pdf','png']:fig.savefig(a.out/('acquisition.'+ext),dpi=150,facecolor='white')
 plt.close(fig)
 table='\n'.join(f"{r['source']} / {r['application']} & "+('unknown' if r['source_cost'] is None else f"{r['source_cost']:,}")+f" & {r['application_cost']:,} & "+('unknown' if r['factor'] is None else f"{r['factor']:.3f}")+r'\\' for r in p['per_result'])
 stages='\n'.join(r['stage'].replace('_',r'\_')+f" & {val(r['new_cost']):,} & {val(r['cumulative_cost']):,} & "+('---' if r['stage']=='U_B' else f"{val(r['reused_route_cost']):,}")+r'\\' for r in rows)
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}
\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}{\Large Topic B: proof routes and acquisition costs}\\[4pt]
Human Compression project\end{center}
The four fixed contracts cover thirty clauses from Buekenhout--Cara (1998),
Cameron--Cara (2002), Archer--Cara--Krempa (2005), and the revised
Garcia-Colin--Leemans manuscript. The common theory is \emph{Forest
coordinates and relative generation}. Its four complete applications
retain the admitted hypotheses, outside theorems, corrections and exclusions.

\paragraph{The complete comparison.}
The whole common paper costs 14,119 characters; the four applications cost
44,942. Three source PDFs contribute 57,539. If $x$ is the unknown original
PDF cost of N001, the complete comparison is
\[R_B=\frac{x+57\,539}{59\,061}.\]
There is no numerical value of $R_B$. The N001 application remains fully
charged. Its authored browser text supplies documentary evidence but is
not substituted for the missing PDF measurement.

\begin{center}\includegraphics[width=\linewidth]{acquisition.pdf}\end{center}
\noindent The unit throughout this page is NFC characters without whitespace
in the complete extracted PDF text, using the reviewed furniture exclusions
and glyph corrections. Image and expanded outside-proof costs remain unknown.

\paragraph{After acquiring the whole common theory.}
The following admitted factors divide the complete source paper by its
complete application. They do not discount the umbrella in the overall
comparison or charge it again at each application.
\begin{center}\begin{tabular}{lrrr}\toprule
Source / application & Source & Application & Conditional factor\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
This proof edition has no required mathematical program dependency.
Validation infrastructure and the six scoped Lean declarations are separately
inventoried; they are not claims of complete formalization.
\newpage
\paragraph{One explicit acquisition order.}
Start with the complete $U_B$, then acquire B1, B2, B3 and B4. Let $K_i$
be the union of passage owners paid through stage $i$. The added cost is
$c(K_i\setminus K_{i-1})$; every complete local paper, including context
and references, belongs to $K_i$. Recorded prerequisites already in
$K_{i-1}$ are not charged again. The table is an exact union calculation,
not a proposed shortest proof or an estimate of time spent.
\begin{center}\begin{tabular}{lrrr}\toprule
Paper added & New cost & Cumulative & Prior passages used\\\midrule
@STAGES@
\bottomrule\end{tabular}\end{center}
The last column counts the already paid passages appearing in that
application's recorded proof route. It is not an extra subtraction from the
new cost. Every historical cumulative stage is symbolic: $x$, then
$x+17\,765$, $x+35\,302$, and $x+57\,539$.

\paragraph{What the paired graph explains.}
The offline reader selects a whole contract or any of its thirty clauses.
Arrows run from prerequisite to use. It offers a compact named-result view
and an expanded proof-branch view. Selecting a box gives the precise source
or current proof location, its paid passages and retained assumptions.
Comparison, attribution and verification links are displayed separately
from proof prerequisites. The five repaired documentary interfaces in the
accepted logical revision remain in force, including the implicit Kneser
connectedness premise and the two Whiston inputs' retained classification
provenance.

The graph contains 73 historical nodes, 85 new nodes, 19 retained external
inputs and seven verification components: 184 nodes and 348 fine edges.
These categories include definitions, statements and proof branches. They
are not comparable counts of results, and no node-count factor is reported.
There are 217 disjoint spans with 214 text owners. Parent boxes and proof
branches can share owners: box costs overlap, while totals count each passage
once. Statement-only source passages are labeled as such; a proof charged
elsewhere does not become an additional cost here.

\paragraph{Result routes and whole papers answer different questions.}
A selected prerequisite union explains which recorded arguments support a
result. It can omit context that is still paid in the complete-paper total.
Neither this union nor a graph traversal is a minimum proof cost. The full
umbrella remains paid within Topic B, independently of other topics.
External proofs, missing original-PDF text and unextracted graphics remain
unknown in both views.

\paragraph{Reproduction and scope.}
The standalone HTML retains all thirty clause mappings and all fine edges;
its JSON files bind the reviewed graph, corrected ownership layer and
admitted measurements. The generated figures and this reader are derived
explanations. They do not change any mathematical contract, source credit,
question count or previously admitted factor. A separate checker verifies
complete owner unions, input hashes and the absence of an invented historical
curve; the UI harness tests all contract and clause routes. No primary-source
text or images are distributed in this reader.
\end{document}
'''.replace('@PAIRS@',table).replace('@STAGES@',stages)
 (a.out/'reader.tex').write_text(tex)
 for i in range(2):
  proc=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','reader.tex'],cwd=a.out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (a.out/f'pass{i+1}.log').write_text(proc.stdout)
  if proc.returncode:raise ValueError(proc.stdout[-2500:])
 log=(a.out/'reader.log').read_text();bad=[s for s in log.splitlines() if re.search('Overfull|Missing character|LaTeX Warning',s)]
 pdf=PdfReader(a.out/'reader.pdf');texts=[p.extract_text() or '' for p in pdf.pages];badglyph=[(i+1,ord(c)) for i,t in enumerate(texts) for c in t if (ord(c)<32 and c not in '\n\t\r') or c=='\ufffd' or 0xe000<=ord(c)<=0xf8ff]
 if bad or badglyph:raise ValueError(str((bad,badglyph)))
 report=dict(status='PASS_RENDER_AND_TEXT_SCAN',pages=len(pdf.pages),page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in texts],diagnostics=bad,bad_glyphs=badglyph,visual_review=False,input_view_data_sha256=hashlib.sha256((a.packet/'view_data.json').read_bytes()).hexdigest())
 (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
