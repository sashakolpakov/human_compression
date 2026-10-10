#!/usr/bin/env python3
"""Exact prime sieve, primorial bootstraps, and complete small-field intake."""
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
import math

Q0=3715232694272
CUTOFF=98660
spf=list(range(CUTOFF+2))
for p in range(2,math.isqrt(CUTOFF+1)+1):
    if spf[p]!=p:continue
    for n in range(p*p,CUTOFF+2,p):
        if spf[n]==n:spf[n]=p
primes=[p for p in range(2,CUTOFF+2) if spf[p]==p]
oddprimes=[p for p in primes if p>2]

def factor(n):
    ans={}
    while n>1:
        p=spf[n];ans[p]=ans.get(p,0)+1;n//=p
    return ans

def bound(ps,c):
    w=len(ps)
    if c==w:return Fraction(8*2**c-6),Fraction(1)
    delta=1-sum((Fraction(1,p) for p in ps[c:]),Fraction(0))
    if delta<=0:return None
    A=8*2**c*(2+Fraction(w-c-1,1)/delta)-6
    return A,delta

boot=[]
Q=Q0
for w,c,B in [(17,2,2135383),(10,1,255289),(9,1,160372),(8,1,98660)]:
    P=math.prod(oddprimes[:w+1])
    assert 8*P>=Q*Q
    A,delta=bound(oddprimes[:w],c)
    assert A>2 and delta>0 and math.ceil((A+1)**2)==B
    boot.append({'old_cutoff':Q,'omega_max':w,'core_prime_count':c,
                 'first_excluded_primorial':P,'delta':[delta.numerator,delta.denominator],
                 'coefficient':[A.numerator,A.denominator],'new_cutoff':B})
    Q=B
assert Q==CUTOFF

fields={}
for p in primes:
    if p<5:continue
    q=p;e=1
    while q<CUTOFF:
        if q%4==1:
            assert q not in fields
            fields[q]=(p,e)
        q*=p;e+=1

records=[]; exceptions=[]
for q,(p,e) in sorted(fields.items()):
    fm,fn=factor(q-1),factor(q+1)
    assert math.prod(r**a for r,a in fm.items())==q-1
    assert math.prod(r**a for r,a in fn.items())==q+1
    ps=sorted((set(fm)|set(fn))-{2})
    witness=None
    for c in range(len(ps)+1):
        bd=bound(ps,c)
        if bd is None:continue
        A,delta=bd
        margin=Fraction((q-3)**2)-q*A*A
        if margin>0:
            witness={'core_prime_count':c,'delta':[delta.numerator,delta.denominator],
                     'coefficient':[A.numerator,A.denominator],
                     'squared_margin':[margin.numerator,margin.denominator]}
            break
    if witness is None:exceptions.append(q)
    records.append({'q':q,'p':p,'exponent':e,'odd_prime_support':ps,'sieve_certificate':witness})
assert len(fields)==4795 and len(exceptions)==406 and max(exceptions)==43889

b=Path(__file__).resolve().parent
report={'status':'PASS','executed_at_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Exact arithmetic, complete prime-power intake and prime-sieve positivity only; no field witness or character-sum proof certified here.',
        'bootstrap':boot,'field_count':len(fields),'exception_count':len(exceptions),
        'exceptions':exceptions,'field_records':records,
        'input_sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in [Path(__file__).resolve(),b/'phase13_unitary_sieve.md']}}
(b/'phase13_unitary_sieve_check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: four exact primorial bootstraps;4795eligiblefields;406witnesscases;max43889.')
