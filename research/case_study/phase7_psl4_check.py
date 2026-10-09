#!/usr/bin/env python3
"""Exact algebra certificates for phase7_psl4.md; Python 3 and SymPy.

Run in place, or use --output /a/scratch/report.json to retain an old report.
The checks certify the printed polynomial identities, not completeness of
the representation-theoretic arguments or the PSL4 maximum-rank conjecture.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import sympy as s


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    checks = []

    def eq(label, left, right):
        difference = left - right
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        assert all(s.expand(entry) == 0 for entry in entries), label
        checks.append(label)

    I = s.eye(4)
    X = s.zeros(4)
    X[0, 1] = X[1, 2] = 1
    a, b, c, d, e, f = s.symbols("a b c d e f")
    R = s.Matrix([[a, b, c, d], [0, a, b, 0], [0, 0, a, 0], [0, 0, e, f]])
    eq("Jordan (3,1) displayed centralizer commutes with X", R * X, X * R)
    unknowns = s.symbols("r0:16")
    Y = s.Matrix(4, 4, unknowns)
    centralizer_equations = s.linear_eq_to_matrix(list(Y * X - X * Y), unknowns)[0]
    assert centralizer_equations.rank() == 10
    assert s.Matrix.hstack(*(s.Matrix(16, 1, list(R.diff(z))) for z in (a,b,c,d,e,f))).rank() == 6
    checks.append("centralizer dimension is six and displayed parametrization is exhaustive")
    expected_square = s.Matrix([
        [a*a-1, 2*a*b, 2*a*c+b*b+d*e, d*(a+f)],
        [0, a*a-1, 2*a*b, 0],
        [0, 0, a*a-1, 0],
        [0, 0, e*(a+f), f*f-1],
    ])
    eq("centralizer involution equations before eliminating b", R*R-I, expected_square)
    U = I + X + X*X/2
    Ui = I - X + X*X/2
    eq("truncated exponential inverse uses denominator two only", U*Ui, I)
    eq("truncated logarithm returns X", (U-I)-(U-I)**2/2, X)
    eq("truncated logarithm of inverse is minus X", (Ui-I)-(Ui-I)**2/2, -X)

    t, z, u, v, w, k = s.symbols("t z u v w k")
    basis = [I[:, i] for i in range(4)]
    T0 = s.diag(1, -1, 1, 1)
    T4 = s.diag(1, 1, -1, 1)
    T1 = I - (basis[1]+a*basis[0]) * (2*basis[1].T+b*basis[3].T)
    T3 = I - (basis[2]+c*basis[0]) * (2*basis[2].T+d*basis[3].T)
    endpoints = {"T0":T0, "T1":T1, "T3":T3, "T4":T4}
    F = s.Matrix([[0,0,0,b*d*t],[0,2*a*d*t,0,0],[0,0,2*b*c*t,0],[b*d*t,0,0,z]])
    for name, T in endpoints.items():
        eq(f"Jordan-three endpoint {name} squares to identity", T*T, I)
        eq(f"Jordan-three endpoint {name} preserves F", T.T*F*T, F)
    for i in ("T0", "T1"):
        for j in ("T3", "T4"):
            eq(f"Jordan-three cross pair {i},{j} commutes", endpoints[i]*endpoints[j], endpoints[j]*endpoints[i])
    N = T0*T1-I
    eq("Jordan-three square identifies nonzero a*b condition", N*N, -2*a*b*(basis[0]*basis[3].T))
    eq("Jordan-three nilpotent cube vanishes", N**3, s.zeros(4))
    C = s.Matrix([[u,v],[w,-u]])
    F2 = s.Matrix([[0,k],[k,z]])
    relation = u*u+v*w-1
    linear = 2*u*k+w*z
    remainder = s.Matrix([[w*linear, k*relation-u*linear], [k*relation-u*linear,z*relation-v*linear]])
    eq("middle-form residual is explicit combination of two defining relations", C.T*F2*C-F2, remainder)

    n = s.Matrix([[0,1],[0,0]])
    Z = s.diag(1,-1)
    N = s.kronecker_product(n, s.eye(2))
    M = s.kronecker_product(s.eye(2), n)
    eq("regular square-zero algebra has N squared zero", N*N, s.zeros(4))
    eq("regular square-zero algebra has M squared zero", M*M, s.zeros(4))
    eq("regular square-zero algebra has commuting generators", N*M, M*N)
    assert (N*M).rank() == 1
    checks.append("regular square-zero algebra has nonzero product of rank one")
    assert s.Matrix.hstack(*(s.Matrix(16, 1, list(E)) for E in (I,N,M,N*M))).rank() == 4
    equations = s.linear_eq_to_matrix(list(Y*N-N*Y)+list(Y*M-M*Y),unknowns)[0]
    assert equations.rank() == 12
    checks.append("centralizer of regular square-zero algebra is exactly its four-dimensional span")
    for T, left_sign, right_sign, name in [
        (s.kronecker_product(Z,s.eye(2)), -1, 1, "outer left"),
        (s.kronecker_product(s.eye(2),Z), 1, -1, "outer right"),
    ]:
        eq(f"{name} conjugates N with required sign", T*N*T, left_sign*N)
        eq(f"{name} conjugates M with required sign", T*M*T, right_sign*M)

    bound_files = [Path(__file__).name, "phase7_psl4.md", "phase3_psl4.md", "psl4_theory.md"]
    report = {
        "status":"PASS",
        "executed_at_utc":datetime.now(timezone.utc).isoformat(),
        "sympy_version":s.__version__,
        "checks_passed":len(checks),
        "checks":checks,
        "method":"Exact symbolic identities over Z[1/2]; displayed residual identities specialize in every odd characteristic. Centralizer dimensions are checked over Q and their explicit normal forms are proved in the note.",
        "scope":"Algebra identities in Propositions B and C. Not module-case completeness, not finite field generation/IP, and not a resolution of ranks five or six.",
        "sha256":{name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in bound_files},
    }
    output = args.output or here/"phase7_psl4_check.json"
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(f"PASS: {len(checks)} exact algebra checks; report {output.name}")


if __name__ == "__main__":
    main()
