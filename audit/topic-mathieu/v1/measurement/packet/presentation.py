"""Complete manuscript comparisons and a coarse acquisition graph."""
import os,json
from calculate import UNITS,APP

COLORS={'source':'#647583','U':'#426b9a','A1':'#499383','CLASSES':'#7db3a5','ROWS':'#b0d0c5','CODE':'#b98249','programs':'#d1a573','required_raw_data':'#906b9d'}
def graph(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs']
 return dict(scope='Complete-document acquisition and required-input relationships, not a fine theorem DAG or an attempt at a minimal proof.',unit='raw untrimmed NFC characters without whitespace',
 nodes=[dict(id='L073',title=r['source_title'],role='original',pages=9,cost=c['L073']),dict(id='U',title='Finite coset recognition',role='whole_common',pages=2,cost=c['U']),
 dict(id='application',title='Corrected complete Mathieu census and all tables',role='whole_application',pages=24,cost=sum(c[k]for k in APP),components=[dict(id=k,pages=n,cost=c[k])for k,n in zip(APP,[5,10,9])]),
 dict(id='programs',title='All seven required mathematical programs',role='required_computational_inputs',printed_pages=11,printed_cost=c['CODE'],raw_alternative_cost=raw['programs'],program_bytes=34695),
 dict(id='data',title='Both complete historical JSON inputs',role='mandatory_data_in_both_routes',cost=raw['required_raw_data'],literal_bytes=83965),
 dict(id='retained',title='Classical identifications, complete catalogues, algorithms and predecessor notation',role='retained_input',cost=None)],
 edges=[dict(source='U',target='application',kind='required_input',evidence='Modular application invokes finite coset recognition; all three local documents are charged.'),dict(source='programs',target='application',kind='required_input',evidence='All seven programs establish exhaustion, witnesses, completion models and literal-row reconciliation.'),dict(source='data',target='programs',kind='required_input',evidence='Both complete JSON files are mandatory notation and literal-comparison inputs; no thinning.'),dict(source='retained',target='U',kind='retained_input',evidence='Classical finite-group and incidence inputs are retained.'),dict(source='retained',target='programs',kind='retained_input',evidence='Complete TomLib data, named-group identification, exact algorithms and historical notation are retained.'),dict(source='L073',target='application',kind='source_correspondence',evidence='Fourteen dispositions and all431 literal rows; source-length comparison, not an additional proof-use assertion.')],
 accounting='A1, CLASSES and ROWS are all application companions. Program representations are alternatives, both with complete JSON. Costs of outside premises remain null. This graph is not used to prune documents or compute node-count ratios.')

def figures(r,out):
 os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Patch
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.hashsalt':'L073-complete-census'})
 p=r['primary'];c=p['costs'];raw=p['raw_costs'];fig,axs=plt.subplots(1,3,figsize=(11.4,4.5));fig.subplots_adjust(left=.075,right=.98,top=.86,bottom=.30,wspace=.42)
 defs=[('written',axs[0],[('Source',[('source',c['L073'])]),('Replacement',[(k,c[k])for k in ['U']+APP])],50000),('computational',axs[1],[('Printed code',[(k,c[k])for k in ['U']+APP+['CODE']]+[('required_raw_data',raw['required_raw_data'])]),('Raw code',[(k,c[k])for k in ['U']+APP]+[('programs',raw['programs']),('required_raw_data',raw['required_raw_data'])])],145000),('conditional',axs[2],[('Source',[('source',c['L073'])]),('Local papers',[(k,c[k])for k in APP])],50000)]
 specs=[]
 for panel,ax,bars,limit in defs:
  for x,(name,parts)in enumerate(bars):
   base=0
   for key,value in parts:
    gid=f'cost-{panel}-{x}-{key}';bar=ax.bar(x,value,bottom=base,color=COLORS[key])[0];bar.set_gid(gid);specs.append(dict(id=gid,panel=panel,value=value,bottom=base,x=x));base+=value
   ax.text(x,base+limit*.022,f'{base:,}',ha='center',fontsize=12)
  ax.set_xticks([0,1],[x[0]for x in bars]);ax.set_ylim(0,limit);ax.tick_params(axis='x',labelsize=11);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
 axs[0].set_title('Whole written topic');axs[0].set_ylabel('NFC nonspace characters');axs[1].set_title('Code + mandatory data');axs[2].set_title('Conditional application')
 labels={'source':'Original','U':'Whole common','A1':'Main application','CLASSES':'All class tables','ROWS':'All source-row tables','CODE':'Printed programs','programs':'Raw programs (alternative)','required_raw_data':'Both complete JSON inputs'}
 fig.legend(handles=[Patch(facecolor=COLORS[k],label=v)for k,v in labels.items()],loc='lower center',bbox_to_anchor=(.5,.045),ncol=4,fontsize=11,frameon=False)
 fig.text(.5,.012,'Conditional comparison prepays whole common paper, all seven programs, both JSON inputs and retained premises.',ha='center',fontsize=11)
 fig.savefig(out/'costs.svg',metadata={'Date':None});fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)
 (out/'plot_data.json').write_text(json.dumps(dict(bars=specs,bar_count=len(specs),program_representations_alternative=True),indent=2)+'\n')
 g=graph(r);(out/'document_graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
 fig,ax=plt.subplots(figsize=(11.4,3.9));ax.set_xlim(0,12);ax.set_ylim(0,5.2);ax.axis('off')
 xy={'L073':(1.9,4.2),'U':(6,4.2),'retained':(10.1,4.2),'data':(1.9,1.4),'programs':(6,1.4),'application':(10.1,1.4)}
 labels={'L073':f"Original L073\n9 pages · {c['L073']:,}",'U':f"Whole common paper\n2 pages · {c['U']:,}",'retained':'Retained proofs / catalogues\nFull costs unknown','data':f"Both complete JSON inputs\n{raw['required_raw_data']:,} characters\n83,965 literal bytes",'programs':f"Seven complete programs\n{c['CODE']:,} printed / {raw['programs']:,} raw",'application':f"Application + all companions\n5 + 10 + 9 pages · {sum(c[k]for k in APP):,}\nMain / class tables / source rows"}
 boxes={}
 for key,(x,y)in xy.items():
  boxes[key]=FancyBboxPatch((x-1.8,y-.6),3.6,1.2,boxstyle='round,pad=.025',facecolor='#edf5f1'if key=='application'else'#f2f4f6',edgecolor='#77848c',lw=.8,zorder=2);ax.add_patch(boxes[key]);ax.text(x,y,labels[key],ha='center',va='center',fontsize=13,zorder=3)
 for e in g['edges']:
  k=(e['source'],e['target']);rad=0 if k==('L073','application')else .10 if k==('retained','programs')else 0
  a=FancyArrowPatch(xy[k[0]],xy[k[1]],patchA=boxes[k[0]],patchB=boxes[k[1]],connectionstyle=f'arc3,rad={rad}',arrowstyle='-|>',mutation_scale=11,lw=1.1,linestyle='--'if e['kind']=='source_correspondence'else'-',color='#667984',shrinkA=4,shrinkB=4,zorder=1);a.set_gid('edge-'+k[0]+'-'+k[1]);ax.add_patch(a)
 ax.text(6,.14,'Solid: required input → use.  Dashed: source correspondence.  All documents and inputs stay charged.',ha='center',fontsize=11)
 fig.tight_layout(pad=.3);fig.savefig(out/'document_graph.svg',metadata={'Date':None});fig.savefig(out/'document_graph.pdf',metadata={'CreationDate':None,'ModDate':None});plt.close(fig)

def reader(r):
 p=r['primary'];c=p['costs'];raw=p['raw_costs'];t=p['totals'];f=p['comparisons']
 tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Complete Mathieu geometry census:\\manuscript and computational costs}
