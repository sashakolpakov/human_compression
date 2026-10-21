from math import gcd
import json

def factors(q):
    assert q > 0 and q & (q-1) == 0
    n=q.bit_length()-1
    assert n>=3 and n%2
    t=1<<((n+1)//2)
    return q-1,q+t+1,q-t+1

rows=0
for n in range(3,102,2):
    q=1<<n;a,b,c=factors(q)
    assert b*c==q*q+1
    assert gcd(a,b)==gcd(a,c)==gcd(b,c)==1
    rows+=1
subfields=0
for d in range(3,32,2):
    s=1<<d;t=1<<((d+1)//2);m=s*s+1
    for r in range(1,32,2):
        q=s**r;a,b,c=factors(q)
        assert (q*q+1)%m==0
        for eps,value in [(1,b),(-1,c)]:
            residues={1:1+s+eps*t,3:1-s+eps*s*t,
                      5:1+s-eps*t,7:1-s-eps*s*t}
            z=residues[r%8]
            assert 0<abs(z)<m and (value-z)%m==0 and value%m
        if r>1:
            assert a%(s-1)==0 and 1<s-1<a
            for value in [b,c]:
                h=gcd(m,value)
                assert 1<h<value
        subfields+=1
assert factors(8)[0]==7  # q=s=8, r=1: the literal unqualified Lemma3.2 fails.
print(json.dumps(dict(status='PASS_L115_ARITHMETIC_CONTROLS',odd_exponents=rows,
                     subfield_parameters=subfields,domain_boundary_example={'s':8,'r':1,'q_minus_one':7},
                     source_credit=0,role='finite controls, not proof of the general theorem')))
