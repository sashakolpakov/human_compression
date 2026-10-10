#!/usr/bin/env python3
"""Exhaust all binary rank-two kernel quotients for d=3,4,5.

Enumerates surjective parameter labels modulo GL(2,2), independently of
the admissible A/B description. The exact subspace-intersection criterion
is compared with that description. No group catalogue is used.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def span(vectors):
    values = {0}
    for x in vectors:
        values |= {y ^ x for y in values}
    return values


def canonical(labels):
    nonzero = next((x for x in labels if x), None)
    second = next((x for x in labels if x not in (0, 1)), None)
    return nonzero == 1 and second == 2


def count_rank(d):
    supports = [(1 << i) | (1 << (i + 1)) for i in range(d - 1)]
    supports += [7 << i for i in range(d - 2)]
    vectors = passed = intersections = 0
    first_failure = None
    for labels in itertools.product(range(4), repeat=2 * d - 3):
        if not canonical(labels):
            continue
        assert span(labels) == {0, 1, 2, 3}
        vectors += 1
        alpha, beta = labels[:d - 1], labels[d - 1:]
        intrinsic = sum(b not in span(alpha[i:i + 2]) for i, b in enumerate(beta))
        cost = sum(bool(a) for a in alpha) + intrinsic
        parabolics = [sum(1 << v for v in span(label for label, support in zip(labels, supports)
                                              if mask & support == support))
                      for mask in range(1 << d)]
        ok = True
        for s, t in itertools.product(range(1 << d), repeat=2):
            meets = parabolics[s] & parabolics[t]
            intersections += 1
            if meets != parabolics[s & t]:
                ok = False
                if first_failure is None:
                    first_failure = {"alpha": alpha, "beta": beta,
                                     "sets_bitmasks": [s, t],
                                     "kernel_intersection_bitset": meets,
                                     "intersection_kernel_bitset": parabolics[s & t]}
        assert ok == (cost == 2)
        passed += ok
    assert vectors == ((2 ** (2 * d - 3) - 1) * (2 ** (2 * d - 3) - 2)) // 6
    assert passed == (25 * d * d - 125 * d + 162) // 2
    return {"rank": d, "canonical_rank_two_quotients": vectors,
            "IP_kernel_systems": passed, "non_IP_kernel_systems": vectors - passed,
            "exact_subspace_intersections": intersections,
            "first_failure": first_failure}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = [count_rank(d) for d in (3, 4, 5)]
    report = {"status": "PASS", "scope": "Finite rank-two linear quotient diagnostics, not the uniform proof",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "cases": results,
              "total_canonical_quotients": sum(x["canonical_rank_two_quotients"] for x in results),
              "total_exact_subspace_intersections": sum(x["exact_subspace_intersections"] for x in results)}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