\author{Human Compression project}\date{}
\begin{document}\maketitle
The original is Leemans--Rowley, \emph{Rank three residually connected
geometries for $M_{22}$, revisited}, Electronic Journal of Combinatorics
17 (2010), N4 (register L073). All nine pages are counted. The accepted
replacement gives the corrected complete 81 rank-two and 431 rank-three
classes, with all 431 literal source-row dispositions. It does not recover
the unavailable historical \texttt{geo[]} identities. The 48-page
Kılıç--Rowley predecessor supplies retained notation; it is not a second
newly recovered original.

\paragraph{The complete written comparison.}
For complete raw extraction in NFC, counting characters without whitespace,
\[
 R_{\rm written}=\frac{@S@}{@U@+(@A@+@C@+@R@)}
 =\frac{@S@}{@W@}=@RW@.
\]
The replacement is longer in this coordinate. All companion papers are
part of the application: the ten-page class tables and nine-page source-row
tables are not free outputs. The whole common paper is paid once. No earlier
umbrella or another application is used without payment.
\begin{center}\begin{tabular}{lrr}\toprule
Complete document&Pages&Characters\\\midrule
Original L073&9&@S@\\
Common theory $U$&2&@U@\\
Main application&5&@A@\\
All class tables&10&@C@\\
All source-row dispositions&9&@R@\\
Complete seven-program appendix&11&@CODE@\\\bottomrule
\end{tabular}\end{center}
\paragraph{Required computation and the conditional comparison.}
Both computational routes pay the two complete JSON inputs: @DATA@
characters, or 83,965 literal file bytes. With the whole printed program
appendix the separate comparison is
$@S@/(@W@+@CODE@+@DATA@)=@RP@$.
Using the seven whole raw programs instead gives
$@S@/(@W@+@RAW@+@DATA@)=@RR@$.
The program representations are alternatives; the JSON is required in both.
There is no complete printed-data substitute or pruning of historical rows.

