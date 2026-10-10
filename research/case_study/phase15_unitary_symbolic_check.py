#!/usr/bin/env python3
"""Exact symbolic identities used by the phase15 generation/intersection proofs."""
import sympy as s
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
I=s.I;a,b=s.symbols('a b',nonzero=True);c=-(1+a*a)/b
one=s.eye(4);zero=s.zeros(4)
R=s.Matrix([[0,I],[I,0]]);S=s.Matrix([[a,b],[c,-a]]);Z=s.diag(1,-1)
r0=s.diag(1,1,-1,-1);r1=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]])
r2=s.diag(R,S);r3=s.Matrix([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
rr=[r0,r1,r2,r3];tests=[]
def test(label,value):
 vals=list(value) if isinstance(value,s.MatrixBase) else [value]
 assert all(s.cancel(v)==0 for v in vals),label
 tests.append(label)
def bar(M):return M.applyfunc(lambda v:s.conjugate(v).subs({s.conjugate(a):-a,s.conjugate(b):-c},simultaneous=True))
for j,M in enumerate(rr):
 test('determinant_%d'%j,M.det()-1)
 test('unitary_%d'%j,M*bar(M).T-one)
for j,sgn in enumerate([1,1,-1,-1]):test('square_%d'%j,rr[j]**2-sgn*one)
for j,k,sgn in [(0,2,1),(0,3,-1),(1,3,-1)]:test('distant_%d%d'%(j,k),rr[j]*rr[k]-sgn*rr[k]*rr[j])
A=s.Matrix([[0,I*a,I*b-1,-I*a],[-I*a,0,-I*a,1-I*c],[1-I*b,I*a,0,I*a],[I*a,I*c-1,-I*a,0]])
B=s.diag(c,c,b,c);h=-a*a-I*(b+c)+2
for j,sgn in [(0,1),(1,1),(2,-1)]:test('symmetric_multiplier_%d'%j,rr[j]*B*rr[j].T-sgn*B)
for j,sgn in [(1,-1),(2,1),(3,1)]:test('alternating_multiplier_%d'%j,rr[j]*A*rr[j].T-sgn*A)
test('A_semilinear_square',A*bar(A)+h*one);test('B_semilinear_square',B*bar(B)-(1+a*a)*one)
test('A_determinant',A.det()-h*h)
T=r1*r2;W=A*B.inv();X=s.Symbol('X')
test('middle_polynomial',T.charpoly(X).as_expr()-(X**4+a*X**3-a*X+1))
test('middle_discriminant',s.discriminant(X**4+a*X**3-a*X+1,X)-4*(a*a-8)**2*(a*a+1))
v=s.Matrix([1,0,0,0]);test('Krylov_determinant',s.Matrix.hstack(v,T*v,T**2*v,T**3*v).det()+I*b)
test('commuting_relative_form',T*W-W*T)
coeff=[s.factor(v) for v in W.charpoly(X).all_coeffs()]
test('W_odd_cubic',coeff[1]);test('W_odd_linear',coeff[3])
f=a*a*b-I*a*a+I*b*b-2*b-I
actualdisc=16*coeff[4]*(coeff[2]**2-4*coeff[4])**2
expectdisc=-16*a**4*(a*a-8)**2*(a*a+b*b+1)**4*f*f/(a*a+1)**11
test('relative_form_discriminant',actualdisc-expectdisc)
test('relative_form_final_factor',f/b+h)
test('kernel_word_first_block',(Z*R)**2-s.eye(2))
test('kernel_word_second_block',(s.diag(Z,Z)*r2)**2-s.diag(s.eye(2),(Z*S)**2))
t,x,y,r,ss=s.symbols('t x y r ss',real=True)
b2=x+I*y;c2=-x+I*y
Uj=s.Matrix([[ss+I*r*x,-r*t],[r*t,ss-I*r*x]])
Vj=s.Matrix([[ss-I*r*x,r*t],[-r*t,ss+I*r*x]])
even=Uj*s.diag(c2,c2)*Uj.T
odd=R*Vj*s.diag(b2,c2)*(R*Vj).T
test('even_power_offdiagonal',even[0,1]-2*I*c2*r*r*x*t)
test('odd_power_offdiagonal',odd[0,1]-2*r*t*x*(ss+r*y))
# The diagonal-difference identity uses t²+x²+y²=1.
rem=s.rem(s.Poly(s.expand(odd[0,0]-odd[1,1]-2*x*((ss+r*y)**2-r*r)),t),s.Poly(t*t+x*x+y*y-1,t)).as_expr()
test('odd_power_diagonal_difference',rem)
base=Path(__file__).resolve().parent
report={'status':'PASS','executed_at_utc':datetime.now(timezone.utc).isoformat(),'exact_identity_count':len(tests),'checks':tests,
 'scope':'Symbolic matrix identities only. Group generation, torus classification, recursive IP and parameter existence remain written arguments.',
 'input_sha256':{Path(__file__).name:sha256(Path(__file__).read_bytes()).hexdigest()}}
(base/'phase15_unitary_symbolic_check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:',len(tests),'exact symbolic identities.')
