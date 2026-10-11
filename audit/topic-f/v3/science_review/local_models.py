#!/usr/bin/env python3
"""Independent integer-coordinate diagnostics, not a uniform-proof premise.
No author program, group package, or author's scoring/model implementation is imported.
"""
from math import comb,prod
from random import Random
from pathlib import Path
import argparse,json

def need(q,msg):
 if not q:raise ValueError(msg)
def rank(A,p):
 A=[list(r)for r in A];i=0
 for j in range(len(A[0])):
  k=next((k for k in range(i,len(A))if A[k][j]%p),None)
  if k is None:continue
  A[i],A[k]=A[k],A[i];d=pow(A[i][j],-1,p);A[i]=[x*d%p for x in A[i]]
  for k in range(len(A)):
   if k!=i:
    d=A[k][j];A[k]=[(x-d*y)%p for x,y in zip(A[k],A[i])]
  i+=1
  if i==len(A):break
 return i
class Model:
 def __init__(self,p,n,even=False,carry=True):
  self.p=p;self.n=n;self.e=(n-1)//(p-1)+1;self.r=(n-1)%(p-1)+1;self.even=even
  self.mods=tuple([p**self.e]*self.r+[p**(self.e-1)]*(p-1-self.r)+([p]if even else[]))
  self.zero=(0,)*len(self.mods);self.s=self.vec([1]+[0]*(len(self.mods)-1));z=[0]*len(self.mods);z[self.r-1]=p**(self.e-1);self.z=self.vec(z)if carry else self.zero
  self.id=(self.zero,0,0);self.beta=(self.zero,1,0);self.sig=(self.zero,0,1);self.sg=(self.s,0,0)
  self.order=2*p*prod(self.mods);self.a=self.mul(self.beta,self.sg);self.b=self.mul((self.neg(self.s),0,0),self.sig)
 def vec(self,x):return tuple(a%m for a,m in zip(x,self.mods))
 def add(self,x,y):return self.vec([a+b for a,b in zip(x,y)])
 def neg(self,x):return self.vec([-a for a in x])
 def scale(self,k,x):return self.vec([k*a for a in x])
 def T(self,v,k=1):
  for _ in range(k%self.p):
   w=list(v);d=self.p-1;last=v[d-1]
   for i in range(d):w[i]=v[i]+(v[i-1]if i else 0)-comb(self.p,i+1)*last
   if self.even:
    j=(v[0]+self.p*v[-1])%(self.p**2);w[-1]=((j-w[0])//self.p)%self.p
   v=self.vec(w)
  return v
 def S(self,v):
  result=self.zero
  for i in range(self.p-1):
   e=[0]*len(v);e[i]=1;col=self.T(self.vec(e),-i)
   # The auxiliary coordinate in this basis is corrected only after the ring part.
   result=self.add(result,self.scale((-1)**i*v[i],col))
  if self.even:
   w=list(result);j=(v[0]+self.p*v[-1])%(self.p**2);w[-1]=((j-w[0])//self.p)%self.p;result=self.vec(w)
  return result
 def sigP(self,v,k):
  return (self.S(v),0)if k==0 else(self.add(self.S(v),self.neg(self.z)),self.p-k)
 def mul(self,a,b):
  v,k,t=a;w,l,u=b
  if t:w,l=self.sigP(w,l)
  return (self.add(self.add(v,self.T(w,-k)),self.scale((k+l)//self.p,self.z)),(k+l)%self.p,t^u)
 def power(self,a,n):
  out=self.id
  while n:
   if n&1:out=self.mul(out,a)
   a=self.mul(a,a);n//=2
  return out
 def inv(self,a):return self.power(a,self.order-1)
 def cyclic(self,a,bound):
  ans=[];x=self.id
  for i in range(bound):
   ans.append(x);x=self.mul(x,a)
   if x==self.id:return ans
  raise ValueError('cyclic bound')
 def random(self,r):return(tuple(r.randrange(m)for m in self.mods),r.randrange(self.p),r.randrange(2))
 def validate(self):
  p=self.p;basis=[self.vec([int(j==i)for j in range(len(self.mods))])for i,m in enumerate(self.mods)if m>1]
  need(all(self.T(v,p)==v and self.S(self.S(v))==v and self.S(self.T(self.S(v)))==self.T(v,-1)for v in basis),'linear dihedral action')
  need(self.S(self.s)==self.s and self.T(self.z)==self.z and self.S(self.z)==self.neg(self.z),'actual carry hypotheses')
  cols=[self.T(self.s,i)for i in range(p)];rows=[[col[j]%p for col in cols]for j,m in enumerate(self.mods)if m>1];need(rank(rows,p)==len(rows),'orbit spans module mod p, hence whole finite abelian p-group')
  w=self.z
  for col in cols:w=self.add(w,col)
  need(self.power(self.a,p)==(w,0,0)and self.power(self.beta,p)==(self.z,0,0),'exact powers with carry')
  A=self.cyclic(self.a,p*p+1);B=self.cyclic(self.b,2*p**self.e+1)
  need(len(A)==p*p and len(B)==2*p**self.e and set(A)&set(B)=={self.id},'exact cyclic orders and intersection')
  need(self.power(self.mul(self.a,self.b),2)==self.id and self.mul(self.a,self.b)!=self.id,'product involution')
  R=Random(130000+p*1000+self.n*10+self.even)
  for _ in range(200):
   x,y,z=[self.random(R)for i in range(3)];need(self.mul(self.mul(x,y),z)==self.mul(x,self.mul(y,z)),'associativity');need(self.mul(x,self.inv(x))==self.id,'inverse')
  need(self.order>len(A)*len(B),'non-tight')
  return dict(p=p,n=self.n,even=self.even,group_order=self.order,type=[len(A),len(B)],intersection=1,module_rank=len(rows),random_associativity=200,carry=list(self.z),norm_plus_carry=list(w))

def unitriangular_checks():
 positions=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];results=[]
 for p in [3,5,7]:
  zero=(0,)*6
  def mul(a,b):
   A=dict(zip(positions,a));B=dict(zip(positions,b));return tuple((A[i,j]+B[i,j]+sum(A.get((i,k),0)*B.get((k,j),0)for k in range(i+1,j)))%p for i,j in positions)
  def power(a,n):
   z=zero
   while n:
    if n&1:z=mul(z,a)
    a=mul(a,a);n//=2
   return z
  def inv(a):return power(a,p*p-1)
  def comm(a,b):return mul(mul(mul(inv(a),inv(b)),a),b)
  R=Random(p)
  for _ in range(100):
   x=tuple(R.randrange(p)for _ in range(6));y=tuple(R.randrange(p)for _ in range(6));c=comm(x,y);d=comm(c,x);e=comm(c,y)
   for k in range(1,9):
    rhs=mul(mul(mul(mul(power(x,k),power(y,k)),power(inv(c),comb(k,2))),power(inv(d),comb(k,3))),power(inv(e),2*comb(k,3)+comb(k,2)))
    need(power(mul(x,y),k)==rhs,'complete class-three collection formula')
   need(comm(comm(inv(x),inv(y)),inv(x))==inv(d)and comm(comm(inv(x),inv(y)),inv(y))==inv(e),'triple inversion')
  results.append(dict(p=p,pairs=100,power_tests=800,triple_inversion_tests=200))
 return results

def regular_ip(mul,identity,a,b,alpha,expected):
 def times(g,h):return(mul(g[0],alpha(h[0])if g[1]else h[0]),g[1]^h[1])
 one=(identity,0);rs=[(a,1),(identity,1),(alpha(b),1)]
 need(all(times(x,x)==one and x!=one for x in rs)and times(rs[0],rs[2])==times(rs[2],rs[0]),'regular doubling string')
 def closure(gens):
  seen={one};queue=[one]
  for x in queue:
   for g in gens:
    y=times(x,g)
    if y not in seen:seen.add(y);queue.append(y)
  return seen
 sub=[closure([rs[i]for i in range(3)if mask>>i&1])for mask in range(8)]
 need(len(sub[7])==expected,'full regular marked generation')
 for i in range(8):
  for j in range(8):need(sub[i]&sub[j]==sub[i&j],'all64 subset IP identities')
 return dict(order=expected,type=[len(sub[3])//2,len(sub[6])//2],IP_pairs=64)

def regular_models():
 out=[]
 for p in [3,5]:
  m=Model(p,3,carry=False)
  def tau(g):v,k,t=g;return(m.neg(v),k,t)
  def alpha(g):return m.mul(m.mul(m.inv(m.sg),m.mul(m.mul(m.sig,tau(g)),m.sig)),m.sg)
  q=regular_ip(m.mul,m.id,m.a,m.b,alpha,4*p**4);need(q['type']==[p,2*p**m.e],'exact second cyclotomic type');out.append(dict(model='zero-carry second marking',p=p,**q))
 for p in [3,5,7]:
  def hm(x,y):
   i,j,k=x;a,b,c=y;return((i+a)%(p*p),(j+b)%p,(k+c-a*j)%p)
  def theta_inv(x):
   i,j,k=x;return((-i)%(p*p),(j-i)%p,(-i*(i-1)//2-k)%p)
  def gm(x,y):
   h,t=x;q,u=y;v=hm(h,theta_inv(q)if t else q)
   if t and u:v=hm(v,(0,1,0))
   return(v,t^u)
  def alpha(x):
   (i,j,k),t=x;return(((-i)%(p*p),(-j-t)%p,k),t)
  e=((0,0,0),0);a=((1,0,0),0);b=((0,0,0),1);R=Random(p+901)
  for _ in range(100):
   x,y,z=[((R.randrange(p*p),R.randrange(p),R.randrange(p)),R.randrange(2))for i in range(3)]
   need(gm(gm(x,y),z)==gm(x,gm(y,z))and alpha(gm(x,y))==gm(alpha(x),alpha(y))and alpha(alpha(x))==x,'mixed group and reversal identities')
  q=regular_ip(gm,e,a,b,alpha,4*p**4);need(q['type']==[p*p,2*p],'mixed regular type');out.append(dict(model='mixed Heisenberg',p=p,**q))
 return out

def p_only_models():
 out=[]
 for p in [3,5,7]:
  for n in [2,3,4,5,6]:
   m=Model(p,n);R=Random(90000+p*10+n)
   need(m.T(m.z)==m.z and m.z!=m.zero and m.scale(p,m.z)==m.zero,'all-parity nonzero fixed carry')
   norm=m.zero
   for k in range(p):norm=m.add(norm,m.T(m.s,k))
   need(norm==m.zero and m.power(m.beta,p)==(m.z,0,0)and m.power(m.a,p)==(m.z,0,0),'all-parity norm and carry powers')
   v=m.s;chain=[]
   for k in range(n+1):
    chain.append(v!=m.zero);v=m.add(m.T(v),m.neg(v))
   need(chain==[True]*n+[False],'actual lower central length')
   for _ in range(100):
    xyz=[]
    for i in range(3):
     v,k,t=m.random(R);xyz.append((v,k,0))
    x,y,z=xyz;need(m.mul(m.mul(x,y),z)==m.mul(x,m.mul(y,z)),'p-only associativity without reflection')
   out.append(dict(p=p,n=n,order=p**(n+1),nilpotency_class=n,parity_unrestricted=True))
 return out

def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args();need(not args.out.exists(),'fresh output')
 cases=[(3,4,False),(3,6,False),(5,4,False),(5,6,False),(7,4,False),(3,4,True),(3,6,True),(5,6,True),(7,8,True)]
 rows=[Model(*c).validate()for c in cases]
 controls=[]
 # Odd n changes the sign of the carry and prevents sigma descending.
 m=Model(5,3);need(m.S(m.z)!=m.neg(m.z),'odd module length sign obstruction');controls.append('odd length rejects carry reflection')
 # No carry: a genuine regular reversal, so nonzero odd carry is essential.
 m=Model(3,4,carry=False);R=Random(77)
 def tau(g):v,k,t=g;return(m.neg(v),k,t)
 def alpha(g):return m.mul(m.mul(m.inv(m.sg),m.mul(m.mul(m.sig,tau(g)),m.sig)),m.sg)
 need(alpha(m.a)==m.inv(m.a)and alpha(m.b)==m.inv(m.b),'zero carry restores pair reversal')
 for _ in range(100):
  x,y=m.random(R),m.random(R);need(alpha(m.mul(x,y))==m.mul(alpha(x),alpha(y))and alpha(alpha(x))==x,'actual reversal automorphism with zero carry')
 controls.append('zero carry permits a genuine reversal')
 # p=2 carries have z=z^-1; this is the exact missing obstruction.
 need((-1)%2==1,'order-two carry');controls.append('order-two carry has no fixed/inverse contradiction')
 # Nonabelian S3 is generated by two involutions: identity inverts them but not their product.
 def compose(a,b):return tuple(a[b[i]]for i in range(3))
 x=(1,0,2);y=(0,2,1);xy=compose(x,y);need(compose(x,x)==compose(y,y)==(0,1,2)and compose(xy,xy)!=(0,1,2),'abelian closure hypothesis');controls.append('noncommuting generators invalidate inversion-on-closure')
 result=dict(status='PASS',independent_of_author_programs=True,finite_diagnostics_not_uniform_proof=True,carry_models=rows,p_only_models=p_only_models(),class_three=unitriangular_checks(),regular_models=regular_models(),hypothesis_controls=controls)
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(rows),'carry models;3 class-three matrix groups;',len(controls),'controls')
if __name__=='__main__':main()
