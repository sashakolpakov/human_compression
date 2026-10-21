#!/usr/bin/env python3
"""Independent exact affine-array check of the L003 s=6 presentation.

No finder, GAP, SymPy, or author's checker is imported. Arrays encode right
actions (i,n)->(p[i],n+v[i]); composition is calculated on all states at once.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check(path):
    data = json.loads(Path(path).read_text())
    n = data["degree"]
    assert n == 216
    ident = (tuple(range(n)), (0,) * n)
    gens = []
    for perm, voltage in zip(data["permutations"], data["weights"], strict=True):
        assert sorted(perm) == list(range(1, n + 1))
        assert len(voltage) == n and all(type(x) is int for x in voltage)
        gens.append((tuple(x - 1 for x in perm), tuple(voltage)))
    assert len(gens) == 3

    def mul(a, b):
        p, v = a
        q, w = b
        return tuple(q[p[i]] for i in range(n)), tuple(v[i] + w[p[i]] for i in range(n))

    def inv(a):
        p, v = a
        back = [0] * n
        for i, j in enumerate(p):
            back[j] = i
        return tuple(back), tuple(-v[back[i]] for i in range(n))

    def power(a, k):
        if k < 0:
            return power(inv(a), -k)
        out = ident
        for _ in range(k):
            out = mul(out, a)
        return out

    def product(*args):
        out = ident
        for a in args:
            out = mul(out, a)
        return out

    for a in gens:
        assert mul(a, inv(a)) == ident == mul(inv(a), a)
    x, y, z = gens
    parameter = product(y, power(product(z, y), 2))
    # Direct substitution into the primary manuscript p.17, with
    # (a,b,c,d,e,f,g,h)=(3,0,2,0,1,1,6,0).
    relators = [
        power(x, 6), power(y, 3), power(z, 2),
        power(product(z, x), 3), power(product(z, y), 6),
        power(product(inv(x), y), 2),
        power(product(inv(y), power(x, -2)), 3),
        power(product(z, power(x, 3)), 2),
        product(inv(x), z, power(product(inv(y), z), 2),
                z, x, power(product(z, y), 2)),
        power(parameter, 6),
    ]
    assert all(r == ident for r in relators)
    witness = power(product(x, y, x, z), 2)
    assert witness[0] == ident[0]
    assert witness[1][0] == -1
    assert power(parameter, 6) == ident
    assert all(power(parameter, k) != ident for k in (1, 2, 3))
    # Independent check that the finite permutation image is regular of order216.
    seen, queue = {ident[0]}, [ident[0]]
    for p in queue:
        for q, _ in gens:
            pq = tuple(q[p[i]] for i in range(n))
            if pq not in seen:
                seen.add(pq)
                queue.append(pq)
    assert len(seen) == n and len({p[0] for p in seen}) == n
    return {
        "status": "PASS", "certificate_sha256": digest(path),
        "checker_sha256": digest(__file__), "degree": n,
        "relators": len(relators), "relator_state_checks": len(relators) * n,
        "finite_permutation_image_order": len(seen),
        "finite_permutation_action_regular": True,
        "witness": "(x*y*x*z)^2", "witness_permutation_identity": True,
        "witness_translation_at_state_1": witness[1][0],
        "witness_translation_histogram": dict(sorted(Counter(witness[1]).items())),
        "parameter_word_exact_order": 6,
        "uniform_conclusion": "The displayed source presentation is infinite for every positive parameter divisible by six.",
        "scope": "An infinite image; no subgroup-rewriting assumption, finite-quotient exclusion, or hypertope intersection-property conclusion.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = check(args.data)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
