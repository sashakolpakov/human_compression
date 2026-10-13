#!/usr/bin/env python3
"""Independent literal permutation closure; no GAP or author helper imports."""
from itertools import combinations
from pathlib import Path
import argparse,json
ID=tuple(range(8))
def transpositions(pairs):
 p=list(ID)
 for a,b in pairs:p[a-1],p[b-1]=p[b-1],p[a-1]
 return tuple(p)
def mul(a,b):return tuple(b[x]for x in a)
def subgroup(gs):
 found={ID};todo=[ID]
 for a in todo:
  for g in gs:
   c=mul(a,g)
   if c not in found:found.add(c);todo.append(c)
 return frozenset(found)
def need(v,m):
 if not v:raise ValueError(m)
def certify(r,Q):
 need(len(r)==4 and all(sorted(x)==list(ID)and x!=ID and mul(x,x)==ID for x in r),'four actual involutions')
 need(all(mul(r[i],r[j])==mul(r[j],r[i])for i in range(4)for j in range(i+2,4)),'string commuting')
 subs={mask:subgroup([r[i]for i in range(4)if mask>>i&1])for mask in range(16)}
 need(len(subs[15])==40320,'S8 by faithful full degree8 order')
 orbits=[]
 for i in range(4):
  H=subs[15^(1<<i)];pieces=[];unseen=set(ID)
  while unseen:
   a=min(unseen);o={h[a]for h in H};pieces.append(sorted(x+1 for x in o));unseen-=o
  orbits.append(pieces)
  need(len(Q[i])==2,'two selected edges per colour')
  for aa,bb in Q[i]:
   a,b=aa-1,bb-1;need(a!=b and r[i][a]==b,'literal generator edge');need(b not in {h[a]for h in H},'actual omitted-group orbit crossing')
 edges=[tuple(sorted(e))for col in Q for e in col]
 need(len(set(edges))==8,'eight distinct selected edges')
 adjacency={i:set()for i in range(1,9)}
 for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
 seen={1};queue=[1]
 for a in queue:
  for b in adjacency[a]:
   if b not in seen:seen.add(b);queue.append(b)
 need(seen==set(range(1,9)),'connected full-vertex selection')
 selected=[(1,2,0),(2,4,2),(4,3,0),(3,1,2)]
 need(all(tuple(sorted((a,b)))in {tuple(sorted(e))for e in Q[i]}for a,b,i in selected),'displayed unique selected square')
 # Connected E=V gives cycle rank one, so the displayed simple square is unique.
 second=[(1,2,0),(2,7,3),(7,5,0),(5,1,3)]
 need(all(r[i][a-1]==b-1 for a,b,i in second),'actual second alternating square')
 need(tuple(sorted((1,5)))in Q[3]and tuple(sorted((2,7)))not in Q[3],'exactly one of parallel colour3 edges selected')
 failures=[(a,b)for a in range(16)for b in range(16)if subs[a]&subs[b]!=subs[a&b]]
 need(failures==[(7,14),(14,7)],'exact full intersection-property failures')
 need([len(subs[7]),len(subs[14]),len(subs[7]&subs[14]),len(subs[6])]==[720,720,24,12],'literal parabolic orders')
 parity=[sum(g[a]>g[b]for a in range(8)for b in range(a+1,8))%2 for g in r]
 need(parity==[1,0,0,1],'exact oddness obstruction')
 return dict(order=40320,omission_orbits=orbits,subset_groups=16,intersection_pairs=256,IP_failure_masks=failures,parabolic_orders=[720,720,24,12],selected_vertices=8,selected_edges=8,cycle_rank=1,selected_square=[1,2,4,3],second_square=[1,2,7,5],generator_parities=parity)
def run():
 r=[transpositions(x)for x in [[(1,2),(3,4),(5,7)],[(2,6),(7,8)],[(1,3),(2,4)],[(1,5),(2,7),(6,8)]]]
 Q=[[(1,2),(3,4)],[(2,6),(7,8)],[(1,3),(2,4)],[(1,5),(6,8)]]
 out=certify(r,Q)
 controls=[]
 for name,rr,qq in [('noninvolutory',[(1,2,0,3,4,5,6,7)]+r[1:],Q),('missing generator',[ID]+r[1:],Q),('remove displayed selected square',r,[[(1,2),(5,7)]]+Q[1:]),('missing selected edge',r,Q[:3]+[[(1,5)]]),('both parallel edges selected',r,Q[:3]+[[(1,5),(2,7)]]),('wrong generator edge',r,[[(1,3),(3,4)]]+Q[1:])]:
  try:certify(rr,qq)
  except ValueError as e:controls.append(dict(name=name,rejected_at=str(e)))
  else:raise ValueError('survived control '+name)
 out.update(status='PASS_INDEPENDENT_COORDINATE_RECONSTRUCTION',controls=controls,author_code_imported=False,full_L044_or_conjecture_claim=False)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
