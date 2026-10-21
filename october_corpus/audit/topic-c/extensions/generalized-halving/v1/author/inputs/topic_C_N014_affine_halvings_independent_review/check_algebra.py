"""Independent exact homogeneous-matrix/normal-orbit diagnostic; no author imports.
Finite tests supplement a separate complete written proof review.
"""
from collections import deque
from fractions import Fraction
from pathlib import Path
import argparse,itertools,json,hashlib
from sympy import Matrix,eye
from sympy.matrices.normalforms import hermite_normal_form

def need(x,s):
 if not x:raise ValueError(s)
def affine(n,A=None,v=None):
 m=eye(n+1)
 if A is not None:m[:n,:n]=A
 if v is not None:m[:n,n]=Matrix(v)
 return m

def product(ms,n):
 r=eye(n+1)
 for m in ms:r=r*m
 return r

def translation(m,n):
 need(m[:n,:n]==eye(n),'pure translation')
 return tuple(int(x) for x in m[:n,n])

def normal_orbit(v,even):
 n=len(v);seen={v};todo=deque([v])
 while todo:
  x=todo.popleft();ys=[]
  for i in range(n-1):
   y=list(x);y[i],y[i+1]=y[i+1],y[i];ys.append(tuple(y))
  y=list(x);y[-1]*=-1
  if even:y[-2]*=-1
  ys.append(tuple(y))
  for y in ys:
   if y not in seen:seen.add(y);todo.append(y)
 return sorted(seen)

def lattice(vs):return hermite_normal_form(Matrix.hstack(*(Matrix(v) for v in vs)))
def intersect_even(B):
 n=B.rows;bits=[sum(int(x) for x in B[:,j])%2 for j in range(n)]
 if not any(bits):return hermite_normal_form(B)
 j=bits.index(1)
 return hermite_normal_form(Matrix.hstack(2*B[:,j],*(B[:,i]-bits[i]*B[:,j] for i in range(n) if i!=j)))

