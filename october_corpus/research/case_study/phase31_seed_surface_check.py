#!/usr/bin/env python3
"""Exact surface/orientation diagnostics for the retained finite seed; no large cover."""
import argparse
import json
from pathlib import Path
from hashlib import sha256
from collections import Counter


def multiply(a,b):
    return tuple(a[b[i]] for i in range(len(a)))


def closure(gens):
    identity=tuple(range(len(gens[0])))
    found={identity}; queue=[identity]
    for g in queue:
        for h in gens:
            x=multiply(g,h)
            if x not in found:
                found.add(x);queue.append(x)
    return found


def cosets(G,H):
    return sorted({frozenset(multiply(g,h) for h in H) for g in G},key=min)


def rank(matrix,p):
    a=[[x%p for x in row] for row in matrix]
    r=0
    for j in range(len(a[0])):
        i=next((i for i in range(r,len(a)) if a[i][j]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r]
        inv=pow(a[r][j],-1,p)
        a[r]=[(x*inv)%p for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                coeff=a[i][j]
                a[i]=[(x-coeff*y)%p for x,y in zip(a[i],a[r])]
        r+=1
    return r


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--seed',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise SystemExit('Choose a new output path.')
    raw=args.seed.read_bytes()
    assert sha256(raw).hexdigest()=='215f02bef8f6948b6ade6916202151b7b9d3cb8a2f731d2cc41ea721a103905d'
    seed=json.loads(raw)
    c,b,d=[tuple(x-1 for x in g) for g in seed['marking_1_based']]
    G=closure([c,b,d]);identity=tuple(range(7))
    V,E,F=cosets(G,closure([b,d])),cosets(G,closure([c,d])),cosets(G,closure([c,b]))
    assert [len(V),len(E),len(F)]==[12,30,12]
    ends=[sorted(i for i,v in enumerate(V) if v&e) for e in E]
    assert all(len(pair)==2 for pair in ends)
    assert len(set(map(tuple,ends)))==30
    face_edges=[[i for i,e in enumerate(E) if e&f] for f in F]
    assert face_edges==seed['face_blocks']
    # Traverse the literal five-cycle of each closed face.
    cycles=[]; boundaries=[]
    for edges in face_edges:
        vertices=sorted({v for i in edges for v in ends[i]})
        assert len(edges)==len(vertices)==5
        neighbors={v:sorted((w,i) for i in edges if v in ends[i] for w in ends[i] if w!=v) for v in vertices}
        assert all(len(n)==2 for n in neighbors.values())
        start=min(vertices);previous=None;current=start;cycle=[];row=[0]*30
        while True:
            cycle.append(current)
            nxt,e=next((w,i) for w,i in neighbors[current] if w!=previous)
            row[e]=1 if ends[e]==[current,nxt] else -1
            previous,current=current,nxt
            if current==start:break
            assert current not in cycle
        assert len(cycle)==5
        cycles.append(cycle);boundaries.append(row)
    # Choose face orientations so every shared edge cancels integrally.
    incident_faces=[[i for i,row in enumerate(boundaries) if row[e]] for e in range(30)]
    assert all(len(pair)==2 for pair in incident_faces)
    signs={0:1};queue=[0]
    for i in queue:
        for e,value in enumerate(boundaries[i]):
            if not value:continue
            j=next(j for j in incident_faces[e] if j!=i)
            required=-signs[i]*value*boundaries[j][e]
            if j in signs:assert signs[j]==required
            else:signs[j]=required;queue.append(j)
    assert len(signs)==12
    d2=[[signs[f]*boundaries[f][e] for f in range(12)] for e in range(30)]
    assert all(sum(row)==0 for row in d2)
    d1=[[(-1 if v==u else 1 if v==w else 0) for u,w in ends] for v in range(12)]
    assert all(sum(d1[v][e]*d2[e][f] for e in range(30))==0 for v in range(12) for f in range(12))
    # Barycentric links, triangle panels, and the independent flag-color character.
    flags=[(i,j,k) for i,v in enumerate(V) for j,e in enumerate(E) for k,f in enumerate(F) if v&e&f]
    assert len(flags)==120
    panels=Counter((typ,tuple(x for t,x in enumerate(flag) if t!=typ)) for flag in flags for typ in range(3))
    assert len(panels)==180 and set(panels.values())=={2}
    for typ,objects in enumerate([V,E,F]):
        for index in range(len(objects)):
            links=[tuple((t,x) for t,x in enumerate(flag) if t!=typ) for flag in flags if flag[typ]==index]
            vertices={x for pair in links for x in pair}
            degree=Counter(x for pair in links for x in pair)
            assert set(degree.values())=={2}
            reached={min(vertices)}
            while True:
                new=reached|{y for pair in links for x in pair for y in pair if x in reached}
                if new==reached:break
                reached=new
            assert reached==vertices
    chi=lambda g:int(g[5]==6)
    assert all(chi(multiply(g,h))==chi(g)^chi(h) for g in G for h in G)
    assert [chi(g) for g in [c,b,d]]==[1,1,1]
    flag_colors={}
    for flag in flags:
        i,j,k=flag;common=V[i]&E[j]&F[k]
        assert len(common)==1
        flag_colors[flag]=chi(next(iter(common)))
    for omitted,other in panels:
        pair=[flag for flag in flags if tuple(x for t,x in enumerate(flag) if t!=omitted)==other]
        assert flag_colors[pair[0]]!=flag_colors[pair[1]]
    homology=[]
    for p in [2,3,5,7,11]:
        ranks=[rank(d1,p),rank(d2,p)]
        assert ranks==[11,11]
        homology.append({'prime':p,'boundary_ranks':ranks,'H1_dimension':30-sum(ranks)})
    result={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'retained_seed_sha256':sha256(raw).hexdigest(),
            'cell_counts':[12,30,12],'barycentric_triangles':120,'barycentric_panels':180,
            'connected_circular_links':54,'closed_pentagonal_faces':12,
            'edge_endpoints':ends,'face_cycles':cycles,'face_orientation_signs':[signs[i] for i in range(12)],
            'integer_boundary_d1':d1,'integer_boundary_d2':d2,
            'boundary_composition_zero':True,'global_face_cycle_sum_zero':True,
            'flag_color_homomorphism_products_checked':14400,
            'Euler_characteristic':-6,'orientable_genus':4,'homology_diagnostics':homology,
            'scope':'Literal finite seed surface, orientability, and selected homology matrices only. No large homology cover, lifted code, infinite family, or geometric halving conclusion is inferred from finite sampling; those follow from the written theorem.'}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('SEED_SURFACE_PASS faces12 links54 oriented genus4 H1=8 at primes2,3,5,7,11')

if __name__=='__main__':main()
