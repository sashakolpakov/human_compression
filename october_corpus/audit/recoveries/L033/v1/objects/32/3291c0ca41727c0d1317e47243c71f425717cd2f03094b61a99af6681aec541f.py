"""Small literal controls for the three new elementary synthesis joins."""
import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json,copy
from pathlib import Path
def need(v,m):
    if not v:raise ValueError(m)
def mul(a,b):return tuple(b[x]for x in a)
def closure(gs,n):
    e=tuple(range(n));out={e};todo=[e]
    for a in todo:
        for b in gs:
            c=mul(a,b)
            if c not in out:out.add(c);todo.append(c)
    return frozenset(out)
def cosets(g,h):return sorted(set(frozenset(mul(x,y)for x in h)for y in g),key=lambda s:sorted(s))
def actual_kernel(g,types):return frozenset(x for x in g if all(frozenset(mul(y,x)for y in c)==c for C in types for c in C))
def core(g,h):
    return frozenset(x for x in h if all(mul(mul(y,x),tuple(y.index(k)for k in range(len(y))))in h for y in g))
def controls():
    # C2 times S3, three marks; all action/coset facts checked as sets.
    gs=[(1,0,2,3,4),(0,1,3,2,4),(0,1,2,4,3)];g=closure(gs,5);need(len(g)==12,'C2xS3 literal group')
    sub={frozenset(J):closure([gs[i]for i in J],5)for k in range(4)for J in itertools.combinations(range(3),k)}
    need(all(sub[J]&sub[K]==sub[J&K]for J in sub for K in sub),'full IP64')
    factors=[sub[frozenset([0])],sub[frozenset([1,2])]]
    need(len({mul(a,b)for a in factors[0]for b in factors[1]})==12,'literal direct product bijection')
    P=[sub[frozenset(set(range(3))-{i})]for i in range(3)];C=[cosets(g,h)for h in P]
    need(all(c&d for c in C[0]for j in [1,2]for d in C[j]),'cross-component direct-sum incidence')
    same_component=0
    def project(c):return frozenset(tuple(x[i]-2 for i in [2,3,4])for x in c)
    for c in C[1]:
        for d in C[2]:need(bool(c&d)==bool(project(c)&project(d)),'factor-incidence iff');same_component+=1
    families=[P,[g,g],[sub[frozenset([1])],sub[frozenset([2])]],factors]
    pair_checks=0;kernel_orders=[]
    for H in families:
        T=[cosets(g,h)for h in H];need(actual_kernel(g,T)==frozenset.intersection(*(core(g,h)for h in H)),'actual action kernel')
        kernel_orders.append(len(actual_kernel(g,T)))
        for i,j in itertools.combinations(range(len(T)),2):
            for c in T[i]:
                for d in T[j]:
                    if c&d:
                        x=min(c&d);need(frozenset(mul(y,x)for y in H[i])==c and frozenset(mul(y,x)for y in H[j])==d,'common representative');pair_checks+=1
    need(kernel_orders[1]==12,'nonfaithful full-family example')
    # Exact scaled D4 fundamental orbits. Fourth-type roots are all +/-2ei +/-2ej.
    v=(1,1,1,1);w=(1,1,1,-1);x=(0,0,0,2)
    dot=lambda a,b:sum(i*j for i,j in zip(a,b))
    need([dot(v,w),dot(v,x),dot(w,x)]==[2,2,-2],'bad triple actual pair magnitudes')
    roots=[]
    for i,j in itertools.combinations(range(4),2):
        for a,b in itertools.product([-2,2],repeat=2):
            z=[0]*4;z[i]=a;z[j]=b;roots.append(tuple(z))
    need(len(set(roots))==24,'complete fourth-type orbit')
    candidates=[y for y in roots if abs(dot(x,y))==4];need(len(candidates)==12,'12 candidates incident to e4')
    need(all(not(abs(dot(v,y))==4 and abs(dot(w,y))==4)for y in candidates),'no fourth-type extension')
    c=(1,2,3,0);w0=(3,2,1,0);need(mul(c,c)!=(w0),'A3 half-power counterexample')
    return dict(status='PASS_SMALL_L033_SYNTHESIS_JOINS',group_elements=12,subgroup_intersections=64,coset_pair_checks=pair_checks,same_component_incidence_pairs=same_component,kernel_orders=kernel_orders,D4_fourth_type=24,D4_incident_candidates=12,D4_extensions=0,A3_half_power_qualified=True,target_censuses=0)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(a.out.is_absolute()and not a.out.exists(),'fresh output');r=controls();a.out.mkdir();(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
