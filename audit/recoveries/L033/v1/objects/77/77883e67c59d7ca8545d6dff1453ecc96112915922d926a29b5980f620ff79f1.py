"""Literal dual-cell and complete small-residue controls, no author imports."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import product,combinations
import json,hashlib
W=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verts(anchor,axes):
    return frozenset(tuple(anchor[j]+(bits[axes.index(j)]if j in axes else0)for j in range(3))for bits in product([0,1],repeat=len(axes)))
def object_(kind,anchor,axes=()):return(kind,tuple(anchor),tuple(axes))
def target_inc(a,b):
    if a[0]==b[0]:return a==b
    if a[0]<2 and b[0]<2:return sum(abs(x-y)for x,y in zip(a[1],b[1]))==1
    av=verts(a[1],a[2]);bv=verts(b[1],b[2]);return av<=bv or bv<=av
def source_inc(a,b):
    if a[0]==b[0]:return a==b
    if a[0]in[0,2]and b[0]in[0,2]:return sum(abs(x-y)for x,y in zip(a[1],b[1]))==1
    av=verts(a[1],a[2]);bv=verts(b[1],b[2]);return av<=bv or bv<=av
def dual(a):
    kind,v,axes=a
    if kind in[0,2]:return object_(0 if kind==0 else1,v)
    if kind==3:return object_(3,tuple(x-1 for x in v),(0,1,2))
    i=axes[0];return object_(2,tuple(x-1+(j==i)for j,x in enumerate(v)),tuple(j for j in range(3)if j!=i))
def connected(vertices,edges):
    reached={vertices[0]};queue=[vertices[0]]
    for x in queue:
        for y in edges[x]:
            if y not in reached:reached.add(y);queue.append(y)
    return len(reached)==len(vertices)
def main():
    inputs=[pin(p)for p in [Path(__file__),W.parent/'cubic_example_v1/cubes.tex',W.parent/'cubic_example_work/source05.png']]
    source=[[]for _ in range(4)]
    for v in product(range(-1,2),repeat=3):
        kind=0 if sum(v)%2==0 else2;source[kind].append(object_(kind,v,(0,1,2)))
        source[3].append(object_(3,v))
        for i in range(3):source[1].append(object_(1,v,(i,)))
    checks=0
    for i,j in combinations(range(4),2):
        for a in source[i]:
            for b in source[j]:need(source_inc(a,b)==target_inc(dual(a),dual(b)),'literal source dual incidence');checks+=1
    target=[[]for _ in range(4)]
    for v in product(range(-1,3),repeat=3):target[sum(v)%2].append(object_(sum(v)%2,v))
    for v in product(range(-1,2),repeat=3):
        target[3].append(object_(3,v,(0,1,2)))
        for axes in combinations(range(3),2):target[2].append(object_(2,v,axes))
    base=[object_(0,(0,0,0)),object_(1,(1,0,0)),object_(2,(0,0,0),(0,1)),object_(3,(0,0,0),(0,1,2))]
    residues=[]
    for free in combinations(range(4),2):
        fixed=[base[k]for k in range(4)if k not in free]
        objs=[x for k in free for x in target[k]if all(target_inc(x,y)for y in fixed)]
        edges={x:[y for y in objs if x[0]!=y[0]and target_inc(x,y)]for x in objs}
        need(all(len(edges[x])==2 for x in objs)and connected(objs,edges),'cycle residue')
        residues.append(dict(types=list(free),vertices=len(objs)))
    need([r['vertices']for r in residues]==[4,6,4,6,4,8],'all six exact cycles')
    rank3=[]
    for fixed_type in range(4):
        objs=[x for k in range(4)if k!=fixed_type for x in target[k]if target_inc(x,base[fixed_type])]
        edges={x:[y for y in objs if x[0]!=y[0]and target_inc(x,y)]for x in objs}
        need(connected(objs,edges),'connected full rank3 residue');rank3.append(len(objs))
    need([pin(Path(r['path']))for r in inputs]==inputs,'stable inputs')
    O=W/'independent01';need(not O.exists(),'fresh output');O.mkdir();report=dict(status='PASS_INDEPENDENT_CUBIC_DUAL_AND_RESIDUES',inputs=inputs,source_object_counts=list(map(len,source)),cross_type_incidence_pairs=checks,rank2_residues=residues,rank3_residue_sizes=rank3,author_helpers_imported=False,infinite_theorem_proved_by_written_argument=True,target_census=False,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputs'}))
if __name__=='__main__':main()
