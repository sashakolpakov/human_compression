#!/usr/bin/env python3
"""Independent finite coset/colored-chamber interface checks; not a uniform proof."""
import argparse
import json
from collections import deque
from itertools import combinations, permutations, product
from pathlib import Path


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def audit_group(name, elements, mul, one, marks):
    elements = tuple(elements)
    inv = {g: next(h for h in elements if mul(g, h) == one and mul(h, g) == one)
           for g in elements}

    def generated(gs):
        found = {one}
        todo = [one]
        while todo:
            x = todo.pop()
            for g in gs:
                y = mul(x, g)
                if y not in found:
                    found.add(y)
                    todo.append(y)
        return frozenset(found)

    need(generated(marks) == set(elements), name + ' generation')
    subsets = [frozenset(s) for n in range(4) for s in combinations(range(3), n)]
    support = {s: generated([mul(inv[marks[i]], marks[j]) for i in s for j in s])
               for s in subsets}
    for s in subsets:
        for t in subsets:
            need(support[s] & support[t] == support[s & t], name + ' C-plus')
    H = [support[frozenset(set(range(3)) - {i})] for i in range(3)]
    cosets = [[*dict.fromkeys(frozenset(mul(g, h) for h in H[i]) for g in elements)]
              for i in range(3)]
    chambers = [c for c in product(*cosets)
                if all(c[i] & c[j] for i, j in combinations(range(3), 2))]
    C = tuple(H)
    D = tuple(frozenset(mul(marks[1], h) for h in H[0]) if i == 0 else H[i]
              for i in range(3))

    def act(g, c):
        return tuple(frozenset(mul(g, h) for h in v) for v in c)

    pos = {act(g, C): (g, False) for g in elements}
    neg = {act(g, D): (g, True) for g in elements}
    need(len(pos) == len(neg) == len(elements) and not pos.keys() & neg.keys(), name + ' free orbits')
    need(set(chambers) == pos.keys() | neg.keys(), name + ' two chamber orbits')
    neighbors = {}
    for c in chambers:
        for i in range(3):
            candidates = [d for d in chambers if d != c and all(c[j] == d[j] for j in range(3) if j != i)]
            need(len(candidates) == 1, name + ' thinness')
            neighbors[c, i] = candidates[0]
    wrong_sign_detected = False
    for g in elements:
        for i in range(3):
            actual = neighbors[act(g, C), i]
            need(actual == act(mul(g, inv[marks[i]]), D), name + ' literal adjacency')
            wrong_sign_detected |= actual != act(mul(g, marks[i]), D)
    need(wrong_sign_detected, name + ' weakened adjacency control')

    # Enumerate all color-preserving chamber automorphisms by the image of C.
    # Every assignment is forced by labeled-neighbor propagation; accept only
    # when every edge is consistent and the resulting map is a bijection.
    aut = []
    for target in chambers:
        mapping = {C: target}
        queue = deque([C])
        consistent = True
        while queue and consistent:
            c = queue.popleft()
            for i in range(3):
                d, e = neighbors[c, i], neighbors[mapping[c], i]
                if d in mapping:
                    if mapping[d] != e:
                        consistent = False
                        break
                else:
                    mapping[d] = e
                    queue.append(d)
        if consistent:
            need(len(mapping) == len(chambers), name + ' chamber connectedness')
            if len(set(mapping.values())) == len(chambers):
                aut.append(mapping)
    # Independently test marked inversion by propagating a group map from the
    # identity and checking all generator edges, then every product.
    theta = {one: one}
    queue = deque([one])
    possible = True
    while queue and possible:
        g = queue.popleft()
        for a in marks:
            h, image = mul(g, a), mul(theta[g], inv[a])
            if h in theta:
                if theta[h] != image:
                    possible = False
                    break
            else:
                theta[h] = image
                queue.append(h)
    if possible:
        need(len(theta) == len(elements) == len(set(theta.values())), name + ' theta bijection')
        need(all(theta[mul(g,h)] == mul(theta[g],theta[h]) for g in elements for h in elements), name + ' theta homomorphism')
    need(len(aut) == len(elements) * (2 if possible else 1), name + ' full group criterion')

    # Check every proper flag's orbit and every rank-two residue directly.
    proper_flags = 0
    rank_two_residues = 0
    for s in subsets:
        if len(s) == 3:
            continue
        flags = {tuple(c[i] for i in sorted(s)) for c in chambers}
        base = tuple(C[i] for i in sorted(s))
        orbit = {tuple(frozenset(mul(g,h) for h in v) for v in base) for g in elements}
        need(flags == orbit, name + ' proper flag transitivity')
        proper_flags += len(flags)
    for fixed_type in range(3):
        for fixed in cosets[fixed_type]:
            types = [i for i in range(3) if i != fixed_type]
            vertices = {(i, v) for i in types for v in cosets[i] if v & fixed}
            first = next(iter(vertices))
            reached = {first}
            todo = [first]
            while todo:
                i, v = todo.pop()
                for j, w in vertices:
                    if i != j and v & w and (j,w) not in reached:
                        reached.add((j,w)); todo.append((j,w))
            need(reached == vertices, name + ' rank-two residue connectedness')
            rank_two_residues += 1
    return {'model': name, 'group_order': len(elements), 'chambers': len(chambers),
            'type_counts': list(map(len, cosets)), 'proper_flags': proper_flags,
            'rank_two_residues': rank_two_residues, 'full_colored_automorphisms': len(aut),
            'marked_inversion_exists': possible, 'wrong_sign_rejected': wrong_sign_detected}


