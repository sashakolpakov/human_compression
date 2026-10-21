#!/usr/bin/env python3
"""Exact controls for the written all-degree class estimates, not their proof."""
import sys
if sys.flags.optimize:
    raise RuntimeError('optimized execution is not accepted')
import argparse
import json
from fractions import Fraction as F
from math import prod
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def gl(n, q):
    return q**(n*(n-1)//2)*prod(q**i-1 for i in range(1,n+1))

def gu(n, q):
    return q**(n*(n-1)//2)*prod(q**i-(-1)**i for i in range(1,n+1))

def sp(m, q):
    """Sp_(2m)(q), including Sp_0=1."""
    return q**(m*m)*prod(q**(2*i)-1 for i in range(1,m+1))

def orth_even(m, q, sign):
    return 2*q**(m*(m-1))*(q**m-sign)*prod(q**(2*i)-1 for i in range(1,m))

def orth_odd(m, q):
    return 2*sp(m,q)

def symmetric_isometries(k,q):
    if k%2:
        return sp((k-1)//2,q)
    return q**(k-1)*sp((k-2)//2,q)

def symplectic_nonalt_class(m,k,q):
    u=(4*m*k-3*k*k+k)//2
    return F(sp(m,q),q**u*sp(m-k,q)*symmetric_isometries(k,q))

def linear_bound(n,q,unitary):
    g=gu if unitary else gl
    k,l=divmod(n,2)
    if q%2==0:
        return F(g(n,q),q**(k*(2*n-3*k))*g(k,q)*g(l,q)), 'unipotent'
    if n%2:
        k=min((j for j in range(2,n,2)),key=lambda j:abs(2*j-n))
        return F(g(n,q),g(k,q)*g(n-k,q)), 'semisimple_unbalanced'
    if k%2==0:
        return F(g(n,q),2*g(k,q)**2), 'semisimple_balanced'
    split=(q%4==3) if unitary else (q%4==1)
    if split:
        return F(g(n,q),2*g(k,q)**2), 'scalar_balanced'
    return F(g(n,q),2*gl(k,q*q)), 'quadratic_centralizer'

def symplectic_bound(m,q):
    if q%2==0:
        return symplectic_nonalt_class(m,m,q)
    return F(sp(m,q),2*(gl(m,q) if q%4==1 else gu(m,q)))

def odd_orthogonal_bound(m,q):
    a=(m if m%2==0 else m+1)//2
    b=m-a
    sign=(-1 if q%4==3 else 1)**a
    return F(orth_odd(m,q),orth_even(a,q,sign)*orth_odd(b,q))

def even_orthogonal_bound(m,q,sign):
    if q%2==0:
        k=m if m%2==0 else m-1
        return symplectic_nonalt_class(m,k,q)*F(q**(m-k),q**m+sign)
    a=m//2
    b=m-a
    first=(-1 if q%4==3 else 1)**a
    second=sign*first
    fusion=2 if a==b else 1
    return F(orth_even(m,q,sign),fusion*orth_even(a,q,first)*orth_even(b,q,second))

def unitary_four_exact(q):
    need(q%4==3,'this formula is for q=3 mod 4')
    balanced=F(q**4*(q*q-q+1)*(q*q+1),2)
    unbalanced=q**3*(q-1)*(q*q+1) if q%8==7 else 0
    return balanced+unbalanced

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    a=parser.parse_args();need(not a.out.exists(),'output already exists')
    rows=[]
    fields=[2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,31,32,49,64]
    def record(family,rank,q,lower,power):
        need(lower.denominator in (1,2),'unexpected orbit denominator')
        need(lower>F(q**power,4),f'quarter bound fails for {family,rank,q}')
        rows.append({'family':family,'rank_parameter':rank,'q':q,'lower_numerator':lower.numerator,'lower_denominator':lower.denominator,'exponent':power})
    for q in fields:
        for n in range(4,25):
            for unitary in (False,True):
                lower,_=linear_bound(n,q,unitary)
                record('PSU' if unitary else 'PSL',n,q,lower,n*n//2)
        for m in range(2,15):
            record('PSp',m,q,symplectic_bound(m,q),m*m+m)
        if q%2:
            for m in range(3,15):
                record('Omega_odd',m,q,odd_orthogonal_bound(m,q),m*m+m)
        for m in range(4,15):
            for sign in (1,-1):
                record('Omega_even_'+str(sign),m,q,even_orthogonal_bound(m,q,sign),m*m-1)
    exact=[]
    for q in fields:
        if q%4==3:
            value=unitary_four_exact(q)
            need(value.denominator==1,'nonintegral U4 formula')
            need(value<F(q**8,2),'source half bound unexpectedly holds')
            exact.append({'q':q,'involutions':int(value),'source_half_bound':str(F(q**8,2))})
    need(unitary_four_exact(3)==2835,'U4(3) ordinary-table control')
    need(unitary_four_exact(7)==2683975,'U4(7) literal arithmetic')
    need(symplectic_nonalt_class(2,2,2)==45,'Sp4(2) double-transposition class')
    need(symplectic_nonalt_class(3,3,2)==3780,'Sp6(2) full-rank class')
    report={'status':'PASS_EXACT_ARITHMETIC_CONTROLS_ONLY','rows':rows,'number_of_rows':len(rows),'unitary_four_correction':exact,'mathematical_scope':'The written product estimates prove all ranks and fields; these samples are controls, not premises.'}
    a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],len(rows),'class controls',len(exact),'U4 controls')

if __name__=='__main__':
    main()
