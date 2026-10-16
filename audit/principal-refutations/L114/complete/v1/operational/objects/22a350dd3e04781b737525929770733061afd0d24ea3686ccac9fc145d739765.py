"""Independent literal reader of the one returned F8 marking; no ambient enumeration."""
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
        if a&8:a^=11
    return c

def mm(a,b):
    return tuple(sumxor(mul(a[4*i+k],b[4*k+j]) for k in range(4)) for i in range(4) for j in range(4))
def sumxor(xs):
    r=0
    for x in xs:r^=x
    return r
ID=tuple(int(i==j) for i in range(4) for j in range(4))
W=tuple(int(i+j==3) for i in range(4) for j in range(4))
def z(b):return (1,0,0,0,0,1,0,0,b,0,1,0,mul(mul(b,b),mul(b,b)),b,0,1)
def matrix(x):
    need(isinstance(x,list) and len(x)==16 and all(type(a) is int and 0<=a<8 for a in x),'F8 matrix syntax')
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

def verify(d):
    need(d['status']=='RETURNED_ONE_SAVED_SZ8_MARKING_PANELS','Returned scope')
    need(d['field']=={'degree':3,'modulus':11},'Fixed F8 field')
    # x^3+x+1 has no root in F2, so is irreducible of degree three.
    need(all((x**3+x+1)%2 for x in [0,1]),'Irreducible cubic')
    need(all(any(mul(a,b)==1 for b in range(1,8)) for a in range(1,8)),'Seven nonzero inverses')
    a,b,c=W,mm(mm(z(2),W),z(2)),z(1)
    need([matrix(x) for x in d['involutions']]==[a,b,c],'Exact retained involutions')
    need(all(x!=ID and mm(x,x)==ID for x in [a,b,c]),'Three nonidentity involutions')
    gens=[[a,b],[a,c],[b,c]]
    need([[matrix(x) for x in r] for r in d['generators']]==gens,'Exact generators')
    need(len(d['groups'])==3,'Three groups')
    G=[group(r,g,n) for r,g,n in zip(d['groups'],gens,[14,10,10])]
    need([len(G[i]&G[j]) for i,j in [(0,1),(0,2),(1,2)]]==[2,2,2],'Pair intersections')
    need(G[0]&G[1]&G[2]=={ID},'Triple intersection')
    panels=[]
    for i in range(3):
        j,k=[t for t in range(3) if t!=i]
        cosets={frozenset(mm(x,h) for h in G[i]) for x in G[j]}
        need(len(cosets)==len(G[j])//len(G[i]&G[j]),'Complete incident-coset partition')
        rows=[]
        for C in sorted(cosets,key=lambda x:sorted(x)):
            if not C&G[k]:continue
            rows.append(dict(elements=[list(x) for x in sorted(C)],intersection_with_first=[list(x) for x in sorted(C&G[j])],intersection_with_second=[list(x) for x in sorted(C&G[k])],common_representatives=[list(x) for x in sorted(C&G[j]&G[k])]))
        panels.append(dict(missing_type=i,base_types=[j,k],candidate_cosets=len(cosets),actual_panel_size=len(rows),standard_chambers=sum(bool(x['common_representatives']) for x in rows),cosets=rows))
    need(d['panels']==panels,'Exact full incidence panel records')
    need(d['ambient_group_enumerated'] is False and d['complete_group_classification_claim'] is False,'No ambient census claim')
    return dict(status='PASS_ONE_RETAINED_SZ8_MARKING',orders=[len(g) for g in G],pair_intersection_orders=[2,2,2],triple_intersection_order=1,actual_panel_sizes=[r['actual_panel_size'] for r in panels],standard_chambers=[r['standard_chambers'] for r in panels],source_refutation=False,ambient_classification='Explicit classical Suzuki matrix/maximal-subgroup premise, not verified by this finite reader')

def controls(d):
    bad=[]
    x=copy.deepcopy(d);x['field']['modulus']=13;bad.append(('field',x))
    x=copy.deepcopy(d);x['involutions'][0][0]^=1;bad.append(('marking',x))
    x=copy.deepcopy(d);x['groups'][0][0][0]^=1;bad.append(('subgroup',x))
    x=copy.deepcopy(d);x['panels'][0]['cosets'].pop();bad.append(('missing_coset',x))
    x=copy.deepcopy(d);x['panels'][1]['cosets'][0]['intersection_with_second']=[];bad.append(('false_intersection',x))
    x=copy.deepcopy(d);x['panels'][2]['standard_chambers']=3;bad.append(('false_chamber_count',x))
    rejected=[]
    for name,x in bad:
        try:verify(x)
        except ValueError:rejected.append(name)
        else:raise ValueError('Damage survived: '+name)
    return rejected
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('--controls',action='store_true');a=p.parse_args()
    d=json.loads(a.input.read_text());r=verify(d)
    if a.controls:r['rejected_damages']=controls(d)
    print(json.dumps(r,sort_keys=True))
