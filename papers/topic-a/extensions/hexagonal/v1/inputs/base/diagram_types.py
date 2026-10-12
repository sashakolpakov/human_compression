#!/usr/bin/env python3
"""Exact optional check of the elementary four-vertex diagram case split."""
from fractions import Fraction
from itertools import combinations, permutations, product
import json

def derive():
 edges=list(combinations(range(4),2));perms=list(permutations(range(4)));classes={}
 for vals in product(range(2,7),repeat=6):
  d=dict(zip(edges,vals));deg=[sum(v>2 for e,v in d.items() if i in e) for i in range(4)]
  seen={0}
  for _ in range(4):seen|={j for i in seen for j in range(4) if j!=i and d[tuple(sorted((i,j)))]>2}
  if len(seen)!=4 or sorted(deg)==[1,1,2,2]:continue
  sums=[sum((Fraction(1,d[e]) for e in combinations(t,2)),Fraction()) for t in combinations(range(4),3)]
  if min(sums)<1 or 1 not in sums:continue
  key=min(tuple(d[tuple(sorted((p[i],p[j])))] for i,j in edges) for p in perms);classes[key]=classes.get(key,0)+1
 return {'status':'PASS','classes':list(classes),'count':len(classes),'scope':'Optional exact rational check; the complete diagram case split is written. No existence classification.'}
if __name__=='__main__':
 r=derive()
 if r['count']!=16:raise ValueError(r)
 print(json.dumps(r,indent=2))
