#!/usr/bin/env python3
"""Independent finite-field audit of the exact projective matrix predicates."""
import itertools,json

def need(ok,msg):
    if not ok:raise RuntimeError('PHASE241_REJECT '+msg)

def mul(a,b,p):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%p for i in range(2) for j in range(2))
def scale(c,a,p):return tuple(c*x%p for x in a)
def det(a,p):return (a[0]*a[3]-a[1]*a[2])%p
def pc(a,b,p):
    lhs=mul(a,b,p);rhs=mul(b,a,p)
    return [c for c in range(1,p) if lhs==scale(c,rhs,p)]
def scalar(a,p):return a[1]==a[2]==0 and a[0]==a[3] and a[0]!=0
def signed_scalar(a,p):
    return a[1]==a[2]==0 and a[3]!=0 and a[0] in [a[3],(-a[3])%p]

def main():
    rows=[]
    for p in [3,5,7]:
        matrices=[a for a in itertools.product(range(p),repeat=4) if det(a,p)!=0]
        semisimple=0;semihits=0;unipotent=0;unihits=0
        for l in range(1,p):
            if l*l%p==1:continue
            A=(l,0,0,1)
            for d in range(1,p):
                S=(0,d,1,0)
                for M in matrices:
                    semisimple+=1
                    if pc(M,A,p) and pc(M,S,p):
                        semihits+=1;need(signed_scalar(M,p),'semisimple conclusion')
        A=(1,1,0,1)
        for d in range(p):
            S=(p-1,d,0,1)
            for M in matrices:
                unipotent+=1
                if pc(M,A,p) and pc(M,S,p):
                    unihits+=1;need(scalar(M,p),'unipotent conclusion')
        rows.append(dict(p=p,invertible_matrices=len(matrices),semisimple_configurations=semisimple,
                         semisimple_hypothesis_hits=semihits,unipotent_configurations=unipotent,unipotent_hypothesis_hits=unihits))
    p=5;M=(0,1,1,0);A=(4,0,0,1);S=M
    need(det(M,p)!=0 and pc(M,A,p)==[4] and pc(M,S,p)==[1] and not signed_scalar(M,p),'order-two boundary counterexample')
    p=2;M=(1,1,0,1);A=M;S=(1,0,0,1)
    need(det(M,p)!=0 and pc(M,A,p)==[1] and pc(M,S,p)==[1] and not scalar(M,p),'characteristic-two boundary counterexample')
    print(json.dumps(dict(status='PASS',finite_audit=rows,
      excluded_boundary_counterexamples=[dict(field=5,l=4,d=1,M=[0,1,1,0],commutation_scalars=[4,1]),
        dict(field=2,d=0,M=[1,1,0,1],commutation_scalars=[1,1])],
      scope='Independent finite diagnostics and concrete false boundary statements, not a substitute for the general Lean proof.'),indent=2))

if __name__=='__main__':main()
