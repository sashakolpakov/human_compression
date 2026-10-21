"""Exact rational matrix arithmetic for the displayed integral word identities.
The uniform case uses eight abstract labels, not a test at a selected n.
"""
from fractions import Fraction as F
from functools import reduce

def need(ok,msg):
 if not ok:raise ValueError(msg)
def eye(n):return tuple(tuple(F(i==j) for j in range(n))for i in range(n))
def mat(n,entries):
 a=[list(r)for r in eye(n)]
 for i,j,v in entries:a[i-1][j-1]=F(v)
 return tuple(map(tuple,a))
def mul(a,b):
 n=len(a);return tuple(tuple(sum((a[i][k]*b[k][j]for k in range(n)),F(0))for j in range(n))for i in range(n))
def prod(*xs):return reduce(mul,xs)
def inv(a):
 n=len(a);a=[list(r)+list(s)for r,s in zip(a,eye(n))]
 for i in range(n):
  j=next((j for j in range(i,n)if a[j][i]),None);need(j is not None,'singular matrix')
  a[i],a[j]=a[j],a[i];v=a[i][i];a[i]=[x/v for x in a[i]]
  for j in range(n):
   if j!=i:
    v=a[j][i];a[j]=[x-v*y for x,y in zip(a[j],a[i])]
 return tuple(tuple(r[n:])for r in a)
def power(a,n):
 if n<0:return power(inv(a),-n)
 b=eye(len(a))
 for _ in range(n):b=mul(b,a)
 return b
def cj(a,b):return prod(b,a,inv(b))
def cm(a,b):return prod(inv(a),inv(b),a,b)
def t(n,i,j,v=1):return mat(n,[(i,j,v)])
def d(n,*js):return mat(n,[(j,j,-1)for j in js])
def p(n,*pairs):return mat(n,[(i,j,1)for a,b in pairs for i,j in [(a,b),(b,a)]]+[(i,i,0)for pair in pairs for i in pair])
def delta(a):
 out=[]
 for i,r in enumerate(a):
  for j,x in enumerate(r):
   x-=int(i==j)
   if x:need(x.denominator==1,'noninteger output');out.append([i+1,j+1,int(x)])
 return out
def rec(a):return delta(a)
def monomial(a):
 out=[]
 for j in range(len(a)):
  ns=[(i,x)for i,row in enumerate(a)if (x:=row[j])]
  need(len(ns)==1 and abs(ns[0][1])==1,'not signed monomial')
  out.append(ns[0][0]+1)
 return out
