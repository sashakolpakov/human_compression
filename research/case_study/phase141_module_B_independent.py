#!/usr/bin/env python3
"""Independent finite diagnostics for Module B; standard library, no author imports.

This does not prove its arbitrary-parameter theorems. All acceptance checks
remain active under python -O. The report path must be new.
"""
import argparse, collections, hashlib, itertools, json, math
from fractions import Fraction
from pathlib import Path

def require(value, message):
    if not value: raise RuntimeError(message)

def subsets(n,k):
    return [sum(1<<i for i in x) for x in itertools.combinations(range(n),k)]

def distance_checks():
    rows=[]
    for k in range(1,4):
        for n in range(2*k+1,10):
            vs=subsets(n,k);v=len(vs);neigh=[[j for j,b in enumerate(vs) if not a&b] for a in vs]
            # Every source vertex is used, not just one orbit representative.
            pairs=0;diam=0;four=False
            for start,a in enumerate(vs):
                dist=[-1]*(2*v);dist[start]=0;q=collections.deque([start])
                while q:
                    t=q.popleft();part=t//v
                    for j in neigh[t%v]:
                        w=j+(1-part)*v
                        if dist[w]<0:dist[w]=dist[t]+1;q.append(w)
                require(min(dist)>=0,'bipartite double disconnected')
                for j,b in enumerate(vs):
                    c=(a&b).bit_count();s=n-2*k
                    require(dist[j]==2*((k-c+s-1)//s),'even distance')
                    require(dist[j+v]==2*((c+s-1)//s)+1,'odd distance')
                    common=len(set(neigh[start])&set(neigh[j]))
                    expected=math.comb(n-2*k+c,k) if n-2*k+c>=k else 0
                    require(common==expected,'common-neighbor count')
                    if start!=j and common>=2:four=True
                    pairs+=2
                diam=max(diam,max(dist))
            require(diam==2*((k+n-2*k-1)//(n-2*k))+1,'diameter')
            require(four==(n>=2*k+2),'four-cycle/thickness boundary')
            rows.append({'n':n,'k':k,'vertices':2*v,'ordered_parity_distance_pairs':pairs,'diameter':diam,'has_four_cycle':four,'panel_size':math.comb(n-k,k)})
    require(next(r for r in rows if r['n']==3 and r['k']==1)['panel_size']==2,'thin boundary')
    require(all(r['panel_size']>=3 for r in rows if (r['n'],r['k'])!=(3,1)),'other panels thick')
    return rows

def exact_rank(matrix):
    a=[[Fraction(x) for x in row] for row in matrix];rank=0
    for col in range(len(a[0])):
        pivot=next((i for i in range(rank,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        lead=a[rank][col];a[rank]=[x/lead for x in a[rank]]
        for i in range(rank+1,len(a)):
            c=a[i][col]
            if c:a[i]=[x-c*y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank

def graph63():
    sets=subsets(7,2);vertices=list(itertools.product(range(3),sets));n=len(vertices)
    a=[[int(i!=j and not x&y) for j,y in vertices] for i,x in vertices]
    require(n==63 and all(sum(r)==20 for r in a),'graph63 valency')
    dims={}
    for lam,mult in [(20,1),(-10,2),(-8,6),(4,12),(2,14),(-1,28)]:
        rank=exact_rank([[a[i][j]-lam*(i==j) for j in range(n)] for i in range(n)])
        require(n-rank==mult,'wrong exact eigenspace dimension')
        dims[str(lam)]=mult
    require(sum(dims.values())==n,'incomplete eigenbasis')
    for other in [1,2]:
        z=[int(i==0)-int(i==other) for i,_ in vertices]
        require(all(sum(a[i][j]*z[j] for j in range(n))==-10*z[i] for i in range(n)),'type-difference eigenvector')
    # Every vertex link is checked against the literal two-copy KG(5,2) model.
    links=[]
    for ix,(i,x) in enumerate(vertices):
        ns=[j for j in range(n) if a[ix][j]]
        require(len(ns)==20,'link order')
        require(all(sum(a[j][k] for k in ns)==3 for j in ns),'link degree')
        require(all((vertices[j][1]&x)==0 and vertices[j][0]!=i for j in ns),'link support')
        links.append(len(ns))
    return {'vertices':n,'degree':20,'exact_rational_eigenspace_dimensions':dims,'least_eigenspace':'two independent type-difference vectors, eigenvalue -10','links_checked':len(links),'link_order':20,'link_degree':3,'full_automorphism_order_from_reviewed_reconstruction_proof':math.factorial(7)*math.factorial(3),'claim_limit':'The computation verifies the matrix spectrum and link model. The full graph group follows from the independently reviewed maximum-independent-set and Johnson reconstruction proof, not an automorphism census.'}

def forest_checks():
    models=[([1,2,1],[(0,1),(1,2)]),([1,1,1,2],[(0,1),(1,2),(1,3)]),([1,1,2,2],[(0,1),(1,2),(2,3)])]
    rows=[]
    for weights,edges in models:
        n=sum(weights);r=len(edges);blocks=[];start=0
        for w in weights:blocks.append(set(range(start,start+w)));start+=w
        perms=list(itertools.permutations(range(n)))
        def image(p,a):return frozenset(p[x] for x in a)
        components=[];groups=[]
        for mask in range(1<<r):
            cs=[{i} for i in range(len(weights))]
            for j,(u,v) in enumerate(edges):
                if mask>>j&1:
                    cu=next(c for c in cs if u in c);cv=next(c for c in cs if v in c)
                    if cu!=cv:cs.remove(cu);cs.remove(cv);cs.append(cu|cv)
            parts=[frozenset().union(*(blocks[i] for i in c)) for c in cs]
            components.append(parts);groups.append({p for p in perms if all(image(p,a)==a for a in parts)})
        for a in range(1<<r):
            for c in range(1<<r):require(groups[a]&groups[c]==groups[a&c],'forest group intersection')
        cuts=[]
        for j in range(r):cuts.append(next(c for c in components[((1<<r)-1)^(1<<j)] if 0 not in c))
        domains=[list({image(p,c) for p in perms}) for c in cuts]
        flags=0
        for mask in range(1<<r):
            inds=[i for i in range(r) if mask>>i&1]
            actual={tuple(image(p,cuts[i]) for i in inds) for p in perms}
            pairwise=set()
            for xs in itertools.product(*(domains[i] for i in inds)):
                if all(len(xs[a]&xs[c])==len(cuts[inds[a]]&cuts[inds[c]]) for a in range(len(inds)) for c in range(a)):
                    pairwise.add(xs)
            require(pairwise==actual,'flag completion')
            flags+=len(actual)
        rows.append({'weights':weights,'edges':edges,'points':n,'permutations_enumerated':len(perms),'ordered_subgroup_pairs':4**r,'all_partial_flags_checked':flags})
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    if a.output.exists():raise SystemExit('Refusing existing output')
    result={'status':'PASS_bounded_independent_diagnostics','method':'Python standard library; newly written bitset graph/BFS, exact Fraction row reduction and full small permutation enumeration; no imports of author code or reports.','distances':distance_checks(),'graph63':graph63(),'weighted_forests':forest_checks(),'uniform_claim':'The arbitrary-parameter results are certified here by separate written mathematical review, not extrapolation from these finite checks.'}
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':result['status'],'distance_models':len(result['distances']),'distance_pairs':sum(x['ordered_parity_distance_pairs'] for x in result['distances']),'forest_pairs':sum(x['ordered_subgroup_pairs'] for x in result['weighted_forests']),'partial_flags':sum(x['all_partial_flags_checked'] for x in result['weighted_forests']),'graph63_eigen_dimensions':result['graph63']['exact_rational_eigenspace_dimensions']}))
if __name__=='__main__':main()
