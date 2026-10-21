#!/usr/bin/env python3
"""Independent integral centralizer audit for the PSL4 zero-product proof.

Requires Python 3 and SymPy. Integer Smith factors and primitive template
coordinates establish the stated centralizers over every field of odd
characteristic. This checks linear algebra, not normal-form case coverage.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    O, I = s.zeros(2), s.eye(2)
    X = s.Matrix([[0, 1], [1, 0]])
    Z = s.diag(1, -1)
    J = s.Matrix([[0, 1], [-1, 0]])
    a, b, c, d, e, f, g = s.symbols("a b c d e f g")

    def block(A, B, C, D):
        return A.row_join(B).col_join(C.row_join(D))

    def unit(i, j):
        M = s.zeros(4)
        M[i - 1, j - 1] = 1
        return M

    def factors(M):
        D = smith_normal_form(M, domain=s.ZZ)
        return [abs(int(D[i, i])) for i in range(min(D.shape)) if D[i, i]]

    vars_y = s.symbols("y0:16")
    Y = s.Matrix(4, 4, vars_y)
    E = s.Matrix([[c, d], [e, f]])
    cases = [
        ("rank (1,1), independent images and forms", unit(1, 3), unit(2, 4),
         block(s.diag(a, b), E, O, s.diag(a, b)), (a, b, c, d, e, f), [1] * 10),
        ("rank (1,1), common image", unit(1, 3), unit(1, 4),
         s.Matrix([[a, b, c, d], [0, e, f, g], [0, 0, a, 0], [0, 0, 0, a]]),
         (a, b, c, d, e, f, g), [1] * 9),
        ("rank (1,2)", unit(1, 4), unit(1, 3) + unit(2, 4),
         block(s.Matrix([[a, b], [0, a]]), E, O, s.Matrix([[a, b], [0, a]])),
         (a, b, c, d, e, f), [1] * 10),
        ("rank (2,2)", block(O, I, O, O), block(O, Z, O, O),
         block(s.diag(a, b), E, O, s.diag(a, b)), (a, b, c, d, e, f),
         [1] * 8 + [2] * 2),
        ("anticommuting outer lifts", s.diag(X, -X), s.diag(J, J),
         block(a * I, b * J, c * J, d * I), (a, b, c, d),
         [1] * 8 + [2] * 4),
    ]
    records = []
    for label, L, R, T, parameters, expected in cases:
        equations, rhs = s.linear_eq_to_matrix(list(Y * L - L * Y) + list(Y * R - R * Y), vars_y)
        assert rhs == s.zeros(32, 1)
        actual = factors(equations)
        assert actual == expected, (label, actual)
        assert T * L == L * T and T * R == R * T, label
        coordinates, constant = s.linear_eq_to_matrix(list(T), parameters)
        assert constant == s.zeros(16, 1)
        template_factors = factors(coordinates)
        assert template_factors == [1] * len(parameters), label
        assert 16 - len(actual) == len(parameters), label
        records.append({
            "case": label,
            "centralizer_dimension_every_odd_characteristic": len(parameters),
            "commutator_system_smith_factors": actual,
            "template_coordinate_smith_factors": template_factors,
            "template_commutation_identity": "PASS",
        })
    inputs = [Path(__file__).name, "phase7_psl4_zero_product.md", "phase7_psl4_zero_product_check.py", "phase7_psl4.md", "phase3_psl4.md", "psl4_theory.md"]
    report = {
        "status": "PASS",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "sympy_version": s.__version__,
        "cases": records,
        "scope": "All five centralizer templates are exact over every field of odd characteristic, including three. Normal-form coverage, finite-2-group splitting and the PSL4 contradiction are written proof obligations, not established by this script. No rank-six exclusion is claimed.",
        "sha256": {name: hashlib.sha256((here / name).read_bytes()).hexdigest() for name in inputs},
    }
    output = args.output or here / "phase7_psl4_zero_product_audit_check.json"
    output.write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: all five integer centralizer systems and primitive templates; report " + output.name)


if __name__ == "__main__":
    main()
