"""Compose complete local order32 censuses; no graph algorithm is imported.

Receipts are locally authenticated completion records, not Root/SDK authority.
The ordinary exhaustion and disjointness theorems remain documentary premises.
"""
import argparse,hashlib,json,math,os,resource,stat,sys,time
from pathlib import Path,PurePosixPath

POLICY=dict(input_extent=8*2**20,read_bytes=32*2**20,file_bytes=2*2**20,
  paths=256,line_bytes=1024,output_bytes=65536,source_namespace=65536,
  rss_bytes=128*2**20,science_seconds=120,outer_seconds=150,
  ram_admission_gib=4,ram_floor_gib=3,disk_admission_gib=10,disk_floor_gib=8)
MANIFESTS=dict(bipartite='37f9851f85762437b31818099e1f40abd00bc9825d0c7bc2786a275407034d7d',
  two_centre='27c1d89c56ffdef67ba6a71ab009a0386d6071bd783e5060eddf3385147596ea',
  centre_halves='a2afc046ed7d962b22021e57c1c0cf26f8c3534d87ad36d1cb83bb65b0884e5f')
KERNELS=dict(bipartite='76569104f5a2062be761b6e514134846d3d403ba7d27fe83265df7aef4c38a93',
  two_centre='5d68a44042cbd1a115a6ab941879a6eceec65b61a90188f03813ac090eb12a32',
  centre_halves='1129b778b53fe4bc550731be53bd587a4dd553aeeea16f23557d47e5c2e5f61b')
SHAPES={1:[8,9,10,11,12,13,14],2:[4,5,6,7],3:[2,3],4:[1]}
PROOF_CLOSURE_SHA='9a93d3bf75c639a7b7d96590408a249d746880b5aa08ee0263be3a046f486eb1'
TARGET=dict(order=32,degree=5,girth=4,diameter=8,ordinary_uncolored_isomorphism=True)

def need(ok,why):
  if not ok:raise ValueError(why)

def integer(x,lo=0,hi=2**40):
  return type(x)is int and lo<=x<=hi

def same(a,b):
  if type(a)is not type(b):return False
  if type(a)is dict:return a.keys()==b.keys()and all(same(a[k],b[k])for k in a)
  if type(a)is list:return len(a)==len(b)and all(same(x,y)for x,y in zip(a,b))
  return a==b

def canonical(x):
  return(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')

def strict(raw):
  def pairs(items):
    out={}
    for k,v in items:need(k not in out,'duplicate JSON field');out[k]=v
    return out
  def bad(_):raise ValueError('finite JSON required')
  def number(s):
    x=float(s);need(math.isfinite(x),'finite JSON number');return x
  return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad,parse_float=number)

def relative(name):
  need(type(name)is str and name and '\\'not in name,'relative POSIX path')
  p=PurePosixPath(name)
  need(not p.is_absolute()and p.as_posix()==name
    and all(s not in ('','.','..')for s in name.split('/')),'no absolute/dot/traversal path')
  return name

def descriptor(ref,cap=2*2**20):
  need(type(ref)is dict and set(ref)=={'path','bytes','sha256'}
    and integer(ref['bytes'],0,cap)and type(ref['sha256'])is str
    and len(ref['sha256'])==64 and set(ref['sha256'])<=set('0123456789abcdef'),
    'complete bounded file descriptor')
  relative(ref['path']);return ref

def joined(base,ref):
  descriptor(ref);relative(base)
  return dict(ref,path=base+'/'+ref['path'])