def solve_case(n,s,k,cache):
 S,Z,a,x,y=cache
 if k==1:
  q=product([x]+[S[i] for i in range(2,n)]+[Z[n]]+[S[i] for i in range(n-1,1,-1)]+[S[1]],n)
  q2=product([x]+[S[i] for i in range(2,n)]+[y]+[S[i] for i in range(n-2,1,-1)]+[S[1]],n)
  power=s if s%2==0 else 2*s
  v=[s]+[0]*(n-1);B=s*eye(n)
 elif k==2:
  A=product([S[i] for i in range(2,n)]+[Z[n]]+[S[i] for i in range(n-1,1,-1)],n)
  A2=product([S[i] for i in range(2,n)]+[y]+[S[i] for i in range(n-2,1,-1)],n)
  q=x*A*S[1]*A;q2=x*A2*S[1]*A2
  if n==3:
   literal=x*S[2]*S[1]*y*S[1]*S[2];need(literal==q2,'source Proposition5.12 special word')
  power=s;v=[s,s]+[0]*(n-2)
  cols=[Matrix([1 if j==i else -1 if j==i-1 else 0 for j in range(n)]) for i in range(1,n)]
  B=Matrix.hstack(Matrix([1,1]+[0]*(n-2)),*cols)*s
 else:
  q=product([x]+[S[i] for i in range(2,n)]+[Z[n],S[1]]+[S[i] for i in range(2,n)]+[Z[n]],n)
  q2=product([x]+[S[i] for i in range(2,n)]+[S[1]]+[S[i] for i in range(2,n-1)]+[y],n)
  u=product([a]+[S[i] for i in range(1,n)]+[Z[n]],n)
  need(q==u*u and q2==u*u,'literal both kn words are u squared')
  power=n*s//2 if n*s%2==0 else n*s;v=[s]*n
  B=Matrix.hstack(*(2*s*eye(n)[:,i] for i in range(n-1)),Matrix(v))
 L=intersect_even(B);expected_index=(s**n//2 if s%2==0 else s**n) if k==1 else s**n if k==2 else (2**(n-2)*s**n if n*s%2==0 else 2**(n-1)*s**n)
 need(abs(int(L.det()))//2==expected_index,'independent period intersection index')
 ans=[]
 for even,m in [(False,q),(True,q2)]:
  t=translation(m**power,n);R=lattice(normal_orbit(t,even));inclusion=L.inv()*R
  need(all(z.q==1 for z in inclusion),'normal relator lattice lies in intended period')
  f=abs(int(R.det()))//abs(int(L.det()));expected=2**(n-1) if (k==1 and s%2 or k==n and n*s%2) else 2 if even and k==n and n%2==0 else 1
  need(f==expected,'exact missing factor')
  ans.append({'operation':2 if even else 1,'literal_relator_vector':list(t),'normal_lattice_HNF':list(R),'period_HNF':list(L),'D_period_index':expected_index,'presented_over_intended_factor':f})
 return {'n':n,'s':s,'k':k,'cases':ans}

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();rows=[];pairs=0
 for n in range(3,8):
  S={};Z={}
  for i in range(1,n):
   A=eye(n);A[i-1,i-1]=A[i,i]=0;A[i-1,i]=A[i,i-1]=1;S[i]=affine(n,A)
  for i in range(1,n+1):A=eye(n);A[i-1,i-1]=-1;Z[i]=affine(n,A)
  ar=affine(n,Z[1][:n,:n],[1]+[0]*(n-1));x=ar*S[1]*ar;y=Z[n]*S[n-1]*Z[n]
  old=[ar]+[S[i] for i in range(1,n)]+[Z[n]]
  # Old Coxeter matrix; endpoint doubling deduced independently at the level of generators.
  E=[[1 if i==j else (4 if {i,j} in [{0,1},{n-1,n}] else 3 if abs(i-j)==1 else 2) for j in range(n+1)] for i in range(n+1)]
  first=[x]+old[1:];E1=[r[:] for r in E]
  for j in range(1,n+1):E1[0][j]=E1[j][0]=2 if j==1 else E[1][j]
  second=first[:-1]+[y];E2=[r[:] for r in E1]
  for j in range(n):E2[n][j]=E2[j][n]=2 if j==n-1 else E1[n-1][j]
  for gens,exps in [(old,E),(first,E1),(second,E2)]:
   for i in range(n+1):
    need(gens[i]**2==eye(n+1),'actual involutions')
    for j in range(i):
     need((gens[i]*gens[j])**exps[i][j]==eye(n+1),'actual Coxeter pair');pairs+=1
  for s in range(2,7):
   for k in [1,2,n]:rows.append(solve_case(n,s,k,(S,Z,ar,x,y)))
 # Explicit weakened choices, rejected at actual arithmetic conditions.
 controls=[]
 def reject(name,fn):
  try:fn()
  except ValueError:controls.append(name);return
  raise ValueError('mutation accepted '+name)
 z=next(r for r in rows if r['n']==4 and r['s']==2 and r['k']==4)['cases'][1]
 reject('full signed orbit cannot replace even signed orbit',lambda:need(z['presented_over_intended_factor']==1,'even orbit has missing factor2'))
 z=next(r for r in rows if r['n']==3 and r['s']==3 and r['k']==1)['cases'][0]
 reject('odd period source presentation is complete',lambda:need(z['presented_over_intended_factor']==1,'odd factor4'))
 reject('odd period may be intersected trivially with D',lambda:need(intersect_even(3*eye(3))==3*eye(3),'odd-period intersection doubles index'))
 z=next(r for r in rows if r['n']==3 and r['s']==3 and r['k']==3)['cases'][1]
 reject('odd-n all-one orbit has even-n index defect',lambda:need(z['presented_over_intended_factor']==2,'odd case factor4 instead'))
 out={'status':'PASS_INDEPENDENT_FINITE_ALGEBRA_DIAGNOSTIC','author_imports':False,'uniform_proof_claim_from_samples':False,'parameter_triples':len(rows),'literal_extra_relations':2*len(rows),'Coxeter_pair_checks':pairs,'controls':controls,'rows':rows}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,default=int)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
if __name__=='__main__':main()
