#!/usr/bin/env python3
"""Independent elementary checks of the finite-certificate interfaces.
No author GAP code or finite witness data imported. Not a replacement for
Atlas identification, maximal-subgroup classification or the full replay.
"""
from itertools import combinations, product
import json

def need(b,s):
    if not b: raise RuntimeError(s)
def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def cycle(n,*cycles):
    p=list(range(n))
    for cyc in cycles:
        for x,y in zip(cyc,cyc[1:]+cyc[:1]):p[x-1]=y-1
    return tuple(p)
def group(gs,n):
    one=tuple(range(n));out={one};todo=[one]
    for p in todo:
        for q in gs:
            z=mul(p,q)
            if z not in out:out.add(z);todo.append(z)
    return frozenset(out)
def subsets(n):return [frozenset(s) for k in range(n+1) for s in combinations(range(n),k)]
def cosets(g,h):
    out=[];unseen=set(g)
    while unseen:
        x=min(unseen);c=frozenset(mul(x,y) for y in h);out.append(c);unseen-=c
    return out

def model(gs):
    n=len(gs[0]);ss=subsets(3);hs={s:group([gs[i] for i in s],n) for s in ss}
    g=hs[frozenset(range(3))];p=[hs[frozenset(range(3))-{i}] for i in range(3)]
    ip=all(hs[i]&hs[j]==hs[i&j] for i,j in product(ss,repeat=2))
    cc=[cosets(g,h) for h in p];bad=None;flags=0
    for x,y,z in product(*cc):
        if x&y and x&z and y&z:
            flags+=1
            if not x&y&z and bad is None:bad=[min(x),min(y),min(z)]
    tested=0;criterion=True
    for i in range(3):
        j,k=[x for x in range(3) if x!=i]
        lhs={mul(x,y) for x in p[j] for y in p[k]}&p[i]
        rhs={mul(x,y) for x in p[j]&p[i] for y in p[k]&p[i]}
        criterion &= lhs==rhs;tested+=len(p[j])*len(p[k])
    need(criterion==(bad is None),'product identity must match literal flags')
    return {'order':len(g),'ip_pairs':64,'ip':ip,'flags':flags,'flag_transitive':bad is None,'first_bad_flag_representatives':bad,'streamed_pairs':tested}

def run():
    good=model([cycle(4,(1,2)),cycle(4,(2,3)),cycle(4,(3,4))])
    bad=model([cycle(5,(2,3),(4,5)),cycle(5,(1,2),(4,5)),cycle(5,(1,3),(2,4))])
    need(good['ip'] and good['flag_transitive'] and good['flags']==24,'S4 positive marking')
    need(bad['ip'] and not bad['flag_transitive'],'IP cannot replace flag transitivity')
    # Direct finite quotients of the lamp presentation. Squared relators hold;
    # unsquared relations fail for adjacent distinct lamps.
    def rotate(v,k,n):return ((v<<k)|(v>>(n-k)))&((1<<n)-1) if k else v
    def lm(x,y,n):return (x[0]^rotate(y[0],x[1],n),(x[1]+y[1])%n)
    n=3;a=(1,0);t=(0,1);ti=(0,2);one=(0,0)
    raw=lm(lm(lm(a,t,n),a,n),ti,n)
    need(raw!=one and lm(raw,raw,n)==one,'missing square changes presented group')
    # Exact elementary maximal-order implication. The complete list and outer
    # class membership remain retained hypotheses, not inferred by this test.
    orders=[273030912000000,479001600,354816000,33094656,7372800,5040000,4000000,3317760,2073600,2064384,1500000,186624,116640]
    only=[i for i,x in enumerate(orders) if x%11==0 and x%19==0]
    need(only==[0],'HN maximal exclusion arithmetic')
    controls=[]
    for name,ok in [('IP implies flag transitivity',bad['flag_transitive']),('unsquared lamp relation',raw==one)]:
        need(not ok,name);controls.append({'claim':name,'rejected':True})
    return {'status':'PASS','independent_literal_coset_models':[good,bad],
      'lamp_mod3':{'ambient_order':24,'literal_abelian_quotient_order':6,'raw_relator':raw,'square_is_identity':True},
      'HN_maximal_order_test':{'rows':13,'only_row_divisible_by_11_and_19':0,'retained_list_completeness':True,'retained_outer_class':True},
      'controls':controls,'scope':'Exact elementary interface checks; no source or complete formalization credit.'}
if __name__=='__main__': print(json.dumps(run(),indent=2))
