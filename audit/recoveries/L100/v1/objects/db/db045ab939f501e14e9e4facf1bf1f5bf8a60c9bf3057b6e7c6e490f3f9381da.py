"""Read-only literal equivariant joins; no group or graph-isomorphism search."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse, hashlib, importlib.util, itertools, json
from pathlib import Path

G=Path(__file__).resolve().parent.parent
C=G/'constructions_component_v1'
D=G/'palette_serialization_v1/derived'
P=G/'palette_serialization_frozen01/fresh/source_projection.json'
def read(p): return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def need(v,s):
    if not v: raise ValueError(s)
spec=importlib.util.spec_from_file_location('acquired_constructions',C/'constructions.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def attempt(model, projection, geometry, types, elements, automorphism):
    """Find base objects fixed by each actual parabolic, then check every row."""
    sizes=[len(geometry.objects[t]) for t in types]
    if sorted(model['type_sizes'])!=sorted(sizes):return None
    generators=[[automorphism[tuple(v-1 for v in p)] for p in gs] for gs in projection['parabolic_generators']]
    for ts in itertools.permutations(types):
        if [len(geometry.objects[t]) for t in ts]!=model['type_sizes']:continue
        fixed=[]
        for t,gs in zip(ts,generators):
            fixed.append([i for i,x in enumerate(geometry.objects[t]) if all(c.image(x,g)==x for g in gs)])
        if any(not x for x in fixed):continue
        for base in itertools.product(*fixed):
            if not all((geometry.adj[ts[i],ts[j]][base[i]]>>base[j])&1 for i,j in itertools.combinations(range(len(ts)),2)):continue
            images=[]
            for t,coset in zip(model['types'],model['coset_positions']):
                st=ts[t-1];x=geometry.objects[st][base[t-1]]
                images.append(geometry.lookups[st][c.image(x,elements[coset[0]-1])])
            by_type={t:{a:i for a,(u,i) in enumerate(zip(model['types'],images)) if u==t} for t in range(1,len(ts)+1)}
            if any(sorted(v.values())!=list(range(len(geometry.objects[ts[t-1]]))) for t,v in by_type.items()):continue
            correct=True
            for a,(t,i) in enumerate(zip(model['types'],images)):
                actual={b-1 for b in model['adjacency'][a]}
                expected={b for u,rows in by_type.items() if u!=t for b,j in rows.items() if (geometry.adj[ts[t-1],ts[u-1]][i]>>j)&1}
                if actual!=expected:correct=False;break
            if not correct:continue
            # Explicit all-member well-definedness, beyond generator-based proof.
            members=0
            for a,(t,coset) in enumerate(zip(model['types'],model['coset_positions'])):
                st=ts[t-1];x=geometry.objects[st][base[t-1]]
                need(all(geometry.lookups[st][c.image(x,elements[k-1])]==images[a] for k in coset),'all coset members same object')
                members+=len(coset)
            return dict(catalogue_to_construction_types=[t+1 for t in ts],base_object_indices=list(base),
                        base_object_masks=[geometry.objects[t][b] for t,b in zip(ts,base)],
                        object_images=images,checked_coset_members=members,checked_incidence_rows=model['n'])
    return None

def duality(metadata,elements,group_generators):
    points=metadata['coordinate_points'];labels=metadata['coordinate_to_retained']
    dual_lines={}
    for i,a in enumerate(points):
        line=c.mask(labels[j] for j,v in enumerate(points) if c.fs(c.fm(x,y) for x,y in zip(a,v))==0)
        dual_lines[line]=labels[i]
    need(set(dual_lines)==set(metadata['lines']),'complete literal dual coordinate correspondence')
    def dual(p):
        q=[None]*21
        for line,i in dual_lines.items():q[i]=dual_lines[c.image(line,p)]
        return tuple(q)
    mapping={tuple(p):dual(p) for p in elements};domain=set(mapping)
    need(set(mapping.values())==domain,'duality maps the exact group bijectively to itself')
    for p in elements:
        for g in group_generators:
            need(mapping[c.mul(p,g)]==c.mul(mapping[tuple(p)],mapping[tuple(g)]),'every Cayley edge verifies dual automorphism')
    return mapping,dict(line_to_dual_point=[[x,y] for x,y in sorted(dual_lines.items())],
                        generator_images=[list(mapping[tuple(g)]) for g in group_generators],
                        all_elements=len(elements),all_generator_edges=len(elements)*len(group_generators))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir()
    metadata=read(C/'expected/model.json');group=read(D/'group_elements.json')
    need(set(c.closure([tuple(p) for p in metadata['retained_generators']],21))=={tuple(v-1 for v in p) for p in group['elements']},'exact equality of constructed and census permutation groups')
    elements=[tuple(v-1 for v in p) for p in group['elements']];projection=read(P)['representatives']
    dual,dual_evidence=duality(metadata,elements,[tuple(v-1 for v in p) for p in group['generators']])
    twists=[('identity',{p:p for p in elements}),('duality',dual)]
    routes=[('5.1','5.1',(0,1,2,3,4)),('5.2','5.2',(0,1,2,3,4))]
    for q in read(C/'expected/truncations.json'):
        routes.append((q['source_label'],q['model'],tuple(t-1 for t in q['retained_types'])))
    results=[];inputs=[pin(C/'constructions.py'),pin(C/'expected/model.json'),pin(C/'expected/truncations.json'),pin(D/'group_elements.json'),pin(P)]
    models={i:read(D/f'model{i}.json') for i in range(1,30)}
    inputs += [pin(D/f'model{i}.json') for i in range(1,30)]
    for label,variant,types in routes:
        found=[]
        for twist,aut in twists:
            transformed=[aut[p] for p in elements]
            for choice in itertools.permutations(range(3),2):
                geometry=c.Geometry(metadata,variant,choice)
                for i,model in models.items():
                    if model['rank']!=len(types):continue
                    q=attempt(model,projection[i-1],geometry,types,transformed,aut)
                    if q:
                        q.update(source_label=label,model=variant,retained_types=[t+1 for t in types],choice=list(choice),catalogue_index=i,source=model['source'],group_automorphism=twist)
                        found.append(q)
                if found:break
            if found:break
        need(len(found)==1,f'unique actual construction class {label}/{variant}: {[q["catalogue_index"] for q in found]}')
        results.append(found[0]);print(label,variant,found[0]['catalogue_index'],flush=True)
    (a.out/'joins.json').write_text(json.dumps(dict(status='LITERAL_CONSTRUCTION_JOINS',routes=results,duality=dual_evidence,inputs=inputs,graph_runs=0,target_censuses=0,source_credit=0),indent=2)+'\n')

if __name__=='__main__':main()
