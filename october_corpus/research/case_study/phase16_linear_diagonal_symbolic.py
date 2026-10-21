#!/usr/bin/env python3
"""Exact rational-polynomial identities; no finite-field extrapolation."""
import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
h, a, b, v, w, z = s.symbols('h a b v w z')
I = s.eye(4)
checks = []

def check(name, expression):
    entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    assert all(s.cancel(x) == 0 for x in entries), (name, expression)
    checks.append(name)

def x(i, j, t):
    out = s.eye(4)
    out[i-1, j-1] = t
    return out

def comm(A, B):
    return A*B*A.inv()*B.inv()

r0 = s.Matrix([[0,1,1,0],[0,0,0,1],[-h,0,0,-1],[0,-h,0,0]])
r1 = s.diag(1,1,-1,1)
r2 = s.Matrix([[-1,0,0,0],[1,1,0,0],[-1,-2,-1,0],[0,1,1,1]])
r3 = s.diag(-1,1,1,-1)
rr = [r0,r1,r2,r3]
B = s.Matrix([[-4,2,0,-1],[2,-1,0,-2*h],[0,0,1+4*h,0],[-1,-2*h,0,h]])
for j, (r, square, det) in enumerate(zip(rr,[-h,1,1,1],[h*h,-1,1,1])):
    check(f'square_{j}',r*r-square*I)
    check(f'determinant_{j}',r.det()-det)
for i,j,sign in [(0,2,1),(0,3,-1),(1,3,1)]:
    check(f'string_{i}_{j}',rr[i]*rr[j]-sign*rr[j]*rr[i])
T = r0*r1
check('first_rotation_square',T*T-s.Matrix([[h,0,0,2],[0,-h,0,0],[0,0,h,0],[0,0,0,-h]]))
check('first_rotation_fourth',T**4-h*h*I)
for label,M,coords in [('12',r1*r2,[0,4,2]),('23',r2*r3,[-2,0,-2])]:
    N = M*M-I
    check(f'unipotent_cube_{label}',N**3)
    check(f'simple_coordinates_{label}',s.Matrix([N[1,0],N[2,1],N[3,2]])-s.Matrix(coords))
    X = s.Symbol('X')
    eigenpoly = (X-1)**3*(X+1) if label == '12' else (X-1)**2*(X+1)**2
    check(f'rotation_eigenvalues_{label}',M.charpoly(X).as_expr()-eigenpoly)
W = s.Matrix([[0,0,1,0],[0,0,0,1],[-h,0,0,0],[0,-h,0,0]])
check('W_conjugation',x(3,2,1)*r0*x(3,2,-1)-W)
check('upper_root_supply',W*x(3,2,1)*W.inv()-x(1,4,-1/h))
for label,i,j,k,l,target in [
    ('initial12',1,4,4,2,(1,2)), ('initial24',2,1,1,4,(2,4)),
    ('initial23',2,4,4,3,(2,3)), ('initial34',3,1,1,4,(3,4)),
    ('power12step',1,2,2,3,(1,3)), ('power12return',1,3,3,2,(1,2)),
    ('power23step',2,3,3,4,(2,4)), ('power23return',2,4,4,3,(2,3)),
    ('power34return',3,2,2,4,(3,4))]:
    check(label,comm(x(i,j,a),x(k,l,b))-x(*target,a*b))
check('form_determinant',B.det()-(1+4*h)**3)
for j,mult in [(0,-h),(1,1),(2,1)]:
    check(f'facet_form_{j}',rr[j]*B*rr[j].T-mult*B)

# Verify the successive elimination, retaining free entries until forced.
for d1,d3,d4 in itertools.product([-1,1],repeat=3):
    u21,u31,u41 = s.symbols('u21 u31 u41')
    g = s.Matrix([[d1,0,0,0],[u21,1,0,0],[u31,v,d3,0],[u41,z,w,d4]])
    defect = g*B*g.T-B
    check(f'row11_{d1}_{d3}_{d4}',defect[0,0])
    solution = {u21:s.Rational(1,2)*(1-d1)}
    check(f'row12_{d1}_{d3}_{d4}',defect[0,1].subs(solution))
    solution[u31] = v/2
    check(f'row13_{d1}_{d3}_{d4}',defect[0,2].subs(solution))
    solution[u41] = z/2+s.Rational(1,4)*(d1-d4)
    check(f'row14_{d1}_{d3}_{d4}',defect[0,3].subs(solution))
    check(f'row24_{d1}_{d3}_{d4}',defect[1,3].subs(solution)-(1-d4)*(1+4*h)/2)
    # Under d4=1, the remaining rows force w=d3*v/2 and z=v²/4.
    if d4 == 1:
        reduced = defect.subs(solution)
        check(f'row34_{d1}_{d3}',reduced[2,3]-(1+4*h)*(d3*w-v/2))
        check(f'row44_{d1}_{d3}',reduced[3,3].subs(w,d3*v/2)-(1+4*h)*(v*v-4*z)/4)
        check(f'all_form_entries_{d1}_{d3}',reduced.subs({w:d3*v/2,z:v*v/4}))

# Exact character projectors on the three simple root coordinates.
chars = [(1,-1),(-1,1),(-1,-1)]
u = s.Matrix([-1,-2,-1])
actions = [(i,j,s.diag(*[(c[0]**i)*(c[1]**j) for c in chars])) for i,j in itertools.product([0,1],repeat=2)]
for k,c in enumerate(chars):
    proj = sum((s.Rational(1,4)*c[0]**i*c[1]**j*A for i,j,A in actions),s.zeros(3))
    target = s.zeros(3,1); target[k] = -u[k]
    check(f'character_difference_projector_{k}',sum((s.Rational(1,4)*c[0]**i*c[1]**j*(u-A*u) for i,j,A in actions),s.zeros(3,1))-target)

report = {
    'result':'PASS','executed_utc':datetime.now(timezone.utc).isoformat(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'sympy_version':s.__version__,'exact_identity_count':len(checks),'checks':checks,
    'scope':'Rational-function identities, exact sign cases and character projectors. The all-field group generation and recursive intersection argument remain written proofs.',
    'denominators':'Only powers of 2 and h; form elimination additionally assumes 1+4h nonzero.',
}
(HERE/'phase16_linear_diagonal_symbolic.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {len(checks)} exact identities')
