"""Literal polynomial fields and projective subgroups; no GAP imports."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
from pathlib import Path
from itertools import product
import argparse, json

def field(q, polynomial):
    def mul(a,b):
        c=0
        while b:
            if b&1:c^=a
            b>>=1;a<<=1
            if a&q:a^=polynomial
        return c
    M=[[mul(a,b)for b in range(q)]for a in range(q)]
    # The quotient polynomial ring has inverses for every nonzero element.
    # Hence it is a field; no irreducibility assumption is supplied as data.
    assert all(set(row)==set(range(q))for row in M[1:])
    inv=[0]+[M[a].index(1)for a in range(1,q)]
    def power(a,k):
        b=1
        while k:
            if k&1:b=M[b][a]
            a=M[a][a];k>>=1
        return b
    return M,inv,power

def run(s,m,polynomial):
    q=s**m;M,inv,power=field(q,polynomial)
    K=frozenset(x for x in range(q)if power(x,s)==x)
    assert len(K)==s
    assert all(a^b in K and M[a][b]in K for a in K for b in K)
    t=next(x for x in range(q)if x not in K)
    T=frozenset(a^M[t][b]for a in K for b in K)
    assert len(T)==s*s and K<T
    assert all(a^b in T for a in T for b in T)
    assert all(M[a][b]in T for a in K for b in T)
    def normalize(a):
        z=inv[next(x for x in a if x)]
        return tuple(M[z][x]for x in a)
    def multiply(A,B):
        a,b,c,d=A;e,f,g,h=B
        return normalize((M[a][e]^M[b][g],M[a][f]^M[b][h],
                          M[c][e]^M[d][g],M[c][f]^M[d][h]))
    one=(1,0,0,1)
    def u(x):return(1,x,0,1)
    def dilation(x):return normalize((x,0,0,1))
    def closure(gens,limit):
        seen={one};queue=[one]
        for a in queue:
            for b in gens:
                c=multiply(a,b)
                if c not in seen:seen.add(c);queue.append(c)
            assert len(seen)<=limit
        return frozenset(seen)
    hs=[u(x)for x in K]+[(0,1,1,0)]
    bs=[u(x)for x in K]+[dilation(x)for x in K if x]
    H=closure(hs,s*(s*s-1));B=closure(bs,s*(s-1))
    Q=closure(bs+[u(t)],s*s*(s-1))
    allH=frozenset(normalize(a)for a in product(K,repeat=4)
                   if M[a[0]][a[3]]!=M[a[1]][a[2]])
    allQ=frozenset(normalize((a,b,0,1))for a in K if a for b in T)
    allB=frozenset(normalize((a,b,0,1))for a in K if a for b in K)
    assert H==allH and Q==allQ and B==allB and H&Q==B
    assert (len(H),len(Q),len(B))==(s*(s*s-1),s*s*(s-1),s*(s-1))
    points=sorted(K)+[q];index={x:i for i,x in enumerate(points)}
    def transform(A,x):
        a,b,c,d=A
        numerator,denominator=(a,c)if x==q else(M[a][x]^b,M[c][x]^d)
        return q if not denominator else M[numerator][inv[denominator]]
    ha={tuple(index[transform(A,x)]for x in points)for A in H}
    cosets=sorted({tuple(sorted(k^x for k in K))for x in T})
    quotient={x:i for i,c in enumerate(cosets)for x in c}
    qa={tuple(quotient[transform(A,c[0])]for c in cosets)for A in Q}
    for A in Q:
        assert all(len({quotient[transform(A,x)]for x in c})==1 for c in cosets)
    def two_transitive(actions,d):
        assert all(sorted(a)==list(range(d))for a in actions)
        images={(a[0],a[1])for a in actions}
        return len(images)==d*(d-1)
    assert two_transitive(ha,s+1)and two_transitive(qa,s)
    assert len(ha)==len(H)and len(qa)==s*(s-1)and len(Q)//len(qa)==s
    # Enumerate subspaces, not their group or geometry isomorphism classes.
    planes={frozenset(a^M[x][b]for a in K for b in K)
            for x in range(q)if x not in K}
    assert len(planes)==(s**(m-1)-1)//(s-1)
    assert T in planes
    # A larger additive quotient is not two-transitive under K*.
    wide_cosets={frozenset(k^x for k in K)for x in range(q)}
    orbit={frozenset(k^M[a][t]for k in K)for a in K if a}
    assert len(orbit)==s-1 and len(wide_cosets)==s**(m-1)
    assert (len(orbit)==len(wide_cosets)-1)==(m==2)
    return dict(s=s,m=m,q=q,polynomial=polynomial,K=sorted(K),t=t,
                group_orders=[len(H),len(Q),len(B)],intersection_exact=True,
                local_degrees=[s+1,s],local_images=[len(ha),len(qa)],
                local_kernels=[1,s],subfield_planes=len(planes),
                ambient_quotient_two_transitive=(m==2),
                H_generators=[list(x)for x in hs],
                Q_generators=[list(x)for x in bs+[u(t)]])

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert not a.out.exists()
    models=[run(s,m,f)for s,m,f in [(4,2,19),(4,3,67),(8,2,67),(8,3,529)]]
    report=dict(status='PASS_PROJECTIVE_SUBFIELD_PLANES',models=models,
                general_proof_verified_by_program=False,
                subfield_maximality_retained_classical_theorem=True,
                ambient_group_enumerated=False,geometry_class_count_claimed=False)
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
