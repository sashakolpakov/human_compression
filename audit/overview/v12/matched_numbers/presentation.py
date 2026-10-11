#!/usr/bin/env python3
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import load
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def plots(d,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
 fig=plt.figure(figsize=(9,8));ax=fig.add_axes([.23,.66,.69,.23]);bx=fig.add_axes([.23,.13,.69,.40]);bars=[]
 fig.text(.06,.95,'Manuscripts with executable listings excluded on both sides',fontsize=14,weight='bold')
 fig.text(.06,.915,'Calibrated selected text · NFC nonspace characters · zero-based axes',fontsize=10)
 def bar(a,gid,y,width,color,left=0):
  patch=a.barh(y,width,left=left,height=.30,color=color)[0];patch.set_gid(gid);bars.append((a,gid,left,y-.15,width,.30))
 names=list(d['topics']);maximum=max(t['primary']['source_sum'] for t in d['topics'].values())
 for i,name in enumerate(names):
  p=d['topics'][name]['primary'];y=2-i;bar(ax,'bar-whole-source-'+name,y+.18,p['source_sum'],SOURCE);bar(ax,'bar-common-'+name,y-.18,p['common_sum'],COMMON);left=p['common_sum']
  for source,cost in p['application_bundle_costs'].items():bar(ax,'bar-bundle-'+source,y-.18,cost,APP,left);left+=cost
 ax.set_yticks([2,1,0],names);ax.set_xlim(0,maximum*1.08);ax.set_ylim(-.6,2.6)
 fig.text(.06,.585,'Conditional pairs: whole topic common theory and actual required premises',fontsize=10)
 fig.text(.06,.562,'must already be acquired. Optional validation is not a proof premise.',fontsize=10)
 pairs=[(name,source,f) for name,t in d['topics'].items() for source,f in t['primary']['conditional'].items()]
 maximum=max(x[2]['source_cost'] for x in pairs)
 for i,(name,source,f) in enumerate(pairs):
  y=5-i;bar(bx,'bar-pair-source-'+source,y+.18,f['source_cost'],SOURCE);bar(bx,'bar-pair-app-'+source,y-.18,f['replacement_cost'],APP)
 bx.set_yticks(range(5,-1,-1),[x[1] for x in pairs]);bx.set_xlim(0,maximum*1.08);bx.set_ylim(-.55,5.55);bx.set_xlabel('Complete manuscript characters after the exact listing masks')
 for a in [ax,bx]:
  a.grid(axis='x',alpha=.2);a.set_axisbelow(True);a.spines[['right','top','left']].set_visible(False);a.tick_params(axis='y',length=0)
 fig.text(.23,.035,'Original manuscripts',color=SOURCE,weight='bold');fig.text(.52,.035,'Whole common',color=COMMON,weight='bold');fig.text(.77,.035,'Applications',color='#347567',weight='bold')
 fig.canvas.draw();H=fig.get_figheight()*72;expected={}
 for a,gid,left,y,w,h in bars:
  p=a.transData.transform((left,y));q=a.transData.transform((left+w,y+h));scale=72/fig.dpi;expected[gid]=[p[0]*scale,H-q[1]*scale,(q[0]-p[0])*scale,(q[1]-p[1])*scale]
 for ext in ['svg','pdf']:fig.savefig(out/('costs.'+ext))
 plt.close(fig);return {'rectangles':expected,'bars':len(expected),'axis_origins_zero':True,'software_inclusive_factor':None}
def reader(d):
 n=lambda x:f'{x:,}';whole=[];pairs=[];sensitivity=[]
 for name,t in d['topics'].items():
  p=t['primary'];whole.append(f"{name} & {n(p['source_sum'])} & {n(p['common_sum'])} & {n(sum(p['application_bundle_costs'].values()))} & {float(p['written']['decimal']):.6f}\\\\")
  for s,f in p['conditional'].items():pairs.append(f"{s} & {n(f['source_cost'])} & {n(f['replacement_cost'])} & {float(f['decimal']):.6f}\\\\")
  vals=[float(x['written']['decimal']) for k,x in t['coordinates'].items() if not k.startswith('text_only')]
  sensitivity.append(f"{name} & {min(vals):.6f} & {max(vals):.6f}\\\\")
 text=[];names={'whitespace_tokens':'Whitespace tokens','alphanumeric_units':'Alphanumeric units','characters_without_whitespace':'Nonspace characters','characters_with_collapsed_whitespace':'Collapsed-space characters','utf8_bytes_with_collapsed_whitespace':'Collapsed UTF-8 bytes'}
 for normalization in ['NFC','NFKC']:
  for unit,label in names.items():
   c=d['topics']['Operations']['coordinates'][f'text_only_without_listings/{normalization}/{unit}'];text.append(f"{normalization}: {label} & {c['source_sum']:,} & {c['whole_written']:,} & {float(c['written']['decimal']):.6f}\\\\")
 return r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=27mm]{geometry}\usepackage{fontspec,booktabs,amsmath,graphicx,hyperref}
