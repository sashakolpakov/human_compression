"""Small exact geometric controls with no author imports."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
from itertools import combinations,product
import json
W=Path(__file__).resolve().parent
def need(b,m):
 if not b:raise ValueError(m)
def compose(g,h):
 return tuple((1 if x>0 else -1)*g[abs(x)-1] for x in h)
def action(g,x):
 y=[0]*len(g)
 for i,a in enumerate(g):y[abs(a)-1]=(1 if a>0 else -1)*x[i]
 return tuple(y)
def closure(gs,n):
 e=tuple(range(1,n+1));a={e};q=[e]
 for x in q:
  for g in gs:
   y=compose(g,x)
   if y not in a:a.add(y);q.append(y)
 return a
def dot(x,y):return sum(a*b for a,b in zip(x,y))
reports=[]
for typ,n in [('B',3),('D',4)]:
 gs=[]
 for i in range(n-1):
  s=list(range(1,n+1));s[i],s[i+1]=s[i+1],s[i];gs.append(tuple(s))
 if typ=='B':gs.append(tuple(list(range(1,n))+[-n]));weights=[tuple(1 if j<=i else 0 for j in range(n))for i in range(n)]
 else:
  s=list(range(1,n+1));s[-2],s[-1]=-n,-(n-1);gs.append(tuple(s))
  weights=[tuple(2 if j<=i else 0 for j in range(n))for i in range(n-2)]+[tuple([1]*(n-1)+[-1]),tuple([1]*n)]
 G=closure(gs,n);need(len(G)==(48 if typ=='B' else 192),'actual group order')
 antipode=tuple(-i for i in range(1,n+1));need(antipode in G,'central antipode')
 pars=[closure(gs[:i]+gs[i+1:],n)for i in range(n)]
 need(all(antipode not in H for H in pars),'proper parabolic injection')
 for i,j in combinations(range(n),2):need(not any(compose(a,b)==antipode for a in pars[i]for b in pars[j]),'literal product avoidance')
 orbits=[{action(g,w)for g in G}for w in weights]
 pair_checks=0;bad=[]
 for i in range(n):
  for j in range(n):
   if i==j:continue
   actual={action(g,weights[j])for g in pars[i]};c=dot(weights[i],weights[j]);need(c>0,'positive fundamental pair')
   for v in orbits[j]:
    pair_checks+=1;need(dot(weights[i],v)<=c and ((dot(weights[i],v)==c)==(v in actual)),'exact numerical incidence criterion')
 for i,j,k in product(range(n),repeat=3):
  if len({i,j,k})!=3:continue
  for v in orbits[k]:
   if dot(weights[i],v)==dot(weights[i],weights[k]) and dot(weights[j],v)==-dot(weights[j],weights[k]):bad.append([i,j,k,list(v)])
 need(bool(bad)==(typ=='D'),'negative triangle distinction')
 canonical=lambda g:min(g,tuple(-x for x in g))
 sub=[]
 for mask in range(1<<n):sub.append({canonical(g)for g in closure([gs[i]for i in range(n)if mask>>i&1],n)})
 for a,b in product(range(1<<n),repeat=2):need(sub[a]&sub[b]==sub[a&b],'all actual quotient subset intersections')
 reports.append(dict(type=typ+str(n),order=len(G),fundamental_orbit_sizes=list(map(len,orbits)),pair_checks=pair_checks,negative_triangle_count=len(bad),first_negative_triangle=bad[:1],quotient_subset_pairs=(1<<n)**2))
# Uniform displayed D_n signed triple and its explicit two-sign-change map.
for n in range(4,42,2):
 v=(1,)*n;w=(1,)*(n-1)+(-1,);x=(0,)*(n-1)+(2,)
 g=list(range(1,n+1));g[0]=-n;g[-1]=-1
 need(action(g,w)==w and action(g,(2,)+(0,)*(n-1))==tuple(-a for a in x),'explicit even signed permutation')
 need(dot(v,w)>0 and dot(v,x)>0 and dot(w,x)<0,'displayed negative triple')
out=dict(status='PASS_INDEPENDENT_GEOMETRIC_CONTROLS',cases=reports,even_D_cases=19)
(W/'independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
