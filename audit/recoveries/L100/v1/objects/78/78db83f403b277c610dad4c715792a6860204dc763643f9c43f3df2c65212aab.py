"""Independent field maps and all 24 saved incidence isomorphisms."""
import argparse
import itertools as it
import json
from pathlib import Path
import independent as v

p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True)
p.add_argument('--out',type=Path,required=True);a=p.parse_args()
v.require(not a.out.exists(),'fresh output')
data=json.loads((a.packet/'expected/model.json').read_text())
points=[tuple(x) for x in data['coordinate_points']]
labels=data['coordinate_to_retained']; inverse={x:i for i,x in enumerate(labels)}
point_index={x:i for i,x in enumerate(points)}
transforms=(lambda x:(v.MULT[2][x[0]],x[1],x[2]),
            lambda x:tuple(v.MULT[y][y] for y in x))
orbits=[list(map(v.members,o)) for o in data['hyperoval_orbits']]
maps=[]; induced=[]
for k,transform in enumerate(transforms):
    m=tuple(labels[point_index[v.normal(transform(points[inverse[i]]))]] for i in range(21))
    v.require(list(m)==data['normalizers'][k]['points'],'literal coordinate normalizer')
    orbit_map=[]
    for source in orbits:
        image={frozenset(m[x] for x in h) for h in source}
        targets=[j for j,target in enumerate(orbits) if image==set(target)]
        v.require(len(targets)==1,'entire hyperoval orbit image');orbit_map.append(targets[0])
    v.require(orbit_map==data['normalizers'][k]['hyperoval_orbits'],'all orbit images')
    maps.append(m);induced.append(tuple(orbit_map))
seen={(0,1,2)};queue=list(seen)
for x in queue:
    for g in induced:
        y=tuple(g[z] for z in x)
        if y not in seen:seen.add(y);queue.append(y)
v.require(len(queue)==6,'all six ordered orbit choices')
def objects(choice):
    return [list(map(v.members,data['lines'])),[frozenset([i]) for i in range(21)],
            orbits[choice[0]],orbits[choice[1]],
            [frozenset(s) for s in it.combinations(range(21),2)]]
rows=json.loads((a.packet/'expected/choice_maps.json').read_text());tests=0
v.require(len(rows)==24,'exact complete map list')
keys={(r['variant'],tuple(r['source_choice']),r['normalizer']) for r in rows}
v.require(keys=={(variant,choice,k) for variant in ['5.1','5.2']
    for choice in it.permutations(range(3),2) for k in range(2)},'all map indices')
for row in rows:
    point_map=maps[row['normalizer']]
    v.require(row['target_choice']==[induced[row['normalizer']][j] for j in row['source_choice']],
              'actual ordered target choice')
    source=objects(row['source_choice']);target=objects(row['target_choice']);actual=[]
    for domain,codomain in zip(source,target):
        lookup={x:i for i,x in enumerate(codomain)}
        action=[lookup[frozenset(point_map[i] for i in x)] for x in domain]
        v.require(sorted(action)==list(range(len(domain))),'all object bijections');actual.append(action)
    v.require(actual==row['object_maps'],'every saved literal object map')
    count=0
    for i,j in it.combinations(range(5),2):
        for x,s in enumerate(source[i]):
            for y,t in enumerate(source[j]):
                v.require(v.incident(i,s,j,t,row['variant'])==v.incident(
                    i,target[i][actual[i][x]],j,target[j][actual[j][y]],row['variant']),
                    'every incidence and nonincidence')
                count+=1
    v.require(count==row['pair_tests'],'reported pair coverage');tests+=count
result=dict(status='PASS_INDEPENDENT_NORMALIZER_MAPS',maps=len(rows),
            incidence_pairs=tests,hyperoval_orbit_maps=induced,ordered_choices=len(queue),
            normalization_proof='Conjugation by an invertible diagonal matrix preserves determinant-one matrices; field Frobenius preserves determinant one. The literal point permutations and all orbit/object maps are checked here.',
            whole_source_credit=0)
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
