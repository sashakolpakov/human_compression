#!/usr/bin/env python3
"""Literal accepted affine models; new group-structure work only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import json,hashlib
HERE=Path(__file__).resolve().parent;STUDY=HERE.parent
I=((1,0,0),(0,1,0),(0,0,1));Z=(0,0,0)
W=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
def mv(A,v):return tuple(sum(x*y for x,y in zip(row,v)) for row in A)
def plane(A,v,s):
 ans=[]
 for i in range(4):
  w=mv(A,W[i]);e=1 if w in W else -1;j=W.index(tuple(e*x for x in w));num=e-1+2*sum(x*y for x,y in zip(W[j],v));
  if num%4:raise ValueError("nonintegral accepted plane action")
  for k in range(s):ans.append(j*s+(e*k+num//4)%s+1)
 return ans
R=[(((0,1,0),(1,0,0),(0,0,1)),Z),(((1,0,0),(0,0,1),(0,1,0)),Z),(((0,-1,0),(-1,0,0),(0,0,-1)),(0,0,1)),(((0,-1,0),(-1,0,0),(0,0,1)),Z)]
rows=[]
for s in [3,4,5,6]:
 qp=[]
 for j in range(3):
  A=tuple(tuple(((-1 if i==j else 1) if i==k else 0) for k in range(3)) for i in range(3));v=tuple(int(i==j) for i in range(3));qp.append(plane(A,v,s))
 qp += [plane(A,v,s) for A,v in R[:2]]
 roots=[(1,-1,0),(0,1,-1),(0,1,1)]
 rows.append(dict(row='T6.'+str(s-1),s=s,marking=[plane(A,v,s) for A,v in R],translation_basis=[plane(I,v,s) for v in roots],split_complement=qp,twice_coordinate=plane(I,(2,0,0),s)))
# A faithful 48-root action of the accepted linear Q. R1,R2,R3,R4 fix the origin.
roots=[]
for j in range(4):
 for e in [-1,1]:roots.append(tuple(F(e if i==j else 0) for i in range(4)))
roots += [tuple(F(x,2) for x in a) for a in product([-1,1],repeat=4)]
for i,j in combinations(range(4),2):
 for a,b in product([-1,1],repeat=2):roots.append(tuple(F(a if k==i else b if k==j else 0) for k in range(4)))
roots=sorted(set(roots))
if len(roots)!=48:raise ValueError("root count")
n=(1,-1,-1,-1)
R1=tuple(tuple(F(i==j)-F(n[i]*n[j],2) for j in range(4)) for i in range(4))
R2=tuple(tuple(F((-1 if i==3 else 1) if i==j else 0) for j in range(4)) for i in range(4))
def swap(i,j):return tuple(tuple(F(k== (j if h==i else i if h==j else h)) for k in range(4)) for h in range(4))
square=[R1,R2,swap(2,3),swap(1,2)]
perms=[[roots.index(mv(A,v))+1 for v in roots] for A in square]
f=HERE/'inputs/model_data.json';finite=json.loads(f.read_text())
obj={'cubic':rows,'square_linear':perms,'finite_models':finite['models'],'finite_data_binding':{'path':'topic_A_L121_application/finite/model_data.json','bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()},'scope':'Accepted marked models reused; no geometry or universal-presentation calculation repeated.'}
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
 args.out.write_text(json.dumps(obj,indent=2)+'\n')
