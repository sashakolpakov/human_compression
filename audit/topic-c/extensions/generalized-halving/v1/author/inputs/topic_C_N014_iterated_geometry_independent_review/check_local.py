#!/usr/bin/env python3
"""Independent bounded diagnostics; no author imports, no uniform proof claim."""
import argparse,itertools,json
from pathlib import Path
import sympy as S

def need(b,m):
 if not b: raise ValueError(m)
def unit(n,i,sgn=1):return tuple(sgn if j==i else 0 for j in range(n))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def distance(x,y):return sum(abs(a-b) for a,b in zip(x,y))
def roots(n):return {add(unit(n,i,a),unit(n,j,b)) for i,j in itertools.combinations(range(n),2) for a,b in itertools.product((-1,1),repeat=2)}
def graph_profile(vertices,adj):
 vs=list(vertices);edges=[(i,j) for i in range(len(vs)) for j in range(i) if adj(vs[i],vs[j])]
 nbr=[set() for _ in vs]
 for i,j in edges:nbr[i].add(j);nbr[j].add(i)
 colors={0:0}; todo=[0];bip=True
 while todo:
  i=todo.pop()
  for j in nbr[i]:
   if j not in colors:colors[j]=1-colors[i];todo.append(j)
   elif colors[j]==colors[i]:bip=False
 return dict(vertices=len(vs),edges=len(edges),connected=len(colors)==len(vs),bipartite=bip)
def local_flags():
 rows=[]
 for n in range(3,7):
  cube=list(itertools.product((0,1),repeat=n));ev=[v for v in cube if sum(v)%2==0];od=[v for v in cube if sum(v)%2]
  families=[[(v,) for v in cube],[(p,w) for p in ev for w in od if distance(p,w)==1],[(p,q) for p,q in itertools.combinations(ev,2) if distance(p,q)==2],[(p,q,w) for p,q in itertools.combinations(ev,2) if distance(p,q)==2 for w in od if distance(p,w)==distance(q,w)==1]]
  totals=[];center_checks=0
  for family in families:
   totals.append(len(family))
   for flag in family:
    lo=tuple(min(v[i] for v in flag) for i in range(n));hi=tuple(max(v[i] for v in flag) for i in range(n));d=sum(x!=y for x,y in zip(lo,hi))
    need(d<=2,'small-face span')
    # Actual cubes meeting these vertices have lower corners in {-1,0,1}^n.
    choices=[tuple(x for x in (-1,0,1) if all(x<=v[i]<=x+1 for v in flag)) for i in range(n)]
    corners=list(itertools.product(*choices))
    need(len(corners)==2**(n-d),'dual cube cardinality')
    varying=[i for i in range(n) if len(choices[i])==2]
    need(len(varying)==n-d,'dual cube dimension')
    # Odd central cube chosen by reflection/translation; count its neighboring
    # cubes containing the flag directly, not from a graph-family formula.
    neighbors=[unit(n,i,sgn) for i in range(n) for sgn in (-1,1)]
    valid=[v for v in neighbors if all(all(v[i]<=x[i]<=v[i]+1 for i in range(n)) for x in flag)]
    need(len(valid)==n-d,'facets through common span')
    need(all(sub(x,y) in roots(n) for x,y in itertools.combinations(valid,2)),'actual common center shadow clique')
    center_checks+=1
  rows.append(dict(n=n,lower_flags_by_size_and_kind=totals,dual_cube_and_clique_checks=center_checks))
 return rows

def hom(n,which):
 M=S.eye(n+1)
 if which=='left':M[0,0]=-1;M[0,n]=1
 elif which=='right':M[n-1,n-1]=-1
 else:
  i,j=which;M[i,i]=M[j,j]=0;M[i,j]=M[j,i]=1
 return M
def marked(n,a,b):
 g=[hom(n,'left')]+[hom(n,(i,i+1)) for i in range(n-1)]+[hom(n,'right')]
 # Construct from displayed explicit formulas independently of author conjugations.
 if a:
  j=a;M=hom(n,(0,j));M[0,:]=-M[0,:];M[j,:]=-M[j,:];M[0,n]=M[j,n]=1;g[0]=M
 if b:
  i=n-1-b;j=n-1;M=hom(n,(i,j));M[i,:]=-M[i,:];M[j,:]=-M[j,:];g[-1]=M
 return g
def order(M):
 P=S.eye(M.rows)
 for m in range(1,13):
  P=P*M
  if P==S.eye(M.rows):return m
 raise ValueError('order exceeds12')
