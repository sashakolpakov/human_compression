"""Whole B6 costs and explicit acquisition, adapted from the accepted A9 chart mechanics."""
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_HALF_UP
import os,tempfile,json
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'B6_numbers_mpl'))
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'B6_numbers_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from calculate import R,load,IDS,APPS,PRIMARY,U,V,N,GROUPS,key
SOURCE='#344354';COMMON='#286e99';APP='#81bdb0'
def display(f):
 with localcontext()as c:c.prec=50;return str((Decimal(f['numerator'])/Decimal(f['denominator'])).quantize(Decimal('.000001'),rounding=ROUND_HALF_UP))
def finish(fig,bars,out,stem):
 fig.canvas.draw();H=fig.get_figheight()*72;expected={}
 for ax,gid,x,y,w,h in bars:
  low=ax.transData.transform((x,y));high=ax.transData.transform((x+w,y+h));scale=72/fig.dpi;expected[gid]=[low[0]*scale,H-high[1]*scale,(high[0]-low[0])*scale,(high[1]-low[1])*scale]
 fig.savefig(out/(stem+'.svg'),metadata={'Date':None});fig.savefig(out/(stem+'.pdf'),metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 return dict(expected_rectangles=expected,bars=len(expected),axis_origin_zero=True,manuscript_only=True)
def plots(r,out):
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42,'svg.hashsalt':'B6-whole-common-and-applications'})
 p=r['primary'];d=p['document_costs'];fig=plt.figure(figsize=(9,8));ax=fig.add_axes([.23,.76,.66,.14]);bx=fig.add_axes([.23,.12,.66,.51]);bars=[]
 def bar(ax,gid,y,w,color,left=0):
  q=ax.barh(y,w,left=left,height=.34,color=color)[0];q.set_gid(gid);bars.append((ax,gid,left,y-.17,w,.34))
 fig.text(.04,.965,'Two full common papers and six complete applications',fontsize=14,weight='bold');fig.text(.04,.925,'Raw untrimmed NFC nonspace characters; every cost axis begins at zero.',fontsize=10)
 bar(ax,'bar-whole-source',1,p['source_sum'],SOURCE);left=0
 for doc in ['U_B','U_B6']+list(APPS.values()):bar(ax,'bar-whole-'+doc,0,d[doc],COMMON if doc.startswith('U')else APP,left);left+=d[doc]
 ax.set_yticks([1,0],['Six original texts','Both U + all six apps']);ax.set_ylim(-.55,1.55);ax.set_xlim(0,max(p['source_sum'],p['whole_written'])*1.15)
 for y,z in [(1,p['source_sum']),(0,p['whole_written'])]:ax.text(z+p['whole_written']*.013,y,f'{z:,}',fontsize=9,va='center')
 maxcost=max(d['U_B'],d['U_B6'],*p['source_costs'].values(),*p['applications'].values())
 for y,doc in [(7,'U_B'),(6,'U_B6')]:bar(bx,'bar-acquire-'+doc,y,d[doc],COMMON);bx.text(d[doc]+maxcost*.018,y,f'{d[doc]:,}',va='center',fontsize=9)
 for j,k in enumerate(IDS):y=5-j;bar(bx,'bar-source-'+k,y+.20,p['source_costs'][k],SOURCE);bar(bx,'bar-application-'+k,y-.20,p['applications'][k],APP)
 bx.set_yticks(list(range(7,-1,-1)),['Whole prior U (16 pp.)','Whole supplement (10 pp.)']+[k+' / '+APPS[k]for k in IDS]);bx.set_ylim(-.65,7.65);bx.set_xlim(0,maxcost*1.15);bx.set_xlabel('Complete manuscript costs; software and external premises separate')
 for a in [ax,bx]:a.grid(axis='x',alpha=.2);a.set_axisbelow(True);a.spines[['right','top','left']].set_visible(False);a.tick_params(axis='y',length=0)
 fig.text(.04,.705,'Conditional applications assume both entire common papers and required premises.',fontsize=10)
 fig.text(.18,.040,'Originals',color=SOURCE,weight='bold');fig.text(.42,.040,'Whole common',color=COMMON,weight='bold');fig.text(.70,.040,'Applications',color='#347567',weight='bold')
 costs=finish(fig,bars,out,'costs')
 fig=plt.figure(figsize=(9,4.5));ax=fig.add_axes([.14,.20,.79,.61]);bars=[]
 for row in r['primary_acquisition']:
  i=row['stage']
  for name,z,offset,color in [('source',row['source_written'],-.19,SOURCE),('replacement',row['replacement_written'],.19,COMMON)]:
   if not z:continue
   q=ax.bar(i+offset,z,width=.32,color=color)[0];gid=f'bar-cumulative-{name}-{i}';q.set_gid(gid);bars.append((ax,gid,i+offset-.16,0,.32,z))
 ax.set_xlim(-.65,7.65);ax.set_ylim(0,max(p['source_sum'],p['whole_written'])*1.15);ax.set_xticks(range(8),['Old U']+list(APPS.values())[:-1]+['New U','B6']);ax.set_ylabel('Cumulative manuscript characters');ax.set_xlabel('Old U and five applications; new U before the sixth application');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.spines[['right','top']].set_visible(False)
 ax.annotate(f'+{d["U_B6"]:,} new common',xy=(6.19,r['primary_acquisition'][6]['replacement_written']),xytext=(4.9,163000),ha='center',fontsize=9,arrowprops={'arrowstyle':'->','color':COMMON})
 fig.text(.04,.94,'Complete acquisition in the declared order',fontsize=14,weight='bold');fig.text(.16,.047,'Originals acquired so far',color=SOURCE,weight='bold');fig.text(.58,.047,'Replacement acquired so far',color=COMMON,weight='bold')
 cumulative=finish(fig,bars,out,'cumulative')
 return dict(primary_coordinate=r['primary_coordinate'],costs=costs,cumulative=cumulative)
