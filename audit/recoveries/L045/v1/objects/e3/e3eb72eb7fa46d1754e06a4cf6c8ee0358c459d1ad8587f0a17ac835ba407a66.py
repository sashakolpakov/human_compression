#!/usr/bin/env python3
"""Independent literal binary quadratic forms; no target-group census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('optimized execution is not accepted')
import argparse
import json
from pathlib import Path
from lower_bounds import need, unitary_four_exact, symplectic_nonalt_class

def parity(n):
    return n.bit_count()%2

def qvalue(v,c,m):
    mask=(1<<m)-1
    e=v&mask;f=v>>m
    return parity(e&f)^parity(v&c)

def image(v,m,k):
    return v^((v>>m)&((1<<k)-1))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();need(not a.out.exists(),'output exists')
    rows=[];evaluations=0
    for m in range(2,5):
        for k in range(1,m+1):
            counts={1:0,-1:0};totals={1:0,-1:0}
            for c in range(1<<(2*m)):
                zeros=sum(qvalue(v,c,m)==0 for v in range(1<<(2*m)))
                sign=1 if zeros>1<<(2*m-1) else -1
                need(zeros==(1<<(2*m-1))+sign*(1<<(m-1)),'literal form sign count')
                totals[sign]+=1
                fixed=True
                for v in range(1<<(2*m)):
                    evaluations+=1
                    if qvalue(image(v,m,k),c,m)!=qvalue(v,c,m):
                        fixed=False;break
                coefficient_test=(c&((1<<k)-1))==((1<<k)-1)
                need(fixed==coefficient_test,'invariance coefficient condition')
                if fixed:
                    counts[sign]+=1
            for sign in (1,-1):
                need(totals[sign]==2**m*(2**m+sign)//2,'total quadratic-form sign mass')
                need(counts[sign]==2**(2*m-k-1),'fixed quadratic-form sign mass')
            rows.append({'m':m,'k':k,'total_forms':totals,'fixed_forms':counts})
    # Independently enumerate all permutations of six letters; Sp4(2)=S6 is
    # only an explicit small consistency control, not a retained premise.
    import itertools
    double_transpositions=0
    for perm in itertools.permutations(range(6)):
        if all(perm[perm[i]]==i for i in range(6)) and sum(perm[i]!=i for i in range(6))==4:
            double_transpositions+=1
    need(double_transpositions==symplectic_nonalt_class(2,2,2),'literal S6 class control')
    report={'status':'PASS_LITERAL_SMALL_CONTROLS','quadratic_rows':rows,'literal_queries':evaluations,'permutations':720,'double_transpositions':double_transpositions,'unitary_four_three':int(unitary_four_exact(3))}
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(rows),evaluations)

if __name__=='__main__':
    main()
