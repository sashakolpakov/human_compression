#!/usr/bin/env python3
"""Actual manuscript-cost rectangles and complete, symmetric reader."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
from compute import need,read,write,UNITS,ORDER

def setup(out):
 os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.hashsalt':'enlarged-mixes-written-v1','pdf.fonttype':42})
 return plt

def costs(r,out):
 plt=setup(out);c=r['primary']['document_costs'];fig,(left,right)=plt.subplots(1,2,figsize=(10,3.5));fig.subplots_adjust(left=.09,right=.995,bottom=.30,top=.87,wspace=.36)
 colors={'F005':'#666666','L016':'#aaaaaa','U0':'#426b9a','U1':'#759ac1','A1':'#438776','A2':'#83b9a9','A3':'#c49554'};patches=[]
 def bar(ax,name,x,key,bottom=0):
  p=ax.bar(x,c[key],bottom=bottom,width=.62,color=colors[key])[0];p.set_gid(name);patches.append((p,dict(id=name,document=key,cost=c[key],base_cost=bottom,axis=0 if ax is left else 1)))
 for x,keys in [(0,['F005','L016']),(1,['U0','U1','A1','A2','A3'])]:
  bottom=0
  for k in keys:bar(left,'whole-'+k,x,k,bottom);bottom+=c[k]
  left.text(x,bottom+2400,f'{bottom:,}',ha='center',fontsize=11)
 left.set_xticks([0,1],['Both sources','Whole U + all apps']);left.set_ylim(0,r['primary']['source_cost']*1.17);left.set_title('One whole-topic manuscript comparison');left.set_ylabel('NFC nonspace characters')
 for x,keys in [(0,['F005']),(1,['A1','A2']),(3,['L016']),(4,['A3'])]:
  bottom=0
  for k in keys:bar(right,'conditional-'+k,x,k,bottom);bottom+=c[k]
  right.text(x,bottom+1800,f'{bottom:,}',ha='center',fontsize=11)
 right.set_xticks([0,1,3,4],['F005','MX1','L016','MX2']);right.set_ylim(0,max(c['F005'],c['L016'])*1.2);right.set_title('Applications after full common acquisition')
 for ax in [left,right]:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 from matplotlib.patches import Patch
 fig.legend(handles=[Patch(color=colors[k],label=k)for k in colors],ncol=7,loc='lower center',bbox_to_anchor=(.53,.015),frameon=False)
 fig.canvas.draw();factor=72/fig.dpi;h=fig.get_figheight()*72;bars=[]
 for patch,v in patches:
  box=patch.get_window_extent();v.update(svg=[box.x0*factor,h-box.y1*factor,box.width*factor,box.height*factor],pdf=[box.x0*factor,box.y0*factor,box.width*factor,box.height*factor]);bars.append(v)
 axes=[]
 for i,ax in enumerate([left,right]):
  a=ax.transData.transform((0,0));b=ax.transData.transform((0,1));axes.append(dict(axis=i,minimum=0,zero_pdf_y=float(a[1]*factor),points_per_unit=float((b[1]-a[1])*factor)))
 fig.savefig(out/'complete_costs.svg',metadata={'Date':None});fig.savefig(out/'complete_costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 write(out/'plot_geometry.json',dict(status='ACTUAL_ZERO_BASELINE_RECTANGLES',bars=bars,bar_count=len(bars),axes=axes,unit='raw_untrimmed/NFC/characters_without_whitespace',software_not_in_comparison=True,conditional_acquisition_not_free=True))

def document_graphs(r,out):
 plt=setup(out);c=r['primary']['document_costs'];fig,(a,b)=plt.subplots(1,2,figsize=(10,3.3));fig.subplots_adjust(left=.015,right=.985,bottom=.12,top=.83,wspace=.15)
 from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
 records=[]
 def node(ax,name,x,y,w,h,text,color):
  ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.025',facecolor=color,edgecolor='#53616f',linewidth=.7));ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=11);records.append(dict(id=name,text=text,kind='document or explicitly unknown input',cost=None if name=='external'else c.get(name)))
 def edge(ax,start,end):ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=10,color='#4b5864',linewidth=1))
 for ax in [a,b]:ax.set_xlim(0,10);ax.set_ylim(0,6);ax.axis('off')
 a.set_title('Complete historical sources',fontsize=12)
 node(a,'F005',.5,3.8,4,1.3,f"F005: 21 pages\n{c['F005']:,} characters",'#eeeeee');node(a,'L016',5.5,3.8,4,1.3,f"L016: 12 pages\n{c['L016']:,} characters",'#eeeeee')
 node(a,'external',1,1,8,1.2,'Retained outside results and historical software\nCosts unknown; no zero-cost assumption','#fff4df');edge(a,(3,2.2),(2.5,3.8));edge(a,(7,2.2),(7.5,3.8))
 b.set_title('Two common papers; both complete applications',fontsize=12)
 node(b,'U0',.2,4.1,4.1,1.1,f"U0: simultaneous actions\n5 pages; {c['U0']:,}",'#d8e6f3');node(b,'U1',5.5,4.1,4.1,1.1,f"U1: graph covers\n4 pages; {c['U1']:,}",'#e1ebf5');edge(b,(4.35,4.65),(5.45,4.65))
 node(b,'A1',.1,1.8,2.8,1.1,f"A1: F005 local\n8 pages; {c['A1']:,}",'#d3eadd');node(b,'A2',3.25,1.8,2.8,1.1,f"A2: exceptions\n4 pages; {c['A2']:,}",'#e4f1e9');node(b,'A3',6.9,1.8,2.8,1.1,f"A3: L016\n6 pages; {c['A3']:,}",'#f3e3cc')
 edge(b,(1.7,4.05),(1.5,2.95));edge(b,(3,4.05),(4.65,2.95));edge(b,(7.5,4.05),(8.3,2.95))
 b.text(5,.65,'MX1 = A1 + A2; MX2 = A3\nTwo required certificates are additional proof inputs.',ha='center',va='center',fontsize=11)
 fig.text(.5,.025,'Arrows record paper-level proof reuse; box size is not a complexity measure. Full common papers are paid once.',ha='center',fontsize=11)
 fig.savefig(out/'document_graphs.svg',metadata={'Date':None});fig.savefig(out/'document_graphs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 write(out/'document_graphs.json',dict(nodes=records,current_edges=[['U0','U1'],['U0','A1'],['U0','A2'],['U1','A3']],historical_edges=[['external','F005'],['external','L016']],scope='Paper-level reuse and declared acquisition, not an exhaustive theorem DAG or a node-count compression factor.',required_files=r['required_files'],external_cost=None))

def reader(r,out):
 p=r['primary'];c=p['document_costs'];invent=p['separate_inventory_costs'];text=TEMPLATE
 values={**c,'SOURCE':p['source_cost'],'COMMON':p['common_cost'],'MX1':p['application_costs']['MX1'],'MX2':p['application_costs']['MX2'],'WRITTEN':p['written_denominator'],'REQRAW':invent['required_raw'],'OPTRAW':invent['optional_raw'],'DRIVERS':invent['drivers'],'LEAN':invent['formal'],'DIFFERENCE':p['source_cost']-p['written_denominator']}
 for k in ORDER:values[k]=f"{float(p['comparisons'][k]['decimal']):.6f}"
 rows=[]
 labels=['Whitespace tokens','Alphanumeric runs','Nonspace characters','Collapsed-space characters','Collapsed-space UTF-8 bytes']
 for unit,label in zip(UNITS,labels):
  z=next(x for x in r['coordinates']if(x['variant'],x['normalization'],x['unit'])==('raw_untrimmed','NFC',unit));rows.append(label+' & '+' & '.join(f"{float(z['comparisons'][k]['decimal']):.3f}"for k in ORDER)+r' \\')
 values['ROWS']='\n'.join(rows)
 for k,v in values.items():text=text.replace('@'+k+'@',str(v))
 need('@'not in text,'reader complete values');(out/'measurement.tex').write_text(text)

TEMPLATE=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\begin{document}
\begin{center}{\Large Mixes and graph covers: complete manuscript costs}\\[3pt]
Two originals, both entire common papers, and both complete applications
\end{center}
This comparison enlarges the existing Mixes topic. It retains all 21 pages of
Cunningham and Hubard's mix-criteria article (F005) and all 12 pages of
Leemans and Toledo's faithful-maniplex article (L016). Their corrected principal
contracts have distinct scientific acceptance. The measurement counts two
originals, not their 54 detailed source dispositions.

\textbf{One whole-topic comparison.} The primary coordinate is literal
untrimmed PDF extraction, NFC characters without whitespace. It includes title
matter, abstracts, references, page furniture and arXiv banners on both sides.
\begin{center}\begin{tabular}{lrr}\toprule
Complete manuscript & Pages & Characters\\\midrule
F005 source &21&@F005@\\
L016 source &12&@L016@\\
Common simultaneous-action theory $U_0$ &5&@U0@\\
Common cover theory $U_1$ &4&@U1@\\
F005 local application $A_1$ &8&@A1@\\
F005 exceptional application $A_2$ &4&@A2@\\
L016 application $A_3$ &6&@A3@\\\bottomrule
\end{tabular}\end{center}
\[
 R_{\mathrm{manuscripts}}=
 \frac{@F005@+@L016@}{@U0@+@U1@+@A1@+@A2@+@A3@}
 =\frac{@SOURCE@}{@WRITTEN@}=@whole_topic@.
\]
Both common papers are charged once in this topic. Both F005 papers remain
one complete application, including its exceptional correction. No overlap
is deducted, and no common premise is imported free from another topic.

\textbf{Conditional comparisons.} Only after acquiring \emph{both entire}
common papers, \emph{both whole required finite certificates}, and all retained
mathematical inputs, the individual source/application comparisons are
\[
 r_{\mathrm{F005}}\mid(U,P)=\frac{@F005@}{@A1@+@A2@}
 =@conditional_MX1@,\qquad
 r_{\mathrm{L016}}\mid(U,P)=\frac{@L016@}{@A3@}
 =@conditional_MX2@.
\]
They do not waive the common acquisition in the whole-topic comparison.
The written replacement is @DIFFERENCE@ characters shorter in this primary
representation. This measures manuscript length, not total research effort,
minimum proof complexity or historical originality.

\textbf{Symmetric software boundary.} Optional validation is excluded on
both sides. Neither fixed source contains an executable listing. Their
mathematical tables, formulas, written algorithms and references to software
remain counted. Unprovided historical software has unknown cost. Therefore no
software-inclusive compression factor is calculated; the required programs
remain essential separately disclosed proof inputs, rather than being
reclassified as optional.

\newpage
\begin{center}\includegraphics[width=\textwidth]{complete_costs.pdf}\end{center}
Both axes start at zero. The left panel stacks all source and replacement
manuscripts. The right panel shows the two conditional comparisons; its
application bars presuppose the whole common and required-certificate
acquisition. Neither panel charges optional validation on only one side.

\begin{center}\includegraphics[width=\textwidth]{document_graphs.pdf}\end{center}
The common argument is reused across simultaneous actions and equivariant
graph covers. The paper-level arrows show that reuse, not an exhaustive
historical theorem graph. Every displayed manuscript is counted in full;
box dimensions and node counts are not complexity measures. Required finite
certificates and retained external mathematical inputs remain explicit even
though their full historical costs are unavailable.

\textbf{Scope.} F005 retains its five literal counterexample targets and two
convention-qualified targets, with corrected rooted criteria; its three final
problems remain unanswered. L016's literal Lemma 3.5 is disproved and repaired
under faithfulness. Proposition 5.4 correctly says \emph{without} the component
intersection property. Its principal families and rank-three result are
recovered; ancillary smallest/atlas counts and further-cover questions remain
outside that contract. These qualifications do not prune either full source.

\newpage
\section*{Whole programs and representation limits}
The two required finite certificates are the complete
\texttt{check\_coprime.g} and \texttt{base\_certificate.g}. Their raw primary
cost is @REQRAW@ characters; the complete two-page printed alternative costs
@REQ@. Printed and raw versions represent the same files and are never added
together. The source-side counterpart remains unknown, so neither inventory
produces an additional ratio.
\begin{center}\begin{tabular}{lrr}\toprule
Separate complete raw-file inventory &Files&Characters\\\midrule
Required finite certificates &2&@REQRAW@\\
Optional validation &4&@OPTRAW@\\
Operational drivers &5&@DRIVERS@\\
Scoped Lean files &2&@LEAN@\\\bottomrule
\end{tabular}\end{center}
All four optional files remain visible. The three-page new optional appendix
costs @VAL@ characters; the two old mixed appendices cost @OLD_CODE1@ and
@OLD_CODE2@ and remain historical inventories. They are not extra required
charges or current optional-inclusive comparisons. The two Lean files provide
six generic declarations, four new and two reused. They do not formalize all
geometry, the finite presentations or either complete source.

\textbf{Unit sensitivity.} Complete untrimmed extraction under NFC gives:
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit&Whole topic&F005 conditional&L016 conditional\\\midrule
@ROWS@
\bottomrule\end{tabular}\end{center}
The JSON and CSV retain all five units under NFC and NFKC in raw-untrimmed,
raw-selected and calibrated-selected forms: 30 coordinates and 90 exact
fractions. Selection removes only the separately bound running headers and
isolated folios. Calibration changes declared visible glyph representations,
including script letters, brace pieces and arrow-tee components; the original
raw extraction always remains available. Literal line-break hyphens remain.

All 180 earlier F005 PDF cells and 70 raw-file cells are retained exactly.
The new five-document input contributes 150 PDF cells and 60 raw-file cells.
The combined eleven-document inventory includes historical code PDFs and
therefore is \emph{not} a list of eleven denominator terms. The current
manuscript denominator contains exactly the two common papers and three
application papers shown on page 1.

Diagram labels are retained when extractable. Full graphic/layout cost,
retained outside proofs, original software, runtime, engineering and complete
formalization remain unknown rather than zero. Distinct input acceptance is
bound; this numerical author packet still requires a separate arithmetic,
graph and reader review. It creates no new source, question or novelty credit.
\end{document}
'''

def build(r,out,engine):
 need(not out.exists(),'fresh render directory');out.mkdir(parents=True);costs(r,out);document_graphs(r,out);reader(r,out)
 for i in range(2):
  z=subprocess.run([str(engine),'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=out,text=True,capture_output=True);(out/f'render{i}.log').write_text(z.stdout+z.stderr);need(z.returncode==0,'XeLaTeX exit')
 log=(out/'measurement.log').read_text();need(not re.search('Overfull|Missing character|LaTeX Warning|Package .* Warning',log),'reader glyph/layout diagnostic')
 from pypdf import PdfReader
 pages=[pg.extract_text()for pg in PdfReader(out/'measurement.pdf').pages];need(len(pages)==3,'three complete reader pages');write(out/'render_report.json',dict(status='AUTHOR_RENDER_PASS_VISUAL_SEPARATE',pages=3,page_text_sha256=[hashlib.sha256(t.encode()).hexdigest()for t in pages],diagnostics=[]))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));a=p.parse_args();build(read(a.results),a.out,a.xelatex)
