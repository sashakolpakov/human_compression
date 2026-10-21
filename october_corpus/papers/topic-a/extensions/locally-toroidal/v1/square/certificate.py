#!/usr/bin/env python3
"""Fixed exact affine certificate; no finite-period sampling."""
from collections import deque
from itertools import combinations, product as cartesian
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

D=4
I=tuple(int(i==j) for i in range(D) for j in range(D))
Z=(0,)*D
ONE=(I,Z)

def require(test,message):
    if not test: raise ValueError(message)

def mm(A,B):
    return tuple(sum(A[4*i+k]*B[4*k+j] for k in range(4)) for i in range(4) for j in range(4))

def mv(A,v):
    return tuple(sum(A[4*i+k]*v[k] for k in range(4)) for i in range(4))

def mul(x,y):
    v=mv(x[0],y[1])
    return mm(x[0],y[0]),tuple(a+b for a,b in zip(x[1],v))

def word(gs,indices):
    r=ONE
    for i in indices:r=mul(r,gs[i])
    return r

def power(x,n):
    r=ONE
    for _ in range(n):r=mul(r,x)
    return r

def integral(M):
    require(all(x.q==1 for x in M),'integral coordinates')
    return tuple(int(x) for x in M)

def basis(vectors):
    cols=sorted(set(vectors)-{Z})
    H=hermite_normal_form(sp.Matrix.hstack(*(sp.Matrix(c) for c in cols))) if cols else sp.zeros(4,0)
    return tuple(tuple(int(x) for x in H[:,j]) for j in range(H.cols))

def generators():
    B=sp.eye(4);B[:,3]=sp.ones(4,1)/2
    n=sp.Matrix([1,-1,-1,-1])
    original=[(sp.diag(-1,1,1,1),sp.Matrix([1,0,0,0])),(sp.eye(4)-n*n.T/2,sp.zeros(4,1)),(sp.diag(1,1,1,-1),sp.zeros(4,1))]
    for i,j in [(2,3),(1,2)]:
        A=sp.eye(4);A.row_swap(i,j);original.append((A,sp.zeros(4,1)))
    rho=[(integral(B.inv()*A*B),integral(B.inv()*t)) for A,t in original]
    tau=[rho[1],rho[2],mul(rho[1],rho[3]),mul(rho[0],rho[4])]
    return B,rho,tau

def fibers(gs):
    lifts={I:ONE};todo=deque([I]);raw=[]
    while todo:
        q=todo.popleft()
        for s in gs:
            h=mul(s,lifts[q]);p=h[0]
            if p not in lifts:lifts[p]=h;todo.append(p)
            raw.append((p,tuple(a-b for a,b in zip(h[1],lifts[p][1]))))
        require(len(lifts)<=1152,'finite linear bound')
    inverses={q:integral(sp.Matrix(4,4,q).inv()) for q in lifts}
    normalized={mv(inverses[p],v) for p,v in raw}
    return lifts,basis(normalized),len(raw)

def geometry(sets):
    for a,b in cartesian(range(16),repeat=2):
        require(sets[a]&sets[b]==sets[a&b],'linear intersection property')
    elements=sorted(sets[15]);lookup={x:i for i,x in enumerate(elements)}
    cosets={};bases={}
    for omit in range(4):
        P=sets[15^(1<<omit)];todo=set(elements);parts=[]
        while todo:
            g=min(todo);part={mm(h,g) for h in P}
            require(len(part)==len(P) and part<=todo,'right coset partition')
            todo-=part;parts.append(sum(1<<lookup[h] for h in part))
        cosets[omit]=parts;bases[omit]=next(c for c in parts if c>>lookup[I]&1)
    counts={}
    for k in [3,4]:
        for types in combinations(range(4),k):
            base=bases[types[0]];choices=[[p for p in cosets[t] if p&base] for t in types[1:]]
            count=0
            for rest in cartesian(*choices):
                if not all(x&y for x,y in combinations(rest,2)):continue
                count+=1;meet=base
                for c in rest:meet&=c
                require(meet,'typed coset Helly')
            counts[''.join(map(str,types))]=count
    require(counts=={'012':18,'013':18,'023':18,'123':18,'0123':36},'complete normalized flags')
    sizes=[len(cosets[t]) for t in range(4)]
    require(sizes==[32,32,24,24],'maximal coset counts')
    return dict(IP_equalities=256,coset_counts=sizes,normalized_flags=counts)

