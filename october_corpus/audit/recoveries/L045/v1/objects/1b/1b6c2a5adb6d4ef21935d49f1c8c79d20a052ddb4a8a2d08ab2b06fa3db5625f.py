#!/usr/bin/env python3
"""Exact controls for the written symplectic inequalities; not a rank census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('optimized execution is not accepted')
from fractions import Fraction as F
from pathlib import Path
import argparse,json
from lower_bounds import symplectic_bound

def need(test,message):
    if not test:raise ValueError(message)

def primes(n):
    return [r for r in range(2,n+1) if n%r==0 and all(r%d for d in range(2,int(r**.5)+1))]

def sp_upper(r,q):
    if r==0:return 0
    if r==1:return q*q-1
    if (r,q)==(2,2):return 75
    return 2*(q**(r*r+r)+q**(r*r+r-1))

def j_solutions(m,q):
    if m%2:return sp_upper((m-1)//2,q)+1
    if m==2:return q
    if m==4:return q**4+q**3-q*q
    return q**(m-1)+q**(m-2)*sp_upper((m-2)//2,q)

def bounds(m,q):
    if q%2:
        if m==2:
            mu=F((q+1)*(q*q+1),2)+q*q+q+1
        else:
            a=(m*m+m-2)//2
            mu=(q+1)*(2*(q**a+q**(a-1))+1)-1
        cosets=1
    else:
        mu=2*q**3-q*q-1 if m==2 else q**(m*(m+1)//2)*j_solutions(m,q)-1
        cosets=2 if m==2 else 1
    cover=sum(2*(q**(m*m//r+m)+q**(m*m//r+m-r)) for r in primes(m))
    if not q%2:cover+=2*(q**(m*m)+q**(m*m-1))
    reverse=cosets*(q**m+1)*mu
    return {'centralizer_bound':mu,'cosets':cosets,'cover_bound':cover,'reversing_bound':reverse,'total':reverse+cover}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'output exists')
    fields=[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,31,32,49,64]
    finite={(2,2),(2,3),(2,4),(3,2),(3,3),(3,4),(4,2),(4,3),(4,4)}
    rows=[]
    for m in range(2,41):
        for q in fields:
            if (m,q) in finite:continue
            b=bounds(m,q);lo=symplectic_bound(m,q)
            need(lo>b['total'],f'count inequality {(m,q)}')
            if m>=3:
                generic=F(q**(m*m+m),4) if q%2 else F(2*q**(m*m+m),3)
                need(generic>b['total'],f'generic inequality {(m,q)}')
            rows.append({'m':m,'q':q,'lower_numerator':lo.numerator,'lower_denominator':lo.denominator,**{k:str(v) for k,v in b.items()}})
    # Exact degree-four final polynomial lower margin, all coefficients
    # after q=z+8 are nonnegative. Coefficient arithmetic is independent
    # of the finite field list above.
    from math import comb
    terms={6:1,5:-4,4:-3,3:-4,2:-1,0:3}
    shifted=[sum(c*comb(i,j)*8**(i-j) for i,c in terms.items() if i>=j) for j in range(7)]
    need(all(x>=0 for x in shifted)and shifted[0]>0,'even degree-four universal margin')
    # q^3-3q^2-3q-3 at q=z+5, for odd degree-four mu<q^3.
    terms2={3:1,2:-3,1:-3,0:-3}
    shifted2=[sum(c*comb(i,j)*5**(i-j) for i,c in terms2.items() if i>=j) for j in range(4)]
    need(all(x>=0 for x in shifted2)and shifted2[0]>0,'odd degree-four mu')
    report={'status':'PASS_EXACT_SYMPLECTIC_INEQUALITY_CONTROLS','rows':rows,'number_of_rows':len(rows),'q8_shifted_margin':shifted,'q5_shifted_centralizer_margin':shifted2,'classification_cover':'EXPLICIT_CONDITIONAL_INPUT; not certified by these samples','scope':'The written estimates prove all ranks and fields; controls do not replace the proof.'}
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(rows))
if __name__=='__main__':main()
