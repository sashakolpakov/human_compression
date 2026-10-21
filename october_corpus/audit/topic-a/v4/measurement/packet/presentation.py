#!/usr/bin/env python3
"""Complete unified-A acquisition and manuscript costs; no software factor."""
from pathlib import Path
import json,os,tempfile
os.environ.setdefault("MPLCONFIGDIR",str(Path(tempfile.gettempdir())/"L121_numbers_mpl"))
os.environ.setdefault("XDG_CACHE_HOME",str(Path(tempfile.gettempdir())/"L121_numbers_cache"))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import R,load
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def cost_plot(r,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'svg.hashsalt':'l121-expanded-a-complete-documents'})
 p=r['primary'];d=p['document_costs'];order=r['source_ids'];apps=r['applications'];fig=plt.figure(figsize=(9,9));ax=fig.add_axes([.21,.75,.70,.14]);bx=fig.add_axes([.21,.10,.70,.53]);fig.text(.04,.965,'One common theory and nine complete applications',fontsize=15,weight='bold');fig.text(.04,.927,'Calibrated selected NFC nonspace characters · cost axes start at zero',fontsize=10);bars=[]
 def bar(a,gid,y,w,color,left=0):
  q=a.barh(y,w,left=left,height=.36,color=color)[0];q.set_gid(gid);bars.append((a,gid,y-.18,left,w,.36))
 bar(ax,'bar-whole-source',1,p['source_sum'],SOURCE);left=0
 for doc,color in [('U',COMMON)]+[(apps[x],APP)for x in order]:bar(ax,'bar-whole-'+doc,0,d[doc],color,left);left+=d[doc]
 ax.set_yticks([1,0],['Nine originals','Whole U + nine apps']);ax.set_ylim(-.55,1.55);ax.set_xlim(0,max(p['source_sum'],p['whole_written'])*1.12)
 ax.text(p['source_sum']*1.015,1,f"{p['source_sum']:,}",va='center',fontsize=9);ax.text(p['whole_written']+p['source_sum']*.015,0,f"{p['whole_written']:,}",va='center',fontsize=9)
 mx=max(d['U'],*[d[x]for x in order],*[d[apps[x]]for x in order]);bar(bx,'bar-acquire-U',9,d['U'],COMMON);bx.text(d['U']+mx*.015,9,f"{d['U']:,}",va='center',fontsize=9)
 for i,x in enumerate(order):y=8-i;bar(bx,'bar-source-'+x,y+.2,d[x],SOURCE);bar(bx,'bar-application-'+x,y-.2,d[apps[x]],APP)
 bx.set_yticks(list(range(9,-1,-1)),['Acquire whole U']+[x+' / '+apps[x]for x in order]);bx.set_ylim(-.6,9.6);bx.set_xlim(0,mx*1.12);bx.set_xlabel('Complete manuscript characters; code/data/external premises separate')
 for a in [ax,bx]:a.grid(axis='x',alpha=.2);a.set_axisbelow(True);a.spines[['right','top','left']].set_visible(False);a.tick_params(axis='y',length=0)
 fig.text(.04,.690,'Conditional applications assume whole U and all actual required computation,',fontsize=10);fig.text(.04,.665,'presentation data and retained mathematical premises already acquired.',fontsize=10);fig.text(.20,.025,'Original manuscripts',color=SOURCE,weight='bold');fig.text(.49,.025,'Whole common',color=COMMON,weight='bold');fig.text(.75,.025,'Applications',color='#347567',weight='bold')
 fig.canvas.draw();H=fig.get_figheight()*72;expected={}
 for a,gid,y,left,w,h in bars:
  c=a.transData.transform((left,y));e=a.transData.transform((left+w,y+h));scale=72/fig.dpi;expected[gid]=[c[0]*scale,H-e[1]*scale,(e[0]-c[0])*scale,(e[1]-c[1])*scale]
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 return dict(primary_coordinate=r['primary_coordinate'],expected_rectangles=expected,bars=len(expected),axis_origin_zero=True,software_costs_separate=True,ratio_bars=False)
def cumulative_plot(r,out):
 fig=plt.figure(figsize=(9,4.7));ax=fig.add_axes([.13,.19,.82,.61]);bars=[]
 for row in r['primary_acquisition']:
  i=row['stage']
  for label,cost,dx,color in [('source',row['source_written'],-.19,SOURCE),('replacement',row['replacement_written'],.19,COMMON)]:
   if cost==0:continue
   patch=ax.bar(i+dx,cost,width=.32,color=color)[0];gid=f'bar-cumulative-{label}-{i}';patch.set_gid(gid);bars.append((gid,i+dx-.16,0,.32,cost))
 ax.set_xlim(-.65,9.65);ax.set_ylim(0,max(r['primary']['source_sum'],r['primary']['whole_written'])*1.12)
 ax.set_xticks(range(10),['U']+[r['applications'][x]for x in r['source_ids']]);ax.set_xlabel('Acquire whole U, then each complete application in source order')
 ax.set_ylabel('Cumulative manuscript characters');ax.spines[['right','top']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
 fig.text(.04,.935,'Complete cumulative acquisition',fontsize=15,weight='bold')
 fig.text(.04,.87,'Actual costs in the declared order; the cost axis begins at zero.',fontsize=10)
 fig.text(.20,.045,'All originals acquired so far',color=SOURCE,weight='bold');fig.text(.60,.045,'Whole U + applications',color=COMMON,weight='bold')
 fig.canvas.draw();H=fig.get_figheight()*72;expected={}
 for gid,x,y,w,h in bars:
  c=ax.transData.transform((x,y));e=ax.transData.transform((x+w,y+h));scale=72/fig.dpi;expected[gid]=[c[0]*scale,H-e[1]*scale,(e[0]-c[0])*scale,(e[1]-c[1])*scale]
 fig.savefig(out/'cumulative.svg',metadata={'Date':None});fig.savefig(out/'cumulative.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 return dict(expected_rectangles=expected,bars=len(expected),acquisition=r['primary_acquisition'],source_zero_stage0=True,software_costs_separate=True,optimized_order_claim=False)
def plots(r,out):return dict(primary_coordinate=r['primary_coordinate'],costs=cost_plot(r,out),cumulative=cumulative_plot(r,out))
def tex(r):
 p=r['primary'];d=p['document_costs'];n=lambda x:f'{x:,}';rows=[]
 for x in r['source_ids']:
  a=r['applications'][x];rows.append(f"{x} & {a} & {n(d[x])} & {n(d[a])} & {float(p['conditional'][x]['decimal']):.6f}\\\\")
 names={'required_program_or_data':'Required programs and data','inherited_auxiliary':'Inherited auxiliaries','operational_runners':'Operational runners','partial_formal_files':'Partial formal files'};groups=[]
 for k,g in r['whole_file_group_costs'].items():groups.append(f"{names[k]} & {g['files']} & {n(g['metrics']['NFC']['characters_without_whitespace'])} & {n(g['literal_bytes'])}\\\\")
 sensitivity=[]
 for norm in ['NFC','NFKC']:
  for unit,label in [('whitespace_tokens','Whitespace tokens'),('alphanumeric_units','Alphanumeric units'),('characters_without_whitespace','Nonspace characters'),('characters_with_collapsed_whitespace','Collapsed-space characters'),('utf8_bytes_with_collapsed_whitespace','Collapsed UTF-8 bytes')]:
   vals=[r['coordinates']['/'.join((v,norm,unit))]['written']['decimal']for v in ['raw_untrimmed','raw_selected','calibrated_selected']];sensitivity.append(f'{norm}: {label} & '+' & '.join(f'{float(v):.6f}'for v in vals)+r'\\')
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Supported kernels and affine constructions}
\author{Nine-original manuscript comparison}\date{}
\begin{document}\maketitle
The nine complete originals contain '''+n(p['source_sum'])+r''' characters. The entire common paper and all nine complete applications contain '''+n(p['whole_written'])+r''' characters. The primary whole-topic comparison is
\[
 R=\frac{\sum_{i=1}^{9}c(S_i)}{c(U)+\sum_{i=1}^{9}c(A_i)}
 =\frac{'''+str(p['source_sum'])+'}{'+str(p['whole_common'])+'+'+str(p['application_sum'])+r'''}
 ='''+f"{float(p['written']['decimal']):.6f}"+r'''.
\]
Here $c$ counts characters excluding whitespace after NFC normalization of the accepted selected and calibrated PDF extraction. This convention was fixed before evaluation and preserves the prior A coordinate. It measures the length of these manuscripts, not the least possible proof length or historical originality.

All 131 source pages, the whole 23-page common paper and all 56 application pages are charged. Titles, abstracts, full proofs, tables, references, author addresses and extractable figure labels remain. There is no common-theory import free of charge, overlap subtraction, omitted application or cross-topic pooled rate.

\textbf{Conditional on prior acquisition.} The following factors are $c(S_i)/c(A_i)$ after acquiring the \emph{entire} common theory and the actual required computations, data and retained mathematical premises. Every full application is charged. L121 uses no sibling application as a premise.
\begin{center}\begin{tabular}{llrrr}\toprule
Original & App & Source & Application & Conditional\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
The eight earlier conditional values are exactly unchanged in all 30 coordinates. Adding L121 contributes 27,367 source characters and 25,549 application characters while the common paper remains unchanged. The whole-topic factor decreases from '''+f"{float(p['prior_whole_written']['decimal']):.6f}"+r''' for eight sources to '''+f"{float(p['written']['decimal']):.6f}"+r''' for nine. Both editions remain explicitly bound; this is an observed addition effect, not a new mathematical claim.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
The upper chart pays the whole common paper and each complete application. The lower chart displays the same common acquisition cost and every source/application pair. All 30 rectangles have areas proportional to manuscript length at their chart's fixed height; cost axes begin at zero. They represent text costs, not ratios or theorem counts.

Executable code is excluded symmetrically from the written comparison. Mathematical proofs, algorithms described in prose, presentations and tables remain. Required programs and data remain premises despite being outside this manuscript-only scalar. Historical source software is unknown, so there is no software-inclusive or optional-validation-inclusive factor.
\newpage
\begin{center}\includegraphics[width=\textwidth]{cumulative.pdf}\end{center}
Stage zero acquires all of $U$. Each later stage adds one complete source on the historical side and its complete application on our side. These ten cumulative stages use the inherited documentary order followed by L121. No optimal order or general sawtooth behavior is asserted. Required computation, data and external proofs remain separately acquired obligations.

\textbf{Complete separate file inventory.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Whole files & Count & NFC nonspace & Literal bytes\\\midrule
'''+ '\n'.join(groups)+r'''
\bottomrule\end{tabular}\end{center}
All 45 contents are distinct and fully inventoried. The twenty mathematical files comprise the eleven old required files and L121's eight programs plus mandatory \texttt{model\_data.json}. In particular \path{cubic_relation/check.py} is a required calculation. Six operational runners and three auxiliaries remain separate. The sixteen formal files are fifteen Lean modules and one dependency manifest; all formal scopes remain partial.

The three old printed appendices total 30 pages and represent only the old eleven-file mathematical collection. Their primary text costs are '''+n(d['CODE_A'])+', '+n(d['CODE_AFFINE'])+' and '+n(d['CODE_DIAGRAM'])+r''' characters. No complete printed representation exists for the enlarged twenty-file collection. These partial printed costs are not added to raw files, nor used for a whole-program factor. Historical software and retained external proof costs remain unknown, not zero.
\newpage
\textbf{Sensitivity of the whole written factor.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Raw complete & Raw selected & Calibrated\\\midrule
'''+ '\n'.join(sensitivity)+r'''
\bottomrule\end{tabular}\end{center}
All 30 coordinates and 300 exact fractions are supplied in JSON and CSV: one whole-topic and nine conditional comparisons in each coordinate. Every fraction records its complete unreduced source and replacement costs, reduced numerator and denominator, and a twelve-place decimal. The 240 previous conditional fraction records are preserved exactly. All 660 PDF input cells and 450 complete raw-file cells are unchanged from the adopted inputs.

Raw complete extraction retains running furniture. Selection removes only the exact accepted furniture; calibration applies occurrence-bound actual glyph repairs. Ordinary printed hyphens and ligatures remain, and NFKC is a separate sensitivity. The new source contributes twelve whole pages and its replacement eleven. Neither contains an executable listing. The 18 source and 51 application glyph repairs and all earlier source calibrations are the adopted input layer, not new decisions in this numerical calculation.

\textbf{Scientific and measurement limits.} The 102 earlier dispositions and L121's 27 corrected dispositions remain unchanged: nine original manuscripts, not 129 originals. The L121 corrections, retained Euclidean Coxeter and toroidal inputs, and all prior source qualifications remain in force. Numerical comparison adds no source, theorem, question or formalization credit.

L035's unextracted image labels on physical pages 9, 10, 12 and 22 remain unmeasured. L121's vector diagrams on pages 5--7 retain extracted labels but not priced graphical structure. Full graphics/layout, retained external proof libraries, installed software/databases, historical programs/data and complete formalization costs are unknown. The six added Lean declarations verify countermodel relations and two nonconsequences only; they do not formalize group orders, infinite families or geometry.

The numerical author previously reviewed these inputs and contributed to earlier affine work. Input authoring, scientific acceptance and root input adoption are separately bound; earlier numerical mechanics are reused with attribution. This packet performs no new extraction, mathematical enumeration or Lean compilation. A distinct numerical review is required before public admission.
\end{document}
'''
if __name__=='__main__':
 r=load(R/'results.json');g=plots(r,R);(R/'plot_data.json').write_text(json.dumps(g,indent=2)+'\n');(R/'reader.tex').write_text(tex(r))
