#!/usr/bin/env python3
"""Produce a concise TeX/PDF reader and complete-document acquisition figure."""
import argparse,json,os,tempfile,subprocess,hashlib,re
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'topic-c-cost-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader
from accounting import need

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh rendering directory');a.out.mkdir(parents=True)
 data=json.loads((a.packet/'view_data.json').read_text());p=data['measurement']['primary'];rows=data['acquisition']['stages'];value=lambda x:x['calibrated_selected']['NFC']['characters_without_whitespace']
 additions=[value(r['new_cost']) for r in rows];cumulative=[value(r['cumulative_cost']) for r in rows];written=[value(r['written_cumulative_cost']) for r in rows]
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.hashsalt':'topic-c-proof-costs'})
 fig,axs=plt.subplots(1,2,figsize=(9,3.05),layout='constrained')
 ax=axs[0];bars=ax.bar([i+.18 for i in range(6)],additions,width=.34,color='#235a85',label='Complete new document')
 known=[(i+2,r['source_cost']) for i,r in enumerate(p['per_result']) if r['source_cost'] is not None];old=ax.bar([i-.18 for i,v in known],[v for i,v in known],width=.34,color='#a06736',label='Complete source paper')
 for b in list(bars)+list(old):ax.text(b.get_x()+b.get_width()/2,b.get_height()+500,f'{int(b.get_height()):,}',ha='center',fontsize=6.5)
 ax.text(3.82,700,'unknown',ha='center',fontsize=7);ax.set_xticks(range(6),['U_C','code','L088\nC1','N013\nC2','L108\nC3','F014\nC4']);ax.set_ylim(0,35500);ax.set_title('Complete documents');ax.set_ylabel('NFC characters without whitespace');ax.legend(frameon=False,fontsize=7,loc='upper left')
 ax=axs[1];ax.plot(range(6),written,'o-',color='#235a85',label='Written papers');ax.plot(range(6),cumulative,'s--',color='#488169',label='Including required programs');ax.set_xticks(range(6),['U_C','+ code','+ C1','+ C2','+ C3','+ C4']);ax.set_ylim(0,93000);ax.legend(frameon=False,fontsize=7,loc='upper left');ax.set_title('Acquire each passage once')
 for i,v in enumerate(cumulative):ax.annotate(f'{v:,}',(i,v),xytext=(0,8),textcoords='offset points',ha='center',fontsize=6.5)
 ax.text(.02,.04,'No complete numerical source curve:\nL108 remains unknown.',transform=ax.transAxes,fontsize=7)
 for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 for ext in ['svg','pdf','png']:fig.savefig(a.out/('acquisition.'+ext),dpi=160,facecolor='white')
 plt.close(fig)
 table='\n'.join(f"{r['source']} / {r['application']} & "+('unknown' if r['source_cost'] is None else f"{r['source_cost']:,}")+f" & {r['application_cost']:,} & "+('unknown' if r['factor'] is None else f"{r['factor']:.3f}")+r'\\' for r in p['per_result'])
 stage='\n'.join(r['stage'].replace('_',r'\_')+f" & {value(r['new_cost']):,} & {value(r['written_cumulative_cost']):,} & {value(r['cumulative_cost']):,} & "+('---' if r['stage'] in ['U_C','CODE'] else f"{value(r['reused_route_cost']):,}")+r'\\' for r in rows)
 tex=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}
\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}{\Large Topic C: proofs and their costs}\\[4pt]Human Compression project\end{center}
The common paper, \emph{Changes of chamber generators and binary translation
groups}, supports four complete applications: Janko geometries (C1), halving
generalized cubes (C2), Petrials (C3), and equal-parameter polyhedra (C4).
The fixed comparison preserves forty source clauses, including their explicit
corrections, retained theorems and two excluded auxiliary assertions.

\paragraph{The complete written comparison.}
The common paper costs 27,131 characters and the four applications cost
44,146. The three available source PDFs contribute 60,256. If $x$ is the
unknown cost of the original L108 PDF, then
\[R_C^{\mathrm{written}}=\frac{x+60\,256}{71\,277}.\]
There is no numerical overall factor. The full 10,071-character Petrial
application remains in the denominator. Its source browser rendering fixes
the mathematical statement boundary, but is not a substitute PDF measurement.

Both complete GAP programs are required for the Janko application. Their
printed appendix costs 8,799, charged once, giving the separate comparison
\[R_C^{\mathrm{programs}}=\frac{x+60\,256}{80\,076}.\]
Counting the two full raw files instead gives denominator 79,600. This is an
alternative representation of the same programs, not an additional charge.

