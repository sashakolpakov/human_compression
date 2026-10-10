#!/usr/bin/env python3
"""Enumerate all small universal central-kernel quotients independently.

For each subspace N of the edge/triple coordinate space, directly test
(N+W_S) intersect (N+W_T) = N+W_(S intersect T).  Candidate subspaces
are not selected using the proposed alpha/beta classification.
This is a vector-space diagnostic, not a group enumeration.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def all_subspaces(dimension):
    """Unique binary RREF bases, with the lowest set bit as pivot."""
    for rank in range(dimension + 1):
        for pivots in itertools.combinations(range(dimension), rank):
            pivot_set = set(pivots)
            free = [(i, j) for i, p in enumerate(pivots)
                    for j in range(p + 1, dimension) if j not in pivot_set]
            for choice in range(1 << len(free)):
                rows = [1 << p for p in pivots]
                for bit, (i, j) in enumerate(free):
                    if choice >> bit & 1:
                        rows[i] |= 1 << j
                vectors = [0]
                for row in rows:
                    vectors += [v ^ row for v in vectors]
                yield rank, sum(1 << v for v in vectors)


def predicted_polynomial(rank):
    """Direct formula in the proposed theorem, for comparison only."""
    result = [0] * (2 * rank - 2)
    for bits in range(1 << (rank - 1)):
        poly = [1]
        for i in range(rank - 2):
            coefficient = 1 << (((bits >> i) & 1) + ((bits >> (i + 1)) & 1))
            new = [0] * (len(poly) + 1)
            for j, c in enumerate(poly):
                new[j] += coefficient * c
                new[j + 1] += c
            poly = new
        for j, c in enumerate(poly):
            result[j + bits.bit_count()] += c
    return result


def run(rank):
    supports = [3 << i for i in range(rank - 1)]
    supports += [7 << i for i in range(rank - 2)]
    dimension = len(supports)
    masks = [sum(1 << j for j, t in enumerate(supports) if t & s == t)
             for s in range(1 << rank)]
    low_masks = [sum(1 << v for v in range(1 << dimension) if not (v >> j & 1))
                 for j in range(dimension)]
    full = (1 << (1 << dimension)) - 1
    high_masks = [full ^ lo for lo in low_masks]
    pairs = [(a, b, a & b) for a in range(1 << rank)
             for b in range(a, 1 << rank)]
    counts = [0] * (dimension + 1)
    subspaces = 0
    tested_meets = 0
    for subspace_rank, n in all_subspaces(dimension):
        subspaces += 1
        cache = {0: n}

        def adjoining(mask):
            if mask not in cache:
                bit = mask & -mask
                j = bit.bit_length() - 1
                value = adjoining(mask ^ bit)
                shift = 1 << j
                translated = ((value & low_masks[j]) << shift) | ((value & high_masks[j]) >> shift)
                cache[mask] = value | translated
            return cache[mask]

        preimages = [adjoining(mask) for mask in masks]
        valid = True
        for a, b, intersection in pairs:
            tested_meets += 1
            if preimages[a] & preimages[b] != preimages[intersection]:
                valid = False
                break
        if valid:
            counts[dimension - subspace_rank] += 1
    expected = predicted_polynomial(rank)
    assert counts == expected, (rank, counts, expected)
    assert counts[1] == 5 * rank - 10
    assert counts[2] == (25 * rank * rank - 125 * rank + 162) // 2
    return {"rank": rank, "universal_kernel_dimension": dimension,
            "all_subspaces_enumerated": subspaces,
            "intersection_tests_until_rejection": tested_meets,
            "valid_quotients_by_excess": counts,
            "formula_coefficients": expected, "status": "PASS"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = [run(rank) for rank in (3, 4, 5)]
    assert [r["all_subspaces_enumerated"] for r in results] == [16, 374, 29212]
    report = {"status": "PASS", "date": "2026-10-10",
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "All binary RREF subspaces; direct coordinate-preimage intersection tests; no candidate-classification filter.",
              "scope": "Independent finite vector-space diagnostic for the universal central-cover model; not group enumeration or a proof for arbitrary rank.",
              "cases": results}
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
