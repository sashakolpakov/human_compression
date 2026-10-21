import itertools
import json
from pathlib import Path

p=13
K={1,3,9,12,10,4}
def need(x,s):
    if not x: raise ValueError(s)
def norm(v): return min(((k*v[0])%p,(k*v[1])%p) for k in K)
pts=sorted({norm((a,b)) for a in range(p) for b in range(p) if a or b})
ix={v:i for i,v in enumerate(pts)}
def det(v,w): return (v[0]*w[1]-v[1]*w[0])%p
adj=[{j for j,w in enumerate(pts) if det(v,w) in K} for v in pts]
need(len(pts)==28 and {len(n) for n in adj}=={13},'graph size')
tri=[t for t in itertools.combinations(range(28),3) if all(b in adj[a] for a,b in itertools.combinations(t,2))]
counts={len(set.intersection(*(adj[i] for i in t))) for t in tri}
need(counts=={2},'all triangle completions')
quads=[t for t in itertools.combinations(range(28),4) if all(b in adj[a] for a,b in itertools.combinations(t,2))]
need(len(quads)*4==2*len(tri),'quad count')
antipodes=[]
for i in range(28):
    row=[j for j in range(28) if j!=i and j not in adj[i] and not(adj[i]&adj[j])]
    need(len(row)==1,'unique antipode')
    antipodes.append(row[0])
need(all(adj[i].isdisjoint(adj[antipodes[i]]) for i in range(28)),'antipodal neighbours')

# Paley local automorphism bound from a six-cycle and six attachment triples.
paley=[{j for j in range(13) if (i-j)%13 in K} for i in range(13)]
cycle=[1]
cycle.append(min(paley[1]&K))
while len(cycle)<6:
    nxt=(paley[cycle[-1]]&K)-{cycle[-2]}
    need(len(nxt)==1,'local cycle step')
    z=next(iter(nxt));need(z not in cycle,'local cycle closes too early');cycle.append(z)
need(cycle[0] in paley[cycle[-1]],'cycle closure')
patterns={tuple(i for i,v in enumerate(cycle) if v in paley[x]):x for x in range(1,13) if x not in K}
need(len(patterns)==6,'distinct outside patterns')
dihedral=[]
for sign in (1,-1):
 for shift in range(6):
    perm=tuple((sign*i+shift)%6 for i in range(6))
    image={tuple(sorted(perm[i] for i in t)) for t in patterns}
    if image==set(patterns):dihedral.append(perm)
need(len(dihedral)==6,'Paley point stabilizer upper bound')

def mm(a,b):return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%13 for i in range(2) for j in range(2))
I=(1,0,0,1)
def project(a):return min(a,tuple(-x%13 for x in a))
def inv(a):return project((a[3],-a[1]%13,-a[2]%13,a[0]))
def group(gens):
    out={project(I)}; todo=list(out)
    while todo:
        a=todo.pop()
        for b in gens:
            x=project(mm(a,b))
            if x not in out:out.add(x);todo.append(x)
    return out
alpha=[I,(4,0,7,10),(4,6,0,10),(3,0,0,9)]
G=group(alpha[1:]);need(len(G)==1092,'PSL group')
parts={}
for mask in range(16):
    labels=[i for i in range(4) if mask>>i&1]
    parts[mask]=group([project(mm(inv(alpha[i]),alpha[j])) for i in labels for j in labels])
for a in range(16):
 for b in range(16):need(parts[a]&parts[b]==parts[a&b],'IC-plus')
Hs=[parts[15^(1<<i)] for i in range(4)]
need([len(h) for h in Hs]==[39]*4,'parabolics')
base=[ix[norm(v)] for v in [(4,1),(1,0),(0,1),(1,1)]]
def act(a,j):
    x,y=pts[j];return ix[norm(((a[0]*x+a[1]*y)%13,(a[2]*x+a[3]*y)%13))]
need(all({a for a in G if act(a,base[i])==base[i]}==Hs[i] for i in range(4)),'literal stabilizers')
need(all(b in adj[a] for a,b in itertools.combinations(base,2)),'base chamber')
for i,j in itertools.combinations(range(4),2):
    orbit={(act(a,base[i]),act(a,base[j])) for a in G}
    need(orbit=={(u,v) for u in range(28) for v in adj[u]},'all coset incidences')

# A is the literal PSL action together with the scalar 2 involution modulo K.
actions={tuple(act(a,j) for j in range(28)) for a in G}
scalar=tuple(ix[norm((2*x%13,2*y%13))] for x,y in pts)
full=actions|{tuple(scalar[a[j]] for j in range(28)) for a in actions}
need(len(full)==2184,'actual lower automorphism bound')
need(all({f[j] for j in adj[i]}==adj[f[i]] for f in full for i in range(28)),'actual graph actions')
ordered_tri={(a,b,c) for t in tri for a,b,c in itertools.permutations(t)}
need({tuple(f[i] for i in base[:3]) for f in full}==ordered_tri,'free transitive triangle action')
chambers={tuple(t) for q in quads for t in itertools.permutations(q)}
orbit={tuple(f[i] for i in base) for f in full}
need(len(orbit)==2184 and len(chambers)==4368,'two full orbits')
other=next(iter(chambers-orbit))
need({tuple(f[i] for i in other) for f in full}==chambers-orbit,'second full orbit')
need(all(len({c for c in chambers if all(c[i]==t[i] for i in range(3))})==2 for t in [base]),'panel control')

# Actual residue at the first two base objects.
common=adj[base[0]]&adj[base[1]]
vertices={(t,v) for t in (2,3) for v in common}
remaining=set(vertices);components=[]
while remaining:
    seed=next(iter(remaining));comp={seed};queue=[seed];remaining.remove(seed)
    while queue:
        t,v=queue.pop()
        for w in common&adj[v]:
            z=(5-t,w)
            if z in remaining:remaining.remove(z);comp.add(z);queue.append(z)
    components.append(sorted(comp))
need(sorted(map(len,components))==[6,6],'disconnected actual rank-two residue')
out={'status':'PASS_EXPLICIT_L029_CANDIDATE','p':p,'K':sorted(K),'points':pts,
     'vertices':28,'degree':13,'triangles':len(tri),'K4s':len(quads),'chambers':len(chambers),
     'triple_completion_counts':sorted(counts),'alpha':alpha,'G_order':len(G),
     'parabolic_orders':[len(h) for h in Hs],'subset_intersections_checked':256,
     'base':base,'full_matrix_action_order':len(full),'full_graph_upper_bound':28*13*6,
     'paley_neighbour_cycle':cycle,'paley_outside_patterns':{str(t):x for t,x in patterns.items()},
     'paley_allowed_dihedral':dihedral,'actual_residue_components':components,
     'scope':'Explicit finite candidate and elementary automorphism-bound data; not independently reviewed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['points','actual_residue_components']}))
