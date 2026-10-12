#!/usr/bin/env python3
"""Optional exact symbolic diagnostics; not a proof of uniform dimension claims."""
import argparse,json
from pathlib import Path
import sympy as s
u=s.symbols('u',nonzero=True)
checks=[]
def norm(X,p=0):
 def f(v):
  v=s.cancel(v)
  if not p:return v
  a,b=s.fraction(v)
  return s.cancel(s.Poly(a,u,modulus=p).as_expr()/s.Poly(b,u,modulus=p).as_expr())
 return X.applyfunc(f)
def conj(X,Y,p=0):return norm(Y*X*Y.inv(),p)
def comm(X,Y,p=0):return norm(X*Y*X.inv()*Y.inv(),p)
def test(name,X,Y,p=0):
 if any(v!=0 for v in norm(X-Y,p)):raise ValueError(name)
 checks.append(name)
def reject(name,X,Y,p=0):
 if all(v==0 for v in norm(X-Y,p)):raise ValueError('failed negative '+name)
 checks.append('rejected:'+name)
def roots(n,*terms):
 X=s.eye(n)
 for i,j,a in terms:
  T=s.eye(n);T[i-1,j-1]=a;X=X*T
 return X
def generic(n):
 k=n//2;e=(-1)**k;I=s.eye(n);A=I.copy()
 for i in [1,2,n-3,n-2]:A[i,i]=-1
 A[1,0]=1;A[n-2,n-1]=1
 if n==6:
  A=I.copy();A[0,0]=A[5,5]=-1;A[1,0]=A[4,5]=-1
 mu=s.zeros(n);tau=s.zeros(n)
 for i in range(n):mu[(i+1)%n,i]=1;tau[n-1-i,i]=1
 B=s.diag(*([e/u]*k+[1]*k))*tau;C=tau*mu;E=norm(B*C)
 def ck(label,X,Y):test(f'n{n}:{label}',X,Y)
 ck('A2',A*A,I);ck('B2',B*B,e/u*I);ck('C2',C*C,I);ck('AB',A*B,B*A)
 ck('detB',s.Matrix([B.det()]),s.Matrix([u**(-k)]))
 ck('detC',s.Matrix([C.det()]),s.Matrix([(-1)**(k-1)]))
 X=comm(A,conj(A,E))
 if n>=8:
  T=conj(norm((X*conj(A,E**2))**2),E);Z=comm(T,X);R=comm(A,Z);V=conj(R,B);W=comm(Z,V)
  ck('X',X,roots(n,(3,1,-1),(n-1,1,e*u)))
  if n==8:
   ck('T',T,roots(n,(4,3,-u),(5,2,u),(5,3,-u*u),(n,3,u**3)))
   ck('Z',Z,roots(n,(4,1,u),(5,1,u*u),(n,1,-u**3)))
  else:
   ck('T',T,roots(n,(4,3,-e*u),(5,2,1),(5,3,-e*u),(n,3,e*u**3)))
   ck('Z',Z,roots(n,(4,1,e*u),(5,1,e*u),(n,1,-e*u**3)))
  ck('R',R,roots(n,(n-1,1,-e*u**3)));ck('V',V,roots(n,(2,n,-u*u)));ck('W',W,roots(n,(2,1,-e*u**5)))
  D=s.eye(n);D[n-2,n-2]=D[3,3]=-1
  ck('isolation',comm(D,X),roots(n,(n-1,1,-2*e*u)))
 else:
  Q=comm(conj(A,E**4),X);R=comm(A,Q);h=u*u+4*u
  ck('X',X,roots(n,(3,1,-1),(5,1,-u)));ck('Q',Q,roots(n,(5,1,2*u),(6,1,-u*u)))
  ck('R',R,roots(n,(5,1,-h)));Y=norm((conj(A,E**4)*roots(n,(5,1,h)))**2)
  ck('seed',Y,roots(n,(6,1,u*h)));ck('adjacent',conj(Y,E),roots(n,(1,2,u*h)))
  D=s.diag(1,1,1,1,-1,-1);P=comm(D,X)
  ck('isolation',P,roots(n,(5,1,2*u)));ck('opposite',conj(P,C),roots(n,(1,5,2*u)))
