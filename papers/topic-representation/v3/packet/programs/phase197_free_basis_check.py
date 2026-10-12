#!/usr/bin/env python3
"""Bounded checks of the reduced-word criterion and finite source core graphs."""
import argparse
import itertools as it
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError("P197_REJECT " + message)


def words(rank, length):
    current = [()]
    yield ()
    alphabet = [s * i for i in range(1, rank + 1) for s in (1, -1)]
    for _ in range(length):
        current = [w + (a,) for w in current for a in alphabet if not w or w[-1] != -a]
        yield from current


def factor_membership(w, omitted, i):
    # Independent of the last-i prefix: try every cut in the reduced word.
    return any(not (set(map(abs, w[:k])) & omitted) and i not in map(abs, w[k:])
               for k in range(len(w) + 1))


def check_words(rank, length, alter_prefix):
    total = 0
    for w in words(rank, length):
        support = set(map(abs, w))
        for i in range(1, rank + 1):
            occurrences = [k + 1 for k, a in enumerate(w) if abs(a) == i]
            end = (min if alter_prefix else max)(occurrences, default=0)
            prefix_support = set(map(abs, w[:end]))
            others = [j for j in range(1, rank + 1) if j != i]
            for size in range(rank):
                for js in it.combinations(others, size):
                    omitted = set(js)
                    cut = factor_membership(w, omitted, i)
                    need(cut == (not omitted & prefix_support), "last-occurrence cut criterion")
                    pairwise = all(factor_membership(w, {j}, i) for j in js)
                    need(cut == pairwise, "all-factor product identity")
        total += 1
    return dict(rank=rank, max_length=length, reduced_words=total)


def core(n):
    # Positive labels orient edges; record outgoing positive and inverse labels.
    oriented = {0: set()}
    edges = []
    for j in range(1, n + 1):
        for sign in (1, -1):
            v = (j, sign)
            oriented[v] = set()
            edges.append((0, v, j * sign))
            for i in range(1, n + 1):
                if i != j:
                    edges.append((v, v, i))
    for u, v, label in edges:
        need(label not in oriented[u], "folded graph outgoing label")
        oriented[u].add(label)
        need(-label not in oriented[v], "folded graph inverse label")
        oriented[v].add(-label)
    rank = len(edges) - len(oriented) + 1
    need(rank == 2 * n * (n - 1), "core rank")
    return dict(ambient_rank=n, vertices=len(oriented), unoriented_edges=len(edges), free_rank=rank)


def signed_type_actions(n):
    basis = [(j, sign, i) for j in range(n) for sign in (1, -1) for i in range(n) if i != j]
    actions = set()
    signed_actions = set()
    for p in it.permutations(range(n)):
        for eps in it.product((1, -1), repeat=n):
            action = tuple(basis.index((p[j], sign * eps[j], p[i])) for j, sign, i in basis)
            signed = tuple((action[k], eps[i]) for k, (_, _, i) in enumerate(basis))
            actions.add(action)
            signed_actions.add(signed)
    need(len(actions) == len(signed_actions) == 2**n * __import__('math').factorial(n), "ambient signed subgroup")
    if n == 2:
        three_cycle = (1, 2, 0, 3)
        need(three_cycle not in actions, "basis three-cycle outside source square group")
        need(len(set(it.permutations(range(4)))) == 24 and len(actions) == 8, "S4 versus square group")
    return dict(ambient_rank=n, basis_size=len(basis), source_type_image_order=len(actions))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--alter-prefix", action="store_true")
    args = p.parse_args()
    result = dict(status="PASS_BOUNDED_FREE_WORD_AND_CORE_CHECKS",
                  words=[check_words(3, 6, args.alter_prefix), check_words(4, 5, args.alter_prefix)],
                  cores=[core(n) for n in range(2, 7)],
                  signed_actions=[signed_type_actions(n) for n in range(2, 5)])
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
