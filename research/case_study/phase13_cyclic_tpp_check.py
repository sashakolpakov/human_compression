#!/usr/bin/env python3
"""Exact small-action check and frozen-input binding for phase13.

No group catalogue is searched. The finite through-256 result is retained.
"""
import hashlib
import itertools
import json
from pathlib import Path


def act(matrix, vector):
    out = 0
    for bit, column in enumerate(matrix):
        if vector & (1 << bit):
            out ^= column
    return out


def compose(left, right):
    return tuple(act(left, column) for column in right)


def closure(generators, dim):
    identity = tuple(1 << i for i in range(dim))
    found = {identity}
    todo = [identity]
    while todo:
        value = todo.pop()
        for generator in generators:
            product = compose(value, generator)
            if product not in found:
                found.add(product)
                todo.append(product)
    return found


def gl(dim):
    result = []
    for matrix in itertools.product(range(1 << dim), repeat=dim):
        if len({act(matrix, v) for v in range(1 << dim)}) == 1 << dim:
            result.append(matrix)
    return result


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    base = Path(__file__).resolve().parent
    action_results = []
    for dim in (1, 2):
        matrices = gl(dim)
        cases = 0
        for basis in matrices:
            for first, second in itertools.product(matrices, repeat=2):
                image = closure((first, second), dim)
                if len(image) & (len(image) - 1):
                    continue
                if act(first, basis[0]) != basis[0]:
                    continue
                if dim == 2 and act(second, basis[1]) != basis[1]:
                    continue
                cases += 1
                assert any(all(act(g, v) == v for g in image) for v in basis)
        action_results.append({
            "dimension": dim,
            "invertible_matrices": len(matrices),
            "marked_basis_action_cases": cases,
            "cases_without_a_common_fixed_marked_vector": 0,
        })

    # An essential scope boundary: three coordinates are different.
    first = (1, 5, 3)
    second = (6, 2, 3)
    third = compose(first, second)
    image = closure((first, second), 3)
    assert len(image) == 4
    assert act(first, 1) == 1 and act(second, 2) == 2 and act(third, 4) == 4
    assert not any(all(act(g, v) == v for g in image) for v in (1, 2, 4))

    cert_path = base / "phase3_cyclic_tpp_certificate.json"
    finite_cert = json.loads(cert_path.read_text())
    retained = []
    for filename in (
        "phase3_cyclic_tpp_exploration.md",
        "phase3_cyclic_tpp_search.g",
        "phase3_cyclic_tpp_search.log",
    ):
        actual = hash_file(base / filename)
        assert actual == finite_cert["sha256"][filename], filename
        retained.append({"file": filename, "sha256": actual})

    result = {
        "status": "PASS",
        "scope": "Exact GL1/GL2 action check plus retained through-256 input binding; not a new group census or full formal proof.",
        "action_results": action_results,
        "dimension_three_scope_boundary": {
            "first_columns": first,
            "second_columns": second,
            "generated_group_order": len(image),
            "common_fixed_marked_coordinates": 0,
        },
        "retained_finite_input": retained,
        "retained_finite_certificate_sha256": hash_file(cert_path),
        "proof_sha256": hash_file(base / "phase13_cyclic_tpp.md"),
        "checker_sha256": hash_file(Path(__file__).resolve()),
        "new_group_catalogue_search": False,
        "new_Lean_module": False,
    }
    print(json.dumps(result, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
