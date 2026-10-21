"""Complete literal graph calculations; no cached group orders or graph library.

direct_graphs.py is reused whole from the accepted L013 finite packet.
These checks certify supplied graphs, not completeness of the four-cage list.
"""
from pathlib import Path
from collections import Counter, deque
import argparse, json, re
from direct_graphs import check_simple, profile, isomorphisms, valid_map, need

HERE=Path(__file__).resolve().parent

def cycle_counts(A,length):
    A=check_simple(A)
    need(isinstance(length,int) and length>=3,'cycle length')
    counts={(u,v):0 for u in range(len(A)) for v in A[u] if u<v}
    total=0
    for root in range(len(A)):
        def visit(path):
            nonlocal total
            if len(path)==length:
                if root in A[path[-1]] and path[1]<path[-1]:
                    total+=1
                    for u,v in zip(path,path[1:]+[root]):
                        counts[tuple(sorted((u,v)))]+=1
                return
            for v in sorted(A[path[-1]]):
                if v>root and v not in path:visit(path+[v])
        visit([root])
    need(sum(counts.values())==length*total,'cycle-edge incidence identity')
    return dict(total=total,edge_histogram=dict(sorted(Counter(counts.values()).items())),
                counts=[[u,v,c] for (u,v),c in sorted(counts.items())])

def egr(A):
    pr=profile(A)
    if len(pr['degrees'])!=1 or pr['girth'] is None:
        return dict(is_egr=False,profile=pr,cycles=None)
    cycles=cycle_counts(A,pr['girth'])
    return dict(is_egr=len(cycles['edge_histogram'])==1,profile=pr,cycles=cycles)

def mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        a<<=1
        if a&4:a^=7
        b>>=1
    return c

def coordinate_graph():
    A=[set() for _ in range(32)]
    def edge(u,v):A[u].add(v);A[v].add(u)
    for x in range(4):
        for y in range(4):
            edge(4*x+y,4*x+(y^1))
            for m in range(4):edge(4*x+y,16+4*m+(y^mul(m,x)))
    for m in range(4):
        for b in range(4):edge(16+4*m+b,16+4*m+(b^2))
    return check_simple(A)

def supplied_graphs():
    graphs=[('coordinate_H',coordinate_graph()),
            ('source_Magma_G',check_simple(json.loads((HERE/'inputs/source_G.json').read_text())))]
    for i in range(4):
        lines=(HERE/f'inputs/cage-k5.g5-0{i}.dr').read_text().strip().splitlines()
        need(lines[0].strip()=='n30' and len(lines)==31,'cage header/rows')
        A=check_simple([{int(v) for v in re.findall(r'\d+',row)} for row in lines[1:]])
        need(len(A)==30,'cage order')
        graphs.append((f'Brouwer_cage_{i+1}',A))
    return graphs

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))

def order(p):
    identity=tuple(range(len(p)));q=identity
    for i in range(1,10000):
        q=compose(q,p)
        if q==identity:return i
    raise ValueError('unneeded large order')

def full_group(A,complete_order):
    data=json.loads((HERE/'inputs/G_group.json').read_text())
    generators=[tuple(x) for x in data['automorphism_generators']]
    for g in generators:need(valid_map(A,A,g),'literal group generator')
    identity=tuple(range(len(A)));seen={identity};queue=deque([identity])
    while queue:
        g=queue.popleft()
        for h in generators:
            x=compose(g,h)
            if x not in seen:seen.add(x);queue.append(x)
    need(len(seen)==complete_order==48,'generated equals uncached full automorphism order')
    E={g for g in seen if order(g)<=2}
    need(len(E)==16 and E=={tuple(g) for g in data['normal_elementary_abelian_subgroup']},'literal E16')
    need(all(compose(g,h) in E and compose(g,h)==compose(h,g) for g in E for h in E),'abelian closed E')
    c=tuple(data['complement_generator']);need(c in seen and order(c)==3,'complement C3')
    c2=compose(c,c)
    need({compose(compose(c,g),c2) for g in E}==E,'normality')
    cosets=[E,{compose(g,c) for g in E},{compose(g,c2) for g in E}]
    need(set.union(*cosets)==seen and sum(map(len,cosets))==len(seen),'exact semidirect product')
    fixed=sum(compose(g,c)==compose(c,g) for g in E)
    need(fixed==4,'specified complement action')
    return dict(order=len(seen),normal_order=len(E),complement_order=3,fixed_normal_elements=fixed)

