"""Independent small mathematical checks and synthetic producer controls."""
import argparse
import hashlib
import itertools
import json
import os
import sys
import types
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--volume',type=Path,required=True)
    args = parser.parse_args()
    if not (sys.flags.ignore_environment and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError('ordinary -E -B -S controls')
    root = Path(__file__).resolve(strict=True).parent
    with (root/'manifest.json').open('rb') as stream:
        raw = stream.read(16385)
    if len(raw) > 16384 or hashlib.sha256(raw).hexdigest() != args.manifest_sha256:
        raise ValueError('exact release manifest')
    manifest = json.loads(raw)
    with (root/'run.py').open('rb') as stream:
        source = stream.read(32769)
    if len(source) > 32768 or hashlib.sha256(source).hexdigest() != manifest['files']['runner']['sha256']:
        raise ValueError('exact producer Source')
    R = types.ModuleType('synthetic_portable_producer')
    R.__file__ = str(root/'run.py')
    exec(compile(source,R.__file__,'exec',dont_inherit=True),R.__dict__)
    R.need(all(k not in os.environ for k in R.ENVIRONMENT),'four retained environment denials')
    bundle = R.Bundle(root,'manifest.json',args.manifest_sha256)
    R.need(bundle.refs['controls']['path'] == Path(__file__).name,'truthful current controls identity')
    T = R.activate(bundle)
    guard = T.Guard(args.volume)
    checks = []
    def done(name,condition=True):
        R.need(condition,name)
        guard.check()
        checks.append(name)
    def reject(name,fragment,call):
        try:
            call()
        except ValueError as exc:
            done(name,fragment in str(exc))
            return
        raise ValueError('unexpected acceptance: '+name)
    row = T.row_data(1)
    profiles = T.Profiles(row,'L',guard)
    brute = {m for m in itertools.combinations_with_replacement(range(8),6)
        if tuple(sum(v >> j & 1 for v in m) for j in range(3)) == (3,3,4)}
    acquired = list(profiles.interval(0,profiles.total()))
    done('DP_equals_independent1716_multiset_domain',
        {m for i,m in acquired} == brute and [i for i,m in acquired] == list(range(len(brute))))
    left = ((0,3,4,5,6,7),((1,3),(1,5),(2,5),(3,4),(4,5)))
    right = ((1,1,2,4,7,7),((0,4),(1,4),(2,5),(3,5),(4,5)))
    engine = T.Engine(guard)
    marked = (1,2,0,1,6,6,(0,0),(1,0,0),left,right)
    graph = T.graph_from_code(marked)
    distance = []
    for start in range(32):
        d = [-1]*32
        d[start] = 0
        queue = [start]
        for v in queue:
            for w in range(32):
                if graph[v] & (1 << w) and d[w] < 0:
                    d[w] = d[v]+1
                    queue.append(w)
        distance.append(d)
    done('fixture_independent_degree_girth_and_diameter',
        all(mask.bit_count() == 5 for mask in graph)
        and min(map(min,distance)) == 0 and max(map(max,distance)) == 8
        and all(distance[0][v]%2 != distance[0][w]%2 for v in range(32)
                for w in range(32) if graph[v] & (1 << w))
        and any((graph[v]&graph[w]).bit_count() >= 2 for v in range(32) for w in range(v)))
    code,witness = T.ordinary_code(graph,engine)
    full = [T.marked_code(graph,(a,b),m,tuple(x%2 for x in distance[0]),engine)[0]
        for a,b in itertools.combinations(range(32),2) if distance[a][b] == 8
        for m in range(32) if distance[a][m] == distance[b][m] == 4]
    done('intrinsic_root_reduction_equals_all_physical_roots',full and min(full) == code)
    order = tuple((5*i+7)%32 for i in range(32))
    moved = tuple(sum(1 << j for j,w in enumerate(order) if graph[v] & (1 << w)) for v in order)
    other,trace = T.ordinary_code(moved,engine)
    done('arbitrary_relabeling_and_full32_witness',other == code
         and T.witness_ok(moved,other,trace) and T.witness_ok(graph,code,witness))
    class Profiles:
        def __init__(self,*args):pass
        def total(self):return 2
        def interval(self,*args):return iter(((0,(0,)),(1,(1,))))
    class Engine:
        def __init__(self,*args):pass
        def forms(self,row,side,masks):
            return [masks],dict(omission_candidates=1,profile_orbit_representative=1)
    toy = types.SimpleNamespace(Profiles=Profiles,Engine=Engine,
        row_data=lambda i:dict(q=1,t=0,u=0,nL=5,nR=5,mL=(),mR=()),
        check_side=lambda *args:None,graph_from_code=lambda marked:marked,
        ordinary_code=lambda marked,e:((marked[-2],marked[-1]),tuple(range(32))),
        witness_ok=lambda *args:True)
    codes,rows,totals = R.enumerate_all(toy,guard)
    done('toy_complete28_domains14_products_global_union',len(rows) == 14
         and totals == dict(local_forms=56,pairs=56,profiles=56) and len(codes) == 4
         and all(row['completed_pairs'] == 4 for row in rows))
    class GapProfiles(Profiles):
        def interval(self,*args):return iter(((0,(0,)),(2,(1,))))
    bad = types.SimpleNamespace(**vars(toy))
    bad.Profiles = GapProfiles
    reject('profile_gap_refused','complete deterministic profile order',lambda:R.enumerate_all(bad,guard))
    reject('relative_escape_refused','literal relative artifact path',lambda:R.relative(root,'../run.py'))
    reject('duplicate_JSON_key_refused','duplicate JSON key',lambda:R.strict(b'{"a":1,"a":2}'))
    R.need(args.out.is_absolute() and args.out.parent.resolve(strict=True) == args.out.parent
           and not os.path.lexists(args.out),'fresh absolute synthetic output')
    args.out.mkdir()
    original = R.POLICY
    try:
        R.POLICY = dict(original,shard_records=2,shard_bytes=32,output_bytes=512)
        sharded = args.out/'shards'
        sharded.mkdir()
        samples = {b'[4]\n',b'[0]\n',b'[2]\n',b'[1]\n',b'[3]\n'}
        shards,n,size,sha = R.emit_codes(sharded,samples,guard)
        R.verify_shards(sharded,shards,n,size,sha,guard)
        done('shards_match_independent_sorted_concatenation',n == 5 and len(shards) == 3
             and sha == hashlib.sha256(b''.join(sorted(samples))).hexdigest())
        R.POLICY = dict(original,output_bytes=3)
        refused = args.out/'refusal'
        refused.mkdir()
        reject('data_cap_refuses_whole_record','complete scientific output byte bound',
               lambda:R.emit_codes(refused,{b'[0]\n'},guard))
        done('refused_data_has_no_partial_shard',not list(refused.iterdir()))
    finally:
        R.POLICY = original
    bundle.sweep()
    report = dict(schema='QUINTIC_BIPARTITE_PUBLIC_SYNTHETIC_CONTROLS_V1',status='PASS',
        manifest=bundle.manifest,inputs=bundle.refs,checks=checks,
        synthetic_graph_fixtures=1,synthetic_producer_pairs=56,
        actual_full_producer_runs=0,original_case_credit=0,
        scope='Small independent domains, one graph fixture and synthetic orchestration only.')
    R.write_whole(args.out,'result.json',R.canonical(report),16384)
    guard.check(145)


if __name__ == '__main__':
    main()
