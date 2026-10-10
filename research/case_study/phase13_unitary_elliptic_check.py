#!/usr/bin/env python3
"""Exact symbolic geometry and original quadratic-field diagnostics.

The finite diagnostics do not prove the general sheaf estimate or the IP.
Only Python stdlib and SymPy are used; no group-recognition database.
"""
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math
import sympy as s

x,y,d,z=s.symbols('x y d z')
F=d*x*y*y+2*d*x*x*y-x-2*y
Fx,Fy=s.diff(F,x),s.diff(F,y)
assert s.expand(F-x*Fx+2*y*(d*x*x+1))==0
assert s.expand(Fy-2*d*x*y+4-2*(d*x*x+1))==0
assert s.expand(Fx.subs(y,-2*x)-3+4*(d*x*x+1))==0
Fhom=d*x*y*y+2*d*x*x*y-x*z*z-2*y*z*z
dx,dy,dz=[s.diff(Fhom,v) for v in (x,y,z)]
assert dy.subs({x:1,y:0,z:0})==2*d
assert dx.subs({x:0,y:1,z:0})==d
assert dx.subs({x:1,y:-2,z:0})==-4*d
assert s.Poly(s.expand(Fhom-(y-x)*(d*x*y+z*z)),x,y,z,d,modulus=3).is_zero
# The derivative at x=eps1/delta,y=eps2/delta equals4eps1eps2.
delta=s.symbols('delta',nonzero=True)
for a in (-1,1):
    for b in (-1,1):
        sub={x:a/delta,y:b/delta,d:delta**2}
        assert s.simplify(F.subs(sub))==0
        assert s.simplify(Fx.subs(sub))==4*a*b
mu=(delta*y-1)/(delta*y+1)
lam=delta*x
tt=lam-1/lam
tp=mu-1/mu
assert s.cancel((tt*tp-2)+2*F.subs(d,delta**2)/(x*(delta**2*y*y-1)))==0

def factors(n):
    ans=[]; j=2
    while j*j<=n:
        if n%j==0:
            ans.append(j)
            while n%j==0:n//=j
        j+=1
    if n>1:ans.append(n)
    return ans

def isprime(n):
    return n>=2 and all(n%i for i in range(2,math.isqrt(n)+1))

ps=[p for p in range(3,64) if isprime(p)]
assert len(ps)==17 and 2**102<22**6*math.prod(ps)
assert 176**6//8==3715232694272 and 176**6%8==0

class Quad:
    """F_p[delta]/(delta²-d), represented by integer coefficient pairs."""
    def __init__(self,p,ns): self.p,self.d=p,ns;self.zero=(0,0);self.one=(1,0)
    def add(self,a,b):return ((a[0]+b[0])%self.p,(a[1]+b[1])%self.p)
    def neg(self,a):return((-a[0])%self.p,(-a[1])%self.p)
    def sub(self,a,b):return self.add(a,self.neg(b))
    def mul(self,a,b):return((a[0]*b[0]+self.d*a[1]*b[1])%self.p,(a[0]*b[1]+a[1]*b[0])%self.p)
    def power(self,a,n):
        out=self.one
        while n:
            if n&1:out=self.mul(out,a)
            a=self.mul(a,a);n//=2
        return out
    def inv(self,a):
        assert a!=self.zero
        denom=(a[0]*a[0]-self.d*a[1]*a[1])%self.p
        scale=pow(denom,-1,self.p)
        return(a[0]*scale%self.p,-a[1]*scale%self.p)
    def div(self,a,b):return self.mul(a,self.inv(b))
    def mm(self,A,B):
        return [[sumfield([self.mul(A[i][k],B[k][j]) for k in range(4)],self) for j in range(4)] for i in range(4)]
    def eye(self):return [[self.one if i==j else self.zero for j in range(4)]for i in range(4)]
    def mpow(self,A,n):
        out=self.eye()
        while n:
            if n&1:out=self.mm(out,A)
            A=self.mm(A,A);n//=2
        return out

def sumfield(vals,K):
    out=K.zero
    for a in vals:out=K.add(out,a)
    return out