def coordinate_maps(A):
    maps=[]
    for s in range(4):
        for t in range(4):
            for c in range(4):
                p=[4*(x^s)+(y^mul(c,x)^t) for x in range(4) for y in range(4)]
                p += [16+4*(m^c)+(b^t^mul(m^c,s)) for m in range(4) for b in range(4)]
                need(valid_map(A,A,p),'affine map');maps.append(p)
    dual=[16+4*mul(x,x)+mul(2,mul(y,y)) for x in range(4) for y in range(4)]
    dual += [4*mul(2,mul(m,m))+mul(2,mul(b,b)) for m in range(4) for b in range(4)]
    need(valid_map(A,A,dual),'corrected semilinear duality')
    need({p[0] for p in maps}==set(range(16)) and {p[16] for p in maps}==set(range(16,32)),'two type orbits')
    return dict(affine_maps=len(maps),duality=True,vertex_transitive=True)

def controls():
    # Source's literal appendix omits zero-count edges. K4 disjoint cube
    # is cubic of girth three and demonstrates the exact logical error.
    A=[set(range(4))-{u} for u in range(4)]
    A += [{4+(u^bit) for bit in (1,2,4)} for u in range(8)]
    r=egr(A)
    need(not r['is_egr'] and r['profile']['girth']==3,'zero-edge rejection')
    need(r['cycles']['edge_histogram']=={0:12,2:6},'exact zero-edge counterexample')
    need({c for _,_,c in r['cycles']['counts'] if c>0}=={2},'source positive-only multiplicity set')
    positive=egr([set(range(4))-{u} for u in range(4)])
    need(positive['is_egr'] and positive['cycles']['edge_histogram']=={2:6},'positive K4')
    need(not egr([{1},{0}])['is_egr'],'acyclic input rejection')
    malformed=0
    for bad in ([[0]],[[1],[]],[[3],[0]]):
        try:check_simple(bad)
        except (ValueError,IndexError):malformed+=1
    need(malformed==3,'malformed graph controls')
    return dict(zero_edge_counterexample=r,positive_K4=positive,acyclic_rejected=True,malformed_rejections=malformed)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();need(not args.out.exists(),'fresh report path')
    rows=[];graphs=supplied_graphs()
    expected=[(32,4,1920,{12:80}),(32,4,48,{12:80}),
              (30,3,120,{12:45,14:30}),(30,3,20,{12:50,13:20,14:5}),
              (30,3,30,{12:60,14:15}),(30,3,96,{12:24,13:48,16:3})]
    for (name,A),(n,diam,aut,hist) in zip(graphs,expected):
        pr=profile(A);need(pr==dict(order=n,degrees=[5],girth=5,diameter=diam,connected=True),'graph profile '+name)
        cycles=cycle_counts(A,5);need(cycles['edge_histogram']==hist,'exact cycle histogram '+name)
        group=isomorphisms(A,A);need(group['count']==aut,'uncached automorphism order '+name)
        rows.append(dict(name=name,profile=pr,cycles=cycles,automorphisms=group))
    noiso=isomorphisms(graphs[0][1],graphs[1][1],first=True)
    need(noiso['count']==0,'complete nonisomorphism search')
    report=dict(status='PASS_LITERAL_FINITE_CERTIFICATES',graphs=rows,
                G_group=full_group(graphs[1][1],rows[1]['automorphisms']['count']),
                H_maps=coordinate_maps(graphs[0][1]),H_to_G=noiso,controls=controls(),
                classification_completeness_reproved=False,external_census_rerun=False)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],graphs=len(rows),uncached_automorphism_orders=6,
                         orders=[r['automorphisms']['count'] for r in rows],G_group=report['G_group'],
                         H_to_G=noiso['count'],controls=6)))

if __name__=='__main__':main()
