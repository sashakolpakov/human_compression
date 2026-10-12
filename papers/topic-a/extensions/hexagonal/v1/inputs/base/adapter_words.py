#!/usr/bin/env python3
"""Exact word adapters, using only involution cancellation and declared commuting pairs."""
import json

def mul(*ws):return tuple(v for w in ws for v in w)
def inv(w):return tuple(reversed(w))
def power(w,n):return mul(*([w]*n)) if n>=0 else power(inv(w),-n)
def reduce_word(w,comm):
    # Each performed move is a commuting swap followed by an involution cancellation.
    r=[]
    for c in w:
        j=len(r)-1
        while j>=0 and r[j]!=c and frozenset((r[j],c)) in comm:j-=1
        if j>=0 and r[j]==c:r.pop(j)
        else:r.append(c)
    # Sorting commuting letters cannot change the represented element.
    changed=True
    while changed:
        changed=False
        for j in range(len(r)-1):
            if r[j]>r[j+1] and frozenset((r[j],r[j+1])) in comm:
                r[j],r[j+1]=r[j+1],r[j];changed=True
    return tuple(r)
def eq(w,v,c):
    z=reduce_word(mul(w,inv(v)),c)
    if z:raise ValueError((w,v,z))
a,b,c,d=[(i,) for i in range(4)]

def periods8(x,y,z):
 return [(mul(inv(y),power(x,-2)),mul(y,power(x,2))),
         (mul(z,power(x,3)),mul(inv(x),z,power(x,-2))),
         (mul(inv(x),z,power(mul(inv(y),z),2)),mul(z,x,power(mul(z,y),2))),
         (mul(y,power(mul(z,y),2)),mul(inv(y),power(mul(y,z),2)))]

def run():
 rows=[]
 # Cubic: source (x,y,z)=(ba,bc,bd), fixed/variable period words.
 x,y,z=mul(b,a),mul(b,c),mul(b,d);comm={frozenset(q) for q in [(0,2),(0,3),(2,3)]}
 eq(mul(inv(y),power(z,-2)),mul(c,power(mul(b,d),2),b),comm)
 eq(mul(inv(x),power(z,-2)),mul(a,power(mul(b,d),2),b),comm)
 rows.append({'family':'cubic','marks':['ba','bc','bd'],'exact_period_identities':2})
 # Square: (ad,ab,ac), all four local periods; the third is the product
 # of two commuting local translations, subsequently raised to arbitrary s.
 x,y,z=mul(a,d),mul(a,b),mul(a,c);comm={frozenset(q) for q in [(0,2),(1,3)]};p=periods8(x,y,z)
 targets=[power(mul(b,power(mul(a,d),2),a),2),power(mul(c,power(mul(d,a),2)),2),power(mul(d,power(mul(c,b),2)),2),power(mul(a,power(mul(b,c),2),b),2)]
 for lhs,rhs in zip([power(p[0][0],2),mul(*p[1]),mul(*p[2]),power(p[3][0],2)],targets):eq(lhs,rhs,comm)
 rows.append({'family':'square','marks':['ad','ab','ac'],'exact_period_identities':4,'unbounded_parameter':'(UV)^s=w^(2s), using the local translation commutation proved in the retained Euclidean triangle group'})
 # Finite: (ca,cd,cb), fixed periods plus w^(3t), t=1,2.
 x,y,z=mul(c,a),mul(c,d),mul(c,b);comm={frozenset(q) for q in [(0,3),(1,2)]};p=periods8(x,y,z)
 targets=[power(mul(d,power(mul(c,a),2),c),2),power(mul(b,power(mul(a,c),2),a),2),power(mul(a,power(mul(b,d),2)),2),mul(c,power(mul(d,b),2),d)]
 for lhs,rhs in zip([power(p[0][0],2),power(p[1][0],2),mul(*p[2]),p[3][0]],targets):eq(lhs,rhs,comm)
 rows.append({'family':'finite','marks':['ca','cd','cb'],'exact_period_identities':4,'variable_word':'c(db)^2d, exponent3t'})
 # A reversed noncommuting product is a genuine rejected word identity.
 try:eq(mul(a,b),mul(b,a),set())
 except ValueError:negative=True
 else:raise ValueError('invalid commutation accepted')
 return {'status':'PASS','rows':rows,'exact_word_identities':10,'negative_noncommuting_control':negative,'scope':'Only exact period-word adapters. No new GAP, geometry, or universal-family assertion is inferred from sampling.'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
