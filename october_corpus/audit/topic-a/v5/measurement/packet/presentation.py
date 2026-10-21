#!/usr/bin/env python3
"""Complete unified-A acquisition and manuscript costs; no software factor."""
from pathlib import Path
import json,os,tempfile
os.environ.setdefault("MPLCONFIGDIR",str(Path(tempfile.gettempdir())/"L003_numbers_mpl"))
os.environ.setdefault("XDG_CACHE_HOME",str(Path(tempfile.gettempdir())/"L003_numbers_cache"))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import R,load
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def cost_plot(r,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'svg.hashsalt':'l003-expanded-a-complete-documents'})
 p=r['primary'];d=p['document_costs'];a_cost=p['application_costs'];order=r['source_ids'];apps=r['applications'];fig=plt.figure(figsize=(9,9));ax=fig.add_axes([.21,.75,.70,.14]);bx=fig.add_axes([.21,.10,.70,.53]);fig.text(.04,.965,'Common theory and ten complete applications',fontsize=15,weight='bold');fig.text(.04,.927,'Calibrated selected NFC nonspace characters · cost axes start at zero',fontsize=10);bars=[]
 def bar(a,gid,y,w,color,left=0):
  q=a.barh(y,w,left=left,height=.36,color=color)[0];q.set_gid(gid);bars.append((a,gid,y-.18,left,w,.36))
 bar(ax,'bar-whole-source',1,p['source_sum'],SOURCE);left=0
 for doc,color,cost in [(x,COMMON,d[x])for x in r['common_documents']]+[(apps[x],APP,a_cost[apps[x]])for x in order]:bar(ax,'bar-whole-'+doc,0,cost,color,left);left+=cost
 ax.set_yticks([1,0],['Ten originals','Whole U + ten apps']);ax.set_ylim(-.55,1.55);ax.set_xlim(0,max(p['source_sum'],p['whole_written'])*1.12)
 ax.text(p['source_sum']*1.015,1,f"{p['source_sum']:,}",va='center',fontsize=9);ax.text(p['whole_written']+p['source_sum']*.015,0,f"{p['whole_written']:,}",va='center',fontsize=9)
 mx=max(p['whole_common'],*[d[x]for x in order],*a_cost.values());bar(bx,'bar-acquire-U',10,p['whole_common'],COMMON);bx.text(p['whole_common']+mx*.015,10,f"{p['whole_common']:,}",va='center',fontsize=9)
 for i,x in enumerate(order):y=9-i;bar(bx,'bar-source-'+x,y+.2,d[x],SOURCE);bar(bx,'bar-application-'+x,y-.2,a_cost[apps[x]],APP)
 bx.set_yticks(list(range(10,-1,-1)),['Acquire whole U']+[x+' / '+apps[x]for x in order]);bx.set_ylim(-.6,10.6);bx.set_xlim(0,mx*1.12);bx.set_xlabel('Complete manuscript characters; code/data/external premises separate')
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
 ax.set_xlim(-.65,10.65);ax.set_ylim(0,max(r['primary']['source_sum'],r['primary']['whole_written'])*1.12)
 ax.set_xticks(range(11),['U']+[r['applications'][x]for x in r['source_ids']]);ax.set_xlabel('Acquire whole U, then each complete application in source order')
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
    p=r['primary']; d=p['document_costs']; n=lambda x:f'{x:,}'
    rows=[]
    for source in r['source_ids']:
        app=r['applications'][source]
        rows.append(f"{source} & {app} & {n(d[source])} & {n(p['application_costs'][app])} & {float(p['conditional'][source]['decimal']):.6f}\\\\")
    labels={'required_program':'Required programs','required_data':'Required data',
            'operational':'Operational files','optional_validation':'Optional validation',
            'partial_formal':'Partial formal files','output_receipt':'Output receipts'}
    groups=[f"{labels[k]} & {g['files']} & {n(g['metrics']['NFC']['characters_without_whitespace'])} & {n(g['literal_bytes'])}\\\\"
            for k,g in r['whole_file_group_costs'].items()]
    sensitivity=[]
    for norm in ['NFC','NFKC']:
        for unit,label in [('whitespace_tokens','Whitespace tokens'),('alphanumeric_units','Alphanumeric units'),('characters_without_whitespace','Nonspace characters'),('characters_with_collapsed_whitespace','Collapsed-space characters'),('utf8_bytes_with_collapsed_whitespace','Collapsed UTF-8 bytes')]:
            vals=[r['coordinates']['/'.join((v,norm,unit))]['written']['decimal'] for v in ['raw_untrimmed','raw_selected','calibrated_selected']]
            sensitivity.append(f'{norm}: {label} & '+' & '.join(f'{float(v):.6f}' for v in vals)+r'\\')
    return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Supported kernels, translation lattices\\and finite marked quotients}
\author{Comparison of ten complete originals}\date{}
\begin{document}\maketitle
The complete originals contain '''+n(p['source_sum'])+r''' characters. The complete common theory and applications contain '''+n(p['whole_written'])+r''' characters. Charging the common theory once within this topic gives
\[
R=\frac{\sum_{i=1}^{10}c(S_i)}{c(U)+\sum_{i=1}^{10}c(A_i)}
=\frac{'''+str(p['source_sum'])+'}{'+str(p['whole_common'])+'+'+str(p['application_sum'])+r'''}
='''+f"{float(p['written']['decimal']):.6f}"+r'''.
\]
Here $c$ counts nonspace characters in the accepted, selected and calibrated PDF extraction after NFC normalization. The convention is unchanged from the previous comparison. It measures these written proofs and their exposition; it does not estimate minimum proof length or historical originality.

