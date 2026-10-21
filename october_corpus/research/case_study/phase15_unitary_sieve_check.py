#!/usr/bin/env python3
"""Exact phase15 prime-support bootstrap and exhaustive field intake."""
from fractions import Fraction as F
from math import prod,isqrt,ceil
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
CUTOFF=1029254
spf=list(range(CUTOFF+2))
for p in range(2,isqrt(CUTOFF+1)+1):
    if spf[p]==p:
        for n in range(p*p,CUTOFF+2,p):
            if spf[n]==n:spf[n]=p
primes=[p for p in range(2,CUTOFF+2) if spf[p]==p]
C6=prod((F(64,p) for p in primes if p<64),start=F(1))
Q=ceil(8**6*C6)
assert Q==725311328745792

def factor(n):
    out={}
    while n>1:
        p=spf[n];out[p]=out.get(p,0)+1;n//=p
    return out

def bound(ps,c,C=8,genus=1):
    w=len(ps)
    if c==w:return F(C*2**c-C+2*genus),F(1)
    delta=1-sum((F(1,p) for p in ps[c:]),F(0))
    if delta<=0:return None
    return C*2**c*(2+F(w-c-1)/delta)-C+2*genus,delta

boot=[]
for w,c,B in [(21,3,16427566),(12,2,1574926),(11,2,1029254)]:
    P=prod(primes[:w+1]);assert P>=Q*Q
    A,d=bound(primes[:w],c)
    assert A>0 and d>0 and ceil(A*A)==B
    boot.append({'previous_cutoff':Q,'omega_max':w,'core_prime_count':c,
                 'excluded_primorial':P,'delta':[d.numerator,d.denominator],
                 'coefficient':[A.numerator,A.denominator],'new_cutoff':B})
    Q=B
assert Q==CUTOFF
fields={}
for p in primes:
    if p%4!=3:continue
    q=p;e=1
    while q<CUTOFF:
        if e%2 and q>=7:fields[q]=(p,e)
        q*=p;e+=1
records=[];exceptions=[]
for q,(p,e) in sorted(fields.items()):
    fm,fn=factor(q-1),factor(q+1)
    ps=sorted(set(fm)|set(fn)); C,genus=(2,0) if p==3 else (8,1)
    cert=None
    for c in range(len(ps)+1):
        bd=bound(ps,c,C,genus)
        if bd is None:continue
        A,d=bd; margin=F((q+1)**2)-q*A*A
        if margin>0:
            cert={'core_prime_count':c,'delta':[d.numerator,d.denominator],
                  'coefficient':[A.numerator,A.denominator],
                  'squared_margin':[margin.numerator,margin.denominator]}
            break
    if cert is None:exceptions.append(q)
    records.append({'q':q,'p':p,'exponent':e,'minus_factors':fm,'plus_factors':fn,
                    'character_bound':C,'sieve_certificate':cert})
assert len(fields)==40389 and len(exceptions)==1699 and max(exceptions)==245519
base=Path(__file__).resolve().parent
report={'status':'PASS','executed_at_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'Exact rational arithmetic and exhaustive finite field-size intake only; the curve and character bounds are retained written proofs.',
        'initial_C_sixth_power':[C6.numerator,C6.denominator],
        'initial_cutoff':725311328745792,'bootstrap':boot,'field_count':len(fields),
        'exception_count':len(exceptions),'exceptions':exceptions,'field_records':records,
        'input_sha256':{Path(__file__).name:sha256(Path(__file__).read_bytes()).hexdigest()}}
(base/'phase15_unitary_sieve_check.json').write_text(json.dumps(report,indent=2)+'\n')
(base/'phase15_unitary_exceptions.g').write_text('phase15fields := '+str([[q,*fields[q]] for q in exceptions])+';;\n')
print('PASS: 3 bootstraps;40389 fields;1699 exceptions;largest245519.')
