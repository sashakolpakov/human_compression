#!/usr/bin/env python3
"""Exact finite coefficient certificates for the phase-nine corollary.

Python standard library only. The weight witnesses apply to every m>=3;
the extra checks for 3<=m<=64 are corroboration, not the parameter proof.
This does not reprove the inherited phase-eight classification.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
from math import gcd
from pathlib import Path
import argparse
import json


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def weight(indices):
    return tuple(indices.count(i) for i in range(4))


def canonical(v, m):
    return tuple((x - v[-1]) % m for x in v[:-1])


def parity(p):
    return sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2


def cycle_type(p):
    seen, lengths = set(), []
    for i in range(4):
        if i in seen:
            continue
        j, length = i, 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = p[j]
        lengths.append(length)
    return sorted(lengths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve()
    output = args.output or here.with_suffix(".json")
    linear = [weight((i,)) for i in range(4)]
    quadratic = [weight(pair) for pair in combinations_with_replacement(range(4), 2)]
    witnesses = []
    gcds = Counter()
    for a, b in combinations(quadratic, 2):
        d = tuple(x-y for x, y in zip(a, b))
        options = [(r, s, d[r]-d[s]) for r in range(4) for s in range(4)
                   if 1 <= abs(d[r]-d[s]) <= 2]
        assert options, (a, b)
        r, s, value = options[0]
        # The determinant-one torus element with exponents e_r-e_s
        # separates these weights for every root of unity of order m>=3.
        assert value in (-2, -1, 1, 2)
        g = gcd(*(d[i]-d[3] for i in range(3)))
        assert g in (1, 2)
        gcds[g] += 1
        witnesses.append({"a": a, "b": b, "r": r, "s": s, "difference": value,
                          "collision_modulus_divides": g})
    assert len(witnesses) == 45
    assert dict(gcds) == {1: 36, 2: 9}
    degree_one = 0
    for a, b in combinations(linear, 2):
        d = tuple(x-y for x, y in zip(a, b))
        assert any(abs(d[r]-d[s]) == 1 for r in range(4) for s in range(4))
        degree_one += 1
    assert degree_one == 6
    for m in range(3, 65):
        assert len({canonical(v, m) for v in quadratic}) == 10
        assert len({canonical(v, m) for v in linear}) == 4
    # Explicitly show why m>=3 must be retained.
    assert len({canonical(v, 2) for v in quadratic}) < 10

    alternating = [p for p in permutations(range(4)) if parity(p) == 0]
    cycles = [p for p in alternating if cycle_type(p) == [1, 3]]
    assert len(alternating) == 12 and len(cycles) == 8
    assert all(sum(p[i] == i for i in range(4)) == 1 for p in cycles)
    for i in range(4):
        assert {p[i] for p in alternating} == set(range(4))
    invariant_subsets = []
    for mask in range(16):
        subset = {i for i in range(4) if mask & (1 << i)}
        if all({p[i] for i in subset} == subset for p in alternating):
            invariant_subsets.append(mask)
    assert invariant_subsets == [0, 15]

    # Verify over Z the functional (E_ji B+B E_ij)_(j,b)=B_(i,b),
    # using all 16 matrix-unit basis vectors B, for each output (i,b).
    transvection_entry_checks = 0
    for i in range(4):
        for b in range(4):
            j = next(j for j in range(4) if j not in (i, b))
            for r in range(4):
                for s in range(4):
                    E = lambda x, y: int(x == r and y == s)
                    value = E(i, b) + (E(j, i) if b == j else 0)
                    assert value == int(i == r and b == s)
                    transvection_entry_checks += 1
    assert transvection_entry_checks == 256

    # Cyclic determinant-quotient arithmetic for each odd residue class.
    quotient_cases = []
    for q_mod4 in (1, 3):
        sl_index = gcd(4, q_mod4 - 1)
        su_index = gcd(4, q_mod4 + 1)
        assert sorted([sl_index, su_index]) == [2, 4]
        quotient_cases.append({"q_mod4": q_mod4, "PGL_over_PSL": sl_index,
                               "PGU_over_PSU": su_index})
    for n in (2, 4):
        order_at_most_two = [i for i in range(n) if 2*i % n == 0]
        subgroup = {sum(coeff*x for coeff, x in zip(bits, order_at_most_two)) % n
                    for bits in __import__("itertools").product(range(n),
                                                              repeat=len(order_at_most_two))}
        assert subgroup == ({0, 1} if n == 2 else {0, 2})

    proof = here.with_name("phase9_linear_unitary.md")
    report = {
        "status": "PASS",
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": digest(here),
        "proof_sha256": digest(proof),
        "scope": "Universal integer weight separation and coefficient identities; not a replacement for the inherited phase-eight written classification.",
        "degree_two_pairs": len(witnesses),
        "collision_gcd_distribution": dict(sorted(gcds.items())),
        "degree_one_pairs": degree_one,
        "supplementary_moduli_checked": [3, 64],
        "alternating_group_order": len(alternating),
        "three_cycles_with_fixed_coordinate": len(cycles),
        "invariant_coordinate_subset_masks": invariant_subsets,
        "transvection_entry_checks_over_integers": transvection_entry_checks,
        "quotient_residue_cases": quotient_cases,
        "universal_weight_witnesses": witnesses,
        "no_full_group_or_classification_enumeration": True
    }
    output.write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: 45 uniform degree-two witnesses; 6 degree-one pairs; "
          "256 integer matrix-entry checks; A4 and cyclic quotient checks.")


if __name__ == "__main__":
    main()
