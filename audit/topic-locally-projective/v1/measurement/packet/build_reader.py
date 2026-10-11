#!/usr/bin/env python3
"""Full-cost reader and actual zero-origin bars; no science recomputation."""
import argparse,json,subprocess
from pathlib import Path
from compute import accepted_inputs,derive,need,dump

def render_assets(r,out):
 out.mkdir(parents=True,exist_ok=False)
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import Patch
 plt.rcParams.update({'svg.hashsalt':'LocallyProjective-v1','font.family':'DejaVu Sans','font.size':9})
 c=r['primary'];d=c['document_costs'];m=c['mandatory_data_cost'];w=c['written_cost'];pc=c['printed_program_cost'];rc=c['raw_program_cost']
 colors=['#6d819a','#396a92','#57a68d','#a181bf','#e0a246']
 labels=['Sources','Whole common','Applications','Programs','Mandatory JSON']
 bars=[('Originals',[c['source_cost'],0,0,0,0]),('Written replacement',[0,c['whole_common_cost'],c['application_cost'],0,0]),('Printed programs + data',[0,c['whole_common_cost'],c['application_cost'],pc,m]),('Raw programs + data',[0,c['whole_common_cost'],c['application_cost'],rc,m])]
 fig,ax=plt.subplots(figsize=(8.2,2.8))
 for y,(label,vals) in enumerate(bars):
  x=0
  for j,val in enumerate(vals):
   if val:ax.barh(y,val,left=x,color=colors[j],height=.55);x+=val
  ax.text(x+700,y,f'{x:,}',va='center',fontsize=9)
 ax.set_yticks(range(4),[z[0] for z in bars]);ax.invert_yaxis();ax.set_xlim(0,max(sum(b[1]) for b in bars)*1.13);ax.set_xlabel('NFC non-space characters; calibrated selected extraction')
 ax.legend(handles=[Patch(color=c,label=l) for c,l in zip(colors,labels)],ncol=3,loc='lower left',bbox_to_anchor=(0,1.01),frameon=False,fontsize=8)
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);fig.tight_layout()
 rects=[dict(x=float(p.get_x()),y=float(p.get_y()),width=float(p.get_width()),height=float(p.get_height())) for p in ax.patches]
 for ext in ['svg','pdf','png']:fig.savefig(out/('costs.'+ext),dpi=170,metadata={'Date':None} if ext=='svg' else {'CreationDate':None,'ModDate':None} if ext=='pdf' else None)
 plt.close(fig)
 docs=[('L084 original',d['L084']),('L095 original',d['L095']),('Whole common: proof + tables',c['whole_common_cost']),('L084 application',d['A1']),('L095 application',d['A2'])]
 fig,ax=plt.subplots(figsize=(8.2,2.6));ax.barh(range(5),[x[1] for x in docs],color=[colors[0],colors[0],colors[1],colors[2],colors[2]],height=.6)
 for y,(_,val) in enumerate(docs):ax.text(val+200,y,f'{val:,}',va='center')
 ax.set_yticks(range(5),[x[0] for x in docs]);ax.invert_yaxis();ax.set_xlim(0,max(x[1] for x in docs)*1.16);ax.set_xlabel('Full document costs; common acquisition is paid once')
 ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True);fig.tight_layout()
 drects=[dict(x=float(p.get_x()),y=float(p.get_y()),width=float(p.get_width()),height=float(p.get_height())) for p in ax.patches]
 for ext in ['svg','pdf','png']:fig.savefig(out/('documents.'+ext),dpi=170,metadata={'Date':None} if ext=='svg' else {'CreationDate':None,'ModDate':None} if ext=='pdf' else None)
 plt.close(fig)
 dump(out/'plot_data.json',{'primary':[c[k] for k in ['variant','normalization','unit']],'zero_origin':True,'whole_cost_graph':{'components':labels,'bars':[{'label':label,'components':dict(zip(labels,vals)),'total':sum(vals)} for label,vals in bars],'rendered_rectangles':rects},'common_and_applications_graph':{'bars':[dict(label=l,total=n) for l,n in docs],'rendered_rectangles':drects},'all_full_document_costs':True,'printed_raw_alternative':True,'mandatory_data_in_both_routes':True,'acquisition_curve_claimed':False})
 nice=lambda n:f'{n:,}'
 def mf(f):return r'\frac{'+str(f['numerator'])+'}{'+str(f['denominator'])+'}='+f"{f['factor']:.6f}"
 q=c['comparisons'];cond=c['conditional_applications'];ac=c['conditional_acquisition']
 unitnames=dict(whitespace_tokens='Whitespace tokens',alphanumeric_units='Alphanumeric runs',characters_without_whitespace='Non-space characters',characters_with_collapsed_whitespace='Collapsed characters',utf8_bytes_with_collapsed_whitespace='Collapsed UTF-8 bytes')
 tables=[]
 for var,title in [('raw_untrimmed','Untrimmed extraction'),('raw_selected','Exact furniture removed'),('calibrated_selected','Furniture removed and visible symbols calibrated')]:
  rows=[]
  for row in r['coordinates']:
   if row['variant']==var:
    fs=list(row['comparisons'].values())+list(row['conditional_applications'].values())
    rows.append(unitnames[row['unit']]+' & '+row['normalization']+' & '+' & '.join(f"{f['factor']:.6f}" for f in fs)+r' \\')
  tables.append(r'\par\vspace{6pt}\textbf{'+title+r'}\par\smallskip\begin{tabular}{@{}llrrrrr@{}}\toprule Unit & Form & Written & Printed+data & Raw+data & L084 cond. & L095 cond.\\\midrule '+'\n'.join(rows)+r'\bottomrule\end{tabular}')
 tex=r'''\documentclass[a4paper,11pt]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}\setlength{\emergencystretch}{2em}
\title{Locally projective quotients: complete written costs}
\author{Human Compression project}\date{Private numerical candidate; distinct review pending}
\begin{document}\raggedright\begin{center}{\Large\bfseries Locally projective quotients: complete written costs}\\[4pt]Human Compression project\\{\small Private numerical candidate; distinct review pending}\end{center}
Two originals remain distinct: L084 is the complete two-page 2006 publisher
erratum, and L095 is the full fifteen-page July 2003 arXiv v1. The accepted
replacement recovers their corrected principal contracts, with all 52 source
dispositions and all 145 historical rows retained. No unseen journal edition
or corrected source text is substituted in the numerator.

\section*{Written papers}
The primary unit is the number of non-whitespace characters in NFC, after exact
running furniture removal and the accepted visible-symbol calibration.
Titles, abstract, addresses, version banner, tables and references remain.
\begin{center}\begin{tabular}{@{}lrr@{}}\toprule Complete document & Pages & Characters\\\midrule
L084 original & 2 & @S1@\\
L095 original & 15 & @S2@\\
Common proof & 7 & @U@\\
Common census tables & 5 & @T@\\
L084 application & 2 & @A1@\\
L095 application & 3 & @A2@\\\midrule
Combined originals & 17 & @SOURCE@\\
Whole common and applications & 17 & @WRITTEN@\\\bottomrule\end{tabular}\end{center}
The common bundle includes the complete marked-group, geometry and census
proofs. Neither application borrows an unpaid proof from its sibling or another
topic. Writing $U^*=U+\mathrm{tables}$, the combined written comparison is
\[\frac{c(L084)+c(L095)}{c(U^*)+c(A_1)+c(A_2)}=@WF@.\]
The written replacement is longer by @EXCESS@ characters in this coordinate.
A factor below one records that increase; it is not a compression gain.
\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
\newpage
\section*{Including the complete programs and data}
All six complete mathematical programs are required finite computations.
Their six-page printed appendix costs @PRINT@ characters; the full raw
alternative costs @RAW@. In \emph{both} cases the entire required
\texttt{source\_tables.json} adds @DATA@ characters (39,150 raw bytes).
Its 145 rows are used in historical reconciliation, not subgroup enumeration.
The printed code is not a substitute for these data. Thus the two alternatives are
\[\frac{c(L084)+c(L095)}{c(U^*)+c(A_1)+c(A_2)+c(\mathrm{printed\ programs})+c(\mathrm{data})}=@PF@,\]
\[\frac{c(L084)+c(L095)}{c(U^*)+c(A_1)+c(A_2)+c(\mathrm{raw\ programs})+c(\mathrm{data})}=@RF@.\]
Neither row adds both code representations or prunes any file or data field.

\section*{After acquiring the whole common theory, programs and data}
The conditional comparisons are source/application only after that acquisition:
\[\frac{c(L084)}{c(A_1)}=@C1@,\qquad \frac{c(L095)}{c(A_2)}=@C2@.\]
The prior known acquisition is @COMMON@ for the whole common bundle, plus the
complete code and @DATA@ for data: @ACPRINT@ using printed code, or @ACRAW@
using raw code. Retained external inputs are also prerequisites; their full costs
are unknown. These conditional factors do not replace the combined comparison.
\begin{center}\includegraphics[width=\linewidth]{documents.pdf}\end{center}

\section*{Separate costs and limits}
The six raw programs total 24,255 bytes. Three operational drivers total 32,220
raw bytes (@DRIVER@ primary characters). Eleven regenerated outputs total
3,470,182 bytes, including the complete computed subgroup representatives.
They remain separately inventoried; outputs generated in the same computation
are not charged again as independent enumeration inputs. No output-text metric
or formal proof cost is inferred from storage bytes. There are no Lean files or
declarations in this edition.

Classical local geometry and polytope correspondences, named finite groups,
and exact GAP/ACE/NetworkX algorithms remain retained inputs. Thirteen selected
runtime/model pins do not measure their full implementations or proofs.
Those costs, historical software, graphics/layout and full formalization remain
unknown, not zero. The unavailable historical \texttt{g.txt} is not used.
No new mathematical, source, question or formal credit is claimed.
\newpage
\section*{Metric and extraction sensitivity}
All 30 coordinates keep the same complete boundary. ``Printed+data'' and
``Raw+data'' include the full mandatory JSON; the two conditional columns
assume all prior acquisition specified above. The table rounds display only;
JSON and CSV retain all 150 exact fractions.

{\fontsize{8.4}{10}\selectfont @TABLES@}

The untrimmed coordinate retains every extracted character, including running
furniture. Selected variants remove only the exact erratum running header and
isolated page numbers. Eight actual font classes receive 61 occurrence-bound
repairs: calligraphic capitals, a correspondence envelope, proof-end squares
and mapsto tails. A tail remains separate from its adjacent arrow. Printed
hyphens remain literal; NFC and NFKC are distinct sensitivities.

The source’s incorrect historical counts are not changed by calibration.
L095’s table rules are inline images. This is a full-document extractable-text
comparison, not a complete measure of graphical construction or intrinsic proof
complexity. The numerical author also authored the inputs; the accepted input
review was distinct. These new calculations require their own independent
review. No source extraction, GAP, census or Lean execution was repeated here.
\end{document}
'''
 substitutions={'S1':nice(d['L084']),'S2':nice(d['L095']),'U':nice(d['U']),'T':nice(d['TABLES']),'A1':nice(d['A1']),'A2':nice(d['A2']),'SOURCE':nice(c['source_cost']),'WRITTEN':nice(w),'EXCESS':nice(w-c['source_cost']),'WF':mf(q['written_papers']),'PRINT':nice(pc),'RAW':nice(rc),'DATA':nice(m),'PF':mf(q['printed_programs_plus_mandatory_data']),'RF':mf(q['raw_programs_plus_mandatory_data']),'C1':mf(cond['L084']),'C2':mf(cond['L095']),'COMMON':nice(c['whole_common_cost']),'ACPRINT':nice(ac['printed_total']),'ACRAW':nice(ac['raw_total']),'DRIVER':nice(c['operational_driver_cost_separate']),'TABLES':'\n'.join(tables)}
 for k,val in substitutions.items():tex=tex.replace('@'+k+'@',val)
 need('@' not in tex.replace('@{}',''),'unresolved reader substitution')
 (out/'reader.tex').write_text(tex)
 return tex

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');render_assets(derive(*accepted_inputs()),a.out)
 if a.render:
  for i in range(2):
   q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(a.out/f'render{i}.log').write_bytes(q.stdout);need(q.returncode==0,'XeLaTeX render')
 print('PASS reader and complete-document graphs')
