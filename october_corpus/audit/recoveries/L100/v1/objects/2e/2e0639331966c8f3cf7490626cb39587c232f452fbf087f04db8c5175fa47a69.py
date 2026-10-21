"""Small explicit canonical maps for the printed circular, affine and Petersen bonds."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json
from pathlib import Path
from construction_join import c,D,pin,need,read
W=Path(__file__).resolve().parent

def iso_small(A,B):
    need(len(A)==len(B),'small graph size')
    def search(mapping):
        if len(mapping)==len(A):return mapping
        options=[]
        for x in A:
            if x in mapping:continue
            choices=[y for y in B if y not in mapping.values() and len(A[x])==len(B[y]) and all((u in A[x])==(v in B[y])for u,v in mapping.items())]
            options.append((len(choices),x,choices))
        _,x,choices=min(options)
        for y in choices:
            q=search(mapping|{x:y})
            if q is not None:return q
        return None
    ans=search({});need(ans is not None,'literal canonical graph map')
    need(all({ans[y]for y in A[x]}==B[ans[x]]for x in A),'all small graph adjacency rows')
    return ans

def identify(vertices,types,adj,label):
    sides=[sorted(v for v in vertices if types[v]==t)for t in sorted({types[v]for v in vertices})]
    if label.startswith('C-') or label.startswith('P'):
        candidates=[(edges,points) for edges,points in [sides,sides[::-1]] if all(len(adj[v]&set(points))==2 for v in edges)]
        need(candidates,'edges have exactly two endpoints')
        for edges,points in candidates:
            pairs=[frozenset(adj[v]&set(points))for v in edges]
            if len(pairs)!=len(set(pairs)):continue
            if label.startswith('C-'):
                if set(pairs)!={frozenset(x)for x in itertools.combinations(points,2)}:continue
                pointmap={p:i for i,p in enumerate(points)}
                return dict(kind='complete_graph_incidence',points=len(points),point_images=[[p+1,pointmap[p]]for p in points],edge_images=[[v+1,sorted(pointmap[p]for p in pair)]for v,pair in zip(edges,pairs)])
            if len(points)!=10 or len(edges)!=15:continue
            graph={p:{q for pair in pairs if p in pair for q in pair if q!=p}for p in points}
            atoms=list(itertools.combinations(range(5),2));standard={i:{j for j in range(10)if set(atoms[i]).isdisjoint(atoms[j])}for i in range(10)}
            mp=iso_small(graph,standard)
            return dict(kind='Petersen_incidence',point_images=[[p+1,list(atoms[mp[p]])]for p in points],edge_images=[[v+1,sorted(mp[p]for p in pair)]for v,pair in zip(edges,pairs)])
        raise ValueError('named graph incidence does not match')
    need(label in ['Af','Af*'],'named bond')
    points,lines=sorted(sides,key=len);need(len(points)==16 and len(lines)==20,'affine order4 domains')
    pos={v:i for i,v in enumerate(points)};linepoints=[frozenset(pos[v]for v in adj[l]&set(points))for l in lines]
    need(all(len(x)==4for x in linepoints),'affine lines size4')
    pairs=[tuple(sorted(p))for line in linepoints for p in itertools.combinations(line,2)]
    need(len(pairs)==len(set(pairs))==120,'every affine point pair exactly once')
    remaining=set(range(20));parallel=[]
    while remaining:
        first=min(remaining);cls={i for i in range(20)if i==first or linepoints[i].isdisjoint(linepoints[first])}
        need(len(cls)==4 and cls<=remaining and set().union(*(linepoints[i]for i in cls))==set(range(16)),'parallel class partition')
        parallel.append(sorted(cls));remaining-=cls
    need(len(parallel)==5,'five parallel classes')
    completed=[c.mask(linepoints[i]|{16+next(k for k,cls in enumerate(parallel)if i in cls)})for i in range(20)]
    completed.append(c.mask(range(16,21)))
    frame=next(q for q in itertools.combinations(range(21),4)if all(not any(set(t)<=set(c.bits(l))for l in completed)for t in itertools.combinations(q,3)))
    pts,standard=c.coordinate_plane();standard_frame=[pts.index(v)for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]]
    mp=c.plane_map(completed,standard,dict(zip(frame,standard_frame)))
    images=[c.image(l,mp)for l in completed];need(set(images)==set(standard),'all completed projective lines')
    return dict(kind='affine_plane_F4',point_images=[[p+1,mp[i]]for i,p in enumerate(points)],
                line_images=[[v+1,images[i]]for i,v in enumerate(lines)],infinity_line=images[-1],coordinate_points=pts,
                complete_projective_map=list(mp),parallel_classes=[[lines[i]+1for i in cls]for cls in parallel])

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir()
    inventory=read(W/'diagram_inventory02.json');comparison=read(W/'diagram_comparison01.json');literal=read(W/'literal_diagrams01/diagrams.json');results=[]
    for s,j in zip(inventory['rows'],comparison['rows']):
        hit=j['candidates'][0];index=hit['catalogue_index'];mp=hit['source_node_to_catalogue_type'];m=read(D/f'model{index}.json');d=literal['records'][index-1]
        adj=[{v-1for v in row}for row in m['adjacency']];base=[v-1for v in d['base_chamber']]
        for e in s['edges']:
            label=e['printed_label']
            if not (label.startswith('C-') or label.startswith('P') or label in ['Af','Af*']):continue
            ts={mp[u]for u in e['nodes']};vertices={v for v,t in enumerate(m['types'])if t in ts and all(v in adj[base[k]]for k in range(m['rank'])if k+1not in ts)}
            q=identify(vertices,m['types'],adj,label);q.update(source_label=s['label'],catalogue_index=index,source_nodes=e['nodes'],catalogue_types=sorted(ts),printed_label=label)
            results.append(q)
    (a.out/'named_residues.json').write_text(json.dumps(dict(status='EXPLICIT_CANONICAL_RANK_TWO_RESIDUE_MAPS',records=results,
        inputs=[pin(W/'diagram_inventory02.json'),pin(W/'diagram_comparison01.json'),pin(W/'literal_diagrams01/diagrams.json')],
        qualifications=['Maps check actual circular/Petersen/affine geometries; asymmetric printed orientation is retained and can be read from each endpoint map.',
                        'General search-classification, full automorphism orders and all larger named parabolic/Borel groups are not claimed here.'],source_credit=0),indent=2)+'\n')
    print('PASS',len(results),'canonical residue maps')
if __name__=='__main__':main()
