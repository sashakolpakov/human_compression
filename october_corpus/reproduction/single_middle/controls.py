"""Controls for the singleton-middle producer."""
import argparse
import hashlib
import itertools
import json
import os
import resource
import stat
import sys
import time
import types
from pathlib import Path

START = time.monotonic()


def need(ok, why):
    if not ok:
        raise ValueError(why)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss *= 1 if sys.platform == 'darwin' else 1024
    if rss >= 128*2**20 or time.monotonic()-START >= 120:
        raise RuntimeError('128MiB120s controls bound')

def signature(value):
    return (value.st_dev,value.st_ino,value.st_mode,value.st_nlink,
            value.st_size,value.st_mtime_ns,value.st_ctime_ns)

def read_file(path, cap):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
         and 0 <= before.st_size <= cap,'bounded ordinary file')
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        raw = stream.read(cap+1)
        closed = os.fstat(stream.fileno())
    need(signature(before) == signature(opened) == signature(closed)
         == signature(path.lstat()) and len(raw) == before.st_size,
         'whole stable ordinary file')
    return raw

def independent_expand(code, edges):
    """Direct control construction, independent of the subject decoder."""
    shape,ports,rows = code
    graph = [set() for unused in range(16)]
    pairs = [(0,a) for a in range(1,6)]
    pairs += [(6+a,6+b) for a,b in edges[shape-1]]
    pairs += [(1+a,6+v) for a,mask in enumerate(rows) for v in range(7) if mask & (1 << v)]
    pairs += [(13+b,6+v) for b,mask in enumerate(ports) for v in range(7) if mask & (1 << v)]
    for a,b in pairs:
        graph[a].add(b)
        graph[b].add(a)
    return tuple(sum(1 << w for w in row) for row in graph)

def independent_permute(graph, order):
    n = len(graph)
    return tuple(sum(1 << j for j,old in enumerate(order) if graph[v] & (1 << old)) for v in order)

