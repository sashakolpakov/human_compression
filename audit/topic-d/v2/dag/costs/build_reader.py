#!/usr/bin/env python3
"""Produce the readable cost account from unchanged accepted measurements."""
import argparse,json,os,tempfile,subprocess,hashlib,re
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'topic-d-cost-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader
from accounting import need

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh rendering directory');a.out.mkdir(parents=True)
 d=json.loads((a.packet/'view_data.json').read_text());p=d['measurement']['primary'];rows=d['acquisition']['stages']
 val=lambda x:x['calibrated_selected']['NFC']['characters_without_whitespace']
 additions=[val(r['new_cost']) for r in rows];cum=[val(r['cumulative_cost']) for r in rows];written=[val(r['written_cumulative_cost']) for r in rows]
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.hashsalt':'topic-d-proof-costs'})
 fig,axs=plt.subplots(1,2,figsize=(9,3),layout='constrained')
 ax=axs[0];bars=ax.bar([i+.18 for i in range(5)],additions,width=.34,color='#235a85',label='Complete new document')
 old=ax.bar([i+2-.18 for i in range(3)],[r['source_cost'] for r in p['per_result']],width=.34,color='#a06736',label='Complete source paper')
 for b in list(bars)+list(old):ax.text(b.get_x()+b.get_width()/2,b.get_height()+400,f'{int(b.get_height()):,}',ha='center',fontsize=6.4)
 ax.set_xticks(range(5),['U_D','code','L066\nD1','L074\nD2','L104\nD3']);ax.set_ylim(0,34500);ax.set_ylabel('NFC characters without whitespace');ax.set_title('Complete documents');ax.legend(frameon=False,fontsize=7)
 ax=axs[1];ax.plot(range(5),written,'o-',color='#235a85',label='Written papers');ax.plot(range(5),cum,'s--',color='#488169',label='Including all eight programs')
 oldcum=[val(r['historical_cumulative']['complete_cost']) for r in rows if r['historical_cumulative']]
 ax.plot([2,3,4],oldcum,'^:',color='#a06736',label='Complete source manuscripts')
 ax.set_xticks(range(5),['U_D','+ code','+ D1','+ D2','+ D3']);ax.set_ylim(0,85000);ax.set_title('Acquire each passage once');ax.legend(frameon=False,fontsize=7,loc='upper left')
 for i,v in enumerate(cum):ax.annotate(f'{v:,}',(i,v),xytext=(0,8),textcoords='offset points',ha='center',fontsize=6.4)
 for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 for ext in ['svg','pdf','png']:fig.savefig(a.out/('acquisition.'+ext),dpi=160,facecolor='white')
 plt.close(fig)
 pairs='\n'.join(f"{r['source']} / {r['application']} & {r['source_cost']:,} & {r['application_cost']:,} & {r['factor']:.3f}"+r'\\' for r in p['per_result'])
 stages='\n'.join(r['stage'].replace('_',r'\_')+f" & {val(r['new_cost']):,} & {val(r['written_cumulative_cost']):,} & {val(r['cumulative_cost']):,} & "+('---' if r['stage'] in ['U_D','CODE'] else f"{val(r['reused_route_cost']):,}")+r'\\' for r in rows)
 tex=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setlength{\emergencystretch}{2em}
\begin{document}
\begin{center}{\Large Topic D: proofs and their costs}\\[4pt]Human Compression project\end{center}
The common paper on stabilizers, support and enumeration supports three complete
applications: commuting involutions (D1), Suzuki polyhedra (D2), and Hall--Janko
geometries (D3). The comparison preserves the thirty-seven admitted source clauses
and their stated qualifications. The paired graph records actual proof routes;
it does not replace the complete manuscripts by their shortest selected routes.

\paragraph{Written papers.}
The three complete source PDFs cost 47,894 characters. The whole common theory
costs 15,632 and the three applications cost 29,855, giving
\[R_D^{\mathrm{written}}=\frac{47\,894}{15\,632+29\,855}
 =\frac{47\,894}{45\,487}=1.052916\ldots.\]
Title, abstract, definitions, proofs, tables, context and references are included.
The unused normalizer theorem remains paid as part of the whole common paper.

\paragraph{Including the complete program.}
The twelve-page appendix preserves five required mathematical programs and
three complete diagnostics. All eight are charged, including comments and the
wrapper, at 27,070 characters. The separate comparison is
\[R_D^{\mathrm{programs}}=\frac{47\,894}{45\,487+27\,070}
 =\frac{47\,894}{72\,557}=0.660088\ldots.\]
The full eight raw files cost 26,185; substituting them for the printed appendix
gives $47\,894/71\,672=0.668239\ldots$. They are alternatives, never additional
charges. Two complete operational drivers cost 10,038 raw characters and
12,765 actual bytes, separately inventoried rather than included in these factors.

