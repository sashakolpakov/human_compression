#!/usr/bin/env python3
"""Build both complete mathematical dependency drawings and their cost explanation."""
import argparse,html,json,os,textwrap,tempfile,hashlib
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'affine-cost-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from accounting import add,need,sha
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
UNIT='characters_without_whitespace'
def primary(w):return w['calibrated_selected']['NFC'][UNIT]
def draw(g,w,side,out):
 nodes={n['id']:n for n in g['nodes']};keep={n for n,r in nodes.items() if r['side']==side}
 changed=True
 while changed:
  old=set(keep);keep|={e['source'] for e in g['edges'] if e['target'] in keep and e['kind'] in g['logical_edge_kinds']};changed=keep!=old
 edges=[e for e in g['edges'] if e['source'] in keep and e['target'] in keep and e['kind'] in g['logical_edge_kinds']]
 pred={n:set() for n in keep}
 for e in edges:pred[e['target']].add(e['source'])
 depth={}
 def level(n,path=()):
  need(n not in path,'DAG acyclic')
  if n not in depth:depth[n]=max([level(p,path+(n,))+1 for p in pred[n]]+ [0])
  return depth[n]
 for n in keep:level(n)
 cols={}
 for n in sorted(keep):cols.setdefault(depth[n],[]).append(n)
 # Stable barycentric ordering reduces crossings without changing a logical edge.
 for _ in range(3):
  ranks={n:i for ns in cols.values() for i,n in enumerate(ns)}
  for col,ns in sorted(cols.items()):ns.sort(key=lambda n:(sum(ranks[p] for p in pred[n])/len(pred[n]) if pred[n] else ranks[n],n))
 width=390;gap=150;bh=126;step=155;top=105;maxrows=max(map(len,cols.values()));height=top+maxrows*step+75
 positions={n:(35+d*(width+gap),top+i*step+(maxrows-len(ns))*step/2) for d,ns in cols.items() for i,n in enumerate(ns)}
 fullwidth=80+(max(depth.values())+1)*(width+gap)-gap
 title='Historical source proof routes' if side=='historical' else 'Complete current common theory and application'
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{fullwidth}" height="{height}" viewBox="0 0 {fullwidth} {height}">',
 '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#6d8090"/></marker></defs>',
 '<rect width="100%" height="100%" fill="#ffffff"/>',f'<text x="35" y="35" font-family="sans-serif" font-size="25" font-weight="bold">{title}</text>',
 '<text x="35" y="63" font-family="sans-serif" font-size="16">Prerequisite → use. Box costs share passage owners: unite owners before summing. External proofs are unknown.</text>',
 '<text x="35" y="86" font-family="sans-serif" font-size="15">Costs: calibrated NFC characters without whitespace. Full manuscripts, context and references remain paid separately.</text>']
 for i,e in enumerate(edges):
  x,y=positions[e['source']];xx,yy=positions[e['target']];a=x+width;b=y+bh/2;c=xx;d=yy+bh/2
  parts.append(f'<path id="edge-{i}" data-source="{html.escape(e["source"])}" data-target="{html.escape(e["target"])}" d="M{a},{b} C{a+gap*.52},{b} {c-gap*.52},{d} {c},{d}" fill="none" stroke="#6d8090" stroke-opacity=".55" stroke-width="1.5" marker-end="url(#arrow)"><title>{html.escape(e["kind"]+": "+e["source"]+" → "+e["target"])}</title></path>')
 for n in sorted(keep):
  row=nodes[n];x,y=positions[n];link=w['node_interfaces'][n];flags=row.get('documentary_flags',[]);unknown=link['known_weight'] is None
  fill='#fff1e9' if flags else '#f0f1f3' if unknown else '#e9f4ed' if row['document']=='CODE' else '#eaf2fb' if side=='new' else '#faf1db'
  cost='External proof: unknown' if unknown else f'Interface text: {primary(link["known_weight"]):,}'
  lines=textwrap.wrap(row['label'],43,break_long_words=False,break_on_hyphens=False);need(len(lines)<=4,'label fits '+n)
  parts.append(f'<g id="node-{html.escape(n)}" data-node="{html.escape(n)}"><title>{html.escape(n+": "+row["label"]+". "+" ".join(flags))}</title><rect x="{x}" y="{y}" width="{width}" height="{bh}" rx="7" fill="{fill}" stroke="#99a7b3"/><text x="{x+12}" y="{y+20}" font-family="sans-serif" font-size="14" font-weight="bold">{html.escape(n)}</text>')
  for j,line in enumerate(lines):parts.append(f'<text x="{x+12}" y="{y+42+j*17}" font-family="sans-serif" font-size="15">{html.escape(line)}</text>')
  parts.append(f'<text x="{x+12}" y="{y+113}" font-family="sans-serif" font-size="13" fill="#384b58">{html.escape(cost)}</text></g>')
 parts.append(f'<text x="35" y="{height-28}" font-family="sans-serif" font-size="16">Orange boxes retain source qualifications. Programs are green. Logical counts describe this drawing; they are not a compression measure.</text></svg>')
 (out/f'{side}_graph.svg').write_text('\n'.join(parts)+'\n')
 return {'side':side,'nodes':sorted(keep),'edges':[{'source':e['source'],'target':e['target'],'kind':e['kind']} for e in edges], 'omitted_nonlogical_kinds':g['nonlogical_edge_kinds'],'expanded_external_proof_cost':None,'coordinates':{n:list(positions[n]) for n in sorted(keep)},'font_size_px':15,'box_size_px':[width,bh],'node_count_factor':None}

