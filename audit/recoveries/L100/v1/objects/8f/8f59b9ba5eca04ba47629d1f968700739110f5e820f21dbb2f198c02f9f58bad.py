import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,collections,itertools,json
from pathlib import Path
import probe_engine as c
P=Path(__file__).resolve().parent
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def load():
    return dict(meta=read(P/'inputs/projective_model.json'),raw=read(P/'inputs/group_elements.json'),model=read(P/'inputs/catalogue_model10.json'),projection=read(P/'inputs/source_projection.json'),orbits=read(P/'inputs/baer_orbits.json')['orbits'])
def validate_orbits(data):
    meta=data['meta'];orbits=data['orbits'];lines=meta['lines']
    need(len(lines)==len(set(lines))==21 and all(l.bit_count()==5 for l in lines),'21 literal projective lines')
    flat=[b for orbit in orbits for b in orbit]
    need(len(orbits)==3 and all(len(o)==120 for o in orbits) and len(flat)==len(set(flat))==360,'360 distinct subplanes, three 120-orbits')
    for orbit in orbits:
        need(orbit==sorted(orbit),'ordered orbit')
        for b in orbit:
            need(0<=b<1<<21 and b.bit_count()==7 and all((b&l).bit_count() in (1,3) for l in lines),'actual Fano subplane criterion')
        found={orbit[0]};todo=[orbit[0]]
        for b in todo:
            for g in meta['retained_generators']:
                x=c.image(b,g)
                if x not in found:found.add(x);todo.append(x)
        need(found==set(orbit),'exact full generator orbit')
    return orbits
def geometries(data):return [c.Geometry(o,data['meta']['lines'],corrected=True) for o in data['orbits']]
def validate_witness(w,orbit,lines):
    # Independent set formulation: no use of Geometry.incident or its bit rows.
    need(set(w)=={'baer_orbit','line_pair','point_pair','joining_line','line_pair_baer_neighbours','point_pair_baer_neighbours','printed_degree','corrected_degree'},'exact witness schema')
    l1,l2=w['line_pair'];p=w['point_pair'];j=w['joining_line']
    need(l1 in lines and l2 in lines and l1!=l2 and p.bit_count()==2 and 0<=p<1<<21,'literal witness objects')
    L1=set(c.bits(l1));L2=set(c.bits(l2));Q=set(c.bits(p));J=set(c.bits(j))
    need(j in lines and Q<=J and not (L1|L2)&Q and bool(L1&L2&J),'printed incident pair')
    a=[b for b in orbit if set(c.bits(b))&(L1|L2)==L1&L2]
    d=[b for b in orbit if not set(c.bits(b))&Q and len(set(c.bits(b))&J)==3]
    need(a==w['line_pair_baer_neighbours'] and d==w['point_pair_baer_neighbours'],'complete actual Baer neighbours')
    need(len(a)==len(d)==4 and not set(a)&set(d),'nonextendible printed flag')
    need(w['printed_degree']==18 and w['corrected_degree']==6,'separate printed/corrected degrees')
    return 2*len(orbit)
def validate_map(r,data,geometry):
    need(r['catalogue_index']==10 and r['type_sizes']==[120,210,210] and r['source_pairs']==94500,'exact mapped model scope')
    raw=data['raw'];elements=[tuple(x-1 for x in g) for g in raw['elements']];domain=set(elements)
    need(len(domain)==len(elements)==20160,'acquired exact full group')
    h=tuple(r['normalizer_points']);need(sorted(h)==list(range(21)),'point permutation')
    need(all(c.image(l,h) in data['meta']['lines'] for l in data['meta']['lines']),'normalizer preserves literal lines')
    aut={g:c.conjugate(g,h) for g in elements};need(set(aut.values())==domain,'actual full-group normalization')
    types=[t-1 for t in r['catalogue_to_source_types']];need(sorted(types)==[0,1,2],'type bijection')
    base=r['base_indices'];need(len(base)==3 and all(type(x)==int and 0<=x<len(geometry.objects[t]) for x,t in zip(base,types)),'valid base objects')
    model=data['model'];need(model['source']==[24,1] and model['type_sizes']==[210,210,120],'actual accepted model10')
    for t,i,gens in zip(types,base,data['projection']['representatives'][9]['parabolic_generators']):
        x=geometry.objects[t][i]
        need(all(c.action(t,x,aut[tuple(a-1 for a in g)])==x for g in gens),'actual parabolic fixes base object')
    result=c.verify_map(model,geometry,types,base,elements,aut,r['object_images'],[tuple(x-1 for x in g) for g in raw['generators']])
    need(result==r['checks'],'exact complete positive-map checks')
    return result
def source_comparison(data,gs):
    # Literal set conditions independently compare every pair to both constructions.
    lines=data['meta']['lines'];queries=0;common=collections.Counter()
    for orbit,g in zip(data['orbits'],gs):
        for i,B in enumerate(orbit):
            S=set(c.bits(B))
            for j,(a,b) in enumerate(g.objects[1]):
                A=set(c.bits(a));D=set(c.bits(b));v=S&(A|D)==A&D
                need(v==bool(g.adj[0,1][i]>>j&1),'literal first source relation');queries+=1
            for j,p in enumerate(g.objects[2]):
                Q=set(c.bits(p));J=set(c.bits(g.join[p]));v=not S&Q and len(S&J)==3
                need(v==bool(g.adj[0,2][i]>>j&1),'literal second source relation');queries+=1
    for i,(a,b) in enumerate(gs[0].objects[1]):
        A=set(c.bits(a));B=set(c.bits(b));printed=0
        for j,p in enumerate(gs[0].objects[2]):
            Q=set(c.bits(p));J=set(c.bits(gs[0].join[p]));v=not (A|B)&Q and bool(A&B&J)
            counts=tuple((g.adj[1,0][i]&g.adj[2,0][j]).bit_count() for g in gs)
            for g,n in zip(gs,counts):need(bool(g.adj[1,2][i]>>j&1)==(v and n>0),'exact common-Baer repair')
            if v:printed+=1;common[counts]+=1
            queries+=1
        need(printed==18,'every printed degree18')
        need(all(g.adj[1,2][i].bit_count()==6 for g in gs),'every corrected degree6')
    need(common==collections.Counter({(2,0,0):1260,(0,2,0):1260,(0,0,2):1260}),'printed flags split between the three orbits')
    return dict(set_predicate_queries=queries,printed_flags=3780,common_Baer_distribution={','.join(map(str,k)):v for k,v in sorted(common.items())})
def audit(data,cert):
    need(cert['status']=='PASS_LITERAL_BAER_GEOMETRY_33_CONSTRUCTIONS','recorded positive certificate')
    validate_orbits(data);gs=geometries(data)
    need(len(cert['maps'])==len(cert['source_witnesses'])==3,'all three choices')
    reports=[]
    for k,(r,w,g) in enumerate(zip(cert['maps'],cert['source_witnesses'],gs)):
        need(r['baer_orbit']==w['baer_orbit']==k,'exact orbit identity')
        validate_witness(w,data['orbits'][k],data['meta']['lines']);reports.append(validate_map(r,data,g))
    return dict(status='PASS_L100_BAER_REPAIR_AND_PRINTED_FLAG_DEFECT',subplanes=360,orbits=[120]*3,positive_maps=reports,source_comparison=source_comparison(data,gs),target_runs=0,subset_enumerations=0,principal_classification_refuted=False,whole_source_credit=0)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
    d=load();r=audit(d,read(P/'expected/certificate.json'));a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
