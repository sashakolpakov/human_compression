#!/usr/bin/env python3
"""Exact identities and the complete normalized deleted-S7 obstruction.

SymPy is used for rational-function identities only. Polynomial identities
have denominators powers of 2 and nonzero torus parameters, so survive in
all odd characteristics. The deleted-module calculation is independently
performed by integer row reduction modulo 7. Neither this script nor its
output certifies the retained reflection classification or the whole proof.
"""
from itertools import product, permutations
import json
import sympy as sp


def zero(M):
    return all(sp.cancel(x) == 0 for x in M)


def symbolic():
    I=sp.eye(5); checks=[]
    def eq(label,A,B):
        if any(x.has(sp.Float) for x in list(A)+list(B)): raise AssertionError('inexact coefficient '+label)
        if not zero(A-B): raise AssertionError(label)
        checks.append(label)
    t,v=sp.symbols('t v', nonzero=True)
    u,w=sp.symbols('u w')
    B=sp.zeros(5)
    B[0,2]=B[2,0]=B[1,3]=B[3,1]=B[4,4]=1
    N=sp.zeros(5);N[1,2]=1;N[0,3]=-1
    a=sp.diag(1,-1,1,-1,1)
    def M(t,u):
        R=sp.zeros(5)
        R[0,0]=R[3,3]=t;R[1,1]=R[2,2]=sp.Integer(1)/t;R[4,4]=1
        R[0,2]=-t*u*u/2;R[4,2]=u;R[0,4]=-t*u
        return R
    R=M(t,u)
    for label,A,C in [('221_form',R.T*B*R,B),('221_N',R*N,N*R),
                       ('221_a',R*a,a*R),('221_law',R*M(v,w),M(t*v,w+u/v))]:eq(label,A,C)
    eq('221_det',sp.Matrix([R.det()]),sp.Matrix([1]))
    eq('221_reverse',a*N*a,-N)
    eq('221_involution',M(-1,u)**2,I)
    E=sp.zeros(5);E[0,2]=-u*u
    eq('221_characteristic_image',(M(1,u)-I)**2,E)

    B3=sp.Matrix([[0,0,1],[0,1,0],[1,0,0]])
    N=sp.zeros(5);N[0,1]=1;N[1,2]=-1
    def M3(T,y,S,c):
        R=sp.zeros(5);R[0,0]=R[1,1]=R[2,2]=c
        R[3:5,2]=y;R[0,2]=-(y.T*S*y)[0]/(2*c)
        R[3:5,3:5]=T
        for j in range(2):R[0,3+j]=-c*(y.T*S*T[:,j])[0]
        return R
    S=sp.Matrix([[0,1],[1,0]]);B=sp.diag(B3,S)
    a=sp.diag(-1,1,-1,-1,-1)
    for tag,T,c in [('rotation',sp.diag(t,1/t),1),('reflection',sp.Matrix([[0,t],[1/t,0]]),-1)]:
        R=M3(T,sp.Matrix([u,w]),S,c)
        eq('311_general_'+tag+'_form',R.T*B*R,B)
        eq('311_general_'+tag+'_N',R*N,N*R)
        eq('311_general_'+tag+'_a',R*a,a*R)
        eq('311_general_'+tag+'_det',sp.Matrix([R.det()]),sp.Matrix([1]))
    S=sp.eye(2);B=sp.diag(B3,S);a=sp.diag(1,-1,1,1,-1)
    def affine(l,m,u):return M3(sp.diag(l,m),sp.Matrix([l*m*u,0]),S,l*m)
    for l,m in product([-1,1],repeat=2):
        R=affine(l,m,u)
        eq(f'311_affine_{l}_{m}_form',R.T*B*R,B)
        eq(f'311_affine_{l}_{m}_a',R*a,a*R)
        eq(f'311_affine_{l}_{m}_N',R*N,N*R)
        for L,M in product([-1,1],repeat=2):
            eq(f'311_law_{l}_{m}_{L}_{M}',R*affine(L,M,w),affine(l*L,m*M,u+m*w))
    E=sp.zeros(5);E[0,2]=-u*u
    eq('311_characteristic_image',(affine(1,1,u)-I)**2,E)
    # Negative-primary (3,1) plus positive line. The same formula has y
    # supported on the negative-primary residual line; the other is separate.
    a=sp.diag(1,-1,1,1,-1)
    h=sp.diag(-(sp.eye(3)+N[:3,:3]+N[:3,:3]**2/2),-1,1)
    for l,m in product([-1,1],repeat=2):
        R=affine(l,m,u)
        eq(f'negative31_{l}_{m}_h',R*h,h*R)
        eq(f'negative31_{l}_{m}_a',R*a,a*R)
    return checks


