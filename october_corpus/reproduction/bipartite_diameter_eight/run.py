"""Enumerate bipartite quintic graphs of order 32, girth 4 and diameter 8.

The manifest identifies the mathematical kernel and proofs. All profile
domains and fourteen side products contribute to one ordinary code set.
"""
import argparse
import hashlib
import json
import os
import stat
import sys
import time
import types
from pathlib import Path, PurePosixPath

THEORY_SHA = '76569104f5a2062be761b6e514134846d3d403ba7d27fe83265df7aef4c38a93'
TABLE_SHA = '458b6914b4164d23398677f5c98099827343619f0b1c78d9006b773ccc7aabad'
POLICY = dict(rss_mib=128, outer_seconds=150, science_seconds=120,
    ram_admission_gib=4, ram_floor_gib=3, disk_admission_gib=10,
    disk_floor_gib=8, pairs=65536, codes=65536, local_forms=65536,
    shard_bytes=2097152, shard_records=4096, output_bytes=16777216,
    code_bytes=1024, source_namespace=65536, input_extent=262144,
    input_reads=1048576, metadata_bytes=65536, shards=32)
ROLES = ('runner','theory','controls','table','normal_form',
    'normal_form_review','canonicalization','canonicalization_review',
    'mathematical_review','supervisor','runtime_base','requirements')
ENVIRONMENT = ('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG',
               'OPENSSL_CONF','OPENSSL_MODULES')


def need(ok, why):
    if not ok:
        raise ValueError(why)


def integer(value, lo, hi):
    return type(value) is int and lo <= value <= hi


def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),
        ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')


def strict(raw):
    def pairs(items):
        value = {}
        for key,item in items:
            need(key not in value,'duplicate JSON key')
            value[key] = item
        return value
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda value:(_ for _ in ()).throw(ValueError('finite JSON')))


def signature(value):
    return (value.st_dev,value.st_ino,value.st_mode,value.st_nlink,
            value.st_size,value.st_mtime_ns,value.st_ctime_ns)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def hex_digest(value):
    return type(value) is str and len(value) == 64 and set(value) <= set('0123456789abcdef')


def relative(root, name):
    need(type(name) is str and 1 <= len(name) <= 160 and '\\' not in name,
         'bounded relative artifact name')
    parsed = PurePosixPath(name)
    need(not parsed.is_absolute() and str(parsed) == name
         and all(part not in ('','.','..') for part in parsed.parts),
         'literal relative artifact path')
    path = root.joinpath(*parsed.parts)
    need(path.resolve(strict=True) == path,'ordinary artifact path without symlinks')
    return path


def descriptor(name, raw):
    return dict(path=name,bytes=len(raw),sha256=digest(raw))


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


class Bundle:
    """Closed relative input set, with actual whole reads on both sweeps."""
    def __init__(self, root, manifest_name, manifest_sha):
        self.root = root
        self.read_bytes = 0
        path = relative(root,manifest_name)
        raw = read_file(path,16384)
        self.read_bytes += len(raw)
        need(hex_digest(manifest_sha) and digest(raw) == manifest_sha,
             'exact release manifest digest')
        self.manifest = descriptor(manifest_name,raw)
        value = strict(raw)
        need(set(value) == {'schema','files','policy','scope'}
             and value['schema'] == 'QUINTIC_BIPARTITE_PUBLIC_REPRODUCTION_V1'
             and value['policy'] == POLICY and set(value['files']) == set(ROLES),
             'portable release manifest')
        self.refs = value['files']
        self.rows = {manifest_name:self.manifest}
        for ref in self.refs.values():
            need(type(ref) is dict and set(ref) == {'path','bytes','sha256'}
                 and integer(ref['bytes'],0,262144) and hex_digest(ref['sha256']),
                 'complete relative whole-file descriptor')
            relative(root,ref['path'])
            need(ref['path'] not in self.rows,'one role and version per artifact path')
            self.rows[ref['path']] = ref
        need(sum(ref['bytes'] for ref in self.rows.values()) <= POLICY['input_extent'],
             'declared input extent bound')
        need(sum(self.refs[k]['bytes'] for k in ('runner','theory','controls','supervisor','runtime_base'))
             <= POLICY['source_namespace'],'Source namespace bound')
        need(self.refs['theory']['bytes'] == 19822
             and self.refs['theory']['sha256'] == THEORY_SHA
             and self.refs['table']['bytes'] == 3938
             and self.refs['table']['sha256'] == TABLE_SHA,
             'retained kernel and table')

    def read(self, ref):
        need(self.rows.get(ref['path']) == ref,'declared exact relative input')
        need(self.read_bytes+ref['bytes'] <= POLICY['input_reads'],'fixed small whole-input read allowance')
        raw = read_file(relative(self.root,ref['path']),ref['bytes'])
        need(descriptor(ref['path'],raw) == ref,'whole input digest and size')
        self.read_bytes += len(raw)
        return raw

    def sweep(self):
        for name in sorted(self.rows):
            self.read(self.rows[name])