\begin{center}\includegraphics[width=\linewidth]{acquisition.pdf}\end{center}
\noindent All figures on this page use NFC characters without whitespace in
complete extracted PDF text, with the reviewed furniture exclusions and glyph
calibration. The same accounting is supplied for all thirty policy coordinates.
Unextracted graphics and expanded outside-proof costs remain unknown.

\paragraph{After acquiring the whole common theory and both programs.}
These are the admitted complete-source / complete-application factors.
\begin{center}\begin{tabular}{lrrr}\toprule
Source / application & Source & Application & Conditional factor\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
\newpage
\paragraph{A declared acquisition order.}
Acquire the complete $U_C$, the complete program appendix, and then C1,
C2, C3 and C4. Every application includes its definitions, title, context,
references and all proof passages. Let $K_i$ be the union of passage owners
paid by stage $i$. The new cost is $c(K_i\setminus K_{i-1})$; a prerequisite
already in $K_{i-1}$ is not charged again. No cost is shared across topics.
\begin{center}\begin{tabular}{lrrrr}\toprule
Added & New cost & Written total & With programs & Prior text used\\\midrule
@STAGES@
\bottomrule\end{tabular}\end{center}
The last column measures already acquired passages used by the complete local
paper's recorded arguments. It is not an extra subtraction from that paper's
cost. The historical cumulative written costs are 12,640, then 39,658,
then $x+39\,658$, and finally $x+60\,256$. Thus no complete numerical
historical acquisition curve is available. The sequence is a reading order,
not an estimate of research effort or a shortest possible proof.

\paragraph{What a smaller proof route measures.}
The paired graph records prerequisite-to-use arrows for each of the forty
clauses and for the four complete contracts. The additional identification of
the equal-parameter construction with the earlier polygon construction stays
separate. Each route's known cost is the union of its exclusive passage owners.
It can omit context still paid in the complete paper. Accordingly these route
subtotals are explanations, not replacement denominators or new compression
factors. Parent results and their proof branches may share a statement owner;
box costs overlap, while every total counts that passage once.

There are 156 graph nodes: 64 historical, 62 current, 26 retained external
inputs and four verification components, with 249 typed edges. Their categories
include definitions, statements and proof branches, at different levels of
detail. No node-count ratio is defined. The accounting has 199 text owners
and 195 selected-text spans. It also assigns excluded furniture to explicit
owners for the untrimmed sensitivity; no printed text is silently dropped.

\paragraph{Scope and verification.}
The accepted logical revision restores the seed and subgroup assumptions of
the historical Janko calculation without extending the string-only recognition
theorem to nonstring exercise cases. It records the historical halving C-group
premise and Cayley--Hamilton use, and keeps the current displacement proof
independent of unnecessary binary-module assumptions. Geometry is established
before naming the Janko residues. All source qualifications remain attached
to their original clauses.

The original L108 PDF, outside-proof expansions and graphic costs remain
unknown. The existing sixteen Lean declarations verify specified displacement,
intersection and semidirect-product components; they are not full formalizations
of the applications. The two complete Janko programs are preserved unchanged.
The cost checker verifies full-document conservation, unions and deliberate
corruptions. The offline HTML shows all proof routes, locations and unknown
inputs; its deterministic DOM test is not a real-browser layout test.
This new ownership and reader layer awaits independent review. It changes
no mathematical contract, source or question credit, or admitted paper factor.
\end{document}
'''.replace('@PAIRS@',table).replace('@STAGES@',stage)
 (a.out/'reader.tex').write_text(tex)
 for i in range(2):
  run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','reader.tex'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  (a.out/f'pass{i+1}.log').write_text(run.stdout);need(run.returncode==0,run.stdout[-3000:])
 log=(a.out/'reader.log').read_text();bad=[l for l in log.splitlines() if re.search(r'Overfull|Missing character|LaTeX Warning',l)]
 pdf=PdfReader(a.out/'reader.pdf');texts=[page.extract_text() or '' for page in pdf.pages];badglyph=[(i+1,ord(c)) for i,t in enumerate(texts) for c in t if (ord(c)<32 and c not in '\n\t\r') or c=='\ufffd' or 0xe000<=ord(c)<=0xf8ff];need(not bad and not badglyph,'clean render and glyph scan '+str((bad,badglyph)))
 report={'status':'PASS_RENDER_AND_TEXT_SCAN','pages':len(pdf.pages),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in texts],'diagnostics':bad,'bad_glyphs':badglyph,'visual_review':False,'view_data_sha256':hashlib.sha256((a.packet/'view_data.json').read_bytes()).hexdigest()}
 (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
