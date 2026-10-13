"""Exact polynomial checks for a working proof; no whole-source acceptance."""
from pathlib import Path
import json
import sympy as sp

u = sp.Symbol('u', nonzero=True)
records = []

def clean(m):
    return m.applyfunc(sp.cancel)

def conj(x, y):
    return clean(y*x*y.inv())

def comm(x, y):
    return clean(x*y*x.inv()*y.inv())

def t(n, i, j, a):
    x=sp.eye(n); x[i-1,j-1]=a; return x

def product(n, entries):
    x=sp.eye(n)
    for i,j,a in entries: x=x*t(n,i,j,a)
    return clean(x)

def check(label, lhs, rhs):
    assert clean(lhs-rhs)==sp.zeros(lhs.rows), (label, clean(lhs-rhs))
    records.append(label)

def marks(n, e=1, a=u):
    A=sp.eye(n)
    negatives=[1,n] if n<=6 else [2,3,n-2,n-1]
    for i in negatives: A[i-1,i-1]=-1
    A[1,0]=A[n-2,n-1]=a
    B=sp.zeros(n)
    for i in range(n): B[n-1-i,i]=1
    C=sp.zeros(n)
    for i in range(n-1): C[n-2-i,i]=1
    C[n-1,n-1]=e
    return A,B,C

# All dimensions n>=8: eight abstract, distinct labels
# (1,2,3,4,5,n-2,n-1,n). Untouched coordinates are fixed.
for e in [1,-1]:
    n=8
    A=sp.eye(n); AE=sp.eye(n); AEE=sp.eye(n)
    for i in [2,3,6,7]: A[i-1,i-1]=-1
    for i in [3,4,7,8]: AE[i-1,i-1]=-1
    for i in [4,5,8,1]: AEE[i-1,i-1]=-1
    A[1,0]=A[6,7]=u
    AE[2,1]=u; AE[7,0]=e*u
    AEE[3,2]=u; AEE[0,1]=u
    X=comm(A,AE)
    check(f'uniform e={e}: X',X,product(n,[(3,1,-u**2),(7,1,e*u**2)]))
    Y=clean((X*AEE)**2)
    check(f'uniform e={e}: Y',Y,product(n,[(3,2,-u**3),(4,1,u**3),(4,2,-u**4),(7,2,e*u**3)]))
    # Exact E-transport on these four entries: (3,2)->(4,3),
    # (4,1)->(5,2), (4,2)->(5,3), (n-1,2)->(n,3).
    T=product(n,[(4,3,-u**3),(5,2,u**3),(5,3,-u**4),(8,3,e*u**3)])
    Z=comm(T,X)
    check(f'uniform e={e}: Z',Z,product(n,[(4,1,u**5),(5,1,u**6),(8,1,-e*u**5)]))
    R=comm(A,Z)
    check(f'uniform e={e}: R',R,t(n,7,1,-e*u**6))
    # Reversal sends (n-1,1) to (2,n), with unit weights.
    V=t(n,2,8,-e*u**6)
    check(f'uniform e={e}: W',comm(Z,V),t(n,2,1,-u**11))

A,B,C=marks(7); E=B*C
X=comm(A,conj(A,E)); T=conj((X*conj(A,E**2))**2,E)
Z=comm(T,X); R=comm(A,Z); V=conj(R,B); W=comm(Z,V)
check('n7 X',X,product(7,[(3,1,-u**2),(6,1,u**2)]))
check('n7 T',T,product(7,[(4,3,-u**3),(5,2,u**3),(5,3,-u**4),(7,3,u**3)]))
check('n7 Z',Z,product(7,[(4,1,u**5),(5,1,u**6),(7,1,-u**5)]))
check('n7 R',R,product(7,[(5,1,-2*u**6),(6,1,-u**6)]))
check('n7 V',V,product(7,[(2,7,-u**6),(3,7,-2*u**6)]))
check('n7 W',W,product(7,[(2,1,-u**11),(3,1,-2*u**11)]))
Q=comm(W,conj(W,E)); J=comm(A,Q)
check('n7 Q',Q,product(7,[(3,1,-u**22),(4,1,-2*u**22)]))
check('n7 J',J,t(7,3,1,2*u**22))
S=clean(J*Q**2)
check('n7 corrected cancellation',S,t(7,4,1,-4*u**22))
check('n7 adjacent seed',comm(conj(S,E**2),V),t(7,6,7,8*u**28))

