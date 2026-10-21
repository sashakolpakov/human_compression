"""Finite order obstructions in the proof; not a subgroup computation."""
from math import gcd,isqrt
import json
from pathlib import Path

def is_prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))

def prime_power(n):
    for p in range(2,n+1):
        if not is_prime(p):continue
        v=p
        while v<n:v*=p
        if v==n:return True
    return False

def rows(projective,b):
    bound=b*((2 if projective else 1)*b+1)
    # For all t>=32, the group order is at least (t^3-t)/2,
    # which exceeds the largest bound7260 and increases with t.
    if (32**3-32)//2<=bound:raise ValueError('Insufficient finite cutoff')
    out=[]
    for t in range(4,32):
        if not prime_power(t) or (projective and (t%2==0 or t<5)):continue
        n=t*(t*t-1)//gcd(2,t-1)
        if n>bound or n<=b or n%b:continue
        d=n//b
        out.append(dict(t=t,group_order=n,intersection_order=b,index=d,
                        required_dividend=(2 if projective else 1)*b,
                        divisibility_passes=((2 if projective else 1)*b)%(d-1)==0))
    return out

report=dict(status='FINITE_ORDER_OBSTRUCTIONS_EVALUATED',cutoff=32,
            scope='All prime powers within the elementary order bounds; existence and fusion require the written proof.',
            cases=[dict(projective=projective,intersection_order=b,rows=rows(projective,b))
                   for projective in [False,True] for b in [12,24,60]],
            subgroup_searches=0,whole_source_credit=0)
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():raise ValueError('Fresh result required')
    a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],cases=len(report['cases']))))
