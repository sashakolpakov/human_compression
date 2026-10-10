#!/usr/bin/env python3
"""Independent symbolic audit of the phase17 PGU4 template.

All identities are computed in Q(i,k), i^2=-1.  The field involution
fixes i and sends k to -k; it is NOT complex conjugation.  Polynomial
identities with denominator a power of two specialize to every odd
characteristic.  This does not verify generation or the group IP.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    k, x = s.symbols("k x")
    i = s.I
    bar = lambda a: a.applyfunc(lambda z: s.expand(z).subs(k, -k))
    zero = lambda a: all(s.simplify(z) == 0 for z in a)
    ident = s.eye(4)
    h = s.diag(1, -1, 1, -1)
    r = s.Matrix([[0, i], [i, 0]])
    ss = s.Matrix([[k, i-k], [i+k, -k]])
    generators = [
        s.diag(1, 1, -1, -1),
        s.Matrix([[1,0,0,0], [0,0,0,1], [0,0,1,0], [0,1,0,0]]),
        s.diag(r, ss),
        s.Matrix([[0,0,1,0], [0,0,0,1], [1,0,0,0], [0,1,0,0]]),
    ]
    b = s.diag(i+k, i+k, i-k, i+k)
    v = s.ones(4, 1)
    a = b*h
    nu = -1-k*k
    m = generators[2]*generators[3]
    n = m*m+ident
    c = m*(ident+n/2)
    checks = {}
    for j, g in enumerate(generators):
        checks[f"unitary_{j}"] = zero(g*h*bar(g).T-h)
        checks[f"square_{j}"] = zero(g*g-(-ident if j == 2 else ident))
        checks[f"determinant_{j}"] = s.simplify(g.det()-(-1 if j == 1 else 1)) == 0
    for j, multiplier in [(0, 1), (1, 1), (2, -1)]:
        checks[f"B_multiplier_{j}"] = zero(generators[j]*b*generators[j].T-multiplier*b)
    for j, l, multiplier in [(0,2,1), (0,3,-1), (1,3,1)]:
        checks[f"distant_{j}_{l}"] = zero(generators[j]*generators[l]-multiplier*generators[l]*generators[j])
    checks["block_diagonal_word"] = zero((generators[0]*generators[1])**2-s.diag(1,-1,1,-1))
    checks["N_nonzero"] = not zero(n)
    checks["N_square"] = zero(n*n)
    checks["M_characteristic"] = s.expand(m.charpoly(x).as_expr()-(x*x+1)**2) == 0
    checks["middle_characteristic"] = s.expand((generators[1]*generators[2]).charpoly(x).as_expr()-(x*x+1)*(x*x-k*x-1)) == 0
    checks["sigma_square"] = zero(a*bar(a)-nu*ident)
    checks["sigma_antiunitary"] = zero(bar(a).T*h*a-nu*h)
    checks["v_isotropic"] = zero(v.T*h*v)
    checks["sigma_v_isotropic"] = zero(bar(a*v).T*h*a*v)
    checks["cross_pair"] = s.simplify((v.T*h*a*v)[0]-(4*i+2*k)) == 0
    checks["C_square"] = zero(c*c+ident)
    checks["C_v"] = zero(c*v-i*v)
    checks["C_B_defect"] = s.simplify((c*b*c.T+b)[0,1]+i*k*k/2) == 0
    patterns = [list((generators[0]*generators[1])**j*v) for j in range(4)]
    checks["left_dihedral_line_orbit"] = patterns == [[1,1,1,1], [1,1,-1,-1], [1,-1,1,-1], [1,-1,-1,1]]
    report = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version": s.__version__,
        "ring": "Q(i,k), i^2=-1; bar(i)=i, bar(k)=-k",
        "checks": checks,
        "number_of_checks": len(checks),
        "scope": "Independent symbolic identities only. No group generation, full IP, or Lean verification is claimed.",
    }
    text = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
    assert all(checks.values())


if __name__ == "__main__":
    main()