\begin{center}\includegraphics[width=\linewidth]{acquisition.pdf}\end{center}
\noindent These figures use calibrated complete PDF extracted text, NFC characters
without whitespace. All thirty policy coordinates are provided. Expanded external
proofs, catalogue and algorithm construction, historical software, and graphics
remain unknown costs, not zero.

\paragraph{After acquiring the whole common theory and all eight programs.}
\begin{center}\begin{tabular}{lrrr}\toprule
Source / application & Complete source & Complete application & Conditional factor\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
\newpage
\paragraph{Acquisition and reuse.}
Acquire the whole $U_D$, the complete program appendix, and then D1, D2 and D3.
For the union $K_i$ of passage owners paid through stage $i$, the new cost is
$c(K_i\setminus K_{i-1})$. Every application is charged in full. Previously
acquired prerequisites are not charged again, and no common theory is discounted
because another topic uses overlapping arguments.
\begin{center}\begin{tabular}{lrrrr}\toprule
Added & New cost & Written total & With programs & Prior text used\\\midrule
@STAGES@
\bottomrule\end{tabular}\end{center}
The last column is the owner union of already acquired text used by the local
paper's recorded arguments. It is not a further subtraction from the application's
length. The matching historical cumulative costs are 20,916, 41,577 and 47,894.
This is a declared reading order, not a research chronology or a claim of a
sawtooth pattern.

\paragraph{What a proof route measures.}
Each of the 37 clauses has a historical route and a current proof or explicit
retention/exclusion boundary. The generating-series and faithfulness outputs are
shown separately, without new source credit. For a set of prerequisite nodes
$S$, its known text cost is
\[c_{\mathrm{route}}(S)=c\!\left(\bigcup_{v\in S}\operatorname{owners}(v)\right).\]
Historical arrows document the reasoning asserted in each source; they do not
retroactively certify a corrected or overbroad historical lemma.
Shared statement passages and program wrappers therefore appear once in a union.
Repeated physically printed statements remain counted at every location.
Context outside a selected route remains paid in the complete-paper comparisons.
No factor is computed from a route subtotal, box sum or number of nodes.

The logical graph has 137 nodes and 284 typed arrows: 50 historical nodes,
58 current nodes, 20 external inputs and 9 verification components. The cost
partition has 220 owners and 215 selected-text spans. Every extracted character
belongs to exactly one owner in each of the three text policies. The untrimmed
sensitivity assigns furniture to explicit owners. Both Unicode normalizations
and all five counting units conserve every whole-document total.

\paragraph{Scope and evidence.}
L066's corrected reversal argument and exceptional full-automorphism computation
remain distinct from its historical proof. The Suzuki local normalization,
generation, intersection and duality checks are paid alongside the common
support count; Suzuki's classification, Lüneburg's structure and other classical
inputs retain their original attribution and unknown expanded costs.
The Hall--Janko census includes every Borel anchor and the complete geometric
recognition tests. Its printed diagrams, full geometric automorphism/correlation
groups, doubling relation and supplement annotations remain excluded from the
fixed principal census contract. Their source text is still charged.

The five required programs enter logical routes; the three diagnostics have
positive printed costs but only validation arrows. The original ten scoped Lean
declarations and the later generic supplement of 28 declarations are formal
evidence, not complete formalizations of the applications. The latter comprises
12 plus 16 declarations, not 12 in addition to 28.

The input calibration uses the accepted occurrence-bound repairs, including the
L066 extracted-character/encoding collision; that embedded font has no
ToUnicode stream. No source PDF, primary text or source raster is exported.
The offline viewer exposes proof locations, actual edges, owners and unknown
inputs. Its deterministic DOM tests are not real-browser layout tests. This
ownership and reader packet awaits independent review and changes no accepted
paper factor, source credit or question credit.
\end{document}
'''.replace('@PAIRS@',pairs).replace('@STAGES@',stages)
 (a.out/'reader.tex').write_text(tex)
 for i in range(2):
  run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','reader.tex'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  (a.out/f'pass{i+1}.log').write_text(run.stdout);need(run.returncode==0,run.stdout[-3000:])
 log=(a.out/'reader.log').read_text();bad=[l for l in log.splitlines() if re.search(r'Overfull|Missing character|LaTeX Warning',l)]
 pdf=PdfReader(a.out/'reader.pdf');texts=[p.extract_text() or '' for p in pdf.pages]
 badglyph=[(i+1,ord(c)) for i,t in enumerate(texts) for c in t if (ord(c)<32 and c not in '\n\t\r') or c=='\ufffd' or 0xe000<=ord(c)<=0xf8ff]
 need(not bad and not badglyph,'clean render and glyph scan '+str((bad,badglyph)))
 report={'status':'PASS_RENDER_AND_TEXT_SCAN','pages':len(pdf.pages),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest() for t in texts],'diagnostics':bad,'bad_glyphs':badglyph,'visual_review':False,'view_data_sha256':hashlib.sha256((a.packet/'view_data.json').read_bytes()).hexdigest()}
 (a.out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
