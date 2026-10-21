#!/usr/bin/env python3
"""Exact retained distributions and the shared restricted-distance interface."""
import math


def need(test,message):
    if not test:
        raise ValueError(message)


def full(record,k,source_table):
    n=105;w=record['weight_counts']
    need(record['length']==n and record['basis_rows']==k and record['coefficient_vectors']==3**k,
         'retained dimensions')
    need(len(w)==n+1 and w[0]==1 and sum(w)==3**k and all(isinstance(x,int)and x>=0 for x in w),'complete weights')
    need(w==[source_table.get(str(i),0)for i in range(n+1)],'complete printed source table')
    d=next(i for i in range(1,n+1)if w[i])
    need((d,w[d])=={20:(33,770),19:(36,3360)}[k],'main minimum parameters')
    dual=[]
    for j in range(n+1):
        num=sum(c*sum((-1)**s*2**(j-s)*math.comb(i,s)*math.comb(n-i,j-s)
                      for s in range(max(0,j-n+i),min(i,j)+1))for i,c in enumerate(w)if c)
        need(num>=0 and num%3**k==0,'MacWilliams coefficient')
        dual.append(num//3**k)
    dd=next(i for i in range(1,n+1)if dual[i])
    need(sum(dual)==3**(n-k) and (dd,dual[dd])=={20:(6,15680),19:(5,84)}[k],'dual distribution')
    return {'n':n,'dimension':k,'distance':d,'minimum_words':w[d],'dual_dimension':n-k,
            'dual_distance':dd,'dual_minimum_words':dual[dd],'full_dual_distribution':dual}


def restricted(record,candidate):
    n,k,d=105,20,candidate['distance']
    need(k*(d-1)//n==5 and k*d//n==5,'exact averaging cutoffs')
    need(record['length']==n and record['dimension_input']==k and record['prime']==3
         and record['message_weight_bound']==5,'restricted dimensions')
    expected=sum(math.comb(k,i)*2**i for i in range(6))
    counts=record['restricted_weight_counts']
    need(expected==583569 and record['messages']==expected and len(counts)==n+1
         and counts[0]==1 and sum(counts)==expected
         and all(isinstance(x,int)and x>=0 for x in counts),'complete restricted count')
    need(record['minimum_codeword_weight_over_nonzero_messages']==d and not any(counts[1:d])
         and counts[d]==candidate['restricted_minimum_count'],'restricted distance and minimum-set exhaustion')
    need(sum(x!='0'for x in record['minimum_witness'])==d,'restricted attaining word')
    return {'status':'PASS','dimension':k,'distance':d,'minimum_words':candidate['minimum_words'],
            'messages':expected,'restricted_minimum_count':counts[d],
            'theorem':'transitive information-set averaging and invariant minimum-set exhaustion',
            'full_weight_distribution_computed':False}
