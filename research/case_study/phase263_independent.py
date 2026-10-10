#!/usr/bin/env python3
"""Independent finite permutation checks; imports no author group code."""
import argparse, collections, itertools, json, pathlib

def need(b,s):
    if not b: raise RuntimeError('PHASE263_REJECT '+s)
def mul(a,b): return tuple(b[i] for i in a) # right action
def identity(n): return tuple(range(n))
def inv(a): return tuple(a.index(i) for i in range(len(a)))
def order(a):
    x=identity(len(a)); k=0
    while True:
        x=mul(x,a); k+=1
        if x==identity(len(a)): return k
def closure(rr,n):
    one=identity(n); seen={one}; todo=[one]
    for x in todo:
        for r in rr:
            y=mul(x,r)
            if y not in seen: seen.add(y); todo.append(y)
    return seen
def parity(a): return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2
def cycles(n,s):
    import re
    out=list(range(n))
    for block in re.findall(r'\(([^()]*)\)',s):
        cc=[int(x)-1 for x in block.split(',')]
        for x,y in zip(cc,cc[1:]+cc[:1]):out[x]=y
    return tuple(out)
def ip(rr,n):
    hs=[closure([rr[i] for i in range(len(rr)) if (m>>i)&1],n) for m in range(1<<len(rr))]
    return all(hs[a]&hs[b]==hs[a&b] for a in range(len(hs)) for b in range(len(hs)))
def local(n,even,total,types):
    ambient={x for x in itertools.permutations(range(n)) if not even or not parity(x)}
    invol=[x for x in ambient if order(x)==2]; rows=[]
    for rr in itertools.permutations(invol,3):
        if mul(rr[0],rr[2])!=mul(rr[2],rr[0]) or closure(rr,n)!=ambient:continue
        need(ip(rr,n),'all-subset IP after generation admission')
        rows.append(rr)
    need(len(rows)==total,'complete ordered string census')
    counts=collections.Counter((order(mul(r[0],r[1])),order(mul(r[1],r[2])),order(mul(mul(r[0],r[1]),r[2]))) for r in rows)
    need(dict(counts)==types,'complete type multiplicities')
    # Every listed class is already one orbit under the natural S_n conjugations.
    permutations=list(itertools.permutations(range(n))); remaining=set(rows); orbits=[]
    while remaining:
        r=next(iter(remaining)); orb={tuple(mul(mul(inv(p),x),p) for x in r) for p in permutations}
        need(orb<=set(rows),'conjugation preserves all admission conditions')
        orbits.append(len(orb));remaining-=orb
    need(sorted(orbits)==[total//3]*3,'three transitive marked type classes')
    return {'ambient':len(ambient),'involutions':len(invol),'triples':len(rows),'subset_pairs_per_triple':64,'types':[[list(k),v] for k,v in sorted(counts.items())],'orbits':sorted(orbits)}

S23=[
'(1,2)(3,24)(4,23)(5,22)(6,21)(7,20)(8,19)(9,18)(10,17)(11,16)(12,15)(13,14)',
'(1,5)(2,7)(3,21)(4,11)(6,17)(8,23)(9,13)(10,24)(12,14)(15,18)(16,19)(20,22)',
'(1,4)(2,23)(3,9)(5,13)(6,16)(7,10)(8,15)(11,21)(12,19)(14,22)(17,20)(18,24)',
'(1,10)(2,17)(3,22)(4,18)(5,24)(6,7)(8,13)(9,23)(11,15)(12,16)(14,19)(20,21)']
S13=['(3,9)(4,10)(5,11)(6,12)(7,13)(8,14)',
'(1,4)(2,14)(3,9)(5,13)(6,11)(7,12)',
'(1,2)(3,7)(4,6)(8,14)(9,13)(10,12)',
'(1,2)(4,14)(5,13)(6,12)(7,11)(8,10)']
D13='(1,3)(2,9)(4,7)(5,8)(6,12)(10,11)(13,14)'

def witness(n,strings,expected,ends,typ,mutate=False):
    r=[cycles(n,s) for s in strings]
    if mutate:
        t=cycles(n,'(1,2)');r[3]=mul(mul(t,r[3]),t)
    need(len(set(r))==4 and all(order(x)==2 for x in r),'four distinct involutions')
    need(all(mul(r[i],r[j])==mul(r[j],r[i]) for i in range(4) for j in range(i+2,4)),'actual distant commutations')
    G=closure(r,n);A=closure(r[:3],n);B=closure(r[1:],n)
    need(len(G)==expected and [len(A),len(B)]==ends,'complete group and both end closures')
    need([order(mul(r[i],r[i+1])) for i in range(3)]==typ,'adjacent orders')
    if n==24:
        need(ip(r[:3],n),'actual S4 end has IP')
        counts=collections.Counter(order(x) for x in A)
        need(dict(counts)=={1:1,2:9,3:8,4:6},'actual end element-order inventory')
    else:
        d=cycles(n,D13)
        need([mul(mul(inv(d),x),d) for x in r]==r[::-1],'actual simultaneous reversal')
        wrong=mul(d,cycles(n,'(1,2)'))
        need([mul(mul(inv(wrong),x),wrong) for x in r]!=r[::-1],'altered reversal rejected')
    return {'degree':n,'whole_order':len(G),'end_orders':[len(A),len(B)],'type':typ,'faces':[len(G)//len(B),len(G)//len(A)]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--mutate-witness',action='store_true');a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh report')
    if a.mutate_witness:
        witness(24,S23,6072,[24,6072],[3,4,12],True);raise RuntimeError('mutation unexpectedly passed')
    results={'local':[local(4,False,72,{(3,3,4):24,(3,4,3):24,(4,3,3):24}),local(5,True,360,{(3,5,5):120,(5,3,5):120,(5,5,3):120})],
    'witnesses':[witness(24,S23,6072,[24,6072],[3,4,12]),witness(14,S13,1092,[1092,1092],[3,7,3])],
    'status':'PASS','limits':['Pure Python permutation closures; projective identification also checked by the separately replayed GAP certificate.','No general all-prime theorem inferred from these finite checks.']}
    a.out.write_text(json.dumps(results,indent=2)+'\n');print('PHASE263_INDEPENDENT_PASS')
if __name__=='__main__':main()