def scalar(A,K):return all(A[i][j]==(A[0][0] if i==j else K.zero) for i in range(4) for j in range(4))
def theta(n):return math.prod([Fraction(p-1,p) for p in factors(n)])

records=[]
for p in [5,13,17,29,37,41,53,61,73,89,97,101,109,113]:
    assert isprime(p) and p%4==1
    ns=next(a for a in range(2,p) if pow(a,(p-1)//2,p)==p-1)
    K=Quad(p,ns); n=(p+1)//2; m=p-1
    while m%2==0:m//=2
    prim_square=lambda a:all(pow(a,(p-1)//r,p)!=1 for r in factors(p-1))
    u=[]
    for yy in range(1,p):
        muy=K.div((p-1,yy),(1,yy)); hh=K.mul(muy,muy)
        assert K.power(muy,p+1)==K.one and K.power(hh,n)==K.one
        if all(K.power(hh,n//r)!=K.one for r in factors(n)):u.append((yy,muy))
    umap=dict(u)
    count=0;interior=0;first=None
    for xx in range(1,p):
        okg=prim_square(ns*xx*xx%p)
        for yy in range(1,p):
            if (ns*xx*yy*yy+2*ns*xx*xx*yy-xx-2*yy)%p:continue
            interior+=1
            if okg and yy in umap:
                count+=1
                if first is None:first=(xx,yy)
    points=interior+4
    assert (points-p-1)**2<=4*p
    A,B=2**len(factors(m)),2**len(factors(n))
    error=8*A*B-4*A-4*B
    gap=Fraction(count,1)/(theta(m)*theta(n))-points
    if gap<0:assert gap*gap<=p*error*error
    witness=None
    if first is not None:
        xx,yy=first;ll=(0,xx);mm=umap[yy]
        t=K.sub(ll,K.inv(ll));tp=K.sub(mm,K.inv(mm));kk=K.neg(K.add(t,tp))
        assert K.mul(t,tp)==(2,0)
        assert kk[0]==0 and kk[1]!=0
        ii=next(a for a in range(1,p) if a*a%p==p-1)
        zero=K.zero; one=K.one;minus=(p-1,0); im=(ii,0)
        r1=[[one,zero,zero,zero],[zero,zero,zero,one],[zero,zero,minus,zero],[zero,one,zero,zero]]
        r2=[[zero,im,zero,zero],[im,zero,zero,zero],[zero,zero,kk,K.sub(im,kk)],[zero,zero,K.add(im,kk),K.neg(kk)]]
        T=K.mm(r1,r2);order=p*p-1
        assert K.mpow(T,order)==K.eye()
        tested=factors(order)
        for prime in tested:assert not scalar(K.mpow(T,order//prime),K)
        witness={'x':xx,'y':yy,'k_coefficients':kk,'i':ii,'projective_order':order,'tested_prime_divisors':tested}
    records.append({'q':p,'nonsquare_d':ns,'curve_points':points,'primitive_pairs':count,'witness':witness,'criterion_squared_margin':(p+1)**2-p*(error+2)**2})

b=Path(__file__).resolve().parent
report={'status':'PASS','executed_at_utc':datetime.now(timezone.utc).isoformat(),'scope':['Exact smoothness/branch-point/Cayley polynomial identities','Universal divisor bound and explicit threshold','Independent coefficient-pair arithmetic in14quadratic prime-field extensions','All affine curve points and primitive pairs in these14fields','Direct projective matrix-order certificate for every successful sample'], 'not_certified':['Hasse-Weil and l-adic character-sum inputs','Uniform group-generation/IP proof','Exhaustion of the full finite range'],'sympy_version':s.__version__,'prime_diagnostics':records,'input_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in [Path(__file__).resolve(),b/'phase13_unitary_elliptic.md']}}
(b/'phase13_unitary_elliptic_check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: symbolic geometry; exact uniform threshold;14prime-field curve counts and direct matrix-order certificates.')
for r in records:print(r['q'],r['curve_points'],r['primitive_pairs'])
