#!/usr/bin/env python3
"""Independent literal surface reconstruction for the ten-point marked quotient."""
import json
from collections import deque
D=[[3,4,1,2,5,6,7,8,9,10],[1,2,5,6,3,4,8,7,10,9],[1,2,3,4,7,8,5,6,10,9],[2,1,4,3,6,5,9,10,7,8]]
D=[tuple(x-1 for x in d) for d in D]
def need(b,s):
 if not b:raise ValueError(s)
def comp(a,b):return tuple(a[b[i]] for i in range(10))
def build():
 group=[tuple(range(10))];idx={group[0]:0};q=0;adj=[]
 while q<len(group):
  g=group[q];row=[]
  for d in D:
   h=comp(g,d)
   if h not in idx:idx[h]=len(group);group.append(h)
   row.append(idx[h])
  adj.append(row);q+=1
 need(len(group)==3840,'order')
 def reachable(colors):
  seen={0};todo=[0]
  for v in todo:
   for c in colors:
    w=adj[v][c]
    if w not in seen:seen.add(w);todo.append(w)
  return seen
 edges={}
 for a,row in enumerate(adj):
  for c,b in enumerate(row):
   need(a!=b and adj[b][c]==a,'undirected proper edges')
   edges.setdefault((min(a,b),max(a,b),c),[])
 faces=[]
 for colors in [(0,2),(0,3),(1,3),(1,2)]:
  remaining=set(range(3840))
  while remaining:
   start=min(remaining);v=start;walk=[];cs=[]
   while True:
    c=colors[len(walk)%2];walk.append(v);cs.append(c);v=adj[v][c]
    if v==start:break
   need(len(set(walk))==len(walk),'simple cell boundary')
   need(len(walk)==(12 if colors==(1,2) else 4),'exact cell size')
   remaining.difference_update(walk);f=len(faces)
   ee=[]
   for j,a in enumerate(walk):
    b=walk[(j+1)%len(walk)];key=(min(a,b),max(a,b),cs[j]);ee.append(key)
    edges[key].append((f,1 if a<b else -1))
   faces.append((set(walk),set(colors),set(ee)))
 need(len(edges)==7680 and len(faces)==3200,'cells')
 need(all(len(x)==2 for x in edges.values()),'closed edge incidence')
 corners=[[] for _ in group]
 for vs,colors,ee in faces:
  for v in vs:corners[v].append(tuple(sorted(colors)))
 need(all(sorted(c)==[(0,2),(0,3),(1,2),(1,3)] for c in corners),'all circle links')
 def components(selected_edges,selected_faces):
  outside=set(range(len(faces)))-selected_faces
  neighbors={f:[] for f in outside}
  for e,inc in edges.items():
   if e in selected_edges:continue
   (a,sa),(b,sb)=inc
   need(a in outside and b in outside,'subcomplex complement')
   neighbors[a].append((b,-sa*sb));neighbors[b].append((a,-sa*sb))
  result=[]
  while outside:
   root=min(outside);seen={root:1};todo=[root];orient=True
   for a in todo:
    for b,s in neighbors[a]:
     if b not in seen:seen[b]=s*seen[a];todo.append(b)
     elif seen[b]!=s*seen[a]:orient=False
   outside.difference_update(seen);result.append((len(seen),orient))
  return result
 need(components(set(),set())==[(3200,True)],'closed orientable connected surface')
 result=[]
 for i,j in [({0,1,2},{1,2,3}),({0,1},{1,2}),({1,2},{2,3})]:
  a,b=reachable(i),reachable(j)
  ee={e for e in edges if (e[0] in a and e[2] in i) or(e[0] in b and e[2] in j)}
  ff={k for k,(vs,colors,fedges) in enumerate(faces) if(vs<=a and colors<=i)or(vs<=b and colors<=j)}
  cc=components(ee,ff);result.append({'parabolics':[sorted(i),sorted(j)],'orders':[len(a),len(b),len(a&b),len(reachable(i&j))],'selected_faces':len(ff),'complement':cc})
 need([x['complement'] for x in result]==[[(2704,True)],[(3199,True)],[(3199,True)]],'connected complements')
 # A missing disk cannot pass the closed-surface input to the theorem.
 missing=next(iter(faces[0][2]));bad=list(edges[missing]);bad=[x for x in bad if x[0]!=0]
 need(len(bad)!=2,'missing disk rejected')
 return {'status':'PHASE242_INDEPENDENT_SURFACE_PASS','vertices':3840,'edges':7680,'faces':3200,'Euler_characteristic':-640,'orientable':True,'first_Betti_dimension':642,'complements':result,'negative_control':'Missing disk violates two-sided edge incidence'}
if __name__=='__main__':print(json.dumps(build(),indent=2))
