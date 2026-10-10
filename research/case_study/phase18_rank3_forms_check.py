#!/usr/bin/env python3
"""Exact form-space dimensions and frozen fold identities; no generation claim."""
from pathlib import Path
import hashlib,json,datetime
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parent

def basis(alternating=False):
 out=[]
 for i in range(4):
  for j in range(i+(1 if alternating else 0),4):
   b=S.zeros(4);b[i,j]=1
   if i!=j:b[j,i]=-1 if alternating else 1
   out.append(b)
 return out

def dimension(bs,conditions):
 mat=S.Matrix.hstack(*[S.Matrix.vstack(*[(g.T*b*g-m*b).reshape(16,1) for g,m in conditions]) for b in bs])
 sn=smith_normal_form(mat,domain=ZZ)
 nonzero=[abs(int(sn[i,i])) for i in range(min(sn.shape)) if sn[i,i]]
 assert all(x in (1,2) for x in nonzero),nonzero
 return len(bs)-len(nonzero)

sym,alt=basis(),basis(True)
weights=[(1,1),(1,-1),(-1,1),(-1,-1)]
count=0
for a in range(5):
 for b in range(5-a):
  for c in range(5-a-b):
   ds=[a,b,c,4-a-b-c]
   ws=[w for w,d in zip(weights,ds) for _ in range(d)]
   A=S.diag(*[w[0] for w in ws]);C=S.diag(*[w[1] for w in ws])
   expected=sum(d*(d+1)//2 for d in ds)
   assert dimension(sym,[(A,1),(C,1)])==expected
   assert expected==4 if ds==[1,1,1,1] else expected>=5
   count+=1
for r in (1,2,3):
 B=S.diag(*([-1]*r+[1]*(4-r)))
 assert dimension(sym,[(B,1)])==r*(r+1)//2+(4-r)*(5-r)//2
A=S.diag(1,1,-1,-1)
C=S.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
assert A*C==-C*A
assert dimension(alt,[(A,-1),(C,-1)])==3
assert dimension(alt,[(A,-1)])==4
h=S.symbols('h')
r0=S.Matrix([[0,1,1,0],[0,0,0,1],[-h,0,0,-1],[0,-h,0,0]])
r1=S.diag(1,1,-1,1)
r2=S.Matrix([[-1,0,0,0],[1,1,0,0],[-1,-2,-1,0],[0,1,1,1]])
r3=S.diag(-1,1,1,-1)
assert r0*r2==r2*r0 and r1*r3==r3*r1
assert r1*r3==S.diag(-1,1,-1,-1)
u1=S.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
u3=C
assert u1*u3==S.Matrix([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]])
assert u1*u3==u3*u1
result={
 'status':'PASS','executed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'proof_sha256':hashlib.sha256((ROOT/'phase18_rank3_forms.md').read_bytes()).hexdigest(),
 'joint_multiplicity_patterns':count,'middle_symmetric_types':3,
 'alternating_space_dimensions':[3,4],
 'nonzero_smith_factors':'only 1 or 2 in all dimension systems; no odd-characteristic rank loss',
 'fold_identities':'PASS, both frozen matrix patterns',
 'scope':'Exact finite templates establishing dimension formula diagnostics and fold identities; no finite generation or universal rank-three existence claim.'}
(ROOT/'phase18_rank3_forms_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
