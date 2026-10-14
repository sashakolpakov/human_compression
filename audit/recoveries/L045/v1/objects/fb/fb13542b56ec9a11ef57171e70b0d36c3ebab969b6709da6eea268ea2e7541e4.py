"""Distinct controls: no import from the author packet."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from pathlib import Path
from itertools import product
from math import prod
from fractions import Fraction
import json
W=Path(__file__).resolve().parent

def need(b,s):
 if not b:raise ValueError(s)
def mul(a,b,q):
 if q==2:return a*b
 r=0
 while b:
  if b&1:r^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return r
def dot(a,b,q):
 z=0
 for x,y in zip(a,b):z^=mul(x,y,q)
 return z
def symporder(d,q):return q**(d*d)*prod(q**(2*i)-1 for i in range(1,d+1))
rows=[]
for q in (2,4):
 for k in range(1,5):
  vs=[v for v in product(range(q),repeat=k) if dot(v,v,q)==1]
  nodes=[0]
  def walk(selected,candidates):
   nodes[0]+=1
   if len(selected)==k:return 1
   return sum(walk(selected+[v],[u for u in candidates if dot(u,v,q)==0]) for v in candidates)
  actual=walk([],vs)
  expected=symporder((k-1)//2,q) if k%2 else q**(k-1)*symporder((k-2)//2,q)
  need(actual==expected,'actual symmetric bilinear isometries')
  rows.append(dict(q=q,k=k,actual=actual,nodes=nodes[0]))

def gu(n,q):return q**(n*(n-1)//2)*prod(q**i-(-1)**i for i in range(1,n+1))
unitary=[]
for q in (3,7,11,19,23,27,31,43,47,59,71):
 N=q+1;center=[j*N//4 for j in range(4)]
 multisets=set()
 for a in range(N):
  if (2*a)%N not in center:continue
  for k in (1,2,3):
   v=tuple(sorted([a]*k+[(a+N//2)%N]*(4-k)))
   if sum(v)%N==0:multisets.add(v)
 classes={min(tuple(sorted((a+c)%N for a in v)) for c in center) for v in multisets}
 sizes=[]
 for v in sorted(classes):
  vals=sorted(set(v));need(len(vals)==2,'noncentral eigenvalues')
  k=v.count(vals[0]);scalar_stab=sum(tuple(sorted((a+c)%N for a in v))==v for c in center)
  ambient=Fraction(gu(4,q),gu(k,q)*gu(4-k,q));sizes.append(int(ambient/scalar_stab))
 actual=sum(sizes)
 expected=q**4*(q*q-q+1)*(q*q+1)//2+(q**3*(q-1)*(q*q+1) if q%8==7 else 0)
 need(actual==expected and actual<Fraction(q**8,2),'projective scalar fusion count')
 need(len(classes)==(2 if q%8==7 else 1),'all norm-one scalar families')
 unitary.append(dict(q=q,lift_classes=len(multisets),projective_families=len(classes),sizes=sizes,involutions=actual))
r=dict(status='PASS_DISTINCT_CLASSICAL_CONTROLS',symmetric_isometry_rows=rows,unitary_scalar_fusion_rows=unitary,limitations='Finite controls supplement the full reviewed proof. Non-norm-one eigenspaces for q=3 mod8 are excluded by the separate written determinant argument; no character-table or author code imported.')
(W/'independent_controls.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
