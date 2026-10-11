"""Readable whole-document bars and document dependencies; no theorem-node ratio."""
import os, json
from pathlib import Path
from calculate import UNITS

def graph(result):
    c=result['primary']['costs'];raw=result['primary']['raw_costs']
    return dict(scope='Complete-document acquisition and scientific dependence; not a fine theorem DAG.',
        cost_unit='calibrated selected NFC characters without whitespace',
        nodes=[dict(id='L010',title='Two gluing methods for string C-group representations of the symmetric groups',short='Original L010',cost=c['L010'],pages=15,role='source'),
               dict(id='U1',title='Gluing permutation markings through a common point',short='Common point theorem',cost=c['U1'],pages=5,role='common'),
               dict(id='U2',title='Two copies of a tree and their permutation intersections',short='Synchronized trees',cost=c['U2'],pages=6,role='common'),
               dict(id='A1',title='Gluing symmetric-group markings and detecting a failed intersection',short='Complete application',cost=c['A1'],pages=5,role='application'),
               dict(id='CODE',title='Complete diagnostic programs for gluing',short='Three complete diagnostics',cost=c['CODE'],raw_alternative_cost=raw['programs'],pages=4,role='validation_only'),
               dict(id='external',title='Endpoint sesquiextension and end-parabolic criterion',short='Retained classical inputs',cost=None,role='retained_input')],
        edges=[dict(source='U1',target='U2',kind='proof_use',locator='U2 Theorem5 and Section6 use pure-leaf extension from U1.'),
               dict(source='U1',target='A1',kind='proof_use',locator='A1 Section1 and the pure-tail steps.'),
               dict(source='U2',target='A1',kind='proof_use',locator='A1 Sections1,3,4 use the tree/paired-row formulas.'),
               dict(source='external',target='A1',kind='retained_proof_use',locator='A1 Section1 and Lemmas1–2; source Propositions2.2–2.3.'),
               dict(source='L010',target='A1',kind='source_correspondence',locator='Twenty-three accepted source dispositions; this arrow is not a proof premise.'),
               dict(source='CODE',target='U1',kind='validation_only',locator='Complete check_gluing.g, not a uniform premise.'),
               dict(source='CODE',target='U2',kind='validation_only',locator='Complete check_parallel.g, not a uniform premise.'),
               dict(source='CODE',target='A1',kind='validation_only',locator='Complete check_applications.g, not a uniform premise.')],
        accounting='The whole U1 and U2 are each charged once even though U1 is also used by U2. References, wrappers and repeated text are not removed. Whole code is separately charged, with its raw form an alternative. No sum of closure costs or node-count factor is used.')

