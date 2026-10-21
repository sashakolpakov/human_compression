import sys
if sys.flags.optimize: raise SystemExit('normal Python required')
from itertools import product,permutations
from pathlib import Path
import json

def mul(a,b):
 r=0
 for _ in range(2):
  if b&1:r^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return r

def add(xs):
 r=0
 for x in xs:r^=x
 return r

def h(v,w):return add(mul(mul(x,x),y)for x,y in zip(v,w))
def mm(A,B):return tuple(add(mul(A[3*i+k],B[3*k+j])for k in range(3))for i in range(3)for j in range(3))
def determinant(A):return add(mul(mul(A[p[0]],A[3+p[1]]),A[6+p[2]])for p in permutations(range(3)))
def norm(A):
 x=next(x for x in A if x);inv=next(y for y in range(1,4)if mul(x,y)==1);return tuple(mul(inv,y)for y in A)
I=(1,0,0,0,1,0,0,0,1)
vs=[v for v in product(range(4),repeat=3)if h(v,v)==1];su=[]
for a in vs:
 for b in vs:
  if h(a,b):continue
  for c in vs:
   if h(a,c)or h(b,c):continue
   A=a+b+c
   if determinant(A)==1:su.append(A)
assert len(su)==216 and len(set(su))==216
psu=set(map(norm,su));assert len(psu)==72
inv=[A for A in psu if A!=I and norm(mm(A,A))==I];assert len(inv)==9
pairs=0
for a in inv:
 for b in inv:
  if a==b:continue
  assert norm(mm(a,b))!=norm(mm(b,a));pairs+=1
# Exhaust the four-interval elementary commutation identity in literal S4.
pp=list(permutations(range(4)));one=tuple(range(4))
def pm(a,b):return tuple(a[b[i]]for i in range(4))
count=0
for B in pp:
 if pm(B,B)!=one:continue
 for A in pp:
  AB=pm(A,B)
  if pm(AB,AB)!=one:continue
  for C in pp:
   BC=pm(B,C);ABC=pm(AB,C)
   if pm(BC,BC)!=one or pm(ABC,ABC)!=one:continue
   assert pm(A,C)==pm(C,A);count+=1
r=dict(status='PASS_INDEPENDENT_LITERAL_UNITARY_AND_INTERVAL_IDENTITY',method='GF4 polynomial arithmetic, standard diagonal Hermitian form, no GAP/CAS/author imports',norm_one_vectors=len(vs),SU_order=len(su),PSU_order=len(psu),involutions=len(inv),distinct_pairs=pairs,S4_four_interval_triples=count)
Path('independent_unitary.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