A,B,C=marks(5); B=-B; E=B*C
X=comm(A,conj(A,E)); D=comm(A,conj(X,E))
check('n5 X',X,product(5,[(3,1,-u**2),(4,1,u**2)]))
check('n5 D',D,product(5,[(4,1,u**4-u**3),(4,2,u**3),(5,1,-u**3),(5,2,-2*u**2)]))
check('n5 D transport',conj(D,E.inv()),product(5,[(3,1,u**3),(4,1,-2*u**2),(3,5,u**4-u**3),(4,5,-u**3)]))
Y=comm(conj(X,E),conj(D,E.inv()))
check('n5 Y',Y,product(5,[(3,2,-u**6+u**5),(4,2,u**5)]))
T=conj(Y,E**3); J=comm(conj(A,E**2),T)
check('n5 T',T,product(5,[(1,5,-u**6+u**5),(2,5,u**5)]))
check('n5 J',J,product(5,[(1,5,u**6),(2,5,-2*u**5)]))
check('n5 adjacent seed',T**2*J,t(5,1,5,u**5*(2-u)))

# Normalized dimension-six construction. Scalar normalization does not
# change conjugation. Parameter u below is the paper's v.
A,B,C=marks(6,a=-1)
B=sp.diag(*([-1/u]*3+[1]*3))*B
E=B*C; h=u**2+4*u
X=comm(A,conj(A,E)); Q=comm(conj(A,E**4),X)
check('n6 X',X,product(6,[(3,1,-1),(5,1,-u)]))
check('n6 Q',Q,product(6,[(5,1,2*u),(6,1,-u**2)]))
check('n6 cancellation',comm(A,Q),t(6,5,1,-h))
check('n6 next seed',(conj(A,E**4)*t(6,5,1,h))**2,t(6,6,1,u*h))
check('n6 adjacent seed',conj(t(6,6,1,u*h),E),t(6,1,2,u*h))
D=sp.diag(1,-1,-1,1,1,1)
check('n6 isolate',comm(D,A),t(6,2,1,-2))
check('n6 opposite',conj(conj(t(6,2,1,-2),B),E**2),t(6,1,2,2*u))

# The common five-dimensional invariant subspace has ordered basis
# (e1,e2,e_(n-2),e_(n-1),en). Its complement has monomial fourth power I.
for sigma in [-1,1]:
    for epsilon in [-1,1]:
        delta=-sigma
        V=sp.zeros(5)
        V[3,0]=delta; V[2,1]=delta; V[1,2]=delta
        V[0,3]=sigma; V[1,3]=u
        V[4,4]=epsilon*sigma; V[3,4]=epsilon*u
        N=sp.zeros(5); N[1,4]=epsilon*u**2; N[2,4]=-u**2
        check(f'five-space fourth power {sigma},{epsilon}',V**4,sp.eye(5)+N)
        check(f'five-space square zero {sigma},{epsilon}',N*N,sp.zeros(5))
        for power,row,columns in [(1,1,[2,3]),(2,1,[0,1]),(-1,2,[0,1])]:
            M=clean(V**power)
            assert all(M[row,j]!=0 for j in columns)
            assert all(N[i,j]==0 for i in range(5) for j in columns)

# Rows used to prove monomial exclusion; these finite displays guide the
# generic matrix-unit proof, and are not a dimension induction.
power_rows=[]
for n,e,a in [(5,1,u),(6,1,-1),(6,-1,1),(7,1,u),(8,1,u),(9,-1,u),(10,-1,u)]:
    A,B,C=marks(n,e,a); V=A*C; N=clean(V**4-sp.eye(n))
    assert N*N==sp.zeros(n)
    entries=lambda M:[(i+1,j+1,str(M[i,j])) for i in range(n) for j in range(n) if M[i,j]!=0]
    power_rows.append({'n':n,'epsilon':e,'a':str(a),'N':entries(N),
        'V_row2':[(j+1,str(V[1,j])) for j in range(n) if V[1,j]!=0],
        'V2_row2':[(j+1,str((V**2)[1,j])) for j in range(n) if (V**2)[1,j]!=0],
        'Vinv_row_nminus2':[(j+1,str(V.inv()[n-3,j])) for j in range(n) if V.inv()[n-3,j]!=0]})
out={'status':'PASS_EXACT_POLYNOMIAL_IDENTITIES','identities':records,'uniform_basis':['1','2','3','4','5','n-2','n-1','n'],
     'uniform_dimensions':'Every n>=8; two exhaustive values epsilon=1,-1; other coordinates fixed',
     'power_displays_are_samples':True,'power_rows':power_rows,'whole_source_credit':0,'Lean_credit':0}
Path(__file__).with_name('finite_H_words_report.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'identities':len(records),'power_displays':len(power_rows)}))
