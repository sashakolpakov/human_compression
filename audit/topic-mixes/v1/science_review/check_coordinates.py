#!/usr/bin/env python3
"""Independent reconstruction from the literal S5 cycles and voltage vector."""
from itertools import permutations,product
from pathlib import Path
import argparse,json
def need(ok,msg):
    if not ok:raise ValueError(msg)
E=tuple(range(5));Z=(0,)*6
def mul(p,q):return tuple(p[q[i]] for i in range(5))
def inv(p):return tuple(p.index(i) for i in range(5))
def cycle(xs):
    r=list(E)
    for a,b in zip(xs,xs[1:]+xs[:1]):r[a-1]=b-1
    return tuple(r)
def cyclic(p):
    out=[];q=E
    while q not in out:out.append(q);q=mul(q,p)
    need(q==E,'cyclic group closes');return frozenset(out)
def span(vectors):
    result={Z}
    for v in vectors:result={tuple((x+t*y)%3 for x,y in zip(w,v)) for w in result for t in range(3)}
    return result
def report():
    S=list(permutations(range(5)));index={g:i for i,g in enumerate(S)}
    subgroups=[cyclic(cycle(x)) for x in [(1,2,3,4,5),(1,2,3,5,4),(1,2,4,5,3),(1,2,4,3,5),(1,2,5,4,3),(1,2,5,3,4)]]
    need(len(set(subgroups))==6 and all(len(x)==5 for x in subgroups),'six literal Sylow subgroups')
    pi={g:tuple(subgroups.index(frozenset(mul(mul(g,h),inv(g)) for h in K)) for K in subgroups) for g in S}
    s=[cycle((i+1,i+2)) for i in range(4)]
    need([pi[g] for g in s]==[(4,2,1,5,0,3),(5,3,4,1,2,0),(3,2,1,0,5,4),(1,0,4,5,2,3)],'actual conjugation table S1')
    def act(g,v):
        out=[0]*6
        for i in range(6):out[pi[g][i]]=v[i]
        return tuple(out)
    def semimult(a,b):
        v,g=a;w,h=b;gw=act(g,w);return tuple((x+y)%3 for x,y in zip(v,gw)),mul(g,h)
    u=[Z,(2,2,0,1,0,1),Z,Z];marks=list(zip(u,s));one=(Z,E)
    def value(word):
        out=one
        for i in word:out=semimult(out,marks[i])
        return out
    need(all(value([i,i])==one for i in range(4)),'literal involutions')
    need(all(value([i,j])==value([j,i]) for i in range(4) for j in range(i+2,4)),'literal string relations')
    need(value([0,1]*3)==value([2,3]*3)==one,'outer braid relations')
    v=(1,1,2,2,1,2);need(value([1,2]*3)==(v,E),'middle cube S2')
    five=[v,act(s[0],v),act(s[3],v),act(mul(s[0],s[3]),v),act(mul(s[1],s[0]),v)]
    need(five==[(1,1,2,2,1,2),(1,2,1,2,1,2),(1,1,1,2,2,2),(2,1,1,2,1,2),(2,2,1,2,1,1)] and len(span(five))==243,'five written rows span full augmentation module')
    def difference(i,j):
        w=[0]*6;w[i]=1;w[j]=2;return tuple(w)
    VA=span([difference(0,5),difference(1,2),difference(3,4)])
    VB=span([difference(0,3),difference(1,5),difference(2,4)])
    need(len(VA)==len(VB)==27,'end translation dimensions')
    need(span(act(g,v) for g in S if g[4]==4)==VA and span(act(g,v) for g in S if g[0]==0)==VB,'independent full S4-orbit spans')
    need(all({w[h] for w in VA}=={0,1,2} and {w[h] for w in VB}=={0,1,2} and v[h]!=0 for h in range(6)),'all sheet projections surjective')
    def graph(coords):
        sheets=list(product(range(3),repeat=len(coords)));flags=[(g,t) for g in S for t in sheets];lookup={q:i for i,q in enumerate(flags)}
        edges=[]
        for g,t in flags:
            edges.append([lookup[(mul(g,s[i]),tuple((a+act(g,u[i])[h])%3 for a,h in zip(t,coords)))] for i in range(4)])
        need(all(edges[edges[q][i]][i]==q and len({q,*edges[q]})==5 for q in range(len(flags)) for i in range(4)),'simple colored involutions')
        need(all(edges[edges[q][i]][j]==edges[edges[q][j]][i] for q in range(len(flags)) for i in range(4) for j in range(i+2,4)),'actual string commutation')
        partitions=[]
        for mask in range(16):
            parts=[0]*len(flags)
            for root in range(len(flags)):
                if parts[root]:continue
                seen={root};todo=[root]
                while todo:
                    q=todo.pop()
                    for i in range(4):
                        if mask>>i&1:
                            z=edges[q][i]
                            if z not in seen:seen.add(z);todo.append(z)
                bits=sum(1<<q for q in seen)
                for q in seen:parts[q]=bits
            partitions.append(parts)
        need(partitions[15][0]==(1<<len(flags))-1,'whole connected component')
        return flags,lookup,edges,partitions
    def intersections(parts,masks):
        n=0
        for a in masks:
            for b in masks:
                for q in range(len(parts[0])):
                    need(parts[a][q]&parts[b][q]==parts[a&b][q],'all actual subset orbit intersections');n+=1
        return n
    inputs=[];lifts=0
    for h in range(6):
        flags,lookup,edges,parts=graph((h,));n=intersections(parts,range(16))
        need(all(parts[7][q].bit_count()==parts[14][q].bit_count()==72 and parts[6][q].bit_count()==18 for q in range(360)),'every local component size')
        H=[g for g in S if pi[g][h]==h];need(len(H)==20 and len({(g[0],g[4]) for g in H})==20,'actual sharply two-transitive normalizer')
        medial={parts[6][q] for q in range(360)};need(len(medial)==20,'twenty middle components')
        moved=set()
        for a in H:
            for b in range(3):
                f=[lookup[(mul(a,g),((t[0]+b)%3,))] for g,t in flags]
                need(len(set(f))==360 and all(f[edges[q][i]]==edges[f[q]][i] for q in range(360) for i in range(4)),'every displayed automorphism lift')
                moved.add(parts[6][f[0]]);lifts+=1
        need(moved==medial,'actual transitive action on all medial components')
        inputs.append(dict(coordinate=h,flags=360,all_subset_IP_identities=n,facets=72,vertex_figures=72,medial_sections=18,medial_components=20,verified_automorphisms=60))
    flags,lookup,edges,parts=graph((0,1));end_checks=0
    for mask in [7,14]:end_checks+=intersections(parts,[j for j in range(16) if j&mask==j])
    gstar=mul(mul(s[1],s[2]),s[3]);need(gstar==cycle((2,3,4,5)) and pi[gstar]==(4,1,0,2,3,5),'specified compatible good root')
    good=lookup[gstar,(0,0)];bad=lookup[E,(0,0)]
    def fiber(mask,q):return {t for j,(g,t) in enumerate(flags) if g==flags[q][0] and parts[mask][q]>>j&1}
    whole=frozenset(product(range(3),repeat=2));diag={(0,0),(1,1),(2,2)};anti={(0,0),(2,1),(1,2)}
    need(fiber(7,bad)==fiber(14,bad)==whole and fiber(6,bad)==diag,'bad root has unequal actual fibers')
    need(fiber(7,good)==fiber(6,good)==anti and fiber(14,good)==whole,'good root fibers exactly S5')
    need((parts[7][bad]&parts[14][bad]).bit_count()==54 and parts[6][bad].bit_count()==18,'actual bad end intersection')
    need(parts[7][good]&parts[14][good]==parts[6][good] and parts[6][good].bit_count()==18,'actual good full intersection')
    need(({t for t in fiber(7,good) if t[0]==0}&{t for t in fiber(14,good) if t[0]==0})=={(0,0)},'literal first-factor variance intersection trivial')
    cube=[1,2]*3;wa=(cube+[0]+cube+[0])*2;h=[2,3];wb=(cube+h+list(reversed(cube))+list(reversed(h)))*2
    def walk(word):
        q=bad
        for i in word:q=edges[q][i]
        return q
    target=lookup[E,(1,0)]
    need(walk(wa)==walk(wb)==target and not(parts[6][bad]>>target&1),'both literal path words and no middle path')
    return dict(status='PASS_DISTINCT_SIX_COORDINATE_RECONSTRUCTION',author_modules_imported=False,Sylow_subgroups=6,group_order_from_full_kernel=29160,independent_inputs=inputs,input_IP_identities=sum(x['all_subset_IP_identities'] for x in inputs),actual_automorphism_lifts=lifts,mix_flags=1080,mixed_end_IP_identities=end_checks,good_root=good,bad_root=bad,good_intersection=18,bad_intersection=54,marked_middle=18,good_first_coordinate_variance_intersection=1,both_actual_witness_words=True,whole_source_or_conjecture_credit=False)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');r=report();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='independent_inputs'}))
