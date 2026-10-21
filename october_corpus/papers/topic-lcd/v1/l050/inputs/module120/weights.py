#!/usr/bin/env python3
"""Check complete weight distributions and derive exact dual distributions."""
import argparse
import json
import math
from pathlib import Path


def need(x, message):
    if not x:
        raise ValueError(message)


def derive(record, k):
    n=120
    w=record['weight_counts']
    need(record['length']==n and record['basis_rows']==k and
         record['coefficient_vectors']==3**k, 'enumeration dimensions')
    need(len(w)==n+1 and w[0]==1 and all(isinstance(x,int) and x>=0 for x in w)
         and sum(w)==3**k, 'complete enumeration counts')
    need(all(x%2==0 for x in w[1:]),'nonzero scalar pairs')
    distance=next(i for i in range(1,n+1) if w[i])
    need(distance==48 and w[48]==1260,'complete minimum-word statement')
    dual=[]
    for j in range(n+1):
        numerator=0
        for i,a in enumerate(w):
            if not a:
                continue
            coefficient=sum((-1)**s * 2**(j-s) * math.comb(i,s) * math.comb(n-i,j-s)
                            for s in range(max(0,j-(n-i)),min(i,j)+1))
            numerator+=a*coefficient
        need(numerator>=0 and numerator%(3**k)==0,'MacWilliams coefficient')
        dual.append(numerator//(3**k))
    need(dual[0]==1 and sum(dual)==3**(n-k),'full dual count')
    dual_distance=next(i for i in range(1,n+1) if dual[i])
    need(dual_distance==4 and dual[4]=={15:2100,16:1260}[k],'dual minimum')
    return {'n':n,'k':k,'words':3**k,'d':distance,'minimum_words':w[48],
            'dual_k':n-k,'dual_d':dual_distance,'dual_minimum_words':dual[4],
            'full_weight_counts':w,'full_dual_weight_counts':dual}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--K',type=Path,required=True)
    p.add_argument('--N',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    result={'status':'PASS','K':derive(json.loads(a.K.read_text()),15),
            'N':derive(json.loads(a.N.read_text()),16),
            'retained_theorem':'classical ternary MacWilliams identity'}
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({name:{k:v for k,v in result[name].items() if not k.startswith('full_')}
                      for name in ['K','N']},sort_keys=True))


if __name__=='__main__':
    main()
