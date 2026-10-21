import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent;D=G/'palette_serialization_v1/derived'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def mul(p,q):return tuple(q[x]for x in p)
def inv(p):
    r=[0]*len(p)
    for i,j in enumerate(p):r[j]=i
    return tuple(r)
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class Ambient:
    def __init__(self,raw):
        self.elements=[tuple(x-1 for x in p)for p in raw['elements']];self.index={p:i for i,p in enumerate(self.elements)};self.generators=[tuple(x-1 for x in p)for p in raw['generators']]
        need(len(self.elements)==len(self.index)==20160,'literal acquired ambient group')
class Model:
    def __init__(self,m,A):
        self.raw=m;self.A=A;self.objects=[[a for a,t in enumerate(m['types'])if t==u]for u in range(1,m['rank']+1)]
        self.lookups=[{a:i for i,a in enumerate(xs)}for xs in self.objects]
        self.adjsets=[set(x-1 for x in row)for row in m['adjacency']]
        self.which=[]
        for t,xs in enumerate(self.objects):
            which=[None]*len(A.elements)
            for a in xs:
                for k in m['coset_positions'][a]:need(which[k-1]is None,'disjoint actual cosets');which[k-1]=a
            need(None not in which,'complete actual coset partition');self.which.append(which)
        self.reps=[A.elements[coset[0]-1]for coset in m['coset_positions']]
        need(len(m['group_action'])==len(A.generators),'complete actual generator-action arrays')
        for g,p in zip(A.generators,m['group_action']):
            need(all(self.act(a,g)==p[a]-1 for a in range(m['n'])),'actual coset action handedness/model identity')
    def act(self,a,g):return self.which[self.raw['types'][a]-1][self.A.index[mul(self.reps[a],g)]]
    def incident(self,a,b):return b in self.adjsets[a]
class Geometry:
    def __init__(self,model,types=None,point=None,pair=None):
        self.model=model;self.types=list(range(len(model.objects)))if types is None else list(types)
        self.point=point;self.pair=pair
        self.objects=[model.objects[point]if t==pair else model.objects[t]for t in self.types]
        self.lookups=[{a:i for i,a in enumerate(xs)}for xs in self.objects]
        self.shadows={};self.shadow_inverse={};self.sufficient_checks=0
        if pair is not None:
            need(point!=pair and point in self.types and pair in self.types,'distinct retained point/pair types')
            points=set(model.objects[point])
            for e in model.objects[pair]:
                shadow=frozenset(model.adjsets[e]&points);need(len(shadow)==2 and shadow not in self.shadow_inverse,'distinct two-point shadows')
                self.shadows[e]=shadow;self.shadow_inverse[shadow]=e
                for t,xs in enumerate(model.objects):
                    if t in [point,pair]:continue
                    for x in xs:
                        need(model.incident(e,x)==all(model.incident(p,x)for p in shadow),'exact concrete sufficient doubling condition');self.sufficient_checks+=1
        self.adj={}
        for i,j in itertools.combinations(range(len(self.types)),2):
            rows=[0]*len(self.objects[i]);cols=[0]*len(self.objects[j])
            for a,x in enumerate(self.objects[i]):
                for b,y in enumerate(self.objects[j]):
                    if pair is not None and {self.types[i],self.types[j]}=={point,pair}:v=frozenset([x,y])in self.shadow_inverse
                    else:v=model.incident(x,y)
                    if v:rows[a]|=1<<b;cols[b]|=1<<a
            self.adj[i,j]=rows;self.adj[j,i]=cols
    def act(self,t,a,g):return self.model.act(a,g)
def verify_map(target,geometry,A,aut,types,base,images):
    need(sorted(types)==list(range(len(geometry.types))),'type permutation')
    need(len(images)==target['n'],'complete map')
    for t in range(target['rank']):
        need(sorted(images[a]for a,u in enumerate(target['types'])if u==t+1)==list(range(len(geometry.objects[types[t]]))),'typewise bijection')
    members=0
    for a,(t,coset)in enumerate(zip(target['types'],target['coset_positions'])):
        u=types[t-1];x=geometry.objects[u][base[t-1]]
        for k in coset:
            need(geometry.lookups[u][geometry.act(u,x,aut[A.elements[k-1]])]==images[a],'every coset member');members+=1
    pairs=0
    for a,t in enumerate(target['types']):
        expected=set()
        for b,u in enumerate(target['types']):
            if u==t:continue
            pairs+=1
            if geometry.adj[types[t-1],types[u-1]][images[a]]>>images[b]&1:expected.add(b+1)
        need(expected==set(target['adjacency'][a]),'all incidence and nonincidence rows')
    action=0
    for g,p in zip(A.generators,target['group_action']):
        for a,t in enumerate(target['types']):
            u=types[t-1];x=geometry.objects[u][images[a]]
            need(geometry.lookups[u][geometry.act(u,x,aut[g])]==images[p[a]-1],'every generator-object action');action+=1
    return dict(coset_members=members,cross_type_pairs=pairs,generator_objects=action)
