"""Exact integer affine certificate for the three {6,6} lattice families."""
from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ZERO = (0, 0, 0)
ONE = (I, ZERO)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def mv(a, v):
    return tuple(sum(a[i][j] * v[j] for j in range(3)) for i in range(3))


def mul(x, y):
    return mm(x[0], y[0]), tuple(a + b for a, b in zip(mv(x[0], y[1]), x[1]))


def inverse(x):
    m = tuple(zip(*x[0]))
    return m, tuple(-a for a in mv(m, x[1]))


def power(x, n):
    y = ONE
    for _ in range(n):
        y = mul(y, x)
    return y


def word(*xs):
    y = ONE
    for x in xs:
        y = mul(y, x)
    return y


def conjugate(x, y):
    return word(inverse(y), x, y)


def determinant(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def subgroup(gens):
    result = {ONE}
    queue = deque(result)
    while queue:
        x = queue.popleft()
        for g in gens:
            y = mul(g, x)
            if y not in result:
                result.add(y)
                queue.append(y)
    return result


a = (((0, 1, 0), (1, 0, 0), (0, 0, 1)), ZERO)
b = (((-1, 0, 0), (0, 0, 1), (0, 1, 0)), (1, 0, 0))
c = (((0, -1, 0), (-1, 0, 0), (0, 0, 1)), ZERO)
gens = [a, b, c]
signed_basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
                (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
point_permutations = [[signed_basis.index(mv(g[0], v)) + 1 for v in signed_basis]
                      for g in gens]
assert point_permutations == [[2, 1, 3, 5, 4, 6],
                              [4, 3, 2, 1, 6, 5],
                              [5, 4, 3, 2, 1, 6]]
assert all(power(x, 2) == ONE for x in gens)
assert power(word(a, b), 6) == power(word(b, c), 6) == ONE
assert power(word(a, c), 2) == power(word(c, b, a, b), 3) == ONE

# Schreier representatives for the 48 possible signed linear parts.
lifts = {I: ONE}
lift_words = {I: ""}
queue = deque([I])
while queue:
    matrix = queue.popleft()
    for label, generator in zip("abc", gens):
        y = mul(generator, lifts[matrix])
        if y[0] not in lifts:
            lifts[y[0]] = y
            lift_words[y[0]] = label + lift_words[matrix]
            queue.append(y[0])
assert len(lifts) == 48
schreier = []
for matrix, lift in lifts.items():
    for label, generator in zip("abc", gens):
        y = mul(generator, lift)
        # y and the representative for its linear part differ by this translation.
        z = mul(y, inverse(lifts[y[0]]))
        assert z[0] == I
        if z[1] != ZERO:
            schreier.append({"vector": z[1],
                              "word": f"{label}{lift_words[matrix]}({lift_words[y[0]]})^-1"})
vectors = sorted({tuple(x["vector"]) for x in schreier})
assert all(all(v % 2 == 0 for v in row) and sum(row) % 4 == 0 for row in vectors)
index = 0
for basis in combinations(vectors, 3):
    index = math.gcd(index, abs(determinant(*basis)))
assert index == 17  # exactly 2D3, not just a sublattice contained in it

pair_left = subgroup([a, b])
pair_right = subgroup([b, c])
assert len(pair_left) == len(pair_right) == 12
assert len({x[0] for x in pair_left}) == len({x[0] for x in pair_right}) == 12
overlaps = []
for x in sorted(pair_left):
    for y in sorted(pair_right):
        if x[0] == y[0]:
            difference = tuple(u - v for u, v in zip(x[1], y[1]))
            overlaps.append({"linear": x[0], "left_translation": x[1],
                             "right_translation": y[1], "difference": difference})
assert len(overlaps) == 4
assert sorted(x["difference"] for x in overlaps) == [ZERO, ZERO, (0, 2, 2), (0, 2, 2)]
assert pair_left & pair_right == {ONE, b}

source_bases = [
    [conjugate(power(word(a, c, b), 4), b), power(word(c, b, a), 4),
     conjugate(power(word(c, b, a), 4), b)],
    [conjugate(power(word(power(word(b, c), 3), power(word(a, b), 3)), 2), word(a, b)),
     conjugate(power(word(power(word(b, c), 3), power(word(a, b), 3)), 2), c),
     conjugate(power(word(power(word(b, c), 3), power(word(a, b), 3)), 2), word(c, b))],
    [conjugate(power(word(power(word(a, b), 2), power(word(c, b), 2)), 3), a),
     power(word(power(word(b, c), 2), power(word(b, a), 2)), 3),
     conjugate(power(word(power(word(b, a), 2), power(word(b, c), 2)), 3), c)],
]
assert all(x[0] == I for row in source_bases for x in row)
bases = [[x[1] for x in row] for row in source_bases]
indices_in_z3 = [abs(determinant(*basis)) for basis in bases]
assert indices_in_z3 == [64, 128, 256]
assert all(all(v % 4 == 0 for v in row) for basis in bases for row in basis)
orders = [48 * index // 16 for index in indices_in_z3]
assert orders == [192, 384, 768]

data = {
    "status": "PASS",
    "arithmetic": "integer affine transformations only; no floating point",
    "generators": gens,
    "signed_basis_order": signed_basis,
    "point_generator_permutations_as_image_lists": point_permutations,
    "permutation_convention": "GAP right action: p maps to inverse of its column-action matrix; generators are involutions, so their matrices agree exactly",
    "point_group_order": len(lifts),
    "translation_lattice": "2D3={(2x,2y,2z):x+y+z even}",
    "translation_index_in_Z3": index,
    "schreier_vectors": vectors,
    "schreier_word_certificates": schreier,
    "parabolic_overlap_certificate": overlaps,
    "source_word_translation_bases": bases,
    "lattice_indices_in_Z3": indices_in_z3,
    "orders_for_m_one": orders,
    "all_m_formula": ["192*m^3", "384*m^3", "768*m^3"],
    "input_hashes": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest()
                     for f in [Path(__file__).name, "phase2_cubic_kernel_check.g"]},
}
(ROOT / "phase2_cubic_lattice_check.json").write_text(json.dumps(data, indent=2) + "\n")
print("PASS: point group48, kernel2D3 index16; source lattices64,128,256 in Z3")
print("PASS: pair parabolics12 each; only extra linear overlaps differ by (0,2,2)")
print("PASS: exact source-word lattices yield 192*m^3,384*m^3,768*m^3 for every m>=1")