def tex(r):
 p=r['primary'];d=p['document_costs'];fmt=lambda x:f'{x:,}';rows=[]
 for k in IDS:rows.append(f'{k} & {APPS[k]} & {fmt(p["source_costs"][k])} & {fmt(p["applications"][k])} & {display(p["conditional"][k])}\\\\')
 groups=[];labels=['Required / auxiliary programs','Optional validation','Operational drivers','Partial formal files']
 for group,label in zip(GROUPS,labels):
  z=r['whole_file_groups'][group];groups.append(f'{label} & {z["files"]} & {fmt(z["metrics"]["NFC"][U[2]])} & {fmt(z["literal_bytes"])}\\\\')
 sensitivity=[]
 names=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed UTF-8 bytes']
 for n in N:
  for u,label in zip(U,names):
   values=[next(x for x in r['coordinates']if key(x)==(v,n,u))['written']for v in V]
   sensitivity.append(n+': '+label+' & '+' & '.join(display(z)for z in values)+r'\\')
 art=p['article_only_sensitivity'];sw=p['separate_software'];new=p['addition']
 text=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage{fontspec,unicode-math,amsmath,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}\setlength{\emergencystretch}{2em}
\hypersetup{hidelinks}
\title{Coset geometries and symmetric group markings}
\author{Six-original manuscript comparison}\date{}
\begin{document}\maketitle
The six complete original representations contain @SOURCE@ characters. Both complete common papers and all six applications contain @WRITTEN@. The fixed primary comparison is
\[
 R=\frac{\sum_{i=1}^6c(S_i)}{c(U_B)+c(U_{B6})+\sum_{i=1}^6c(B_i)}
 =\frac{@SOURCERAW@}{@UOLDRAW@+@UNEWRAW@+@APPSRAW@}
 =\mathbf{@FACTOR@}.
\]
\textbf{This is whole-topic expansion, not achieved whole-topic compression.}
The replacement is @EXTRA@ characters longer in this coordinate. The primary counts raw, untrimmed NFC characters excluding whitespace; it was fixed before calculation and retains the previous B convention. No metric or boundary was changed to obtain a preferred result.

