#!/usr/bin/env python3
"""Distinct checks of the new prime-rank and difference-code bridges."""
import argparse
import json
from pathlib import Path
import numpy as np

def need(condition, message):
    if not condition:
        raise ValueError(message)

def rank(matrix, p):
    a = np.array(matrix, dtype=np.int64).copy() % p
    r = 0
    for j in range(a.shape[1]):
        hits = np.flatnonzero(a[r:,j])
        if not len(hits):
            continue
        i = r + int(hits[0])
        a[[r,i]] = a[[i,r]]
        a[r] = a[r] * pow(int(a[r,j]), -1, p) % p
        a[r+1:] = (a[r+1:] - a[r+1:,j,None]*a[r]) % p
        r += 1
        if r == len(a):
            break
    return r

def run():
    polynomial = sum(1 << i for i in (0,1,5,6,7,9,11))
    blocks = []
    for m in range(4096):
        word = 0
        for i in range(12):
            if m & (1 << i):
                word ^= polynomial << i
        if word.bit_count() == 7:
            blocks.append(word)
    expected = {120:{3:21,7:119,11:99},176:{3:21,5:175,7:175,17:155},253:{2:252,3:23,5:230,7:252}}
    rank_results = {}
    A120 = H120 = None
    for t,n in ((2,120),(1,176),(0,253)):
        bs = [b for b in blocks if not b & ((1 << t)-1)]
        need(len(bs) == n, 'deleted block count')
        A = np.array([[int(x != y and (x&y).bit_count() == 3) for y in bs] for x in bs], dtype=np.int64)
        actual = {p:rank(A,p) for p in expected[n]}
        need(actual == expected[n], 'exceptional ranks')
        rank_results[n] = actual
        if n == 120:
            A120 = A
            H120 = np.array([[(b >> i)&1 for b in bs] for i in range(t,23)], dtype=np.int64)
    H,A = H120,A120
    need(np.array_equal(H@H.T % 3, np.eye(21,dtype=np.int64)), 'incidence isometry')
    need(np.array_equal(H.T@H % 3, (1-A)%3), 'incidence projector')
    S = (A[1:]-A[0]) % 3
    augmentation = (H[:-1]-H[-1]) % 3
    need(rank(S,3) == rank(augmentation,3) == rank(np.vstack((S,augmentation)),3) == 20, 'difference code equals incidence augmentation')
    need(rank(S@S.T,3) == 19 and rank(np.vstack((S,np.ones((1,120),dtype=np.int64))),3) == 20, 'one-dimensional constant hull')
    reflexive = (A+np.eye(120,dtype=np.int64))%3
    need(not np.any(S@reflexive%3) and rank(reflexive,3) == 100, 'reflexive code is exact S dual')
    complement = (np.ones((120,120),dtype=np.int64)-np.eye(120,dtype=np.int64)-A)%3
    need(rank(complement,3) == 99 and rank(np.vstack((complement,np.ones((1,120),dtype=np.int64),reflexive)),3) == 100, 'constant plus C dual equals S dual')
    cycle = np.array([[int((i-j)%4 in (1,3)) for j in range(4)] for i in range(4)],dtype=np.int64)
    comp = np.ones((4,4),dtype=np.int64)-np.eye(4,dtype=np.int64)-cycle
    need(rank(cycle,3) == rank(cycle@cycle,3) == 2 and rank(comp,3) == 4, 'C4 converse counterexample')
    return {'status':'PASS','prime_ranks':rank_results,'new_source_corrections':{'120_mod11':99,'176_mod17':155},'actual_S120_dimension':20,'actual_S120_hull_dimension':1,'S120_dual_is_reflexive_code':True,'S120_dual_is_constant_plus_C120_dual':True,'C4_converse_counterexample':True,'author_or_retained_constructor_imports':False,'105_ranks':'unchanged complete finite elimination checked in author replay; no independent repeat of accepted105 construction','enumerations':'accepted complete distributions reused, none repeated','claims':'finite interfaces only; no historical priority or full Lean claim'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    report=run()
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
