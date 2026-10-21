"""Exact illustrative controls; the written proof supplies the general result."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from fractions import Fraction as F
from itertools import permutations,product
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def need(c,m):
 if not c:raise RuntimeError(m)
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def plus(a,b):return [[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r]for r in a]
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def rank(a):
 a=[list(map(F,r))for r in a];i=0
 for j in range(len(a[0])):
  k=next((k for k in range(i,len(a))if a[k][j]),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i];v=a[i][j];a[i]=[x/v for x in a[i]]
  for k in range(len(a)):
   if k!=i:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[i])]
  i+=1
 return i
def permute(a,p):return [[a[p[i]][p[j]]for j in range(len(p))]for i in range(len(p))]
# Two equivalent sign summands for C2. A is a positive square root on its
# image, yet B=A^2 does not commute with an invariant projection Q.
U=[[F(1),F(0)],[-F(1),F(0)],[F(0),F(1)],[F(0),-F(1)]]
A=scale(mul(mul(U,[[F(2),F(1)],[F(1),F(1)]]),tr(U)),F(1,2))
Q=scale([[U[i][0]*U[j][0]for j in range(4)]for i in range(4)],F(1,2))
B=mul(A,A);C=mul(mul(A,Q),A);D=mul(mul(A,plus(eye(4),scale(Q,-1))),A)
need(plus(C,D)==B,'sandwiched decomposition')
need(mul(B,Q)!=mul(Q,B),'control really is noncommuting')
need(rank(B)==2 and rank(C)==rank(D)==1,'proper positive pieces')
for M in [B,C,D]:
 need(M==tr(M) and permute(M,[1,0,3,2])==M and all(sum(row)==0 for row in M),'centered invariant pieces')
# Rational distance double-centering: all hollow symmetric matrices of
# degree3 with the displayed entries, including non-Euclidean examples.
J=plus(eye(3),[[F(-1,3)]*3 for _ in range(3)]);roundtrips=0
for a,b,c in product([-2,0,1,3],repeat=3):
 M=[[F(0),F(a),F(b)],[F(a),F(0),F(c)],[F(b),F(c),F(0)]]
 Gram=scale(mul(mul(J,M),J),F(-1,2))
 recovered=[[Gram[i][i]+Gram[j][j]-2*Gram[i][j]for j in range(3)]for i in range(3)]
 need(recovered==M and all(sum(r)==0 for r in Gram),'exact linear inverse')
 roundtrips+=1
# Equilateral triangle: designating rotations does not remove reflections.
full=[p for p in permutations(range(3))if permute(J,p)==J]
need(len(full)==6,'full triangle group is S3')
rotations=[(0,1,2),(1,2,0),(2,0,1)]
need(all(p in full for p in rotations)and len(full)>len(rotations),'prescribed subgroup is smaller')
# Faithful permutation representation does not force injectivity of the orbit.
constant=(1,1,1);orbit={tuple(constant[p[i]]for i in range(3))for p in permutations(range(3))}
need(len(orbit)==1,'full stabilizer can collapse an orbit')
# A combinatorial digon has two different edges with the same two vertices.
vertices=[-1,1];edges=[{0,1},{0,1}]
need(vertices[0]!=vertices[1] and {vertices[i]for i in edges[0]}=={vertices[i]for i in edges[1]},'vertex injection alone does not separate faces')
report=dict(status='PASS_DISTINCT_EXACT_REALIZATION_CONTROLS',noncommuting_projection=True,ranks=[rank(B),rank(C),rank(D)],hollow_distance_roundtrips=roundtrips,full_triangle_symmetries=len(full),designated_rotations=3,faithful_representation_collapsed_orbit=True,digon_faces_not_separated=True,general_mathematical_proof=False)
(P/'independent_controls.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