def activate(bundle):
    need(relative(bundle.root,bundle.refs['runner']['path']) == Path(__file__).resolve(strict=True),
         'truthful current runner identity')
    bundle.sweep()
    raw = bundle.read(bundle.refs['theory'])
    module = types.ModuleType('retained_quintic_bipartite_theory')
    module.__file__ = str(relative(bundle.root,bundle.refs['theory']['path']))
    exec(compile(raw,module.__file__,'exec',dont_inherit=True),module.__dict__)
    table = strict(bundle.read(bundle.refs['table']))
    need(type(table) is dict and table['schema'] ==
         'F009_BIPARTITE_QUINTIC_FOURTEEN_SYMBOLIC_MIDDLE_SKELETONS_V1'
         and canonical(table['rows']) == canonical([module.row_data(i) for i in range(1,15)]),
         'all fourteen table rows')
    need(module.TABLE_SHA == TABLE_SHA,'table joined to retained mathematical Source')
    return module


def side_forms(T, row, side, engine, guard, totals):
    profiles = T.Profiles(row,side,guard)
    total = profiles.total()
    need(integer(total,0,54264),'proved raw profile bound')
    forms,seen = [],set()
    next_profile = 0
    omission_candidates = orbit_profiles = 0
    for ordinal,masks in profiles.interval(0,total):
        guard.tick()
        need(ordinal == next_profile,'complete deterministic profile order')
        next_profile += 1
        local,counts = engine.forms(row,side,masks)
        omission_candidates += counts['omission_candidates']
        orbit_profiles += counts['profile_orbit_representative']
        for code in local:
            T.check_side(row,side,code)
            need(code not in seen,'distinct local forms in the complete profile domain')
            seen.add(code)
            forms.append(code)
            totals['local_forms'] += 1
            need(totals['local_forms'] <= POLICY['local_forms'],'full-run local-form storage bound')
    need(next_profile == total,'whole raw profile domain completed')
    return forms,dict(side=side,raw_profiles=total,completed_profiles=next_profile,
        orbit_profiles=orbit_profiles,omission_candidates=omission_candidates,
        local_forms=len(forms))


def enumerate_all(T, guard):
    engine = T.Engine(guard)
    codes = set()
    totals = dict(local_forms=0,pairs=0,profiles=0)
    rows = []
    for index in range(1,15):
        guard.check()
        row = T.row_data(index)
        left,lstats = side_forms(T,row,'L',engine,guard,totals)
        right,rstats = side_forms(T,row,'R',engine,guard,totals)
        pairs = len(left)*len(right)
        need(totals['pairs']+pairs <= POLICY['pairs'],'full-run pair refusal bound')
        completed = 0
        before = len(codes)
        for li,L in enumerate(left):
            for ri,R in enumerate(right):
                guard.tick()
                marked = (1,row['q'],row['t'],row['u'],row['nL'],row['nR'],
                          row['mL'],row['mR'],L,R)
                graph = T.graph_from_code(marked)
                code,witness = T.ordinary_code(graph,engine)
                need(T.witness_ok(graph,code,witness),'every full32 adjacency isomorphism witness')
                raw = canonical(code)
                need(len(raw) <= POLICY['code_bytes'],'whole ordinary code record bound')
                codes.add(raw)
                need(len(codes) <= POLICY['codes'],'full-run ordinary-code storage bound')
                completed += 1
        need(completed == pairs,'entire row Cartesian product completed')
        totals['pairs'] += completed
        totals['profiles'] += lstats['raw_profiles']+rstats['raw_profiles']
        rows.append(dict(row=index,left=lstats,right=rstats,pairs=pairs,
            completed_pairs=completed,new_ordinary_codes=len(codes)-before))
        del left,right
    need(len(rows) == 14 and len(rows)*2 == 28,'all skeleton and side domains completed')
    return codes,rows,totals


