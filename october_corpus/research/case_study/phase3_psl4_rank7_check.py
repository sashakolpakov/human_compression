"""Finite F2 support audit and integral identities for the rank-seven proof.

The exhaustive check covers the combinatorial support-forcing step only.
It does not replace the paper proof or formalize representation theory.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sympy as s


def span(vectors):
    result = {0}
    for v in vectors:
        result |= {w ^ v for w in tuple(result)}
    return result


def form(bits):
    matrix = [[0] * 4 for _ in range(4)]
    for value, (i, j) in zip(bits, combinations(range(4), 2)):
        matrix[i][j] = matrix[j][i] = value
    return lambda x, y: sum(
        ((x >> i) & 1) * matrix[i][j] * ((y >> j) & 1)
        for i in range(4) for j in range(4)
    ) % 2


def full_affine_supports(plane):
    cosets = {frozenset(x ^ w for w in plane) for x in range(16)}
    supports = []
    for coset in cosets:
        for size in [3, 4]:
            for values in combinations(sorted(coset), size):
                assert span([v ^ values[0] for v in values]) == plane
                supports.append(values)
    return supports


left, right = span([1, 2]), span([4, 8])
forms = pairs = compatible = compatible_forms = 0
for bits in product([0, 1], repeat=6):
    omega = form(bits)
    if any(all(omega(x, y) == 0 for y in range(16)) for x in range(1, 16)):
        continue
    forms += 1
    W1 = {x for x in range(16) if all(omega(x, y) == 0 for y in right)}
    W5 = {x for x in range(16) if all(omega(x, y) == 0 for y in left)}
    assert W1 & W5 == {0}
    hits = 0
    for S1, S5 in product(full_affine_supports(W1), full_affine_supports(W5)):
        pairs += 1
        assert len({a ^ b for a in S1 for b in S5}) == len(S1) * len(S5)
        values = {omega(a, b) for a in S1 for b in S5}
        if len(values) != 1:
            continue
        compatible += 1
        hits += 1
        assert W1 == left and W5 == right
        assert set(S1) <= left and set(S5) <= right
        assert values == {0}
        assert omega(1, 2) == omega(4, 8) == 1
        assert all(omega(a, b) == 0 for a in left for b in right)
    compatible_forms += bool(hits)

assert (forms, pairs, compatible, compatible_forms) == (28, 11200, 25, 1)

# The exact identities used for the final tensor-form step.
a, b, c, x, y, z, t = s.symbols("a b c x y z t")
L = s.Matrix([[a, b], [c, -a]])
Z = s.diag(1, -1)
K = s.Matrix([[0, b], [-c, 0]])
assert K*Z + Z*K == s.zeros(2)
assert s.simplify(K*L + L*K) == s.zeros(2)
M = s.Matrix([[x, y], [z, t]])
J = s.Matrix([[0, 1], [-1, 0]])
assert s.simplify(M.T*J*M - M.det()*J) == s.zeros(2)

root = Path(__file__).resolve().parent
names = ["phase3_psl4_rank7.md", "phase3_psl4_rank7_check.py"]
report = {
    "status": "passed",
    "nondegenerate_F2_commutator_forms": forms,
    "full_affine_support_pairs": pairs,
    "compatible_pairs": compatible,
    "compatible_commutator_forms": compatible_forms,
    "forced_form": "omega(v0,v2)=omega(v4,v6)=1; all cross pairings zero",
    "integral_symbolic_matrix_identities": 3,
    "scope": "Finite exhaustive audit of the Pauli-support combinatorics and three integral matrix identities. It does not formalize the entire rank-seven theorem or establish publication priority.",
    "artifacts": [{"path": name, "sha256": hashlib.sha256((root/name).read_bytes()).hexdigest()}
                  for name in names],
}
(root / "phase3_psl4_rank7_check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