All 152 source pages, all 41 common pages and all 63 application pages are included. The common theory comprises the unchanged 23-page paper (66,140 characters), the complete 14-page supplement (33,986) and the four-page structural argument (8,145). Each is paid in full. Titles, abstracts, proofs, tables, references, addresses and extracted figure labels remain.

\textbf{Individual factors after acquiring the common theory.}
The factors below are $c(S_i)/c(A_i)$. Their prerequisite is the entire common theory, all 99 required program and data contents, and the retained external mathematical premises. Every application is complete; no sibling application is a free premise.
\begin{center}\begin{tabular}{llrrr}\toprule
Original & App & Source & Application & Factor\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
The first eight individual factors are unchanged. L121 now has a one-page application: its four substantial proof bodies have moved into the paid common supplement. L003 includes its entire 17-page application, comprising the seven-page main text and companions of four, four and two pages.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
Both charts use complete manuscript costs and axes beginning at zero. The upper replacement bar includes all three common components and all ten applications. The lower chart shows common acquisition followed by each source/application pair. These 35 bars represent text length, not theorem counts or ratios.

The larger common theory makes L121 a short corollary, but it has an acquisition cost. The complete factor decreases from '''+f"{float(p['prior_whole_written']['decimal']):.6f}"+r''' for nine originals to '''+f"{float(p['written']['decimal']):.6f}"+r''' for ten. The source side gains 45,079 characters; common material gains 42,131; replacing the old L121 application saves 23,322; and L003 adds 42,396 application characters. The net replacement increase is 61,205. Both editions remain available for comparison.
\newpage
\begin{center}\includegraphics[width=\textwidth]{cumulative.pdf}\end{center}
Stage zero acquires the entire common theory. Each subsequent stage adds one complete original and its complete application, in the inherited documentary order followed by L003. The eleven cumulative stages use actual costs. No optimal ordering or general sawtooth law is inferred from this one sequence.

\textbf{Separate complete file inventory.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Whole contents & Count & NFC nonspace & Literal bytes\\\midrule
'''+ '\n'.join(groups)+r'''
\bottomrule\end{tabular}\end{center}
All 253 file occurrences resolve to 203 distinct complete contents. Their accounting classes are disjoint; the original overlapping roles and every file route remain recorded. Data consumed by a proof stays required even when it was produced by an earlier calculation. The complete 28 programs and 71 data contents remain prerequisites.

Executable code is excluded from both sides of the written comparison. Mathematical algorithms described in prose remain. Historical software costs are unknown, so no software-inclusive ratio is reported. The three earlier printed program appendices cover only the old eleven-file subset. Their 30 pages are separate historical representations, never an additional written-proof cost or a complete representation of the enlarged software collection. Partial formal files do not establish complete formalization.
\newpage
\textbf{Sensitivity of the complete written factor.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Raw complete & Raw selected & Calibrated\\\midrule
'''+ '\n'.join(sensitivity)+r'''
\bottomrule\end{tabular}\end{center}
All thirty coordinates and 330 exact fractions are supplied in JSON and CSV. Each fraction retains the unreduced manuscript costs, reduced numerator and denominator, and twelve-place decimal. The previous eight conditional records are unchanged in all thirty coordinates. The 870 PDF cells and 2,030 raw-content cells come from the accepted input audit; this calculation performs no new extraction.

Raw complete text includes running headers and page numbers. Selection removes only their exact audited occurrences. Calibration repairs actual mathematical glyph aliases using the embedded font, encoding and text event. It preserves both visible braces that decoded as TAB, and keeps mapsto components separate. Ordinary ligatures and printed hyphens are not rewritten. NFC and NFKC remain separate sensitivities.

L003 contains 423 occurrences of drawing-font aliases, retained literally and identified separately. They are representation tokens, not a transcription of mathematical or linguistic content. Extracted labels remain, while full graphical structure and unextracted image labels have unknown cost. The scalar therefore measures extraction representation length; it does not price geometric information. Installed libraries, retained external classifications and proof libraries, historical software and complete formalization costs also remain unknown.

\textbf{Scope and attribution.} The previously accepted corrected recovery is the mathematical basis of this comparison. Its order corrections, nonsplitting result, local-period qualifications and precise universal-presentation hypotheses remain in force. Source experiments and conjectures receive no new proof credit from this numerical packet. Ten originals remain ten originals regardless of the number of individual claims or finite checks.

Root authored this arithmetic after separately reviewing the input audit. Earlier fraction, CSV and plotting mechanics are adapted from the accepted L121 comparison; the vector-geometry checker is reused unchanged. The input author and numerical reviewer are identified separately. A fresh numerical review is required before public admission. No mathematical enumeration or Lean compilation is repeated here.
\end{document}
'''

if __name__=='__main__':
    r=load(R/'results.json'); g=plots(r,R)
    (R/'plot_data.json').write_text(json.dumps(g,indent=2)+'\n')
    (R/'reader.tex').write_text(tex(r))
