#!/usr/bin/env python3
"""Independent exact identities for the new rank-three template.

This is a rational-function/entry calculation, not a finite-group generation
or all-field existence checker. All identities are integral in z; odd
characteristic is an assumption of the written proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as S

z = S.symbols('z')
s = -z**2
I = S.eye(4)
H = S.diag(1, -1, 1, -1)
A = S.diag(1, 1, -1, -1)
C = S.Matrix([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
v = S.Matrix([z, -1, s-z, s+1])
bar = lambda M: M.applyfunc(lambda x: x.subs(z, -z))
phi = bar(v).T * H
B = I + v*phi
n = v+C*v
m = A*n
U = (B*C)**2
N = U-I
t = 2*s*(z-1)
checks = []
def check(name, value):
    if isinstance(value, S.MatrixBase):
        assert all(S.expand(x) == 0 for x in value), name
    else:
        assert S.expand(value) == 0, name
    checks.append(name)
check('norm v is -2', (phi*v)[0]+2)
check('B is unitary', bar(B).T*H*B-H)
check('B is involution', B*B-I)
check('determinant B is -1', B.det()+1)
check('A,C anticommute', A*C+C*A)
check('n coordinates', n-S.Matrix([s,s,s,s]))
check('m coordinates', m-S.Matrix([s,s,-s,-s]))
check('W totally isotropic', bar(n.row_join(m)).T*H*n.row_join(m))
check('U fixes n', U*n-n)
check('U sends m to m+tn', U*m-m-t*n)
check('A swaps n,m', A*m-n)
check('C fixes n', C*n-n)
check('C negates m', C*m+m)
check('nilpotent square', N*N-2*n*bar(n).T*H)
check('nilpotent cube', N**3)
check('B fixes n', B*n-n)
check('m,Bm pairing', (bar(m).T*H*B*m)[0]-4*s**2*(1+s))
check('trace t', t+t.subs(z,-z)+4*s)
check('tracezero t', t-t.subs(z,-z)-4*s*z)
check('t-square difference', t**2-t.subs(z,-z)**2+16*s**2*z)
x=S.symbols('x')
check('AB characteristic polynomial', (A*B).charpoly(x).as_expr()-(x-1)*(x+1)*(x**2-2*s*x+1))
check('BC characteristic polynomial', (B*C).charpoly(x).as_expr()-(x-1)**3*(x+1))
# Functional equations with independent formal q-th powers.
u,w,uq,wq=S.symbols('u w uq wq')
a,b,c,d,e,f,g,h=S.symbols('a b c d e f g h')
Pu=S.Matrix([[1,u],[0,1]])
Qw=S.Matrix([[1,0],[-wq,1]])
Du=S.Matrix([[a,b],[c,d]])
Dw=S.Matrix([[e,f],[g,h]])
expected=S.Matrix([[a+e+u*g-wq*b,b+f+u*h],[c+g-wq*d,d+h]])
check('all four off-block additive equations', Pu*Dw+Du*Qw-expected)
# Skew-Hermitian radical sends x*e1+y*e2+f2 to f2.
x0,xb,y=S.symbols('x0 xb y')
X=S.Matrix([[0,-x0],[xb,-y]])
J=S.zeros(4)
J[:2,:2]=S.eye(2);J[2:,2:]=S.eye(2);J[:2,2:]=X
check('remove adjacent-plane coordinates', J*S.Matrix([x0,y,0,1])-S.Matrix([0,0,0,1]))
parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(Path(__file__).with_suffix('.json')))
args=parser.parse_args()
result={'verdict':'PASS','scope':'Exact rational-function identities; not a group-generation certificate','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'count':len(checks),'nonzero_conditions_retained':['Odd characteristic','z nonzero and z^2 nonsquare in Fq','s=-z^2, hence s nonzero and 1+s nonzero'],'all_field_group_generation_checked':False}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'count':len(checks),'output':args.output}))
