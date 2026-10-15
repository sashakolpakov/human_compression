"""Supplementary exact plane controls; not a proof of the uniform theorem."""
import sys
if sys.flags.optimize:raise RuntimeError('Normal Python is required')
from pathlib import Path
import json
I=((1,0,0),(0,1,0),(0,0,1))
def need(b,m):
 if not b:raise ValueError(m)
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(3))for j in range(3))for i in range(3))
def linear(a):return tuple(tuple(a[i][j]for j in range(2))for i in range(2))
def order(a):
 x=I
 for k in range(1,13):
  x=mul(x,a)
  if x==I:return k
 return None
def run():
 cases=[('affine_A2',(((0,-1,1),(-1,0,1),(0,0,1)),((-1,1,0),(0,1,0),(0,0,1)),((1,0,0),(1,-1,0),(0,0,1)))),('affine_C2',(((-1,0,1),(0,1,0),(0,0,1)),((0,1,0),(1,0,0),(0,0,1)),((1,0,0),(0,-1,0),(0,0,1))))]
 rows=[]
 for name,gs in cases:
  need(all(mul(s,s)==I for s in gs),'involutions')
  elements={I:I};front=[I]
  for _ in range(5):
   next_front=[]
   for g in front:
    for s in gs:
     h=mul(g,s)
     if h not in elements:elements[h]=mul(s,elements[g]);next_front.append(h)
   front=next_front
  nonparallel=parallel=minus=preserving=0;orders={};point_parts=set()
  for g,iv in elements.items():
   need(mul(g,iv)==I and mul(iv,g)==I,'exact inverse')
   point_parts.add(linear(g));all_parallel=True
   for s in gs:
    conjugate=mul(mul(g,s),iv);c=mul(conjugate,s)
    if linear(conjugate)!=linear(s):
     all_parallel=False;nonparallel+=1;k=order(c);need(k is not None and k>1,'nonparallel product finite nonidentity')
     orders[k]=orders.get(k,0)+1
    else:
     parallel+=1;need(linear(c)==((1,0),(0,1)),'parallel product translation')
   if all_parallel:
    preserving+=1;need(linear(g)in [((1,0),(0,1)),((-1,0),(0,-1))],'common sign')
    if linear(g)==((-1,0),(0,-1)):
     minus+=1;need(order(g)==2,'point inversion order two')
  need(nonparallel>0 and preserving>0,'nonvacuous controls')
  rows.append(dict(model=name,word_radius=5,elements=len(elements),linear_parts=len(point_parts),nonparallel_pairs=nonparallel,parallel_pairs=parallel,finite_orders=orders,preserves_all_wall_directions=preserving,point_inversions=minus))
 # Dimension-one conclusion, including translated mirrors and identity.
 line_cases=0
 for sign in [-1,1]:
  for b in range(-5,6):
   g=((sign,0,b),(0,1,0),(0,0,1))
   if sign==-1:need(order(g)==2,'dimension one negative sign')
   else:need(linear(g)==((1,0),(0,1)),'dimension one translation')
   line_cases+=1
 return dict(status='PASS_BOUNDED_REFLECTION_COMMUTATORS',models=rows,dimension_one_cases=line_cases,uniform_theorem_from_written_proof=True,whole_original_credit=0)
if __name__=='__main__':print(json.dumps(run(),indent=2))
