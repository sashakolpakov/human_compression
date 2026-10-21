#!/usr/bin/env python3
"""Independent finite checks of the new interfaces, not uniform proofs."""
import argparse
import itertools as it
import json
from functools import lru_cache
from pathlib import Path

def need(b, m):
    if not b:
        raise ValueError(m)

def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))

def generated(gens, n):
    identity = tuple(range(n))
    group = {identity}
    todo = [identity]
    for p in todo:
        for g in gens:
            q = compose(p, g)
            if q not in group:
                group.add(q)
                todo.append(q)
    return frozenset(group)

def image(p, bits):
    return sum(1 << p[i] for i in range(len(p)) if bits >> i & 1)

def sign(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p))) % 2

def laminar_test():
    n = 4
    omega = (1 << n) - 1
    perms = list(it.permutations(range(n)))
    images = {(p, a): image(p, a) for p in perms for a in range(1 << n)}
    count = roots = characters = duplicates = 0
    families = [a for k in range(4) for a in it.combinations(range(16), k)
                if all((x & y) in (0, x, y) for x, y in it.combinations(a, 2))]
    # Include duplicate empty/full/nontrivial constraints explicitly.
    families += [(0, 0), (15, 15), (3, 3), (0, 3, 3)]
    for a in families:
        targets = it.product(*[[x for x in range(16) if x.bit_count() == s.bit_count()] for s in a])
        for xs in targets:
            if any((a[i]&a[j]).bit_count() != (xs[i]&xs[j]).bit_count()
                   for i in range(len(a)) for j in range(i)):
                continue
            realizations = [p for p in perms if all(images[p,s] == t for s,t in zip(a,xs))]
            need(realizations, 'laminar images have no realization')
            count += 1
            duplicates += int(len(set(a)) < len(a))
            domain_mask = omega
            target_mask = omega
            for s,t in zip(a,xs):
                domain_mask &= omega ^ s
                target_mask &= omega ^ t
            for qmask in range(16):
                if qmask & ~domain_mask:
                    continue
                q = [i for i in range(n) if qmask >> i & 1]
                d = [i for i in range(n) if target_mask >> i & 1]
                for u in it.permutations(d, len(q)):
                    sols = set(p for p in realizations if all(p[i] == j for i,j in zip(q,u)))
                    need(sols, 'prescribed root injection fails')
                    roots += 1
                    k = [p for p in perms if all(images[p,s] == s for s in a) and all(p[i] == i for i in q)]
                    g0 = min(sols)
                    need(sols == {compose(g0,p) for p in k}, 'wrong stabilizer coset')
                    need({sign(p) for p in sols} == {(sign(g0)+sign(p)) % 2 for p in k}, 'wrong character image')
                    characters += 1
    # Three deliberate weakened statements have exact counterexamples.
    a, xs = (3,5,9), (3,5,6)
    need(all((a[i]&a[j]).bit_count() == (xs[i]&xs[j]).bit_count() for i in range(3) for j in range(i)), 'pair counts')
    need(not any(all(image(p,s) == t for s,t in zip(a,xs)) for p in perms), 'nonlaminar weakening')
    need(not any(p[0] == 2 and image(p,2) == 4 for p in perms), 'overlap weakening')
    need(not any(sign(p) == 1 and p[:3] == (0,1,2) for p in perms), 'unjustified parity freedom')
    return dict(selected_families=len(families), target_configurations=count,
                prescribed_root_injections=roots, exact_torsors_and_sign_images=characters,
                duplicate_constraint_configurations=duplicates,
                weakening_controls=['nonlaminar pairwise data', 'root image in target', 'parity without stabilizer image'])

def binary_test():
    n=4
    perms=list(it.permutations(range(n)))
    identity=tuple(range(n))
    subgroups={frozenset([identity])}
    todo=list(subgroups)
    for h in todo:
        for g in perms:
            if g in h:
                continue
            k=generated(list(h)+[g], n)
            if k not in subgroups:
                subgroups.add(k);todo.append(k)
    transitive=[h for h in subgroups if len({p[0] for p in h})==n]
    rows=[]
    for h in sorted(transitive, key=lambda x:(len(x), sorted(x))):
        @lru_cache(None)
        def linear_span(vectors):
            span={0}
            for v in vectors:
                span |= {w^v for w in list(span)}
            return frozenset(span)
        cyclic={v:linear_span(tuple(sorted({image(p,v) for p in h}))) for v in range(1,16)}
        @lru_cache(None)
        def module_span(family):
            return linear_span(tuple(sorted(set().union(*(cyclic[v] for v in family))))) if family else frozenset([0])
        maximum=0;tests=0
        for size in range(1,5):
            for family in it.combinations(range(1,16),size):
                independent=all(v not in module_span(family[:i]+family[i+1:]) for i,v in enumerate(family))
                tests+=1
                if independent: maximum=max(maximum,size)
        need(maximum<=2,'transitive binary m=4 bound')
        rows.append(dict(group_order=len(h),maximum_independent_vectors=maximum,families_tested=tests))
    need(len(subgroups)==30 and len(transitive)==9,'complete independently enumerated S4 subgroup list')
    # For the trivial action the four coordinate vectors are independent.
    basis=(1,2,4,8)
    need(all(v not in {sum(basis[j] for j in range(4) if mask>>j&1) for mask in range(16) if not(mask>>i&1)} for i,v in enumerate(basis)), 'nontransitive countermodel')
    return dict(S4_subgroups=len(subgroups),transitive_subgroups=len(transitive),groups=rows,
                weakening_control='trivial action has four independent coordinate vectors',
                uniform_proof=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh report required')
    report=dict(status='PASS',laminar=laminar_test(),binary=binary_test(),
                scope='Independent exhaustive degree-four diagnostics. The uniform conclusions are assessed by written proof reading, not inferred from these samples.')
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()