def brute_code(graph, standard_edges):
    """All physical endpoint vertices and all7! side orders; no subject root filter."""
    ports = [v for v in range(16) if graph[v].bit_count() == 3]
    targets = {tuple(sorted(tuple(sorted(e)) for e in es)):i+1 for i,es in enumerate(standard_edges)}
    best = None
    attempts = 0
    for p in range(16):
        if p in ports:
            continue
        rows = [v for v in range(16) if graph[p] & (1 << v)]
        if len(rows) != 5 or set(rows) & set(ports):
            continue
        if any(graph[a] & (1 << b) for a in rows for b in ports):
            continue
        side = [v for v in range(16) if v != p and v not in rows and v not in ports]
        if len(side) != 7 or any(not any(graph[v] & (1 << a) for a in rows) for v in side):
            continue
        actual_edges = [(u,v) for u in side for v in side if u < v and graph[u] & (1 << v)]
        for order in itertools.permutations(side):
            attempts += 1
            if attempts & 255 == 0:
                need(True,'bounded full7factorial control')
            position = {v:i for i,v in enumerate(order)}
            key = tuple(sorted(tuple(sorted((position[a],position[b]))) for a,b in actual_edges))
            shape = targets.get(key)
            if shape is None:
                continue
            masks = lambda collection:tuple(sorted(sum(1 << i for i,v in enumerate(order)
                if graph[a] & (1 << v)) for a in collection))
            candidate = shape,masks(ports),masks(rows)
            if best is None or candidate < best:
                best = candidate
    need(best is not None,'independent complete root domain nonempty')
    return best


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--volume',type=Path,required=True)
    args = parser.parse_args()
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, 'ordinary -E -B -S controls')
    need(all(k not in os.environ for k in ('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG',
         'OPENSSL_CONF','OPENSSL_MODULES')), 'four retained environment denials')
    root = Path(__file__).resolve(strict=True).parent
    raw = read_file(root/'manifest.json',16384)
    need(hashlib.sha256(raw).hexdigest() == args.manifest_sha256, 'exact release manifest')
    manifest = json.loads(raw)
    source = read_file(root/'run.py',32768)
    need(hashlib.sha256(source).hexdigest() == manifest['files']['runner']['sha256'],
         'producer Source hash')
    R = types.ModuleType('synthetic_single_middle_producer')
    R.__file__ = str(root/'run.py')
    exec(compile(source,R.__file__,'exec',dont_inherit=True),R.__dict__)
    bundle = R.Bundle(root,'manifest.json',args.manifest_sha256)
    need(bundle.refs['controls']['path'] == Path(__file__).name, 'truthful controls identity')
    T = R.activate(bundle)
    guard = T.Guard(args.volume)
    checks = []
    def done(name,condition=True):
        need(condition,name)
        checks.append(name)
    def reject(name,fragment,call):
        try:
            call()
        except ValueError as exc:
            done(name,fragment in str(exc))
            return
        raise ValueError('unexpected acceptance: '+name)
    standards = (((0,1),(1,2),(2,3)),((0,1),(0,2),(0,3)),
                 ((0,1),(1,2),(3,4)),((0,1),(2,3),(4,5)))
    fixtures = ((1,(21,50,104),(58,89,90,101,101)),
                (2,(14,14,14),(113,113,114,116,120)),
                (3,(13,13,13),(106,113,114,114,116)),
                (4,(21,21,21),(90,102,105,106,106)))
    for i,value in enumerate(fixtures,1):
        graph = T.half_from_code(value)
        code,witness = T.canonical_half(graph,guard)
        done('fixture%d_all_roots_and7factorial_code'%i,code == brute_code(graph,standards))
        done('fixture%d_independent_full16_witness'%i,
             independent_permute(graph,witness) == independent_expand(code,standards))
        order = tuple((5*j+3)%16 for j in range(16))
        moved = independent_permute(graph,order)
        other,trace = T.canonical_half(moved,guard)
        need(other == code and independent_permute(moved,trace) == independent_expand(code,standards),
             'ordinary relabeling invariance')
        done('fixture%d_relabeling'%i)
    bad = (2,(14,49,81),(54,90,108,108,114))
    degree_graph = independent_expand(bad,standards)
    done('zero_alpha_still_has_correct_degree_pattern',
         sorted(v.bit_count() for v in degree_graph) == [3]*3+[5]*13)
    reject('zero_alpha_refused','positive endpoint column incidence',lambda:T.validate_presentation(bad))
    reject('relative_escape_refused','literal relative artifact path',lambda:R.relative(root,'../run.py'))
    reject('duplicate_JSON_refused','duplicate JSON key',lambda:R.strict(b'{"x":1,"x":2}'))
    graph = T.half_from_code(fixtures[0])
    fixed,witness = T.canonical_half(graph,guard)
    class ToyDomain:
        na,nb = 4,3
        def __init__(self,*args):pass
        def ports(self,first,last):return ((j,j) for j in range(first,last))
        def port_context(self,j):
            if j == 0:return 'orbit',(),()
            if j == 2:return 'margin',(),()
            return 'compatible',[(1,('alias',)),(3,('construct',))],((),)
        def endpoint_representative(self,rows,stabilizer):return rows[0] != 'alias'
    toy = types.SimpleNamespace(Domain=ToyDomain,BOUNDS=((0,0,4,3),)*4,
        half_from_code=lambda code:graph,canonical_half=lambda g,b:(fixed,witness),
        witness_ok=T.witness_ok)
    codes,domains,totals = R.enumerate_all(toy,guard)
    done('toy_complete_domain_union',len(codes) == 1 and len(domains) == 4
         and totals == dict(compatible_attempts=8,constructed_marked_halves=4,canonical_fixed_points_checked=1)
         and all(d['completed_raw_interval'] == [0,12] for d in domains))
    done('toy_raw_cell_accounting',all(d['counters'] == dict(margin_skips=6,
         port_orbit_skips=4,endpoint_orbit_skips=1,constructed_halves=1,compatible_attempts=2)
         for d in domains))
    class TailDomain(ToyDomain):
        def ports(self,*args):return iter(((0,0),(1,1)))
    broken = types.SimpleNamespace(**vars(toy))
    broken.Domain = TailDomain
    reject('missing_final_block_refused','entire raw rectangle accounted for',lambda:R.enumerate_all(broken,guard))
    need(args.out.is_absolute() and args.out.parent.resolve(strict=True) == args.out.parent
         and not os.path.lexists(args.out), 'fresh absolute synthetic output')
    args.out.mkdir()
    original = R.POLICY
    try:
        R.POLICY = dict(original,evaluations=1)
        reject('compatible_bound_cannot_publish_count','full-run compatible-cell bound',
               lambda:R.enumerate_all(toy,guard))
        R.POLICY = dict(original,shard_records=2,shard_bytes=32,output_bytes=512)
        target = args.out/'shards'
        target.mkdir()
        samples = {b'[0]\n',b'[2]\n',b'[1]\n'}
        shards,n,size,sha = R.emit_codes(target,samples,guard)
        R.verify_shards(target,shards,n,size,sha,guard)
        done('shards_equal_independent_sorted_stream',n == 3 and len(shards) == 2
             and sha == hashlib.sha256(b''.join(sorted(samples))).hexdigest())
        R.POLICY = dict(original,output_bytes=3)
        capped = args.out/'cap_refusal'
        capped.mkdir()
        reject('byte_cap_refuses_whole_record','complete scientific output byte bound',
               lambda:R.emit_codes(capped,{b'[0]\n'},guard))
        done('byte_refusal_leaves_no_partial_shard',not list(capped.iterdir()))
    finally:
        R.POLICY = original
    bundle.sweep()
    report = dict(schema='QUINTIC_SINGLE_MIDDLE_SYNTHETIC_CONTROLS_V1',status='PASS',
        manifest=bundle.manifest,inputs=bundle.refs,checks=checks,
        synthetic_graph_fixtures=4,actual_four_domain_producer_calls=0,
        original_case_credit=0,scope='Independent small domains, explicit fixtures and toy orchestration only.')
    R.write_whole(args.out,'result.json',R.canonical(report),16384)
    guard.check(145)


if __name__ == '__main__':
    main()
