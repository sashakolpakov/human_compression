#!/usr/bin/env python3
"""Independent, standard-library verification of the phase-15 field witnesses.
No author checker or GAP library is imported. This verifies finite parameters,
not the conditional uniform generation/intersection or character-sum proofs.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, time

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def prime_factors(n):
    result=[]; d=2
    while d*d<=n:
        if n%d==0:
            result.append(d)
            while n%d==0: n//=d
        d=3 if d==2 else d+2
    if n>1: result.append(n)
    return result

def trim(a):
    while len(a)>1 and a[-1]==0: a.pop()
    return a

def poly_rem(a,b,p):
    a=trim(a[:]); b=trim(b[:]); inv=pow(b[-1],-1,p)
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b); c=a[-1]*inv%p
        for j in range(len(b)): a[k+j]=(a[k+j]-c*b[j])%p
        trim(a)
    return a

def poly_gcd(a,b,p):
    while trim(b[:])!=[0]: a,b=b,poly_rem(a,b,p)
    inv=pow(a[-1],-1,p)
    return [(x*inv)%p for x in a]

class Base:
    def __init__(self,p,f):
        self.p=p; self.f=tuple(f); self.n=len(f)-1; self.q=p**self.n
        assert self.n>0 and self.f[-1]==1 and all(0<=v<p for v in f)
        assert prime_factors(p)==[p]
        self.zero=(0,)*self.n; self.one=(1,)+(0,)*(self.n-1)
        # Rabin's irreducibility criterion, independently via reduction.
        if self.n>1:
            z=(0,1)+(0,)*(self.n-2)
            assert self.power(z,self.q)==z
            for ell in prime_factors(self.n):
                v=self.sub(self.power(z,p**(self.n//ell)),z)
                assert poly_gcd(list(v),list(f),p)==[1]
    def constant(self,x): return (x%self.p,)+(0,)*(self.n-1)
    def read(self,a):
        assert len(a)==self.n and all(isinstance(x,int) and 0<=x<self.p for x in a)
        return tuple(a)
    def add(self,a,b): return tuple((x+y)%self.p for x,y in zip(a,b))
    def neg(self,a): return tuple((-x)%self.p for x in a)
    def sub(self,a,b): return self.add(a,self.neg(b))
    def mul(self,a,b):
        if self.n==1: return (a[0]*b[0]%self.p,)
        c=[0]*(2*self.n-1)
        for j,x in enumerate(a):
            for k,y in enumerate(b): c[j+k]=(c[j+k]+x*y)%self.p
        for j in range(len(c)-1,self.n-1,-1):
            v=c[j]
            for k in range(self.n): c[j-self.n+k]=(c[j-self.n+k]-v*self.f[k])%self.p
        return tuple(c[:self.n])
    def power(self,a,n):
        out=self.one
        while n:
            if n&1: out=self.mul(out,a)
            a=self.mul(a,a); n//=2
        return out

class Quadratic:
    def __init__(self,F):
        self.F=F; self.zero=(F.zero,F.zero); self.one=(F.one,F.zero); self.i=(F.zero,F.one)
        assert F.q%4==3 and F.power(F.constant(-1),(F.q-1)//2)==F.constant(-1)
    def constant(self,x): return (self.F.constant(x),self.F.zero)
    def add(self,a,b): return (self.F.add(a[0],b[0]),self.F.add(a[1],b[1]))
    def neg(self,a): return (self.F.neg(a[0]),self.F.neg(a[1]))
    def sub(self,a,b): return self.add(a,self.neg(b))
    def mul(self,a,b):
        F=self.F
        return (F.sub(F.mul(a[0],b[0]),F.mul(a[1],b[1])),F.add(F.mul(a[0],b[1]),F.mul(a[1],b[0])))
    def power(self,a,n):
        out=self.one
        while n:
            if n&1: out=self.mul(out,a)
            a=self.mul(a,a); n//=2
        return out
    def bar(self,a): return (a[0],self.F.neg(a[1]))
    def norm(self,a): return self.mul(a,self.bar(a))[0]

def matmul(A,B,E):
    return [[sum_field((E.mul(A[j][k],B[k][l]) for k in range(len(B))),E) for l in range(len(B[0]))] for j in range(len(A))]
def sum_field(values,E):
    out=E.zero
    for v in values: out=E.add(out,v)
    return out

def identity(n,E): return [[E.one if j==k else E.zero for k in range(n)] for j in range(n)]
def matpow(A,n,E):
    out=identity(len(A),E)
    while n:
        if n&1: out=matmul(out,A,E)
        A=matmul(A,A,E); n//=2
    return out

def scalar(A,E):
    return A[0][0]!=E.zero and all(A[j][k]==(A[0][0] if j==k else E.zero) for j in range(len(A)) for k in range(len(A)))
def projective_order(A,m,E):
    assert scalar(matpow(A,m,E),E)
    for ell in prime_factors(m): assert not scalar(matpow(A,m//ell,E),E)

def determinant(A,E):
    n=len(A); out=E.zero
    for perm in itertools.permutations(range(n)):
        term=E.one
        for j in range(n): term=E.mul(term,A[j][perm[j]])
        if sum(perm[j]>perm[k] for j in range(n) for k in range(j+1,n))%2: term=E.neg(term)
        out=E.add(out,term)
    return out

def direct_check(record):
    F=Base(record['p'],record['base_polynomial']); E=Quadratic(F)
    q=record['q']; assert q==F.q and record['exponent']==F.n
    t,x,y=(F.read(record['parameter_'+v]) for v in ('t','x','y'))
    assert all(v!=F.zero for v in (t,x,y))
    assert F.add(F.add(F.mul(t,t),F.mul(x,x)),F.mul(y,y))==F.one
    h=F.add(F.add(F.mul(t,t),F.mul(F.constant(2),y)),F.constant(2)); assert h!=F.zero
    a=(F.zero,t); b=(x,y); c=(F.neg(x),y)
    aa=E.mul(a,a); assert aa[1]==F.zero and aa[0] not in (F.constant(8),F.constant(-1))
    for ell in prime_factors(F.n): assert F.power(aa[0],F.p**(F.n//ell))!=aa[0]
    z,o,i=E.zero,E.one,E.i; no=E.neg(o)
    R=[[z,i],[i,z]]; S=[[a,b],[c,E.neg(a)]]; Z=[[o,z],[z,no]]
    r0=[[o,z,z,z],[z,o,z,z],[z,z,no,z],[z,z,z,no]]
    r1=[[o,z,z,z],[z,z,z,o],[z,z,no,z],[z,o,z,z]]
    r2=[[z,i,z,z],[i,z,z,z],[z,z,a,b],[z,z,c,E.neg(a)]]
    r3=[[z,z,o,z],[z,z,z,o],[no,z,z,z],[z,no,z,z]]
    matrices=[r0,r1,r2,r3]
    for A in matrices:
        assert determinant(A,E)==o
        adj=[[E.bar(A[k][j]) for k in range(4)] for j in range(4)]
        assert matmul(adj,A,E)==identity(4,E)
        projective_order(A,2,E)
    for j,k in ((0,2),(0,3),(1,3)):
        # Their product has projective order at most two.
        assert scalar(matpow(matmul(matrices[j],matrices[k],E),2,E),E)
    m=record['projective_middle_order']; assert m in ((q*q-1)//2,(q*q+1)//2)
    projective_order(matmul(r1,r2,E),m,E)
    orders=record['rank_one_projective_orders']
    for A,n in zip((matmul(Z,S,E),matmul(R,S,E),matmul(matmul(Z,R,E),S,E)),orders): projective_order(A,n,E)
    assert max(orders)>5
    return {'q':q,'projective_middle_order':m,'rank_one_projective_orders':orders,'template_SU4_and_string':True,'conditional_generation_and_IP_hypotheses':True}

def main():
    arg=argparse.ArgumentParser(); arg.add_argument('--output',default='phase15_unitary_witnesses_independent_check.json'); options=arg.parse_args()
    start=time.time(); directory=Path(__file__).resolve().parent
    wp=directory/'phase15_unitary_witnesses.json'; sp=directory/'phase15_unitary_sieve_independent_check.json'
    data=json.loads(wp.read_text()); sieve=json.loads(sp.read_text()); records=data['witnesses']
    assert len(records)==1699 and len({r['q'] for r in records})==1699
    assert sorted(r['q'] for r in records)==sieve['exceptions']
    primitive=[]; irreducible_fields=set(); full_degree=0
    for record in records:
        q,p,e=record['q'],record['p'],record['exponent']; assert q==p**e and q>=7 and q%4==3 and e%2==1
        if record['kind']!='primitive_norm': continue
        F=Base(p,record['base_polynomial']); assert F.q==q and F.n==e
        E=Quadratic(F); lam=(F.read(record['lambda_real']),F.read(record['lambda_imaginary']))
        assert lam!=E.zero and E.power(lam,q)==E.bar(lam)
        N=q*q-1; primes=prime_factors(N)
        assert record['primitive_order']==N and record['prime_divisors']==primes
        assert E.power(lam,N)==E.one
        for ell in primes: assert E.power(lam,N//ell)!=E.one
        inv=E.power(lam,N-1); assert E.mul(lam,inv)==E.one
        u=E.sub(lam,inv); assert E.norm(u)==F.constant(-2)
        assert E.norm(lam)==F.read(record['norm_lambda'])
        a=E.sub(E.bar(u),u); assert a==(F.zero,F.read(record['parameter_t']))
        aa=E.mul(a,a); assert a!=E.zero and aa[1]==F.zero
        assert aa[0] not in (F.constant(8),F.constant(-1))
        # Directly check the four eigenvalue roots and their projective order.
        roots=[lam,E.neg(inv),E.neg(E.bar(lam)),E.bar(inv)]; assert len(set(roots))==4
        for r in roots:
            assert E.add(E.sub(E.add(E.power(r,4),E.mul(a,E.power(r,3))),E.mul(a,r)),E.one)==E.zero
        from math import gcd
        exponents=[1,N//2-1,N//2+q,-q]
        g=N
        for exponent in exponents[1:]: g=gcd(g,exponent-exponents[0])
        assert g==2
        if q>=27:
            for ell in prime_factors(e): assert F.power(aa[0],p**(e//ell))!=aa[0]
            full_degree+=1
        irreducible_fields.add((p,tuple(record['base_polynomial'])))
        primitive.append(q)
    direct=[r for r in records if r['kind']=='direct_parameter']; assert [r['q'] for r in direct]==[19,43]
    specials=data['special_parameters']; assert [r['q'] for r in specials]==[19,23,43]
    for r in direct: assert r in specials
    direct_results=[direct_check(r) for r in specials]
    assert len(primitive)==1697
    report={'status':'PASS','checker_sha256':sha(Path(__file__)),'witness_sha256':sha(wp),'independent_sieve_sha256':sha(sp),'field_list_matches_independent_sieve':True,'field_count':len(records),'primitive_norm_records':len(primitive),'direct_parameter_records_in_sieve':len(direct),'distinct_field_presentations_verified':len(irreducible_fields),'full_square_field_checks_q_at_least_27':full_degree,'arithmetic':'Independent standard-library polynomial quotient arithmetic, Rabin irreducibility, i^2=-1 quadratic extension, trial-division exact multiplicative orders. No GAP or author checker imported.','primitive_checks':['Prime characteristic and irreducible base polynomial','Exact primitive order q^2-1 via all prime divisors','Norm(lambda-lambda^-1)=-2','Exported norm and t coordinates','Four distinct quartic roots and projective order (q^2-1)/2','Full square field for q>=27'],'direct_results':direct_results,'small_field_boundary':{'q7':'Full frozen phase14 group/IP certificate retained; not rerun here.','q11':'Full phase15 group/IP certificate retained; not rerun here.','q23':'Direct parameter hypotheses verified here.'},'scope':'Exact finite parameter arithmetic and coverage only; uniform character bounds, sieve proof, generation, and intersection theorems require their separate written audits. No subgroup closures or all-subset intersections are computed here.','elapsed_seconds':round(time.time()-start,6)}
    output=Path(options.output)
    if not output.is_absolute(): output=directory/output
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