def signature(s):
  return(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

class Files:
  def __init__(self,root):
    self.root=root;self.start=time.monotonic();self.read_bytes=0;self.rows={};self.signatures={}

  def check(self):
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
    need(time.monotonic()-self.start<120 and peak<POLICY['rss_bytes'],'composition128MiB120s bound')

  def path(self,name):
    p=self.root/relative(name)
    need(p.parent.resolve(strict=True)==p.parent,'canonical existing parent')
    return p

  def read(self,ref):
    descriptor(ref);p=self.path(ref['path']);a=p.lstat()
    need(p.resolve(strict=True)==p and stat.S_ISREG(a.st_mode)and a.st_nlink==1
      and a.st_size==ref['bytes'],'ordinary single-link bounded whole input')
    prior=self.rows.setdefault(ref['path'],ref)
    need(prior==ref and len(self.rows)<=POLICY['paths']
      and sum(r['bytes']for r in self.rows.values())<=POLICY['input_extent'],
      'one version and finite unique input bank')
    need(self.read_bytes+ref['bytes']<=POLICY['read_bytes'],'single complete physical-read bank')
    with p.open('rb')as stream:
      opened=os.fstat(stream.fileno());raw=stream.read(a.st_size+1);closed=os.fstat(stream.fileno())
    need(signature(a)==signature(opened)==signature(closed)==signature(p.lstat())
      and len(raw)==ref['bytes']and hashlib.sha256(raw).hexdigest()==ref['sha256'],
      'stable complete size/SHA identity')
    need(self.signatures.setdefault(ref['path'],signature(a))==signature(a),'unchanged first input identity')
    self.read_bytes+=len(raw);self.check();return raw

  def doc(self,ref):
    need(ref['bytes']<=262144,'bounded receipt/manifest document')
    return strict(self.read(ref))

  def finish(self):
    for name in sorted(self.rows):self.read(self.rows[name])
    for name,s in self.signatures.items():need(signature(self.path(name).lstat())==s,'final unchanged input')

def stream_lines(raw,expected,previous=None):
  need(integer(expected,0,65536),'typed stream-record count')
  lines=raw.splitlines(keepends=True)
  need(len(lines)==expected,'actual stream line count')
  for line in lines:
    need(len(line)<=1024 and line.endswith(b'\n')and canonical(strict(line))==line
      and(previous is None or previous<line),'complete canonical strictly sorted stream')
    previous=line
  return previous

def shards(files,receipt,receipt_ref,count):
  need(integer(count,0,65536)and type(receipt['shards'])is list
    and len(receipt['shards'])<=32,'bounded ordinary union')
  parent=str(PurePosixPath(receipt_ref['path']).parent)
  seen=set();digest=hashlib.sha256();total=records=0;previous=None
  for row in receipt['shards']:
    need(type(row)is dict and set(row)=={'path','bytes','sha256','records'}
      and integer(row['records'],1,4096)and '/'not in row['path']and row['path']not in seen,
      'distinct bounded local shard')
    seen.add(row['path']);ref={k:row[k]for k in ('path','bytes','sha256')}
    raw=files.read(joined(parent,ref));previous=stream_lines(raw,row['records'],previous)
    digest.update(raw);total+=len(raw);records+=row['records']
  need(records==count and integer(receipt['output_data_bytes'],0,16*2**20)
    and total==receipt['output_data_bytes']and digest.hexdigest()==receipt['code_set_sha256'],
    'complete count/byte/digest equality')
  return dict(records=records,bytes=total,sha256=digest.hexdigest())

def manifest(files,spec,kind):
  need(type(spec)is dict and set(spec)==({'base','manifest','collections'}if kind=='centre_halves'else {'base','manifest','receipt'}),'component roles')
  relative(spec['base']);ref=descriptor(spec['manifest'],16384)
  need(ref['path']==spec['base']+'/manifest.json'and ref['sha256']==MANIFESTS[kind],
    'frozen supported target-family manifest')
  doc=files.doc(ref)
  schemas=dict(bipartite='QUINTIC_BIPARTITE_PUBLIC_REPRODUCTION_V1',
    two_centre='QUINTIC_TWO_CENTRE_PUBLIC_REPRODUCTION_V1',centre_halves='HB_LOCAL_MANIFEST_V1')
  need(doc['schema']==schemas[kind],'correct target-family schema')
  refs=doc['files'];refs=list(refs.values())if type(refs)is dict else refs
  need(type(refs)is list and len(refs)<=64,'bounded component source/proof list')
  for r in refs:files.read(joined(spec['base'],r))
  kernel=doc['theory']if kind=='centre_halves'else doc['files']['theory']
  need(kernel['sha256']==KERNELS[kind],'correct mathematical kernel, enlarged H rather than strict subset')
  return doc,dict(path='manifest.json',bytes=ref['bytes'],sha256=ref['sha256'])

def bipartite(receipt,m,local):
  need(type(receipt)is dict and not set(receipt)&{'root','Root_review','RootSDK','adopted'},'local bipartite receipt has no Root authority')
  need(receipt.get('schema')=='QUINTIC_BIPARTITE_COMPLETE_REPRODUCTION_RECEIPT_V1'
    and receipt.get('status')=='COMPLETE_FINITE_ENUMERATION'
    and receipt.get('scope')=='Bipartite quintic graphs: order 32, girth 4, diameter 8.'
    and same(receipt.get('manifest'),local) and same(receipt.get('inputs'),m['files'])
    and same(receipt.get('policy'),m['policy']),'exact complete bipartite target family')
  for k in ['all_28_profile_domains_complete','all_14_pair_products_complete','every_pair_full32_witness_checked','source_identity_rechecked']:
    need(receipt.get(k)is True,'complete bipartite receipt '+k)
  need(type(receipt['rows'])is list and [r['row']for r in receipt['rows']]==list(range(1,15))and all(type(r['row'])is int for r in receipt['rows']),
    'all14 distinct skeleton products')
  for row in receipt['rows']:
    for side in ['left','right']:
      d=row[side];need(integer(d['raw_profiles'])and d['completed_profiles']==d['raw_profiles']
        and integer(d['completed_profiles'])and integer(d['local_forms']),'whole side profile domain')
    need(integer(row['pairs'])and integer(row['completed_pairs'])
      and row['pairs']==row['left']['local_forms']*row['right']['local_forms']==row['completed_pairs'],
      'whole side Cartesian product')
  need(integer(receipt['ordinary_classes'],0,m['policy']['codes']),'typed ordinary bipartite count')
  return receipt['ordinary_classes']

def two_centre(receipt,m,local):
  need(type(receipt)is dict and not set(receipt)&{'root','Root_review','RootSDK','adopted'},'local H receipt has no Root authority')
  need(receipt.get('schema')=='QUINTIC_TWO_CENTRE_COMPLETE_REPRODUCTION_RECEIPT_V1'
    and receipt.get('status')=='COMPLETE_FOUR_DOMAIN_ORDINARY_UNION'
    and same(receipt.get('manifest'),local) and same(receipt.get('inputs'),m['files'])
    and same(receipt.get('policy'),m['policy']),'exact enlarged nonnegative-column H family')
  for k in ['all_four_domains_complete','every_marked_half_full16_witness_checked','source_identity_rechecked']:
    need(receipt.get(k)is True,'complete enlarged H receipt '+k)
  need(type(receipt['domains'])is list and [r['shape']for r in receipt['domains']]==[1,2,3,4]and all(type(r['shape'])is int for r in receipt['domains']),
    'allfour enlarged-H shapes')
  for d in receipt['domains']:
    need(integer(d['raw_endpoint_multisets'])and integer(d['raw_port_multisets']),'typed raw rectangle')
    total=d['raw_endpoint_multisets']*d['raw_port_multisets']
    need(d['completed_raw_interval']==[0,total]and all(type(x)is int for x in d['completed_raw_interval']),
      'entire enlarged-H rectangle')
    c=d['counters'];ks=['margin_skips','port_orbit_skips','endpoint_orbit_skips','constructed_halves']
    need(all(integer(c[k])for k in ks)and sum(c[k]for k in ks)==total,'complete H prefix accounting')
  H=receipt['enlarged_half_count']
  need(integer(H,0,m['policy']['codes'])and integer(receipt['independent_two_centre_ordinary_graphs'])
    and receipt['independent_two_centre_ordinary_graphs']==6*H,'typed H/factor-six result')
  return H

def cover(intervals,total):
  need(integer(total)and type(intervals)is list and intervals,'explicit complete raw domain')
  cursor=0
  for pair in sorted(intervals):
    need(type(pair)is list and len(pair)==2 and integer(pair[0],0,total)and integer(pair[1],pair[0],total)
      and pair[0]==cursor and(pair[1]>pair[0]or total==0 and len(intervals)==1),'no gap/overlap')
    cursor=pair[1]
  need(cursor==total,'entire raw domain covered')

def hb_context(r,m,local,b):
  need(type(r)is dict and not set(r)&{'root','Root_review','RootSDK','adopted'}
    and r.get('schema')=='HB_LOCAL_RECEIPT_V1'and same(r.get('manifest'),local)
    and same(r.get('program'),m['program'])and same(r.get('theory'),m['theory'])
    and same(r.get('proof_legs'),m['proof_legs'])and same(r.get('policy'),m['policy'])
    and type(r.get('b'))is int and r['b']==b
    and r.get('closure')=='LOCAL_FINAL_INPUT_AUTHENTICATION','same Hb family/local context; no Root authority')
  need(type(r.get('campaign'))is str and 1<=len(r['campaign'])<=128,'typed local campaign')

def half_collection(files,r,ref,m,local,b,base):
  hb_context(r,m,local,b)
  need(r.get('mode')=='collect'and r.get('scope_complete')is True
    and r.get('frontier')is None and r.get('complete_ordinary_union')is True,
    'full global per-b ordinary union, not a partial collection or marked sum')
  need(integer(r['record_domain'])and r['record_interval']==[0,r['record_domain']]
    and all(type(x)is int for x in r['record_interval'])
    and integer(r['records'],0,4096)and type(r['h_b'])is int and r['h_b']==r['records'],
    'typed full collection interval/count')
  refs=r['interval_receipts'];need(type(refs)is list and 1<=len(refs)<=128
    and len({q['path']for q in refs})==len(refs),'distinct bounded Hb raw receipts')
  need(hashlib.sha256(canonical(refs)).hexdigest()==r['interval_family_sha256'],'whole raw-receipt family identity')
  coverage={s:[]for s in SHAPES[b]};totals={};marked=0
  for q in refs:
    d=files.doc(joined(base,q));hb_context(d,m,local,b)
    shape=d['shape'];need(type(shape)is int and shape in coverage and d['mode']=='enumerate','exact complete side-shape family')
    need(d['campaign']==r['campaign']and same(d['control_report'],r['control_report']),'same fresh acquisition campaign')
    n=d['raw_domain'];need(integer(n)and integer(d['raw_endpoint_multisets'])and integer(d['raw_port_multisets'])
      and n==d['raw_endpoint_multisets']*d['raw_port_multisets'],'same finite raw rectangle')
    need(totals.setdefault(shape,n)==n,'one raw domain per shape')
    pair=d['completed_raw_interval'];need(type(pair)is list and len(pair)==2 and all(type(x)is int for x in pair),'typed completed prefix')
    start,stop=d['requested_raw_interval'];lo,hi=pair
    need(integer(lo,0,n)and integer(hi,lo,n)and type(start)is int and start==lo and integer(stop,hi,n)
      and d['scope_complete']is(hi==stop),'truthful raw prefix')
    c=d['counters'];ks=['margin_skips','port_orbit_skips','endpoint_orbit_skips','constructed_halves']
    need(all(integer(c[k])for k in ks)and sum(c[k]for k in ks)==hi-lo
      and integer(d['records'],0,4096)and c['constructed_halves']==d['records'],'full raw-prefix accounting')
    # Authenticate the carried marked stream and its true record count without
    # rerunning its graph/witness algorithm or treating it as an ordinary count.
    payload=files.read(joined(base,d['data']))
    marked_lines=payload.splitlines(keepends=True)
    need(len(marked_lines)==d['records']and all(len(line)<=1024 and line.endswith(b'\n')and canonical(strict(line))==line for line in marked_lines),'whole canonical marked stream framing')
    marked+=d['records'];coverage[shape].append(pair)
  need(set(totals)==set(coverage),'every required side shape supplied')
  for s in coverage:cover(coverage[s],totals[s])
  expected={str(k):v for k,v in coverage.items()}
  need(same(r['raw_coverage'],expected) and marked==r['record_domain'],'all shapes/full source record family')
  control=files.doc(joined(base,r['control_report']))
  need(control.get('schema')=='HB_LOCAL_CONTROLS_V1'and control.get('status')=='PASS'and same(control.get('program'),m['program'])and same(control.get('theory'),m['theory'])and same(control.get('manifest'),local) and control.get('actual_half_interval_jobs')==0,'same local Hb controls report')
  data=files.read(joined(base,r['data']));stream_lines(data,r['records'])
  return r['h_b'],dict(records=r['records'],bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def combine(B,H,h):
  need(integer(B)and integer(H)and type(h)is dict and set(h)=={1,2,3,4}
    and all(integer(h[b])for b in h),'typed complete scalar inputs')
  # These are analytical equality postchecks after all productions are complete.
  need(h[1]==2 and h[2]==5,'analytical h1/h2 postchecks; no producer stopping target')
  rows=[('one_twin_class_2',6*H),('one_twin_class_3',h[1]*h[4]+h[2]*h[3]),
    ('one_twin_class_4',6),('independent_twin_classes_1_2',h[4]),
    ('independent_twin_classes_1_3',6),('independent_twin_classes_2_2',4),
    ('centre_P3',6),('centre_K2_2',6),('centre_K2_3',18)]
  nonbip=sum(n for _,n in rows)
  return dict(nine_nonbipartite_strata=[dict(stratum=k,ordinary_classes=n)for k,n in rows],
    nonbipartite_classes=nonbip,bipartite_classes=B,ordinary_classes=B+nonbip,
    H=H,h_b={str(k):h[k]for k in sorted(h)},strict_singleton_subset_added=False)

def compose(files,request):
  need(type(request)is dict and request.get('schema')=='ORDER32_LOCAL_COMPOSITION_INPUTS_V1'
    and same(request.get('target'),TARGET) and set(request['components'])=={'bipartite','two_centre','centre_halves'},
    'correct complete fixed target and three component families')
  need(request['proof_dependencies']['path']=='order32_census/PROOF_DEPENDENCIES.json'and request['proof_dependencies']['sha256']==PROOF_CLOSURE_SHA,'exact complete documentary closure pin')
  proofs=files.doc(request['proof_dependencies'])
  need(proofs.get('schema')=='ORDER32_RELATIVE_DOCUMENTARY_PROOF_CLOSURE_V1'
    and type(proofs.get('files'))is list and 1<=len(proofs['files'])<=64,'documentary proof closure')
  for q in proofs['files']:files.read(q['file'])
  values={};identities={};hb_contexts=[]
  for kind in ['bipartite','two_centre']:
    spec=request['components'][kind];m,local=manifest(files,spec,kind)
    receipt=files.doc(spec['receipt'])
    n=bipartite(receipt,m,local)if kind=='bipartite'else two_centre(receipt,m,local)
    identities[kind]=shards(files,receipt,spec['receipt'],n);values[kind]=n
  spec=request['components']['centre_halves'];m,local=manifest(files,spec,'centre_halves')
  rows=spec['collections'];need(type(rows)is list and [q['b']for q in rows]==[1,2,3,4]
    and all(type(q['b'])is int for q in rows),'each b1..4 exactly once')
  h={}
  for row in rows:
    r=files.doc(row['receipt']);h[row['b']],identities['h'+str(row['b'])]=half_collection(files,r,row['receipt'],m,local,row['b'],spec['base'])
    hb_contexts.append((r['campaign'],r['control_report']))
  need(all(x==hb_contexts[0]for x in hb_contexts),'one coherent fresh Hb campaign')
  result=combine(values['bipartite'],values['two_centre'],h)
  files.finish()
  return dict(result,schema='ORDER32_LOCAL_COMPLETE_COMPOSITION_RESULT_V1',target=TARGET,
    complete_all_required_families=True,stream_identities=identities,
    documentary_exhaustion_disjointness_and_gluing_imports=request['proof_dependencies'],
    independent_graph_algorithm=False,Root_or_SDK_authority=False,
    original_source='Cambie, Goedgebeur, Jooken and Van den Eede, arXiv2511.21144v3, AppendixB Table6, page23',
    count_status='RECOVERY_OF_KNOWN_ORIGINAL_EXACT_COUNT',order80_obligation_complete=False,
    new_Original_Lean_conjecture_measurement_credit=0,policy=POLICY,
    declared_input_read_bytes=files.read_bytes,unique_input_paths=len(files.rows))

def bind_inputs(files,template):
  need(template.get('schema')=='ORDER32_LOCAL_COMPOSITION_TEMPLATE_V1'and same(template.get('target'),TARGET),
    'local binding template, not execution approval')
  request=dict(template,schema='ORDER32_LOCAL_COMPOSITION_INPUTS_V1')
  request['components']=strict(canonical(template['components']))
  for kind in ['bipartite','two_centre','centre_halves']:
    spec=request['components'][kind]
    if kind=='centre_halves':
      need([r['b']for r in spec['collections']]==[1,2,3,4]and all(type(r['b'])is int for r in spec['collections']),'four local collection paths')
      rows=spec['collections']
    else:rows=[spec]
    for row in rows:
      name=row['receipt'];relative(name);path=files.path(name);a=path.lstat()
      need(path.resolve(strict=True)==path and stat.S_ISREG(a.st_mode)and a.st_nlink==1
        and 0<=a.st_size<=65536 and files.read_bytes+a.st_size<=POLICY['read_bytes'], 'bounded fresh local receipt')
      with path.open('rb')as stream:
        opened=os.fstat(stream.fileno());raw=stream.read(a.st_size+1);closed=os.fstat(stream.fileno())
      need(len(raw)==a.st_size and signature(a)==signature(opened)==signature(closed)==signature(path.lstat()),'stable observed receipt')
      files.read_bytes+=len(raw)
      ref=dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
      files.read(ref);row['receipt']=ref
  files.finish()
  return request

def main():
  p=argparse.ArgumentParser(allow_abbrev=False)
  p.add_argument('--root',type=Path,required=True);p.add_argument('--inputs',required=True)
  p.add_argument('--sha256',required=True);p.add_argument('--out',required=True);p.add_argument('--bind',action='store_true')
  a=p.parse_args()
  need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary-E-B-S')
  need(all(k not in os.environ for k in ['COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES']),'four environment denials')
  root=a.root.resolve(strict=True);need(root==a.root.absolute()and root.is_dir(),'ordinary absolute assembly root')
  f=Files(root);path=f.path(a.inputs);n=path.stat().st_size;need(n<=65536,'bounded composition input document')
  request_ref=dict(path=a.inputs,bytes=n,sha256=a.sha256);request=f.doc(request_ref)
  source=f.doc(request['source_manifest'])
  need(source.get('schema')=='ORDER32_COMPOSITION_SOURCE_MANIFEST_V1'and same(source.get('policy'),POLICY)
    and same(source.get('proof_dependencies'),request['proof_dependencies'])
    and set(source.get('files',{}))=={'program','controls','supervisor','runtime_base'},'exact small Source manifest')
  need(sum(r['bytes']for r in source['files'].values())<=65536,'complete Source/runtime namespace')
  for r in source['files'].values():f.read(r)
  need(same(request['program'],source['files']['program'])
    and f.path(request['program']['path'])==Path(__file__).resolve(strict=True),'truthful composition Source path')
  result=bind_inputs(f,request)if a.bind else compose(f,request)
  if not a.bind:result['inputs']=request_ref
  out=f.path(a.out);need(not os.path.lexists(out)and not os.path.lexists(out.with_name(out.name+'.staged')),'fresh composition output')
  raw=canonical(result);need(len(raw)<=65536,'whole bounded scalar composition result')
  stage=out.with_name(out.name+'.staged')
  with stage.open('xb')as stream:need(stream.write(raw)==len(raw),'whole scalar output');stream.flush();os.fsync(stream.fileno())
  need(stage.read_bytes()==raw,'whole staged result readback')
  os.replace(stage,out)
  fd=os.open(out.parent,os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
  f.check()
  summary=dict(result=dict(path=a.out,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),binding_only=a.bind)
  if not a.bind:summary['ordinary_classes']=result['ordinary_classes']
  print(canonical(summary).decode(),end='')

if __name__=='__main__':main()
