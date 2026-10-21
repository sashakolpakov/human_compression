#!/usr/bin/env python3
"""Validation of full-space braid polynomials and free-group basis adapters."""
import json
import sympy as sp

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def word(A,B,m):
    out=sp.eye(A.rows)
    for i in range(m):out=out*(A if i%2==0 else B)
    return out.applyfunc(sp.expand)
def zero(M):return all(sp.simplify(v)==0 for v in M)

def check_reflections():
    z,u,v,r,s=sp.symbols('z u v r s')
    checked=[]
    for m in [2,3,4,5,6,8,10]:
        if m==2:
            A=sp.Matrix([[u*u,0,r],[0,1,0],[0,0,1]])
            B=sp.Matrix([[1,0,0],[0,v*v,s],[0,0,1]])
        elif m%2:
            d=-4*z*sp.cos(sp.pi/m)**2
            A=sp.Matrix([[z,1,r],[0,1,0],[0,0,1]])
            B=sp.Matrix([[1,0,0],[d,z,s],[0,0,1]])
        else:
            d=2*u*v*sp.cos(2*sp.pi/m)-u*u-v*v
            A=sp.Matrix([[u*u,1,r],[0,1,0],[0,0,1]])
            B=sp.Matrix([[1,0,0],[d,v*v,s],[0,0,1]])
        need(zero(word(A,B,m)-word(B,A,m)),'full-space symbolic braid '+str(m))
        checked.append(m)
    badA=sp.Matrix([[4,1,1],[0,1,0],[0,0,1]])
    badB=sp.Matrix([[1,0,0],[-25,9,2],[0,0,1]])
    need(not zero(badA*badB-badB*badA),'invalid k=1 shortcut must fail')
    return {'full_space_symbolic_labels':checked,'external_coordinate_couplings':'two independent symbolic variables','negative_even_label_two_rejected':True}

def reduce(w):
    result=[]
    for a in w:
        if result and result[-1]==-a:result.pop()
        else:result.append(a)
    return tuple(result)
def inv(w):return tuple(-x for x in w[::-1])
def subst(w,images):return reduce([b for x in w for b in (images[x] if x>0 else inv(images[-x]))])

def check_free():
    # Named source order a1,a2,b3,b4,c5,c6,t -> x,y,t.
    x=(1,);y=(2,);t=(3,)
    tx=reduce(inv(t)+x+t);ty=reduce(inv(t)+y+t)
    images=[{1:tx,2:ty,3:x,4:tx,5:y,6:x,7:t},
            {1:x,2:y,3:tx,4:x,5:y,6:x,7:t},
            {1:x,2:y,3:x,4:tx,5:y,6:x,7:t}]
    relators=[[(1,-4),(3,-6),(-7,5,7,-2),(-7,6,7,-1)],
              [(4,-1),(1,-6),(2,-5),(-7,6,7,-3)],
              [(1,-6),(6,-3),(2,-5),(-7,1,7,-4)]]
    for im,rels in zip(images,relators):
        for rel in rels:need(subst(rel,im)==(),'source relation under F3 map')
    need(ty!=y,'source T1 a2=c5 slip must not be accepted')
    return {'trees':3,'relators_checked':sum(map(len,relators)),'false_T1_equality_rejected':True}

if __name__=='__main__':print(json.dumps({'status':'PASS','reflections':check_reflections(),'free_group_maps':check_free()},sort_keys=True,indent=2))
