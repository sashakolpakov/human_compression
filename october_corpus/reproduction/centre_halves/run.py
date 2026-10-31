"""Bounded local enumeration and ordinary unions of centre-three halves.

Local file bindings are not Root approval or SDK evidence.
"""
import argparse
import hashlib
import itertools
import json
import os
import stat
import sys
import time
import types
from pathlib import Path

T = None
POLICY = None
ROOT = Path(__file__).resolve().parent

def need(ok, why):
  if not ok:
    raise ValueError(why)

def integer(x, lo, hi):
  return type(x) is int and lo <= x <= hi

def canonical(value):
  return (json.dumps(value, sort_keys=True, separators=(',', ':'),
    ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')

def strict(raw):
  def pairs(items):
    result = {}
    for key, value in items:
      need(key not in result, 'duplicate JSON field')
      result[key] = value
    return result
  return json.loads(raw, object_pairs_hook=pairs,
    parse_constant=lambda value: (_ for _ in ()).throw(ValueError('finite JSON')))

def frozen(value):
  return tuple(frozen(x) for x in value) if type(value) is list else value

def file_signature(value):
  return (value.st_dev,value.st_ino,value.st_mode,value.st_nlink,
      value.st_size,value.st_mtime_ns,value.st_ctime_ns)

def relative(path):
  need(type(path) is str and path and not Path(path).is_absolute()
    and all(x not in ('','.','..') for x in path.split('/'))
    and '\\' not in path, 'relative path')
  target = ROOT/path
  need(target.parent.resolve(strict=True) == target.parent, 'parent path')
  return target

def reference(path, raw):
  return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(raw),
        sha256=hashlib.sha256(raw).hexdigest())

def pin_shape(ref):
  need(type(ref) is dict and set(ref) == {'path','bytes','sha256'}
    and integer(ref['bytes'],0,8*2**20) and type(ref['sha256']) is str
    and len(ref['sha256']) == 64 and set(ref['sha256']) <= set('0123456789abcdef'),
    'file descriptor')
  relative(ref['path'])

def stable_read(name, cap, size=None):
  path = relative(name)
  before = path.lstat()
  need(path.resolve(strict=True) == path and stat.S_ISREG(before.st_mode)
    and before.st_nlink == 1 and 0 <= before.st_size <= cap
    and (size is None or before.st_size == size), 'bounded regular file')
  with path.open('rb') as stream:
    need(file_signature(os.fstat(stream.fileno())) == file_signature(before), 'opened identity')
    raw = stream.read(before.st_size+1)
    need(file_signature(os.fstat(stream.fileno())) == file_signature(before), 'closed identity')
  need(file_signature(path.lstat()) == file_signature(before)
    and len(raw) == before.st_size, 'stable whole file')
  return reference(path,raw),raw

def read_whole(ref, cap):
  pin_shape(ref)
  observed,raw = stable_read(ref['path'],cap,ref['bytes'])
  need(observed == ref, 'whole pinned identity')
  return raw

class Inputs:
  def __init__(self, rows, guard, bootstrap_read_upper=0):
    self.guard = guard
    self.rows = {}
    need(integer(bootstrap_read_upper, 0, 262144), 'bounded declared-artifact bootstrap')
    self.read_bytes = bootstrap_read_upper
    self.closing = False
    for ref in rows:
      pin_shape(ref)
      need(self.rows.get(ref['path'], ref) == ref, 'one input version')
      self.rows[ref['path']] = ref
    need(len(self.rows) <= 1024 and sum(r['bytes'] for r in self.rows.values()) <= POLICY['input_extent'],
      'finite unique declared')
    self.extent = sum(r['bytes'] for r in self.rows.values())

  def read(self, ref, cap=2**21):
    need(self.rows.get(ref['path']) == ref, 'declared ordinary input')
    reserve = 0 if self.closing else self.extent
    if self.read_bytes+ref['bytes']+reserve+2**21+65536 > POLICY['read_bytes']:
      raise T.BoundedStop('read budget reserves closure')
    raw = read_whole(ref, cap)
    self.read_bytes += len(raw)
    return raw

  def document(self, ref, cap=65536):
    return strict(self.read(ref, cap))

  def authenticate_all(self, final=False):
    self.closing = final
    for path in sorted(self.rows):
      self.read(self.rows[path], 8*2**20)
      self.guard.check(145)

class Output:
  def __init__(self, directory):
    self.path = relative(directory)
    need(self.path.is_absolute() and self.path.parent.resolve(strict=True) == self.path.parent
      and not os.path.lexists(self.path), 'fresh output')
    self.path.mkdir()
    self.stage = self.path/'data.jsonl.staged'
    self.stream = self.stage.open('xb')
    self.digest = hashlib.sha256()
    self.bytes = 0
    self.records = 0

  def append(self, records, line_limit):
    raw = [canonical(record) for record in records]
    need(all(len(item) <= line_limit for item in raw), 'whole bounded individual')
    if self.bytes+sum(map(len, raw)) > POLICY['data_bytes']-65536 or self.records+len(raw) > POLICY['records']:
      raise T.BoundedStop('complete-unit output allowance')
    payload = b''.join(raw)
    need(self.stream.write(payload) == len(payload), 'atomic unit write')
    self.digest.update(payload)
    self.bytes += len(payload)
    self.records += len(raw)

  def finish(self):
    self.stream.flush()
    os.fsync(self.stream.fileno())
    self.stream.close()
    target = self.path/'data.jsonl'
    expected = dict(path=self.stage.relative_to(ROOT).as_posix(), bytes=self.bytes, sha256=self.digest.hexdigest())
    read_whole(expected, POLICY['data_bytes'])
    os.replace(self.stage, target)
    sync(self.path)
    return dict(expected, path=target.relative_to(ROOT).as_posix())

def sync(path):
  fd = os.open(path, os.O_RDONLY)
  try:
    os.fsync(fd)
  finally:
    os.close(fd)

def write_document(path, value):
  raw = canonical(value)
  need(len(raw) <= 65536 and not os.path.lexists(path), 'fresh document64KiB')
  staged = path.with_name(path.name+'.staged')
  with staged.open('xb') as stream:
    need(stream.write(raw) == len(raw), 'whole document write')
    stream.flush()
    os.fsync(stream.fileno())
  read_whole(reference(staged, raw), 65536)
  os.replace(staged, path)
  sync(path.parent)
  return reference(path, raw)

def dimensions(b,shape):
  need(integer(b,1,4) and integer(shape,1,14)
    and len(T.SHAPES[shape-1][1]) == 5-b, 'b and complete')
  graph = T.graph_from_edges(6,T.SHAPES[shape-1][1])
  aa,bb = T.independent_rows(graph,4),T.independent_rows(graph,2)
  return T.math.comb(len(aa)+4,5),T.math.comb(len(bb)+b-1,b),aa,bb

def run_interval(job, guard, meter):
  domain = T.Domain(job['b'],job['shape'],meter)
  total = domain.na*domain.nb
  start,stop = job['raw_interval']
  stop = total if stop is None else stop
  need(integer(start,0,total) and integer(stop,start,total), 'finite raw rectangle')
  output = Output(job['output'])
  cursor = start
  counts = dict(margin_skips=0,port_orbit_skips=0,endpoint_orbit_skips=0,
         compatible_attempts=0,constructed_halves=0)
  reason = None
  first = start//domain.na if total else 0
  last = (stop-1)//domain.na+1 if stop > start else first
  try:
    for j,ports in domain.ports(first,last):
      guard.check()
      lo,hi = max(start,j*domain.na),min(stop,(j+1)*domain.na)
      need(cursor == lo, 'complete ordered port-block')
      kind,matching,stabilizer = domain.port_context(ports)
      if kind in ('orbit','margin'):
        counts['port_orbit_skips' if kind == 'orbit' else 'margin_skips'] += hi-cursor
        cursor = hi
        continue
      for i,rows in matching:
        raw = j*domain.na+i
        if raw < lo:
          continue
        if raw >= hi:
          break
        counts['margin_skips'] += raw-cursor
        cursor = raw
        guard.check()
        if counts['compatible_attempts'] >= POLICY['evaluations']:
          raise T.BoundedStop('4096 compatible evaluations')
        counts['compatible_attempts'] += 1
        if not domain.endpoint_representative(rows,stabilizer):
          counts['endpoint_orbit_skips'] += 1
          cursor = raw+1
          continue
        marked = job['b'],job['shape'],ports,rows
        graph = T.half_from_code(marked)
        ordinary,permutation = T.canonical_half(graph,meter)
        need(T.witness_ok(graph,ordinary,permutation), 'whole ordinary isomorphism')
        output.append([(raw,j,i,marked,ordinary,permutation)],1024)
        counts['constructed_halves'] += 1
        cursor = raw+1
      counts['margin_skips'] += hi-cursor
      cursor = hi
  except T.BoundedStop as exc:
    reason = str(exc)
  need(cursor-start == sum(counts[k] for k in ('margin_skips','port_orbit_skips',
       'endpoint_orbit_skips','constructed_halves'))
    and output.records == counts['constructed_halves'], 'entire raw-prefix accounting')
  data = output.finish()
  return dict(b=job['b'],shape=job['shape'],raw_domain=total,
    raw_endpoint_multisets=domain.na,raw_port_multisets=domain.nb,
    requested_raw_interval=[start,stop],completed_raw_interval=[start,cursor],
    scope_complete=cursor == stop,frontier=None if cursor == stop else
    dict(next_raw_cell=cursor,port_multiset=cursor//domain.na,endpoint_multiset=cursor%domain.na),
    counters=counts,stop_reason=reason,data=data,records=output.records,h_b=None)

def cover(intervals, total):
  need(intervals and integer(total,0,2**40), 'explicit complete interval')
  cursor = 0
  for lo,hi in sorted(intervals):
    need(integer(lo,0,total) and integer(hi,lo,total) and lo == cursor
      and (hi > lo or total == 0 and len(intervals) == 1), 'no gap, overlap')
    cursor = hi
  need(cursor == total, 'entire finite domain')

def interval_family(job, gate, inputs, own):
  refs = job['interval_receipts']
  need(type(refs) is list and 1 <= len(refs) <= 128
    and len({r['path'] for r in refs}) == len(refs), 'distinct bounded interval')
  coverage = {s:[] for s,(_,e) in enumerate(T.SHAPES,1) if len(e) == 5-job['b']}
  docs = []
  for ref in refs:
    doc = accepted(ref,'accepted_interval_receipts',job,gate,inputs,own)
    shape = doc['shape']
    na,nb,_,_ = dimensions(job['b'],shape)
    lo,hi = doc['completed_raw_interval']
    start,stop = doc['requested_raw_interval']
    need(doc['mode'] == 'enumerate' and shape in coverage
      and integer(lo,0,na*nb) and integer(hi,lo,na*nb)
      and type(start) is int and start == lo and integer(stop,hi,na*nb)
      and doc['scope_complete'] is (hi == stop)
      and integer(doc['raw_domain'],na*nb,na*nb) and integer(doc['raw_endpoint_multisets'],na,na)
      and integer(doc['raw_port_multisets'],nb,nb) and integer(doc['records'],0,4096), 'exact interval prefix')
    c = doc['counters']
    keys = ('margin_skips','port_orbit_skips','endpoint_orbit_skips','constructed_halves')
    need(all(integer(c[k],0,na*nb) for k in keys) and sum(c[k] for k in keys) == hi-lo
      and c['constructed_halves'] == doc['records']
      and integer(c['compatible_attempts'],0,4096)
      and 0 <= c['compatible_attempts']-c['endpoint_orbit_skips']-doc['records'] <= 1,
      'full prefix and')
    coverage[shape].append((lo,hi))
    docs.append((shape,lo,ref,doc))
  for shape,intervals in coverage.items():
    na,nb,_,_ = dimensions(job['b'],shape)
    cover(intervals,na*nb)
  docs.sort(key=lambda x:(x[0],x[1],x[2]['path']))
  return docs,hashlib.sha256(canonical(refs)).hexdigest(),coverage

def code_lines(raw, expected):
  lines = raw.splitlines(keepends=True)
  need(len(lines) == expected, 'whole output record')
  for line in lines:
    need(len(line) <= 1024 and canonical(strict(line)) == line, 'whole canonical bounded')
    yield line,strict(line)

def collect(job, gate, inputs, own, guard, meter):
  docs,family,coverage = interval_family(job,gate,inputs,own)
  total = sum(d['records'] for _,_,_,d in docs)
  start,stop = job['record_interval']
  stop = total if stop is None else stop
  need(integer(start,0,total) and integer(stop,start,total)
    and stop-start <= POLICY['evaluations']//2, 'bounded selected record')
  unique = set()
  position = selected = 0
  for shape,lo,_,doc in docs:
    na,nb,aa,bb = dimensions(job['b'],shape)
    aa = tuple(itertools.combinations_with_replacement(aa,5))
    bb = tuple(itertools.combinations_with_replacement(bb,job['b']))
    previous = lo-1
    for line,record in code_lines(inputs.read(doc['data']),doc['records']):
      guard.tick()
      need(type(record) is list and len(record) == 6, 'complete marked record')
      raw,j,i,marked,code,witness = record
      need(integer(raw,previous+1,doc['completed_raw_interval'][1]-1)
        and integer(j,0,nb-1) and integer(i,0,na-1) and raw == j*na+i,
        'ordered original raw-cell')
      if start <= position < stop:
        marked,code,witness = frozen(marked),frozen(code),frozen(witness)
        need(marked == (job['b'],shape,bb[j],aa[i]), 'whole original row')
        graph = T.half_from_code(marked)
        need(T.witness_ok(graph,code,witness), 'full carried ordinary')
        unique.add(canonical(code))
        selected += 1
      position += 1
      previous = raw
  need(position == total and selected == stop-start, 'complete selected record')
  output = Output(job['output'])
  for raw in sorted(unique):
    guard.check()
    code = frozen(strict(raw))
    recovered,witness = T.canonical_half(T.half_from_code(code),meter)
    need(canonical(recovered) == raw and T.witness_ok(T.half_from_code(code),recovered,witness),
      'every output ordinary')
    output.append([code],1024)
  complete = start == 0 and stop == total
  return dict(b=job['b'],scope_complete=True,frontier=None,data=output.finish(),records=output.records,
    record_domain=total,record_interval=[start,stop],interval_family_sha256=family,
    interval_receipts=job['interval_receipts'],raw_coverage=coverage,
    compatible_evaluations=selected+len(unique),complete_ordinary_union=complete,
    h_b=len(unique) if complete else None)

def checked_receipt(doc, job, own):
  need(type(doc) is dict and not set(doc)&{'root','Root_review','RootSDK','adopted'}
    and doc['schema'] == 'HB_LOCAL_RECEIPT_V1'
    and doc['program'] == own and doc['policy'] == POLICY
    and all(doc[k] == job[k] for k in ('theory','manifest','proof_legs','campaign','control_report'))
    and type(doc['b']) is int and doc['b'] == job['b']
    and doc['closure'] == 'LOCAL_FINAL_INPUT_AUTHENTICATION',
    'same local context, no Root authority')
  return doc

def accepted(ref, role, job, gate, inputs, own):
  need(role == 'accepted_interval_receipts' and ref in job['interval_receipts'],
    'explicit local interval descriptor')
  return checked_receipt(inputs.document(ref),job,own)

BOOT = []
BOOT_BYTES = 59889 + Path(__file__).stat().st_size

def acquire(name, cap, expected=None):
  global BOOT_BYTES
  need(0 <= BOOT_BYTES <= 262144, 'bootstrap budget')
  ref,raw = stable_read(name,min(cap,262144-BOOT_BYTES))
  need(expected is None or ref['sha256'] == expected, 'pinned bootstrap')
  BOOT_BYTES += len(raw)
  BOOT.append(ref)
  return ref,raw

def request_shape(job):
  common = set('schema program theory manifest policy proof_legs inputs control_report campaign b mode output binding'.split())
  extra = {'enumerate':{'shape','raw_interval'},
    'collect':{'interval_receipts','record_interval'}}
  need(type(job) is dict and job['mode'] in extra and set(job) == common|extra[job['mode']]
    and job['schema'] == 'HB_LOCAL_JOB_V1'
    and job['binding'] == 'LOCAL_FILES_NO_AUTHORITY'
    and integer(job['b'],1,4) and type(job['campaign']) is str
    and 1 <= len(job['campaign']) <= 64
    and set(job['campaign']) <= set('abcdefghijklmnopqrstuvwxyz0123456789_-'), 'typed local request')
  relative(job['output'])
  part = job['raw_interval'] if job['mode'] == 'enumerate' else job['record_interval']
  need(type(part) is list and len(part) == 2 and integer(part[0],0,2**40)
    and (part[1] is None or integer(part[1],part[0],2**40)), 'half-open requested interval')
  if job['mode'] == 'enumerate':
    need(integer(job['shape'],1,14), 'declared side shape')
  else:
    refs = job['interval_receipts']
    need(type(refs) is list and 1 <= len(refs) <= 128
      and len({r['path'] for r in refs}) == len(refs), 'distinct local intervals')
    for ref in refs: pin_shape(ref)

def bind_job(template, manifest, manifestref):
  need(template['schema'] == 'HB_TEMPLATE_V1', 'local template')
  control,raw = acquire(template['control_path'],65536)
  need(canonical(strict(raw)) == raw, 'canonical controls')
  job = {k:v for k,v in template.items()
    if k not in ('job_path','control_path','receipt_paths')}
  job.update(schema='HB_LOCAL_JOB_V1',program=manifest['program'],
    theory=manifest['theory'],manifest=manifestref,policy=POLICY,
    proof_legs=manifest['proof_legs'],inputs=[],control_report=control,
    binding='LOCAL_FILES_NO_AUTHORITY')
  paths = template['receipt_paths']
  need(type(paths) is list and len(paths) <= 128 and len(set(paths)) == len(paths)
    and (not paths if job['mode'] == 'enumerate' else bool(paths)), 'finite receipt list')
  refs,rows = [],{}
  for name in paths:
    ref,raw = acquire(name,65536)
    doc = checked_receipt(strict(raw),job,manifest['program'])
    need(canonical(doc) == raw and doc['mode'] == 'enumerate', 'local enumeration')
    pin_shape(doc['data'])
    refs.append(ref)
    for r in (ref,doc['data']):
      need(rows.get(r['path'],r) == r, 'one input version')
      rows[r['path']] = r
  job['inputs'] = [rows[p] for p in sorted(rows)]
  if job['mode'] == 'collect':job['interval_receipts'] = refs
  request_shape(job)
  target = relative(template['job_path'])
  need(not os.path.lexists(target) and not os.path.lexists(relative(job['output'])), 'fresh targets')
  return job,target

def main():
  global T,POLICY
  parser = argparse.ArgumentParser(allow_abbrev=False)
  parser.add_argument('--manifest',nargs=2,required=True)
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--job',nargs=2)
  group.add_argument('--bind',nargs=2)
  parser.add_argument('--volume',required=True)
  args = parser.parse_args()
  need(Path(args.volume).resolve(strict=True) == ROOT, 'monitor bundle volume')
  need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
    and not sys.flags.optimize, 'ordinary-E-B-S interpreter')
  need(all(k not in os.environ for k in ('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG',
    'OPENSSL_CONF','OPENSSL_MODULES')), 'four environment denials')
  manifestref,raw = acquire(args.manifest[0],16384,args.manifest[1])
  manifest = strict(raw)
  need(canonical(manifest) == raw and manifest['schema'] == 'HB_LOCAL_MANIFEST_V1',
    'canonical local manifest')
  own = manifest['program']
  ref,raw = acquire(own['path'],32768,own['sha256'])
  need(ref == own and relative(own['path']) == Path(__file__).resolve(strict=True), 'whole caller')
  theory = manifest['theory']
  ref,raw = acquire(theory['path'],16384,theory['sha256'])
  need(ref == theory, 'whole unchanged mathematical kernel')
  T = types.ModuleType('F009_centre_half_math')
  T.__file__ = str(relative(theory['path']))
  exec(compile(raw,T.__file__,'exec',dont_inherit=True),T.__dict__)
  POLICY = T.POLICY
  need(manifest['policy'] == POLICY and type(manifest['files']) is list
    and all(r in manifest['files'] for r in (own,theory))
    and sum(r['bytes'] for r in manifest['active_sources']) <= 65536
    and all(r in manifest['files'] for r in manifest['active_sources']), 'unchanged role policy and Source cap')
  guard = T.Guard(args.volume)
  pair = args.bind or args.job
  requestref,raw = acquire(pair[0],65536,pair[1])
  request = strict(raw)
  need(canonical(request) == raw, 'canonical whole request')
  if args.bind:
    job,target = bind_job(request,manifest,manifestref)
  else:
    job = request
  request_shape(job)
  need(job['manifest'] == manifestref and all(job[k] == manifest[k]
    for k in ('program','theory','policy','proof_legs')), 'exact local context')
  inputs = Inputs(manifest['files']+job['inputs']+job['proof_legs']+BOOT+
    [job['control_report']],guard,BOOT_BYTES)
  inputs.authenticate_all()
  controls = inputs.document(job['control_report'])
  need(controls['schema'] == 'HB_LOCAL_CONTROLS_V1'
    and controls['status'] == 'PASS' and controls['program'] == own
    and controls['theory'] == theory and controls['manifest'] == manifestref
    and controls['actual_half_interval_jobs'] == 0, 'same local generic controls')
  if args.bind:
    inputs.authenticate_all(final=True)
    ref = write_document(target,job)
    guard.check(145)
    print(canonical(dict(local_job=ref,authority='NO_ROOT_APPROVAL')).decode(),end='')
    return
  meter = T.Meter(guard)
  result = run_interval(job,guard,meter) if job['mode'] == 'enumerate' else collect(job,None,inputs,own,guard,meter)
  guard.check(145)
  inputs.authenticate_all(final=True)
  receipt = dict(result,schema='HB_LOCAL_RECEIPT_V1',mode=job['mode'],
    program=own,theory=theory,manifest=manifestref,request=requestref,
    campaign=job['campaign'],control_report=job['control_report'],proof_legs=job['proof_legs'],
    policy=POLICY,work=meter.counts,elapsed_seconds=time.monotonic()-guard.start,
    declared_artifact_read_bytes=inputs.read_bytes,readback_upper_bytes=2162688,
    closure='LOCAL_FINAL_INPUT_AUTHENTICATION',independent_review=False,
    new_credit=0)
  ref = write_document(relative(job['output'])/'receipt.json',receipt)
  guard.check(145)
  print(canonical(dict(receipt=ref,scope_complete=result['scope_complete'],frontier=result.get('frontier'))).decode(),end='')

if __name__ == '__main__':
  main()

