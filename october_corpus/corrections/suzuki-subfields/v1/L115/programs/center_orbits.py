"""Exact scalar-subspace controls; no enumeration of a Suzuki group."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python')
from pathlib import Path
import json
from collections import Counter

def need(ok, why):
    if not ok: raise ValueError(why)

def remainder(a,b):
    while a.bit_length()>=b.bit_length():
        a^=b<<(a.bit_length()-b.bit_length())
    return a

def gcd(a,b):
    while b: a,b=b,remainder(a,b)
    return a

def run(n,modulus):
    q=1<<n
    def mul(a,b):
        c=0
        while b:
            if b&1:c^=a
            b>>=1;a<<=1
            if a&q:a^=modulus
        return c
    def power(a,k):
        b=1
        while k:
            if k&1:b=mul(a,b)
            a=mul(a,a);k>>=1
        return b
    primes=[p for p in range(2,n+1) if n%p==0 and all(p%d for d in range(2,p))]
    need(power(2,q)==2,'Frobenius identity')
    for p in primes:need(gcd(power(2,1<<(n//p))^2,modulus)==1,'Rabin irreducibility')
    K={a for a in range(q) if power(a,8)==a}
    need(len(K)==8,'base field')
    remaining=set(range(q))-K;spaces={};owner={}
    while remaining:
        c=min(remaining)
        W=frozenset(a^mul(b,c) for a in K for b in K)
        need(len(W)==64 and K<W and not (set(W)-K-set(remaining)),'disjoint quotient lines')
        spaces[c]=W
        for a in W-K:owner[a]=c
        remaining-=W
    need(len(spaces)==(q-8)//56,'all two-dimensional subspaces')
    permutation={}
    for c,W in spaces.items():
        image=frozenset(mul(a,a) for a in W)
        target=owner[mul(c,c)]
        need(image==spaces[target],'Frobenius image')
        permutation[c]=target
    need(set(permutation.values())==set(spaces),'Frobenius permutation')
    todo=set(spaces);orbits=[]
    while todo:
        start=min(todo);orbit=[start];at=permutation[start]
        while at!=start:
            need(at not in orbit,'permutation cycle');orbit.append(at);at=permutation[at]
        todo-=set(orbit);orbits.append(orbit)
    fixed=[]
    for k in range(n):
        count=0
        for start in spaces:
            at=start
            for _ in range(k):at=permutation[at]
            count+=at==start
        fixed.append(count)
    need(sum(fixed)==n*len(orbits),'Burnside count')
    return dict(n=n,q=q,base_field=sorted(K),modulus=modulus,
                scalar_subspaces=len(spaces),frobenius_orbits=len(orbits),
                orbit_sizes=dict(sorted(Counter(map(len,orbits)).items())),
                fixed_counts=fixed,orbit_representatives=[o[0] for o in orbits],
                source_mixed_order=q*8*7,corrected_cover_order=8**3*7,
                borel_order=8**2*7,local_degrees=[65,8])

if __name__=='__main__':
    rows=[run(9,(1<<9)|(1<<4)|1),run(15,(1<<15)|(1<<1)|1)]
    report=dict(status='PASS_SCALAR_SUBSPACE_CONTROLS',cases=rows,
                scope='Supplementary exact field calculations, not a Suzuki subgroup census or a whole-original disposition.')
    Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
