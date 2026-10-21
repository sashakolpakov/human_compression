#!/usr/bin/env python3
"""Polynomial identities for the twisted unitary diagonal-extension template."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
k=s.symbols('k',real=True); i=s.I; I=s.eye(4); X=s.symbols('X')
checks=[]
def ck(name,expr):
    entries=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    assert all(s.simplify(x)==0 for x in entries),(name,expr)
    checks.append(name)
R=s.Matrix([[0,i],[i,0]])
S=s.Matrix([[k,i-k],[i+k,-k]])
r0=s.diag(1,1,-1,-1)
r1=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
r2=s.diag(R,S)
r3=s.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
rr=[r0,r1,r2,r3];H=s.diag(1,-1,1,-1)
B=s.diag(i+k,i+k,i-k,i+k);v=s.ones(4,1)
for j,(r,square,det) in enumerate(zip(rr,[1,1,-1,1],[1,-1,1,1])):
    # Here bar(i)=-i and bar(k)=k.
    epsilon=-1 if j==2 else 1
    ck(f'unitary_{j}',r*H*s.conjugate(r).T-epsilon*H)
    ck(f'square_{j}',r*r-square*I)
    ck(f'determinant_{j}',r.det()-det)
for j,l,sign in [(0,2,1),(0,3,-1),(1,3,1)]:
    ck(f'string_{j}_{l}',rr[j]*rr[l]-sign*rr[l]*rr[j])
for j,mult in [(0,1),(1,1),(2,-1)]: ck(f'facet_form_{j}',rr[j]*B*rr[j].T-mult*B)
for j,eigen in [(1,1),(2,i),(3,1)]:ck(f'vertex_line_{j}',rr[j]*v-eigen*v)
T=r0*r1;ck('first_rotation_fourth',T**4-I)
ck('first_rotation_square',T*T-s.diag(1,-1,1,-1))
for j,signs in enumerate([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]):ck(f'first_rotation_line_{j}',T**j*v-s.Matrix(signs))
ck('middle_polynomial',(r1*r2).charpoly(X).as_expr()-(X*X+1)*(X*X-k*X-1))
M=r2*r3;N=M*M+I
ck('last_polynomial',M.charpoly(X).as_expr()-(X*X+1)**2)
ck('last_nilpotence',N*N)
ck('last_nonzero_entry',N[0,0]-i*k)
C=M*(I+N/2)
ck('central_square',C*C+I)
ck('central_line',C*v-i*v)
ck('central_form_obstruction',(C*B*C.T+B)[0,1]+i*k*k/2)
nu=1+k*k;D=B*H
ck('semilinear_square_twisted',D*s.conjugate(D)-nu*I)
ck('semilinear_hermitian_twisted',s.conjugate(D).T*H*D-nu*H)
d=D*v
ck('v_isotropic',(v.T*H*v)[0])
ck('sigma_v_isotropic',(s.conjugate(d).T*H*d)[0])
ck('cross_pair',(v.T*H*d)[0]-(4*i+2*k))
ck('B_determinant',B.det()-(i+k)**3*(i-k))
# Compare the exact block words with the previously used skew-swap construction.
old1=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]])
old3=s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
ck('generation_same_d',(r0*r1)**2-(r0*old1)**2)
ck('generation_negative_u',(r2*r3)**2+(r2*old3)**2)
ck('first_projective_kernel_word',((r0*r1)**2*r2)[:2,:2]**2-s.eye(2))
report={'result':'PASS','executed_utc':datetime.now(timezone.utc).isoformat(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'sympy_version':s.__version__,'exact_identity_count':len(checks),'checks':checks,
        'scope':'Exact identities with i^2=-1, bar(i)=-i and bar(k)=k. The parameter, generation, descent, counting and group-intersection arguments remain written proofs.',
        'denominators':'Only powers of two in these identities; the proof additionally uses k nonzero and norm-surjectivity.'}
(HERE/'phase17_unitary_twisted_symbolic.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities')