def sync(path):
    fd = os.open(path,os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_whole(root, name, raw, cap):
    need(len(raw) <= cap and '/' not in name and name not in ('','.','..'),
         'bounded complete output artifact')
    staged,target = root/(name+'.staged'),root/name
    need(not os.path.lexists(staged) and not os.path.lexists(target),'fresh output artifact names')
    with staged.open('xb') as stream:
        need(stream.write(raw) == len(raw),'whole output write')
        stream.flush()
        os.fsync(stream.fileno())
    need(read_file(staged,cap) == raw,'actual whole staged output authentication')
    os.replace(staged,target)
    sync(root)
    return descriptor(name,raw)


def emit_codes(output, codes, guard):
    shards = []
    pending = []
    size = records = total_bytes = 0
    checksum = hashlib.sha256()
    previous = None
    def finish():
        nonlocal size,pending
        need(len(shards) < POLICY['shards'],'bounded output shard count')
        raw = b''.join(pending)
        ref = write_whole(output,'codes-%03d.jsonl'%len(shards),raw,POLICY['shard_bytes'])
        shards.append(dict(ref,records=len(pending)))
        pending,size = [],0
    for raw in sorted(codes):
        guard.tick()
        need(type(raw) is bytes and raw.endswith(b'\n') and len(raw) <= POLICY['code_bytes']
             and (previous is None or previous < raw),'strict whole global ordinary-code order')
        if pending and (len(pending) == POLICY['shard_records'] or size+len(raw) > POLICY['shard_bytes']):
            finish()
        need(total_bytes+len(raw) <= POLICY['output_bytes'],'complete scientific output byte bound')
        pending.append(raw)
        size += len(raw)
        records += 1
        total_bytes += len(raw)
        checksum.update(raw)
        previous = raw
    if pending:
        finish()
    need(records == len(codes),'all distinct ordinary codes emitted once')
    return shards,records,total_bytes,checksum.hexdigest()


def verify_shards(output, shards, expected_records, expected_bytes, expected_sha, guard):
    checksum = hashlib.sha256()
    records = total = 0
    previous = None
    for ref in shards:
        guard.check(145)
        raw = read_file(output/ref['path'],POLICY['shard_bytes'])
        need(descriptor(ref['path'],raw) == {k:ref[k] for k in ('path','bytes','sha256')},
             'actual whole final output shard authentication')
        lines = raw.splitlines(keepends=True)
        need(len(lines) == ref['records'] <= POLICY['shard_records'],'whole final shard records')
        for line in lines:
            need(canonical(strict(line)) == line and (previous is None or previous < line),
                 'complete canonical sorted ordinary-code output')
            previous = line
        checksum.update(raw)
        records += len(lines)
        total += len(raw)
    need((records,total,checksum.hexdigest()) == (expected_records,expected_bytes,expected_sha),
             'whole code-set checksum')


def main():
    parser = argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('--manifest',default='manifest.json')
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--volume',type=Path,required=True)
    args = parser.parse_args()
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize,'ordinary -E -B -S interpreter')
    need(all(name not in os.environ for name in ENVIRONMENT),'four retained environment denials')
    need(args.out.is_absolute() and args.out.parent.resolve(strict=True) == args.out.parent
         and not os.path.lexists(args.out),'fresh absolute output directory')
    need(args.volume.is_absolute() and args.volume.resolve(strict=True) == args.volume
         and args.volume.is_dir(),'ordinary existing output volume')
    need(args.out.parent.stat().st_dev == args.volume.stat().st_dev,'disk guard covers output volume')
    bundle = Bundle(Path(__file__).resolve(strict=True).parent,args.manifest,args.manifest_sha256)
    T = activate(bundle)
    guard = T.Guard(args.volume)
    args.out.mkdir()
    codes,rows,totals = enumerate_all(T,guard)
    guard.check(145)
    shards,count,size,checksum = emit_codes(args.out,codes,guard)
    verify_shards(args.out,shards,count,size,checksum,guard)
    bundle.sweep()
    guard.check(145)
    receipt = dict(schema='QUINTIC_BIPARTITE_COMPLETE_REPRODUCTION_RECEIPT_V1',
        status='COMPLETE_FINITE_ENUMERATION',manifest=bundle.manifest,inputs=bundle.refs,
        policy=POLICY,rows=rows,totals=totals,ordinary_classes=count,
        code_set_sha256=checksum,code_set_encoding='Sorted canonical ASCII JSON lines; one LF each; concatenate listed shards.',
        shards=shards,output_data_bytes=size,
        input_read_bytes=bundle.read_bytes,elapsed_seconds=time.monotonic()-guard.start,
        all_28_profile_domains_complete=True,all_14_pair_products_complete=True,
        every_pair_full32_witness_checked=True,source_identity_rechecked=True,
        resource_closure='Outer report closes ownership and sampled resource limits.',
        scope='Bipartite quintic graphs: order 32, girth 4, diameter 8.')
    ref = write_whole(args.out,'receipt.json',canonical(receipt),POLICY['metadata_bytes'])
    guard.check(145)
    print(canonical(dict(receipt=ref,ordinary_classes=count,code_set_sha256=checksum)).decode(),end='')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc)[:1024],file=sys.stderr)
        raise SystemExit(1)
