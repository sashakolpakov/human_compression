"""Exact arithmetic controls for the written orthogonal inequalities.

Finite controls supplement the monotonicity proof; they are not a proof
of the infinite ranges or of a maximal subgroup classification.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
from fractions import Fraction as F
from itertools import product
from math import gcd
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

def power(q, n):
    return F(q ** n) if n >= 0 else F(1, q ** (-n))

def odd_b(m, q):
    return (18*(1+power(q,-m))*power(q,-m*(m-1)//2)
            +6*power(q,-m)+4*m*(1+power(q,-m))*power(q,-m*m))

def odd_d(m,q):
    d=m*m-1
    return sum((36*power(q,m+2*(m*m//4)-d),
                16*power(q,m*m-2*m+2-d),
                11*power(q,(m*m+m)//2-d),
                8*m*power(q,m*m//2-d),6*m*power(q,m-d)))

def even_d(m,q):
    d=m*m-1
    e=(3*m*m-2*m-1)//4 if m%2 else (3*m*m-4)//4
    return sum((8*power(q,e+m-d),18*power(q,m*m-2*m+2-d),
                12*power(q,(m*m+m)//2-d),8*m*power(q,m*m//2-d),
                8*m*power(q,m-d)))

def d4(kind,q):
    t=(q**3+1)*(q+1)
    if kind=='minus_odd':
        value=24*(q**4+1)*q**8+8*q**8+16*(q**4+1)
    elif kind=='even':
        value=q**11*t+20*(q+1)*q**9+32*q**8+16*t
    elif kind=='plus_generic':
        value=24*t*q**8+20*(q+1)*q**9+16*t
    elif kind=='plus_five':
        need(q==5,'special field');value=48*t*q**8+18*q**12+20*(q+1)*q**9+16*t
    else:raise ValueError('unknown case')
    return F(value,q**16)

def spectra(q,u):
    a=q**3+1;b=q*q-q+1;m=a if q%2==0 else a//2
    half=lambda n:(n*pow(2,-1,a))%m if q%2==0 else n//2%m
    need(q%2==0 or u%2==1,'integral odd half weights')
    basis=[1,q,q*q,u*b]
    natural=sorted((s*v)%m for v in basis for s in [-1,1])
    generic=u%(q+1)not in (1,q)
    records=[]
    for parity,eps in [(0,1),(1,-1)]:
        literal=sorted(half(sum(s*v for s,v in zip(signs,basis)))
                       for signs in product([-1,1],repeat=4)
                       if sum(s==-1 for s in signs)%2==parity)
        c=half(1+q+q*q+eps*u*b);d=half((1-eps*u)*b)
        proposed=sorted([(c*pow(q,j,m))%m for j in range(6)]+[d,(-d)%m])
        need(literal==proposed,'complete signed weight list')
        need(c%b==q%b,'large representative mod cyclotomic factor')
        if generic:
            need(literal!=natural and 0 not in literal,'generic separation and no scalar eigenspace')
        records.append(proposed)
    if q==5 and u==1:
        need(records[1]==natural and records[0].count(0)==2,'q5 distinguished module')
        need(half(1+5+25+21)==26 and gcd(26,63)==1,'q5 large eigenvalue order')
    return 2

def main():
    base=[]
    for kind,m,q,fn,cap in [
        ('odd_B',3,5,odd_b,F(194,1000)),('odd_B',4,3,odd_b,F(1,10)),
        ('odd_D',5,3,odd_d,F(25,1000)),
        ('even_D',5,4,even_d,F(127,1000)),('even_D',6,4,even_d,F(127,1000)),
        ('even_D',7,2,even_d,F(41,1000))]:
        v=fn(m,q);need(v<cap,'written base margin')
        base.append(dict(kind=kind,m=m,q=q,value=str(v),decimal=float(v),written_cap=str(cap)))
    for kind,q,cap in [('minus_odd',3,F(302,1000)),('even',4,F(324,1000)),
                       ('plus_generic',7,F(12,1000)),('plus_five',5,F(124,1000))]:
        v=d4(kind,q);need(v<cap,'written D4 base margin')
        base.append(dict(kind=kind,q=q,value=str(v),decimal=float(v),written_cap=str(cap)))
    arithmetic=0
    for q in range(2,41):
        for m in range(3,31):
            if q%2 and (m>=4 or q>=5):need(odd_b(m,q)<F(1,4),'B range');arithmetic+=1
            if m>=5 and q%2:need(odd_d(m,q)<F(1,4),'odd D range');arithmetic+=1
            if m>=5 and q%2==0 and (m>=7 or q>=4):need(even_d(m,q)<F(1,4),'even D range');arithmetic+=1
            if m>=4:
                need((F(q**m+1,m)-1)**3>q**m,'extension-power degree inequality');arithmetic+=1
                if q%2:need((F(q**m+1,4)-1)**3>q**m,'odd multiplier degree');arithmetic+=1
    signed_lists=0;units=0
    for q in range(3,102):
        b=q*q-q+1
        need(pow(q,6,b)==1 and all(pow(q,j,b)!=1 for j in [1,2,3]),'cyclotomic order six')
        for u in range(1,q+1):
            if gcd(u,q+1)==1:signed_lists+=spectra(q,u);units+=1
    fields=0
    for p in [2,3,5,7,11]:
        for h in range(1,5):
            q=p**(2*h);b=q*q-q+1
            need(all((p**h*q-pow(q,j,b))%b for j in range(6)),'field plus diagram exclusion')
            fields+=1
    lower=[]
    for q in [2,4,8,16,32,64]:
        plus=F(q*q*(q**4-1)**2*(q**6-1),q**16)
        minus=F(q*q*(q**8-1)*(q**6-1),q**16)
        need(minus>plus>F(1,2),'actual even D4 orbit margin')
        lower.append(dict(q=q,plus=str(plus),minus=str(minus)))
    print(json.dumps(dict(status='PASS_FINITE_ORTHOGONAL_ARITHMETIC_CONTROLS',
                         written_base_margins=base,integer_parameter_checks=arithmetic,
                         triality_unit_choices=units,complete_signed_weight_lists=signed_lists,
                         field_diagram_controls=fields,even_D4_lower_controls=lower,
                         classification_claim=False,uniform_proof='written monotonicity, not finite controls')))

if __name__=='__main__':main()
