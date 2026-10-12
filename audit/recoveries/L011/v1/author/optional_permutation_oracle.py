#!/usr/bin/env python3
"""Independent small-coordinate validation, without GAP or author search imports."""
import itertools,json
from functools import lru_cache

def oracle(n):
 perms=[p for p in itertools.permutations(range(n)) if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2==0]
 index={p:i for i,p in enumerate(perms)};identity=index[tuple(range(n))];size=len(perms)
 mul=[[index[tuple(b[a[i]] for i in range(n))] for b in perms] for a in perms]
 inv=[a for a in range(size) if a!=identity and mul[a][a]==identity]
 allbits=(1<<size)-1
 @lru_cache(None)
 def span(key):
  seen={identity};stack=[identity]
  while stack:
   x=stack.pop()
   for a in key:
    y=mul[x][a]
    if y not in seen:seen.add(y);stack.append(y)
  return sum(1<<x for x in seen)
 def subgroup(xs):return span(tuple(sorted(xs)))
 def full_ip(p):
  groups=[subgroup([p[i] for i in range(len(p)) if mask>>i&1]) for mask in range(1<<len(p))]
  return all(groups[i]&groups[j]==groups[i&j] for i in range(len(groups)) for j in range(i,len(groups)))
 counts={};witnesses={}
 def dfs(p,h):
  r=len(p);counts[r]=counts.get(r,0)+1
  for t in inv:
   if h>>t&1 or mul[p[-1]][t]==mul[t][p[-1]]:continue
   if any(mul[a][t]!=mul[t][a] for a in p[:-1]):continue
   q=p+(t,)
   if not full_ip(q):continue
   hh=subgroup(q)
   if hh==allbits:witnesses[r+1]=witnesses.get(r+1,0)+1
   else:dfs(q,hh)
 for a in inv:dfs((a,),subgroup([a]))
 return dict(degree=n,group_order=size,involutions=len(inv),raw_prefix_counts=counts,raw_generating_markings=witnesses)
if __name__=='__main__':
 rows=[oracle(5),oracle(6)]
 if rows[0]['raw_generating_markings']!={3:360} or rows[1]['raw_generating_markings']!={}:raise ValueError('independent oracle discrepancy')
 print(json.dumps({'status':'PASS','role':'OPTIONAL_SMALL_COORDINATE_VALIDATION','cases':rows,'positive_inner_classes':360//60},indent=2))