def target(n,a,b):
 E={(i,i+1):3 for i in range(1,n-1)}
 if a==0:E[0,1]=4
 elif a==1:E[0,2]=3
 else:
  E.update({(0,1):3,(0,2):3,(0,3):4 if n==3 else 3})
 if b==0:E[n-1,n]=4
 elif b==1:E[n-2,n]=3
 else:E.update({(n-3,n):3,(n-2,n):3,(n-1,n):3})
 if (n,a,b) in ((3,1,1),(4,2,1),(5,2,2)):E[0,n]=3
 return E
def diagrams():
 rows=[]
 for n in range(3,8):
  states=[(0,0),(1,0),(1,1),(2,0)]+([(2,1)] if n>=4 else [])+([(2,2)] if n>=5 else [])
  for a,b in states:
   g=marked(n,a,b);actual={(i,j):order(g[i]*g[j]) for i,j in itertools.combinations(range(n+1),2)}
   need(all(order(x)==2 for x in g),'involution');need({p:m for p,m in actual.items() if m>2}==target(n,a,b),'all diagram bonds')
   need(all(order((g[i]*g[j])[:n,:n])==m for (i,j),m in actual.items()),'linear lower bound')
   E=target(n,a,b);leaves=[i for i in range(n+1) if sum(i in p for p in E)==1]
   if (a,b)==(0,0):expected=[0,n]
   elif (a,b)==(1,0):expected=[0,1,n]
   elif (a,b)==(1,1):expected=[] if n==3 else [0,1,n-1,n]
   elif (a,b)==(2,0):expected=[] if n==3 else [n]
   elif (a,b)==(2,1):expected=[] if n==4 else [n-1,n]
   else:expected=[]
   need(leaves==expected,'exhaustive leaf list')
   rows.append(dict(n=n,state=[a,b],pairs=len(actual),leaves=leaves))
 return rows

def run():
 local=local_flags();graphs=[]
 for m in range(3,8):
  cube=list(itertools.product((0,1),repeat=m))
  for parity in (0,1):
   d=graph_profile([v for v in cube if sum(v)%2==parity],lambda x,y:distance(x,y)==2)
   need(d['connected'] and not d['bipartite'],'demicube PC')
   graphs.append(dict(kind='demicube',m=m,parity=parity,**d))
  cp=graph_profile([unit(m,i,s) for i in range(m) for s in (-1,1)],lambda x,y:sub(x,y) in roots(m))
  need(cp['connected'] and not cp['bipartite'],'cross-polytope PC');graphs.append(dict(kind='cross-polytope',m=m,**cp))
 rows=diagrams()
 # Concrete second-step degeneracy; no classification algorithm needed.
 n=3;z=(0,)*n;e=unit(n,0);f=unit(n,1);p=add(e,f)
 square1={z,e,f,p};square2={z,tuple(-x for x in e),tuple(-x for x in f),tuple(-x for x in p)}
 def period(v):return all(x%2==0 for x in v) and sum(x//2 for x in v)%2==0
 need(period(tuple(2*x for x in p)),'opposite root collision 2D')
 need(not any(period(sub(e,x)) for x in square2),'B2 counterexample')
 need(not any({add(x,t) for x in square2}==square1 for t in [sub(x,z) for x in square1] if period(t)),'distinct square orbits')
 controls=[]
 def rejected(fn):
  try:fn()
  except ValueError:return True
  return False
 q=graph_profile([(0,0),(1,1)],lambda x,y:distance(x,y)==2)
 need(rejected(lambda:need(not q['bipartite'],'dimension2 is not PC-safe')),'dimension control');controls.append('dimension2 demicube cannot replace dimension>=3')
 need(rejected(lambda:need(not period((2,2,0)),'k2s2 admitted')),'period control');controls.append('k2s2 omission rejected by actual root collision')
 need(rejected(lambda:need(any(period(sub(e,x)) for x in square2),'wrong B2')),'B2 control');controls.append('false odd-vertex square incidence rejected')
 need(rejected(lambda:need(order(marked(3,2,0)[0]*marked(3,2,0)[3])==3,'wrong4bond')),'bond control');controls.append('n3 4-bond changed to3 rejected')
 need(rejected(lambda:need(order(marked(5,2,2)[0]*marked(5,2,2)[5])==2,'missing overlap')),'overlap control');controls.append('n5 overlap bond omission rejected')
 return dict(status='PASS',role='independent bounded diagnostics only; written proof is uniform',lower_flag_checks=local,shadow_graphs=graphs,diagrams=rows,controls=controls,source_period_counterexample=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run();a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],local_flags=sum(x['dual_cube_and_clique_checks'] for x in r['lower_flag_checks']),diagrams=len(r['diagrams']),shadow_graphs=len(r['shadow_graphs']),controls=len(r['controls']))))