def build(root,out):
 p=load(HERE/'partition.json');w=load(HERE/'weights.json');g=load(root/'topic_Affine_logical_dag_v2/logical_graph.json');m=w['unchanged_complete_document_measurement']
 graphs={s:draw(g,w,s,out) for s in ['historical','new']}
 (out/'graphs.json').write_text(json.dumps(graphs,indent=2)+'\n')
 stages=[];paid=set()
 for key in ['U_Affine','CODE','AF1']:
  now={o for o,r in p['owners'].items() if r['document']==key};need(not now&paid,'disjoint documents');paid|=now
  stages.append({'stage':key,'complete_owner_ids':sorted(now),'new_cost':add(w['owner_costs'][n] for n in now),'cumulative_owner_ids':sorted(paid),'cumulative_cost':add(w['owner_costs'][n] for n in paid)})
 ac={'stages':stages,'historical_full_document_cost':w['document_costs']['L012'],'scope':'An explicit library acquisition order, not elapsed research chronology. Full U and six complete programs are paid before the full application. No sawtooth claim can be inferred from one application.','cross_topic_discount':False,'expanded_external_proof_cost':None,'graphics_cost':None}
 (out/'acquisition.json').write_text(json.dumps(ac,indent=2)+'\n')
 plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'affine-cost-acquisition'})
 fig,ax=plt.subplots(figsize=(8.1,3.05));colors=['#3775a5','#668f62','#b27535'];vals=[primary(x['new_cost']) for x in stages];start=0
 for val,col,label in zip(vals,colors,['Common paper','Six whole programs','Application']):
  ax.barh(1,val,left=start,color=col,height=.35,label=label);ax.text(start+val/2,1,f'{val:,}',ha='center',va='center',color='white',fontsize=11);start+=val
 old=primary(w['document_costs']['L012']);ax.barh(0,old,color='#786963',height=.35);ax.text(old/2,0,f'{old:,}',ha='center',va='center',color='white',fontsize=11)
 ax.set_yticks([0,1],['Historical manuscript','Complete replacement']);ax.set_xlim(0,start*1.08);ax.set_xlabel('Calibrated NFC characters without whitespace');ax.legend(loc='upper left',bbox_to_anchor=(0,1.23),ncol=3,frameon=False);ax.spines[['top','right']].set_visible(False)
 fig.tight_layout()
 for ext in ['pdf','svg','png']:fig.savefig(out/f'acquisition.{ext}',dpi=170,bbox_inches='tight')
 plt.close(fig)
 tex=r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=26mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,array,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\setmonofont{Menlo}
\hypersetup{colorlinks=true,urlcolor=blue}\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\setlength{\emergencystretch}{3em}
\title{Where the affine proof costs lie}\author{\texttt{human\_compression}}\date{Exclusive text assignment; independent cost review pending}
\begin{document}\maketitle\vspace{-1em}
The accepted comparison concerns one complete historical manuscript,
Hou--Feng--Leemans, \emph{Regular 3-polytopes of order $2^np$},
arXiv:2001.02945v2 (14 July 2024), and its complete replacement: the common
paper, the application, and six whole mathematical programs. Its 33 detailed
records describe one principal contract, including retained inputs and
qualifications. They are not 33 new theorems.

The table preserves the independently accepted measurement. The ruler is
calibrated NFC characters without whitespace; all other 29 coordinates remain
in the data. These are extracted-text costs. Formula layout, unextracted
images, expanded external proofs and unavailable historical software are
unknown. No total comparison including those unknown quantities is asserted.
\begin{center}\begin{tabular}{@{}lr@{}}\toprule
Complete document & Cost \\\midrule
Historical manuscript (17 pages) & 32,767\\
Common paper (7 pages) & 19,070\\
Application (9 pages) & 22,638\\
Six complete programs, printed appendix (8 pages) & 17,250\\\bottomrule
\end{tabular}\end{center}
The whole written comparison is $32767/41708\simeq0.786$.
Including the printed programs gives $32767/58958\simeq0.556$;
using their complete raw files instead gives $32767/58390\simeq0.561$.
The raw and printed forms are alternatives, not two charges for the same code.
The replacement is longer under these whole-topic rulers.
After the \emph{whole} common paper and all six programs have been paid,
the separate conditional comparison is $32767/22638\simeq1.447$.
It does not replace the whole-topic comparison or waive the acquisition cost.

