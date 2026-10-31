"""UNRUN synthetic scalar/receipt/framing/IO controls; no graph producer runs."""
import argparse,copy,hashlib,json,os,stat,sys,tempfile,types
from pathlib import Path
if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize):
  raise ValueError('require-E-B-S/no-O before Source activation')
if any(k in os.environ for k in ['COVERAGE_PROCESS_START','COVERAGE_PROCESS_CONFIG','OPENSSL_CONF','OPENSSL_MODULES']):
  raise ValueError('four environment denials before Source activation')

def main():
  p=argparse.ArgumentParser(allow_abbrev=False)
  p.add_argument('--program',type=Path,required=True);p.add_argument('--sha256',required=True)
  p.add_argument('--out',type=Path,required=True);a=p.parse_args()
  def program():
    q=a.program;s=q.lstat()
    if not(q.is_absolute()and q.resolve(strict=True)==q and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<=65536):raise ValueError('bounded Source')
    with q.open('rb')as f:r=f.read(s.st_size+1)
    if len(r)!=s.st_size or hashlib.sha256(r).hexdigest()!=a.sha256:raise ValueError('whole Source')
    return r
  raw=program();m=types.ModuleType('order32_composition_tested');m.__file__=str(a.program)
  exec(compile(raw,str(a.program),'exec'),m.__dict__)
  checks=[]
  def done(name,yes=True):
    if not yes:raise AssertionError(name)
    checks.append(name)
  def refuse(name,f):
    try:f()
    except(ValueError,KeyError,TypeError,AssertionError):done(name);return
    raise AssertionError('negative accepted: '+name)
  r=m.combine(20,10,{1:2,2:5,3:7,4:11})
  done('nine_strata_alternative_counts_no_reference_target',r['ordinary_classes']==194 and r['nonbipartite_classes']==174 and len(r['nine_nonbipartite_strata'])==9)
  refuse('analytical_h1_postcheck',lambda:m.combine(20,10,{1:3,2:5,3:7,4:11}))
  refuse('analytical_h2_postcheck',lambda:m.combine(20,10,{1:2,2:4,3:7,4:11}))
  refuse('typed_scalar_bool',lambda:m.combine(True,10,{1:2,2:5,3:7,4:11}))
  refuse('missing_half_family',lambda:m.combine(20,10,{1:2,2:5,3:7}))
  refuse('absolute_path',lambda:m.relative('/tmp/a'))
  refuse('parent_traversal',lambda:m.relative('a/../b'))
  refuse('duplicate_JSON_field',lambda:m.strict(b'{"x":1,"x":2}'))
  refuse('nonfinite_JSON',lambda:m.strict(b'{"x":NaN}'))
  refuse('overflow_nonfinite_JSON',lambda:m.strict(b'{"x":1e10000}'))
  done('sorted_stream_exact_count',m.stream_lines(b'[1]\n[2]\n',2)==b'[2]\n')
  refuse('duplicate_code_line',lambda:m.stream_lines(b'[1]\n[1]\n',2))
  refuse('reversed_code_order',lambda:m.stream_lines(b'[2]\n[1]\n',2))
  refuse('truncated_final_LF',lambda:m.stream_lines(b'[1]',1))
  refuse('stream_count_mismatch',lambda:m.stream_lines(b'[1]\n',2))
  refuse('stream_bool_count',lambda:m.stream_lines(b'[1]\n',True))
  m.cover([[0,2],[2,5]],5);done('complete_prefix_cover')
  m.cover([[0,0]],0);done('explicit_zero_domain')
  refuse('raw_domain_gap',lambda:m.cover([[0,2],[3,5]],5))
  refuse('raw_domain_overlap',lambda:m.cover([[0,3],[2,5]],5))
  refuse('empty_domain_double_prefix',lambda:m.cover([[0,0],[0,0]],0))
  class Fake:
    def __init__(self):self.data={}
    def add(self,name,value):
      b=value if type(value)is bytes else m.canonical(value)
      self.data[name]=b;return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    def read(self,ref):
      m.descriptor(ref);b=self.data[ref['path']]
      m.need(len(b)==ref['bytes']and hashlib.sha256(b).hexdigest()==ref['sha256'],'synthetic pin');return b
    def doc(self,ref):return m.strict(self.read(ref))
  f=Fake();base='hb';local=dict(path='manifest.json',bytes=1,sha256='1'*64)
  kernel=dict(path='halves.py',bytes=1,sha256='2'*64);runner=dict(path='run.py',bytes=1,sha256='3'*64)
  manifest=dict(program=runner,theory=kernel,policy={'records':4096},proof_legs=[])
  control=f.add('hb/controls.json',dict(schema='HB_LOCAL_CONTROLS_V1',status='PASS',program=runner,theory=kernel,manifest=local,actual_half_interval_jobs=0))
  localcontrol=dict(control,path='controls.json')
  common=dict(schema='HB_LOCAL_RECEIPT_V1',manifest=local,program=runner,theory=kernel,policy=manifest['policy'],proof_legs=[],b=4,
    campaign='toy',control_report=localcontrol,closure='LOCAL_FINAL_INPUT_AUTHENTICATION')
  marked=f.add('hb/raw/data.jsonl',b'[0,0,0,[],[],[]]\n')
  rawreceipt=dict(common,mode='enumerate',shape=1,raw_domain=1,raw_endpoint_multisets=1,raw_port_multisets=1,
    requested_raw_interval=[0,1],completed_raw_interval=[0,1],scope_complete=True,frontier=None,
    counters=dict(margin_skips=0,port_orbit_skips=0,endpoint_orbit_skips=0,constructed_halves=1,compatible_attempts=1),
    records=1,data=dict(marked,path='raw/data.jsonl'))
  rr=f.add('hb/raw/receipt.json',rawreceipt);localrr=dict(rr,path='raw/receipt.json')
  ordinary=f.add('hb/collect/data.jsonl',b'[1]\n')
  collected=dict(common,mode='collect',scope_complete=True,frontier=None,complete_ordinary_union=True,
    record_domain=1,record_interval=[0,1],records=1,h_b=1,interval_receipts=[localrr],
    interval_family_sha256=hashlib.sha256(m.canonical([localrr])).hexdigest(),raw_coverage={'1':[[0,1]]},data=dict(ordinary,path='collect/data.jsonl'))
  receipt_ref=dict(path='hb/collect/receipt.json',bytes=1,sha256='0'*64)
  count,identity=m.half_collection(f,collected,receipt_ref,manifest,local,4,base)
  done('full_local_Hb_family_and_stream_pin',count==1 and identity['records']==1)
  bad=copy.deepcopy(collected);bad['complete_ordinary_union']=False
  refuse('partial_collection_refusal',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  bad=copy.deepcopy(collected);bad['b']=True
  refuse('wrong_typed_Hb_family',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  bad=copy.deepcopy(collected);bad['root']='/root'
  refuse('local_receipt_cannot_claim_Root_authority',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  bad=copy.deepcopy(collected);bad['h_b']=True
  refuse('typed_half_count_bool',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  bad=copy.deepcopy(collected);bad['interval_receipts']=[localrr,localrr]
  refuse('duplicate_raw_receipt',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  bad=copy.deepcopy(collected);bad['interval_family_sha256']='0'*64
  refuse('raw_family_identity_mismatch',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  bad=copy.deepcopy(collected);bad['record_interval']=[0,0]
  refuse('incomplete_record_union',lambda:m.half_collection(f,bad,receipt_ref,manifest,local,4,base))
  refuse('strict_singleton_receipt_is_not_enlarged_H',lambda:m.two_centre(dict(schema='QUINTIC_SINGLE_MIDDLE_COMPLETE_REPRODUCTION_RECEIPT_V1'),{},{}))
  bm=dict(files={},policy={'codes':65536})
  side=dict(raw_profiles=1,completed_profiles=1,local_forms=1)
  bip=dict(schema='QUINTIC_BIPARTITE_COMPLETE_REPRODUCTION_RECEIPT_V1',status='COMPLETE_FINITE_ENUMERATION',
    scope='Bipartite quintic graphs: order 32, girth 4, diameter 8.',manifest=local,inputs={},policy=bm['policy'],ordinary_classes=3,
    all_28_profile_domains_complete=True,all_14_pair_products_complete=True,every_pair_full32_witness_checked=True,source_identity_rechecked=True,
    rows=[dict(row=i,left=side.copy(),right=side.copy(),pairs=1,completed_pairs=1)for i in range(1,15)])
  done('complete_bipartite_typed_family',m.bipartite(bip,bm,local)==3)
  bad=copy.deepcopy(bip);bad['rows'][0]['left']['completed_profiles']=0
  refuse('partial_bipartite_profile',lambda:m.bipartite(bad,bm,local))
  bad=copy.deepcopy(bip);bad['ordinary_classes']=3.0
  refuse('float_count_not_integer',lambda:m.bipartite(bad,bm,local))
  bad=copy.deepcopy(bip);bad['rows'][1]['row']=1
  refuse('missing_skeleton_row',lambda:m.bipartite(bad,bm,local))
  hm=dict(files={},policy={'codes':4096})
  hreceipt=dict(schema='QUINTIC_TWO_CENTRE_COMPLETE_REPRODUCTION_RECEIPT_V1',status='COMPLETE_FOUR_DOMAIN_ORDINARY_UNION',
    manifest=local,inputs={},policy=hm['policy'],all_four_domains_complete=True,every_marked_half_full16_witness_checked=True,source_identity_rechecked=True,
    enlarged_half_count=3,independent_two_centre_ordinary_graphs=18,
    domains=[dict(shape=i,raw_endpoint_multisets=1,raw_port_multisets=1,completed_raw_interval=[0,1],
      counters=dict(margin_skips=0,port_orbit_skips=0,endpoint_orbit_skips=0,constructed_halves=1))for i in range(1,5)])
  done('complete_enlarged_H_typed_family',m.two_centre(hreceipt,hm,local)==3)
  bad=copy.deepcopy(hreceipt);bad['domains'][3]['completed_raw_interval']=[0,0]
  refuse('partial_H_rectangle',lambda:m.two_centre(bad,hm,local))
  bad=copy.deepcopy(hreceipt);bad['enlarged_half_count']=True
  refuse('bool_H_count',lambda:m.two_centre(bad,hm,local))
  sh=f.add('bipout/codes-000.jsonl',b'[1]\n[2]\n')
  sr=dict(sh,path='codes-000.jsonl',records=2)
  sd=dict(shards=[sr],output_data_bytes=sh['bytes'],code_set_sha256=sh['sha256'])
  done('all_shards_stream_checksum',m.shards(f,sd,dict(path='bipout/receipt.json'),2)['records']==2)
  bad=copy.deepcopy(sd);bad['code_set_sha256']='0'*64
  refuse('whole_stream_checksum_mismatch',lambda:m.shards(f,bad,dict(path='bipout/receipt.json'),2))
  needroot=a.out.parent;assert needroot.resolve(strict=True)==needroot and not os.path.lexists(a.out)
  with tempfile.TemporaryDirectory(prefix='order32-compose-controls-',dir=needroot)as temp:
    root=Path(temp);p0=root/'data';p0.write_bytes(b'abc');ref=dict(path='data',bytes=3,sha256=hashlib.sha256(b'abc').hexdigest())
    io=m.Files(root);done('whole_stable_file_identity',io.read(ref)==b'abc')
    p0.write_bytes(b'xyz');refuse('changed_whole_body',lambda:io.read(ref))
    link=root/'link';link.symlink_to(p0)
    refuse('symlink_refusal',lambda:m.Files(root).read(dict(ref,path='link')))
    other=root/'hard';os.link(p0,other)
    refuse('hardlink_refusal',lambda:m.Files(root).read(dict(ref,path='hard')))
  if program()!=raw:raise ValueError('closing Source identity')
  result=m.canonical(dict(schema='ORDER32_COMPOSITION_CONTROLS_V1',status='PASS',program_sha256=a.sha256,
    checks=checks,count=len(checks),actual_graph_producer_invocations=0,Root_or_SDK_authority=False))
  with a.out.open('xb')as out:out.write(result);out.flush();os.fsync(out.fileno())
  print(result.decode(),end='')

if __name__=='__main__':main()
