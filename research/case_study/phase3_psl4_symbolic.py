"""Exact polynomial checks for the new PSL4 form identities.

This checks identities over Z modulo the stated polynomial relations. It is
not a certificate of the representation-theoretic classification or of the
full PSL4 maximum-rank conjecture.
"""

from pathlib import Path
import hashlib
import json
import sympy as s


def zero_matrix(matrix):
    remainders = [s.expand(z) for z in matrix]
    assert all(z == 0 for z in remainders), remainders
    return len(remainders)


def main():
    a, b, c, d, e, f, u, v, w, x, y, h, j = s.symbols(
        "a b c d e f u v w x y h j"
    )
    L = s.Matrix([[a, b], [c, -a]])
    R = s.Matrix([[d, e], [f, -d]])
    QL = s.diag(c, b)
    QR = s.diag(f, e)
    checks = {}
    checks["left_diagonal_form"] = zero_matrix(
        L.T * QL * L - QL - (a*a + b*c - 1)*QL
    )
    checks["right_diagonal_form"] = zero_matrix(
        R.T * QR * R - QR - (d*d + e*f - 1)*QR
    )
    middle = s.Matrix([[u, 0, v, 0], [0, h, 0, 0],
                       [w, 0, -u, 0], [0, 0, 0, j]])
    B = s.diag(x*c, x*b, y*f, y*e)
    involution_relation = u*u + v*w - 1
    weight_relation = x*c*v - y*f*w
    explained = s.zeros(4)
    explained[0, 0] = x*c*involution_relation - w*weight_relation
    explained[0, 2] = explained[2, 0] = u*weight_relation
    explained[2, 2] = y*f*involution_relation + v*weight_relation
    explained[1, 1] = x*b*(h*h - 1)
    explained[3, 3] = y*e*(j*j - 1)
    checks["separated_support_middle"] = zero_matrix(
        middle.T * B * middle - B - explained)
    Z = s.diag(1, -1)
    X = s.Matrix([[0, 1], [1, 0]])
    J = s.Matrix([[0, 1], [-1, 0]])
    Lnormal = s.Matrix([[a, b], [-b, -a]])
    checks["normal_form_symmetric_form"] = zero_matrix(
        Lnormal.T * Z * Lnormal - Z - (a*a - b*b - 1)*Z)
    assert X.T * Z * X == -Z
    assert X.T * J * X == -J
    assert Z.T * J * Z == -J
    assert X * Lnormal == -Lnormal * X
    checks["sign_intertwiner_and_form_identities"] = 4
    for P in [s.eye(2), X, Z, J]:
        for Q in [s.eye(2), X, Z, J]:
            assert P.T * Q * P in [Q, -Q]
    checks["all_pauli_matrices_preserve_each_pauli_form_up_to_sign"] = 16
    r, z = s.symbols("r z")
    off_diagonal = s.Matrix([[0, r], [z, 0]])
    checks["off_diagonal_symmetric_form"] = zero_matrix(
        off_diagonal.T * X * off_diagonal - X - (r*z - 1)*X)

    # Abstract rank-one reflection expansion: B(v,v)=2d and
    # B(v,z)=d*f(z). The four terms must cancel exactly.
    fx, fy, weight = s.symbols("fx fy weight")
    assert s.expand(-fx*weight*fy - fy*weight*fx + fx*fy*2*weight) == 0
    checks["rank_one_reflection_form_expansion"] = 1

    here = Path(__file__).resolve()
    report = {
        "status": "passed",
        "arithmetic": "direct exact polynomial identities over Z; constraint combinations are explicitly supplied, with no division",
        "sympy_version": s.__version__,
        "checks": checks,
        "scope": "Matrix identities only; no certificate of the normal-form classification, irreducibility deductions, or the full PSL4 rank conjecture.",
        "script_sha256": hashlib.sha256(here.read_bytes()).hexdigest(),
        "proof_sha256": hashlib.sha256(
            here.with_name("phase3_psl4.md").read_bytes()).hexdigest(),
    }
    target = here.with_name("phase3_psl4_symbolic.json")
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
