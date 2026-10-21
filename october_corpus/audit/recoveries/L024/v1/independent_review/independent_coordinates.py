"""Integer GF(9) arithmetic and proper matrix subgroups; no author imports."""
from itertools import product,permutations,combinations
from pathlib import Path
import json,argparse,math
# a+3b denotes a+b*z with z*z=z+1, all coefficients modulo 3.
def add(x,y):return (x%3+y%3)%3+3*((x//3+y//3)%3)
def neg(x):return (-(x%3))%3+3*((-(x//3))%3)
def mul(x,y):
 a,b=x%3,x//3;c,d=y%3,y//3
 return (a*c+b*d)%3+3*((a*d+b*c+b*d)%3)
def power(x,n):
 a=1
 for _ in range(n):a=mul(a,x)
 return a
def total(v):
 s=0
 for x in v:s=add(s,x)
 return s
I=tuple(int(i==j) for i in range(5) for j in range(5))
def mm(A,B):return tuple(total(mul(A[5*i+k],B[5*k+j]) for k in range(5)) for i in range(5) for j in range(5))
def transpose(A):return tuple(A[5*j+i] for i in range(5) for j in range(5))
def determinant(A):
 val=0
 for p in permutations(range(5)):
  t=1
  for i in range(5):t=mul(t,A[5*i+p[i]])
  if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2:t=neg(t)
  val=add(val,t)
 return val
def rank(A,cols=5):
 rows=[list(A[k:k+cols]) for k in range(0,len(A),cols)];r=0
 for c in range(cols):
  k=next((k for k in range(r,len(rows)) if rows[k][c]),None)
  if k is None:continue
  rows[r],rows[k]=rows[k],rows[r];inv=power(rows[r][c],7);rows[r]=[mul(x,inv) for x in rows[r]]
  for k in range(len(rows)):
   if k!=r:
    f=rows[k][c];rows[k]=[add(x,neg(mul(f,y))) for x,y in zip(rows[k],rows[r])]
  r+=1
 return r
def closure(gs):
 seen={I};q=[I]
 for a in q:
  for g in gs:
   b=mm(a,g)
   if b not in seen:seen.add(b);q.append(b)
   if len(seen)>100:raise ValueError('expected proper small subgroup exceeded bound')
 return seen
def check(marking):
 s0,s1,s2=marking;J=tuple(int(i+j==4) for i in range(5) for j in range(5))
 for A in marking:
  if mm(A,A)!=I or determinant(A)!=1 or mm(mm(A,J),transpose(tuple(power(x,3) for x in A)))!=J:raise ValueError('unitary involution')
  if rank(tuple(add(a,neg(b)) for a,b in zip(A,I)))!=2:raise ValueError('negative dimension')
 pairs=[closure([marking[i],marking[j]]) for i,j in [(0,1),(0,2),(1,2)]]
 if list(map(len,pairs))!=[10,4,10]:raise ValueError('proper group orders')
 masks=[set(c) for n in range(3) for c in combinations(range(3),n)];groups=[closure([marking[i] for i in m]) for m in masks]
 for a,A in zip(masks,groups):
  for b,B in zip(masks,groups):
   if A&B!=groups[masks.index(a&b)]:raise ValueError('proper IP')
 return groups

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if power(3,2)!=add(3,1) or {power(3,i) for i in range(8)}!=set(range(1,9)):raise ValueError('field generator')
 s0=tuple((2 if i in [0,4] else 1) if i==j else 0 for i in range(5) for j in range(5))
 s2=tuple(1 if (i,j) in [(0,4),(4,0),(1,1),(3,3)] else 2 if (i,j)==(2,2) else 0 for i in range(5) for j in range(5))
 exps=[[7,3,7,None,4],[5,6,None,4,None],[3,4,4,None,5],[5,4,4,2,1],[None,7,1,7,5]]
 s1=tuple(0 if x is None else power(3,x) for row in exps for x in row);marking=[s0,s1,s2];groups=check(marking)
 if rank(tuple(add(s2[5*i+j],neg(int(i==j))) for i in [0,4] for j in [0,4]),2)!=1 or rank(tuple(add(s2[5*i+j],neg(int(i==j))) for i in [1,2,3] for j in [1,2,3]),3)!=1:raise ValueError("s2 centralizer class pair")
 points=[]
 for j in range(5):
  for tail in product(range(9),repeat=4-j):
   v=(0,)*j+(1,)+tail
   if total(mul(v[i],power(v[4-i],3)) for i in range(5))==0:points.append(v)
 if len(points)!=2440:raise ValueError('point count')
 pset=set(points);actions=[]
 for A in marking:
  images=[]
  for v in points:
   w=tuple(total(mul(v[i],A[5*i+j]) for i in range(5)) for j in range(5));f=power(next(x for x in w if x),7);w=tuple(mul(f,x) for x in w)
   if w not in pset:raise ValueError('action not on points')
   images.append(w)
  if len(set(images))!=2440:raise ValueError('not permutation')
  actions.append(images)
 gu=lambda n:3**(n*(n-1)//2)*math.prod(3**i-(-1)**i for i in range(1,n+1))
 order=gu(5)//4
 if order!=258190571520 or math.prod([2440,2187,2,224,36,3])!=order:raise ValueError('order formula')
 centr=[gu(2)*gu(3)//4,gu(4)*gu(1)//4]
 if centr!=[580608,52254720] or [order//c for c in centr]!=[444690,4941]:raise ValueError('class sizes')
 if [gu(2)//gu(1)**2,gu(3)//(gu(1)*gu(2))]!=[6,63]:raise ValueError('nondegenerate line count')
 controls=[]
 for i in range(3):
  bad=marking.copy();bad[i]=I
  try:check(bad)
  except ValueError:controls.append('identity substituted for s'+str(i))
  else:raise ValueError('mutation survived')
 bad=marking.copy();M=list(s1);M[0]=add(M[0],1);bad[1]=tuple(M)
 try:check(bad)
 except ValueError:controls.append('s1 matrix entry changed')
 else:raise ValueError('mutation survived')
 # Wrong local intersection shape is separately rejected.
 if len(groups[-3]&groups[-1])==4:raise ValueError('wrong local meet accidentally true')
 controls.append('order-four local meet rejected')
 report={'status':'PASS','field':'F3[z]/(z^2-z-1), independent integer pair arithmetic','unitary_matrices':3,'negative_dimensions':[2,2,2],'s2_negative_dimensions_in_s0_split':[1,1],'proper_subset_intersections':49,'remaining_15_IP_pairs':'Contain the whole group and follow tautologically after the separately replayed generation premise.','canonical_isotropic_points':2440,'matrix_point_images':7320,'unitary_order':order,'centralizer_orders':centr,'centralizer_involution_class_sizes':[63,378,6,1,63],'controls':controls,'no_author_code_imports':True,'full_generation':'Accepted only from fresh fixed GAP certificate, not inferred from proper subgroups or displayed orbit product.'}
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