def four(p):
 I=s.eye(4);A=s.Matrix([[0,0,0,-1],[0,0,-1,0],[0,1,0,0],[1,0,0,0]])
 B=s.Matrix([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]])if p else s.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
 sign=-1 if p else 1
 G=s.Matrix([[-1,0,0,0],[sign,1,0,0],[sign*u,0,1,0],[sign*u,0,0,1]])
 def ck(label,X,Y):test(f'n4:char{p or "not3"}:{label}',X,Y,p)
 ck('A2',A*A,-I);ck('B2',B*B,-I if p else I);ck('G2',G*G,I);ck('anticommute',A*B,-B*A)
 J=norm(G*conj(G,A*B,p)*G,p)
 if p:
  D=norm((conj(G,A*B,p)*G)**2*conj(J,B,p),p);DD=norm(D*conj(D,A,p),p)
  D0=s.Matrix([[-1,0,0,0],[0,-1,u,u],[0,u,-u*u-1,1-u*u],[-u,0,0,1]])
  DD0=s.Matrix([[-1,0,0,-u],[-1,1,0,-u],[-u,0,1,u*u-1],[-u,0,0,-u*u-1]])
  ck('D',D,D0);ck('DD',DD,DD0);wrong=DD0.copy();wrong[3,3]=-u-1
  reject('printed_DD44',DD,wrong,p)
  T=norm(G*DD*conj(G,A,p),p);P=norm((conj(T,B,p)*J)**2,p);w=u**3+u
  ck('T',T,roots(4,(2,4,u),(3,4,u*u)));ck('P',P,roots(4,(4,2,w)))
  ck('PAB',conj(P,A*B,p),roots(4,(3,1,w)));ck('PA',conj(P,A,p),roots(4,(1,3,-w)))
  Q=comm(conj(G,A*B,p),conj(P,A*B,p),p);ck('Q',Q,roots(4,(3,2,w)));ck('QA',conj(Q,A,p),roots(4,(2,3,-w)))
  S=norm((T*s.diag(-1,1,-1,1))**2,p);ck('split',S,roots(4,(2,4,-u)));ck('opposite',conj(S,B,p),roots(4,(4,2,u)))
 else:
  S34=norm(J*A*B);S12=conj(S34,A);D=norm(S12*J)
  ck('D',D,s.diag(-1,-1,1,1));ck('comm',comm(D,G),roots(4,(3,1,2*u),(4,1,2*u)))
  V=roots(4,(3,1,-u),(4,1,-u));E=norm(G*V);U=conj(V,A)
  ck('E',E,s.diag(-1,1,1,1)*roots(4,(2,1,1)));ck('U',U,roots(4,(1,4,u),(2,4,u)))
  ck('seed',(U*E)**2,roots(4,(2,4,3*u)));ck('opposite',conj(roots(4,(2,4,u)),B),roots(4,(4,2,u)))
  reject('printed_gamma_conjugator',conj(V,G),U);reject('square_only_E',U*E**2,roots(4,(2,4,3*u)))
for n in [6,8,10,12,14,16]:generic(n)
four(3);four(0)
report={'status':'PASS','role':'OPTIONAL_SYMBOLIC_VALIDATION_NOT_UNIFORM_PROOF_PREMISE','sympy_version':s.__version__,'dimensions_sampled':[6,8,10,12,14,16],'characteristic_three_ring':'F3[u]','other_ring':'Q(u)','checks':checks,'count':len(checks),'limitations':'Sampled dimensions do not prove the all-dimension theorem; the manuscript uses a uniform support calculation.'}
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks)}))
