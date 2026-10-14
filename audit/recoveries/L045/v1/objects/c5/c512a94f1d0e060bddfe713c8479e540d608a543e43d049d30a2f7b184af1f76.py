import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import json, math
from pathlib import Path

def need(x,m):
    if not x: raise ValueError(m)

def divisors(n):
    ds=set()
    for d in range(1,math.isqrt(n)+1):
        if n%d==0: ds.update((d,n//d))
    return sorted(ds)

rows=[]; tested=0
for q in (2,3,4,5,7,9):
    m=4; A=q**(m-1)+1; B=q+1
    expected=A if q%2==0 else A//2
    times=divisors(math.lcm(A,B))
    count=0
    for u in range(1,A):
        if math.gcd(u,A)!=1: continue
        for v in range(1,B):
            if math.gcd(v,B)!=1: continue
            def scalar(t):
                residues=(u*t%A,v*t%B)
                return residues==(0,0) or (q%2==1 and residues==(A//2,B//2))
            actual=next(t for t in times if scalar(t))
            need(actual==expected,'arbitrary primitive pair order')
            if q%2: need(v*(A//2)%B==B//2,'arbitrary primitive h half power')
            count+=1
    tested+=count;rows.append(dict(q=q,m=m,all_primitive_pairs=count,projective_order=expected))
# Composite order lemma is tested without a primality premise.
lemma=0
for q in range(2,12):
    for k in range(1,8):
        for M in divisors(q**k+1):
            if M<=2 or (M-1)**3<=q**k:continue
            r=1
            while pow(q,r,M)!=1:r+=1
            need(r==2*k,'composite modulus order lemma')
            lemma+=1
out=dict(status='PASS_INDEPENDENT_PRIMITIVE_QUANTIFIER_AND_COMPOSITE_ORDER',all_primitive_pairs=tested,rows=rows,composite_modulus_cases=lemma,scope='bounded controls; the uniform proof is reviewed separately')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
