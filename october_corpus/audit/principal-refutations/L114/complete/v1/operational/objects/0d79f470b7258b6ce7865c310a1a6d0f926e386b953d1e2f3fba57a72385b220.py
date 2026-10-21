"""Independent literal reader of the one returned F32 marking; no ambient enumeration."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,json

def need(ok,message):
    if not ok:raise ValueError(message)

def mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        b>>=1;a<<=1
        if a&32:a^=37
    return c

def mm(a,b):
    return tuple(sumxor(mul(a[4*i+k],b[4*k+j]) for k in range(4)) for i in range(4) for j in range(4))
def sumxor(xs):
    r=0
    for x in xs:r^=x
    return r
ID=tuple(int(i==j) for i in range(4) for j in range(4))
W=tuple(int(i+j==3) for i in range(4) for j in range(4))
def z(b):
    b2=mul(b,b);b4=mul(b2,b2);b8=mul(b4,b4)
    return (1,0,0,0,0,1,0,0,b,0,1,0,b8,b,0,1)
def matrix(x):
    need(isinstance(x,list) and len(x)==16 and all(type(a) is int and 0<=a<32 for a in x),'F32 matrix syntax')
    return tuple(x)
def group(rows,gens,size):
    need(len(rows)==size,'Prescribed subgroup size')
    G={matrix(r) for r in rows};need(len(G)==size and ID in G,'Distinct group entries and identity')
    need(all(mm(a,b) in G for a in G for b in G),'Full multiplication closure')
    need(all(any(mm(a,b)==ID and mm(b,a)==ID for b in G) for a in G),'Two-sided inverses')
    H={ID};todo=[ID]
    for a in todo:
        for b in gens:
            c=mm(a,b)
            need(c in G,'Generator closure remains in returned subgroup')
            if c not in H:H.add(c);todo.append(c)
    need(H==G,'Generators produce the whole returned subgroup')
    return G

