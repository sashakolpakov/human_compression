#!/usr/bin/env python3
"""Working exact homology test for locally faithful rank-four covers."""
import argparse,itertools,json,pathlib
from fractions import Fraction

def need(ok,msg):
    if not ok:raise RuntimeError('PHASE246_REJECT '+msg)
def mul(g,h):return tuple(h[x] for x in g)
def generated(gens,degree,limit=25000):
    group=[tuple(range(degree))];index={group[0]:0}
    for g in group:
        for s in gens:
            h=mul(g,s)
            if h not in index:
                need(len(group)<limit,'group enumeration limit');index[h]=len(group);group.append(h)
    return group,index
def rank_reduce(v,rows,p):
    v={k:(Fraction(x) if p==0 else x%p) for k,x in v.items() if x}
    for k,row in sorted(rows.items()):
        a=v.get(k,0)
        if a:
            for j,x in row.items():
                val=v.get(j,0)-a*x
                if p:val%=p
                if val:v[j]=val
                else:v.pop(j,None)
    return v
def insert(v,rows,p):
    v=rank_reduce(v,rows,p)
    if not v:return False
    k=min(v);a=v[k];inv=1/a if p==0 else pow(a,-1,p)
    rows[k]={j:(x*inv if p==0 else x*inv%p) for j,x in v.items()};return True
def analyze(model,primes=(0,2,3,5,7),complex_data=False):
    degree=model['degree'];ss=[tuple(x-1 for x in s) for s in model['generators']]
    one=tuple(range(degree));need(len(ss)==4 and len(set(ss))==4 and all(sorted(s)==list(one) and mul(s,s)==one and s!=one for s in ss),'string generators')
    need(all(mul(ss[i],ss[j])==mul(ss[j],ss[i]) for i,j in [(0,2),(0,3),(1,3)]),'string commutation')
    group,index=generated(ss,degree)
    def subgroup(ids):return set(generated([ss[i] for i in ids],degree)[0])
    A=subgroup([0,1,2]);B=subgroup([1,2,3]);C=subgroup([1,2]);D=A&B
    for ids in [(0,1,2),(1,2,3)]:
        sets=[set(c) for k in range(4) for c in itertools.combinations(ids,k)]
        sub={tuple(sorted(c)):subgroup(c) for c in sets}
        need(all(sub[tuple(sorted(I))]&sub[tuple(sorted(J))]==sub[tuple(sorted(I&J))] for I in sets for J in sets),'both end intersection properties')
    # H g are the right cosets. Left multiplication inside the model below is
    # achieved by a consistent inverse convention; the four-cell word is
    # palindromically symmetric because r0 and r3 commute.
    def cosets(H):
        labels={};reps=[]
        for g in group:
            if g not in labels:
                k=len(reps);reps.append(g)
                for h in H:labels[mul(h,g)]=k
        need(len(labels)==len(group),'coset partition')
        return labels,reps
    la,ra=cosets(A);lb,rb=cosets(B);lc,rc=cosets(C)
    endpoints=[(la[g],len(ra)+lb[g]) for g in rc]
    edges=len(rc);vertices=len(ra)+len(rb)
    boundaries=[]
    for g in group:
        # Right-coset version of e_gC−e_gr0C+e_gr0r3C−e_gr3C.
        terms=[(g,1),(mul(ss[0],g),-1),(mul(mul(ss[0],ss[3]),g),1),(mul(ss[3],g),-1)]
        row={}
        for h,sign in terms:row[lc[h]]=row.get(lc[h],0)+sign
        row={e:x for e,x in row.items() if x}
        vertex_boundary={}
        for e,x in row.items():
            u,v=endpoints[e];vertex_boundary[u]=vertex_boundary.get(u,0)-x;vertex_boundary[v]=vertex_boundary.get(v,0)+x
        need(not any(vertex_boundary.values()),'square is a cellular cycle')
        boundaries.append(row)
    defects=sorted({lc[g] for g in D-C})
    need(all(endpoints[e]==endpoints[lc[one]] for e in defects),'defects are parallel edges')
    # Exact repeated rows and their negatives generate the same lattice.
    unique=set()
    for row in boundaries:
        if row:
            sign=1 if row[min(row)]>0 else -1
            unique.add(tuple(sorted((e,sign*a) for e,a in row.items())))
    elimination_rows=[dict(r) for r in sorted(unique)]
    reports=[]
    for p in primes:
        rows={}
        for v in elimination_rows:insert(v,rows,p)
        zero=[];remainders=[]
        for e in defects:
            rr=rank_reduce({e:1,lc[one]:-1},rows,p)
            if not rr:zero.append(e)
            remainders.append({str(k):str(v) for k,v in rr.items()})
        reports.append(dict(field='Q' if p==0 else p,boundary_rank=len(rows),H1_dimension=edges-vertices+1-len(rows),
                            surviving_defects=len(defects)-len(zero),killed_defects=zero,C_group=not zero,remainders=remainders))
    report=dict(name=model.get('name'),group_order=len(group),A_order=len(A),B_order=len(B),C_order=len(C),D_order=len(D),
                graph_vertices=vertices,graph_edges=edges,square_relator_rows=len(boundaries),defect_edges=defects,fields=reports)
    if complex_data:report['complex']=dict(endpoints=endpoints,boundaries=boundaries)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=pathlib.Path,required=True);ap.add_argument('--index',type=int);ap.add_argument('--out',type=pathlib.Path);a=ap.parse_args()
    model=json.loads(a.input.read_text())
    if a.index is not None:model=model[a.index]
    report=analyze(model);s=json.dumps(report,indent=2)+'\n'
    if a.out:
        need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.write_text(s)
    print(s)
