"""Exceptional inequalities allowing outer involutory reversers.

Arithmetic only until the explicit group-theoretic interfaces are reviewed.
This edition uses kappa = number of square-one elements in Aut(G)/Inndiag(G),
not an assertion that every automorphism centralizing x is inner-diagonal.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
from fractions import Fraction as F
from math import comb, prod
from pathlib import Path
import json
from exceptional_lower_bounds import add, mul, mon as mono, scale, product, orders, sl


def mon(n, c=1):
    return scale(mono(n), F(c))


def power(p, n):
    return product([p] * n)


def shift(p, m):
    return [sum(p[i] * comb(i, j) * m ** (i-j) for i in range(j, len(p)))
            for j in range(len(p))]


def serial(p):
    return [[F(x).numerator, F(x).denominator] for x in p]


rows = []


def row(name, variable, minimum, L, T, C, B, W, kappa):
    delta = add(L, scale(add(add(scale(mul(T, C), kappa), B), scale(T, W)), -1))
    translated = shift(delta, minimum)
    if translated[0] <= 0 or any(x < 0 for x in translated):
        raise ValueError((name, translated[0], [i for i, x in enumerate(translated) if x < 0]))
    rows.append(dict(name=name, variable=variable, minimum=minimum,
                     lower=serial(L), torus_upper=serial(T), mu_upper=serial(C),
                     other_maximals_upper=serial(B), weyl_order=W, kappa=kappa,
                     difference=serial(delta), shifted_coefficients=serial(translated)))


q, one = mon(1), mon(0)
phi30 = [F(x) for x in [1,1,0,-1,-1,-1,0,1,1]]
phi18 = add(add(mon(6), mon(3, -1)), one)
phi9 = add(add(mon(6), mon(3)), one)
phi12 = add(add(mon(4), mon(2, -1)), one)
phi6 = add(add(mon(2), mon(1, -1)), one)
row('E8', 'q', 2, mon(128,F(1,2)), phi30,
    scale(mul(mon(84),add(mon(20),mon(19))),2), mon(0,0),
    prod([2,8,12,14,18,20,24,30]),2)
row('E7', 'q', 2, mon(70,F(1,4)), mul(phi18,add(q,one)),
    scale(mul(mon(42),add(mon(12),mon(11))),2),
    scale(mul(add(q,one),add(mon(42),mon(41))),2),2903040,2)
row('E6 both signs', 'q', 2, mon(40,F(1,2)),phi9,
    scale(add(mon(28),mon(27)),2),scale(add(mon(15),mon(12)),2),51840,4)
row('F4 q>=3', 'q', 3, mon(28,F(1,2)),phi12,mon(22),
    scale(add(mon(16),mon(15)),4),1152,2)
row('G2 q>=5', 'q', 5, mon(8,F(1,2)),phi6,mon(5),
    scale(add(mon(5),mon(4)),6),12,2)
row('3D4 q>=4', 'q', 4,mon(16,F(1,2)),phi12,mon(11),mon(0,0),192,2)
s=mon(1);q=scale(power(s,2),2)
T=add(add(add(add(power(q,2),scale(mul(s,q),2)),q),scale(s,2)),one)
row('2F4', 's, q=2s^2', 2,scale(power(q,14),F(1,2)),T,power(q,11),mon(0,0),1152,1)
T=add(add(q,scale(s,2)),one)
row('Suzuki', 's, q=2s^2', 2,mul(add(q,[-1]),add(power(q,2),one)),
    T,add(q,[-1]),mon(0,0),8,1)
q=scale(power(s,2),3);T=add(add(q,scale(s,3)),one)
row('small Ree','s, q=3s^2',3,scale(power(q,4),F(1,2)),T,
    scale(power(q,2),2),mon(0,0),12,1)

fixed=[]
for q0 in (2,3):
    L=F(q0**16,2);T=q0**4-q0**2+1;C=q0**11
    margin=L-T*C-192*T
    if margin<=0:raise ValueError('small triality margin')
    fixed.append(dict(name='3D4('+str(q0)+')',lower=str(L),torus=T,mu=C,
                      kappa=1,other_maximals=0,normalizer=192*T,margin=str(margin)))
q0=2
G=sum(c*q0**i for i,c in enumerate(orders['F4']))
C=q0**18*(q0*(q0*q0-1))**2
if G%C:raise ValueError('nonintegral class')
L=G//C;T=17;mu=q0**22;B=4*(q0**20+q0**19);N=1152*T
margin=L-2*T*mu-B-N
if margin<=0:raise ValueError('F4(2) margin')
fixed.append(dict(name='F4(2)',lower=L,torus=T,mu=mu,kappa=2,
                  other_maximals=B,normalizer=N,margin=margin))

report=dict(status='PASS_CONDITIONAL_COSET_ARITHMETIC',rows=rows,fixed=fixed,
            group_interfaces='Pending proof and independent review; not inferred by this arithmetic',
            whole_original_credit=0)
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(rows),'polynomial families and',len(fixed),'fixed cases')
