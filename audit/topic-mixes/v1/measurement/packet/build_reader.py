#!/usr/bin/env python3
"""Complete F005 cost rectangles and readable comparison, only from authorized results."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
from compute import need,read,write,UNITS

def plot(r,out):
 need(r['input_bindings']['input_acceptance'] is not None,'accepted inputs before plotting actual costs')
 os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'mix-f005-complete-costs-v1','pdf.fonttype':42})
 c=r['primary']['document_costs'];fig,(a,b)=plt.subplots(1,2,figsize=(10,3.4));fig.subplots_adjust(left=.085,right=.99,bottom=.30,top=.88,wspace=.30)
 colors={'F005':'#666666','U':'#426b9a','A1':'#579689','A2':'#86bdb2','CODE1':'#b88245','CODE2':'#d7b27c'}
 labels={'F005':'Historical source','U':'Common theory U','A1':'Local application A1','A2':'Exceptional application A2','CODE1':'Main appendix','CODE2':'Exceptional appendix'}
 patches=[]
 def bar(ax,name,x,key,bottom=0):
  p=ax.bar(x,c[key],bottom=bottom,width=.65,color=colors[key])[0];p.set_gid(name)
  patches.append((p,dict(id=name,document=key,cost=c[key],base_cost=bottom,axis=0 if ax is a else 1)))
 bar(a,'cost-source',0,'F005')
 for x,keys in [(1,['U','A1','A2']),(2,['U','A1','A2','CODE1','CODE2'])]:
  bottom=0
  for k in keys:bar(a,'cost-total-'+str(x)+'-'+k,x,k,bottom);bottom+=c[k]
 totals=[c['F005'],sum(c[k]for k in ['U','A1','A2']),sum(c[k]for k in ['U','A1','A2','CODE1','CODE2'])]
 top=max(totals);a.set_ylim(0,top*1.18);a.set_xticks([0,1,2],['Source','Written papers','With all code']);a.set_ylabel('NFC characters without whitespace');a.set_title('Complete source and replacement')
 for x,v in enumerate(totals):a.text(x,v+top*.025,f'{v:,}',ha='center',fontsize=8)
 keys=['U','A1','A2','CODE1','CODE2']
 for x,k in enumerate(keys):bar(b,'cost-component-'+k,x,k)
 top=max(c[k]for k in keys);b.set_ylim(0,top*1.18);b.set_xticks(range(5),['U','A1','A2','Code 1','Code 2']);b.set_title('Every replacement component')
 for x,k in enumerate(keys):b.text(x,c[k]+top*.025,f'{c[k]:,}',ha='center',fontsize=8)
 from matplotlib.patches import Patch
 fig.legend(handles=[Patch(color=colors[k],label=labels[k])for k in ['F005','U','A1','A2','CODE1','CODE2']],loc='lower center',bbox_to_anchor=(.52,.015),ncol=3,frameon=False,fontsize=8)
 for ax in [a,b]:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.tick_params(axis='x',labelsize=8)
 fig.canvas.draw();factor=72/fig.dpi;height=fig.get_figheight()*72;rects=[]
 for patch,rec in patches:
  bb=patch.get_window_extent();rec.update(svg=[bb.x0*factor,height-bb.y1*factor,bb.width*factor,bb.height*factor],pdf=[bb.x0*factor,bb.y0*factor,bb.width*factor,bb.height*factor]);rects.append(rec)
 axes=[]
 for i,ax in enumerate([a,b]):
  zero=ax.transData.transform((0,0));one=ax.transData.transform((0,1));axes.append(dict(axis=i,zero_pdf_y=float(zero[1]*factor),points_per_unit=float((one[1]-zero[1])*factor),minimum=0))
 fig.savefig(out/'complete_costs.svg',metadata={'Date':None});fig.savefig(out/'complete_costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 record=dict(status='ACTUAL_VECTOR_RECTANGLES',primary=['raw_untrimmed','NFC','characters_without_whitespace'],bars=rects,bar_count=14,axes=axes,source_and_replacement_complete=True,raw_code_alternative_not_added=True,sawtooth_claim=False)
 write(out/'plot_geometry.json',record);return record

def reader(r,out):
 p=r['primary'];c=p['document_costs'];raw=p['raw_costs'];app=p['application_cost'];written=p['written_denominator'];code=p['printed_program_cost']
 f=lambda k:f"{float(p['comparisons'][k]['decimal']):.6f}"
 rows=[]
 for u,label in zip(UNITS,['Whitespace tokens','Alphanumeric units','Nonspace characters','Characters, spaces collapsed','UTF-8 bytes, spaces collapsed']):
  z=next(x for x in r['coordinates']if (x['variant'],x['normalization'],x['unit'])==('raw_untrimmed','NFC',u))
  rows.append(label+' & '+' & '.join(f"{float(z['comparisons'][k]['decimal']):.3f}"for k in ['written_papers','conditional_application','including_printed_programs','including_raw_programs_alternative'])+r' \\')
 wording='shorter' if c['F005']>written else ('longer' if c['F005']<written else 'equal in length')
 text=TEMPLATE
 vals={**c,'APP':app,'WRITTEN':written,'PRINTED':code,'RAW':raw['programs'],'PRINTEDTOTAL':written+code,'RAWTOTAL':written+raw['programs'],'DRIVERS':raw['drivers'],'LEAN':raw['formal'],'WR':f('written_papers'),'CR':f('conditional_application'),'PR':f('including_printed_programs'),'RR':f('including_raw_programs_alternative'),'ROWS':'\n'.join(rows),'DIRECTION':wording,'DIFFERENCE':abs(c['F005']-written)}
 for k,v in vals.items():text=text.replace('@'+k+'@',str(v))
 need('@'not in text and all(ord(c)>=32 or c in '\n\t'for c in text),'all reader values replaced; no control glyphs');(out/'measurement.tex').write_text(text)

TEMPLATE=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Mix criteria: complete manuscript costs}\end{center}
The historical article is Cunningham and Hubard, \emph{Polytopality criteria
for the mix of polytopes and maniplexes}, arXiv:2506.19334v1, all 21 physical
pages. The comparison concerns its accepted corrected principal contract:
35 principal and background rows, with all three final problems still
unanswered. One original is compared with one complete application in two
papers, after paying for its entire common theory.

\textbf{Whole topic.} The primary ruler is literal untrimmed PDF extraction,
NFC characters without whitespace, fixed before counting. Titles, abstracts,
body, references, page footers and the source arXiv banner remain counted.
\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & Characters\\\midrule
Historical F005 source & 21 & @F005@\\
Common theory $U$ & 5 & @U@\\
Local application $A_1$ & 8 & @A1@\\
Exceptional application $A_2$ & 4 & @A2@\\
Both complete code appendices & $4+3$ & @PRINTED@\\\bottomrule
\end{tabular}\end{center}
The written comparison charges both complete application papers:
\[
 R_{\mathrm{written}}=\frac{@F005@}{@U@+@A1@+@A2@}
 =\frac{@F005@}{@WRITTEN@}=@WR@.
\]
After acquisition of the \emph{whole} common paper and \emph{all three}
complete mathematical programs, the one conditional comparison is
\[
 r\mid(U,P)=\frac{@F005@}{@A1@+@A2@}=\frac{@F005@}{@APP@}=@CR@.
\]
This conditional measure does not remove the acquisition from the whole-topic
cost. The exceptional correction receives no free prior-work allowance;
there is no overlap or cross-topic discount.

\textbf{Whole program alternatives.} One GAP file is a required finite
certificate for the coprime-label example. Two full Python files validate
written coordinate proofs. All three remain charged in these alternatives:
\[
 R_{\mathrm{printed}}=\frac{@F005@}{@WRITTEN@+@PRINTED@}=@PR@,
 \qquad
 R_{\mathrm{raw}}=\frac{@F005@}{@WRITTEN@+@RAW@}=@RR@.
\]
Printed and raw representations are alternatives, never simultaneous charges.
Both program-inclusive forms are longer than the source in this primary unit;
the sensitivity table preserves the different results in other units.
Three complete drivers cost @DRIVERS@ characters separately; one full Lean
file costs @LEAN@ separately and contains two generic declarations. Neither
is silently included in the displayed factors, and the full source is not
formalized. Historical software cost is unknown, rather than zero.

\newpage
\begin{center}\includegraphics[width=\textwidth]{complete_costs.pdf}\end{center}
Both axes start at zero. The rectangles show the actual complete costs in the
primary unit, including both code appendices in the last total. The written
replacement is @DIRECTION@ by @DIFFERENCE@ characters in this representation.
A single source supplies no recurring sawtooth pattern or theorem-node
compression statistic.

\textbf{Units and sensitivities.} For complete untrimmed text in NFC:
\begin{center}\small\begin{tabular}{lrrrr}\toprule
Unit & Written & Conditional & Printed & Raw code\\\midrule
@ROWS@
\bottomrule\end{tabular}\end{center}
The JSON and CSV retain all five units under NFC and NFKC for untrimmed raw,
selected raw and calibrated selected text: thirty coordinates and 120 exact
fractions. The two selected sensitivities remove only isolated page footers;
nine visually checked glyph aliases affect only the calibrated sensitivity.
All source and replacement documents obey the same declared boundary.

\textbf{Scientific and measurement limits.} The accepted proofs include five
literal counterexample targets, including Corollaries 6.10(3) and 6.15(2),
and two further targets under the explicitly stated medial-component
convention. Their corrected rooted criteria and retained classical inputs
remain visible in the scientific source map. No answer to the three final
problems, new source credit or historical originality claim is made by this
measurement.

The accepted input audit binds 45 complete PDF pages, all three whole
mathematical programs, and the separate driver and formal inventories.
Extractable diagram labels and literal proxies are counted; full graphical
information, external proofs, software runtime, engineering and full
formalization costs remain unknown. These factors describe the declared text
representation, not minimum proof complexity or total research effort.
Distinct numerical review is required before publication.
\end{document}
'''
def build(r,out,engine):
 need(not out.exists(),'fresh render output');out.mkdir(parents=True);g=plot(r,out);reader(r,out)
 for i in range(2):
  z=subprocess.run([str(engine),'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=out,capture_output=True,text=True)
  (out/f'render{i}.log').write_text(z.stdout+z.stderr);need(z.returncode==0,'XeLaTeX exit')
 log=(out/'measurement.log').read_text();need(not re.search('Overfull|Missing character|LaTeX Warning|Package .* Warning',log),'reader layout/glyph diagnostics')
 from pypdf import PdfReader
 pages=[p.extract_text()for p in PdfReader(out/'measurement.pdf').pages];need(len(pages)==2,'two complete reader pages')
 report=dict(status='AUTHOR_RENDER_PASS_VISUAL_REVIEW_SEPARATE',pages=2,page_text_sha256=[hashlib.sha256(t.encode()).hexdigest()for t in pages],cost_rectangles=g['bar_count'],diagnostics=[]);write(out/'render_report.json',report)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--results',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));a=ap.parse_args();build(read(a.results),a.out,a.xelatex)
