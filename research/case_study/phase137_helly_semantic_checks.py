#!/usr/bin/env python3
"""Finite author diagnostics for the exact hypotheses of typed Helly transfer."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cosets(group, mul, subgroup):
    return list(dict.fromkeys(frozenset(mul(h, g) for h in subgroup) for g in group))


def helly_profile(group, mul, subgroups):
    families = [cosets(group, mul, p) for p in subgroups]
    total = pairwise = 0
    failures = []
    for size in range(len(subgroups) + 1):
        for indices in itertools.combinations(range(len(subgroups)), size):
            for selected in itertools.product(*(families[i] for i in indices)):
                total += 1
                if all(a & b for a, b in itertools.combinations(selected, 2)):
                    pairwise += 1
                    common = set(group)
                    for a in selected:
                        common.intersection_update(a)
                    if not common:
                        failures.append({"types": indices,
                                         "cosets": [sorted(a, key=repr) for a in selected]})
    return {"holds": not failures, "families_checked": total,
            "pairwise_families": pairwise, "failure_count": len(failures),
            "first_failure": failures[0] if failures else None}


def structural(group, mul, one, subgroups, q, base, bmul,
               coordinates, coordinate_one, free, coordinate_factors, coordinate_mul):
    require(all(mul(one, x) == x == mul(x, one) for x in group), "Identity failed")
    require(all(any(mul(x, y) == one == mul(y, x) for y in group) for x in group),
            "Inverse failed")
    subgroup_ok = all(one in p and all(mul(x, y) in p for x in p for y in p)
                      for p in subgroups)
    require(subgroup_ok, "Input subgroup failed")
    image = [{q(x) for x in p} for p in subgroups]
    kernel = [x for x in group if q(x) == q(one)]
    coordinate_product = set(itertools.product(*coordinate_factors))
    coordinate_isomorphism = (
        len(set(map(coordinates, kernel))) == len(kernel) and
        set(map(coordinates, kernel)) == coordinate_product and
        coordinates(one) == coordinate_one and
        all(coordinates(mul(x, y)) == coordinate_mul(coordinates(x), coordinates(y))
            for x in kernel for y in kernel))
    require(coordinate_isomorphism, "Explicit kernel coordinate isomorphism failed")
    profile = [all((x in p) == all(coordinates(x)[a] == coordinate_one[a]
                    for a in range(len(coordinate_one)) if a not in free[i])
                   for x in kernel) for i, p in enumerate(subgroups)]
    return {"coordinate_isomorphism": coordinate_isomorphism, "epimorphism": set(map(q, group)) == set(base) and
               all(q(mul(x, y)) == bmul(q(x), q(y)) for x in group for y in group),
            "intersection_images": all({q(x) for x in p & r} == image[i] & image[j]
                                       for i, p in enumerate(subgroups)
                                       for j, r in enumerate(subgroups)),
            "coordinate_profiles": profile,
            "kernel_order": len(kernel),
            "base_helly": helly_profile(base, bmul, image),
            "upstairs_helly": helly_profile(group, mul, subgroups)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Fresh output directory required")
    d8 = list(itertools.product(range(4), range(2)))
    s3 = list(itertools.permutations(range(3)))
    def dm(x, y):
        return ((x[0] + (-1 if x[1] else 1) * y[0]) % 4, (x[1] + y[1]) % 2)
    def sm(x, y):
        return tuple(x[y[i]] for i in range(3))
    for group, mul in [(d8, dm), (s3, sm)]:
        require(all(mul(mul(x, y), z) == mul(x, mul(y, z))
                    for x in group for y in group for z in group), "Factor associativity failed")
    require(any(dm(x, y) != dm(y, x) for x in d8 for y in d8), "D8 unexpectedly abelian")
    require(any(sm(x, y) != sm(y, x) for x in s3 for y in s3), "S3 unexpectedly abelian")
    group = list(itertools.product(d8, s3, range(2)))
    one = ((0, 0), (0, 1, 2), 0)
    def mul(x, y):
        return dm(x[0], y[0]), sm(x[1], y[1]), (x[2] + y[2]) % 2
    subgroups = [{x for x in group if x[1] == one[1]},
                 {x for x in group if x[0] == one[0]},
                 {x for x in group if x[2] == 0}]
    add2 = lambda x, y: (x + y) % 2
    positive = structural(group, mul, one, subgroups, lambda x: x[2], [0, 1], add2,
                          lambda x: x[:2], one[:2], [{0}, {1}, {0, 1}], [d8, s3],
                          lambda x, y: (dm(x[0], y[0]), sm(x[1], y[1])))
    require(positive["epimorphism"] and positive["intersection_images"] and
            all(positive["coordinate_profiles"]) and positive["base_helly"]["holds"] and
            positive["upstairs_helly"]["holds"], "Nonabelian positive case failed")
    v4 = list(itertools.product(range(2), repeat=2))
    vm = lambda x, y: ((x[0] + y[0]) % 2, (x[1] + y[1]) % 2)
    lines = [{(0, 0), (1, 0)}, {(0, 0), (1, 1)}, {(0, 0), (0, 1)}]
    bad_intersection = structural(v4, vm, (0, 0), lines, lambda x: x[0], [0, 1], add2,
                                  lambda x: (x[1],), (0,), [set(), set(), {0}], [[0, 1]],
                                  lambda x, y: (add2(x[0], y[0]),))
    require(bad_intersection["epimorphism"] and not bad_intersection["intersection_images"] and
            all(bad_intersection["coordinate_profiles"]) and
            bad_intersection["base_helly"]["holds"] and
            not bad_intersection["upstairs_helly"]["holds"], "Intersection-image control failed")
    bad_profile = structural(v4, vm, (0, 0), lines, lambda x: 0, [0], lambda x, y: 0,
                             lambda x: x, (0, 0), [{0}, set(), {1}], [[0, 1], [0, 1]], vm)
    require(bad_profile["epimorphism"] and bad_profile["intersection_images"] and
            bad_profile["coordinate_profiles"] == [True, False, True] and
            bad_profile["base_helly"]["holds"] and not bad_profile["upstairs_helly"]["holds"],
            "Coordinate-profile control failed")
    bad_base = structural(v4, vm, (0, 0), lines, lambda x: x, v4, vm,
                          lambda x: (), (), [set(), set(), set()], [], lambda x, y: ())
    require(bad_base["epimorphism"] and bad_base["intersection_images"] and
            all(bad_base["coordinate_profiles"]) and not bad_base["base_helly"]["holds"] and
            not bad_base["upstairs_helly"]["holds"], "Base-Helly control failed")
    out.mkdir(parents=True, exist_ok=False)
    report = {"status": "PASS", "positive_nonabelian_kernel": positive,
              "single_hypothesis_counterexamples": {
                  "intersection_image": bad_intersection,
                  "coordinate_profile": bad_profile,
                  "base_helly": bad_base},
              "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "author_diagnostics_not_independent_review": True,
              "universal_theorem_is_supplied_by_Lean_not_finite_enumeration": True}
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "nonabelian_positive_group_order": len(group),
                      "single_hypothesis_counterexamples": 3, "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
