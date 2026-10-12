#!/usr/bin/env python3
"""Independent literal-permutation closure, not a universal upper-bound oracle."""
import argparse,copy,hashlib,itertools,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
PIN='61c2ebdab0787f6aba639b6c9e53d52302e054329772de75ed35c331790ff90a'
CYCLES=[[(1,2),(3,6),(4,7),(5,8),(9,11),(10,12),(13,14),(15,16)],[(1,3),(2,6),(4,5),(7,8),(9,13),(10,14),(11,15),(12,16)],[(1,4),(2,7),(3,9),(5,10),(6,11),(8,12),(13,14),(15,16)],[(1,5),(2,8),(3,4),(6,7),(9,12),(10,11),(13,16),(14,15)]]
ONE=tuple(range(16))
def need(b,m):
 if not b:raise ValueError(m)
def perm(cycles):
 p=list(ONE)
 for c in cycles:
  for x,y in zip(c,c[1:]+c[:1]):p[x-1]=y-1
 need(sorted(p)==list(ONE),'permutation');return tuple(p)
def mul(p,q):return tuple(q[p[x]] for x in range(16))
def power(p,n):
 q=ONE
 for _ in range(n):q=mul(q,p)
 return q
def order(p):
 q=ONE
 for i in range(1,1000):
  q=mul(q,p)
  if q==ONE:return i
 raise ValueError('order limit')
def closure(gs):
 seen={ONE};pending=[ONE]
 for p in pending:
  for g in gs:
   q=mul(p,g)
   if q not in seen:seen.add(q);pending.append(q)
 return seen
def evaluate(cycles):
 g=list(map(perm,cycles));need([order(x) for x in g]==[2]*4,'four involutions')
 need([order(mul(g[i],g[i+1])) for i in range(3)]==[4,4,6],'exact adjacent products')
 need(all(mul(g[i],g[j])==mul(g[j],g[i]) for i in range(4) for j in range(i+2,4)),'string commutations')
 word=lambda ii:__import__('functools').reduce(mul,[g[i] for i in ii],ONE)
 need(order(word([0,1,2,1]))==4 and order(word([1,2,3]))==3,'torus and Petrie relations')
 sub={mask:closure([g[i] for i in range(4) if mask>>i&1]) for mask in range(16)}
 need(len(sub[15])==768 and len(sub[7])==128 and len(sub[14])==48,'literal image and local orders')
 for i in range(16):
  for j in range(16):need(sub[i]&sub[j]==sub[i&j],'all subgroup intersections')
 fv=[len(sub[14])//len(sub[m]) for m in [12,10,6]];need(fv==[4,12,6],'vertex-figure counts')
 # A direct coloring obstruction also checks the flag graph convention.
 colors={ONE:0};pending=[ONE];odd_conflict=False
 for p in pending:
  for x in g[1:]:
   q=mul(p,x)
   if q in colors:odd_conflict|=(colors[p]==colors[q])
   else:colors[q]=1-colors[p];pending.append(q)
 need(len(colors)==48 and odd_conflict,'connected nonbipartite vertex flag graph')
 return dict(image_order=768,local_orders=[128,48],all_subset_pairs=256,subset_orders=[len(sub[i]) for i in range(16)],vertex_f_vector=fv,euler=-2,nonorientable=True,genus=4)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();p=a.author;need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
 need(sha(p/'manifest.json')==PIN,'author freeze')
 for e in json.loads((p/'manifest.json').read_text())['exports']:need((p/e['path']).stat().st_size==e['bytes'] and sha(p/e['path'])==e['sha256'],'author file '+e['path'])
 src=json.loads((p/'bindings.json').read_text())['source'];need(sha(a.study_root/src['path'])==src['sha256'] and (a.study_root/src['path']).stat().st_size==src['bytes'],'primary pin')
 if (HERE/'manifest.json').exists():
  for e in json.loads((HERE/'manifest.json').read_text())['exports']:need((HERE/e['path']).stat().st_size==e['bytes'] and sha(HERE/e['path'])==e['sha256'],'review file')
 tex=(p/'order768.tex').read_text();display=tex.split('\\begin{align*}')[1].split('\\end{align*}')[0]
 printed=[]
 for row in display.split('\\\\'):
  if not row.strip():continue
  pairs=re.findall(r'\((\d+)\\,(\d+)\)',row);printed.append([tuple(map(int,x)) for x in pairs])
 need(printed==CYCLES,'literal manuscript generators');data=evaluate(CYCLES)
 controls=[]
 bad=copy.deepcopy(CYCLES);bad[2],bad[3]=bad[3],bad[2]
 variants=[('swap last two generators',bad),('repeat first generator',[CYCLES[0],CYCLES[0],CYCLES[2],CYCLES[3]]),('omit transposition',[CYCLES[0][:-1]]+CYCLES[1:])]
 for name,cs in variants:
  try:evaluate(cs)
  except ValueError:controls.append(name)
  else:raise ValueError('bad marking survived '+name)
 def boundaries(x):need(x==data,'exact independent image conclusions')
 for name,key,val in [('wrong image order','image_order',384),('wrong local orders','local_orders',[64,48]),('wrong genus','genus',3),('orientable claim','nonorientable',False),('omit pair checks','all_subset_pairs',255),('wrong face count','vertex_f_vector',[4,12,8])]:
  d=copy.deepcopy(data);d[key]=val
  try:boundaries(d)
  except ValueError:controls.append(name)
  else:raise ValueError('bad result survived')
 # Frozen replay is evidence for the presentation upper bounds, not this image closure.
 for e in json.loads((HERE/'replay_bindings.json').read_text()):need((HERE/'replay'/e['path']).stat().st_size==e['bytes'] and sha(HERE/'replay'/e['path'])==e['sha256'],'replay binding')
 out=json.loads((HERE/'replay/report.json').read_text());need(out['status']=='PASS' and out['universal_order']==768 and out['facet_order']==128 and out['vertex_figure_order']==48 and out['rendered_pages']==2,'fresh universal presentation replay')
 need('PASS_768_AND_GENUS4' in (HERE/'replay/stdout.log').read_text() and not (HERE/'replay/stderr.log').read_text(),'clean exact GAP replay')
 result=dict(status='PASS',author_manifest=PIN,independent_image=data,independent_controls=controls,upper_bound_basis='Fresh exact GAP finitely presented group calculation; not inferred from image closure.',whole_original_accepted=False,new_question_credit=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
