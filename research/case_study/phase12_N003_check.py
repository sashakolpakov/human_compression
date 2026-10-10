#!/usr/bin/env python3
"""Exact finite diagnostics for the forest/parity reduction; not a uniform proof.

Only the Python standard library is used. Actual permutation closures and
cosets are compared with independently constructed component/sign predicates.
Historical certificates are neither imported nor changed.
"""
import argparse
import hashlib
import itertools as it
import json
import math
from pathlib import Path


def trees(n):
    for word in it.product(range(n), repeat=n - 2):
        degree = [1] * n
        for x in word:
            degree[x] += 1
        edges = []
        for x in word:
            leaf = next(i for i in range(n) if degree[i] == 1)
            edges.append(tuple(sorted((leaf, x))))
            degree[leaf] -= 1
            degree[x] -= 1
        ends = [i for i in range(n) if degree[i] == 1]
        edges.append(tuple(ends))
        yield tuple(sorted(edges))


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def transposition(n, e):
    p = list(range(n))
    p[e[0]], p[e[1]] = p[e[1]], p[e[0]]
    return tuple(p)


def sign(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2


def components(n, edges):
    parent = list(range(n))

    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i

    for a, b in edges:
        parent[root(a)] = root(b)
    return [root(i) for i in range(n)]


class Permutations:
    def __init__(self, n):
        self.n = n
        self.perms = list(it.permutations(range(n)))
        self.index = {p: i for i, p in enumerate(self.perms)}
        self.identity = self.index[tuple(range(n))]
        self.full = (1 << len(self.perms)) - 1
        self.even = sum(1 << i for i, p in enumerate(self.perms) if sign(p) == 0)
        self.action = {}
        self.closure_cache = {}
        self.coset_cache = {}

    def right(self, g):
        if g not in self.action:
            self.action[g] = [self.index[compose(p, self.perms[g])] for p in self.perms]
        return self.action[g]

    def subgroup(self, gens):
        key = tuple(sorted(set(gens)))
        if key not in self.closure_cache:
            steps = [self.right(g) for g in key]
            seen, stack = {self.identity}, [self.identity]
            while stack:
                x = stack.pop()
                for step in steps:
                    y = step[x]
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            self.closure_cache[key] = sum(1 << x for x in seen)
        return self.closure_cache[key]

    def component_group(self, edges):
        block = components(self.n, edges)
        return sum(1 << j for j, p in enumerate(self.perms)
                   if all(block[i] == block[p[i]] for i in range(self.n)))

    def cosets(self, subgroup):
        if subgroup not in self.coset_cache:
            result, remaining = [], self.full
            members = [i for i in range(len(self.perms)) if subgroup >> i & 1]
            while remaining:
                x = (remaining & -remaining).bit_length() - 1
                step = self.right(x)
                coset = sum(1 << step[h] for h in members)
                assert (coset & remaining) == coset
                result.append(coset)
                remaining ^= coset
            self.coset_cache[subgroup] = result
        return self.coset_cache[subgroup]


def all_helly(P, parabolics):
    """Enumerate every nonempty typed partial flag, not just full chambers."""
    cosets = [P.cosets(H) for H in parabolics]
    flags = 0

    def walk(i, chosen, meet):
        nonlocal flags
        for j in range(i, len(cosets)):
            for C in cosets[j]:
                if all(C & D for D in chosen):
                    common = meet & C
                    assert common, (P.n, j, chosen, C)
                    flags += 1
                    walk(j + 1, chosen + [C], common)

    walk(0, [], P.full)
    return flags


def check_marking(P, edges, distinguished, check_helly):
    tau = [P.index[transposition(P.n, e)] for e in edges]
    if distinguished is None:
        gens = tau
    else:
        s = P.perms[tau[distinguished]]
        gens = [tau[i] if i == distinguished else
                P.index[compose(s, P.perms[tau[i]])] for i in range(len(edges))]
    r = len(gens)
    groups = []
    for mask in range(1 << r):
        H = P.subgroup([gens[i] for i in range(r) if mask >> i & 1])
        forest = [edges[i] for i in range(r)
                  if mask >> i & 1 or i == distinguished]
        expected = P.component_group(forest)
        if distinguished is not None and not (mask >> distinguished & 1):
            expected &= P.even
        assert H == expected, (P.n, edges, distinguished, mask)
        groups.append(H)
    assert groups[-1] == P.full
    assert groups[0] == 1 << P.identity
    assert len(set(groups)) == 1 << r
    for I, H in enumerate(groups):
        for J, K in enumerate(groups):
            assert H & K == groups[I & J]
    full = (1 << r) - 1
    parabolics = [groups[full ^ (1 << i)] for i in range(r)]
    assert all(not (H >> gens[i] & 1) for i, H in enumerate(parabolics))
    flags = all_helly(P, parabolics) if check_helly else 0
    # Check actual residual-generation identities (source G2).
    for mask, H in enumerate(groups):
        if mask.bit_count() < 2:
            continue
        subgroups = [groups[mask ^ (1 << i)] for i in range(r) if mask >> i & 1]
        union = 0
        for subgroup in subgroups:
            union |= subgroup
        actual = P.subgroup([i for i in range(len(P.perms)) if union >> i & 1])
        assert actual == H
    return {"subset_groups": len(groups), "intersection_checks": len(groups) ** 2,
            "typed_partial_flags": flags}


def marked_counts(n):
    raw, inverse_classes = set(), set()
    tree_count = 0
    for edges in trees(n):
        tree_count += 1
        taus = [transposition(n, e) for e in edges]
        for i, s in enumerate(taus):
            marking = [s] + [compose(s, t) for j, t in enumerate(taus) if j != i]
            raw.add(tuple(sorted(marking)))
            inverse_classes.add(tuple(sorted(min(g, inverse(g)) for g in marking)))
    expected = (n ** (n - 2), (n - 1) * n ** (n - 2),
                math.comb(n, 2) * (n - 1) ** (n - 3))
    actual = (tree_count, len(raw), len(inverse_classes))
    assert actual == expected
    return {"n": n, "trees": actual[0], "actual_twisted_sets": actual[1],
            "inverse_identified_twisted_sets": actual[2]}


def inverse(p):
    result = [0] * len(p)
    for i, j in enumerate(p):
        result[j] = i
    return tuple(result)


def span(vectors):
    result = {0}
    for v in vectors:
        if v not in result:
            result |= {w ^ v for w in result}
    return frozenset(result)


def module_check(m):
    vectors = range(1 << m)
    cyclic = {v: span(w for w in vectors if w.bit_count() == v.bit_count())
              for v in vectors}
    pair_span = {(v, w): span(cyclic[v] | cyclic[w])
                 for v in vectors for w in vectors if v < w}
    triples = 0
    for a, b, c in it.combinations(range(1, 1 << m), 3):
        triples += 1
        assert (a in pair_span[b, c] or b in pair_span[a, c]
                or c in pair_span[a, b])
    even = {v for v in vectors if v.bit_count() % 2 == 0}
    for v in vectors:
        if v not in (0, (1 << m) - 1):
            assert even <= cyclic[v]
    return {"dimension": m, "nonzero_triples_tested": triples,
            "max_independent_family_at_most": 2}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="phase12_N003_check.json")
    args = parser.parse_args()
    counts = [marked_counts(n) for n in range(3, 7)]
    records = []
    for n in range(3, 7):
        P = Permutations(n)
        chosen = list(trees(n)) if n <= 5 else [
            tuple((i, i + 1) for i in range(n - 1)),
            tuple((0, i) for i in range(1, n)),
            ((0, 1), (0, 2), (0, 3), (3, 4), (4, 5)),
        ]
        totals = {"markings": 0, "subset_groups": 0, "intersection_checks": 0,
                  "typed_partial_flags": 0}
        for edges in chosen:
            for distinguished in [None] + list(range(n - 1)):
                # Full Helly enumeration for every n<=5 marking; three shapes at n=6.
                result = check_marking(P, edges, distinguished, True)
                totals["markings"] += 1
                for key, value in result.items():
                    totals[key] += value
        records.append({"n": n, "trees_checked": len(chosen), **totals})
    report = {
        "status": "PASS",
        "scope": "Finite diagnostic only; no verification of Whiston inputs or all-n classification",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "labelled_counts": counts,
        "actual_group_and_coset_checks": records,
        "permutation_module_checks": [module_check(m) for m in range(3, 7)],
        "all_parameter_proof": "phase12_N003_reduction.md",
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
