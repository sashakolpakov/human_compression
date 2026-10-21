#!/usr/bin/env python3
"""An elementary tuple-permutation certificate; no S18 enumeration or algebra package."""
import json
from collections import deque
N=18
ONE=tuple(range(N))

def require(value,message):
    if not value: raise ValueError(message)
def cycles(*cc):
    p=list(ONE)
    for cyc in cc:
        for x,y in zip(cyc,cyc[1:]+cyc[:1]):p[x-1]=y-1
    require(sorted(p)==list(ONE),'permutation');return tuple(p)
def mul(p,q):return tuple(q[i] for i in p)
def inverse(p):
    r=[0]*N
    for i,j in enumerate(p):r[j]=i
    return tuple(r)
def power(p,n):
    r=ONE
    while n:
        if n&1:r=mul(r,p)
        p=mul(p,p);n//=2
    return r
def word(s,marks):
    r=ONE
    for x in s:r=mul(r,marks[x])
    return r
def conjugate(p,g):return mul(mul(inverse(g),p),g)
def orbit_partition(gens):
    todo=set(range(N));parts=[]
    while todo:
        seed=min(todo);seen={seed};queue=deque([seed])
        while queue:
            x=queue.popleft()
            for g in gens:
                y=g[x]
                if y not in seen:seen.add(y);queue.append(y)
        parts.append(sorted(i+1 for i in seen));todo-=seen
    return parts
def subgroup(gens):
    seen={ONE};queue=deque([ONE])
    while queue:
        p=queue.popleft()
        for q in gens:
            s=mul(p,q)
            if s not in seen:seen.add(s);queue.append(s)
        require(len(seen)<=180,'only bounded proper old subgroups may be enumerated')
    return seen
A=cycles((1,2),(5,6),(7,8),(11,12),(13,14),(17,18))
B=cycles((2,3),(4,5),(7,9),(10,11),(14,15),(16,17))
C=cycles((3,4),(5,7),(6,8),(9,10),(11,13),(12,14),(15,16))
T=cycles((1,18))
TREE=[('',(4,9)),('q',(5,7)),('c',(3,10)),('qa',(6,8)),('cq',(2,11)),
 ('cqa',(1,12)),('cqc',(2,13)),('cqaq',(12,18)),('cqac',(1,14)),
 ('cqcq',(3,13)),('cqaqa',(11,17)),('cqacq',(15,18)),('cqcqa',(3,14)),
 ('cqcqc',(4,11)),('cqaqaq',(10,16)),('cqcqcq',(5,10)),('cqcqcqa',(6,10))]

def verify(t=T,w_exponent=8,tree=TREE):
    a,b,c=A,B,C;q=mul(t,b);marks={'a':a,'b':b,'c':c,'q':q}
    old=[a,q,c];new=[t,a,b,c]
    for xs in [old,new]:
        require(len(set(xs))==len(xs),'distinct marks')
        require(all(x!=ONE and power(x,2)==ONE for x in xs),'nonidentity involutions')
        for i in range(len(xs)):
            for j in range(i+2,len(xs)):
                require(mul(xs[i],xs[j])==mul(xs[j],xs[i]),'string commutations')
    require(sum(q[i]!=i for i in range(N))==14,'old middle has seven transpositions')
    require(c[0]==0 and c[17]==17,'chosen edge avoids c-edges')
    seed=power(word('aqcq',marks),45)
    require(seed==cycles((4,9)),'generation seed word')
    edges=[]
    for w,pair in tree:
        require(conjugate(seed,word(w,marks))==cycles(pair),'conjugate tree edge '+w)
        edges.append(cycles(pair))
    require(len(tree)==17 and orbit_partition(edges)==[list(range(1,19))],'connected spanning tree certificate')
    # The graph-transposition theorem now proves old generation of the full S18.
    r=mul(a,q);s=mul(q,c)
    require(r==cycles((1,3,2,18,16,17),(4,5,6),(7,8,9),(10,11,12),(13,15,14)),'old left rotation')
    require(mul(b,c)==cycles((2,4,7,10,13,11,9,5,3),(6,8),(12,14,16,17,15)),'right rotation')
    require(power(r,6)==ONE and all(power(r,i)!=ONE for i in range(1,6)),'left order six')
    require(power(s,90)==ONE and all(power(s,i)!=ONE for i in range(1,90)),'right order ninety')
    require(power(mul(t,a),4)==ONE and power(mul(t,a),2)!=ONE,'new first adjacent order four')
    require(power(mul(a,b),3)==ONE and mul(a,b)!=ONE,'new middle adjacent order three')
    proper={mask:subgroup([old[i] for i in range(3) if mask&(1<<i)]) for mask in range(7)}
    require([len(proper[i]) for i in [3,6]]==[12,180],'dihedral end orders')
    pairs=0;whole_cases=0
    for i in range(8):
        for j in range(8):
            if i==7 or j==7:
                # A subgroup intersects the whole generated group in itself.
                require((i&j)==(j if i==7 else i),'whole-group subset identity');whole_cases+=1
            else:require(proper[i]&proper[j]==proper[i&j],'actual proper parabolic intersection')
            pairs+=1
    middle=orbit_partition([a,b]);end=orbit_partition([t,a,b])
    require(middle==[list(range(k,k+3)) for k in range(1,19,3)],'six middle triples')
    require(end==[[1,2,3,16,17,18],[4,5,6],[7,8,9],[10,11,12],[13,14,15]],'six-point end orbit')
    w=mul(mul(mul(mul(mul(a,power(mul(b,c),2)),b),a),power(mul(c,b),w_exponent)),a)
    require(power(mul(b,c),45)==cycles((6,8)),'witness initial transposition')
    require(w[5]==0 and w[7]==17,'witness endpoint transport')
    require(conjugate(power(mul(b,c),45),w)==t and t!=ONE,'disjoint-label intersection witness')
    return dict(points=N,old_group='S18 by connected transposition certificate',generation_tree_edges=len(tree),
        old_type=[6,90],new_adjacent_orders=[4,3,90],old_parabolic_pairs=pairs,directly_enumerated_proper_pairs=pairs-whole_cases,
        whole_group_cases_by_containment=whole_cases,max_enumerated_group_order=max(map(len,proper.values())),
        middle_orbits=middle,end_orbits=end,witness='((bc)^45)^(a(bc)^2ba(cb)^8a)=t',
        all_source_case_three_hypotheses_checked=True,old_marking_C=True,new_marking_C=False,
        full_symmetric_group_enumerated=False,uses_GAP=False,
        permutations_one_based={k:[x+1 for x in p] for k,p in {'a':a,'b':b,'c':c,'t':t,'q':q}.items()})

def main():
    result=verify();controls=[]
    for name,kwargs in [('wrong_power',{'w_exponent':7}),('missing_tree_edge',{'tree':TREE[:-1]}),
                         ('wrong_split_transposition',{'t':cycles((1,17))})]:
        try:verify(**kwargs)
        except ValueError as e:controls.append({'name':name,'rejected_at':str(e)})
        else:raise RuntimeError('Bad certificate accepted '+name)
    result.update(status='PASS',rejected_controls=controls,uniform_source_recovery=False)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
