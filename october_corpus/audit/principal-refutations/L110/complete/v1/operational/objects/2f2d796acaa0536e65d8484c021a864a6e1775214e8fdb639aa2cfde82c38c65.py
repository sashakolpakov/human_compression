"""Exact extra seed and overlapping-prime checks for L110 Constructions 8/9."""
from pathlib import Path
from collections import Counter
from itertools import product
from math import gcd, prod
import hashlib
import json
import time

from phase5_suzuki_check import Field, ID, W
from phase6_suzuki_torus_check import generated, mat_pow
from phase7_suzuki_seed_check import rho_matrix, tau


def companion(d):
    return 2*((1 << d)+1)-tau(d)


def run_example(label, torus_order, e, primes, selected, complement):
    n = e*prod(primes)
    gamma = torus_order(e)
    m = gamma*prod(selected)
    assert torus_order(n) % m == 0
    assert len(set(selected)) == len(selected)
    for a, ell in zip(primes, selected):
        assert torus_order(e*a) % (gamma*ell) == 0
    rows = []
    for mask in range(1 << len(primes)):
        d, mJ = n, m
        removed = []
        for i, (a, ell) in enumerate(zip(primes, selected)):
            if mask >> i & 1:
                d //= a
                mJ //= ell
                removed.append(a)
        assert gcd(m, torus_order(d)) == mJ
        rows.append({"removed_field_primes": removed, "field_degree": d,
                     "cyclic_intersection_order": mJ,
                     "cyclic_by_complement_order": complement*mJ})
    # This map is on the cyclic subgroup A. Unlike K/H_i, these A/A_i
    # are genuine quotient groups, with residues modulo distinct primes.
    fibers = Counter(tuple(x % ell for ell in selected) for x in range(m))
    assert set(fibers) == set(product(*(range(ell) for ell in selected)))
    assert set(fibers.values()) == {gamma}
    return {"family": label, "base_degree": e, "ambient_degree": n,
            "base_torus_order": gamma, "relative_primes": primes,
            "selected_primes": selected, "selected_base_overlaps":
            [ell for ell in selected if gamma % ell == 0],
            "cyclic_subgroup_order": m, "complement_order": complement,
            "intersections": rows, "coordinate_tuples": len(fibers),
            "each_coordinate_fiber_size": gamma}


def main():
    started = time.monotonic()
    here = Path(__file__).parent
    old = json.loads((here/"phase6_suzuki_torus_check.json").read_text())
    F = Field(3, 11)
    r = tuple(old["F2_order4_normalizer"])
    c = F.mm(mat_pow(F, r, 2), W)
    assert c != ID and mat_pow(F, c, 5) == ID
    assert all(pow(2, i, 5) != 1 for i in [1, 2, 3])
    assert pow(2, 4, 5) == 1
    assert rho_matrix(F, c) == c
    S2 = generated(F, [r, W], 20)
    centralizer = {g for g in S2 if F.mm(g, c) == F.mm(c, g)}
    assert centralizer == generated(F, [c], 5)
    conjugate = F.mm(F.mm(mat_pow(F, r, 3), c), r)
    power = next(i for i in range(1, 5) if mat_pow(F, c, i) == conjugate)
    assert power in [2, 3]
    examples = [
        run_example("Construction8 split", lambda d: (1 << d)-1,
                    3, [7, 3], [7, 73], 2),
        run_example("Construction9 tau branch", tau,
                    3, [13, 3], [13, 37], 4),
        run_example("Construction9 companion branch", companion,
                    3, [5, 3], [5, 109], 4),
    ]
    result = {
        "status": "PASS",
        "scope": "Exact second binary torus seed plus all-subset integer intersections and exhaustive cyclic coordinate maps in three examples with a selected prime dividing the base torus order.",
        "second_torus_seed": {"order5_matrix": list(c),
                              "rho_fixes_matrix": True,
                              "binary_Sz2_centralizer_order": len(centralizer),
                              "order4_complement_conjugation_power": power,
                              "character_trace_selected": -2,
                              "character_determinant": 2},
        "overlapping_prime_examples": examples,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_hashes": {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                         for name in ["phase5_suzuki_check.py",
                                      "phase5_suzuki_higher_check.py",
                                      "phase6_suzuki_torus_check.py",
                                      "phase6_suzuki_torus_check.json",
                                      "phase7_suzuki_seed_check.py"]},
        "elapsed_seconds": round(time.monotonic()-started, 3),
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
