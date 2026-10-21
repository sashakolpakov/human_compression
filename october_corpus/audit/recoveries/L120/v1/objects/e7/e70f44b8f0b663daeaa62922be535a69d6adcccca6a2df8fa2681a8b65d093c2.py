"""Independent finite checks; no author imports and no uniform proof premise."""
import itertools,json,math,sys
from pathlib import Path
if sys.flags.optimize:raise RuntimeError('unoptimized required')
def need(x,m):
 if not x:raise ValueError(m)
def mul(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inv(a):return tuple(a.index(i) for i in range(len(a)))
def close(gens,n):
 one=tuple(range(n));out={one};todo=[one]
 while todo:
  x=todo.pop()
  for y in gens:
   z=mul(x,y)
   if z not in out:out.add(z);todo.append(z)
 return out
def even(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2==0
def group_control(n,alt):
 G=set(p for p in itertools.permutations(range(n)) if not alt or even(p));one=tuple(range(n));cyclicnormal=[]
 for x in G-{one}:
  C=close([x],n)
  if all(mul(mul(g,x),inv(g)) in C for g in G):cyclicnormal.append(len(C))
 need(not cyclicnormal,'hypothesis independent verification')
 invol=[p for p in G-{one} if mul(p,p)==one];triples=0;ipchecks=0
 for a,c in itertools.permutations(invol,2):
  if mul(a,c)!=mul(c,a):continue
  for b in invol:
   if b in [a,c] or close([a,b,c],n)!=G:continue
   triples+=1;t=[a,b,c];subs=[close([t[i] for i in range(3) if k>>i&1],n) for k in range(8)]
   for i in range(8):
    for j in range(8):need(subs[i]&subs[j]==subs[i&j],'all subset IP');ipchecks+=1
 return {'group':('A' if alt else 'S')+str(n),'order':len(G),'involutions':len(invol),'qualifying_triples':triples,'IP_checks':ipchecks,'cyclic_normal_subgroups':0}
def field_control(q):
 W=[v for v in itertools.product(range(q),repeat=4) if sum(v)%q==0];perms=list(itertools.permutations(range(4)))
 action=lambda v,p:tuple(v[p[i]] for i in range(4))
 signatures={tuple(action(v,p) for v in W) for p in perms};need(len(signatures)==24,'literal W action faithful')
 nonzero=[v for v in W if any(v)]
 def norm(v):
  a=next(x for x in v if x);return tuple(x*pow(a,-1,q)%q for x in v)
 points={norm(v) for v in nonzero};fixed=[v for v in points if all(norm(action(v,p))==v for p in perms)]
 if q==2:need((1,1,1,1) in fixed,'even action reducible')
 else:
  need(not fixed,'no invariant line')
  # Dot product on W has Gram I+J, determinant4; lines and planes are dual.
  basis=[tuple(int(j==i)-int(j==3) for j in range(4)) for i in range(3)]
  gram=[[sum(x*y for x,y in zip(a,b))%q for b in basis] for a in basis]
  det=sum((-1 if sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2 else 1)*math.prod(gram[i][p[i]] for i in range(3)) for p in itertools.permutations(range(3)))%q
  need(det==4,'nondegenerate invariant dot form')
  need(q*(q*q-1)//2==60>24,'Omega obstruction')
 return {'q':q,'vectors':len(W),'projective_points':len(points),'faithful_images':len(signatures),'fixed_projective_points':len(fixed)}
out={'status':'PASS','groups':[group_control(4,False),group_control(4,True),group_control(5,True)],'modules':[field_control(2),field_control(5)],'uniform_proof_premise':False}
Path('independent_report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
