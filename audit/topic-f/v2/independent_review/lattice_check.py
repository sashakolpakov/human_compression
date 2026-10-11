#!/usr/bin/env python3
"""Independent integer ideal-lattice diagnostic, without importing author code."""
import argparse,hashlib,json,math
from pathlib import Path
import sympy as S
from sympy.matrices.normalforms import hermite_normal_form

def need(ok,msg):
    if not ok:raise RuntimeError(msg)

def data(p):
    # Work in Z[z]/(1+z+...+z^(p-1)), independently of the author's pi basis.
    d=p-1;Z=S.zeros(d)
    for j in range(d-1):Z[j+1,j]=1
    for i in range(d):Z[i,d-1]=-1
    v=S.zeros(d,1);v[0]=1
    T=Z-S.eye(d)
    B=S.Matrix.hstack(*[T**i*v for i in range(d)])
    need(abs(B.det())==1,'integral change of basis')
    C=S.Matrix.hstack(*[Z**((-i)%p)*v for i in range(d)])
    need(C*C==S.eye(d) and C*Z*C==Z**(p-1),'exact conjugation matrices')
    need(Z**p==S.eye(d) and sum([Z**j for j in range(p)],S.zeros(d))==S.zeros(d),'exact cyclotomic identities')
    return Z,T,B,C

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args();need(not args.out.exists(),'fresh output')
    rows=[]
    for p in [3,5,7,11]:
        Z,T,B,C=data(p)
        for n in range(1,11):
            e=(n-1)//(p-1)+1;r=(n-1)%(p-1)+1
            D=S.diag(*[p**(e if i<r else e-1) for i in range(p-1)])
            actual=hermite_normal_form(T**n);expected=hermite_normal_form(B*D)
            need(actual==expected,'ideal lattice diagonal assertion')
            need(abs(actual.det())==p**n,'ideal index')
            stable=(T**n).inv()*C*(T**n)
            need(all(x.q==1 for x in stable),'conjugation ideal invariance')
            rows.append({'p':p,'n':n,'index':p**n,'moduli':list(map(int,D.diagonal())),'HNF_equal':True,'conjugation_preserves_ideal':True})
    # A missing unit on the last cyclotomic coefficient breaks the pth-power relation.
    Z,T,B,C=data(5);bad=Z.copy();bad[0,4-1]=0
    need(bad**5!=S.eye(4),'corrupt relation control')
    result={'status':'PASS','models':rows,'count':len(rows),'independence':'Integer z-basis companion matrices and Hermite normal form; no author program imported. Bounded validation only.','controls':[{'change':'delete cyclotomic constant term','status':'REJECTED'}],'sympy':S.__version__}
    args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','models':len(rows)}))
if __name__=='__main__':main()
