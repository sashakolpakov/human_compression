#!/usr/bin/env python3
"""Exact bounded normal-form checks for the cyclic-index family.

No source catalogue or GAP group identifiers are used. These are finite checks,
not the all-parameter proof in phase169_cyclic_index_completion.md.
"""
import argparse
from collections import deque
import hashlib
from itertools import product
import json
import os
from pathlib import Path


def require(test, message):
    if not test:
        raise RuntimeError(message)


def check(M, e):
    half=M//2
    def nm(s,t):
        u,v=s;w,k=t
        return (u^w,(v+k+e*v*w*half)%M)
    def A(s):
        u,v=s
        return (u^(v%2),(v+e*(v*(v-1)//2)*half)%M)
    def C(s):
        u,v=s
        return (u,(-v+e*u*half)%M)
    ns=list(product(range(2),range(M)))
    for n in ns:
        require(A(A(n))==n and C(C(n))==n and A(C(n))==C(A(n)), 'Bad commuting involutory actions')
    action_pairs=0
    for s,t in product(ns,repeat=2):
        require(A(nm(s,t))==nm(A(s),A(t)), 'A not automorphism')
        require(C(nm(s,t))==nm(C(s),C(t)), 'C not automorphism')
        action_pairs+=1
    # The mathematical cocycle proof supplies all-parameter associativity.
    # Exhaustively cross-check its smallest normal form as an implementation control.
    assoc=0
    if M==4:
        for s,t,u in product(ns,repeat=3):
            require(nm(nm(s,t),u)==nm(s,nm(t,u)), 'N associativity failed')
            assoc+=1
    def mul(s,t):
        u,v,a,c=s;w,k,b,d=t
        n=(w,k)
        if a:n=A(n)
        if c:n=C(n)
        uv=nm((u,v),n)
        return uv+(a^b,c^d)
    one=(0,0,0,0)
    def power(s,k):
        ans=one
        while k:
            if k&1:ans=mul(ans,s)
            s=mul(s,s);k//=2
        return ans
    def inv(s):
        return power(s,M-1)
    def comm(s,t):
        return mul(mul(mul(inv(s),inv(t)),s),t)
    def conjugate(s,t):
        return mul(mul(inv(t),s),t)
    a=(0,0,1,0);c=(0,0,0,1);r=(0,1,0,0);x=(1,0,0,0)
    b=mul(r,c);z=power(r,half);gens=[a,b,c]
    universe=set(product(range(2),range(M),range(2),range(2)))
    for g in universe:
        require(power(g,M)==one and mul(g,inv(g))==one and mul(inv(g),g)==one,'Wrong exponent/inverse')
    def generated(gens):
        found={one};queue=deque([one])
        while queue:
            s=queue.popleft()
            for t in gens:
                n=mul(s,t)
                if n not in found:
                    found.add(n);queue.append(n)
        return found
    require(generated(gens)==universe,'Wrong generated group')
    require(all(power(g,2)==one and g!=one for g in gens),'Markers not involutions')
    require(comm(a,c)==one and power(mul(a,b),2)==x,'Wrong marking')
    require(power(r,M)==one and power(r,M//2)!=one,'Wrong rotation order')
    subs=[generated([gens[i] for i in range(3) if mask>>i&1]) for mask in range(8)]
    for i,j in product(range(8),repeat=2):
        require(subs[i]&subs[j]==subs[i&j],'IP failure')
    h=comm(x,c);w=mul(mul(mul(a,b),c),b)
    require(h==power(z,e) and conjugate(h,b)==power(w,2),'Extra word bridge fails')
    require(mul(power(w,2),power(mul(c,b),half*e))==one,'Literal Coxeter extra relator fails')
    p=r;q=mul(a,b);rho=a
    require(power(p,M)==power(q,4)==power(rho,2)==one,'Original presentation orders fail')
    require(conjugate(p,q)==mul(power(q,2),inv(p)),'Original p^q relation fails')
    require(conjugate(p,power(q,2))==power(p,1+half*e),'Original p^(q²) fails')
    require(conjugate(p,rho)==mul(power(q,2),p),'Original p^rho fails')
    require(conjugate(q,rho)==inv(q),'Original q^rho fails')
    require(mul(inv(q),rho)==b and mul(mul(inv(p),inv(q)),rho)==c,'Inverse substitutions fail')
    center={g for g in universe if all(mul(g,s)==mul(s,g) for s in gens)}
    expected_center=generated([x,z] if e==0 else [z])
    require(center==expected_center,'Wrong center invariant')
    d=power(r,2);L=generated([c,d]);H=generated([a,x])
    LH={mul(l,h) for l in L for h in H}
    require(len(L)==M and len(H)==4 and L&H=={one} and len(LH)==4*M,'Wrong exact factors')
    require(generated([c,d,a,x])==LH and b not in LH,'Wrong index-two product/complement')
    action_relations=[(d,a,mul(d,power(z,e))),(c,a,c),(d,x,d),(c,x,mul(c,power(z,e))),
                      (d,b,inv(d)),(c,b,mul(d,c)),(a,b,mul(x,a)),(x,b,x)]
    for s,t,image in action_relations:
        require(conjugate(s,t)==image,'Wrong semidirect action')
    require(all(conjugate(l,h) in L for l in L for h in H),'Inner factor not normal')
    require(all(conjugate(k,b) in LH for k in LH),'Outer index-two factor not normal')
    require(all(mul(l,h)==mul(h,l) for l in L for h in H)==(e==0),'Wrong direct/semidirect parameter')
    return {'M':M,'epsilon':e,'order':len(universe),'exponent':M,'center_order':len(center),
            'all_marked_IP_pairs':64,'N_action_pairs':action_pairs,'N_associativity_triples':assoc,
            'source_presentations_and_inverse_substitutions':True,'factors':[len(L),len(H),2],
            'inner_action_trivial':e==0,'complete_group_elements_checked':len(universe)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    require(not os.path.lexists(args.output),'Refusing existing output path')
    cases=[check(M,e) for M in [4,8,16,32,64,128] for e in ([0] if M==4 else [0,1])]
    result={'status':'PASS_BOUNDED_NORMAL_FORM_CHECKS','cases':cases,
            'total_IP_pairs':sum(r['all_marked_IP_pairs'] for r in cases),
            'complete_group_elements_checked':sum(r['complete_group_elements_checked'] for r in cases),
            'whole_family_proof':'Written proof, not established by this finite sample',
            'GAP_or_external_catalogue_used':False,'Lean_certificate':False,
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('PHASE169_NORMAL_FORMS_PASS',len(cases))


if __name__=='__main__':main()