\textbf{From passages to proof routes.}
Every character belongs to exactly one of 194 owners, including four owners
for page furniture in the untrimmed coordinate. The selected texts have 190
disjoint spans. Front matter, references, connective prose, unused common
results and excluded source assertions all retain their costs. Repeated
printed statements are paid for every occurrence.

A mathematical node can refer to several owners. Two nodes may need the same
statement or presentation, so their displayed interface costs can overlap.
For a proof route we first take the logical prerequisite closure, then the
\emph{union} of its owners, and only then sum. Adding box costs would be wrong.
There is no compression factor derived from graph size or from an individual
33-row route. The full manuscript remains the denominator boundary even
where a selected proof uses only part of it.
\newpage
\textbf{The shared arguments and local work.}
The supported-kernel theorem supplies the odd-factor construction; the
application still pays for its exact commutator periods and reverse
presentation bound. The affine presentation bridge and period-intersection
criterion are reused for both cubic types. Each application supplies its
actual translation words, invariant lattice and finite overlap calculation.
The source instead rewrites three subgroups and identifies three base
quotients for each cubic type. Both graphs retain these actual dependencies;
neither substitutes invented repetitions for the source's own reuse.

Problem 1.1, the separate small-order table and the uniqueness assertion for
the two order-384 seeds remain excluded. The final odd-label existence
question was already answered historically; its complete local model is
included with attribution and no new question credit.

The exact source presentations and common theorem statements are explicitly
shared among their branches. For example, each branch of source Lemma 4.5
includes its setup and common displayed argument. Its first branch remains
flagged as false in the bound edition. The replacement proves the sign
obstruction and corrected construction. Corollary 5.2's printed reference
is also flagged. Costs do not validate either documentary defect.

The one-edge extension has an independent proof. Its comparison with the
supported-kernel theorem is not treated as a premise. The unused deletion
corollary and the smaller-period lemma remain paid in the full common paper.
Historical citations and replacement citations are treated alike: their
printed statements are measurable, while unincorporated proofs remain null.

\includegraphics[width=\linewidth]{acquisition.pdf}
The drawing shows an acquisition order, not the chronology of research.
With one application, it cannot demonstrate a repeated sawtooth pattern.
Common theory reused from another topic is paid again for this independent
topic; only reuse inside this topic can use its already acquired library.

\textbf{Complete graphs and evidence.}
The linked \href{historical_graph.svg}{historical graph} and
\href{new_graph.svg}{replacement graph} show every mathematical prerequisite
edge in their respective sides, including external leaves. Arrows point from
prerequisite to use. Box labels give overlapping interface costs, not new
charges. Formal, diagnostic, operational, attribution and comparison links
are separately recorded and do not enlarge proof closures.

The six mathematical files stay whole, including embedded diagnostics.
Two drivers and one diagnostic are separately measured (16,581 raw characters);
three Lean files are also separate (7,958), with exactly nine scoped
declarations. These prove two smaller-period statements, three sign identities
and four generic quotient criteria. They do not certify affine coordinates,
actual subgroup presentations or catalogue completeness. Historical code and
algorithm/catalogue construction costs remain unknown.

\textbf{Review boundary.}
The logical graph and complete-document arithmetic have distinct prior
acceptances. The present author also reviewed that graph and authored the
canonical affine papers; this ownership assignment therefore awaits another
reviewer. Its replay verifies all 120 PDF metric cells, all whole files and
all prerequisite-owner unions. It introduces no new mathematical result,
source credit, conjecture solution or formal theorem.
\end{document}
'''
 (out/'reader.tex').write_text(tex)
 (out/'reader_input_bindings.json').write_text(json.dumps({'files':{str(p.relative_to(root)):sha(p.read_bytes()) for p in [HERE/'partition.json',HERE/'weights.json',HERE/'protocol.json',root/'topic_Affine_logical_dag_v2/logical_graph.json']},'scope':'Derived views only; exact admitted whole-document arithmetic preserved.'},indent=2)+'\n')
 return graphs

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 g=build(a.study_root.resolve(),a.out)
 print(json.dumps({k:{'nodes':len(v['nodes']),'logical_edges':len(v['edges'])} for k,v in g.items()}))
if __name__=='__main__':main()
