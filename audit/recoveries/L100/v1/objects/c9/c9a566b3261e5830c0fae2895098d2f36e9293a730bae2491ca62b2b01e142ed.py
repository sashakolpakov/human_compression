import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json
from pathlib import Path
from literal_joins import Geometry,need
class Small:
    def __init__(self,n,edges,subsets):
        self.objects=[list(range(n)),list(range(n,n+len(edges))),list(range(n+len(edges),n+len(edges)+len(subsets)))]
        self.adjsets=[set()for unused in sum(self.objects,[])];self.raw=dict(rank=3,type_sizes=list(map(len,self.objects)))
        def link(a,b):self.adjsets[a].add(b);self.adjsets[b].add(a)
        for e,pair in zip(self.objects[1],edges):
            for p in pair:link(p,e)
        for z,points in zip(self.objects[2],subsets):
            for p in points:link(p,z)
            for e,pair in zip(self.objects[1],edges):
                if set(pair)<=set(points):link(e,z)
    def incident(self,a,b):return b in self.adjsets[a]
    def act(self,a,g):return g[a]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');models=queries=flagchecks=0
    for n,edges in [(3,[(0,1),(1,2),(2,0)]),(4,[(0,1),(1,2),(2,3),(3,0)]),(3,[(0,1),(1,2)]),(5,[(0,i)for i in range(1,5)])]:
        subsets=[set(xs)for k in range(1,n+1)for xs in itertools.combinations(range(n),k)]
        m=Small(n,edges,subsets);g=Geometry(m,point=0,pair=1);models+=1
        for x,y in itertools.product(range(n),repeat=2):
            expect=x!=y and any(set(e)=={x,y}for e in edges)
            need(bool(g.adj[0,1][x]>>y&1)==expect,'independent bipartite double');queries+=1
            for j,points in enumerate(subsets):
                new=expect and x in points and y in points
                old=any(set(e)=={x,y} and set(e)<=points for e in edges)
                need(new==old,'exact full-flag correspondence');flagchecks+=1
        for i,z in enumerate(m.objects[2]):
            need(g.adj[2,0][i]==g.adj[2,1][i],'two equal copies of old point relation')
    damages=[]
    def reject(name,m):
        try:Geometry(m,point=0,pair=1)
        except ValueError:damages.append(name);return
        raise ValueError('unrejected '+name)
    reject('three_point_shadow',Small(3,[(0,1,2)],[{0,1,2}]))
    reject('duplicate_edge_shadow',Small(3,[(0,1),(1,0)],[{0,1,2}]))
    m=Small(3,[(0,1)],[{0,1}]);e=m.objects[1][0];z=m.objects[2][0];m.adjsets[e].remove(z);m.adjsets[z].remove(e);reject('wrong_pair_other_relation',m)
    a.out.mkdir(parents=True);r=dict(status='PASS_SMALL_DOUBLING_CONTROLS',models=models,independent_point_pairs=queries,full_flag_checks=flagchecks,damages=damages,target_runs=0)
    (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
