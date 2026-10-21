#!/usr/bin/env python3
"""Exact mixed-modulus cyclotomic models; emits literal GAP permutations."""
import argparse, itertools, json, math, pathlib

PARAMETERS = [(3,3),(3,4),(3,6),(5,3),(5,5),(7,3),(11,3)]

def need(ok, msg):
    if not ok:
        raise RuntimeError('PHASE236_REJECT '+msg)

def model(p, m, corrupt=False):
    d=p-1; n=m-1; e=(n-1)//d+1; r=(n-1)%d+1
    mod=[p**(e if i<r else e-1) for i in range(d)]
    def norm(v): return tuple(x%q for x,q in zip(v,mod))
    zero=norm([0]*d); one=norm([1]+[0]*(d-1))
    def add(v,w):return norm([x+y for x,y in zip(v,w)])
    def neg(v):return norm([-x for x in v])
    def act(T,v):return norm([sum(a*b for a,b in zip(row,v)) for row in T])
    def matrix(cols):return tuple(tuple(cols[j][i] for j in range(d)) for i in range(d))
    basis=[norm([int(i==j) for i in range(d)]) for j in range(d)]
    I=matrix(basis)
    def compose(T,U):return matrix([act(T,col) for col in zip(*U)])
    def power(T,k):
        out=I
        for _ in range(k):out=compose(T,out)
        return out
    pi=[[0]*d for _ in range(d)]
    for i in range(d-1):pi[i+1][i]=1
    for i in range(d):pi[i][-1]=-math.comb(p,i+1)
    if corrupt:pi[0][-1]=0
    Z=matrix([add(act(pi,v),v) for v in basis])
    def well_defined(T):
        return all((mod[j]*T[i][j])%mod[i]==0 for i in range(d) for j in range(d))
    need(well_defined(Z),'zeta respects the mixed-modulus lattice')
    need(power(Z,p)==I,'cyclotomic p-th power')
    need(Z!=I,'nonabelian action')
    Zinv=power(Z,p-1)
    barpi=matrix([add(act(Zinv,v),neg(v)) for v in basis])
    cols=[];v=one
    for _ in range(d):cols.append(v);v=act(barpi,v)
    S=matrix(cols)
    need(well_defined(S),'conjugation respects the mixed-modulus lattice')
    need(compose(S,S)==I,'conjugation square')
    need(compose(compose(S,Z),S)==Zinv,'conjugation reverses zeta')
    for v in basis:
        w=zero;u=v
        for _ in range(p):w=add(w,u);u=act(Z,u)
        need(w==zero,'cyclotomic norm zero')
    A=list(itertools.product(*(range(q) for q in mod)))
    points=[(v,k) for v in A for k in range(p)]
    idx={v:i+1 for i,v in enumerate(points)}
    need(len(points)==p**m,'normal-form cardinality')
    backwards=[act(power(Z,(-k)%p),one) for k in range(p)]
    s=[idx[(add(v,backwards[k]),k)] for v,k in points]
    beta=[idx[(v,(k+1)%p)] for v,k in points]
    sigma=[idx[(act(S,v),(-k)%p)] for v,k in points]
    tau=[idx[(neg(v),k)] for v,k in points]
    for perm in [s,beta,sigma,tau]:need(sorted(perm)==list(range(1,len(points)+1)),'literal permutation')
    return dict(p=p,m=m,e=e,r=r,moduli=mod,degree=len(points),s=s,beta=beta,sigma=sigma,tau=tau)

def emit(path, corrupt=False):
    data=[model(p,m,corrupt=corrupt) for p,m in PARAMETERS]
    rows=[]
    for row in data:
        fields=['p:='+str(row['p']),'m:='+str(row['m']),
                'moduli:='+str(row['moduli'])]
        fields += [key+':=PermList('+str(row[key])+')' for key in ['s','beta','sigma','tau']]
        rows.append('rec('+','.join(fields)+')')
    path.write_text('PHASE236_DATA := [\n'+',\n'.join(rows)+'\n];\n')
    return [{k:v for k,v in row.items() if k not in ['s','beta','sigma','tau']} for row in data]

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--corrupt-cyclotomic',action='store_true');a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh model output')
    print(json.dumps(emit(a.out,a.corrupt_cyclotomic),indent=2))
