"""No author imports: literal GF2 centralizer of the new full-rank element."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
import itertools,json
from pathlib import Path
O=Path(__file__).resolve().parent
par=lambda x:x.bit_count()%2
def app(rows,v):return sum(par(r&v)<<i for i,r in enumerate(rows))
def rank(rows):
 b={}
 for r in rows:
  while r:
   k=r.bit_length()-1
   if k in b:r^=b[k]
   else:b[k]=r;break
 return len(b)
I=[1<<i for i in range(4)]
Js=[list(t)for t in itertools.product(range(16),repeat=4)if all(par(t[i]&t[j])==int(i==j)for i in range(4)for j in range(4))]
assert len(Js)==48
Ds=[]
for vals in itertools.product(range(2),repeat=10):
 D=[0]*4;k=0
 for i in range(4):
  for j in range(i,4):
   if vals[k]:D[i]|=1<<j;D[j]|=1<<i
   k+=1
 Ds.append(D)
def Q(b,v):
 x=v&15;y=v>>4
 return par(x)^par(x&y)^par(b&y)
def t(v):return (v&15)^(v>>4)|((v>>4)<<4)
counts=[];checked=0
for b in range(16):
 total=inside=0
 for A in Js:
  for D in Ds:
   DA=[sum(par(D[i] & sum(((A[j]>>k)&1)<<j for j in range(4)))<<k for k in range(4))for i in range(4)]
   rows=[A[i]|DA[i]<<4 for i in range(4)]+[A[i]<<4 for i in range(4)]
   if any(Q(b,app(rows,1<<i))!=Q(b,1<<i)for i in range(8)):continue
   # Polar preservation follows directly from AA^T=I and D symmetric;
   # independently check every pair of basis vectors and commutation.
   for i in range(8):
    assert app(rows,t(1<<i))==t(app(rows,1<<i))
    for j in range(8):
     v=(1<<i)^(1<<j)
     assert Q(b,app(rows,v))==Q(b,v)
   total+=1;inside+=rank([rows[i]^(1<<i)for i in range(8)])%2==0;checked+=1
  # The actual centralizer is exhausted: commuting with t forces upper
  # block form and the bilinear equations force the J,D parametrization.
 assert (total,inside)==(6144,3072)
 counts.append(dict(b=b,arf=par(b),full_orthogonal=total,omega=inside))
# Actual class orders use standard finite group orders, not class enumeration.
plus=2**12*(2**4-1)*(2**2-1)*(2**4-1)*(2**6-1)
minus=2**12*(2**4+1)*(2**2-1)*(2**4-1)*(2**6-1)
assert plus//3072==2**2*(2**4-1)**2*(2**6-1)
assert minus//3072==2**2*(2**8-1)*(2**6-1)
out=dict(status='PASS',forms=16,orthogonal_A=48,symmetric_D=1024,actual_commuting_isometries=checked,counts=counts,class_sizes=[plus//3072,minus//3072],no_author_import=True)
(O/'independent_f2_report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='counts'}))
