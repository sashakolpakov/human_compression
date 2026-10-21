#!/usr/bin/env python3
"""Whole-document charts and reader, generated solely from the fixed results."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import load
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def plots(result,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
 p=result['primary'];d=p['document_costs'];order=result['source_ids'];apps=result['applications'];expected={}
 fig=plt.figure(figsize=(9,7.5));ax=fig.add_axes([.20,.71,.72,.17]);bx=fig.add_axes([.20,.11,.72,.48])
 fig.text(.05,.96,'Complete papers and conditional applications',fontsize=16,weight='bold')
 fig.text(.05,.915,'NFC nonspace characters · raw extraction · all axes start at zero',fontsize=10)
 bars=[]
 def bar(axis,gid,y,w,color,left=0):
  patch=axis.barh(y,w,left=left,height=.36,color=color)[0];patch.set_gid(gid);bars.append((axis,gid,y-.18,left,w,.36))
 bar(ax,'bar-whole-source',1,p['source_sum'],SOURCE)
 left=0
 for key,color in [('U',COMMON)]+[(apps[x],APP) for x in order]:
  bar(ax,'bar-whole-'+key,0,d[key],color,left);left+=d[key]
 ax.set_yticks([1,0],['Five originals','Common + five apps']);ax.set_ylim(-.55,1.55);ax.set_xlim(0,p['source_sum']*1.12)
 ax.text(p['source_sum']*1.01,1,f"{p['source_sum']:,}",va='center',fontsize=9)
 ax.text(p['whole_written']+p['source_sum']*.015,0,f"{p['whole_written']:,}",va='center',fontsize=9)
 maxv=max(d['U'],*[d[x] for x in order]);bar(bx,'bar-acquire-U',5,d['U'],COMMON)
 bx.text(d['U']+maxv*.015,5,f"{d['U']:,}",va='center',fontsize=9)
 for i,x in enumerate(order):
  y=4-i;bar(bx,'bar-source-'+x,y+.2,d[x],SOURCE);bar(bx,'bar-application-'+x,y-.2,d[apps[x]],APP)
 bx.set_yticks([5,4,3,2,1,0],['Acquire whole U']+[x+' / '+apps[x] for x in order]);bx.set_ylim(-.6,5.6);bx.set_xlim(0,maxv*1.12)
 bx.set_xlabel('Complete manuscript characters; programs and external premises separate')
 for a in [ax,bx]:
  a.grid(axis='x',alpha=.2);a.set_axisbelow(True);a.spines[['right','top','left']].set_visible(False);a.tick_params(axis='y',length=0)
 fig.text(.05,.655,'Conditional comparisons start only after whole U, six required programs,',fontsize=10)
 fig.text(.05,.632,'mandatory JSON and retained mathematical premises have been acquired.',fontsize=10)
 fig.text(.20,.018,'Original manuscripts',color=SOURCE,weight='bold');fig.text(.49,.018,'Whole common',color=COMMON,weight='bold');fig.text(.73,.018,'Applications',color='#347567',weight='bold')
 fig.canvas.draw();height=fig.get_figheight()*72
 for axis,gid,y,left,w,h in bars:
  a=axis.transData.transform((left,y));b=axis.transData.transform((left+w,y+h));scale=72/fig.dpi
  expected[gid]=[a[0]*scale,height-b[1]*scale,(b[0]-a[0])*scale,(b[1]-a[1])*scale]
 for extension in ['svg','pdf']:fig.savefig(out/('costs.'+extension))
 plt.close(fig)
 return {'primary_coordinate':result['primary_coordinate'],'unit':'raw NFC nonspace characters','expected_rectangles':expected,'bars':len(expected),'axis_origin_zero':True,'software_costs_separate':True,'ratios_are_not_plotted_as_costs':True}
def tex(result):
 p=result['primary'];d=p['document_costs'];groups=result['whole_file_group_costs'];n=lambda x:f'{x:,}'
 rows=[]
 for x in result['source_ids']:
  a=result['applications'][x];f=p['conditional'][x]
  rows.append(f"{x} & {a} & {n(d[x])} & {n(d[a])} & {float(f['decimal']):.6f}\\\\")
 sensitivity=[]
 units=[('whitespace_tokens','Whitespace tokens'),('alphanumeric_units','Alphanumeric units'),('characters_without_whitespace','Nonspace characters'),('characters_with_collapsed_whitespace','Collapsed-space characters'),('utf8_bytes_with_collapsed_whitespace','Collapsed UTF-8 bytes')]
 for normalization in ['NFC','NFKC']:
  for unit,label in units:
   values=[result['coordinates']['/'.join((v,normalization,unit))]['written']['decimal'] for v in ['raw_untrimmed','raw_selected','calibrated_selected']]
   sensitivity.append(f"{normalization}: {label} & "+' & '.join(f'{float(v):.6f}' for v in values)+r'\\')
 group_rows=[]
 names={'required_programs':'Required programs','required_data':'Mandatory JSON','optional_validation':'Optional validation','operational_drivers':'Operational drivers','partial_formal':'Partial Lean files'}
 for key,g in groups.items():group_rows.append(f"{names[key]} & {g['files']} & {n(g['metrics']['NFC']['characters_without_whitespace'])} & {n(g['literal_bytes'])}\\\\")
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Projective groups, polytopes and maniplexes}
\author{Five-source manuscript comparison}\date{}
\begin{document}\maketitle
\textbf{Written papers.} The five complete originals contain '''+n(p['source_sum'])+r''' characters, compared with '''+n(p['whole_written'])+r''' in the whole common theory and five applications. In the fixed primary coordinate, the manuscript factor is
\[
 \frac{\sum_i c(L_i)}{c(U)+\sum_i c(A_i)}
 =\frac{'''+str(p['source_sum'])+'}{'+str(p['whole_common'])+'+'+str(p['application_sum'])+r'''}
 ='''+f"{float(p['written']['decimal']):.6f}"+r'''.
\]
Here $c$ counts nonwhitespace characters after NFC normalization of raw, untrimmed PDF extraction. Printed hyphens, headers and page numbers remain. This is a manuscript comparison, not a complete proof, software or graphics cost comparison.

The entire 20-page common paper is charged once. In the source order below, the five applications occupy 1, 2, 5, 2 and 4 pages, paired with originals of 9, 14, 11, 8 and 25 pages respectively. All 67 source pages and 34 replacement scientific pages are included. No other topic supplies a free common proof.

\textbf{After acquiring the common theory and required premises.} Each conditional factor below is $c(L_i)/c(A_i)$. It assumes acquisition of the full common paper, all six required programs, the mandatory JSON and the retained mathematical inputs. Optional validation is not a theorem premise.
\begin{center}\begin{tabular}{llrrr}\toprule
Original & App & Source & Application & Conditional\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}

The shared proofs cover projective centralizers and end subgroups, exceptional marked groups, reversal of rotation generators, trace and subfield restrictions, and primitive-square constructions. These are the accepted five principal contracts, with 110 explicit source dispositions. Full manuscripts are the numerator even where ancillary tables or quoted theorems remain retained rather than regenerated.

The exact L043 edition is the 25-page arXiv1606.08017v1. Its residue-10 branch modulo 11 is restored with the explicit 571 witness; auxiliary trace, abelianization and finite-table corrections stay visible. L056's auxiliary count is qualified in characteristic two. L079's P\(\Sigma\)L\((2,25)\) case lies outside its retained principal contract. The complete source maps preserve the older L021 corrections and all ancillary exclusions. No new scientific or question credit is assigned by this calculation.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
The upper graph charges the whole common paper and every application. The lower graph shows the common acquisition cost and all five complete source/application pairs. It is a document-cost picture, not a theorem-dependency graph or a minimality claim. Full required software and external premises are separate; no reduction in their cost is inferred from shorter application bars.

\textbf{Symmetric software boundary.} The five sources and six replacement scientific papers contain no executable listings. Mathematical tables, relations, matrices and algorithm prose remain on both sides. Required and optional replacement programs are outside this manuscript coordinate; their complete inventories are retained. Historical source software costs are unknown, so every software-inclusive factor remains null.
\newpage
\textbf{Complete separate inventories.}
\begin{center}\begin{tabular}{lrrr}\toprule
Whole files & Count & NFC nonspace chars & Literal bytes\\\midrule
'''+ '\n'.join(group_rows)+r'''
\bottomrule\end{tabular}\end{center}
The 20-page required appendix contains '''+n(d['REQUIRED'])+r''' primary characters and includes the complete mandatory JSON. The seven-page optional appendix contains '''+n(d['VALIDATION'])+r''' characters. Printed and raw forms are alternatives, never additive. Required status is unchanged: the six finite-proof programs and certificate data remain prerequisites. The seven Lean files support 42 scoped declarations (nine new), not full source formalization.

For historical accuracy, L043 names \emph{Magma} and the \(L_2\)-quotient algorithm. Three frozen input metadata fields incorrectly say GAP; our implementations use GAP and Python. This explicit attribution correction changes neither counts nor program roles.

\textbf{Sensitivity of the whole written factor.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Raw & Selected & Calibrated\\\midrule
'''+ '\n'.join(sensitivity)+r'''
\bottomrule\end{tabular}\end{center}
``Selected'' removes only the exact accepted running furniture. ``Calibrated'' additionally uses the accepted event-bound glyph repairs; brace pieces and mapsto strokes are disclosed text proxies, not reconstructed layout. Both normalizations and all five units are retained: 30 coordinates and 180 exact fractions are supplied in JSON and CSV. The primary coordinate was fixed before evaluation; it was not chosen from these factors.

Full graphical and formula-layout costs, classical external proofs, historical software, catalogue construction and complete formalization costs remain unknown, not zero. Retained inputs include Dickson/Giudici subgroup results, projective automorphisms, Schulte--Weiss and McMullen--Schulte geometry, the character estimate, finite-field facts, and the Dirichlet/Suzuki inputs to L021. Full costs are not silently supplied by another topic. The exact accepted input and scientific review manifests are bound in the portable packet; this numerical author also authored the expanded science. A distinct arithmetic review is still required.
\end{document}
'''
def main():
 r=Path(__file__).resolve().parent;d=load(r/'results.json');g=plots(d,r);(r/'plot_data.json').write_text(json.dumps(g,indent=2)+'\n');(r/'reader.tex').write_text(tex(d))
if __name__=='__main__':main()
