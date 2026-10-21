import itertools,json
from pathlib import Path
def perm(n,cycles):
 p=list(range(n))
 for a,b in cycles:p[a-1],p[b-1]=p[b-1],p[a-1]
 return tuple(p)
def check(n,cycles,anchors):
 t=[perm(n,c)for c in cycles];a,b,c=t;assert all(p[p[x]]==x for p in t for x in range(n));assert all(a[c[x]]==c[a[x]]for x in range(n))
 u,v=0,n-1;assert a[u]!=u and c[u]==u and c[v]!=v and a[v]==v
 if anchors:assert b[u]==u and b[v]==v
 else:assert b[v]!=v
 seen={0};todo=[0]
 while todo:
  for p in t:
   q=p[todo[-1]]
   if q not in seen:seen.add(q);todo.insert(0,q)
  todo.pop()
 assert len(seen)==n
 return {'degree':n,'both_anchors':anchors,'transitive':True}
rows=[check(4,[[(1,2)],[(2,3)],[(3,4)]],True),check(8,[[(1,2),(3,4),(5,6)],[(2,3),(4,7),(5,6)],[(3,5),(4,6),(7,8)]],True),check(7,[[(1,2),(3,4)],[(2,3),(4,6),(5,7)],[(6,7)]],False)]
print(json.dumps({'status':'PASS_NONVACUOUS_BOUNDARY_CONTROLS','cases':rows}))