The entire sixteen-page prior common paper and ten-page supplement are paid once each, with all thirty application pages. The two-page archived finite-neighbor precursor is already incorporated in the supplement and is not charged again. No old common passage is removed because it is no longer on a particular logical route.

The source side contains five full PDFs and N001's complete literal authored rendering. N001's original PDF remains unavailable, so this is not an all-PDF comparison. The L040 identification cover remains in the primary source. Titles, abstracts, whole tables, proofs, references and extractable figure labels stay counted.

\textbf{Conditional on prior acquisition.} Each factor below is $c(S_i)/c(B_i)$ after acquiring \emph{both whole common papers and the complete required topic premises}. These are complete local applications; no sibling application is silently assumed.
\begin{center}\begin{tabular}{llrrr}\toprule
Original & App & Source & Application & Conditional\\\midrule
@PAIRS@
\bottomrule\end{tabular}\end{center}
All five earlier conditional fraction records are exactly unchanged in all thirty coordinates. L047 adds @L047@ source characters, @NEWU@ common characters and @B6@ application characters. The prior whole factor @OLDFACTOR@ and the current @FACTOR@ describe different complete editions; conditional savings do not cancel the added common cost.
\newpage
\begin{center}\includegraphics[width=\linewidth]{costs.pdf}\end{center}
The upper bars compare all six originals with both common papers and every application. The lower bars show the same whole common acquisition and each complete source/application pair. All 23 colored rectangles represent actual manuscript costs, not ratios or proof-node counts. Each axis starts at zero.

Executable software is excluded symmetrically from source and replacement manuscript costs. This includes required computations: their proof role is unchanged, although their implementation costs lie outside this scalar. Mathematical algorithm and proof prose remain counted. Unknown historical software prevents a software-inclusive factor.
\newpage
\begin{center}\includegraphics[width=\linewidth]{cumulative.pdf}\end{center}
Stage zero acquires the entire old common paper (@OLDU@ characters), followed by the five earlier complete source/application pairs. A separate stage then acquires the whole new supplement (@NEWU@ characters): this is the visible common-theory cost jump before B6. The final stage adds L047 and its complete application. Both common papers total @COMMON@ characters. These eight stages show an explicit acquisition order, with no optimality or predetermined sawtooth claim. The conditional table on page 1 assumes both common papers and all required topic premises have already been acquired.

