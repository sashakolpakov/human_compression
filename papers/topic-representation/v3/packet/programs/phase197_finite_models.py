#!/usr/bin/env python3
"""Literal and explicitly repaired L126 models. No assertion-dependent checks."""
import argparse
import itertools as it
import json
import math
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError("P197_REJECT " + message)


def parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2


def model(name, objects, types, incidence, expected, geometric=None):
    need(len(objects) == len(types), name + " type length")
    n = len(objects)
    edges = [[i + 1, j + 1] for i in range(n) for j in range(i + 1, n)
             if incidence(i, j)]
    need(all(types[i - 1] != types[j - 1] for i, j in edges), name + " same-type incidence")
    neighbors = [set() for _ in objects]
    for i, j in edges:
        neighbors[i - 1].add(j - 1)
        neighbors[j - 1].add(i - 1)
    rank = len(set(types))
    flag_counts = [0] * (rank + 1)
    nonextendable = []

    def flags(flag, available):
        flag_counts[len(flag)] += 1
        if flag and len(flag) < rank and not set.intersection(*(neighbors[x] for x in flag)):
            nonextendable.append([x + 1 for x in flag])
        for x in sorted(available):
            flags(flag + [x], {y for y in available & neighbors[x] if y > x})

    flags([], set(range(n)))
    is_geometry = not nonextendable and flag_counts[-1] > 0
    if geometric is not None:
        need(is_geometry == geometric, name + " geometry status")
    return dict(name=name, n=n, rank=rank, types=types, edges=edges,
                expected_groups=expected, flag_counts=flag_counts,
                geometry=is_geometry, nonextendable_witness=next(iter(nonextendable), None))