After acquiring \emph{the whole common paper, all seven programs, both
full JSON inputs and all retained premises}, the local application costs
@APP@ characters across all 24 pages:
\[
 r\mid(U,\mathrm{programs},\mathrm{data})=@S@/@APP@=@RC@.
\]
This conditional comparison also shows an expansion; it is not a standalone
whole-topic saving. The seven programs are required mathematical inputs,
not merely sample diagnostics. The three auxiliary scripts and ten generated
outputs remain inventoried separately, and no Lean formalization is claimed.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
\vspace{-4mm}
\begin{center}\includegraphics[width=\textwidth]{document_graph.pdf}\end{center}
\vspace{-4mm}
The graph describes complete-document acquisition, not a minimal theorem
DAG. All application companions remain in every written denominator. The
three auxiliary scripts contain 20,542 literal bytes (@DRIVERS@ nonspace
characters); the ten generated outputs contain 1,567,120 bytes (@OUTPUTS@
characters). Some outputs feed later pipeline stages; they are not charged
a second time as independent external inputs. Their separate costs remain
available without discount.

\paragraph{Unit and encoding sensitivities.}
Complete raw NFC coordinates are:
\begin{center}\small\begin{tabular}{lrrrr}\toprule
Unit&Written&Printed$+$data&Raw$+$data&Conditional\\\midrule
@METRICS@
\bottomrule\end{tabular}\end{center}
All thirty coordinates and 120 exact fractions are retained in JSON/CSV:
five units, NFC and NFKC, for untrimmed, furniture-selected and calibrated
selected text. Selection only removes exact folios and the repeated journal
footer. Six observed script/Fraktur classes account for 472 calibrated
occurrences; raw text is not silently repaired. Normalized text-byte units
are distinct from literal stored-file bytes.

\paragraph{Retained costs and scope.}
Named Mathieu-group identification, complete TomLib catalogue data, exact
GAP/Design/GRAPE algorithms, classical design/Golay facts and predecessor
notation remain explicit premises. Their full proof and catalogue-construction
costs, complete graphic complexity and full formalization cost are unknown,
not zero. The figures are representation lengths, not minimum proof complexity
or research effort. Scientific and input acceptances are reused; this new
arithmetic/reader awaits distinct review and assigns no source, question or
formal credit.
\end{document}
'''
 vals={'S':c['L073'],'U':c['U'],'A':c['A1'],'C':c['CLASSES'],'R':c['ROWS'],'W':t['written'],'CODE':c['CODE'],'DATA':raw['required_raw_data'],'RAW':raw['programs'],'APP':t['applications'],'DRIVERS':raw['drivers'],'OUTPUTS':raw['generated_outputs']}
 for k,n in [('RW','written'),('RP','including_printed_programs_and_data'),('RR','including_raw_programs_and_data'),('RC','conditional_application')]:vals[k]=f"{float(f[n]['decimal']):.6f}"
 labels=['Whitespace tokens','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed-space UTF-8 bytes'];lines=[]
 for unit,label in zip(UNITS,labels):
  row=next(x for x in r['coordinates']if x['variant']=='raw_untrimmed'and x['normalization']=='NFC'and x['unit']==unit)
  lines.append(label+' & '+' & '.join(f"{float(v['decimal']):.3f}"for v in row['comparisons'].values())+r' \\')
 vals['METRICS']='\n'.join(lines)
 for key,value in vals.items():tex=tex.replace('@'+key+'@',str(value))
 return tex
