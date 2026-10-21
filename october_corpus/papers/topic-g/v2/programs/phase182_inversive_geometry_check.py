#!/usr/bin/env python3
"""Literal Construction 2 on the F3 sublines of P1(F9).

An independently generated finite diagnostic for L092 Lemma 5. The output
is a finite certificate, not a classification of every source parameter.
"""
from collections import Counter, deque
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise RuntimeError(message)


def add(x, y):
    return (x % 3 + y % 3) % 3 + 3 * ((x // 3 + y // 3) % 3)


def mul(x, y):
    a, b, c, d = x % 3, x // 3, y % 3, y // 3
    return (a*c + 2*b*d) % 3 + 3 * ((a*d + b*c) % 3)


def inv(x):
    require(x != 0, "division by zero")
    return next(y for y in range(1, 9) if mul(x, y) == 1)


def compose(a, b):
    return tuple(a[b[i]] for i in range(10))


def generated_permutations(gens):
    seen = {tuple(range(10))}
    queue = deque(seen)
    while queue:
        old = queue.popleft()
        for g in gens:
            new = compose(g, old)
            if new not in seen:
                seen.add(new)
                queue.append(new)
    return sorted(seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), "refusing existing output")
    # F9 = F3[a]/(a^2+1), encoded x+3y; infinity has label 9.
    translation = tuple(add(x, 1) if x < 9 else 9 for x in range(10))
    scaling = tuple(mul(x, 4) if x < 9 else 9 for x in range(10))
    inversion = tuple(9 if x == 0 else 0 if x == 9 else inv(x) for x in range(10))
    pgl = generated_permutations([translation, scaling, inversion])
    require(len(pgl) == 720, "wrong PGL action")
    seed = frozenset([0, 1, 2, 9])
    blocks = sorted({tuple(sorted(g[x] for x in seed)) for g in pgl})
    require(len(blocks) == 30, "wrong subline orbit")
    triple_counts = Counter(T for B in blocks for T in combinations(B, 3))
    require(len(triple_counts) == 120 and set(triple_counts.values()) == {1},
            "not an S(3,4,10)")
    blocksets = [frozenset(B) for B in blocks]
    objects = []
    # Global object numbers carry their type explicitly, so the copied point
    # set cannot accidentally be identified with the original one.
    for x in range(10):
        objects.append((0, x))
    for B in blocksets:
        for T in combinations(sorted(B), 2):
            T = frozenset(T)
            objects.append((1, (T, B-T)))
    for B in blocksets:
        objects.append((2, B))
    for x in range(10):
        objects.append((3, x))
    bytype = [set(i for i, (t, _) in enumerate(objects) if t == k) for k in range(4)]
    neighbours = [set() for _ in objects]

    def incident(i, j):
        ti, x = objects[i]
        tj, y = objects[j]
        if ti > tj:
            return incident(j, i)
        if ti == tj:
            return i == j
        if (ti, tj) == (0, 1):
            return x in y[0]
        if (ti, tj) == (0, 2):
            return x in y
        if (ti, tj) == (0, 3):
            return x != y
        if (ti, tj) == (1, 2):
            return x[0] <= y and not (x[1] & y)
        if (ti, tj) == (1, 3):
            return y in x[1]
        if (ti, tj) == (2, 3):
            return y not in x
        raise RuntimeError("unhandled type pair")

    for i, j in combinations(range(len(objects)), 2):
        if incident(i, j):
            neighbours[i].add(j)
            neighbours[j].add(i)
    allflags = [[] for _ in range(5)]

    def flags(prefix, choices):
        allflags[len(prefix)].append(tuple(prefix))
        for i in sorted(choices):
            flags(prefix+[i], {j for j in choices & neighbours[i] if j > i})

    flags([], set(range(len(objects))))
    chambers = set(allflags[4])
    extended = set()
    for C in chambers:
        for size in range(5):
            extended.update(combinations(C, size))
    require(all(F in extended for layer in allflags for F in layer),
            "nonextendable flag in literal construction")

    def residue(F):
        used = {objects[i][0] for i in F}
        remaining = set.union(*(bytype[t] for t in range(4) if t not in used))
        for i in F:
            remaining &= neighbours[i]
        return remaining

    panel_counts = Counter(len(residue(F)) for F in allflags[3])
    require(min(panel_counts) >= 2, "not firm")
    connected_by_corank = Counter()
    for size in range(3):
        for F in allflags[size]:
            R = residue(F)
            require(bool(R), "empty rank-at-least-two residue")
            seen = {min(R)}
            queue = deque(seen)
            while queue:
                i = queue.popleft()
                new = (neighbours[i] & R) - seen
                seen.update(new)
                queue.extend(new)
            require(seen == R, "disconnected residue: " + repr(F))
            connected_by_corank[4-size] += 1

    # The full PGL orbit construction is independent of the incidence tests.
    # Its literal point permutations induce automorphisms of all four types.
    def image_object(obj, g):
        t, x = obj
        if t in [0, 3]:
            return t, g[x]
        if t == 2:
            return t, frozenset(g[p] for p in x)
        return t, (frozenset(g[p] for p in x[0]), frozenset(g[p] for p in x[1]))

    index = {obj: i for i, obj in enumerate(objects)}
    frobenius = tuple(mul(mul(x, x), x) if x < 9 else 9 for x in range(10))
    semilinear = generated_permutations([translation, scaling, inversion, frobenius])
    require(len(semilinear) == 1440, "wrong semilinear subgroup order")
    automorphism_checks = 0
    for g in [translation, scaling, inversion, frobenius]:
        perm = [index[image_object(obj, g)] for obj in objects]
        require(len(set(perm)) == len(objects), "object action is not bijective")
        for i in range(len(objects)):
            require({perm[j] for j in neighbours[i]} == neighbours[perm[i]],
                    "incidence action failure")
            automorphism_checks += 1
    remaining_chambers = set(chambers)
    orbit_sizes = []
    while remaining_chambers:
        C = min(remaining_chambers)
        orbit = {tuple(sorted(index[image_object(objects[i], g)] for i in C))
                 for g in semilinear}
        require(orbit <= remaining_chambers, "nonpartitioned chamber orbit")
        orbit_sizes.append(len(orbit))
        remaining_chambers -= orbit
    encoding = {'blocks':blocks,'objects':[(t, x if t in [0,3] else
                  sorted(x) if t == 2 else [sorted(x[0]), sorted(x[1])])
                  for t, x in objects],
                'neighbours':[sorted(N) for N in neighbours]}
    report = {'status':'PASS','source':'L092, Construction 2 and Lemma 5',
              'parameters':{'q':3,'e':2,'t':3,'k':4,'v':10},
              'field':'F3[a]/(a^2+1); elements x+3y; infinity=9',
              'group_generators':[translation,scaling,inversion],
              'PGL_order':len(pgl),'semilinear_subgroup_order':len(semilinear),
              'blocks':len(blocks),'steiner_triples':len(triple_counts),
              'object_counts':[len(S) for S in bytype],
              'all_flag_counts':[len(F) for F in allflags],
              'all_flags_extend':True,'panel_completion_distribution':dict(panel_counts),
              'connected_residues_by_corank':dict(connected_by_corank),
              'incidence_automorphism_vertex_checks':automorphism_checks,
              'semilinear_chamber_orbit_sizes':sorted(orbit_sizes),
              'full_geometry_automorphism_group_computed':False,
              'full_design_automorphism_group_computed':False,
              'literal_Lemma_5_residual_connectedness_counterexample':True,
              'does_not_refute_Theorem_11_flag_transitive_classification':True,
              'Lean_certificate':False,
              'certificate_sha256':hashlib.sha256(json.dumps(encoding,sort_keys=True).encode()).hexdigest(),
              'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with args.output.open('x') as f:
        json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
