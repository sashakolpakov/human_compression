#!/usr/bin/env python3
"""Distinct tuple/group-set census; no author imports, no external group library."""
from itertools import permutations
from functools import lru_cache
from pathlib import Path
import argparse,json

def need(ok,msg):
 if not ok:raise ValueError(msg)
def compose(p,q):return tuple(p[q[i]] for i in range(5))
def even(p):return sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0
S=list(permutations(range(5)));A=[p for p in S if even(p)];E=(tuple(range(5)),0)
def product(a,b):return compose(a[0],b[0]),a[1]^b[1]
G=frozenset((p,e) for p in A for e in (0,1));invol=sorted(x for x in G if x!=E and product(x,x)==E)
@lru_cache(None)
def close(gens):
 found={E};front=[E]
 while front:
  x=front.pop()
  for g in gens:
   y=product(x,g)
   if y not in found:found.add(y);front.append(y)
 return frozenset(found)
def subgroup(t):return close(tuple(sorted(t)))
def independent(t):return all(x not in subgroup(t[:i]+t[i+1:]) for i,x in enumerate(t))
def ip(t):
 subs=[subgroup(tuple(t[i] for i in range(len(t)) if m&(1<<i))) for m in range(1<<len(t))]
 return all(subs[a]&subs[b]==subs[a&b] for a in range(len(subs)) for b in range(a))
def order(x):
 z=E
 for n in range(1,121):
  z=product(z,x)
  if z==E:return n
 raise ValueError('order')
# Enumerate with independence, not the author's prefix-IP pruning.
terminal={r:[] for r in range(1,7)};prefix={r:0 for r in range(1,7)}
def walk(t,H):
 prefix[len(t)]+=1
 if H==G:
  if ip(t):terminal[len(t)].append(t)
  return
 if len(t)==6:return
 for x in invol:
  if x in H or any(product(x,y)!=product(y,x) for y in t[:-1]):continue
  v=t+(x,)
  if independent(v):walk(v,subgroup(v))
for x in invol:walk((x,),subgroup((x,)))
inverses={p:tuple(p.index(i) for i in range(5)) for p in S}
def conjugate(t,p):return tuple((compose(compose(p,x[0]),inverses[p]),x[1]) for x in t)
def canon(t,reverse=True):
 orbit=[conjugate(t,p) for p in S]
 return min(orbit+[v[::-1] for v in orbit] if reverse else orbit)
rows=[]
for r,ts in terminal.items():
 reps=sorted({canon(t) for t in ts});entries=[]
 for t in reps:
  entries.append({'marking':[list(x[0])+([5,6] if x[1]==0 else [6,5]) for x in t], 'schlafli':[order(product(t[i],t[i+1])) for i in range(r-1)],'self_dual':canon(t,False)==canon(t[::-1],False)})
 rows.append({'rank':r,'classes':len(reps),'connected':sum(all(v>2 for v in e['schlafli']) for e in entries),'self_dual':sum(e['self_dual'] for e in entries),'representatives':entries,'ordered_full_markings':len(ts)})
need([(x['classes'],x['connected'],x['self_dual']) for x in rows]==[(0,0,0),(0,0,0),(8,8,1),(3,0,0),(0,0,0),(0,0,0)],'whole independent census')
# Exact displayed marking, relation/generation/IP and Coxeter triple checks.
def perm(*cycles):
 p=list(range(5))
 for cyc in cycles:
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):p[a-1]=b-1
 return tuple(p)
a=(perm((1,2),(3,4)),0);b=(perm((1,2),(3,5)),0);c=(perm((1,3),(2,4)),0);z=(E[0],1)
need([order(product(a,b)),order(product(b,c)),order(product(a,c))]==[3,5,2],'displayed products')
need(subgroup((z,a,b,c))==G and ip((z,a,b,c)),'rank4 witness')
need(subgroup(tuple(product(z,x) for x in (a,b,c)))==G,'Coxeter surjection')
# Semantic negative checks: adding a dependent generator, wrong adjacency,
# using connected-only census as all-string census, and false self-duality.
controls=[]
need(not independent((a,b,c,z,a)),'dependent negative');controls.append('dependent generator')
need(not ip((a,b,c,product(a,c))),'IP negative');controls.append('extra endpoint product')
need(product(b,c)!=product(c,b),'nonadjacent negative');controls.append('wrong string ordering')
need(any(2 in x['schlafli'] for x in rows[3]['representatives']),'connected omission');controls.append('connected-only incomplete')
need(all(not x['self_dual'] for x in rows[3]['representatives']),'rank4 self-duality');controls.append('false self-duality')
# Additional bounded independent dihedral check for each m=3..18.
dihedral=[]
for m in range(3,19):
 e=(0,0);elts=[(i,j) for i in range(m) for j in (0,1)]
 def mul(x,y):return ((x[0]+(-1 if x[1] else 1)*y[0])%m,x[1]^y[1])
 @lru_cache(None)
 def cl(t):
  v={e};f=[e]
  while f:
   x=f.pop()
   for y in t:
    q=mul(x,y)
    if q not in v:v.add(q);f.append(q)
  return frozenset(v)
 iv=[x for x in elts if x!=e and mul(x,x)==e];exists=False
 for u in iv:
  for v in iv:
   if u==v:continue
   for w in iv:
    if w in (u,v) or mul(u,w)!=mul(w,u):continue
    t=(u,v,w);ss=[cl(tuple(t[i] for i in range(3) if mask>>i&1)) for mask in range(8)]
    if len(ss[7])==2*m and all(ss[i]&ss[j]==ss[i&j] for i in range(8) for j in range(i)):exists=True
 need(exists==(m%4==2),'dihedral '+str(m));dihedral.append({'m':m,'rank3_exists':exists})
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();args.out.parent.mkdir(parents=True,exist_ok=True)
out={'status':'PASS_DISTINCT_SMALL_ORACLE','group_order':len(G),'involutions':len(invol),'independent_prefixes':prefix,'rows':rows,'controls':controls,'dihedral_cases':dihedral,'author_imports':False,'new_science_scope':False}
args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['rows','dihedral_cases']}))
