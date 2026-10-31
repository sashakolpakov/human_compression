"""Enumerate the nonbipartite independent two-centre family.

All four nonnegative-column half domains contribute to one ordinary code
set. Their product with six left halves gives the entire centre-size-two
stratum. No expected census is an input or a stopping rule.
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

THEORY_SHA = '5d68a44042cbd1a115a6ab941879a6eceec65b61a90188f03813ac090eb12a32'
POLICY = dict(rss_mib=128, outer_seconds=150, science_seconds=120,
    ram_admission_gib=4, ram_floor_gib=3, disk_admission_gib=10,
    disk_floor_gib=8, evaluations=4096, marked_halves=4096, codes=4096,
    shard_bytes=2097152, shard_records=4096, output_bytes=2097152,
    code_bytes=1024, source_namespace=65536, input_extent=262144,
    input_reads=1048576, metadata_bytes=65536, shards=32)
ROLES = ('runner','theory','controls','single_middle_proof',
    'single_middle_review','right_half_proof','right_half_review',
    'centre_proof','centre_review','nonisolated_proof','nonisolated_review',
    'supervisor','runtime_base','requirements')
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
             and value['schema'] == 'QUINTIC_TWO_CENTRE_PUBLIC_REPRODUCTION_V1'
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
        need(self.refs['theory']['bytes'] == 12921
             and self.refs['theory']['sha256'] == THEORY_SHA,
             'exact enlarged two-centre kernel')

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
    module = types.ModuleType('enlarged_two_centre_half_theory')
    module.__file__ = str(relative(bundle.root,bundle.refs['theory']['path']))
    exec(compile(raw,module.__file__,'exec',dont_inherit=True),module.__dict__)
    return module


def frozen(value):
    return tuple(frozen(x) for x in value) if type(value) is list else value


def enumerate_all(T, guard):
    """Account for every raw cell, including proved block and cell aliases."""
    codes = set()
    domains = []
    attempted = constructed = 0
    for shape in range(1,5):
        domain = T.Domain(shape,guard)
        need((domain.na,domain.nb) == T.BOUNDS[shape-1][2:4], 'complete raw domain dimensions')
        cursor = 0
        counts = dict(margin_skips=0,port_orbit_skips=0,
                      endpoint_orbit_skips=0,constructed_halves=0,compatible_attempts=0)
        for j,ports in domain.ports(0,domain.nb):
            guard.check()
            need(cursor == j*domain.na, 'complete consecutive port blocks')
            kind,matching,stabilizer = domain.port_context(ports)
            need(kind in ('orbit','margin','compatible'), 'proved port-block disposition')
            end = (j+1)*domain.na
            if kind in ('orbit','margin'):
                counts['port_orbit_skips' if kind == 'orbit' else 'margin_skips'] += end-cursor
                cursor = end
                continue
            for i,rows in matching:
                raw = j*domain.na+i
                need(cursor <= raw < end, 'complete ordered compatible endpoint index')
                counts['margin_skips'] += raw-cursor
                cursor = raw
                need(attempted < POLICY['evaluations'], 'full-run compatible-cell bound')
                attempted += 1
                counts['compatible_attempts'] += 1
                if not domain.endpoint_representative(rows,stabilizer):
                    counts['endpoint_orbit_skips'] += 1
                    cursor += 1
                    continue
                graph = T.half_from_code((shape,ports,rows))
                code,witness = T.canonical_half(graph,guard)
                need(T.witness_ok(graph,code,witness), 'complete unrooted16vertex witness')
                line = canonical(code)
                need(len(line) <= POLICY['code_bytes'], 'whole ordinary half code bound')
                codes.add(line)
                constructed += 1
                counts['constructed_halves'] += 1
                need(constructed <= POLICY['marked_halves'] and len(codes) <= POLICY['codes'],
                     'full-run marked-half and ordinary-code bounds')
                cursor += 1
            counts['margin_skips'] += end-cursor
            cursor = end
        need(cursor == domain.na*domain.nb and cursor == sum(counts[k] for k in
             ('margin_skips','port_orbit_skips','endpoint_orbit_skips','constructed_halves')),
             'entire raw rectangle accounted for')
        need(counts['compatible_attempts'] == counts['endpoint_orbit_skips']
             +counts['constructed_halves'], 'complete compatible cells only')
        domains.append(dict(shape=shape,raw_endpoint_multisets=domain.na,
            raw_port_multisets=domain.nb,completed_raw_interval=[0,cursor],counters=counts))
    need(len(domains) == 4, 'all four raw domains completed')
    for line in sorted(codes):
        guard.tick()
        value = frozen(strict(line))
        graph = T.half_from_code(value)
        recovered,trace = T.canonical_half(graph,guard)
        need(canonical(recovered) == line and T.witness_ok(graph,recovered,trace),
             'every distinct ordinary code is a complete canonical fixed point')
    return codes,domains,dict(compatible_attempts=attempted,constructed_marked_halves=constructed,
        canonical_fixed_points_checked=len(codes))


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
         and not sys.flags.optimize, 'ordinary -E -B -S interpreter')
    need(all(name not in os.environ for name in ENVIRONMENT), 'four retained environment denials')
    need(args.out.is_absolute() and args.out.parent.resolve(strict=True) == args.out.parent
         and not os.path.lexists(args.out), 'fresh absolute output directory')
    need(args.volume.is_absolute() and args.volume.resolve(strict=True) == args.volume
         and args.volume.is_dir(), 'ordinary existing output volume')
    need(args.out.parent.stat().st_dev == args.volume.stat().st_dev, 'disk guard covers output volume')
    bundle = Bundle(Path(__file__).resolve(strict=True).parent,args.manifest,args.manifest_sha256)
    T = activate(bundle)
    guard = T.Guard(args.volume)
    args.out.mkdir()
    codes,domains,totals = enumerate_all(T,guard)
    guard.check(145)
    shards,count,size,checksum = emit_codes(args.out,codes,guard)
    verify_shards(args.out,shards,count,size,checksum,guard)
    bundle.sweep()
    guard.check(145)
    receipt = dict(schema='QUINTIC_TWO_CENTRE_COMPLETE_REPRODUCTION_RECEIPT_V1',
        status='COMPLETE_FOUR_DOMAIN_ORDINARY_UNION',manifest=bundle.manifest,inputs=bundle.refs,
        policy=POLICY,domains=domains,totals=totals,enlarged_half_count=count,
        independent_two_centre_ordinary_graphs=6*count,code_set_sha256=checksum,
        code_set_encoding='Sorted canonical ASCII JSON lines; one LF each; concatenate listed shards.',
        shards=shards,output_data_bytes=size,input_read_bytes=bundle.read_bytes,
        elapsed_seconds=time.monotonic()-guard.start,all_four_domains_complete=True,
        every_marked_half_full16_witness_checked=True,source_identity_rechecked=True,
        resource_closure='Outer report closes ownership and sampled resource limits.',
        scope='The complete nonbipartite independent centre-size-two stratum; other centre types remain separate.')
    ref = write_whole(args.out,'receipt.json',canonical(receipt),POLICY['metadata_bytes'])
    guard.check(145)
    print(canonical(dict(receipt=ref,enlarged_half_count=count,code_set_sha256=checksum)).decode(),end='')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc)[:1024],file=sys.stderr)
        raise SystemExit(1)