def figures(result,out):
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'complete-gluing-topic'})
    p=result['primary'];c=p['costs'];r=p['raw_costs']
    fig,axs=plt.subplots(1,2,figsize=(10.2,3.45),layout='constrained')
    a=axs[0];a.bar(0,c['L010'],color='#687785')[0].set_gid('cost-source-L010');bottom=0
    for k,color,label in [('U1','#426b9a','Whole common point paper'),('U2','#7c8eb4','Whole tree paper'),('A1','#70a59a','Complete application')]:
        a.bar(1,c[k],bottom=bottom,color=color,label=label)[0].set_gid('cost-written-'+k);bottom+=c[k]
    a.set_xticks([0,1],['Complete source','All written papers']);a.set_ylim(0,46000);a.set_ylabel('NFC nonspace characters')
    a.text(0,c['L010']+700,f"{c['L010']:,}",ha='center');a.text(1,bottom+700,f'{bottom:,}',ha='center')
    a.set_title('Whole written comparison');a.legend(loc='upper center',bbox_to_anchor=(.5,-.13),fontsize=8,frameon=False)
    a=axs[1];values=[c['U1'],c['U2'],c['A1'],c['CODE'],r['programs']]
    bars=a.bar(range(5),values,color=['#426b9a','#7c8eb4','#70a59a','#bd874e','#d4b38f'])
    for bar,key in zip(bars,['U1','U2','A1','CODE','raw-programs']):bar.set_gid('cost-component-'+key)
    a.set_xticks(range(5),['Common\npoint','Tree\npaper','Application','Printed\nprograms','Raw\nprograms']);a.tick_params(axis='x',labelsize=8);a.set_ylim(0,19500)
    for bar,v in zip(bars,values):a.text(bar.get_x()+bar.get_width()/2,v+350,f'{v:,}',ha='center',fontsize=8)
    a.set_title('Complete components');a.text(.5,-.25,'Printed and raw programs are alternatives.',transform=a.transAxes,ha='center',fontsize=9)
    for a in axs:a.spines[['right','top']].set_visible(False);a.grid(axis='y',alpha=.2);a.set_axisbelow(True)
    fig.savefig(out/'costs.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(out/'costs.svg',metadata={'Date':None});plt.close(fig)
    g=graph(result);(out/'document_graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
    fig,a=plt.subplots(figsize=(10.3,3.7));a.set_xlim(0,11);a.set_ylim(0,5.2);a.axis('off')
    xy={'L010':(1.45,4.15),'U1':(4.8,4.15),'U2':(8.4,4.15),'external':(1.45,1.15),'A1':(5.35,1.15),'CODE':(9,1.15)}
    labels={'L010':f"Original L010\n15 pages · {c['L010']:,}",'U1':f"Common point theorem\n5 pages · {c['U1']:,}",'U2':f"Synchronized trees\n6 pages · {c['U2']:,}",'A1':f"Complete application\n5 pages · {c['A1']:,}",'CODE':f"Three full diagnostics\n{c['CODE']:,} printed / {r['programs']:,} raw",'external':'Retained classical inputs\nFull proof cost unknown'}
    boxes={}
    for k,(x,y) in xy.items():
        color='#eef3f8' if k in ('U1','U2') else '#edf5f1' if k=='A1' else '#fbf2e7' if k=='CODE' else '#f2f2f2'
        boxes[k]=FancyBboxPatch((x-1.35,y-.5),2.7,1,boxstyle='round,pad=.035',facecolor=color,edgecolor='#6f7c85',lw=.8,zorder=2)
        a.add_patch(boxes[k]);a.text(x,y,labels[k],ha='center',va='center',fontsize=9,zorder=3)
    for e in g['edges']:
        s,t=xy[e['source']],xy[e['target']];logical=e['kind'] in ('proof_use','retained_proof_use')
        # Curved validation routes run outside the two common-paper boxes.
        rad=.1 if e['source']=='CODE' and e['target']=='U1' else 0
        arrow=FancyArrowPatch(s,t,patchA=boxes[e['source']],patchB=boxes[e['target']],arrowstyle='-|>',mutation_scale=12,shrinkA=4,shrinkB=4,connectionstyle=f'arc3,rad={rad}',lw=1.2,color='#435561' if logical else '#8a969d',linestyle='-' if logical else '--',zorder=1)
        arrow.set_gid('edge-'+e['source']+'-'+e['target']);a.add_patch(arrow)
    a.text(5.5,.08,'Solid arrows: prerequisite → use.  Dashed: source correspondence or validation.',ha='center',fontsize=9,zorder=4)
    fig.tight_layout(pad=.3);fig.savefig(out/'document_graph.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(out/'document_graph.svg',metadata={'Date':None});plt.close(fig)

def reader(r):
    p=r['primary'];c=p['costs'];raw=p['raw_costs'];cmp=p['comparisons'];t=p['totals']
    tex=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Gluing through a common point and along trees:\\complete manuscript costs}
\author{Human Compression project}\date{}
\begin{document}\maketitle
The original is Leemans--Mulpas, \emph{Two gluing methods for string C-group
representations of the symmetric groups}, arXiv:2504.17535v1, 24 April 2025
(register L010). All fifteen pages are counted, including references,
addresses and the identification banner. We compare them with both complete
common papers and the full application. The 23 source records describe one
original; the historical numerical sequence and unused preliminaries are
not claimed newly recovered.

\paragraph{The complete written comparison.}
For calibrated selected NFC characters without whitespace, the comparison is
\[
R_{\mathrm{written}}=\frac{@S@}{@U1@+@U2@+@A@}
=\frac{@S@}{@W@}=@RW@.
\]
The replacement written topic is longer in this coordinate. Both common
papers are charged once, with every proof, wrapper and reference passage.
The earlier Topic B umbrella is not used, and no overlap with another topic
is deducted.

\begin{center}\begin{tabular}{lrr}\toprule
Complete document&Pages&Characters\\\midrule
Original L010&15&@S@\\
Common point paper $U_1$&5&@U1@\\
Synchronized tree paper $U_2$&6&@U2@\\
Application $A$&5&@A@\\
Three diagnostic programs, printed&4&@CODE@\\\bottomrule
\end{tabular}\end{center}

\paragraph{Programs and the conditional application.}
The full four-page program appendix gives the separate comparison
$R_{\mathrm{printed}}=@S@/@WP@=@RP@$.
The three complete raw files cost @RAW@ characters and give
$R_{\mathrm{raw}}=@S@/@WR@=@RR@$. These are alternative representations;
the printed and raw program costs are never added together. All three
programs validate examples and failed weakenings; none is a premise of the
uniform written theorems.

After acquiring \emph{both entire common papers and all three complete
declared programs}, the matched application comparison is
\[
r\mid(U_1,U_2,V)=\frac{@S@}{@A@}=@RC@.
\]
This is a conditional acquisition cost, not the whole-topic factor. The
three operational drivers cost @DRIVERS@ characters separately; the two
Lean files cost @LEAN@ and contain ten scoped declarations. They do not
formalize the complete source or its constructions.

\paragraph{What remains unpriced.}
Full costs of the retained endpoint sesquiextension theorem and classical
end-parabolic criterion are unknown. Historical software, complete formalization,
and the source diagrams' lines, incidence, colour and layout also remain
unknown, not zero. These figures measure available complete texts, not
minimum proof complexity or research effort. No new scientific credit is
assigned by this numerical packet.
\newpage
\begin{center}\includegraphics[width=\textwidth]{costs.pdf}\end{center}
\vspace{-3mm}
\begin{center}\includegraphics[width=\textwidth]{document_graph.pdf}\end{center}
\vspace{-4mm}
The graph shows complete-document dependencies. Each common paper is paid
once even when another paper uses it. Dashed validation and source links
are not proof prerequisites. Retained external proof costs stay unknown.
There is no node-count ratio or repeated-rise-and-fall claim.

\paragraph{Sensitivity to the unit of length.}
For calibrated selected NFC text, the whole written, program-inclusive
and conditional coordinates are:
\begin{center}\small\begin{tabular}{lrrrr}\toprule
Unit&Written&Printed&Raw&Conditional\\\midrule
@METRICS@
\bottomrule\end{tabular}\end{center}
All thirty coordinates are retained in JSON/CSV: five units under NFC and
NFKC, for complete raw extraction, furniture-only selection and calibrated
selection. Only isolated folios and exact running headers are removed in
selected text. Six observed glyph classes produce 175 substitutions; the
short stile is a separate encoded component. The curved code-wrap glyph
retains its literal comma. The unembedded banner is literal ASCII; unchanged
Type0 replacement text has no independent outline-equivalence claim.
Full graphical complexity remains outside these text coordinates.
\end{document}
'''
    replacements={'S':c['L010'],'U1':c['U1'],'U2':c['U2'],'A':c['A1'],'W':t['written'],'CODE':c['CODE'],'RAW':raw['programs'],'WP':t['with_printed_programs'],'WR':t['with_raw_programs'],'DRIVERS':raw['drivers'],'LEAN':raw['formal']}
    for key,name in [('RW','written'),('RP','including_printed_programs'),('RR','including_raw_programs'),('RC','conditional_application')]:replacements[key]=f"{float(cmp[name]['decimal']):.6f}"
    labels=['Whitespace words','Alphanumeric units','Nonspace characters','Collapsed-space characters','Collapsed-space UTF-8 bytes'];metric=[]
    for unit,label in zip(UNITS,labels):
        row=next(x for x in r['coordinates'] if x['variant']=='calibrated_selected' and x['normalization']=='NFC' and x['unit']==unit)
        metric.append(label+' & '+' & '.join(f"{float(row['comparisons'][k]['decimal']):.3f}" for k in ('written','including_printed_programs','including_raw_programs','conditional_application'))+r' \\')
    replacements['METRICS']='\n'.join(metric)
    for key,value in replacements.items():tex=tex.replace('@'+key+'@',str(value))
    return tex
