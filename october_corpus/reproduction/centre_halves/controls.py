"""Independent tiny brute root/orbit fixtures; no original graphs or census."""
import hashlib
import itertools
import json
import os
from pathlib import Path
import stat
import sys
import types
import tempfile

ROOT = Path(__file__).resolve().parent

def need(ok, why):
  if not ok:
    raise ValueError(why)


def read(name, cap):
  p = ROOT/name
  a = p.lstat()
  sig = lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
  need(p.resolve() == p and stat.S_ISREG(a.st_mode) and a.st_nlink == 1 and a.st_size <= cap,'bounded bootstrap')
  with p.open('rb') as f:
    need(sig(a) == sig(os.fstat(f.fileno())),'opened bootstrap')
    raw = f.read(cap+1)
    need(sig(a) == sig(os.fstat(f.fileno())),'closed bootstrap')
  need(sig(a) == sig(p.lstat()) and len(raw) == a.st_size,'stable bootstrap')
  return raw


def main():
  need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
    and not sys.flags.optimize,'ordinary-E-B-S')
  need(all(k not in os.environ for k in ('COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES')),'environment denials')
  manifest_raw = read('manifest.json',16384)
  need(len(sys.argv)==2 and hashlib.sha256(manifest_raw).hexdigest()==sys.argv[1],'pinned manifest')
  def pairs(items):
    need(len(dict(items))==len(items),'duplicate fields')
    return dict(items)
  manifest = json.loads(manifest_raw,object_pairs_hook=pairs,
    parse_constant=lambda x:(_ for _ in ()).throw(ValueError('finite JSON')))
  raw = read('run.py',32768)
  need(manifest['program']==dict(path='run.py',bytes=len(raw),
    sha256=hashlib.sha256(raw).hexdigest()),'whole caller before activation')
  E = types.ModuleType('half_control_caller')
  E.__file__ = str(ROOT/'run.py')
  exec(compile(raw,E.__file__,'exec',dont_inherit=True),E.__dict__)
  need(E.canonical(manifest)==manifest_raw,'canonical manifest')
  raw = E.read_whole(manifest['theory'],16384)
  T = types.ModuleType('half_control_math')
  T.__file__ = str(ROOT/'halves.py')
  exec(compile(raw,T.__file__,'exec',dont_inherit=True),T.__dict__)
  E.T,E.POLICY = T,T.POLICY
  guard=T.Guard(ROOT)
  G=lambda:guard
  inputs=E.Inputs(manifest['files']+[E.reference(ROOT/'manifest.json',manifest_raw)],guard,
    59889+2*len(read('controls.py',16384))+2*manifest['program']['bytes']+manifest['theory']['bytes']+len(manifest_raw))
  inputs.authenticate_all()
  count = 0
  def check(ok):
    nonlocal count
    need(ok,'synthetic check')
    count += 1
  def refuses(f):
    nonlocal count
    try: f()
    except (ValueError,KeyError,TypeError): count += 1
    else: raise ValueError('required refusal')
  def expand(code):
    b,s,pp,aa = code
    g = [set() for _ in range(12+b)]
    edges = [(0,v) for v in range(1,6)]+[(6+x,6+y) for x,y in T.SHAPES[s-1][1]]
    for start,rows in ((1,aa),(12,pp)):
      edges += [(start+i,6+v) for i,m in enumerate(rows) for v in range(6) if m & (1 << v)]
    for x,y in edges: g[x].add(y);g[y].add(x)
    return g
  def brute(g):
    ports = [i for i,x in enumerate(g) if len(x) == 2]
    b,n = len(ports),len(g)
    best = None
    for p in range(n):
      if len(g[p]) != 5 or set(ports)&g[p] or any(set(ports)&g[a] for a in g[p]): continue
      aa = sorted(g[p])
      d = [v for v in range(n) if v != p and v not in aa and v not in ports]
      for order in itertools.permutations(d):
        guard.tick()
        edges = {(i,j) for i in range(6) for j in range(i+1,6) if order[j] in g[order[i]]}
        for s,(_,target) in enumerate(T.SHAPES,1):
          if edges != {tuple(sorted(e)) for e in target}: continue
          masks = lambda rows:tuple(sorted(sum(1 << i for i,v in enumerate(order) if v in g[a]) for a in rows))
          candidate = b,s,masks(ports),masks(aa)
          if best is None or candidate < best: best = candidate
    return best
  fixtures = (
   (4,1,(5,9,17,33),(30,46,54,58,60)),
   (3,2,(10,10,48),(29,45,53,53,58)),
   (2,4,(5,10),(53,53,57,58,58)),
   (1,11,(5,),(53,53,58,58,58)),
   (1,9,(33,),(30,46,54,58,60)))
  for code in fixtures:
    g = expand(code)
    graph = tuple(sum(1 << v for v in row) for row in g)
    check(graph == T.half_from_code(code))
    got,w = T.canonical_half(graph,T.Meter(G()))
    h=expand(got)
    check(got == brute(g) and T.witness_ok(graph,got,w)
       and sorted(w)==list(range(len(g)))
       and all({w[j] for j in h[i]}==g[w[i]] for i in range(len(w))))
    check(T.canonical_half(T.half_from_code(got),T.Meter(G()))[0] == got)
    n = len(graph)
    order = tuple(reversed(range(n)))
    check(T.canonical_half(T.ordered_graph(graph,order),T.Meter(G()))[0] == got)
  check(T.columns(fixtures[0][3])[0] == 0)
  refuses(lambda:T.validate_presentation((True,*fixtures[0][1:])))
  refuses(lambda:T.validate_presentation((4,1,(3,9,17,33),fixtures[0][3])))
  refuses(lambda:T.graph_from_edges(6,[(0,0)]))
  refuses(lambda:T.ordered_graph(T.half_from_code(fixtures[0]),(0,)*16))
  for total,parts in ((7,[(0,2),(2,7)]),(0,[(0,0)])):
    E.cover(parts,total);check(True)
  for parts in ([(0,2),(3,7)],[(0,4),(3,7)],[(0,7),(7,7)]):
    refuses(lambda parts=parts:E.cover(parts,7))
  refuses(lambda:E.cover([(False,1)],1))
  refuses(lambda:E.strict(b'{"x":NaN}'))
  refuses(lambda:E.strict(b'{"x":1,"x":2}'))
  refuses(lambda:E.relative('../escape'))
  refuses(lambda:E.relative('/absolute'))
  check(E.frozen([4,1,[5,9],[30]]) == (4,1,(5,9),(30,)))
  check(len(T.SHAPES)==14 and all(1<=len(e)<=4 for _,e in T.SHAPES))
  check(E.dimensions(2,7)[0] == 0)
  refuses(lambda:E.dimensions(True,1))
  class O:
    def __init__(self,*args): self.rows=[];self.records=0
    def append(self,rows,*args): self.rows.extend(rows);self.records+=len(rows)
    def finish(self): return dict(path='synthetic',bytes=0,sha256='0'*64)
  class D:
    na,nb=4,3
    def __init__(self,*args): pass
    def ports(self,a,b): return ((j,fixtures[0][2]) for j in range(a,b))
    def port_context(self,rows): return 'compatible',[(i,fixtures[0][3]) for i in range(4)],((),)
    def endpoint_representative(self,*args): return True
  oldD,oldC,oldO=T.Domain,T.canonical_half,E.Output
  calls=0
  def c(graph,meter):
    nonlocal calls
    calls+=1
    if calls==4: raise T.BoundedStop('synthetic stop')
    return fixtures[0],tuple(range(16))
  T.Domain,T.canonical_half,E.Output=D,c,O
  job=dict(b=4,shape=1,raw_interval=[0,None],output='synthetic')
  first=E.run_interval(job,G(),T.Meter(G()))
  check(first['completed_raw_interval']==[0,3] and first['frontier']['next_raw_cell']==3)
  second=E.run_interval(dict(job,raw_interval=[3,None]),G(),T.Meter(G()))
  check(second['completed_raw_interval']==[3,12] and second['scope_complete'] is True)
  T.Domain,T.canonical_half=oldD,oldC
  E.Output=oldO
  base=dict(schema='HB_LOCAL_RECEIPT_V1',program=manifest['program'],
    theory=manifest['theory'],manifest=E.reference(ROOT/'manifest.json',manifest_raw),
    policy=T.POLICY,proof_legs=manifest['proof_legs'],campaign='fixture',b=4,
    control_report=dict(path='control.json',bytes=3,sha256='0'*64),
    closure='LOCAL_FINAL_INPUT_AUTHENTICATION',elapsed_seconds=1,mode='enumerate')
  job=dict(base)
  check(E.checked_receipt(base,job,manifest['program'])==base)
  for patch in ({'schema':'F009_CENTRE_HALF_RECEIPT_V1'},{'root':'/root'},
      {'campaign':'stale'},{'program':{}},{'control_report':{}},{'b':True},{'closure':'SUPPORTED'}):
    refuses(lambda patch=patch:E.checked_receipt(dict(base,**patch),job,manifest['program']))
  oldroot=E.ROOT
  with tempfile.TemporaryDirectory(dir=ROOT) as directory:
    E.ROOT=Path(directory)
    (E.ROOT/'control.json').write_bytes(b'{}\n')
    base['control_report']=job['control_report']=E.reference(E.ROOT/'control.json',b'{}\n')
    (E.ROOT/'data.jsonl').write_bytes(b'')
    base['data']=E.reference(E.ROOT/'data.jsonl',b'')
    path=E.ROOT/'receipt.json'
    path.write_bytes(E.canonical(base))
    template=dict(schema='HB_TEMPLATE_V1',campaign='fixture',b=4,
      mode='collect',output='unused',job_path='new.json',control_path='control.json',
      receipt_paths=['receipt.json'],record_interval=[0,None])
    first,_=E.bind_job(template,manifest,base['manifest'])
    path.write_bytes(E.canonical(dict(base,elapsed_seconds=2)))
    second,_=E.bind_job(template,manifest,base['manifest'])
    a,b=first['interval_receipts'][0],second['interval_receipts'][0]
    check(a!=b)
    refuses(lambda:E.read_whole(a,65536))
    check(E.strict(E.read_whole(b,65536))['elapsed_seconds']==2)
    refuses(lambda:E.Inputs([a,b],guard))
    refuses(lambda:E.request_shape(dict(second,Root_review={})))
    check(E.request_shape(second) is None)
  E.ROOT=oldroot
  # A missing side cannot be replaced by a locally valid empty receipt.
  olddim=E.dimensions
  E.dimensions=lambda *args:(0,1,(),())
  shapes=[s for s,(_,edges) in enumerate(T.SHAPES,1) if len(edges)==1]
  ref=dict(path='synthetic',bytes=0,sha256='0'*64)
  job=dict(job,interval_receipts=[ref])
  empty=dict(base,shape=shapes[0],raw_domain=0,raw_endpoint_multisets=0,raw_port_multisets=1,
    requested_raw_interval=[0,0],completed_raw_interval=[0,0],scope_complete=True,records=0,
    counters=dict(margin_skips=0,port_orbit_skips=0,endpoint_orbit_skips=0,
      constructed_halves=0,compatible_attempts=0))
  class I:
    def document(self,*args):return empty
  check(len(E.interval_family(job,None,I(),manifest['program'])[2])==1)
  empty=dict(empty,b=3,shape=2)
  refuses(lambda:E.interval_family(dict(job,b=3),None,I(),manifest['program']))
  E.dimensions=olddim
  inputs.authenticate_all(final=True)
  guard.check()
  report = dict(schema='HB_LOCAL_CONTROLS_V1',status='PASS',checks=count,
    program=manifest['program'],theory=manifest['theory'],
    manifest=E.reference(ROOT/'manifest.json',manifest_raw),actual_half_interval_jobs=0,
    expected_census_count_used=False,scope='Synthetic mathematical and local-file checks only')
  print(E.canonical(report).decode(),end='')


if __name__ == '__main__':
  main()
