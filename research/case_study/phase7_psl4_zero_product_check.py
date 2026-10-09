#!/usr/bin/env python3
"""Exact identities for the zero-product PSL4 rank-five proof.

This does not certify case coverage or prove the full rank conjecture.
Requires Python 3 and SymPy. Default report is adjacent; --output can
select a scratch report without changing a historical report.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import sympy as s


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    checks = []
    I2, I4, O = s.eye(2), s.eye(4), s.zeros(2)
    X = s.Matrix([[0,1],[1,0]])
    Z = s.diag(1,-1)
    J = s.Matrix([[0,1],[-1,0]])
    a,b,c,d,l = s.symbols("a b c d l")

    def eq(label, A, B):
        E = A-B
        entries = list(E) if isinstance(E,s.MatrixBase) else [E]
        assert all(s.cancel(e)==0 for e in entries), label
        checks.append(label)

    def block(A,B,C,D):
        return A.row_join(B).col_join(C.row_join(D))

    def omega(F):
        return block(O,F,-F,O)

    def E(i,j):
        A=s.zeros(4);A[i-1,j-1]=1
        return A

    variables = s.symbols("x0:16")
    Y = s.Matrix(4,4,variables)
    for label,N,M,dimension in [
        ("rank-one independent images and forms",E(1,3),E(2,4),6),
        ("rank-one common image",E(1,3),E(1,4),7),
        ("rank one and rank two",E(1,4),E(1,3)+E(2,4),6),
        ("rank two and rank two",block(O,I2,O,O),block(O,Z,O,O),6),
    ]:
        equations = s.linear_eq_to_matrix(list(Y*N-N*Y)+list(Y*M-M*Y),variables)[0]
        assert 16-equations.rank()==dimension, label
        checks.append(f"common centralizer dimension: {label} = {dimension}")
        eq(f"{label}: N squared zero",N*N,s.zeros(4))
        eq(f"{label}: M squared zero",M*M,s.zeros(4))
        eq(f"{label}: NM zero",N*M,s.zeros(4))
        eq(f"{label}: MN zero",M*N,s.zeros(4))

    N=E(1,4);M=E(1,3)+E(2,4)
    T0=s.diag(1,-1,1,-1);T4=s.diag(1,-1,-1,1)
    F=E(1,4)+E(2,3)-E(4,1)-E(3,2)
    for label,T,multiplier in [
        ("outer left",T0,-1), ("outer right",T4,1),
        ("inner left",T0*(I4+N),-1), ("inner right",(I4+M)*T4,1),
    ]:
        eq(f"rank (1,2) {label} involution",T*T,I4)
        eq(f"rank (1,2) {label} form multiplier",T.T*F*T,multiplier*F)
    T=s.zeros(4)
    T[3,0]=a;T[0,3]=1/a;T[2,1]=b;T[1,2]=1/b
    eq("rank (1,2) remaining monomial squares to I",T*T,I4)
    eq("rank (1,2) remaining monomial negates alternating form",T.T*F*T,-F)

    N=block(O,I2,O,O);M=block(O,l*Z,O,O)
    for Fname,F in [("I",I2),("Z",Z)]:
        for name,U in [("N",I4+N),("M",I4+M)]:
            eq(f"rank (2,2) unipotent {name} preserves Omega_{Fname}",U.T*omega(F)*U,omega(F))
        for name,T,mu in [
            ("T0",s.diag(X,-X),-1 if Fname=="I" else 1),
            ("commuting T4",s.diag(X,X),1 if Fname=="I" else -1),
            ("anticommuting T4",s.diag(s.I*J,s.I*J),-1 if Fname=="I" else 1),
            ("semisimple Z",s.diag(Z,Z),1),
        ]:
            eq(f"rank (2,2) {name} preserves Omega_{Fname} up to stated scalar",T.T*omega(F)*T,mu*omega(F))
    for name,D,F in [("commuting",a*I2+b*X,I2),("anticommuting",a*Z+b*J,Z)]:
        T=block(O,D,D.inv(),O)
        eq(f"rank (2,2) {name} D is self-adjoint for selected F",D.T*F,F*D)
        eq(f"rank (2,2) off-block {name} middle squares to I",T*T,I4)
        eq(f"rank (2,2) off-block {name} middle negates form",T.T*omega(F)*T,-omega(F))

    S=s.diag(X,-X);T=s.diag(J,J)
    Q=block(a*I2,b*J,c*J,d*I2)
    eq("Pauli outer centralizer template commutes with first outer",Q*S,S*Q)
    eq("Pauli outer centralizer template commutes with second outer",Q*T,T*Q)
    equations=s.linear_eq_to_matrix(list(Y*S-S*Y)+list(Y*T-T*Y),variables)[0]
    assert equations.rank()==12
    checks.append("Pauli outer centralizer dimension four, matching template")
    eq("Pauli middle exact involution equations",Q*Q-I4,
       block((a*a-b*c-1)*I2,b*(a+d)*J,c*(a+d)*J,(d*d-b*c-1)*I2))
    Q=Q.subs(d,-a)
    eq("Pauli middle form identity before imposing involution",Q.T*omega(Z)*Q,(-a*a+b*c)*omega(Z))
    Q=s.diag(a*I2,d*I2)
    eq("diagonal Pauli middle form multiplier",Q.T*omega(Z)*Q,a*d*omega(Z))

    report={
        "status":"PASS", "executed_at_utc":datetime.now(timezone.utc).isoformat(),
        "sympy_version":s.__version__,"checks_passed":len(checks),"checks":checks,
        "scope":"Exact identities in rank-five proof. Normal-form coverage and rank-six exclusion are not certified by this script.",
        "sha256":{name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in [Path(__file__).name,"phase7_psl4_zero_product.md"]},
    }
    output=args.output or here/"phase7_psl4_zero_product_check.json"
    output.write_text(json.dumps(report,indent=2)+"\n")
    print(f"PASS: {len(checks)} exact checks; report {output.name}")


if __name__=="__main__":
    main()
