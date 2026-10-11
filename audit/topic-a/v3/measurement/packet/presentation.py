#!/usr/bin/env python3
"""Complete unified-A acquisition and manuscript costs; no software factor."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import R,load
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def plots(r,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'svg.hashsalt':'unified-a-complete-documents'})
 p=r['primary'];d=p['document_costs'];order=r['source_ids'];apps=r['applications'];fig=plt.figure(figsize=(9,9));ax=fig.add_axes([.21,.75,.70,.14]);bx=fig.add_axes([.21,.10,.70,.53]);fig.text(.04,.965,'One common theory and eight complete applications',fontsize=15,weight='bold');fig.text(.04,.927,'Calibrated selected NFC nonspace characters · all axes start at zero',fontsize=10);bars=[]
 def bar(a,gid,y,w,color,left=0):
  q=a.barh(y,w,left=left,height=.36,color=color)[0];q.set_gid(gid);bars.append((a,gid,y-.18,left,w,.36))
 bar(ax,'bar-whole-source',1,p['source_sum'],SOURCE);left=0
 for doc,color in [('U',COMMON)]+[(apps[x],APP)for x in order]:bar(ax,'bar-whole-'+doc,0,d[doc],color,left);left+=d[doc]
 ax.set_yticks([1,0],['Eight originals','Whole U + eight apps']);ax.set_ylim(-.55,1.55);ax.set_xlim(0,max(p['source_sum'],p['whole_written'])*1.12)
 ax.text(p['source_sum']*1.015,1,f"{p['source_sum']:,}",va='center',fontsize=9);ax.text(p['whole_written']+p['source_sum']*.015,0,f"{p['whole_written']:,}",va='center',fontsize=9)
 mx=max(d['U'],*[d[x]for x in order],*[d[apps[x]]for x in order]);bar(bx,'bar-acquire-U',8,d['U'],COMMON);bx.text(d['U']+mx*.015,8,f"{d['U']:,}",va='center',fontsize=9)
 for i,x in enumerate(order):y=7-i;bar(bx,'bar-source-'+x,y+.2,d[x],SOURCE);bar(bx,'bar-application-'+x,y-.2,d[apps[x]],APP)
 bx.set_yticks(list(range(8,-1,-1)),['Acquire whole U']+[x+' / '+apps[x]for x in order]);bx.set_ylim(-.6,8.6);bx.set_xlim(0,mx*1.12);bx.set_xlabel('Complete manuscript characters; code/data/external premises separate')
 for a in [ax,bx]:a.grid(axis='x',alpha=.2);a.set_axisbelow(True);a.spines[['right','top','left']].set_visible(False);a.tick_params(axis='y',length=0)
 fig.text(.04,.690,'Conditional applications assume whole U and all actual required computation,',fontsize=10);fig.text(.04,.665,'presentation data and retained mathematical premises already acquired.',fontsize=10);fig.text(.20,.025,'Original manuscripts',color=SOURCE,weight='bold');fig.text(.49,.025,'Whole common',color=COMMON,weight='bold');fig.text(.75,.025,'Applications',color='#347567',weight='bold')
 fig.canvas.draw();H=fig.get_figheight()*72;expected={}
 for a,gid,y,left,w,h in bars:
  c=a.transData.transform((left,y));e=a.transData.transform((left+w,y+h));scale=72/fig.dpi;expected[gid]=[c[0]*scale,H-e[1]*scale,(e[0]-c[0])*scale,(e[1]-c[1])*scale]
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 return dict(primary_coordinate=r['primary_coordinate'],expected_rectangles=expected,bars=len(expected),axis_origin_zero=True,software_costs_separate=True,ratio_bars=False)
def tex(r):
 p=r['primary'];d=p['document_costs'];n=lambda x:f'{x:,}';rows=[]
 for x in r['source_ids']:
  a=r['applications'][x];rows.append(f"{x} & {a} & {n(d[x])} & {n(d[a])} & {float(p['conditional'][x]['decimal']):.6f}\\\\")
 groups=[];names={'required_program_or_data':'Required computation and data','inherited_auxiliary':'Inherited auxiliary scripts','current_operational_driver':'Current operational drivers','partial_formal_evidence':'Partial Lean modules'}
 for k,g in r['whole_file_group_costs'].items():groups.append(f"{names[k]} & {g['files']} & {n(g['metrics']['NFC']['characters_without_whitespace'])} & {n(g['literal_bytes'])}\\\\")
 sensitivity=[]
 for norm in ['NFC','NFKC']:
  for unit,label in [('whitespace_tokens','Whitespace tokens'),('alphanumeric_units','Alphanumeric units'),('characters_without_whitespace','Nonspace characters'),('characters_with_collapsed_whitespace','Collapsed-space characters'),('utf8_bytes_with_collapsed_whitespace','Collapsed UTF-8 bytes')]:
   vals=[r['coordinates']['/'.join((v,norm,unit))]['written']['decimal']for v in ['raw_untrimmed','raw_selected','calibrated_selected']];sensitivity.append(f'{norm}: {label} & '+' & '.join(f'{float(v):.6f}'for v in vals)+r'\\')
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Supported kernels and affine constructions}
\author{Eight-original manuscript comparison}\date{}
\begin{document}\maketitle
\textbf{Written papers.} The eight complete originals contain '''+n(p['source_sum'])+r''' characters. The whole common paper and all eight complete applications contain '''+n(p['whole_written'])+r''' characters. The fixed primary comparison is
\[
 \frac{\sum_i c(S_i)}{c(U)+\sum_i c(A_i)}
 =\frac{'''+str(p['source_sum'])+'}{'+str(p['whole_common'])+'+'+str(p['application_sum'])+r'''}
 ='''+f"{float(p['written']['decimal']):.6f}"+r'''.
\]
Here $c$ counts nonwhitespace characters after NFC normalization of the accepted selected and calibrated PDF extraction. The primary convention preserves the previously adopted A and Affine coordinate; it was fixed before these factors were evaluated. This measures observed manuscript text, not minimum proof complexity.

All 119 source pages are in scope. The whole 23-page common paper and all 45 application pages are charged, including full tables and references. There is no free common proof from another topic, overlap subtraction or omitted companion. This unifies the eight accepted principal contracts; numerical calculation adds no mathematical, source, question or formalization credit.

\textbf{After acquiring the common theory and required premises.} Conditional factors are $c(S_i)/c(A_i)$ only after acquiring the entire common theory and the actual required computations, presentation data and retained mathematical results. The full local application is charged in every row.
\begin{center}\begin{tabular}{llrrr}\toprule
Original & App & Source & Application & Conditional\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
The accepted 102 source dispositions and their qualifications remain in force. The scientific source maps are \texttt{scope.json} and \texttt{source\_contract\_map.json}; the input packet's \texttt{source\_scope.json} provides measurement routing. Partial formal scope is separate. These corrected locators clarify the inherited input README without changing any frozen proof or count.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
The upper graph charges every complete application beside the whole common contribution. The lower graph shows that common acquisition cost and all eight source/application pairs. The 27 bars represent document lengths, not ratios or proof-node counts. All axes start at zero. The source order is documentary; it implies no optimal order or sawtooth claim.

\textbf{Symmetric listing boundary.} Executable programs are excluded from both sides of the manuscript comparison. The accepted source listing screen and replacement TeX inventory retain mathematical proof, algorithm prose, presentations and tables. Required computations remain proof premises even though their code is not part of this written-text factor. Historical source software is unknown, so software-inclusive and optional-validation-inclusive factors are null.
\newpage
\textbf{Complete separate computational inventory.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Whole files & Count & NFC nonspace chars & Literal bytes\\\midrule
'''+ '\n'.join(groups)+r'''
\bottomrule\end{tabular}\end{center}
The three full printed appendices occupy 30 pages. Their primary text costs are '''+n(d['CODE_A'])+', '+n(d['CODE_AFFINE'])+' and '+n(d['CODE_DIAGRAM'])+r''' characters. They are alternative representations of the complete computational files, never added to the raw files. The eleven required files include full presentation data and the mathematical replay driver. The two operational drivers remain separate, as do the three inherited auxiliary scripts. Fourteen scoped Lean modules are evidence for limited interfaces, not full formalizations of the source papers.

\textbf{Sensitivity of the whole written factor.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Raw & Selected & Calibrated\\\midrule
'''+ '\n'.join(sensitivity)+r'''
\bottomrule\end{tabular}\end{center}
Raw extraction retains running furniture; selected text removes only the exact accepted furniture, and calibration applies the accepted occurrence-bound glyph repairs. All 30 coordinates and 270 exact fractions are preserved in JSON and CSV, with the complete 600 PDF and 300 raw-file input cells unchanged. Printed hyphens and wrap marks remain in measured text. The nine acquisition rows pay the entire common paper first, then complete applications in the displayed source order; required code/data and external costs remain separate.

L035's unextracted image labels on physical pages 9, 10, 12 and 22 remain unmeasured. Full graphics and layout, external classical proofs, installed software/database construction, historical source programs/data and complete formalization costs remain unknown, not zero. The source/font/visual acceptances are reused transparently; this numerical packet performs no source extraction, GAP computation or Lean compilation. Its author worked on earlier proof and audit packets but did not author the unified measurement inputs. A distinct numerical review remains separate.
\end{document}
'''
if __name__=='__main__':
 r=load(R/'results.json');g=plots(r,R);(R/'plot_data.json').write_text(json.dumps(g,indent=2)+'\n');(R/'reader.tex').write_text(tex(r))
