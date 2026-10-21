"""Exact checks for the metacyclic cyclic-TPP proof's power obstruction.

No third-party modules. Run beside this file; writes its own JSON report.
The finite ranges check the modular arithmetic, not the universal theorem.
"""
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import time


def power_sum(base, length, modulus):
    """Return (base**length, sum(base**j for j<length)), modulo modulus."""
    if length == 0:
        return 1, 0
    power, total = power_sum(base, length // 2, modulus)
    total = total * (1 + power) % modulus
    power = power * power % modulus
    if length % 2:
        total = (total + power) % modulus
        power = power * base % modulus
    return power, total


def valuation(number, prime):
    assert number != 0
    result = 0
    while number % prime == 0:
        result += 1
        number //= prime
    return result


def p_power_order(unit, prime, exponent):
    modulus = prime ** exponent
    # The principal-unit p-Sylow has order p**(exponent-1); for p=2,
    # every unit belongs to that Sylow. Test rather than assume membership.
    limit = prime ** (exponent - 1)
    if pow(unit, limit, modulus) != 1:
        return None
    order = 1
    while pow(unit, order, modulus) != 1:
        order *= prime
    return order


def main():
    started = time.perf_counter()
    rows = []
    sanity = 0
    for modulus in (8, 16, 27, 81, 125):
        for base in range(modulus):
            for length in range(17):
                assert power_sum(base, length, modulus) == (
                    pow(base, length, modulus),
                    sum(pow(base, j, modulus) for j in range(length)) % modulus,
                )
                sanity += 1
    for prime, max_m in ((2, 11), (3, 7), (5, 5)):
        for m in range(2, max_m + 1):
            modulus = prime ** m
            actions = 0
            contexts = 0
            for unit in range(1, modulus):
                if gcd(unit, modulus) != 1:
                    continue
                order = p_power_order(unit, prime, m)
                if order is None or order == 1:
                    continue
                n = valuation(order, prime)
                assert order == prime ** n and n <= m - 1
                actions += 1
                for t in range(order):
                    if prime == 2 and t % 2:
                        continue
                    image_order = order // gcd(order, t)
                    k = valuation(image_order, prime)
                    rotation = pow(unit, t, modulus)
                    power, total = power_sum(rotation, image_order, modulus)
                    assert power == 1
                    assert total != 0 and valuation(total, prime) == k
                    # It suffices to inspect s=1: multiplication by a unit s
                    # is a bijection modulo p**m, so cannot turn total into0.
                    contexts += 1
            rows.append({"prime": prime, "normal_exponent": m,
                         "faithful_nontrivial_actions": actions,
                         "forbidden_generator_contexts": contexts})
    # The parity restriction really matters for 2-groups: in a dihedral
    # extension x*y has order2 and its cyclic subgroup avoids <x>.
    dihedral_controls = []
    for m in range(2, 12):
        modulus = 2 ** m
        assert power_sum(modulus - 1, 2, modulus) == (1, 0)
        dihedral_controls.append(modulus)
    source = Path(__file__)
    report = {
        "date": "2026-10-10", "status": "PASS",
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "geometric_sum_direct_sanity_checks": sanity,
        "rows": rows,
        "faithful_actions": sum(r["faithful_nontrivial_actions"] for r in rows),
        "forbidden_generator_contexts": sum(r["forbidden_generator_contexts"] for r in rows),
        "dihedral_odd_exponent_controls": dihedral_controls,
        "elapsed_seconds": time.perf_counter() - started,
        "scope": "Exact finite modular-power checks. The all-parameter metacyclic TPP theorem is proved in the companion written argument, not inferred from these ranges.",
    }
    source.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {report['faithful_actions']} faithful actions; "
          f"{report['forbidden_generator_contexts']} forbidden generator contexts; "
          f"{sanity} direct power-sum cross-checks.")


if __name__ == "__main__":
    main()