\setmainfont{STIXGeneral}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\title{Matched manuscript comparisons}\author{Chamber, ChiralEnumeration and Operations}\date{}
\begin{document}\maketitle
\textbf{Written papers.} These author calculations use the distinctly accepted symmetric listing masks. The formula for each topic remains
\[
 R=\frac{\sum_i c(L_i)}{c(U)+\sum_i c(A_i)}.
\]
The whole common theory and every complete application or companion are paid. The primary unit is NFC nonspace characters in calibrated selected text. Only seven concrete executable blocks have been removed from the source coordinate, matching the absence of listings in the replacement scientific manuscripts. All mathematical prose, algorithm explanations, tables and references remain.
\begin{center}\begin{tabular}{lrrrr}\toprule
Topic & Originals & Common & Applications & Factor\\\midrule
'''+ '\n'.join(whole)+r'''
\bottomrule\end{tabular}\end{center}
A factor below one means that the replacement papers are longer. These compare manuscript lengths; complete software and outside proof costs remain separate. The calculations await distinct review before the held public comparisons can be restored.

\textbf{After acquiring the common theory and required premises.} Each conditional factor is $c(L_i)/c(A_i)$, where $A_i$ contains all companions for that original. It assumes the entire topic common theory, actual required programs, decoders, data and retained mathematical results. Optional validation is not a theorem premise; there is no free theory from another topic.
\begin{center}\begin{tabular}{lrrr}\toprule
Original & Source & Complete application & Conditional\\\midrule
'''+ '\n'.join(pairs)+r'''
\bottomrule\end{tabular}\end{center}
The affected originals are L008, L028 and N006. The N016, N005 and N007 conditional values are unchanged and shown to retain each topic's complete scope. In Operations, N006's application includes the general paper, all nine sporadic certificates and the Harada--Norton companion; N005 and N007 keep their entire applications. The three whole theories are charged separately.

All 43 recoveries and 63 pending originals remain unchanged. No scientific, question or formal credit is created by changing a measurement boundary. All software-inclusive factors and unavailable historical software costs remain null.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
The graphs show complete manuscript costs with axes starting at zero. Common theory is the blue portion of every whole-topic replacement bar; complete applications form the remaining portion. The conditional graph omits the already acquired common cost only under its stated acquisition condition. Required software and outside results remain separately disclosed, not treated as free or relabeled optional.

\textbf{What the masks exclude.} L008 has three Magma functions on physical pages 8--10, including literal program comments. L028 has three enumeration functions/procedure on pages 9--12; Lemma 4.5 and its entire proof, surrounding algorithm descriptions and Section 4.3 remain counted. N006 has one McL pseudocode block on page 20; the group construction, intersection-property definition, halving argument and conclusion remain counted. Twelve page-local chunks avoid all running headers and page numbers. The eleven replacement listing masks are empty.
\newpage
\textbf{Sensitivity and unchanged evidence.} All 600 accepted input cells are reused without re-extraction. Five hundred are unchanged, including every replacement cost. Each topic has the original three variants, two normalizations and five units. The complete 270 standard fractions and 40 additional Operations text-only fractions are supplied as exact integer fractions in JSON and CSV.
\begin{center}\begin{tabular}{lrr}\toprule
Whole topic, 30 standard coordinates & Minimum & Maximum\\\midrule
'''+ '\n'.join(sensitivity)+r'''
\bottomrule\end{tabular}\end{center}
These ranges disclose sensitivity; the primary coordinate was fixed before evaluation and is not selected from the range. Raw extraction, exact-furniture selection and calibrated selection remain distinct.

\textbf{Operations: text-only graphical sensitivity.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Originals & Whole replacement & Factor\\\midrule
'''+ '\n'.join(text)+r'''
\bottomrule\end{tabular}\end{center}
This alternative replaces only previously bound graphical-proxy events by separators and applies the same listing masks. It does not remove ordinary labels or measure full diagram geometry. The original graphical-proxy sensitivity, font maps, physical pages and all scientific editions are unchanged. Full graphics, external proof costs, historical software and complete formalization costs remain unknown, not zero.

\textbf{Whole software remains visible.} The 46 exact files remain bound: Chamber's two mathematical/validation programs, three drivers and three partial formal files; ChiralEnumeration's three programs, driver and partial formal file; Operations' 23 mathematical/validation files, two required decoding drivers, five operational drivers and three partial formal files. Required and optional roles are unchanged. Complete installed/Atlas data and retained catalogue assumptions remain in the inherited inventory; no representation bytes or witness prerequisites were discarded. Partial printed appendices do not become a new full Operations software route.

The numerical author independently reviewed the new listing-mask inputs but did not author them. This arithmetic still requires distinct review. Earlier counts and comparisons remain immutable historical observations; this packet supplies a proposed successor boundary and does not rewrite earlier artifacts or the public catalogue.
\end{document}
'''
def main():
 r=Path(__file__).resolve().parent;d=load(r/'results.json');(r/'reader.tex').write_text(reader(d));(r/'plot_data.json').write_text(json.dumps(plots(d,r),indent=2)+'\n')
if __name__=='__main__':main()