\textbf{Whole-file inventory, separate from the manuscript factor.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Role & Files & NFC nonspace & Literal bytes\\\midrule
@GROUPS@
\bottomrule\end{tabular}\end{center}
The ten mathematical files comprise eight required or auxiliary premises and two optional validations. The latter are not required acquisition. The six added required files include \path{retained/finite_boundary/run.g}: it fixes the exact roster and is not merely a driver. The source names Magma and PrimitiveGroupSims; our required implementations use GAP.

The two complete seven-page code appendices cost @PRINTOLD@ and @PRINTNEW@ characters, @PRINTALL@ together. Their ten complete raw alternatives cost @RAWALL@ characters and @RAWBYTES@ literal bytes. Printed and raw are alternatives, never additive copies. Neither is used for an asymmetric software-inclusive factor. The five operational drivers and two Lean modules stay separate; fourteen inherited declarations remain partial evidence. Four archived independent-review tools are bound as provenance, not added proof premises. GAP algorithms and group catalogues retain unknown external costs.
\newpage
\textbf{Sensitivity of the complete written comparison.}
\begin{center}\small\begin{tabular}{lrrr}\toprule
Unit & Raw complete & Raw selected & Calibrated\\\midrule
@SENSITIVITY@
\bottomrule\end{tabular}\end{center}
The complete record contains thirty settings, with 210 main exact fractions: one whole-topic and six conditional comparisons per setting. Sixty additional fractions give the whole-topic and L040 conditional article-only sensitivities. Exact unreduced costs, reduced fractions and forty-two significant-digit decimal strings are provided. Six-place reader rounding uses exact decimal division.

\textbf{L040 article-only sensitivity.} Removing only its accepted identification-cover text changes the primary source total to @ARTICLE_SOURCE@, leaving every replacement cost unchanged. The whole factor is @ARTICLE_WHOLE@ and L040's conditional is @ARTICLE_CONDITIONAL@. The other five conditionals are unchanged. The primary continues to include the cover.

All 480 accepted main document cells (450 PDF and 30 literal-rendering cells), thirty article-only cells and 170 whole-file cells remain unchanged. There are fifteen measured PDFs over 134 physical pages, including the separate fourteen program pages, plus the literal N001 rendering. The new L047 source is twelve pages and its local application three. Raw selected and calibrated coordinates reuse the accepted exact furniture exclusions and occurrence-bound repairs; none is reevaluated here.

\textbf{Scientific scope.} The accepted corrected principal contracts and retained inputs remain the authority. L047's 58 dispositions are not 58 originals. Its 23 finer ancillary Table 3 reports remain outside the regenerated scope while their whole source text is charged. The source's Conjecture 1.1 was already resolved in L044; this comparison adds no question answer. Earlier source corrections and exclusions remain explicit in their source maps.

Full graphics and layout, unavailable external proofs, catalogue construction, historical software and complete formalization have unknown costs, not zero. These are manuscript comparisons for the declared principal outputs, not claims that every source passage or all software has been replaced. No source, proof, question or formal credit follows from a factor.

The numerical author is enumeration\_volume. The new input author is rewrite\_termination, with distinct root input review/adoption; enumeration\_review authored the new L047 science. Earlier B authorship and the numerical author's distinct review of the root finite-neighbor lemma are disclosed in the packet. This calculation reuses adopted inputs and earlier reader mechanics; it reruns no source extraction, mathematical census or Lean proof.
\end{document}
'''
 vals={'SOURCE':fmt(p['source_sum']),'WRITTEN':fmt(p['whole_written']),'SOURCERAW':str(p['source_sum']),'UOLDRAW':str(d['U_B']),'UNEWRAW':str(d['U_B6']),'APPSRAW':str(p['application_sum']),'FACTOR':display(p['written']),'EXTRA':fmt(p['whole_written']-p['source_sum']),'PAIRS':'\n'.join(rows),'L047':fmt(new['source']),'NEWU':fmt(new['common']),'B6':fmt(new['application']),'OLDFACTOR':display(p['prior_whole_written']),'COMMON':fmt(p['whole_common']),'OLDU':fmt(d['U_B']),'GROUPS':'\n'.join(groups),'PRINTOLD':fmt(d['CODE']),'PRINTNEW':fmt(d['CODE6']),'PRINTALL':fmt(sw['whole_printed_programs']),'RAWALL':fmt(sw['whole_raw_programs']),'RAWBYTES':fmt(sum(r['whole_file_groups'][g]['literal_bytes']for g in GROUPS[:2])),'SENSITIVITY':'\n'.join(sensitivity),'ARTICLE_SOURCE':fmt(art['source_sum']),'ARTICLE_WHOLE':display(art['written']),'ARTICLE_CONDITIONAL':display(art['L040_conditional'])}
 for k,v in vals.items():text=text.replace('@'+k+'@',v)
 assert '@'not in text
 return text
if __name__=='__main__':
 r=load(R/'results.json');(R/'plot_data.json').write_text(json.dumps(plots(r,R),indent=2)+'\n');(R/'reader.tex').write_text(tex(r))
