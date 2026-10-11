#!/usr/bin/env python3
"""Static named C4 view, using exactly the offline reader's prerequisite edges."""
import argparse,json,os,tempfile,textwrap
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'topic-c-dependency-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():raise ValueError('fresh static output')
 a.out.mkdir(parents=True);d=json.loads((a.packet/'view_data.json').read_text());by={n['id']:n for n in d['nodes']};logical=set(d['logical_edge_kinds']);route=set(next(x for x in d['pairs'] if x['id']=='C4')['new_targets'])
 while True:
  old=set(route);route|={e['source'] for e in d['edges'] if e['target'] in route and e['kind'] in logical}
  if old==route:break
 def parent(n):
  while n in d['parents']:n=d['parents'][n]
  return n
 ids=sorted({parent(n) for n in route if by[n]['side']=='new' and not by[n]['external']});es=sorted({(parent(e['source']),parent(e['target'])) for e in d['edges'] if e['kind'] in logical and parent(e['source']) in ids and parent(e['target']) in ids and parent(e['source'])!=parent(e['target'])})
 depth={n:0 for n in ids}
 for i in range(len(ids)):
  new={n:max([depth[x]+1 for x,y in es if y==n]+[0]) for n in ids}
  if new==depth:break
  depth=new
 else:raise ValueError('collapsed graph cycle')
 cols={}
 for n in ids:cols.setdefault(depth[n],[]).append(n)
 maxrows=max(map(len,cols.values()));positions={n:(col*3.0,(maxrows-1)/2-row*1.9) for col,ns in cols.items() for row,n in enumerate(ns)}
 plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'topic-c-static-proof-view'})
 fig,ax=plt.subplots(figsize=(18,7.5));ax.set_xlim(-.2,max(depth.values())*3+2.7);ax.set_ylim((maxrows-1)/2-(maxrows-1)*1.9-1.35,(maxrows-1)/2+.9);ax.axis('off')
 for x,y in es:
  axy=positions[x];bxy=positions[y]
  ax.add_patch(FancyArrowPatch((axy[0]+2.4,axy[1]),(bxy[0],bxy[1]),connectionstyle='arc3,rad=0.06' if bxy[0]-axy[0]>3.01 else 'arc3,rad=0',arrowstyle='-|>',mutation_scale=10,lw=1.0,color='#86939e',zorder=1))
 for n in ids:
  x,y=positions[n];row=by[n];ax.add_patch(FancyBboxPatch((x,y-.78),2.4,1.56,boxstyle='round,pad=.025',linewidth=.7,edgecolor='#9aaebb',facecolor='#e6f2fa',zorder=2))
  ax.text(x+.09,y+.57,n,fontsize=7.4,color='#425869',zorder=3)
  ax.text(x+.09,y+.32,'\n'.join(textwrap.wrap(row['label'],25)),fontsize=7.1,va='top',zorder=3)
  cost=row['weight']['calibrated_selected']['NFC']['characters_without_whitespace'];ax.text(x+.09,y-.64,row['document'],fontsize=7,color='#425869',zorder=3);ax.text(x+2.30,y-.64,f'{cost:,}',ha='right',fontsize=7,color='#425869',zorder=3)
 ax.set_title('C4: common binary translation proofs to equal-parameter polyhedra',fontsize=13,pad=18)
 fig.text(.02,.025,'Arrows: prerequisite → use. Named boxes include shared passages; do not sum box costs. External inputs are hidden in this static view and remain unknown.',fontsize=9)
 for ext in ['svg','pdf','png']:fig.savefig(a.out/('default_graph.'+ext),dpi=150,bbox_inches='tight',facecolor='white')
 plt.close(fig)
 (a.out/'static_graph.json').write_text(json.dumps({'target':'C4 complete fixed contract','side':'new','granularity':'named','displayed_node_ids':ids,'displayed_edges':[{'source':x,'target':y} for x,y in es],'external_nodes_hidden':True,'not_a_browser_screenshot':True},indent=2)+'\n')
 print(json.dumps({'nodes':len(ids),'edges':len(es),'out':str(a.out)}))
if __name__=='__main__':main()
