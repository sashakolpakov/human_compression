#!/usr/bin/env python3
"""Exact GL3(F2) audit of the marked top-involution action."""
import hashlib
import itertools
import json
from pathlib import Path

IDENTITY = (1, 2, 4)


def act(matrix, vector):
    result = 0
    for bit, column in enumerate(matrix):
        if vector & (1 << bit):
            result ^= column
    return result


def mul(left, right):
    return tuple(act(left, column) for column in right)


def closure(generators):
    found = {IDENTITY}
    pending = [IDENTITY]
    while pending:
        value = pending.pop()
        for generator in generators:
            product = mul(value, generator)
            if product not in found:
                found.add(product)
                pending.append(product)
    return found


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    gl = [m for m in itertools.product(range(8), repeat=3)
          if len({act(m, v) for v in range(8)}) == 8]
    inverse = {m: next(n for n in gl if mul(m, n) == IDENTITY) for m in gl}
    pair_count = 0
    marked_count = 0
    survivors = []
    for first in gl:
        if act(first, 1) != 1:
            continue
        for second in gl:
            if act(second, 2) != 2:
                continue
            image = closure((first, second))
            if len(image) & (len(image) - 1):
                continue
            pair_count += 1
            # Phi(R)=<all squares, all commutators>; independent of the
            # dihedral case analysis used in the written proof.
            generators = [mul(g, g) for g in image]
            generators += [mul(mul(inverse[g], inverse[h]), mul(g, h))
                           for g in image for h in image]
            phi = closure(generators)
            for third in sorted({mul(mul(first, second), f) for f in phi}):
                if act(third, 4) != 4:
                    continue
                marked_count += 1
                if any(all(act(g, v) == v for g in image) for v in (1, 2, 4)):
                    continue
                survivors.append({
                    "first_columns": first,
                    "second_columns": second,
                    "third_columns": third,
                    "image_order": len(image),
                    "Frattini_order": len(phi),
                    "common_fixed_vectors": [v for v in range(8)
                                             if all(act(g, v) == v for g in image)],
                })
    assert len(gl) == 168
    assert len(survivors) == 1
    assert survivors[0] == {
        "first_columns": (1, 5, 3),
        "second_columns": (6, 2, 3),
        "third_columns": (6, 5, 4),
        "image_order": 4,
        "Frattini_order": 1,
        "common_fixed_vectors": [0, 7],
    }
    base = Path(__file__).resolve().parent
    print(json.dumps({
        "status": "PASS",
        "GL3_order": len(gl),
        "two_group_image_pairs_fixing_first_two_coordinates": pair_count,
        "marked_third_coset_action_cases": marked_count,
        "survivors_without_a_fixed_marked_coordinate": survivors,
        "scope": "Necessary top-layer action only; does not prove nonexistence of a group extension or a cyclic-TPP counterexample.",
        "proof_sha256": digest(base / "phase13_cyclic_tpp_top_action.md"),
        "checker_sha256": digest(Path(__file__).resolve()),
        "group_catalogue_used": False,
    }, indent=2))


if __name__ == "__main__":
    main()
