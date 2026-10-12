#!/usr/bin/env python3
"""Optional finite diagnostics. These do not prove any uniform statement."""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import gcd
import json

def need(ok, msg):
    if not ok: raise ValueError(msg)
def phi(n): return sum(gcd(i,n)==1 for i in range(1,n+1))
def evaluate(poly,x,p):
    result=0
    for c in reversed(poly): result=(result*x+c)%p
    return result
def divide(a,b):
    r=a[:];q=[0]*(len(a)-len(b)+1)
    while len(r)>=len(b):
        k=len(r)-len(b);v=r[-1];q[k]=v
        for j,c in enumerate(b):r[k+j]-=v*c
        while r and not r[-1]:r.pop()
    need(not r,'nonexact cyclotomic division');return q
def cyclotomics(bound):
    out={}
    for n in range(1,bound+1):
        a=[-1]+[0]*(n-1)+[1]
        for d in range(1,n):
            if n%d==0:a=divide(a,out[d])
        out[n]=a
    return out
def character(x,p):
    v=pow(x%p,(p-1)//2,p)
    return -1 if v==p-1 else v
def order(x,p):
    v=x%p;d=1
    while v!=1:v=v*x%p;d+=1
    return d
def run():
    degree_cases=0
    for p in [3,5,7,11]:
        for m in range(2,51):
            indices=[i for i in range(1,m) if i%p]
            T=1+len(indices);A=sum(indices);K=Fraction(p*T*(T-1),2*(p-1))
            s=sum(phi(i) for i in indices);S=sum(phi(2*i) for i in indices)
            u,v=divmod(m-1,p)
            need(K-A==Fraction(p*u,2)+Fraction(v*(v+1),2*(p-1)),'block subtraction')
            need(s<=S<=A<=K,'degree inequalities');degree_cases+=1
    polynomials=cyclotomics(10);records=[]
    for p in [17,23,31,41,1009]:
        for m in range(2,6):
            indices=[i for i in range(1,m) if i%p];T=len(indices)+1
            K=Fraction(p*T*(T-1),2*(p-1))
            for sign in [1,-1]:
                if sign==-1 and p%4!=1:continue
                factors=[[0,1]]+[polynomials[(2*i if sign==1 else i)] for i in indices]
                weights=[]
                eligible=[]
                for x in range(p):
                    weight=Fraction(1,2**T)
                    for f in factors:weight*=1+character(evaluate(f,x,p),p)
                    need(0<=weight<=1,'weighted range');weights.append(weight)
                    if x and order(x,p)>=m and weight>0:
                        need(character(x,p)==1 and all(character(pow(x,i,p)+sign,p)>=0 for i in range(1,m)),'pattern implications')
                        eligible.append(x)
                need(weights[0]==Fraction(1,2),'zero weight')
                removed=sum(weights[x] for x in range(1,p) if order(x,p)<m)
                need(removed<=sum(phi(i) for i in indices),'low-order cost')
                threshold=Fraction(p, p-1)*2**(T-2)*T*T
                if p>threshold**2:need(bool(eligible),'sufficient positivity')
                records.append({'p':p,'m':m,'sign':sign,'T':T,'eligible':len(eligible),'sufficient_condition':p>threshold**2})
    p=17;y=16;r=4
    need(character(y,p)==1 and order(y,p)==2,'counterexample order')
    need(all(character(pow(y,j,p)-1,p)>=0 for j in [1,2]),'counterexample hypotheses')
    entries=[r*pow(y,i,p)%p for i in [-1,0,1]]
    need(entries==[13,4,13] and len(set(entries))==2,'counterexample cardinality')
    centered=[]
    for p in [7,23,31,47,71,127,151,223]:
        roots={z*z%p:z for z in range(1,p)}
        exact_small=[y for y in roots if y!=1 and character(y+1,p)==1]
        need(len(exact_small)==(p-7)//4,'exact three-tuple count')
        instances=0;even_instances=0
        for n in range(2,13):
            indices=[i for i in range(1,n-1) if i%p]
            T=len(indices)+1;alpha=Fraction(p,p-1)
            need(T<=Fraction(n,1)/alpha+Fraction(1,p),'shorter rounding bound')
            if n>=4:
                K=alpha*T*(T-1)/2
                need(T>=3 and K>=alpha*T and n-1<=alpha*T,'stronger exclusion bounds')
                need((2**(T-1)-Fraction(5,2))*K+2**(T-1)-1>0,'positive final margin')
            for y,z in roots.items():
                if order(y,p)<n or any(character(pow(y,j,p)+1,p)<0 for j in range(1,n-1)):continue
                tuple_=[pow(z,2*i-(n-1),p) for i in range(n)]
                need(len(set(tuple_))==n and all(tuple_),'centered distinct nonzero entries')
                need(all(character(a*b+1,p)>=0 for i,a in enumerate(tuple_) for b in tuple_[i+1:]),'centered tuple products')
                instances+=1;even_instances+=n%2==0
        centered.append({'p':p,'valid_centered_instances':instances,'even_size_instances':even_instances,'three_tuple_parameters':len(exact_small)})
    with localcontext() as ctx:
        ctx.prec=80
        p=Decimal(7);q=p**11;x=q.ln();B=(x/2-2*x.ln())/Decimal(2).ln()
        Q=p/(p-1)*(B+2);m=int(Q);T=m-(m-1)//7
        need(m==10 and T==9 and Decimal(T)>B+2,'printed T inequality fails')
        rounding={'q':int(q),'m':m,'T':T,'B_plus_2':str(B+2),'claim':'Printed intermediate bound fails; no counterexample to Theorem3.5'}
        parameters=[]
        for prime in [7,23,31,47,71,127]:
            for exponent in range(1,102,2):
                if prime==7 and exponent==1:continue
                q=Decimal(prime)**exponent;x=q.ln();B=(x/2-2*x.ln())/Decimal(2).ln()
                alpha=Decimal(prime)/(prime-1);n=int((alpha*(B+2)).to_integral_value(rounding='ROUND_FLOOR'))
                if n<4:continue
                T=n-1-(n-2)//prime
                need(Decimal(T)<=B+2+Decimal(1)/prime,'new parameter rounding')
                need(q.sqrt()>alpha*(Decimal(2)**(T-2))*T*T,'new sufficient inequality')
                parameters.append({'p':prime,'exponent':exponent,'n':n,'T':T})
    return {'status':'PASS_OPTIONAL_DIAGNOSTICS','degree_cases':degree_cases,'prime_field_pattern_cases':records,'centered_prime_cases':centered,'stronger_parameter_cases':parameters,'source_Proposition3_1_entries':entries,'source_Theorem3_5_intermediate':rounding,'uniform_proof_premise':False}
if __name__=='__main__': print(json.dumps(run(),indent=2))
