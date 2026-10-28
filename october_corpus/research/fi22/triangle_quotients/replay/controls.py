"""UNRUN generic finite-array and relative-IO controls, no original Fi22 cases.
Author /root/compact_proof_author. No graph/group/point/word acquisition.
"""
import argparse,hashlib,json,resource,struct,sys,tempfile,time
from pathlib import Path
START=time.monotonic()

def need(ok,why):
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 if not ok:raise ValueError(why)
 if rss>=128*2**20 or time.monotonic()-START>=100:raise RuntimeError('128MiB100s generic controls')

def refused(call,why):
 try:call()
 except(ValueError,KeyError,TypeError,IndexError):return
 raise ValueError('negative generic control accepted: '+why)

class Meter:
 def __init__(self):self.units=0
 def charge(self,count,role):
  need(type(count)is int and count>=0 and type(role)is str,'whole fixture work charge')
  self.units+=count;need(self.units<100000,'bounded synthetic work')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--consumer',nargs=2,required=True)
 ap.add_argument('--self-sha256',required=True);a=ap.parse_args()
 own=Path(__file__).resolve(strict=True);ownraw=own.read_bytes()
 need(len(ownraw)<=16384 and hashlib.sha256(ownraw).hexdigest()==a.self_sha256,'whole bounded controls Source')
 source=Path(a.consumer[0]);raw=source.read_bytes()
 need(source.resolve(strict=True)==source and len(raw)<=50000 and hashlib.sha256(raw).hexdigest()==a.consumer[1],
  'whole new consumer before declaration activation')
 ns={'__name__':'portable_finite_generic_control_subject','__file__':str(source)}
 exec(compile(raw,str(source),'exec'),ns)
 missing=4294967295;names=[];units=0
 def fixture(stage,left,right,certificate):
  nonlocal units
  work=Meter();n=len(left)
  L=struct.pack('<'+'I'*n,*left);R=struct.pack('<'+('H'if stage=='product-mass'else'I')*n,*right)
  C=struct.pack('<'+('H'if stage=='product-mass'else'I')*n,*certificate)
  x,y=ns['prepare'](L,R,stage,n,need,work)
  records,facts=ns['verify'](x,y,stage,0,n,C,need,work);units+=work.units
  return records,facts
 records,facts=fixture('s3-minimum',[1,0,2],[0,2,1],[0,0,0])
 need(records==struct.pack('<IB',0,3)and facts['selected_representatives']==1,'exact generic3-owner S3 minimum')
 names.append('literal_three_owner_S3_positive')
 records,facts=fixture('partner-resolution',[0,0,0,3,3,3],[3,missing,missing,0,missing,missing],
  [3,missing,missing,0,missing,missing])
 need(records==struct.pack('<IB',0,2)and facts['selected_representatives']==1,'exact paired unordered partner')
 records,facts=fixture('partner-resolution',[0,0,0],[0,missing,missing],[0,missing,missing])
 need(records==struct.pack('<IB',0,1)and facts['fixed_partner_components']==1,'fixed unordered partner')
 names.append('paired_and_fixed_partner_positive')
 records,facts=fixture('product-mass',[1,0,missing],[8,8,0],[8,0,0])
 need(records==struct.pack('<IH',0,8)and facts['selected_product_mass']==8,'paired exact mass')
 records,facts=fixture('product-mass',[0,missing,missing],[8,0,0],[4,0,0])
 need(records==struct.pack('<IH',0,4)and facts['selected_product_mass']==4,'fixed exact half mass')
 names.append('paired_and_fixed_mass_positive')
 refused(lambda:fixture('s3-minimum',[1,2,0],[0,2,1],[0,0,0]),'noninvolutory map')
 refused(lambda:fixture('s3-minimum',[1,0,2],[0,2,1],[1,0,0]),'wrong supplied minimum')
 names.append('invalid_S3_relation_and_wrong_certificate_refused')
 refused(lambda:fixture('partner-resolution',[0,0,0],[0,0,missing],[0,missing,missing]),'invented noncanonical lift')
 refused(lambda:fixture('partner-resolution',[0,0,0,3,3,3],[3,missing,missing,3,missing,missing],
  [3,missing,missing,3,missing,missing]),'not an induced involution')
 names.append('noncanonical_lift_and_one_way_partner_refused')
 refused(lambda:fixture('product-mass',[1,0,missing],[8,6,0],[8,0,0]),'unequal partner masses')
 refused(lambda:fixture('product-mass',[0,missing,missing],[1,0,0],[1,0,0]),'nonintegral fixed half mass')
 refused(lambda:fixture('product-mass',[0,missing,missing],[8,1,0],[4,0,0]),'duplicate noncanonical mass')
 names.append('unequal_nonintegral_and_noncanonical_mass_refused')
 with tempfile.TemporaryDirectory(prefix='portable_finite_controls_')as tmp:
  root=Path(tmp).resolve(strict=True);body=b'{"fixture":1}\n';(root/'data.json').write_bytes(body)
  old=dict(path='/unavailable/original_fixture.json',bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
  binding=dict(original=old,relative='data.json');budget=ns['Budget'](root)
  need(budget.mapped(binding)==body,'explicit original-to-relative bytes only');budget.final()
  for name in('../escape','/absolute','nested/../data.json','./data.json'):
   refused(lambda name=name:ns['Budget'](root).mapped(dict(original=old,relative=name)),'path escape')
  bad=dict(old);bad['sha256']='0'*64
  refused(lambda:ns['Budget'](root).mapped(dict(original=bad,relative='data.json')),'wrong whole hash')
  (root/'alias.json').symlink_to(root/'data.json')
  refused(lambda:ns['Budget'](root).mapped(dict(original=old,relative='alias.json')),'noncanonical alias')
 names.append('relative_IO_positive_and_escape_hash_alias_refusals')
 print(json.dumps(dict(schema='PORTABLE_FINITE_ARRAY_CONTROLS_V1',status='PASS',controls=len(names),names=names,
  program=dict(path=str(own),bytes=len(ownraw),sha256=a.self_sha256),
  consumer=dict(path=str(source),bytes=len(raw),sha256=a.consumer[1]),work_units=units,
  original_case_group_point_graph_or_word_calls=0,prior_caller_or_Source_claim=False,
  qualification='Small scalar array fixtures only; no original Fi22 model, owner meaning or scientific replay is acquired.'),sort_keys=True))

if __name__=='__main__':main()
