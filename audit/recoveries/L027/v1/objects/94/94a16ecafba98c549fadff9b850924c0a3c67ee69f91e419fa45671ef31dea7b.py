import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
from pathlib import Path
import itertools,json
O=Path(__file__).parent
reports=[]
for degree,polynomial in [(2,7),(3,11)]:
 q=1<<degree
 def mul(a,b):
  z=0
  while b:
   if b&1:z^=a
   b>>=1;a<<=1
   if a&q:a^=polynomial
  return z
 def plus(values):
  z=0
  for x in values:z^=x
  return z
 def mm(A,B):return tuple(plus(mul(A[3*i+k],B[3*k+j]) for k in range(3))for i in range(3)for j in range(3))
 I=(1,0,0,0,1,0,0,0,1)
 def elem(i,j,a):
  x=list(I);x[3*i+j]^=a;return tuple(x)
 def module(seed,a,b):
  V={seed,(0,0)};changed=True
  while changed:
   old=set(V)
   for x,y in old:V.add((x^mul(a,y),y));V.add((x,y^mul(b,x)))
   for x in old:
    for y in old:V.add((x[0]^y[0],x[1]^y[1]))
   changed=V!=old
  return V
 rows=[]
 for a,b in itertools.product(range(1,q),repeat=2):
  t=mul(a,b);K={0,1}
  while True:
   new=K|{x^y for x in K for y in K}|{mul(t,x)for x in K}
   if new==K:break
   K=new
  L=module((0,1),a,b);R=module((1,0),a,b)
  assert L=={(mul(a,x),y)for x in K for y in K}
  assert R=={(x,mul(b,y))for x in K for y in K}
  assert (L==R)==(a in K)
  assert len(L&R)==(len(K)**2 if a in K else 1)
  rows.append([a,b,len(K),len(L&R)])
 # Enumerate every elation without importing the author/GAP code.
 vectors=[]
 for v in itertools.product(range(q),repeat=3):
  nonzero=next((x for x in v if x),None)
  if nonzero==1:vectors.append(v)
 elations=set()
 for u in vectors:
  for f in itertools.product(range(q),repeat=3):
   if not any(f)or plus(mul(u[i],f[i])for i in range(3)):continue
   elations.add(tuple(I[3*i+j]^mul(u[i],f[j])for i in range(3)for j in range(3)))
 a=2;b=next(x for x in range(1,q)if mul(a,x)==1)
 marks=[elem(1,2,1),elem(2,0,a),elem(0,2,b),elem(1,0,1)]
 commuting=[g for g in elations if all(mm(g,h)==mm(h,g)for h in marks[:3])]
 assert not commuting
 reports.append(dict(q=q,modules=rows,elations=len(elations),possible_fifth_marks=len(commuting)))
(O/'independent.json').write_text(json.dumps(dict(status='PASS_NO_AUTHOR_IMPORT',fields=reports,scope='Independent literal module and fifth-elation controls; not a universal proof or target census'),indent=2)+'\n');print([(x['q'],len(x['modules']),x['elations'])for x in reports])
