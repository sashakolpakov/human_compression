"""Standalone stdlib incidence catalogue and complete supplied-catalogue checker.

Source author /root/readme_final_check; complement-hypergraph idea Root/Nav.
Only the literal universe/index constants are bound at import. Raw/S6
enumeration occurs inside entry functions; there are no project imports.
This is A-L INCIDENCE ONLY, never full side graphs or census coverage.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import resource
import sys
import time

EDGES=((0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),
       (2,3),(2,4),(2,5),(3,4),(3,5),(4,5))
EDGE_ID={pair:i for i,pair in enumerate(EDGES)}
RAW_COUNT=11628
SCHEMA='F009_SIX_SIDE_MISSING_PAIR_ORBIT_CATALOGUE_V1'
SCOPE=dict(incidence_only=True,A_row_labels_forgotten=True,seed_A1_row_not_marked=True,
    full_side_graphs=False,port_library=False,current_H_coverage=False,upper_census_coverage=False,
    new_family_or_Original_or_Lean_or_measurement_credit=0)


class UnpaidBound(Exception):
    pass


def need(value,reason):
    if not value:raise ValueError(reason)


class Work:
    def __init__(self):
        self.started=time.monotonic();self.units=0

    def take(self,count=1):
        self.units+=count
        if self.units>10000000:raise UnpaidBound('UNPAID: shared10M permutation/finite-action units')
        if count==0 or self.units%1024==0:
            rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
            if time.monotonic()-self.started>=20 or rss>128*2**20:
                raise UnpaidBound('UNPAID: internal20s/128MiB; outer512MiB/150s unchanged')


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def strict(raw):
    def pairs(items):
        result={}
        for key,value in items:need(key not in result,'duplicate JSON key');result[key]=value
        return result
    def bad(text):raise ValueError('integer-only finite certificate '+text)
    return json.loads(raw,object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)


def raw_tuple(value):
    need(type(value)is list and len(value)==5 and all(type(x)is int and 0<=x<15 for x in value)
         and value==sorted(value),'five sorted typed loopless-edge indices; parallel edges allowed')
    return tuple(value)


def permutation(value):
    need(type(value)is list and len(value)==6 and all(type(x)is int for x in value)
         and sorted(value)==[0,1,2,3,4,5],'literal bijection old vertex -> new vertex')
    return tuple(value)


def degrees(raw):
    result=[0]*6
    for edge in raw:
        u,v=EDGES[edge];result[u]+=1;result[v]+=1
    return result


def geometry(raw,work):
    work.take();delta=degrees(raw)
    cover=[]
    for i,(u,v)in enumerate(EDGES):
        if all(u in EDGES[e]or v in EDGES[e]for e in raw):cover.append(i)
    return dict(missing_degrees=delta,A_degrees=[5-d for d in delta],two_cover_edges=cover,
        residual_degree_to_L_or_ports=delta,residual_degree_sum=10)


def direct_transform(raw,p,work):
    """Checker path: direct endpoint action, independent of producer edge maps."""
    work.take();out=[]
    for edge in raw:
        u,v=EDGES[edge];a,b=p[u],p[v]
        out.append(EDGE_ID[(a,b)if a<b else(b,a)])
    return tuple(sorted(out))


def group_maps(work):
    result=[]
    for p in itertools.permutations(range(6)):
        work.take();edge_map=[];inverse=[0]*6
        for i,j in enumerate(p):inverse[j]=i
        for u,v in EDGES:
            a,b=p[u],p[v];edge_map.append(EDGE_ID[(a,b)if a<b else(b,a)])
        result.append((p,tuple(edge_map),tuple(inverse)))
    need(len(result)==720,'complete S6 list');work.take(0);return result


def canonical_orbit(raw,maps,work):
    """720 complete images, then explicit image-to-minimum transporters."""
    first={}
    for i,(_,edge_map,_)in enumerate(maps):
        work.take();image=tuple(sorted(edge_map[e]for e in raw))
        first.setdefault(image,i)
    representative=min(first);tau=maps[first[representative]][0];answer={}
    for image,i in first.items():
        work.take();inverse=maps[i][2]
        # If image=raw^p and minimum=raw^tau, use p^-1*tau on image.
        transporter=tuple(tau[inverse[v]]for v in range(6))
        answer[image]=(representative,transporter)
    work.take(0);return representative,answer


def universe():
    return dict(A_vertices=5,L_vertices=6,neighbors_per_A=4,missing_pair_edges=list(map(list,EDGES)),
        missing_pairs_per_A=2,raw_edge_multiset_count=RAW_COUNT,max_missing_degree=4,
        vertex_group='S6',vertex_group_order=720,
        multiset_rows_forget_A_labels=True,parallel_missing_pairs_allowed=True)


def produce(work):
    maps=group_maps(work);cache={};assigned=[];raw_count=invalid=0
    for raw in itertools.combinations_with_replacement(range(15),5):
        work.take();raw_count+=1
        if max(degrees(raw))>4:invalid+=1;continue
        if raw not in cache:
            _,orbit=canonical_orbit(raw,maps,work)
            for image,value in orbit.items():
                need(image not in cache or cache[image]==value,'complete disjoint producer orbit cache')
                cache[image]=value
        rep,p=cache[raw]
        need(direct_transform(raw,p,work)==rep,'every emitted actual vertex transporter')
        assigned.append((raw,rep,p))
    need(raw_count==RAW_COUNT,'all stars-and-bars cases, no truncation')
    representatives=sorted({rep for _,rep,_ in assigned});ids={rep:i for i,rep in enumerate(representatives)}
    counts=[0]*len(representatives)
    for _,rep,_ in assigned:counts[ids[rep]]+=1
    reps=[]
    for rep,count in zip(representatives,counts):
        need(count>0 and 720%count==0,'exact orbit/stabilizer divisibility')
        reps.append(dict(missing_pairs=list(rep),orbit_size=count,stabilizer_size=720//count,**geometry(rep,work)))
    value=dict(schema=SCHEMA,universe=universe(),scope=dict(SCOPE),representatives=reps,
        mapping=[dict(raw=list(raw),representative=ids[rep],vertex_transporter=list(p))for raw,rep,p in assigned],
        counts=dict(raw=raw_count,invalid_degree=invalid,valid=len(assigned),orbits=len(reps)))
    work.take(0);return value


def canonical_representative(raw,work):
    need(max(degrees(raw))<=4,'representative has an A-neighbor in every column')
    for p in itertools.permutations(range(6)):
        need(direct_transform(raw,p,work)>=raw,'representative is the exact S6 minimum')


def mapping_index(rows,rep_count):
    need(type(rows)is list and len(rows)<=RAW_COUNT,'bounded whole mapping list')
    by={}
    for row in rows:
        need(type(row)is dict and set(row)=={'raw','representative','vertex_transporter'},'entire mapping record')
        raw=raw_tuple(row['raw']);p=permutation(row['vertex_transporter']);i=row['representative']
        need(type(i)is int and 0<=i<rep_count and raw not in by,'unique raw case and exact representative index')
        by[raw]=(i,p)
    return by


def verify_mapping(raw,p,representative,work):
    need(direct_transform(raw,p,work)==representative,'supplied permutation really carries this multiset')


def check(value,work):
    """Accept ANY complete valid catalogue in this format, without producer search.

    Representative/mapping list orders and valid transporters may differ.
    Canonicality is checked once per representative; each raw case gets only
    one supplied permutation application. No canonical-orbit cache is built.
    """
    need(type(value)is dict and set(value)=={'schema','universe','scope','representatives','mapping','counts'},'whole catalogue fields')
    need(value['schema']==SCHEMA and canonical(value['universe'])==canonical(universe())
         and canonical(value['scope'])==canonical(SCOPE),'exact incidence-only universe and qualifications')
    reps=value['representatives'];need(type(reps)is list and 1<=len(reps)<=RAW_COUNT,'bounded whole representatives')
    raws=[];seen=set()
    rep_keys={'missing_pairs','orbit_size','stabilizer_size','missing_degrees','A_degrees','two_cover_edges',
              'residual_degree_to_L_or_ports','residual_degree_sum'}
    for r in reps:
        need(type(r)is dict and set(r)==rep_keys,'entire representative geometry record')
        raw=raw_tuple(r['missing_pairs']);need(raw not in seen,'distinct canonical representatives');seen.add(raw)
        canonical_representative(raw,work);g=geometry(raw,work)
        need(all(canonical(r[k])==canonical(v)for k,v in g.items()),'exact2-cover and residual-degree data')
        need(type(r['orbit_size'])is int and r['orbit_size']>0 and type(r['stabilizer_size'])is int
             and r['stabilizer_size']>0 and r['orbit_size']*r['stabilizer_size']==720,'typed orbit/stabilizer fields')
        raws.append(raw)
    by=mapping_index(value['mapping'],len(raws));frequency=[0]*len(raws);raw_count=invalid=valid=0
    for raw in itertools.combinations_with_replacement(range(15),5):
        work.take();raw_count+=1
        if max(degrees(raw))>4:
            need(raw not in by,'invalid degree case is never admitted');invalid+=1;continue
        need(raw in by,'EVERY valid input multiset represented, no missing case')
        i,p=by[raw];verify_mapping(raw,p,raws[i],work);frequency[i]+=1;valid+=1
    need(raw_count==RAW_COUNT and len(by)==valid,'complete exact raw domain and no extra rows')
    need(all(frequency[i]==r['orbit_size']for i,r in enumerate(reps)),'whole complete orbit multiplicities')
    expected=dict(raw=RAW_COUNT,invalid_degree=invalid,valid=valid,orbits=len(reps))
    need(type(value['counts'])is dict and canonical(value['counts'])==canonical(expected),'entire typed counts from fresh full coverage')
    work.take(0);return expected


def controls(work):
    names=[]
    def refused(name,fn):
        try:fn()
        except ValueError:names.append(name)
        else:raise ValueError('expected TEST_ONLY refusal '+name)
    need(max(degrees((0,0,0,0,0)))==5,'five parallel edges have forbidden column degree5');names.append('five_parallel_edges_invalid')
    need(max(degrees((0,1,2,3,4)))==5,'five-edge star has forbidden column degree5');names.append('five_edge_star_invalid')
    rep=(0,0,0,0,9);g=geometry(rep,work)
    need(g['missing_degrees']==[4,4,1,1,0,0]and g['two_cover_edges']==[1,2,5,6]
         and g['A_degrees']==[1,1,4,4,5,5],'independent four-parallel/disjoint-edge cover calculation');names.append('parallel_disjoint_geometry')
    path=(0,5,9,12,14);need(geometry(path,work)['two_cover_edges']==[],'P6 has vertex-cover number3');names.append('path_has_no_two_cover')
    cycle=(0,3,5,9,12);need(geometry(cycle,work)['two_cover_edges']==[],'C5 has vertex-cover number3');names.append('cycle_has_no_two_cover')
    maps=group_maps(work);p=(1,2,0,4,5,3);image=direct_transform(rep,p,work)
    minimum,orbit=canonical_orbit(image,maps,work)
    need(minimum==rep and len(orbit)==90,'heavy disjoint-pair orbit:15 choices times6')
    for raw,(r,q)in orbit.items():verify_mapping(raw,q,r,work)
    names.append('noninvolutory_transport_and_orbit90')
    refused('noncanonical_representative',lambda:canonical_representative(image,work))
    refused('Boolean_edge_alias',lambda:raw_tuple([False,0,0,0,9]))
    refused('Boolean_vertex_alias',lambda:permutation([False,1,2,3,4,5]))
    refused('false_transporter',lambda:verify_mapping(image,(0,1,2,3,4,5),rep,work))
    row=dict(raw=list(rep),representative=0,vertex_transporter=list(range(6)))
    refused('duplicate_raw_coverage',lambda:mapping_index([row,row],1))
    need(len(names)==11,'eleven meaningful TEST_ONLY controls');work.take(0)
    return dict(schema='F009_SIX_SIDE_INCIDENCE_CONTROLS_V1',controls=names,all_passed=True,
        TEST_ONLY=True,whole_11628_catalogue_enumerated=False,scope=dict(SCOPE))


def file_pin(path):
    p=Path(path);a=p.stat();need(p.resolve(strict=True)==p and p.is_file()and not p.is_symlink()and a.st_nlink==1,'canonical ordinary file')
    h=hashlib.sha256();count=0
    with p.open('rb')as f:
        b=os.fstat(f.fileno())
        for raw in iter(lambda:f.read(2**20),b''):h.update(raw);count+=len(raw);need(count<=16*2**20,'whole file16MiB')
        z=os.fstat(f.fileno())
    signature=lambda x:(x.st_dev,x.st_ino,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
    need(signature(a)==signature(b)==signature(z)==signature(p.stat())and count==a.st_size
         and p.resolve(strict=True)==p and not p.is_symlink(),'stable entire canonical file')
    return dict(path=str(p),bytes=count,sha256=h.hexdigest())


def write(path,raw):
    with path.open('xb')as f:need(f.write(raw)==len(raw),'entire fresh output');f.flush();os.fsync(f.fileno())
    return file_pin(path)


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--mode',choices=('produce','check','controls'),required=True)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--supplied',type=Path);parser.add_argument('--sha256')
    a=parser.parse_args();need(not sys.flags.optimize,'ordinary assertions required')
    need((a.mode=='check')==(a.supplied is not None)and(a.supplied is None)==(a.sha256 is None),'paired actual supplied catalogue only for check')
    out=a.out;need(out.is_absolute()and out.parent.resolve(strict=True)==out.parent and not os.path.lexists(out),'fresh canonical absolute output directory')
    work=Work();supplied=None;raw=None
    if a.mode=='produce':value=produce(work)
    elif a.mode=='controls':value=controls(work)
    else:
        supplied=file_pin(a.supplied);need(supplied['sha256']==a.sha256,'actual entire supplied catalogue SHA')
        raw=a.supplied.read_bytes();value=strict(raw);need(raw==canonical(value),'exact canonical supplied bytes, never normalization')
        check(value,work);need(file_pin(a.supplied)==supplied,'same whole catalogue after independent checking')
    emitted=canonical(value);need(raw is None or emitted==raw,'entire supplied catalogue bytes retained')
    need(len(emitted)+65536<=16*2**20,'reserve complete artifact/result bundle16MiB');work.take(0)
    out.mkdir();cr=write(out/('controls.json'if a.mode=='controls'else'catalogue.json'),emitted)
    if raw is not None:need(Path(cr['path']).read_bytes()==raw,'emitted verified catalogue equals every supplied byte')
    result=dict(schema='F009_SIX_SIDE_INCIDENCE_RESULT_V1',mode=a.mode,
        status='PASS_TEST_ONLY_CONTROLS'if a.mode=='controls'else'VERIFIED_COMPLETE_INCIDENCE_ORBIT_CATALOGUE',
        certificate=cr,supplied=supplied,program_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        counts=value.get('counts'),controls=11 if a.mode=='controls'else None,
        work_units=work.units,internal_seconds=time.monotonic()-work.started,
        checker_reruns_producer_search=False if a.mode=='check'else None,scope=dict(SCOPE))
    rr=canonical(result);need(len(rr)<=65536,'small whole result');work.take(0);ref=write(out/'result.json',rr);work.take(0)
    print(json.dumps(dict(status=result['status'],result=ref,certificate=cr,mode=a.mode,new_credit=0),sort_keys=True))


if __name__=='__main__':main()
