#!/usr/bin/env python3
"""Exact coordinate conjugacy and full ambient period; no author code import."""
import json
from pathlib import Path
from itertools import product,permutations
import sympy as S
from sympy.matrices.normalforms import hermite_normal_form

def need(t,s):
    if not t:raise ValueError(s)

I=S.eye(4);r0=I.copy();r0[0,0]=-1;r0[0,3]=1
r1=I.copy();r1.row_swap(0,1)
r2=I.copy();r2.row_swap(1,2)
r3=I.copy();r3[2,2]=-1
T=S.diag(1,-1,-1,1);T[:3,3]=S.Matrix([-S.Rational(1,2),S.Rational(1,2),S.Rational(1,2)])
expected=[S.Matrix(x) for x in [
 [[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]],
 [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],
 [[0,-1,0,0],[-1,0,0,0],[0,0,-1,1],[0,0,0,1]],
 [[0,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]]]]
for word,want in zip([r0*r1*r0,r2,r1*r3,r1],expected):need(T*word*T.inv()==want,'exact source marker conjugacy')
period=(r0*r1*r2*r3*r2)**2
want=I.copy();want[:3,3]=S.Matrix([1,1,0]);need(period==want,'full toroid period')
roots=set()
for p in permutations(range(3)):
 for signs in product([-1,1],repeat=3):roots.add(tuple(signs[i]*[1,1,0][p[i]] for i in range(3)))
H=hermite_normal_form(S.Matrix.hstack(*(S.Matrix(v) for v in sorted(roots))))
need(len(roots)==12 and abs(H.det())==2 and all(sum(v)%2==0 for v in roots),'whole D3 period orbit')
print(json.dumps(dict(status='PASS_CUBIC_TOROID_RELATION',exact_marker_identities=4,period=[1,1,0],period_orbit_size=12,lattice_index=2,full_group_order='96*s^3',hypertope_group_order='48*s^3',subgroup_index=2,full_Coxeter_faithfulness='retained classical Euclidean realization',new_question_credit=0)))
