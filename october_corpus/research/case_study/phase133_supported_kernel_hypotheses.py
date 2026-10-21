#!/usr/bin/env python3
"""Independent finite checks of the supported-kernel hypotheses, not a proof."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def subsets(values):
    values = list(values)
    return [frozenset(x) for n in range(len(values) + 1)
            for x in itertools.combinations(values, n)]


def span(vectors, dimension):
    result = {tuple([0] * dimension)}
    for vector in vectors:
        result |= {tuple(a ^ b for a, b in zip(x, vector)) for x in result}
    return result


def inspect(name, markers, scopes, base_nontrivial, expected_missing):
    """All local groups are C2; the base is C2 or the trivial group.

    All quotient and deletion maps are zero. Thus nontrivial local kernels
    and the distinction between local and global generation are explicit.
    """
    marker_ids = range(len(markers))
    supports = [frozenset(s) for s in scopes]
    jcount = len(supports)
    domain = {0, 1} if base_nontrivial else {0}
    all_sets = subsets(marker_ids)
    parabolics = {s: span([markers[i] for i in s], jcount + 1) for s in all_sets}
    base = {s: {v[0] for v in parabolics[s]} for s in all_sets}
    local = lambda j, s: {v[0] for v in span([(markers[i][j + 1],) for i in s], 1)}
    hypotheses = {
        "distinct_supports": len(set(supports)) == jcount,
        "outside_markers_trivial": all(markers[i][j + 1] == 0
            for j, s in enumerate(supports) for i in marker_ids if i not in s),
        "compatible_markers": True,  # both homomorphisms are zero
        "base_fixed_on_support": all(markers[i][0] == 0
            for s in supports for i in s),
        "local_generation": all(local(j, s) == {0, 1}
            for j, s in enumerate(supports)),
        "proper_parabolic_injectivity": all(local(j, t) == {0}
            for j, s in enumerate(supports) for t in subsets(s) if t < s),
        "base_generation": base[frozenset(marker_ids)] == domain,
        "base_intersection_property": all(base[s] & base[t] == base[s & t]
            for s in all_sets for t in all_sets),
    }
    missing = {key for key, value in hypotheses.items() if not value}
    require(missing == set(expected_missing), (name, missing, expected_missing))
    fiber = {tuple([b]) + x for b in domain for x in itertools.product((0, 1), repeat=jcount)}
    generated = parabolics[frozenset(marker_ids)]
    profile = all(
        ((tuple([0]) + y) in parabolics[s]) ==
        all(y[j] == 0 for j in range(jcount) if not supports[j] <= s)
        for s in all_sets for y in itertools.product((0, 1), repeat=jcount))
    ip = all(parabolics[s] & parabolics[t] == parabolics[s & t]
             for s in all_sets for t in all_sets)
    conclusions = {"full_fiber_generation": generated == fiber,
                   "all_kernel_profiles": profile, "full_intersection_property": ip}
    if expected_missing:
        require(not all(conclusions.values()), (name, "no conclusion failure"))
    else:
        require(all(conclusions.values()), (name, "positive example failed"))
    return {"name": name, "markers": markers, "supports": scopes,
            "base_order": len(domain), "local_orders": [2] * jcount,
            "hypotheses": hypotheses, "missing_hypotheses": sorted(missing),
            "conclusions": conclusions, "generated_order": len(generated),
            "full_fiber_order": len(fiber)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and not args.output.is_symlink(), "Fresh output required")
    cases = [
        inspect("independent_singleton_supports", [(0, 1, 0), (0, 0, 1)],
                [[0], [1]], False, []),
        inspect("duplicate_supports_give_diagonal", [(0, 1, 1)],
                [[0], [0]], False, ["distinct_supports"]),
        inspect("proper_local_kernel_blocks_isolation", [(0, 1, 1), (0, 0, 0)],
                [[0, 1], [0]], False, ["proper_parabolic_injectivity"]),
        inspect("base_not_fixed_gives_diagonal", [(1, 1)],
                [[0]], True, ["base_fixed_on_support"]),
        inspect("outside_markers_give_diagonal", [(0, 1, 1), (0, 1, 1)],
                [[0], [1]], False, ["outside_markers_trivial"]),
        inspect("base_IP_cannot_be_omitted", [(1,), (1,)],
                [], True, ["base_intersection_property"]),
        inspect("local_generation_cannot_be_omitted", [(0, 0)],
                [[0]], False, ["local_generation"]),
    ]
    result = {"status": "PASS", "cases": cases, "positive_examples": 1,
              "single_hypothesis_counterexamples": 6,
              "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "Independent finite hypothesis diagnostics, not a proof of the general theorem or a test of arbitrary nonabelian kernels."}
    with args.output.open("x") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "cases": len(cases), "output": str(args.output)}))


if __name__ == "__main__":
    main()
