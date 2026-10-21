#!/usr/bin/env python3
"""Independent finite quotient-module and literal-diagram diagnostics."""
import argparse
import itertools as it
import json
from pathlib import Path


def require(b, text):
    if not b:
        raise ValueError(text)


def act(v, p):
    return sum(((v >> j) & 1) << p[j] for j in range(len(p)))


def product(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def span(vectors):
    S = {0}
    for v in vectors:
        S |= {w ^ v for w in S}
    return frozenset(S)


def all_subspaces(r):
    known, todo = {frozenset((0,))}, [frozenset((0,))]
    while todo:
        S = todo.pop()
        for v in range(1 << r):
            if v not in S:
                T = frozenset(S | {w ^ v for w in S})
                if T not in known:
                    known.add(T)
                    todo.append(T)
    return known


def gen(generators, mul, one):
    S, todo = {one}, [one]
    while todo:
        x = todo.pop()
        for g in generators:
            y = mul(x, g)
            if y not in S:
                S.add(y)
                todo.append(y)
    return frozenset(S)


def adjacent(r, i):
    p = list(range(r))
    p[i - 1], p[i] = p[i], p[i - 1]
    return tuple(p)


def quotient_models(r):
    one = tuple(range(r))
    swaps = [adjacent(r, i) for i in range(1, r)]
    subspaces = all_subspaces(r)
    stable = sorted((S for S in subspaces if
                     all(act(v, p) in S for p in swaps for v in S)), key=lambda S: (len(S), sorted(S)))
    rows = []
    for R in stable:
        if 1 in R:
            continue  # Excludes exactly the zero seed (the whole module).
        red = lambda v: min(v ^ k for k in R)
        z = red(1)
        require(z != 0, "nonzero seed required")
        def mul(x, y):
            return red(x[0] ^ act(y[0], x[1])), product(x[1], y[1])
        marks = [(z, one)] + [(0, p) for p in swaps]
        groups = []
        for mask in range(1 << r):
            groups.append(gen([marks[i] for i in range(r) if mask & (1 << i)], mul, (0, one)))
            E = [i for i in range(1, r) if mask & (1 << i)]
            P = gen([swaps[i - 1] for i in E], product, one)
            k = 1
            while k < r and k in E:
                k += 1
            W = span([red(1 << j) for j in range(k)]) if mask & 1 else {0}
            # Canonical quotient representatives require reduction after summing.
            W = {red(v) for v in W}
            require(groups[-1] == frozenset(it.product(W, P)), "all parabolic prefix formulas")
        require(all(groups[m] & groups[n] == groups[m & n]
                    for m in range(1 << r) for n in range(1 << r)), "all intersection identities")
        rows.append({"relation_subspace": sorted(R), "group_order": len(groups[-1]),
                     "parabolics": len(groups), "IP_pairs": 1 << (2 * r)})
    return {"rank": r, "all_subspaces_tested": len(subspaces),
            "invariant_subspaces": len(stable), "nonzero_quotient_models": rows}


def sign(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2


def coordinate_permutation(v, p):
    return tuple(2 * p[j] + (bit ^ ((v >> p[j]) & 1))
                 for j in range(len(p)) for bit in range(2))


def source_diagram_marks(r, family):
    # Literal vertical label sets from Table6(15),(16), Table9(2),
    # read with Notation2.6: I_subscript is the complement in {0,...,r-1}.
    labels = set(range(r))
    vertical = []
    for j in range(r):
        excluded = {i for i in (j, j + 1) if 1 <= i < r}
        if family == "15" and j != 0:
            excluded.add(0)
        if family == "16" and j == 0:
            excluded.add(0)
        vertical.append(labels - excluded)
    result = []
    for i in range(r):
        p = list(range(2 * r))
        for j in range(r):
            if i in vertical[j]:
                p[2*j], p[2*j+1] = p[2*j+1], p[2*j]
        if i:
            for bit in range(2):
                u, v = 2*(i-1)+bit, 2*i+bit
                require(p[u] == u and p[v] == v, "horizontal endpoints have no vertical label")
                p[u], p[v] = v, u
        result.append(tuple(p))
    return result


def shears(r, exhaustive=False):
    one = tuple(range(r))
    lam = (1 << r) - 1
    a = sum(1 << j for j in range(r) if j % 2)
    def cocycle(p):
        return (lam if sign(p) else 0) ^ a ^ act(a, p)
    if exhaustive:
        perms = tuple(it.permutations(range(r)))
        cache = {p: cocycle(p) for p in perms}
        require(all(cache[product(p, q)] == cache[p] ^ act(cache[q], p)
                    for p in perms for q in perms), "cocycle for all permutation pairs")
        require(all((v ^ cache[p]) ^ cache[p] == v for v in range(1 << r) for p in perms),
                "involutory ambient shear")
        pairs = len(perms) ** 2
    else:
        pairs = None
    seeds = {"15": 1, "16": lam ^ 1, "Table9(2)": lam}
    for family, z in seeds.items():
        source = source_diagram_marks(r, family)
        target = [coordinate_permutation(z, one)]
        for i in range(1, r):
            p = adjacent(r, i)
            require(cocycle(p) == lam ^ (1 << (i-1)) ^ (1 << i), "adjacent cocycle formula")
            target.append(coordinate_permutation(cocycle(p), p))
        require(source == target, "literal source diagram transport")
    return {"rank": r, "permutation_pairs": pairs, "source_diagrams": list(seeds),
            "all_generator_permutations_equal": True}


def run():
    return {"status": "PASS", "module_quotients": [quotient_models(r) for r in range(2, 6)],
            "shears": [shears(r, exhaustive=r <= 5) for r in range(2, 13)],
            "scope": "Exhaustive small quotient modules and actual graph generator diagnostics; the arbitrary-r/module theorem is verified by written proof review."}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    data = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if a.out:
        require(not a.out.exists(), "fresh output required")
        a.out.write_text(data)
    else:
        print(data, end="")
