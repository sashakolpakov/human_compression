#!/usr/bin/env python3
"""Full common/application lengths for the accepted three-source Mixes boundary."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import R,load
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def plot(r,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'svg.hashsalt':'mixes-three-complete-manuscripts'})
 p=r['primary'];d=p['document_costs'];fig=plt.figure(figsize=(9,8));ax=fig.add_axes([.25,.75,.65,.13]);bx=fig.add_axes([.25,.12,.65,.47]);bars=[]
 fig.text(.04,.965,'Three originals, all common theory and complete applications',fontsize=13,weight='bold');fig.text(.04,.928,'Raw PDF extraction · NFC nonspace characters · zero-based axes',fontsize=10)
 def bar(a,gid,y,w,color,left=0):
  q=a.barh(y,w,left=left,height=.32,color=color,edgecolor='white',linewidth=.3)[0];q.set_gid(gid);bars.append((a,gid,y-.16,left,w,.32))
 bar(ax,'bar-whole-source',1,p['source_sum'],SOURCE);left=0
 for doc in r['common_documents']+[a for ss in r['source_ids']for a in r['application_documents'][ss]]:
  bar(ax,'bar-whole-'+doc,0,d[doc],COMMON if doc in r['common_documents']else APP,left);left+=d[doc]
 ax.set_yticks([1,0],['Three originals','All common + all apps']);ax.set_ylim(-.55,1.55);ax.set_xlim(0,max(p['source_sum'],p['whole_written'])*1.14)
 ax.text(p['source_sum']*1.01,1,f"{p['source_sum']:,}",va='center',fontsize=9);ax.text(p['whole_written']+p['source_sum']*.01,0,f"{p['whole_written']:,}",va='center',fontsize=9)
 mx=max(p['whole_common'],*[d[x]for x in r['source_ids']],*p['application_bundles'].values());bar(bx,'bar-acquire-common',3,p['whole_common'],COMMON);bx.text(p['whole_common']+mx*.015,3,f"{p['whole_common']:,}",va='center',fontsize=9)
 for i,x in enumerate(r['source_ids']):
  y=2-i;bar(bx,'bar-source-'+x,y+.19,d[x],SOURCE);bar(bx,'bar-application-'+x,y-.19,p['application_bundles'][x],APP)
 bx.set_yticks([3,2,1,0],['Acquire all common']+[x+' / '+'+'.join(r['application_documents'][x])for x in r['source_ids']]);bx.set_ylim(-.65,3.65);bx.set_xlim(0,mx*1.14);bx.set_xlabel('Complete manuscript characters; required software is separate')
 for a in[ax,bx]:a.grid(axis='x',alpha=.2);a.set_axisbelow(True);a.spines[['top','right','left']].set_visible(False);a.tick_params(axis='y',length=0)
 fig.text(.04,.682,'Conditional rows assume all common theory, both finite certificates and',fontsize=10);fig.text(.04,.653,'retained mathematical premises acquired. Optional testing is not a prerequisite.',fontsize=10)
 fig.text(.19,.045,'Originals',color=SOURCE,weight='bold');fig.text(.44,.045,'Whole common',color=COMMON,weight='bold');fig.text(.72,.045,'Applications',color='#347567',weight='bold')
 fig.canvas.draw();H=fig.get_figheight()*72;expected={}
 for a,gid,y,left,w,h in bars:
  c=a.transData.transform((left,y));e=a.transData.transform((left+w,y+h));s=72/fig.dpi;expected[gid]=[c[0]*s,H-e[1]*s,(e[0]-c[0])*s,(e[1]-c[1])*s]
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 return dict(primary_coordinate=r['primary_coordinate'],expected_rectangles=expected,bars=len(expected),all_axes_start_at_zero=True,whole_common_segments=3,whole_application_segments=5,source_rows=3,software_comparison=None,node_complexity_claim=False)

def tex(r):
 p=r['primary'];d=p['document_costs'];n=lambda x:f'{x:,}';rows=[]
 for s in r['source_ids']:rows.append(f"{s} & {'+'.join(r['application_documents'][s])} & {n(d[s])} & {n(p['application_bundles'][s])} & {float(p['conditional'][s]['decimal']):.6f}\\\\")
 groups=[];names={'required_finite_certificate':'Required finite certificates','optional_validation':'Optional validation programs','operational_driver':'Operational drivers','partial_formal_evidence':'Partial Lean files'}
 for k,g in r['whole_file_group_costs'].items():groups.append(f"{names[k]} & {g['files']} & {n(g['metrics']['NFC']['characters_without_whitespace'])} & {n(g['literal_bytes'])}\\\\")
 sensitivity=[]
 for norm in['NFC','NFKC']:
  for unit,label in[('whitespace_tokens','Whitespace tokens'),('alphanumeric_units','Alphanumeric units'),('characters_without_whitespace','Nonspace characters'),('characters_with_collapsed_whitespace','Collapsed-space characters'),('utf8_bytes_with_collapsed_whitespace','Collapsed UTF-8 bytes')]:
   vals=[r['coordinates']['/'.join([v,norm,unit])]['written']['decimal']for v in['raw_untrimmed','raw_selected','calibrated_selected']];sensitivity.append(norm+': '+label+' & '+' & '.join(f'{float(v):.6f}'for v in vals)+r'\\')
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Mixes, covers and faithfulness}
\author{Three-original manuscript comparison}\date{}
\begin{document}\maketitle
\textbf{Written papers.} The complete F005, L016 and F007 sources contain '''+n(p['source_sum'])+r''' characters. The entire common theory and all applications contain '''+n(p['whole_written'])+r''' characters. The primary comparison is
\[
\frac{\sum_i c(S_i)}{\sum_j c(U_j)+\sum_i c(A_i)}
=\frac{'''+str(p['source_sum'])+'}{'+str(p['whole_common'])+'+'+str(p['application_sum'])+r'''}
='''+f"{float(p['written']['decimal']):.6f}"+r'''.
\]
Here $c$ counts nonwhitespace characters after NFC normalization of complete raw PDF extraction, including page furniture. This primary coordinate was fixed before evaluation and retains the accepted prior Mixes convention. It measures manuscript text, not minimum proof complexity.

All 62 source pages are included. The common papers U, U1 and U2 occupy 5, 4 and 4 pages and contribute '''+n(d['U'])+', '+n(d['U1'])+' and '+n(d['U2'])+r''' characters. The five application papers occupy 27 pages. Both the F005 exceptional companion and the F007 rank-three companion are paid in full. There is no free old common paper, overlap discount or uncharged cross-topic premise.

\textbf{After acquiring the common theory and required premises.} These conditional factors divide each source by its complete application bundle. They require prior acquisition of all three common papers, both required finite certificates and retained mathematical inputs. Optional validation is not a prerequisite.
\begin{center}\begin{tabular}{llrrr}\toprule
Source & Application bundle & Source & Application & Conditional\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
The complete local costs are A1='''+n(d['A1'])+', A2='+n(d['A2'])+', A3='+n(d['A3'])+', A4='+n(d['A4'])+' and A5='+n(d['A5'])+r''' characters. Full common acquisition is charged once in the whole-topic denominator; it is not charged again inside each conditional factor.

The accepted F005/L016 boundaries retain 35 and 19 dispositions. All three final F005 problems remain unanswered. L016's thin-only lemma needs the stated faithfulness repair; its ancillary smallest-example/Atlas census and further-cover questions are outside principal recovery. This numerical work adds no source, question or formalization credit.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
The upper graph shows all three common papers and all five application papers as full segments. The lower graph shows the complete common acquisition and all three source/application pairs. Sixteen bars represent manuscript lengths, not ratios or theorem-node counts. Every axis starts at zero. The recorded acquisition order is documentary, with no optimality or sawtooth claim.

\textbf{Symmetric software boundary.} Concrete executable programs are excluded on both sides. Mathematical proofs, algorithm prose, presentations and formulas remain counted. The two finite certificates remain required premises; their exclusion from this manuscript factor does not make them optional. Historical source software is unknown, so no software-inclusive factor is computed.
\newpage
\textbf{Separate whole-file inventory.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Whole files & Count & NFC nonspace chars & Literal bytes\\\midrule
'''+ '\n'.join(groups)+r'''
\bottomrule\end{tabular}\end{center}
The complete required-certificate PDF has '''+n(d['REQ'])+r''' characters and prints both required programs. F005's certificate also occurs in historical mixed appendix CODE1; this repeated representation is not an additional charge. The retained optional appendix has '''+n(d['VAL'])+r''' characters and covers only its declared older files; F007's new optional programs have no printed representation here. The historical mixed appendices contain '''+n(d['CODE1'])+' and '+n(d['CODE2'])+r''' characters. Printed and raw representations are never added together. The companion checker has a secondary render role and is counted once among optional files. No mandatory nonprogram data file is hidden in this boundary. Three Lean files contain twelve partial declarations, not a formalization of all source results.

\textbf{Sensitivity of the whole written factor.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Raw & Selected & Calibrated\\\midrule
'''+ '\n'.join(sensitivity)+r'''
\bottomrule\end{tabular}\end{center}
All 30 coordinates and 120 exact fractions are retained in JSON/CSV. The 330 prior PDF and 130 prior raw-file cells are unchanged; the 120 new PDF and 40 new raw cells are the independently accepted values. Selected variants remove only exact page furniture; calibration applies the accepted occurrence-bound repairs. F007 has 1,351 substitutions, including decoded Greek-name aliases. Publisher emblems remain in raw text and only their bound footer is removed in selected variants. Full source figures, graphics, retained outside proofs, software/runtime and complete formalization costs remain unknown.

F007's 48 numbered rows and six additional dispositions retain their accepted qualifications. Its unnumbered page-25 chain-class paragraph is not recovered; Problems 1 and 2 remain unanswered. Problem 3 has the natural reconstruction result and the arbitrary-isomorphism result for finite posets with connected full flag graph. No general infinite arbitrary-isomorphism result or historical priority is claimed. The input authorship, distinct review and root adoption are bound; this numerical packet neither reextracts sources nor reruns scientific programs or Lean.
\end{document}
'''
if __name__=='__main__':
 r=load(R/'results.json');g=plot(r,R);(R/'plot_data.json').write_text(json.dumps(g,indent=2)+'\n');(R/'reader.tex').write_text(tex(r))
