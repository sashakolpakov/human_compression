import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import itertools,json
from pathlib import Path
import certificate_v2 as c
P=Path(__file__).resolve().parent;G=P.parent
meta=c.read(G/'constructions_component_v1/expected/model.json');raw=c.read(G/'palette_serialization_v1/derived/group_elements.json');model=c.read(G/'palette_serialization_v1/derived/model10.json');projection=c.read(G/'palette_serialization_frozen01/fresh/source_projection.json')['representatives'][9]
orbits=c.read(P/'probe01/baer_orbits.json')['orbits'];elements=[tuple(v-1 for v in p)for p in raw['elements']];gens=[tuple(v-1 for v in p)for p in raw['generators']]
h=tuple(meta['normalizers'][0]['points']);twists=[tuple(range(21)),h,c.product(h,h)]
rows=[]
for orbit in [0]:
    geometry=c.Geometry(orbits[orbit],meta['lines'])
    for j,h in enumerate(twists):
        aut={g:c.conjugate(g,h)for g in elements};gs=[[aut[tuple(v-1 for v in g)]for g in z]for z in projection['parabolic_generators']]
        for types in itertools.permutations(range(3)):
            if [len(geometry.objects[t])for t in types]!=model['type_sizes']:continue
            fixed=[[i for i,x in enumerate(geometry.objects[t])if all(c.action(t,x,g)==x for g in z)]for t,z in zip(types,gs)]
            row=dict(orbit=orbit,twist=j,types=types,fixed_sizes=list(map(len,fixed)),candidate_checks=[])
            for base in itertools.product(*fixed):
                flag=all(geometry.adj[types[t],types[u]][base[t]]>>base[u]&1 for t,u in itertools.combinations(range(3),2));r=dict(base=base,flag=bool(flag))
                if flag:
                    images=[]
                    for t,coset in zip(model['types'],model['coset_positions']):
                        typ=types[t-1];x=geometry.objects[typ][base[t-1]];images.append(geometry.lookups[typ][c.action(typ,x,aut[elements[coset[0]-1]])])
                    try:r['passed']=c.verify_map(model,geometry,types,base,elements,aut,images,gens)
                    except Exception as e:r['error']=str(e)
                row['candidate_checks'].append(r)
            rows.append(row)
out=P/'join_diagnosis01.json'
if out.exists():raise ValueError('fresh output')
out.write_text(json.dumps(dict(model_source=model['source'],projection_source=projection['source'],group_action_lengths=list(map(len,model['group_action'])),rows=rows,new_baer_scan=False),indent=2)+'\n');print(out.read_text())
