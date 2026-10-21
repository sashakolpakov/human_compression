"""Verify literal projective matrix identities and the exact failed intersection."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
from itertools import product
from collections import deque
import json
F=11;I=(1,0,0,1);A=(5,1,7,6);B=(0,1,10,0);C=(4,3,9,7);U=(1,1,0,1)
def need(b,s):
    if not b:raise ValueError(s)
def neg(m):return tuple(-x%F for x in m)
def canon(m):return min(m,neg(m))
def det(m):a,b,c,d=m;return(a*d-b*c)%F
def mul(a,b):return tuple(sum(a[2*i+k]*b[2*k+j]for k in range(2))%F for i in range(2)for j in range(2))
def power(a,k):
    ans=I
    for _ in range(k):ans=mul(ans,a)
    return ans
def word(w,gs=(A,B,C)):
    ans=I
    for c in w:ans=mul(ans,gs[ord(c)-97])
    return ans
def closure(gs):
    seen={canon(I)};todo=deque(seen)
    while todo:
        x=todo.popleft()
        for g in gs:
            y=canon(mul(x,g))
            if y not in seen:seen.add(y);todo.append(y)
    return seen
def porder(g):return next(k for k in range(1,100)if canon(power(g,k))==canon(I))
def verify():
    for x in (A,B,C):need(det(x)==1 and power(x,2)==neg(I)and canon(x)!=canon(I),'three involutions')
    need(word('abacbabcac')==neg(U),'explicit elementary generator word')
    X=power(mul(A,B),3);Z=power(mul(B,C),3)
    need(X==(3,10,10,8) and Z==(1,3,3,10)and mul(X,Z)==neg(B),'intersection identities')
    need(canon(X)not in(canon(I),canon(B)),'genuine excess intersection')
    orders=[porder(mul(x,y))for x,y in[(A,B),(B,C),(A,C)]];need(orders==[6,6,5],'hypermap type')
    R=mul(A,B);T=mul(B,C)
    need(canon(mul(power(R,3),power(T,3)))==canon(B),'rotations recover B')
    need(canon(mul(B,mul(R,B)))==canon(power(R,5))and canon(mul(B,mul(T,B)))==canon(power(T,5)),'inner inversion')
    sl=[m for m in product(range(F),repeat=4)if det(m)==1];proj={canon(m)for m in sl}
    need(len(sl)==1320 and len(proj)==660,'literal determinant matrices')
    groups=[closure(gs)for gs in[(A,B,C),(U,B),(R,T),(A,B),(B,C),(B,)]]
    need(groups[0]==groups[1]==groups[2]==proj,'literal full projective groups')
    need([len(g)for g in groups[3:]]==[12,12,2],'pair subgroups')
    H=groups[3]&groups[4];need(len(H)==4 and groups[5]<H,'exact failed intersection')
    for s in range(1,F):
        e=(1,s,0,1);f=(1,0,-pow(s,-1,F)%F,1);d=(s,0,0,pow(s,-1,F))
        need(mul(e,mul(f,e))==mul(d,B),'all diagonal elimination identities')
    return {'status':'PASS_LITERAL_HYPERMAP_COUNTEREXAMPLE','field':11,'matrices':[A,B,C],'elementary_generator_word':'abacbabcac','X':X,'Z':Z,'product_orders':orders,'determinant_one_matrices':len(sl),'projective_group_order':len(proj),'generated_group_order':len(groups[0]),'rotation_group_order':len(groups[2]),'pair_subgroup_orders':[12,12],'intersection_order':len(H),'shared_involution_subgroup_order':2,'all_nonzero_diagonal_identities':10,'scope':'Counterexample to the unnamed survey hypermap-to-IP inference; no named conjecture or whole-source credit.'}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