IDENT=tuple(range(7))
def mul(a,b):return tuple(a[b[i]] for i in range(7))
def inv(a):return tuple(a.index(i) for i in range(7))
def cycle(*pairs):
    a=list(IDENT)
    for i,j in pairs:a[i-1],a[j-1]=j-1,i-1
    return tuple(a)
def cj(x,g):return mul(mul(g,x),inv(g))
def commute(a,b):return mul(a,b)==mul(b,a)
def transitive(gs):
    orbit={0}; todo=[0]
    while todo:
        x=todo.pop()
        for g in gs:
            y=g[x]
            if y not in orbit:orbit.add(y);todo.append(y)
    return len(orbit)==7


def nullspace(A,p=7):
    A=[[x%p for x in row] for row in A];n=len(A[0]);r=0;piv=[]
    for c in range(n):
        j=next((j for j in range(r,len(A)) if A[j][c]),None)
        if j is None:continue
        A[r],A[j]=A[j],A[r];d=pow(A[r][c],-1,p)
        A[r]=[d*x%p for x in A[r]]
        for j in range(len(A)):
            if j!=r:
                z=A[j][c];A[j]=[(x-z*y)%p for x,y in zip(A[j],A[r])]
        piv.append(c);r+=1
        if r==len(A):break
    ans=[]
    for f in set(range(n))-set(piv):
        v=[0]*n;v[f]=1
        for row,c in enumerate(piv):v[c]=-A[row][f]%p
        ans.append(v)
    return ans


def action(g):
    # Basis [e_i-e_7], i=1..5, of T/<1>. To reduce x in T,
    # subtract x_6*1 and keep the first five coordinates.
    cols=[]
    for i in range(5):
        x=[0]*7;x[g[i]]+=1;x[g[6]]-=1
        cols.append([(x[j]-x[5])%7 for j in range(5)])
    return [[cols[j][i] for j in range(5)] for i in range(5)]


def deleted_cases():
    a,b,d=cycle((1,2)),cycle((2,3)),cycle((4,5))
    invs=[g for g in permutations(range(7)) if g!=IDENT and mul(g,g)==IDENT]
    twos=[g for g in invs if commute(g,a) and commute(g,d)]
    threes=[g for g in invs if commute(g,a) and commute(g,b) and not commute(g,d)]
    conjugators=[g for g in permutations(range(7)) if commute(g,a) and commute(g,b) and commute(g,d)]
    target3=cycle((4,6),(5,7))
    targets={(e,f):mul(mul(a if e else IDENT,d if f else IDENT),cycle((3,6))) for e,f in product([0,1],repeat=2)}
    covered=[]
    for x,y in product(twos,threes):
        if not transitive([a,b,x,y,d]):continue
        matches=[(e,f,g) for g in conjugators for (e,f),t in targets.items() if cj(y,g)==target3 and cj(x,g)==t]
        if not matches:raise AssertionError(('normalization',x,y))
        e,f,g=matches[0]
        covered.append({'s2':[j+1 for j in x],'s3':[j+1 for j in y], 'epsilon':e,'delta':f,'conjugator':[j+1 for j in g]})
    cases=[]
    for (e,f),x in sorted(targets.items()):
        spaces=[]
        for sx,sy in product([-1,1],repeat=2):
            equations=[]
            for g,sgn in [(a,1),(b,1),(x,sx),(target3,sy)]:
                A=action(g)
                equations.extend([[A[i][j]-(sgn if i==j else 0) for j in range(5)] for i in range(5)])
            basis=nullspace(equations)
            want=1 if f==0 and sx==1 and sy==-1 else 0
            if len(basis)!=want:raise AssertionError(('space',e,f,sx,sy,basis))
            if basis and basis!=[[0,0,0,0,1]]:raise AssertionError(('root57',basis))
            spaces.append({'s2_eigenvalue':sx,'s3_eigenvalue':sy,'dimension':len(basis),'basis':basis})
        cases.append({'epsilon':e,'delta':f,'spaces':spaces})
    return {'involutions':len(invs),'s2_candidates':len(twos),'s3_candidates':len(threes),
            'normalizing_conjugators':len(conjugators),'transitive_pairs':len(covered),
            'coverage':covered,'four_cases':cases}


def run():
    return {'status':'PASS','symbolic_identities':symbolic(),'deleted_S7':deleted_cases(),
            'scope':'Arithmetic support for the complete written mixed bound; no automatic theorem verification, new conjecture or whole-original credit.'}

if __name__=='__main__':print(json.dumps(run(),indent=2)+'\n',end='')