def dihedral(n):
    directions = [k for k in range(1, (n + 1) // 2) if math.gcd(k, n) == 1]
    obj = [("p", i) for i in range(n)]
    typ = [0 if n % 2 else i % 2 for i in range(n)]
    for k in directions:
        obj += [("e", frozenset((x, (x + k) % n))) for x in range(n)]
        typ += [len(set(typ))] * n

    def inc(i, j):
        a, b = obj[i], obj[j]
        if a[0] == b[0] == "p":
            return n % 2 == 0 and typ[i] != typ[j]
        if a[0] == b[0] == "e":
            return typ[i] != typ[j]
        return a[1] in b[1]

    phi = sum(math.gcd(k, n) == 1 for k in range(n))
    return model("dihedral_" + str(n), obj, typ, inc,
                 [6, 12] if n == 3 else [2 * n if n % 2 else n, n * phi])


def symmetric(n):
    obj = [("p", i) for i in range(n)] + [("e", frozenset(e)) for e in it.combinations(range(n), 2)]
    typ = [0] * n + [1] * (len(obj) - n)
    return model("complete_" + str(n), obj, typ,
                 lambda i, j: obj[i][0] == "p" and obj[j][0] == "e" and obj[i][1] in obj[j][1],
                 [math.factorial(n), 12 if n == 3 else math.factorial(n)], True)


def cube(repaired):
    vertices = list(it.product(range(2), repeat=3))
    edges = [frozenset(e) for e in it.combinations(range(8), 2)
             if sum(a != b for a, b in zip(vertices[e[0]], vertices[e[1]])) == 1]
    faces = [frozenset(i for i, v in enumerate(vertices) if v[k] == bit)
             for k in range(3) for bit in range(2)]
    supports = [frozenset([i]) for i in range(8)] + edges + faces
    typ = [sum(v) % 2 for v in vertices] + [2] * 12 + [3] * 6

    def inc(i, j):
        if typ[i] == typ[j]:
            return False
        if i < 8 and j < 8:
            return repaired and frozenset((i, j)) in edges
        return supports[i] <= supports[j] or supports[j] <= supports[i]

    return model("cube_repaired" if repaired else "cube_literal", supports, typ, inc, [24, 48], repaired)


def petersen():
    vertices = list(map(frozenset, it.combinations(range(5), 2)))
    edges = [frozenset((i, j)) for i, j in it.combinations(range(10), 2) if not vertices[i] & vertices[j]]
    cycle_data = []
    for tail in it.permutations(range(1, 5)):
        order = (0,) + tail
        if order[1] > order[-1]:
            continue
        support = frozenset(vertices.index(frozenset((order[i], order[(i + 1) % 5]))) for i in range(5))
        cycle_edges = frozenset(e for e in edges if e <= support)
        need(len(cycle_edges) == 5, "Petersen pentagon")
        cycle_data.append((parity(order), order, support, cycle_edges))
    cycle_data.sort()
    need([x[0] for x in cycle_data] == [0] * 6 + [1] * 6, "Petersen halves")
    supports = [frozenset([i]) for i in range(10)] + edges + [x[2] for x in cycle_data]
    typ = [0] * 10 + [1] * 15 + [2 + x[0] for x in cycle_data]
    hist = {}
    for a in cycle_data[:6]:
        for b in cycle_data[6:]:
            shared_edges = a[3] & b[3]
            shared_points = a[2] & b[2]
            key = (len(shared_points), len(shared_edges))
            hist[str(key)] = hist.get(str(key), 0) + 1
            need(set().union(*shared_edges) == set(shared_points), "common vertices lie on common edges")
    need(hist == {"(3, 2)": 30, "(0, 0)": 6}, "Petersen cross-cycle table")

    def inc(i, j):
        if typ[i] == typ[j]:
            return False
        if i >= 25 and j >= 25:
            return bool(cycle_data[i - 25][3] & cycle_data[j - 25][3])
        return supports[i] <= supports[j] or supports[j] <= supports[i]

    out = model("petersen_completed", supports, typ, inc, [60, 120], True)
    out["cross_cycle_intersections"] = hist
    out["cycles"] = [dict(parity=a, order=b, support=sorted(c), edges=[sorted(e) for e in sorted(d, key=lambda x: sorted(x))])
                     for a, b, c, d in cycle_data]
    need(out["flag_counts"][-1] == 120, "Petersen chamber count")
    return out


def doily():
    duads = list(map(frozenset, it.combinations(range(6), 2)))
    triples = [frozenset(c) for c in it.combinations(range(15), 3)
               if len(set().union(*(duads[i] for i in c))) == 6]
    need(len(triples) == 15, "syntheme count")
    return model("duad_syntheme", duads + triples, [0] * 15 + [1] * 15,
                 lambda i, j: i < 15 <= j and i in triples[j - 15], [720, 1440], True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gap-output", type=Path, required=True)
    parser.add_argument("--alter-petersen", action="store_true")
    args = parser.parse_args()
    cases = [dihedral(n) for n in range(3, 13)] + [symmetric(n) for n in range(2, 9)]
    cases += [cube(False), cube(True), petersen(), doily()]
    if args.alter_petersen:
        target = next(c for c in cases if c["name"] == "petersen_completed")
        removed = next(e for e in target["edges"] if min(e) >= 26)
        target["edges"].remove(removed)
        need(target["edges"] == petersen()["edges"], "altered Petersen cross-incidence")
    gap = ["P197Cases := ["]
    for c in cases:
        gap.append("rec(name:=" + json.dumps(c["name"]) + ", n:=" + str(c["n"]) +
                   ", types:=" + str([t + 1 for t in c["types"]]) + ", edges:=" + str(c["edges"]) +
                   ", expected:=" + str(c["expected_groups"]) + "),")
    gap[-1] = gap[-1].rstrip(",")
    gap += ["];;", ""]
    args.output.write_text(json.dumps(dict(status="PASS_FINITE_LITERAL_AND_EXPLICIT_COMPLETIONS", cases=cases), indent=2) + "\n")
    args.gap_output.write_text("\n".join(gap))


if __name__ == "__main__":
    main()
