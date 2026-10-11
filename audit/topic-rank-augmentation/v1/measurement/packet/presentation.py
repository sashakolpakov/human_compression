"""Complete L020 document costs; coarse proof and acquisition relationships."""
import os,json
from calculate import UNITS,APP
COLORS={'source':'#647583','U':'#426b9a','A1':'#499383','COUNTER':'#9ccbbf','CODE':'#b98249','programs':'#d1a573'}
def graph(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs']
 return dict(scope='Complete-document boundary, not a fine theorem DAG or minimum proof claim.',unit='raw untrimmed NFC nonspace characters',nodes=[
 dict(id='L020',title=r['source_title'],pages=19,cost=c['L020'],role='original'),
 dict(id='U',title='Rank augmentation from a supported transposition',pages=5,cost=c['U'],role='whole_common'),
 dict(id='A1',title='Splitting a middle generator in the symmetric group',pages=3,cost=c['A1'],role='application'),
 dict(id='COUNTER',title='A counterexample to the six-point case of rank augmentation',pages=3,cost=c['COUNTER'],role='required_local_written_proof'),
 dict(id='CODE',title='Programs for rank augmentation and its obstruction',printed_pages=3,printed_cost=c['CODE'],raw_alternative_cost=raw['programs'],roles=r['boundary']['program_roles']),
 dict(id='retained',title='McMullen–Schulte end criterion, via source Proposition5.1',cost=None,role='retained_external_proof')],edges=[
 dict(source='U',target='A1',kind='proof_use',evidence='Application Section1 uses both-end, block/parity and exact six-point criterion.'),
 dict(source='COUNTER',target='A1',kind='proof_use',evidence='Application Section2 explicitly requires the entire old-C and generation proof of the eighteen-point obstruction.'),
 dict(source='retained',target='U',kind='retained_input',evidence='Common Section1 and end-group conclusions use the classical end criterion.'),
 dict(source='retained',target='COUNTER',kind='retained_input',evidence='Counterproof Section1 retains the rank-three end criterion.'),
 dict(source='CODE',target='A1',kind='required_finite_certificate',evidence='Whole check_examples.g verifies all three literal Section6 examples; application Section3.'),
 dict(source='CODE',target='U',kind='validation_only',evidence='Whole check_models.g is bounded validation, not a uniform premise.'),
 dict(source='CODE',target='COUNTER',kind='validation_only',evidence='Whole check_case.py supplies a transparent certificate supporting an already complete written proof.'),
 dict(source='L020',target='A1',kind='source_correspondence',evidence='Nineteen accepted source dispositions; not an extra proof premise.')],accounting='All eleven written pages paid. Counterproof is local application cost, not a free old correction. Whole code representation is charged separately; no closure or node-count ratio.')

def figures(r,out):
 os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Patch
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.hashsalt':'L020-rank-augmentation'})
 p=r['primary'];c=p['costs'];raw=p['raw_costs'];fig,axs=plt.subplots(1,3,figsize=(11.4,4.5));fig.subplots_adjust(left=.075,right=.98,top=.86,bottom=.30,wspace=.42)
 defs=[('written',axs[0],[('Source',[('source',c['L020'])]),('Replacement',[(k,c[k])for k in ['U']+APP])],40000),('computational',axs[1],[('Printed code',[(k,c[k])for k in ['U']+APP+['CODE']]),('Raw code',[(k,c[k])for k in ['U']+APP]+[('programs',raw['programs'])])],45000),('conditional',axs[2],[('Source',[('source',c['L020'])]),('Local papers',[(k,c[k])for k in APP])],40000)]
 specs=[]
 for panel,ax,bars,limit in defs:
  for x,(name,parts)in enumerate(bars):
   base=0
   for key,value in parts:
    gid=f'cost-{panel}-{x}-{key}';bar=ax.bar(x,value,bottom=base,color=COLORS[key])[0];bar.set_gid(gid);specs.append(dict(id=gid,panel=panel,value=value,bottom=base,x=x));base+=value
   ax.text(x,base+limit*.022,f'{base:,}',ha='center',fontsize=12)
  ax.set_xticks([0,1],[x[0]for x in bars]);ax.set_ylim(0,limit);ax.tick_params(axis='x',labelsize=11);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 axs[0].set_title('Whole written topic');axs[0].set_ylabel('NFC nonspace characters');axs[1].set_title('Whole program alternatives');axs[2].set_title('Conditional application')
 labels={'source':'Original','U':'Whole common','A1':'Application','COUNTER':'Required counterproof','CODE':'Printed programs','programs':'Raw programs (alternative)'}
 fig.legend(handles=[Patch(facecolor=COLORS[k],label=v)for k,v in labels.items()],loc='lower center',bbox_to_anchor=(.5,.045),ncol=3,fontsize=11,frameon=False)
 fig.text(.5,.012,'Conditional comparison prepays whole common paper, all three declared programs and retained premises.',ha='center',fontsize=11)
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 (out/'plot_data.json').write_text(json.dumps(dict(bars=specs,bar_count=len(specs),program_representations_alternative=True),indent=2)+'\n')
 g=graph(r);(out/'document_graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
 fig,ax=plt.subplots(figsize=(11.4,3.9));ax.set_xlim(0,12);ax.set_ylim(-.7,5.2);ax.axis('off')
 xy={'L020':(10.1,4.2),'U':(6,4.2),'retained':(1.9,4.2),'COUNTER':(1.9,1.4),'A1':(6,1.4),'CODE':(10.1,1.4)}
 labels={'L020':f"Original L020\n19 pages · {c['L020']:,}",'U':f"Whole common paper\n5 pages · {c['U']:,}",'retained':'Classical end criterion\nFull proof cost unknown','COUNTER':f"Required counterproof\n3 pages · {c['COUNTER']:,}",'A1':f"Complete source application\n3 pages · {c['A1']:,}",'CODE':f"All three complete programs\n{c['CODE']:,} printed / {raw['programs']:,} raw"}
 boxes={}
 for key,(x,y)in xy.items():
  boxes[key]=FancyBboxPatch((x-1.8,y-.6),3.6,1.2,boxstyle='round,pad=.025',facecolor='#edf5f1'if key in ['A1','COUNTER']else'#f2f4f6',edgecolor='#77848c',lw=.8,zorder=2);ax.add_patch(boxes[key]);ax.text(x,y,labels[key],ha='center',va='center',fontsize=12,zorder=3)
 for e in g['edges']:
  k=(e['source'],e['target']);rad=.18 if k==('CODE','U')else -.22 if k==('CODE','COUNTER')else 0
  logical=e['kind']in ['proof_use','retained_input','required_finite_certificate']
  a=FancyArrowPatch(xy[k[0]],xy[k[1]],patchA=boxes[k[0]],patchB=boxes[k[1]],connectionstyle=f'arc3,rad={rad}',arrowstyle='-|>',mutation_scale=11,lw=1.1,linestyle='-'if logical else(0,(6,4)),color='#435561'if logical else'#8a969d',shrinkA=4,shrinkB=4,zorder=1);a.set_gid('edge-'+k[0]+'-'+k[1]);ax.add_patch(a)
 ax.text(6,-.4,'Solid: proof / finite input → use.  Dashed: source correspondence or validation.',ha='center',fontsize=11)
 fig.tight_layout(pad=.3);fig.savefig(out/'document_graph.svg',metadata={'Date':None});fig.savefig(out/'document_graph.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)

def reader(r):
 p=r['primary'];c=p['costs'];raw=p['raw_costs'];t=p['totals'];f=p['comparisons']
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Rank augmentation:\\complete manuscript and program costs}
\author{Human Compression project}\date{}
\begin{document}\maketitle
The original is De Saedeleer--Leemans--Mulpas, \emph{A rank augmentation
theorem for rank 3 string C-group representations of the symmetric groups},
arXiv:2212.12563v1, 23 December 2022 (L020). All nineteen pages are counted,
including the banner, introductory table, diagrams, references and addresses.
The nineteen accepted dispositions preserve the valid first two cases of
Theorem~4.1 and replace its false third case by an exact criterion and a
complete eighteen-point counterexample. The original retains its literal
claims in every measured representation. This is one original, not two.

\paragraph{The complete written comparison.}
For raw, untrimmed extraction in NFC, counting characters without whitespace,
\[
R_{\rm written}=\frac{@S@}{@U@+(@A@+@C@)}
=\frac{@S@}{@W@}=@RW@.
\]
The whole five-page common paper and both three-page local papers are paid.
The counterproof is a required application dependency; citing an earlier
correction does not make it free. No old Topic B common theory or cross-topic
saving is assumed. Titles, references and repeated exposition remain charged.
\begin{center}\begin{tabular}{lrr}\toprule
Complete document&Pages&Characters\\\midrule
Original L020&19&@S@\\
Common supported-transposition proof&5&@U@\\
Source application&3&@A@\\
Required counterexample proof&3&@C@\\
All three programs, printed&3&@CODE@\\\bottomrule
\end{tabular}\end{center}
\paragraph{Complete programs and the conditional application.}
Including the whole program appendix gives the separate comparison
$@S@/(@W@+@CODE@)=@RP@$.
The three whole raw programs cost @RAW@ characters and give
$@S@/(@W@+@RAW@)=@RR@$. Printed and raw programs are alternatives;
the old two-page appendix is replaced, not added.
The program-inclusive denominators exceed the source length in this coordinate.

After acquiring \emph{the entire common paper, all three declared programs
and all retained premises}, the complete six-page local application costs
@APP@ characters:
\[
r\mid(U,\mathrm{programs})=@S@/(@A@+@C@)=@RC@.
\]
This is a conditional acquisition comparison, not the whole-topic factor.
The source-example program supplies finite certificates; the model program
is bounded validation; the eighteen-point certificate supports the complete
written counterproof. No bounded test replaces a uniform proof.

\paragraph{Separate and unknown costs.}
Three drivers cost @DRIVERS@ nonspace characters (15,947 literal bytes).
Two whole Lean files cost @LEAN@ characters (6,855 bytes), with two generic
and thirteen literal-obstruction declarations, not a full source formalization.
The motivating Table~1 census and classical end criterion remain retained;
full outside-proof, runtime, historical-software, graphic and formalization
costs are unknown, not zero. These are complete-text representation lengths,
not minimum proof complexity or research effort. No new scientific credit is
assigned by this numerical packet.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
\vspace{-4mm}
\begin{center}\includegraphics[width=\textwidth]{document_graph.pdf}\end{center}
\vspace{-4mm}
The graph distinguishes proof dependencies from source correspondence and
validation. It does not remove any document from the cost. In particular,
the counterproof stays in the local application and the common paper is
charged once. Whole-document acquisition sums and every raw file are also
available in JSON/CSV; no node-count factor is used.

\paragraph{Unit and encoding sensitivities.}
Raw, untrimmed NFC coordinates are:
\begin{center}\small\begin{tabular}{lrrrr}\toprule
Unit&Written&Printed&Raw&Conditional\\\midrule
@METRICS@
\bottomrule\end{tabular}\end{center}
All thirty coordinates and 120 exact fractions are retained: five units,
NFC and NFKC, with untrimmed, furniture-selected and calibrated-selected
text. Selection removes only exact repeated headers and isolated page
numbers. Two actual font/byte classes account for 112 observed substitutions:
111 calligraphic G symbols and one blackboard-bold N. The raw coordinates
are unchanged. The arXiv banner remains included; printed hyphens remain
literal. Full diagram topology, colour, curvature and layout are not
reconstructed from extracted labels, so graphic complexity stays unknown.
Normalized text-byte units differ from literal stored-file bytes.

\paragraph{Review boundary.}
Scientific acceptance and the distinct input review are reused. The numerical
author previously reviewed those inputs but did not author them; this new
arithmetic and reader require a distinct numerical review. The source's
larger-orbit and higher-rank questions remain unresolved. No source, question
or formal credit is added here.
\end{document}
'''
 vals={'S':c['L020'],'U':c['U'],'A':c['A1'],'C':c['COUNTER'],'W':t['written'],'APP':t['applications'],'CODE':c['CODE'],'RAW':raw['programs'],'DRIVERS':raw['operational_drivers'],'LEAN':raw['formal_files']}
 for k,n in [('RW','written'),('RP','including_printed_programs'),('RR','including_raw_programs'),('RC','conditional_application')]:vals[k]=f"{float(f[n]['decimal']):.6f}"
 labels=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed-space UTF-8 bytes'];lines=[]
 for unit,label in zip(UNITS,labels):
  row=next(x for x in r['coordinates']if x['variant']=='raw_untrimmed'and x['normalization']=='NFC'and x['unit']==unit)
  lines.append(label+' & '+' & '.join(f"{float(v['decimal']):.3f}"for v in row['comparisons'].values())+r' \\')
 vals['METRICS']='\n'.join(lines)
 for key,value in vals.items():tex=tex.replace('@'+key+'@',str(value))
 return tex