def base_general(n):
 A=mat(n,[(i,i,-1)for i in (2,3,n-2,n-1)]+[(2,1,1),(n-1,n,1)])
 tau=p(n,*[(i,n+1-i)for i in range(1,n//2+1)])
 mu=tuple(tuple(F(i==(j+1)%n)for j in range(n))for i in range(n))
 B=tau if n%4 in (0,1)else tuple(tuple(-x for x in r)for r in tau)
 C=mul(tau,mu)
 if n%4==1:C=mul(d(n,n),C)
 if n%4==3:C=mul(d(n,*range(1,n)),C)
 return A,B,C,mul(B,C)
def words_general(A,B,E):
 X=cm(A,cj(A,E));T=cj(power(mul(X,cj(A,power(E,2))),2),E);Z=cm(T,X);R=cm(A,Z);V=cj(R,B);S=cm(Z,V)
 return dict(X=X,T=T,Z=Z,R=R,V=V,S=S)
def uniform(sigma):
 # Abstract basis: 1,2,3,4,5,N-2,N-1,N. These are distinct for N>=8.
 labels=['1','2','3','4','5','N-2','N-1','N'];n=8
 A=mat(n,[(i,i,-1)for i in(2,3,6,7)]+[(2,1,1),(7,8,1)])
 A1=mat(n,[(i,i,-1)for i in(3,4,7,8)]+[(3,2,1),(8,1,sigma)])
 A2=mat(n,[(i,i,-1)for i in(4,5,8,1)]+[(4,3,1),(1,2,1)])
 X=cm(A,A1);T0=power(mul(X,A2),2)
 # Partial successor map is defined on every support index of T0.
 suc={1:2,2:3,3:4,4:5,7:8}
 es=[]
 for i,j,v in delta(T0):need(i in suc and j in suc,'unsupported uniform successor');es.append((suc[i],suc[j],v))
 T=mat(n,es);Z=cm(T,X);R=cm(A,Z)
 rev={1:8,7:2};es=[]
 for i,j,v in delta(R):need(i in rev and j in rev,'unsupported uniform reversal');es.append((rev[i],rev[j],v))
 V=mat(n,es);S=cm(Z,V)
 return {k:[[labels[i-1],labels[j-1],v]for i,j,v in delta(a)]for k,a in dict(X=X,T=T,Z=Z,R=R,V=V,S=S).items()}
def run():
 results={}
 A=p(2,(1,2));B=d(2,2);C=mat(2,[(1,2,1),(2,2,-1)])
 need(mul(A,B)==tuple(tuple(-x for x in r)for r in mul(B,A)),'projective commutation')
 for x in(A,B,C):need(power(x,2)==eye(2),'n2 involution')
 results['n2']={'BC':rec(mul(B,C)),'conjugate':rec(cj(mul(B,C),A))}
 A=mat(5,[(1,1,-1),(5,5,-1),(2,1,1),(4,5,1)]);B=tuple(tuple(-x for x in r)for r in p(5,(1,5),(2,4)));C=p(5,(1,4),(2,3));E=mul(B,C)
 for x in(A,B,C):need(power(x,2)==eye(5),'n5 involution')
 need(mul(A,B)==mul(B,A),'n5 commuting pair')
 X=cm(A,cj(A,E));Y=cj(X,E);Z=cm(A,Y);W=cj(Z,inv(E));T=cm(Y,W);V=cj(T,power(E,3));R=cm(T,V)
 results['n5']={k:rec(v)for k,v in dict(X=X,Y=Y,Z=Z,W=W,T=T,V=V,R=R).items()}
 A=mat(6,[(1,1,-1),(6,6,-1),(2,1,1),(4,4,0),(5,5,0),(4,5,1),(5,4,1)]);B=p(6,(1,2),(3,4),(5,6));C=p(6,(1,6),(2,5),(3,4))
 for x in(A,B,C):need(power(x,2)==eye(6),'n6 involution')
 need(mul(B,C)==mul(C,B),'n6 commuting pair')
 U=power(mul(cj(A,C),A),2);E=power(mul(A,cj(A,B)),2);L=cj(cj(A,B),E);D=power(mul(A,L),2);Dp=cj(D,C);F=mul(A,cj(A,Dp));Fp=cj(F,C);J=prod(Dp,F,Fp);V=mul(J,L);W=cj(V,B);K=cj(J,C);H=power(prod(K,A,E),2);I0=mul(H,K);M=mul(I0,A);N=cj(W,C);P=power(mul(M,N),2);Q=cj(cj(U,B),E);R=cm(Q,P);R16=cj(R,C);R26=cm(A,R16);R62=cj(R26,mul(B,C));w16=prod(R16,inv(R),R16);w26=prod(R26,inv(R62),R26);r12=cj(R16,w26);w12=cj(w16,w26);r21=inv(cj(r12,w12));p36=mul(inv(r21),V)
 need(r21==t(6,2,1),'n6 t21 extraction');need(p36==p(6,(3,6)),'n6 p36 extraction')
 results['n6']={k:rec(v)for k,v in dict(U=U,E=E,L=L,D=D,Dp=Dp,F=F,Fp=Fp,J=J,V=V,W=W,K=K,H=H,I0=I0,M=M,N=N,P=P,Q=Q,R=R,R16=R16,R26=R26,R62=R62).items()}
 results['n6_permutations']=[monomial(g)for g in(w16,w26,p36,cj(w16,B),cj(p36,B))]
 # Connected edge tree, and complete ordered-pair orbit, independent of signs.
 gens=results['n6_permutations'];seen={(1,6)};todo=[(1,6)]
 for i,j in todo:
  for g in gens:
   z=(g[i-1],g[j-1])
   if z not in seen:seen.add(z);todo.append(z)
 need(len(seen)==30,'n6 all root positions');results['n6_root_orbit']=len(seen)
 A,B,C,E=base_general(7);ws=words_general(A,B,E);Q=cm(ws['S'],cj(ws['S'],E));P=cm(A,Q);unit=mul(ws['S'],inv(P));need(unit==t(7,2,1),'n7 unit cancellation');ws.update(Q=Q,P=P,unit=unit)
 for x in(A,B,C):need(power(x,2)==eye(7),'n7 involution')
 need(mul(A,B)==mul(B,A),'n7 commuting pair');results['n7']={k:rec(v)for k,v in ws.items()}
 results['uniform']={str(sigma):uniform(sigma)for sigma in(-1,1)}
 return results
if __name__=='__main__':
 import json
 print(json.dumps(run(),indent=2))