def attempt(target,projection,geometry,A,aut):
    sizes=list(map(len,geometry.objects))
    if sorted(sizes)!=sorted(target['type_sizes']):return None
    generators=[[aut[tuple(x-1 for x in g)]for g in gs]for gs in projection['parabolic_generators']]
    for types in itertools.permutations(range(len(sizes))):
        if [sizes[t]for t in types]!=target['type_sizes']:continue
        fixed=[[i for i,x in enumerate(geometry.objects[t])if all(geometry.act(t,x,g)==x for g in gs)]for t,gs in zip(types,generators)]
        if any(not xs for xs in fixed):continue
        for base in itertools.product(*fixed):
            if not all(geometry.adj[types[t],types[u]][base[t]]>>base[u]&1 for t,u in itertools.combinations(range(len(types)),2)):continue
            images=[]
            for t,coset in zip(target['types'],target['coset_positions']):
                u=types[t-1];x=geometry.objects[u][base[t-1]];images.append(geometry.lookups[u][geometry.act(u,x,aut[A.elements[coset[0]-1]])])
            try:checks=verify_map(target,geometry,A,aut,types,base,images)
            except ValueError:continue
            return dict(target_to_derived_types=[t+1 for t in types],base_indices=list(base),object_images=images,checks=checks)
    return None
def automorphisms(A,meta):
    identity={p:p for p in A.elements};yield 'identity',identity
    c=load_module('acquired_join',G/'source_join_component_v2/construction_join.py');dual,_=c.duality(meta,A.elements,A.generators)
    yield 'duality',dual
    d,f=[tuple(q['points'])for q in meta['normalizers']];one=tuple(range(21))
    for i in range(3):
        for j in range(2):
            if i==j==0:continue
            h=one
            for unused in range(i):h=mul(h,d)
            if j:h=mul(h,f)
            hi=inv(h);aut={p:mul(mul(hi,p),h)for p in A.elements};need(set(aut.values())==set(A.elements),'exact normalizer automorphism')
            yield f'diagonal{i}_field{j}',aut
            yield f'diagonal{i}_field{j}_duality',{p:dual[q]for p,q in aut.items()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mode',choices=['doubling','truncation'],required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();start=time.monotonic()
    A=Ambient(read(D/'group_elements.json'));meta=read(G/'constructions_component_v1/expected/model.json');projection=read(G/'palette_serialization_frozen01/fresh/source_projection.json')['representatives']
    rows=read(G/'source_join_component_v2/diagram_inventory02.json')['rows'];comparison=read(G/'source_join_component_v2/diagram_comparison01.json')['rows']
    labels={r['label']:r['candidates'][0]['catalogue_index']for r in comparison};cache={};auts=[];aut_iter=automorphisms(A,meta)
    def model(i):
        if i not in cache:cache[i]=Model(read(D/f'model{i}.json'),A)
        return cache[i]
    if a.mode=='doubling':routes=[('2.7','2.6'),('4.1','4.8'),('5.2','5.3'),('5.1','5.4')]
    else:
        routes=[]
        for r in rows:
            text=r['construction_route']
            if 'truncation' in text:
                parents=text.split('truncation',1)[1].split(';',1)[0].split('/')
                routes.extend((x,r['label'])for x in parents)
    results=[]
    for src,dst in routes:
        source=model(labels[src]);target=model(labels[dst]).raw;geometries=[]
        if a.mode=='doubling':
            for point,pair in itertools.permutations(range(source.raw['rank']),2):
                sizes=list(source.raw['type_sizes']);sizes[pair]=sizes[point]
                if sorted(sizes)!=sorted(target['type_sizes']):continue
                try:q=Geometry(source,point=point,pair=pair)
                except ValueError:continue
                geometries.append(q)
        else:
            for types in itertools.combinations(range(source.raw['rank']),target['rank']):
                if sorted(source.raw['type_sizes'][t]for t in types)==sorted(target['type_sizes']):geometries.append(Geometry(source,types=types))
        need(geometries,'literal source type/shadow candidate '+src+' ->'+dst);found=None
        for ai in range(12):
            if ai==len(auts):auts.append(next(aut_iter))
            name,aut=auts[ai]
            for geometry in geometries:
                r=attempt(target,projection[labels[dst]-1],geometry,A,aut)
                if r:
                    found=r|dict(source_label=src,target_label=dst,source_index=labels[src],target_index=labels[dst],source_types=[t+1 for t in geometry.types],point_type=None if geometry.point is None else geometry.point+1,pair_type=None if geometry.pair is None else geometry.pair+1,automorphism=name,automorphism_generator_images=[list(aut[g])for g in A.generators],two_point_shadows=len(geometry.shadows),sufficient_relation_checks=geometry.sufficient_checks);break
            if found:break
        need(found is not None,'complete positive map '+src+' ->'+dst);results.append(found);print(src,'->',dst,found['automorphism'],found['checks'],flush=True)
        (a.out/'partial.json').write_text(json.dumps(dict(mode=a.mode,complete_routes=results),indent=2)+'\n')
    report=dict(status='PASS_LITERAL_'+a.mode.upper()+'_JOINS',routes=results,seconds=time.monotonic()-start,new_ambient_censuses=0,graph_isomorphism_runs=0,source_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
if __name__=='__main__':main()
