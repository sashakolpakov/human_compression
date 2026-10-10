#!/usr/bin/env python3
"""Independent rotation/reflection model for the rank-five separated obstruction."""
import argparse
import itertools
import json
from pathlib import Path


def need(ok,msg):
    if not ok:
        raise ValueError(msg)


def multiply(x,y,quotient=False):
    a,e,b,f,t=x; c,h,d,k,u=y
    result=((a+(-1)**e*c)%4,(e+h)%2,(b+(-1)**f*d)%4,(f+k)%2,(t+u)%2)
    if quotient and result[0]>=2:
        result=(result[0]-2,result[1],(result[2]-2)%4,result[3],result[4])
    return result


def project(x):
    if x[0]<2:
        return x
    return (x[0]-2,x[1],(x[2]-2)%4,x[3],x[4])


def parabolics(marks,quotient):
    result=[]
    for mask in range(32):
        seen={(0,0,0,0,0)}; queue=list(seen)
        for x in queue:
            for i,s in enumerate(marks):
                if mask & (1<<i):
                    y=multiply(x,s,quotient)
                    if y not in seen:
                        seen.add(y); queue.append(y)
        result.append(seen)
    return result


def run():
    marks=[(0,1,0,0,0),(1,1,0,0,0),(0,0,0,0,1),(0,0,0,1,0),(0,0,1,1,0)]
    zero=(0,0,0,0,0)
    base=list(itertools.product(range(2),range(2),range(4),range(2),range(2)))
    cover=list(itertools.product(range(4),range(2),range(4),range(2),range(2)))
    pg,pr=parabolics(marks,True),parabolics(marks,False)
    need(set(base)==pg[31] and set(cover)==pr[31],'generated complete models')
    need(all(project(multiply(x,y))==multiply(project(x),project(y),True)
             for x in cover for y in cover),'quotient is homomorphism')
    need(all(project(s)==s for s in marks),'marked epimorphism')
    kernel=[x for x in cover if project(x)==zero]
    need(kernel==[zero,(2,0,2,0,0)],'diagonal central kernel')
    need(all(marks[i] not in pg[31^(1<<i)] for i in range(5)),'independence')
    need(all(multiply(s,s,True)==zero for s in marks),'involutions')
    need(all(multiply(marks[i],marks[j],True)==multiply(marks[j],marks[i],True)
             for i in range(5) for j in range(i+2,5)),'string commutations')
    for end in (15,30):
        masks=[x for x in range(32) if x&end==x]
        need(len(pg[end])==32,'end order')
        need(all(pg[i]&pg[j]==pg[i&j] for i in masks for j in masks),'end IP')
    need(all(pr[i]&pr[j]==pr[i&j] for i in range(32) for j in range(32)),'cover IP')
    central=(0,0,2,0,0)
    need(pg[3]&pg[24]=={zero,central},'common central involution')
    need(pr[3]&pr[24]=={zero},'unidentified center control')
    # Independently test the forbidden stronger inference about lifting centrality.
    # In D8, two reflections can have commuting images modulo the center without
    # commuting upstairs; this is exactly the adjacent-commutation issue.
    x=(0,1,0,0,0); y=(1,1,0,0,0)
    xy=multiply(x,y); yx=multiply(y,x)
    need(xy!=yx and xy[0]%2==yx[0]%2,'adjacent commuting quotient does not force commuting lifts')
    return {'status':'PASS','model':'D8 rotation/reflection coordinates; diagonal center normalized in left rotation',
            'base_order':64,'cover_order':128,'kernel':[list(x) for x in kernel],
            'base_parabolic_orders':[len(x) for x in pg],
            'cover_parabolic_orders':[len(x) for x in pr],
            'base_IP_failures':[[i,j,len(pg[i]&pg[j]),len(pg[i&j])] for i in range(32) for j in range(32) if pg[i]&pg[j]!=pg[i&j]],
            'cover_IP_pairs':1024,'end_IP_pairs':512,
            'separated_intersection':[list(x) for x in sorted(pg[3]&pg[24])],
            'controls':{'unidentified_centers_have_trivial_intersection':'PASS','adjacent_commutation_need_not_lift':'PASS'},
            'scope':'Finite model only; universal kernel-divisibility theorem is independently reviewed written mathematics.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output file')
    result=run()
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','base_order','cover_order','cover_IP_pairs','end_IP_pairs']}))
