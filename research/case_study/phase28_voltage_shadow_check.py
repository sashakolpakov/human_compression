#!/usr/bin/env python3
"""Exact finite checks of voltage shadow formulas; no general theorem inferred."""
from itertools import combinations, permutations, product
from pathlib import Path
from hashlib import sha256
import argparse
import json


def mul(g,h):
    return tuple(g[h[i]] for i in range(3))


def inv(g):
    return tuple(g.index(i) for i in range(3))


def components(vertices,adjacent):
    todo=set(vertices);out=[]
    while todo:
        stack=[min(todo)];todo.remove(stack[0]);seen=set(stack)
        while stack:
            u=stack.pop()
            new={v for v in todo if adjacent(u,v)}
            todo-=new;seen|=new;stack.extend(new)
        out.append(frozenset(seen))
    return out


def geometry_audit(types,incident):
    flags=[];chambers=[]
    for row in product(*[[None]+list(T) for T in types]):
        F=tuple(x for x in row if x is not None)
        if all(incident(x,y) for x,y in combinations(F,2)):
            flags.append(F)
            if len(F)==len(types):chambers.append(frozenset(F))
    extension_failures=0;rc_failures=0;panels={}
    for F in flags:
        extension_failures+=not any(set(F)<=C for C in chambers)
        missing=set(range(len(types)))-{x[0] for x in F}
        residue=[x for t in missing for x in types[t] if all(incident(x,y) for y in F)]
        if len(missing)>=2:
            rc_failures+=len(components(residue,incident))!=1
        elif len(missing)==1:
            panels[len(residue)]=panels.get(len(residue),0)+1
    assert extension_failures==rc_failures==0
    assert set(panels)=={2}
    return {'objects':list(map(len,types)),'flags':len(flags),'chambers':len(chambers),
            'extension_failures':extension_failures,'RC_failures':rc_failures,
            'panel_sizes':panels}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();output=Path(args.output)
    if output.exists():raise SystemExit('Choose a new output path; existing evidence is not overwritten.')
    A=list(permutations(range(3)));one=(0,1,2);a=(1,0,2);b=(0,2,1);c=(2,1,0)
    base=list(range(4));edges=list(combinations(base,2))
    voltage={(0,1):a,(0,2):a,(0,3):a,(1,2):a,(1,3):b,(2,3):c}
    for (u,v),g in list(voltage.items()):voltage[v,u]=inv(g)
    vertices=list(product(base,A))
    def adjacent(u,v):
        return u[0]!=v[0] and mul(u[1],voltage[u[0],v[0]])==v[1]
    assert len(components(vertices,adjacent))==1
    sign=lambda g:sum(g[i]>g[j] for i in range(3) for j in range(i+1,3))%2
    lifted_edges=[frozenset((u,v)) for u,v in combinations(vertices,2) if adjacent(u,v)]
    assert len(lifted_edges)==36
    assert all(sign(u[1])!=sign(v[1]) for e in lifted_edges for u,v in [tuple(e)])
    shadows=[frozenset(S) for k in range(2,5) for S in combinations(base,k) if 0 in S]
    lifted={S:components([v for v in vertices if v[0] in S],adjacent) for S in shadows}
    H={S:frozenset(g for v,g in next(C for C in lifted[S] if (0,one) in C) if v==0) for S in shadows}
    coset_checks=0
    for S in shadows:
        for C in lifted[S]:
            fiber=frozenset(g for v,g in C if v==0);g=min(fiber)
            assert fiber==frozenset(mul(g,h) for h in H[S]);coset_checks+=1
    common_checks=0;nonempty=0;disconnected=0;empty_compatible=0
    for length in range(1,4):
        for family in combinations(shadows,length):
            common_base=set.intersection(*(set(S) for S in family))
            base_component=next(C for C in components([v for v in vertices if v[0] in common_base],adjacent)
                                if (0,one) in C)
            HF={g for v,g in base_component if v==0}
            meetH=set.intersection(*(set(H[S]) for S in family))
            assert HF<=meetH
            for cs in product(*(lifted[S] for S in family)):
                common_checks+=1
                fibers=[{g for v,g in C if v==0} for C in cs]
                for i,j in combinations(range(length),2):
                    assert bool(cs[i]&cs[j])==bool(fibers[i]&fibers[j])
                Z=set.intersection(*(set(C) for C in cs))
                fiber=set.intersection(*fibers)
                assert bool(Z)==bool(fiber)
                if not Z:
                    empty_compatible+=all(cs[i]&cs[j] for i,j in combinations(range(length),2))
                    continue
                nonempty+=1;g=min(fiber)
                assert fiber=={mul(g,h) for h in meetH}
                count=len(components(Z,adjacent))
                assert count*len(HF)==len(meetH)
                disconnected+=count>1
    # A second connected S3 cover exhibits a nontrivial component index.
    # The two triangle monodromies are <a>, but their common edge has trivial
    # monodromy. Its two lifts inside the chosen components stay disconnected.
    voltage2={(0,1):one,(0,2):one,(0,3):one,(1,2):a,(1,3):a,(2,3):b}
    for (u,v),g in list(voltage2.items()):voltage2[v,u]=inv(g)
    def adjacent2(u,v):
        return u[0]!=v[0] and mul(u[1],voltage2[u[0],v[0]])==v[1]
    assert len(components(vertices,adjacent2))==1
    selected=[]
    for T in [{0,1,2},{0,1,3}]:
        C=next(C for C in components([v for v in vertices if v[0] in T],adjacent2)
               if (0,one) in C)
        assert {g for v,g in C if v==0}=={one,a}
        selected.append(C)
    common=selected[0]&selected[1]
    assert sorted(map(len,components(common,adjacent2)))==[2,2]
    # The tetrahedron's vertex-edge-face incidence is a base geometry. Its
    # triangle shadows lift to components, with no duplicated arbitrary labels.
    triangles=[frozenset(S) for S in combinations(base,3)]
    face_components=[(T,C) for T in triangles
                     for C in components([v for v in vertices if v[0] in T],adjacent)]
    base_types=[[(0,v) for v in base],[(1,frozenset(e)) for e in edges],[(2,T) for T in triangles]]
    def old_incident(x,y):
        if x[0]==y[0]:return x==y
        if x[0]>y[0]:x,y=y,x
        return (x[1] in y[1]) if x[0]==0 else x[1]<=y[1]
    old=geometry_audit(base_types,old_incident)
    lift_types=[[(0,v) for v in vertices],[(1,e) for e in lifted_edges],
                [(2,i) for i in range(len(face_components))]]
    def lift_incident(x,y):
        if x[0]==y[0]:return x==y
        if x[0]>y[0]:x,y=y,x
        if y[0]==1:return x[1] in y[1]
        C=face_components[y[1]][1]
        return (x[1] in C) if x[0]==0 else x[1]<=C
    lift=geometry_audit(lift_types,lift_incident)
    compressed_types=[[(i,v) for v in vertices if sign(v[1])==i] for i in [0,1]]+[lift_types[2]]
    def compressed_incident(x,y):
        if x[0]==y[0]:return x==y
        if x[0]>y[0]:x,y=y,x
        if y[0]==1:return adjacent(x[1],y[1])
        return x[1] in face_components[y[1]][1]
    compressed=geometry_audit(compressed_types,compressed_incident)
    # Pairwise coset compatibility is not a universal group-theoretic Helly fact.
    cosets=[{0,1},{0,2},{1,2}]
    assert all(x&y for x,y in combinations(cosets,2)) and not set.intersection(*cosets)
    report={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'deck_group':'S3, represented directly by six permutations','base_graph':'K4',
            'connected_cover':True,'cover_vertices':len(vertices),'cover_edges':len(lifted_edges),
            'component_coset_checks':coset_checks,'intersection_family_checks':common_checks,
            'nonempty_intersections':nonempty,'disconnected_intersections':disconnected,
            'pairwise_compatible_empty_intersections':empty_compatible,
            'nontrivial_index_control':{'deck_group':'S3','individual_monodromy_orders':[2,2],
                                       'common_shadow_monodromy_order':1,
                                       'intersection_component_sizes':[2,2]},
            'base_tetrahedron':old,'graph_incidence_lift':lift,'bipartite_compression':compressed,
            'C2_squared_Helly_obstruction':cosets,
            'scope':'Finite checks of coset/component formula and all flags/residues in one nonabelian cover; not a uniform proof or cover classification.'}
    # JSON cannot directly serialize sets; the three standalone cosets are sorted.
    report['C2_squared_Helly_obstruction']=[sorted(C) for C in cosets]
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print('VOLTAGE_SHADOW_PASS',coset_checks,common_checks,len(vertices),lift['chambers'],compressed['chambers'])


if __name__=='__main__':main()
