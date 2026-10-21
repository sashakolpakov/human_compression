#!/usr/bin/env python3
"""Bounded diagnostics for the new infinite panel-permutation proof.

The written syllable argument is the proof. This file tests actual reduced
words and all chosen left cyclic moves; it is not an infinite enumeration.
"""
import argparse,itertools,json
from pathlib import Path

def need(ok,message):
    if not ok: raise ValueError('L126_PANEL_REJECT '+message)

def reduce(w):
    a=[]
    for x in w:
        if a and a[-1]==-x:a.pop()
        else:a.append(x)
    return tuple(a)

def mul(a,b):return reduce(a+b)
def inv(a):return tuple(-x for x in reversed(a))
def power(i,n):return (i if n>0 else -i,)*abs(n)
def words(r,length):
    a=[()];yield ()
    for _ in range(length):
        a=[w+(x,) for w in a for x in range(-r,r+1) if x and (not w or w[-1]!=-x)]
        yield from a

def act(w,i,p,first=False):
    if not w:return w
    if first:
        if abs(w[0])!=i:return w
        end=1
        while end<len(w) and w[end]==w[0]:end+=1
        n=end*(1 if w[0]>0 else -1)
        return power(i,p.get(n,n))+w[end:]
    if abs(w[-1])!=i:return w
    start=len(w)-1
    while start and w[start-1]==w[-1]:start-=1
    n=(len(w)-start)*(1 if w[-1]>0 else -1)
    return w[:start]+power(i,p.get(n,n))

def check(first=False):
    r=3;i=1;p={1:2,2:1};q={-1:1,1:-1}
    support=set(p)|set(q)
    pq={n:p.get(q.get(n,n),q.get(n,n)) for n in support}
    total=0;panels=0
    for w in words(r,5):
        z=act(w,i,p,first)
        need(reduce(z)==z,'reduced image')
        need(act(z,i,p,first)==w,'inverse')
        need(act(act(w,i,q,first),i,p,first)==act(w,i,pq,first),'composition')
        for j in range(1,r+1):
            for n in [-2,-1,1,2]:
                h=mul(power(j,n),w)
                image_h=act(h,i,p,first)
                difference=mul(image_h,inv(z))
                need(all(abs(x)==j for x in difference),'labeled panel adjacency')
                panels+=1
        total+=1
    # The type i cosets detect the nontrivial symmetric permutation.
    need(act((i,),i,p)==(i,i),'faithfulness witness')
    return dict(status='PASS_BOUNDED_PANEL_DIAGNOSTICS',rank=r,max_word_length=5,
                reduced_words=total,panel_pairs=panels,uniform_proof=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--alter-first',action='store_true');a=p.parse_args()
    result=check(a.alter_first)
    need(not a.out.exists(),'fresh output')
    a.out.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
