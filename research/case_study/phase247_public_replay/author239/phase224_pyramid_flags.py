#!/usr/bin/env python3
"""Literal pyramid construction and every colored component intersection."""
import json
from collections import deque
from pathlib import Path

def require(ok,label):
 if not ok:raise ValueError(label)

def build_flags(m=3):
 require(m>=2,'square torus side length')
 vertex=lambda x,y:(x%m)+m*(y%m)
 edge=lambda x,y,d:2*vertex(x,y)+d
 base=[]
 for x in range(m):
  for y in range(m):
   vs=[vertex(x,y),vertex(x+1,y),vertex(x+1,y+1),vertex(x,y+1)]
   es=[edge(x,y,0),edge(x+1,y,1),edge(x,y+1,0),edge(x,y,1)]
   require(len(set(vs))==len(set(es))==4,'embedded base square')
   for j in range(4):base.extend([(vs[j],es[j],vertex(x,y)),(vs[(j+1)%4],es[j],vertex(x,y))])
 flags=[]
 for v,e,f in base:
  b=[v,e,f,0];cone=[0,v,e,f]
  for j in range(5):flags.append(tuple(('b' if i<j else 'c',b[i] if i<j else cone[i]) for i in range(4)))
 require(len(flags)==len(set(flags))==40*m*m,'pyramid flag list')
 return flags

def analyze_flags(flags):
 n=len(flags);adj=[]
 for i in range(4):
  blocks={}
  for j,f in enumerate(flags):blocks.setdefault(f[:i]+f[i+1:],[]).append(j)
  require(all(len(a)==2 for a in blocks.values()),'unique flag adjacency')
  a=[None]*n
  for j,k in blocks.values():a[j]=k;a[k]=j
  adj.append(a)
 for i in range(4):
  require(all(adj[i][v]!=v and adj[i][adj[i][v]]==v for v in range(n)),'fixed-point-free involutions')
  for j in range(i+2,4):require(all(adj[i][adj[j][v]]==adj[j][adj[i][v]] for v in range(n)),'string squares')
 orbit=[]
 for mask in range(16):
  labels=[None]*n;remaining=set(range(n))
  while remaining:
   root=min(remaining);seen={root};q=[root]
   for v in q:
    for i in range(4):
     if mask>>i&1:
      w=adj[i][v]
      if w not in seen:seen.add(w);q.append(w)
   bits=sum(1<<v for v in seen)
   for v in seen:labels[v]=bits
   remaining-=seen
  orbit.append(labels)
 require(orbit[15][0]==(1<<n)-1,'connected flag graph')
 for v in range(n):
  for a in range(16):
   for b in range(16):require(orbit[a][v]&orbit[b][v]==orbit[a&b][v],'component intersection property')
 model={'name':'Pyramid_square_torus_3','degree':n,'generators':[[v+1 for v in a] for a in adj]}
 return model,{'flags':n,'rank':4,'all_component_intersections':n*16*16,'status':'PASS'}

def gap_input(model):return 's:=['+','.join('PermList('+str(a)+')' for a in model['generators'])+'];;\n'
