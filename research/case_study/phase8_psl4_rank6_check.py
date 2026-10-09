#!/usr/bin/env python3
"""Exact algebra checks for the rank-six obstruction proof; requires SymPy.

The report records identities and explicit nonvanishing factors, rather
than interpreting failed finite searches as nonexistence proofs.
"""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import sympy as s


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    checks=[]
    I=s.eye(2);O=s.zeros(2)
    X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);J=s.Matrix([[0,1],[-1,0]])
    a,b,c,t=s.symbols("a b c t")

    def eq(label,A,B):
        E=A-B
        entries=list(E) if isinstance(E,s.MatrixBase) else [E]
        assert all(s.cancel(e)==0 for e in entries),label
        checks.append(label)

    # Explicit simultaneous sign-intertwiner equations.
    R=s.Matrix([[a,b],[c,-a]])
    x,y=s.symbols("x y")
    D=s.diag(x,y);K=s.Matrix([[0,x],[y,0]])
    eq("diagonal centralizer constraint for a nonscalar pair",D*R-R*D,
       s.Matrix([[0,b*(x-y)],[c*(y-x),0]]))
    eq("one sign-twist diagonal obstruction contains 2a*x and -2a*y",D*R+R*D,
       s.Matrix([[2*a*x,b*(x+y)],[c*(x+y),-2*a*y]]))
    eq("other sign-twist off-diagonal obstruction",K*R-R*K,
       s.Matrix([[c*x-b*y,-2*a*x],[2*a*y,b*y-c*x]]))
    eq("both-negative sign-intertwiner is a single linear equation",K*R+R*K,(b*y+c*x)*I)
    eq("both-negative template anticommutes with both generators",
       s.Matrix([[0,b],[-c,0]])*R+R*s.Matrix([[0,b],[-c,0]]),O)

    # Every translation coefficient relation factors the middle as a tensor.
    h0,h1=s.symbols("h0 h1")
    for alpha,beta,sigma in itertools.product((0,1),(0,1),(1,-1)):
        ratio=sigma*(-1)**beta
        T=s.zeros(4)
        for i,j in itertools.product((0,1),repeat=2):
            T[2*(i^alpha)+(j^beta),2*i+j]=ratio**i*(h0 if j==0 else h1)
        P=s.zeros(2);Q=s.zeros(2)
        for i in (0,1): P[i^alpha,i]=ratio**i
        for j in (0,1): Q[j^beta,j]=h0 if j==0 else h1
        eq(f"monomial coefficient factorization alpha={alpha}, beta={beta}, sigma={sigma}",T,s.kronecker_product(P,Q))

    # A signed pair intertwiner carries additive commutators with product sign.
    matrices=[]
    for name in ("P","Q","R","S","C"):
        matrices.append(s.Matrix(2,2,s.symbols(f"{name}0:4")))
    PU,QU,PW,QW,C=matrices
    for sp,sq in itertools.product((1,-1),repeat=2):
        eP=PU*C-sp*C*PW;eQ=QU*C-sq*C*QW
        left=(PU*QU-QU*PU)*C-sp*sq*C*(PW*QW-QW*PW)
        right=PU*eQ+sq*eP*QW-QU*eP-sp*eQ*PW
        eq(f"signed additive-commutator transport signs {sp},{sq}",left,right)

    Y=s.Matrix([[0,t],[1/t,0]])
    L=a*Z+b*J
    models=[
        ("one negative",[Z,X,X,I],[Z,I,X,Z],4,4),
        ("two negatives in a row",[Z,X,X,X],[Z,I,X,Y],4,-(t-1/t)**2),
        ("four negatives",[Z,L,X,X],[Z,Z,X,Y],-4*b*b,-(t-1/t)**2),
    ]
    witnesses=[]
    for name,U,W,left_det,right_det in models:
        eq(f"{name}: left pair commutes on W",W[0]*W[1]-W[1]*W[0],O)
        eq(f"{name}: right pair commutes on U",U[2]*U[3]-U[3]*U[2],O)
        eq(f"{name}: nonzero left-block additive commutator determinant",(U[0]*U[1]-U[1]*U[0]).det(),left_det)
        eq(f"{name}: nonzero right-block additive commutator determinant",(W[2]*W[3]-W[3]*W[2]).det(),right_det)
        for triple in itertools.combinations(range(4),3):
            pair=(0,1) if 0 in triple and 1 in triple else (2,3)
            assert set(pair).issubset(triple)
            witnesses.append({"model":name,"triple":list(triple),"distinguishing_pair":list(pair),"nonzero_determinant":str(left_det if pair==(0,1) else right_det)})
    checks.append("all twelve three-endpoint subsets contain a certified distinguishing pair")

    # Tensor form identity, with no invertibility or characteristic assumption.
    P=s.Matrix(2,2,s.symbols("p0:4"));Q=s.Matrix(2,2,s.symbols("q0:4"))
    eq("every two-dimensional matrix preserves J up to determinant",P.T*J*P,P.det()*J)
    T=s.kronecker_product(P,Q);F=s.kronecker_product(J,J)
    eq("every pure tensor preserves J tensor J up to determinant product",T.T*F*T,P.det()*Q.det()*F)

    # Rank (1,2): a nonzero weight translation cannot preserve im N.
    weights=[(0,0),(1,1),(0,1),(1,0)]
    fixed=[]
    for alpha,beta in itertools.product((0,1),repeat=2):
        perm=[weights.index((i^alpha,j^beta)) for i,j in weights]
        fixed.append({"translation":[alpha,beta],"preserves_first_line":perm[0]==0})
        assert (perm[0]==0)==(alpha==0 and beta==0)
    checks.append("rank (1,2): only identity outer-weight translation preserves im N")

    files=[Path(__file__).name,"phase8_psl4_rank6.md","phase7_psl4.md","phase7_psl4_zero_product.md","phase3_psl4.md","phase3_psl4_rank7.md","psl4_theory.md"]
    report={
        "status":"PASS","executed_at_utc":datetime.now(timezone.utc).isoformat(),
        "sympy_version":s.__version__,"checks_passed":len(checks),"checks":checks,
        "three_endpoint_witnesses":witnesses,"rank_one_image_translation_check":fixed,
        "nonvanishing_assumptions":"Odd characteristic; t nonzero with t^2 != 1; b != 0 in the four-negative model. The explicit determinant factors then never vanish.",
        "scope":"Exact new intertwiner and form identities. Completeness of module normal forms and the full conjecture are matters of the written proof and independent review.",
        "sha256":{n:hashlib.sha256((here/n).read_bytes()).hexdigest() for n in files},
    }
    output=args.output or here/"phase8_psl4_rank6_check.json"
    output.write_text(json.dumps(report,indent=2)+"\n")
    print(f"PASS: {len(checks)} exact checks and {len(witnesses)} three-endpoint witnesses; report {output.name}")


if __name__=="__main__": main()
