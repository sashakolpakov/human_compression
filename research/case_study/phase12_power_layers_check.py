#!/usr/bin/env python3
"""Exact small linear checks for phase12_power_layers.md (stdlib only).

The uniform group argument is a written proof. This file checks the
dimension-at-most-two square-action lemma, the canonical dimension-three
actions, and an explicit failure of the weaker top-coordinate shortcut.
"""

from itertools import product
import json


def act(matrix, vector):
    result = 0
    for bit, column in enumerate(matrix):
        if vector & (1 << bit):
            result ^= column
    return result


def compose(left, right):
    return tuple(act(left, column) for column in right)


def span(vectors):
    result = {0}
    for vector in vectors:
        result |= {old ^ vector for old in tuple(result)}
    return result


def identity(dimension):
    return tuple(1 << i for i in range(dimension))


def involutions(dimension):
    unit = identity(dimension)
    return [m for m in product(range(1 << dimension), repeat=dimension)
            if compose(m, m) == unit]


def square_conditions(s, t, x, y, z, d, h):
    return (act(s, x) == x and act(t, y) == y
            and act(t, x) ^ x == act(s, d) ^ d
            and act(s, y) ^ y == act(t, d) ^ d
            and z == x ^ y ^ act(t, d) ^ h ^ act(compose(s, t), h))


def low_dimension(dimension):
    unit = identity(dimension)
    vectors = range(1 << dimension)
    solutions = 0
    nontrivial = 0
    matrices = involutions(dimension)
    for s, t in product(matrices, repeat=2):
        if compose(s, t) != compose(t, s):
            continue
        for x, y, d, h in product(vectors, repeat=4):
            z = x ^ y ^ act(t, d) ^ h ^ act(compose(s, t), h)
            if len(span((x, y, z))) != 1 << dimension:
                continue
            if square_conditions(s, t, x, y, z, d, h):
                solutions += 1
                nontrivial += (s != unit or t != unit)
    assert nontrivial == 0
    return {"dimension": dimension, "involutory_matrices": len(matrices),
            "spanning_solutions": solutions, "nontrivial_actions": nontrivial}


def dimension_three():
    pairs = set()
    solutions = 0
    matrices = involutions(3)
    for s, t in product(matrices, repeat=2):
        if compose(s, t) != compose(t, s):
            continue
        for d, h in product(range(8), repeat=2):
            if square_conditions(s, t, 1, 2, 4, d, h):
                solutions += 1
                pairs.add((s, t))
    expected = {
        ((1, 2, 4), (1, 2, 4)),
        ((1, 2, 6), (3, 2, 6)),
        ((1, 3, 5), (1, 2, 5)),
        ((1, 6, 4), (5, 2, 4)),
    }
    assert pairs == expected
    assert solutions == 32
    return {"involutory_matrices": len(matrices), "solutions": solutions,
            "action_pairs": sorted(pairs)}


def weaker_condition_counterexample():
    s, t = (1, 5, 3), (6, 2, 3)
    unit = identity(3)
    assert compose(s, s) == compose(t, t) == unit
    assert compose(s, t) == compose(t, s)
    assert act(s, 1) == 1 and act(t, 2) == 2
    assert act(compose(s, t), 4) == 4
    generated = {unit, s, t, compose(s, t)}
    assert len(generated) == 4
    fixed = [v for v in range(8) if act(s, v) == act(t, v) == v]
    fixed_coordinates = [v for v in (1, 2, 4) if v in fixed]
    assert fixed == [0, 7] and fixed_coordinates == []
    return {"S_columns": s, "T_columns": t,
            "image_group_order": len(generated), "image_group_exponent": 2,
            "common_fixed_vectors": fixed,
            "common_fixed_coordinates": fixed_coordinates}


def main():
    result = {
        "status": "PASS",
        "low_dimension": [low_dimension(d) for d in range(3)],
        "dimension_three": dimension_three(),
        "weaker_condition_counterexample": weaker_condition_counterexample(),
        "scope": "Exact finite linear algebra only; not the uniform group proof.",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
