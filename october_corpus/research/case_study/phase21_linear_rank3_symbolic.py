#!/usr/bin/env python3
"""Exact localized-polynomial identities; no finite samples prove coverage."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sympy as S

nu, s, u, w = S.symbols('nu s u w', nonzero=True)
I = S.eye(4)
def e(i,j):
    M=S.zeros(4); M[i-1,j-1]=1
    return M
def x(i,j,t): return I+t*e(i,j)
def comm(g,h): return g*h*g.inv()*h.inv()
def simplify(M): return M.applyfunc(S.cancel) if isinstance(M,S.MatrixBase) else S.cancel(M)
checks=[]
def ck(label, actual, expected):
    difference=simplify(actual-expected)
    assert difference==(S.zeros(*difference.shape) if isinstance(difference,S.MatrixBase) else 0), (label,difference)
    checks.append(label)

A=S.zeros(4); A[:2,2:]=S.eye(2); A[2:,:2]=nu*S.eye(2)
C=S.diag(1,1,-1,-1)
v=S.Matrix([1,0,0,1]); phi=S.Matrix([[0,1,1,1]])
B=I-2*v*phi
ck('reflection pairing', (phi*v)[0], 1)
ck('A square', A*A, nu*I)
ck('B square', B*B, I)
ck('C square', C*C, I)
ck('outer anticommutation', A*C, -C*A)
ck('A determinant', A.det(), nu**2)
ck('B determinant', B.det(), -1)
ck('C determinant', C.det(), 1)
ck('A exceptional-line image', A*v, S.Matrix([0,1,nu,0]))
U=(B*C)**2; V=A*U*A.inv()
P=I[:,[0,2,1,3]]
Ub=P.T*U*P; Vb=P.T*V*P
ck('U entire ordered block matrix', Ub, S.Matrix([[1,4,-8,4],[0,1,0,0],[0,0,1,0],[0,0,-4,1]]))
ck('U W block',Ub[:2,:2],S.Matrix([[1,4],[0,1]]))
ck('U quotient block',Ub[2:,2:],S.Matrix([[1,0],[-4,1]]))
ck('V W block',Vb[:2,:2],S.Matrix([[1,0],[4*nu,1]]))
ck('V quotient block',Vb[2:,2:],S.Matrix([[1,-4/nu],[0,1]]))
ck('U lower-left block zero',Ub[2:,:2],S.zeros(2))
ck('V lower-left block zero',Vb[2:,:2],S.zeros(2))
ck('U nilpotent square',(U-I)**2,-16*e(1,2))
ck('U nilpotent cube',(U-I)**3,S.zeros(4))
X=S.symbols('X')
ck('BC characteristic polynomial',(B*C).charpoly(X).as_expr(),(X-1)**3*(X+1))
for sign in [1,-1]:
    ck(f'first trace word sign{sign}',S.trace((Ub[:2,:2]**sign)*Vb[:2,:2]),2+16*sign*nu)
    ck(f'second trace word sign{sign}',S.trace((Ub[2:,2:]**sign)*Vb[2:,2:]),2+16*sign/nu)
ck('first squared-trace difference',(2+16*nu)**2-(2-16*nu)**2,128*nu)
ck('second squared-trace difference',(2+16/nu)**2-(2-16/nu)**2,128/nu)
a,b,c,d=S.symbols('a b c d')
Z=S.BlockMatrix([[-S.eye(2),S.Matrix([[a,b],[c,d]])],[S.zeros(2),S.eye(2)]]).as_explicit()
ck('central block lift square',Z*Z,I)
Y=S.Matrix([[a,b],[c,d]])
E21=S.Matrix([[0,0],[1,0]]); E12=S.Matrix([[0,1],[0,0]])
L=S.eye(2)+u*E21; R=S.eye(2)+w*E12
ck('double root difference',L*Y*R-L*Y-Y*R+Y,S.Matrix([[0,0],[0,u*w*a]]))
T=I-e(1,4)+S.Rational(1,2)*e(3,4)
Q=T*B*x(3,1,s)*B*T.inv()
ck('root extraction first conjugate',Q,I-2*s*(e(4,1)-2*e(4,2)-2*e(4,3)))
ck('root extraction commutator',comm(x(1,3,u),Q),x(4,3,2*u*s))
ck('root43 plus31',comm(x(4,3,u),x(3,1,s)),x(4,1,u*s))
ck('root24 plus41',comm(x(2,4,u),x(4,1,s)),x(2,1,u*s))
ck('root21 plus13',comm(x(2,1,u),x(1,3,s)),x(2,3,u*s))

# The q=9 exceptional-group exclusion is checked as a polynomial identity
# for both possible traces of a primitive element, not by a group recognizer.
t=S.symbols('t')
for trace in [1,-1]:
    modulus=S.Poly(t*t-trace*t-1,t,modulus=3)
    values=[S.rem(S.Poly((2+sign*t)**2,t,modulus=3),modulus).as_expr() for sign in [1,-1]]
    assert S.Integer(-1) in values, (trace,values)
    checks.append(f'q9 trace-square2 at primitive trace{trace}')
report=dict(status='PASS',executed_utc=datetime.now(timezone.utc).isoformat(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    exact_identities=len(checks),checks=checks,
    scope='Exact rational matrix identities over Z[1/2,nu,nu^-1] and q9 polynomial reductions. Dickson, automorphisms, Goursat, perfection and the uniform group argument remain explicit written inputs/proofs; no universal conclusion is inferred from finite sampling.')
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'exact checks')
