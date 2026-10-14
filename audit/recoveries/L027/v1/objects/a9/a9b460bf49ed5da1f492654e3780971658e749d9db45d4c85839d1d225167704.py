import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
from pathlib import Path
import json,itertools

def rank(rows,p):
 rows=[list(x)for x in rows];r=0
 for c in range(len(rows[0])):
  pivot=next((i for i in range(r,len(rows))if rows[i][c]%p),None)
  if pivot is None:continue
  rows[r],rows[pivot]=rows[pivot],rows[r];z=pow(rows[r][c]%p,-1,p);rows[r]=[(v*z)%p for v in rows[r]]
  for i in range(len(rows)):
   if i!=r:
    z=rows[i][c]%p;rows[i]=[(a-z*b)%p for a,b in zip(rows[i],rows[r])]
  r+=1
 return r

def run(p):
 e=1 if p%3==1 else 2
 one=(1,0);zero=(0,0)
 def add(a,b):return((a[0]+b[0])%p,(a[1]+b[1])%p)
 def neg(a):return((-a[0])%p,(-a[1])%p)
 def mul(a,b):return((a[0]*b[0]-a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0]-a[1]*b[1])%p)
 def pw(a,n):
  z=one
  while n:
   if n&1:z=mul(z,a)
   a=mul(a,a);n//=2
  return z
 w=(next(x for x in range(2,p)if(x*x+x+1)%p==0),0)if e==1 else(0,1);ww=mul(w,w)
 def flat(v):return[x for a in v for x in (a[:e])]
 def matmul(A,B):return[[sumf([mul(A[i][k],B[k][j])for k in range(len(B))])for j in range(len(B[0]))]for i in range(len(A))]
 def sumf(v):
  z=zero
  for a in v:z=add(z,a)
  return z
 I=[[one if i==j else zero for j in range(3)]for i in range(3)]
 def mpow(A,n):
  Z=I
  for _ in range(n):Z=matmul(Z,A)
  return Z
 def projective_identity(A):return all(A[i][j]==(A[0][0]if i==j else zero)for i in range(3)for j in range(3))
 result=[]
 for k in [1,-1]:
  kk=(k%p,0);t=mul(kk,add(add(w,w),one));v=[t,neg(t)];first=[]
  for j in range(3):first.append(flat(v));v=[mul(v[0],w),mul(v[1],ww)]
  assert rank(first,p)==2
  v=[neg(add(add(w,w),one)),w];point=[]
  for j in range(6):point.append(flat(v));v=[mul(v[0],w),mul(v[1],neg(ww))]
  assert rank(point,p)==2*e
  affine=[list(pw(w,j)[:e])for j in range(3)];assert rank(affine,p)==e
  a=[[one,zero,zero],[zero,w,zero],[zero,zero,ww]]
  b=[[neg(one),zero,neg(kk)],[zero,neg(ww),neg(mul(kk,ww))],[zero,zero,w]]
  c=[[one,kk,zero],[zero,kk,one],[zero,neg(one),zero]]
  d=[[zero,one,zero],[zero,zero,one],[one,zero,zero]]
  generators=[a,b,c,d]
  orders=[]
  for g in generators:
   orders.append(next(j for j in range(1,7)if projective_identity(mpow(g,j))))
  assert orders==[3,6,6 if k==1 else 3,3]
  for i in range(4):
   g=generators[i]
   for j in range(i+1,4):
    g=matmul(g,generators[j]);assert not projective_identity(g)and projective_identity(matmul(g,g))
  prefixes=[matmul(a,b),matmul(matmul(a,b),c),matmul(matmul(matmul(a,b),c),d)]
  equations=[]
  for g in prefixes:
   assert all(z[1]==0 for row in g for z in row)
   for i,j in itertools.product(range(3),repeat=2):
    row=[0]*9
    for r in range(3):row[3*i+r]+=g[r][j][0];row[3*r+j]-=g[i][r][0]
    equations.append(row)
  assert rank(equations,p)==8
  result.append({'sign':k,'first_module_dimension':2,'point_module_dimension':2*e,'affine_dimension':e,'centralizer_dimension':1,'orders':orders})
 return{'p':p,'field_order':p**e,'cases':result}
if __name__=='__main__':
 out={'status':'PASS_INDEPENDENT_LITERAL_FIELDS','fields':[run(p)for p in [5,7,11,13,17,19,31]],'scope':'Independent finite arithmetic and prime-field module ranks; uniform proof is reviewed separately.'};Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print({'status':out['status'],'fields':len(out['fields']),'markings':14})
