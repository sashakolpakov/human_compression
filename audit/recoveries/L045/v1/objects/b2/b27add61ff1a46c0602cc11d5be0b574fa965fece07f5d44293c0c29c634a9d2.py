"""Independent E7 root-automorphism centralizers, without GAP or author imports."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from pathlib import Path
import json,sympy as s,time
W=Path(__file__).resolve().parent
start=time.monotonic()
def need(x,m):
 if not x:raise ValueError(m)
A=[[2*int(i==j)for j in range(7)]for i in range(7)]
for i,j in [(0,1),(1,2),(2,3),(3,4),(4,5),(2,6)]:A[i][j]=A[j][i]=-1
R={tuple(int(i==j)for i in range(7))for j in range(7)};todo=list(R)
for v in todo:
 for i in range(7):
  z=list(v);z[i]-=sum(a*b for a,b in zip(A[i],v));z=tuple(z)
  if z not in R:R.add(z);todo.append(z)
need(len(R)==126,'complete E7 reflection orbit')
roots=sorted(R);allroots=s.Matrix.hstack(*(s.Matrix(v)for v in roots));cases=[]
for row in json.loads((W/'replay01/lattice/report.json').read_text())['cases']:
 if not row['name'].startswith('E7'):continue
 need(set(map(tuple,row['roots']))==R,'literal E7 roots independently generated')
 M=s.Matrix(row['matrix']);basis=None
 for v in roots:
  cols=[s.Matrix(v)]
  for j in range(6):cols.append(M*cols[-1])
  V=s.Matrix.hstack(*cols)
  if V.det()!=0:basis=v;break
 need(basis is not None,'cyclic root fixes linear centralizer map')
 inverse=V.inv();accepted=[]
 for z in roots:
  cols=[s.Matrix(z)]
  for j in range(6):cols.append(M*cols[-1])
  C=s.Matrix.hstack(*cols)*inverse
  if C*M!=M*C:continue
  images=C*allroots
  if {tuple(images[:,i])for i in range(126)}!=R:continue
  accepted.append([[int(x)for x in rr]for rr in C.tolist()])
 e=18 if row['name']=='E7order18' else 14
 powers=[];C=s.eye(7)
 for i in range(e):powers.append([[int(x)for x in rr]for rr in C.tolist()]);C=C*M
 need(C==s.eye(7) and len(accepted)==e and {str(x)for x in accepted}=={str(x)for x in powers},'centralizer is precisely cyclic powers')
 cases.append(dict(name=row['name'],cyclic_root=basis,candidate_images=126,centralizer_order=len(accepted),matrices=accepted))
need(len(cases)==2,'both exact E7 torus types')
r=dict(status='PASS_INDEPENDENT_E7_ROOT_CENTRALIZERS',method='A commuting linear map is determined by the image of one cyclic root; test all126 possible root images. E7 has no Dynkin diagram automorphism, hence its root automorphism group is its Weyl group.',cases=cases,seconds=time.monotonic()-start)
(W/'independent_weyl.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k!='cases'}));print([(c['name'],c['centralizer_order'])for c in cases])
