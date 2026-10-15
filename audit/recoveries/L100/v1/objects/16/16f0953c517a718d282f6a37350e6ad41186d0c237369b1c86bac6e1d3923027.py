"""Complete finite Baer input and literal source Geometry 3.3 joins.

No GAP, automorphism-group search, graph-isomorphism routine or subgroup
enumeration is called. The accepted 21-point action is used literally.
"""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def need(x,s):
    if not x:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def mask(points):return sum(1<<x for x in points)
def bits(x):
    while x:
        y=x&-x;yield y.bit_length()-1;x-=y
def image(x,p):return mask(p[t]for t in bits(x))
def product(p,q):return tuple(q[x]for x in p)
def inverse(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def conjugate(g,p):return product(product(inverse(p),g),p)
def action(t,x,p):
    if t==1:return tuple(sorted(image(line,p)for line in x))
    return image(x,p)

def baer_input(lines,generators):
    complete=[];tested=0
    for seven in itertools.combinations(range(21),7):
        tested+=1;b=mask(seven)
        if all((b&l).bit_count()in[1,3]for l in lines):complete.append(b)
    remaining=set(complete);orbits=[]
    while remaining:
        seed=min(remaining);found={seed};queue=[seed]
        for b in queue:
            for g in generators:
                x=image(b,g);need(x in remaining,'orbit remains in complete unsorted input')
                if x not in found:found.add(x);queue.append(x)
        orbits.append(sorted(found));remaining-=found
    need(len(complete)==len(set(complete)) and sorted(x for o in orbits for x in o)==sorted(complete),'exact exhaustive orbit partition')
    for b in complete:
        triples=[b&l for l in lines if (b&l).bit_count()==3]
        need(len(triples)==len(set(triples))==7,'seven actual Fano lines')
        need(all(sum((t>>p)&1 for t in triples)==3 for p in bits(b)),'three Fano lines through each point')
        need(all((u&v).bit_count()==1 for u,v in itertools.combinations(triples,2)),'Fano line intersections')
    return orbits,dict(seven_subsets_tested=tested,subplanes=len(complete),orbit_sizes=list(map(len,orbits)),fano_lines_checked=7*len(complete))

class Geometry:
    def __init__(self,orbit,lines,corrected=False):
        self.objects=[orbit,list(itertools.combinations(sorted(lines),2)),sorted(mask(p)for p in itertools.combinations(range(21),2))]
        self.lookups=[{x:i for i,x in enumerate(xs)}for xs in self.objects]
        self.join={p:next(l for l in lines if p&l==p)for p in self.objects[2]}
        need(all(sum(p&l==p for l in lines)==1 for p in self.objects[2]),'every point pair has one literal line')
        self.adj={};self.pairs_checked=0
        for t,u in itertools.combinations(range(3),2):
            rows=[0]*len(self.objects[t]);columns=[0]*len(self.objects[u])
            for i,x in enumerate(self.objects[t]):
                for j,y in enumerate(self.objects[u]):
                    self.pairs_checked+=1
                    incident=self.incident(t,x,u,y)
                    if corrected and (t,u)==(1,2):incident=incident and bool(self.adj[1,0][i]&self.adj[2,0][j])
                    if incident:rows[i]|=1<<j;columns[j]|=1<<i
            self.adj[t,u]=rows;self.adj[u,t]=columns
    def incident(self,t,x,u,y):
        if t>u:return self.incident(u,y,t,x)
        if (t,u)==(0,1):
            l1,l2=y;return (x&(l1|l2))==(l1&l2)
        if (t,u)==(0,2):return x&y==0 and (x&self.join[y]).bit_count()==3
        if (t,u)==(1,2):
            l1,l2=x;return (l1|l2)&y==0 and bool(l1&l2&self.join[y])
        raise ValueError('different actual types required')

def verify_map(model,geometry,types,base,elements,aut,images,group_generators):
    sizes=[len(geometry.objects[t])for t in types]
    need(sizes==model['type_sizes'],'mapped type sizes')
    need(len(images)==model['n'],'complete object map')
    for t,size in enumerate(sizes,1):
        need(sorted(images[a]for a,u in enumerate(model['types'])if u==t)==list(range(size)),'typewise bijection')
    members=0
    for a,(t,coset)in enumerate(zip(model['types'],model['coset_positions'])):
        typ=types[t-1];x=geometry.objects[typ][base[t-1]]
        for k in coset:
            need(geometry.lookups[typ][action(typ,x,aut[elements[k-1]])]==images[a],'all coset members give same object');members+=1
    checks=0
    for a,t in enumerate(model['types']):
        actual=set(x-1 for x in model['adjacency'][a]);expected=set()
        for b,u in enumerate(model['types']):
            if u!=t:
                checks+=1
                if geometry.adj[types[t-1],types[u-1]][images[a]]>>images[b]&1:expected.add(b)
        need(actual==expected,'all incidence and nonincidence rows')
    actions=0
    for perm,g in zip(model['group_action'],group_generators):
        for a,t in enumerate(model['types']):
            typ=types[t-1];x=geometry.objects[typ][images[a]];b=perm[a]-1
            need(model['types'][b]==t and geometry.lookups[typ][action(typ,x,aut[g])]==images[b],'literal generator equivariance');actions+=1
    return dict(coset_members=members,directed_cross_type_pairs=checks,generator_object_pairs=actions)

def find_map(model,projection,geometry,elements,aut,group_generators):
    gs=[[aut[tuple(v-1 for v in g)]for g in generators]for generators in projection['parabolic_generators']]
    for types in itertools.permutations(range(3)):
        if [len(geometry.objects[t])for t in types]!=model['type_sizes']:continue
        fixed=[[i for i,x in enumerate(geometry.objects[t])if all(action(t,x,g)==x for g in group)]for t,group in zip(types,gs)]
        if any(not f for f in fixed):continue
        for base in itertools.product(*fixed):
            if not all(geometry.adj[types[t],types[u]][base[t]]>>base[u]&1 for t,u in itertools.combinations(range(3),2)):continue
            images=[]
            for t,coset in zip(model['types'],model['coset_positions']):
                typ=types[t-1];x=geometry.objects[typ][base[t-1]];images.append(geometry.lookups[typ][action(typ,x,aut[elements[coset[0]-1]])])
            # Candidate generation is followed by a complete positive verification;
            # a negative candidate is not a negative classification claim.
            try:checks=verify_map(model,geometry,types,base,elements,aut,images,group_generators)
            except ValueError:continue
            return dict(catalogue_to_source_types=[t+1 for t in types],base_indices=list(base),object_images=images,checks=checks)
    return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();need(not out.exists()and out.parent.is_dir(),'fresh output');out.mkdir();start=time.monotonic()
    files=[G/'constructions_component_v1/expected/model.json',G/'palette_serialization_v1/derived/group_elements.json',
           G/'palette_serialization_v1/derived/model10.json',G/'palette_serialization_frozen01/fresh/source_projection.json',
           P/'source_clauses.json']
    inputs=[pin(p)for p in files];meta,raw,model,projection,source=map(read,files)
    need(source['label']=='Geometry 3.3'and model['source']==[24,1],'exact source route')
    elements=[tuple(v-1 for v in g)for g in raw['elements']];domain=set(elements);gens=[tuple(v-1 for v in g)for g in raw['generators']]
    need(len(domain)==len(elements)==20160 and all(tuple(g)in domain for g in meta['retained_generators']),'acquired literal point action')
    lines=meta['lines'];need(len(lines)==len(set(lines))==21 and all(l.bit_count()==5 for l in lines),'literal projective lines')
    need(all(image(l,g)in lines for l in lines for g in gens),'actual action on lines')
    saved_path=P/'probe01/baer_orbits.json';inputs.append(pin(saved_path));saved=read(saved_path);orbits=saved['orbits']
    flat=[b for orbit in orbits for b in orbit]
    need(len(flat)==len(set(flat))==360,'complete Baer count from the frame lemma, not from the source table')
    for orbit in orbits:
        need(orbit==sorted(orbit)and orbit,'ordered nonempty orbit')
        for b in orbit:need(b.bit_count()==7 and all((b&l).bit_count()in[1,3]for l in lines),'every acquired set is a Fano subplane')
        found={orbit[0]};todo=[orbit[0]]
        for b in todo:
            for g in meta['retained_generators']:
                x=image(b,g)
                if x not in found:found.add(x);todo.append(x)
        need(found==set(orbit),'exact acquired group orbit')
    inventory=dict(subplanes=len(flat),orbit_sizes=list(map(len,orbits)),completeness='60480 ordered ambient frames /168 frames per embedded Fano plane =360',seven_subset_scan_repeated=False,original_prefix_inventory=saved['inventory'])
    print(json.dumps(inventory),flush=True)
    (out/'baer_orbits.json').write_text(json.dumps(dict(inventory=inventory,orbits=orbits),indent=2)+'\n')
    identity=tuple(range(21));normalizer=tuple(meta['normalizers'][0]['points']);twists=[identity,normalizer,product(normalizer,normalizer)]
    automorphisms=[]
    for h in twists:
        need(sorted(h)==list(range(21))and all(image(l,h)in lines for l in lines),'point/line normalizer permutation')
        mapping={g:conjugate(g,h)for g in elements};need(set(mapping.values())==domain,'literal conjugation normalizes exact group');automorphisms.append(mapping)
    certificates=[];source_witnesses=[]
    for k,orbit in enumerate(orbits):
        printed=Geometry(orbit,lines);geometry=Geometry(orbit,lines,corrected=True);result=None
        need(all(row.bit_count()==18 for row in printed.adj[1,2]),'printed line-pair degree18')
        need(all(row.bit_count()==6 for row in geometry.adj[1,2]),'corrected degree6')
        i=0;extra=printed.adj[1,2][i]&~geometry.adj[1,2][i];need(extra,'a nonextendible printed pair')
        j=next(bits(extra));line_baers=[orbit[b]for b in bits(printed.adj[1,0][i])];point_baers=[orbit[b]for b in bits(printed.adj[2,0][j])]
        need(not set(line_baers)&set(point_baers),'printed flag has empty remaining-type residue')
        source_witnesses.append(dict(baer_orbit=k,line_pair=printed.objects[1][i],point_pair=printed.objects[2][j],joining_line=printed.join[printed.objects[2][j]],line_pair_baer_neighbours=line_baers,point_pair_baer_neighbours=point_baers,printed_degree=18,corrected_degree=6))
        for h,aut in zip(twists,automorphisms):
            found=find_map(model,projection['representatives'][9],geometry,elements,aut,gens)
            if found:result=found|dict(normalizer_points=list(h));break
        need(result is not None,'an exact map to the acquired catalogue for every Baer orbit')
        result.update(baer_orbit=k,catalogue_index=10,type_sizes=list(map(len,geometry.objects)),source_pairs=geometry.pairs_checked)
        certificates.append(result);print('literal_map',k,result['catalogue_to_source_types'],result['checks'],flush=True)
    need([pin(p)for p in files]+[pin(saved_path)]==inputs,'inputs unchanged')
    report=dict(status='PASS_LITERAL_BAER_GEOMETRY_33_CONSTRUCTIONS',inventory=inventory,maps=certificates,inputs=inputs,source_witnesses=source_witnesses,
                distinction='Printed recipe has nonextendible flags; corrected recipe adds existence of a common Baer subplane to the last relation. Principal classification is not refuted.',
                acquired_catalogue_index=10,local_2T='Acquired actual three true flags, transported by complete incidence/action maps.',
                new_group_or_subgroup_or_aut_or_graph_searches=0,source_credit=0,whole_source_credit=0,seconds=time.monotonic()-start)
    (out/'certificate.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
if __name__=='__main__':main()