def run():
    # A4 tetrahedral rotation marking, implemented as actual permutations.
    perms = [p for p in permutations(range(4)) if sum(p[i] > p[j] for i in range(4) for j in range(i+1,4)) % 2 == 0]
    compose = lambda a,b: tuple(a[b[i]] for i in range(4))
    a4 = audit_group('tetrahedral A4', perms, compose, tuple(range(4)),
                     [tuple(range(4)), (1,2,0,3), (1,0,3,2)])
    # Norm-five square-torus orientation group, implemented as C5 semidirect C4.
    # The chosen quarter-turn acts by 2 mod5. No geometry library is imported.
    el = list(product(range(5), range(4)))
    mul = lambda a,b: ((a[0] + pow(2,a[1],5)*b[0]) % 5, (a[1]+b[1]) % 4)
    u,v = (0,1),(1,1)
    torus = audit_group('norm-five square torus', el, mul, (0,0), [(0,0),u,mul(u,v)])
    need(a4['marked_inversion_exists'] and not torus['marked_inversion_exists'], 'both full-group cases exercised')
    # A single cyclic matching has n components; the second matching joins all.
    n = 7
    vertices = list(product(range(n), range(2)))
    def components(two):
        unseen=set(vertices); count=0
        while unseen:
            count+=1;todo=[unseen.pop()]
            while todo:
                x,s=todo.pop()
                adjacent=[(x,1-s)] + ([((x+(-1 if s==0 else 1))%n,1-s)] if two else [])
                for v in adjacent:
                    if v in unseen:unseen.remove(v);todo.append(v)
        return count
    need(components(False)==7 and components(True)==1, 'second matching indispensable for this model')
    # Intersection transport needs both image control and kernel control.
    A={0,1};B={0,1};C={0}
    identity=lambda x:x
    zero=lambda x:0
    need({identity(x) for x in A}&{identity(x) for x in B}!={identity(x) for x in C}, 'missing image hypothesis')
    need(A&B&{x for x in range(4) if identity(x)==0} <= C and A&B != C,'image-hypothesis countermodel')
    need({zero(x) for x in A}&{zero(x) for x in B}=={zero(x) for x in C} and not A&B&{0,1,2,3} <= C,'kernel-hypothesis countermodel')
    return {'status':'PASS','models':[a4,torus],
            'controls':['wrong adjacency sign in both full coset geometries','one matching leaves seven components',
                        'missing image equality in intersection transport','missing kernel containment in intersection transport'],
            'scope':'Finite independent checks of the written interfaces only; no uniform theorem, source classification, or finite-cover multiplicity conclusion is inferred.'}


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path);args=ap.parse_args()
    report=run();text=json.dumps(report,indent=2)+'\n'
    if args.out: args.out.write_text(text)
    print(text)