def root_action(B,gs):
    roots=[]
    for i in range(4):
        for e in [-1,1]:
            v=[0]*4;v[i]=e;roots.append(sp.Matrix(v))
    roots += [sp.Matrix(v)/2 for v in cartesian([-1,1],repeat=4)]
    for i,j in combinations(range(4),2):
        for a,b in cartesian([-1,1],repeat=2):
            v=[0]*4;v[i]=a;v[j]=b;roots.append(sp.Matrix(v))
    roots=sorted(set(tuple(B.inv()*v) for v in roots))
    require(len(roots)==48 and sp.Matrix.hstack(*(sp.Matrix(v) for v in roots)).rank()==4,'faithful root domain')
    perms=[]
    for A,t in gs:
        images=[roots.index(mv(A,v))+1 for v in roots]
        require(sorted(images)==list(range(1,49)),'root permutation')
        perms.append(images)
    return perms

def run():
    B,rho,tau=generators()
    require(all(power(x,2)==ONE and x[0]!=I for x in tau),'nonidentity involutions')
    require(word(tau,[0,2])==rho[3],'recover R3')
    require(power(word(tau,[0,3]),3)==rho[4],'recover R4')
    require(mul(tau[3],power(word(tau,[0,3]),3))==rho[0],'recover R0')
    relators=[([0,1],3),([0,2],2),([0,3],6),([1,2],6),([1,3],2),([2,3],3),([2,3,0,3,0],2),([1,0,3,0,3,0],2),([0,1,2,1,2,1],2)]
    for w,n in relators:require(power(word(tau,w),n)==ONE,'fixed affine relator')
    for i,j in combinations(range(5),2):
        n=[3,3,4,3][i] if j==i+1 else 2
        require(power(word(rho,[i,j]),n)==ONE,'ambient Coxeter relator')
    u=(1,-1,1,0);v=(0,-1,0,1);f2=(0,1,0,0);f3=(0,0,1,0)
    K=basis([u,v]);full=tuple(tuple(int(i==j) for i in range(4)) for j in range(4))
    require(abs(sp.Matrix.hstack(*(sp.Matrix(x) for x in [u,v,f2,f3])).det())==1,'direct summand')
    expected=[1,2,2,6,2,4,12,48,2,12,4,48,6,36,36,1152]
    sets={};rows=[]
    for mask in range(16):
        lifts,L,n=fibers([tau[i] for i in range(4) if mask>>i&1])
        require(len(lifts)==expected[mask],'linear parabolic order')
        require(L==(full if mask==15 else K if mask==14 else ()),'whole translation lattice')
        sets[mask]=set(lifts);rows.append(dict(mask=mask,linear_order=len(lifts),translation_basis=L,normalized_transitions=n))
    w=word(tau,[3,2,1,2,1]);z=word(tau,[3,2,1,2,1,2])
    require(power(w,2)==(I,v),'square period translation')
    require(power(z,3)==(I,u) and z[0]!=I and power((z[0],Z),3)==ONE,'residue word linear order and cube')
    e4=(0,0,0,1);ambient=power(word(rho,[0,1]+[2,3,4]*3),2)
    require(ambient==(I,e4),'ambient period')
    orbit_rows=[]
    for name,mask,x,L,size in [('new_full',15,v,full,24),('new_residue',14,v,K,6),('ambient',15,e4,full,24)]:
        orbit={mv(A,x) for A in sets[mask]}
        require(len(orbit)==size and basis(orbit)==L,'complete period orbit lattice')
        orbit_rows.append(dict(name=name,orbit=sorted(orbit),basis=L))
    perms=root_action(B,rho+tau)
    return dict(status='PASS_FIXED_AFFINE_CERTIFICATE',parabolics=rows,geometry=geometry(sets),period_orbits=orbit_rows,source_parameter_sampling=False),{'rho':perms[:5],'tau':perms[5:]}
