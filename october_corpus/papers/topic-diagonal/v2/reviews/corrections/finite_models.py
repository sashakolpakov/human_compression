#!/usr/bin/env python3
"""Independent explicit finite models; standard library, no assert/native GAP."""
import argparse
import itertools as it
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def generated(gens, mul, identity):
    seen, pending = {identity}, [identity]
    while pending:
        x = pending.pop()
        for y in gens:
            z = mul(x, y)
            if z not in seen:
                seen.add(z)
                pending.append(z)
    return frozenset(seen)


def left_cosets(group, subgroup, mul):
    unseen, result = set(group), []
    while unseen:
        g = min(unseen)
        coset = frozenset(mul(g, h) for h in subgroup)
        require(coset <= unseen, "cosets partition")
        unseen -= coset
        result.append(coset)
    return result


def coord_action(v, p):
    return sum(((v >> i) & 1) << p[i] for i in range(len(p)))


def permutation_product(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def wreath_three():
    perms = tuple(it.permutations(range(3)))
    unit = tuple(range(3))
    identity = (0, unit)
    def mul(x, y):
        return x[0] ^ coord_action(y[0], x[1]), permutation_product(x[1], y[1])
    group = tuple(it.product(range(8), perms))
    cycle = (1, 2, 0)
    cyclic = generated([cycle], permutation_product, unit)
    B = frozenset((0, p) for p in perms)
    BI = frozenset((0, p) for p in cyclic)
    P = frozenset(it.product(range(8), cyclic))
    require(len(group) == 48 and len(P) == 24 and len(B) == 6, "wreath orders")
    require(all(mul(mul(x, y), z) == mul(x, mul(y, z))
                for x in group for y in group for z in group), "wreath group law")
    require(generated([(1, unit), (0, cycle), (0, (1, 0, 2))], mul, identity)
            == frozenset(group), "wreath generators")
    # In rank one, M=empty uses B_b=C3; M={b} uses B=S3.
    orbits = [{p[0] for p in cyclic}, {p[0] for p in perms}]
    require(all(orbits[m] & orbits[n] == orbits[m & n] for m in range(2)
                for n in range(2)), "IPO all subset pairs")
    X, Y = left_cosets(group, P, mul), left_cosets(group, B, mul)
    incidence = [[bool(x & y) for y in Y] for x in X]
    require(len(X) == 2 and len(Y) == 8 and all(map(all, incidence)), "K2,8")
    K = P & B
    require(K == BI and len(P) // len(K) == 8 and len(B) // len(K) == 2,
            "actual two panels")
    require(len(B) // len(BI) == 2, "thin beta")
    require(any(p[0] != 0 for _, p in BI), "Borel action nontrivial")
    # Literal complement product in Proposition 4.3 would give BI alone.
    require(len(BI) != len(P), "complement formula discrepancy")
    return {"order": 48, "parabolic_orders": [24, 6], "Borel_order": 3,
            "type_sizes": [2, 8], "panel_sizes": [8, 2], "incidences": 16,
            "IPO_pairs": 4, "literal_complement_parabolic_order": 3}


def reversal_extension(n):
    rev = tuple(reversed(range(n)))
    def mul(x, y):
        return x[0] ^ (coord_action(y[0], rev) if x[1] else y[0]), x[1] ^ y[1]
    return tuple(it.product(range(1 << n), range(2))), mul


def all_digon(n):
    # Coordinate subspaces prove all subset intersection identities literally.
    supports = [frozenset(v for v in range(1 << n) if v & ~s == 0)
                for s in range(1 << n)]
    require(all(supports[s] & supports[t] == supports[s & t]
                for s in range(1 << n) for t in range(1 << n)), "full IP")
    require(all(((1 << i) ^ (1 << j)) != 0 for i in range(n)
                for j in range(i)), "distinct nontrivial products")
    # Faces: bottom=(-1,0), top=(n,0), two faces at each proper rank.
    faces = [(-1, 0)] + list(it.product(range(n), range(2))) + [(n, 0)]
    diamonds = []
    for lo in faces:
        for hi in faces:
            if hi[0] - lo[0] == 2:
                middle = [x for x in faces if lo[0] < x[0] < hi[0]]
                require(len(middle) == 2, "diamond condition")
                diamonds.append((lo, hi))
    # Every partial flag fixes some choices. Its extending flags form a cube.
    residues = 0
    for choices in it.product((-1, 0, 1), repeat=n):
        flags = {v for v in range(1 << n)
                 if all(c == -1 or ((v >> i) & 1) == c for i, c in enumerate(choices))}
        seen, pending = {min(flags)}, [min(flags)]
        while pending:
            v = pending.pop()
            for i, c in enumerate(choices):
                w = v ^ (1 << i)
                if c == -1 and w not in seen:
                    require(w in flags, "residual flag")
                    seen.add(w)
                    pending.append(w)
        require(seen == flags, "strong flag connectivity")
        residues += 1
    # The coordinate-coset objects are (rank, bit); all different ranks incident.
    parabolics = [supports[((1 << n) - 1) ^ (1 << i)] for i in range(n)]
    cosets = [left_cosets(range(1 << n), p, lambda x, y: x ^ y) for p in parabolics]
    require(all(len(c) == 2 for c in cosets), "two faces at each rank")
    require(all(x & y for i in range(n) for j in range(i)
                for x in cosets[i] for y in cosets[j]), "complete multipartite coset geometry")
    require(all(coord_action(1 << i, tuple(reversed(range(n)))) == 1 << (n - 1 - i)
                for i in range(n)), "duality reverses generators")
    return {"rank": n, "automorphism_order": 1 << n, "chambers": 1 << n,
            "proper_faces": 2 * n, "IP_pairs": 1 << (2 * n),
            "diamond_intervals": len(diamonds), "partial_flag_residues": residues}


def extension_obstructions():
    models = []
    for n in (3, 4):
        group, mul = reversal_extension(n)
        identity = (0, 0)
        require(all(mul(mul(x, y), z) == mul(x, mul(y, z))
                    for x in group for y in group for z in group), "extension associativity")
        invs = [x for x in group if x != identity and mul(x, x) == identity]
        require(all(mul(mul(x, x), mul(x, x)) == identity for x in group), "exponent divides four")
        require(any(mul(x, x) != identity for x in group), "exponent exactly four")
        require(all(mul(x, y) == mul(y, x) for x in invs for y in invs
                    if x[1] == y[1]), "involutions in each part commute")
        bad_triples = [t for t in it.combinations(invs, 3)
                       if all(mul(x, y) != mul(y, x) for x, y in it.combinations(t, 2))]
        require(not bad_triples, "no triangle of noncommuting involutions")
        models.append({"rank": n, "order": len(group), "exponent": 4,
                       "nonidentity_involutions": len(invs),
                       "triple_tests": len(list(it.combinations(invs, 3))),
                       "noncommuting_triangles": len(bad_triples)})
    gl3 = (8 - 1) * (8 - 2) * (8 - 4)
    require(gl3 == 168 and gl3 % 16 != 0, "no rank-three embedding")
    return {"models": models, "rank3_AutA_order": gl3}


def parabolic_caveats():
    xor = lambda x, y: x ^ y
    def data(P, Q):
        group = tuple(range(8))
        minimal = [Q, P]
        supers = [generated([x for i in range(2) if s & (1 << i) for x in minimal[i]],
                            xor, 0) for s in range(4)]
        e_holds = all(supers[s] & supers[t] == supers[s & t] for s in range(4)
                      for t in range(4))
        X, Y = left_cosets(group, P, xor), left_cosets(group, Q, xor)
        return {"Borel": sorted(P & Q), "generated_minimals": sorted(supers[3]),
                "condition_e": e_holds, "RC_rank2": len(supers[3]) == 8,
                "type_sizes": [len(X), len(Y)],
                "incidences": sum(bool(x & y) for x in X for y in Y),
                "generated_empty": sorted(supers[0])}
    connected = data(frozenset((0, 2, 4, 6)), frozenset((0, 1, 4, 5)))
    disconnected = data(frozenset((0, 1)), frozenset((0, 2)))
    require(connected["RC_rank2"] and not connected["condition_e"] and
            connected["Borel"] == [0, 4], "nontrivial Borel counterexample")
    require(disconnected["condition_e"] and not disconnected["RC_rank2"] and
            disconnected["Borel"] == [0], "missing generation counterexample")
    return {"connected_K2_2": connected, "disconnected_two_K2_2": disconnected}


def outer_action():
    # A=D16, elements r^i s^epsilon; all automorphisms use r->r^a,s->r^b s.
    A = tuple(it.product(range(8), range(2)))
    def mul(x, y):
        return (x[0] + (-1 if x[1] else 1) * y[0]) % 8, x[1] ^ y[1]
    autos = tuple(it.product((1, 3, 5, 7), range(8)))
    def action(f, x):
        return (f[0] * x[0] + f[1] * x[1]) % 8, x[1]
    def compose(f, g):
        return f[0] * g[0] % 8, (f[1] + f[0] * g[1]) % 8
    require(all(action(f, mul(x, y)) == mul(action(f, x), action(f, y))
                for f in autos for x in A for y in A), "automorphisms preserve product")
    require(all(len({action(f, x) for x in A}) == 16 for f in autos), "automorphisms bijective")
    # Completeness: r must map to an order-eight element r^a; s to outside that cyclic group.
    require(all((a & 1) == 1 for a, _ in autos) and len(autos) == 32, "all automorphism parameters")
    inner = frozenset(it.product((1, 7), (0, 2, 4, 6)))
    require(generated([(7, 0), (1, 2)], compose, (1, 0)) == inner, "inner automorphism group")
    quotient = left_cosets(autos, inner, compose)
    require(len(quotient) == 4 and all(compose(f, f) in inner for f in autos), "Out is V4")
    X = next(c for c in quotient if (1, 1) in c)
    Y = next(c for c in quotient if (3, 0) in c)
    lifts_x = [f for f in X if compose(f, f) == (1, 0)]
    lifts_y = [f for f in Y if compose(f, f) == (1, 0)]
    sections = [(f, g) for f in lifts_x for g in lifts_y if compose(f, g) == compose(g, f)]
    require(len(lifts_x) == 4 and len(lifts_y) == 6 and not sections, "no lift of Out quotient")
    return {"A_order": 16, "Aut_order": 32, "Inn_order": 8, "Out_order": 4,
            "involutory_lifts_of_X": len(lifts_x), "involutory_lifts_of_Y": len(lifts_y),
            "commuting_lift_pairs": len(sections)}


def run():
    return {"status": "PASS", "wreath": wreath_three(),
            "all_digon": [all_digon(3), all_digon(4)],
            "extensions": extension_obstructions(), "lemma_2_4": parabolic_caveats(),
            "outer_action": outer_action(),
            "scope": "Finite literal models support the separately written uniform arguments; no source-wide acceptance."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = run()
    data = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        require(not args.out.exists(), "output already exists")
        args.out.write_text(data)
    else:
        print(data, end="")
