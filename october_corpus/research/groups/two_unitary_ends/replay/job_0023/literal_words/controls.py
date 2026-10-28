"""UNRUN distinct controls for corpus-relative adopted literal132 replay.
Synthetic IO/history and generic GL7 word equations only. No original model,
marking, case, host caller/gate identity, adoption or paid authority is supplied.
"""
import argparse,copy,hashlib,json,os,resource,sys,tempfile,time
from pathlib import Path
START=time.monotonic()
def need(ok,why):
 if not ok:raise ValueError(why)

class ArithmeticBudget:
 def __init__(self,stop_type=None,limit=None):self.products=0;self.searching=False;self.need=need;self.stop_type=stop_type;self.limit=limit
 def tick(self,soft=False):
  rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(rss<128*2**20 and time.monotonic()-START<100,'generic128MiB100s control bound')
 def multiply(self,A,B):
  self.tick()
  if self.limit is not None and self.products>=self.limit:raise self.stop_type('synthetic forced stop')
  self.products+=1;need(self.products<=50000,'generic50000products')
  return tuple(tuple(sum(A[i][k]*B[k][j]for k in range(len(B)))%11 for j in range(len(B[0])))for i in range(len(A)))

def refused(call):
 try:call()
 except(ValueError,KeyError,TypeError,IndexError):return
 raise ValueError('bad generic metadata was accepted')

def reflection_fixture(kernel,budget):
    one=(1,0,0,0,0,0);x=(0,1,0,0,0,0);I=kernel['I7']
    for a in range(11):
        for b in range(1,11):
            def mul(u,v):
                budget.tick(True);out=[0]*11
                for i in range(6):
                    for j in range(6):out[i+j]=(out[i+j]+u[i]*v[j])%11
                for k in range(10,5,-1):
                    c=out[k];out[k-6]=(out[k-6]-b*c)%11;out[k-5]=(out[k-5]-a*c)%11
                return tuple(out[:6])
            def ring_power(z,n):
                value=one
                for bit in bin(n)[2:]:
                    value=mul(value,value)
                    if bit=='1':value=mul(value,z)
                return value
            z=ring_power(x,47880)
            rows=[mul(tuple(int(i==j)for i in range(6)),z)for j in range(6)]
            Y=((1,0,0,0,0,0,0),)+tuple((0,)+row for row in rows)
            if Y==I or kernel['power'](Y,37,budget)!=I:continue
            frob=[ring_power(tuple(int(i==j)for i in range(6)),1331)for j in range(6)]
            F=((1,0,0,0,0,0,0),)+tuple((0,)+row for row in frob)
            if budget.multiply(F,F)!=I:continue
            if budget.multiply(budget.multiply(F,Y),F)!=kernel['power'](Y,36,budget):continue
            Z=tuple(tuple((10 if i==0 else 1)if i==j else 0 for j in range(7))for i in range(7))
            return Y,F,Z
    raise ValueError('bounded generic ring fixture found no checked reflection pair')

def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'minimal generic EBS')
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--self-sha256',required=True);ap.add_argument('--program',nargs=2,required=True);a=ap.parse_args()
 own=Path(__file__).resolve(strict=True);ownraw=own.read_bytes();subject=Path(a.program[0]);raw=subject.read_bytes()
 need(len(ownraw)<=16384 and hashlib.sha256(ownraw).hexdigest()==a.self_sha256,'whole new control Source')
 need(subject.is_absolute()and subject.resolve(strict=True)==subject and len(raw)<=65536 and hashlib.sha256(raw).hexdigest()==a.program[1],
      'exact new literal replay subject')
 C={'__name__':'portable_literal132_controls_only','__file__':str(subject)};exec(compile(raw,str(subject),'exec'),C);names=[]
 for text in('/private/tmp/host','../escape','a/../b','./x','.git/x','.lake/x','__pycache__/x','a//b',''):
  refused(lambda text=text:C['relative'](text))
 names.append('relative_only_paths_refuse_host_traversal_build_and_noncanonical_values')
 with tempfile.TemporaryDirectory(prefix='q11_literal_replay_controls_',dir='/private/tmp')as td:
  root=Path(td).resolve(strict=True);path=root/'value.json';body=b'{"x":1}\n';path.write_bytes(body)
  sha=hashlib.sha256(body).hexdigest();original=dict(path='/historical/original/value',bytes=len(body),sha256=sha)
  alias=dict(original,path='/historical/retained/value');physical=dict(path='value.json',bytes=len(body),sha256=sha)
  b=C['Budget'](root);mapping=[dict(original=r,relative='value.json')for r in(original,alias)];b.bind(mapping)
  need(C['same_mapped_object'](b,original,alias)and b.read(original)==b.read(alias)==body and b.bytes==len(body),'two exact historical identities share explicit relative object')
  refused(lambda:b.read(dict(original,path=str(path))));refused(lambda:b.read(dict(original,bytes=True)))
  refused(lambda:C['same_mapped_object'](b,original,dict(original,path='/unmapped')))
  refused(lambda:b.bind(mapping+[mapping[0]]));b.bind(mapping);b.recheck();need(b.bytes==2*len(body),'final fresh whole rehash charged')
  path.write_bytes(b'{"x":2}\n');refused(b.recheck);path.write_bytes(body)
  link=root/'link';link.symlink_to(path);other=C['Budget'](root);refused(lambda:other.physical(dict(physical,path='link')))
  names.append('whole_alias_identity_cache_final_hash_mutation_and_no_host_fallback')
  def rr(name,sha='a'*64):return dict(path='/synthetic/'+name,bytes=1,sha256=sha)
  context=dict(original_job=[23,4],projection=rr('projection'),Root_projection_acceptance=rr('projection_acceptance'))
  plan=dict(context=context,expected_positions=[1,2],expected_count=2,literal_arithmetic_parent=rr('ab99',C['PARENT_SHA']),
   existing_adoption=rr('adoption'),historical_after_selector=rr('after'),theorem=rr('theorem'),theorem_review=rr('review'),
   historical_result=rr('result'),historical_plan=rr('plan'),carrier=rr('carrier'))
  carrier=dict(schema='Q11_TWO_END37_SUPPLIED_LITERAL_WORDS_V1',grammar=C['LITERAL_GRAMMAR'],original_job=[23,4],projection=context['projection'],
   selector=rr('before'),records=[[1,1,'0'*64,'1','10'],[2,2,'1'*64,'01212110121210101010','1']])
  cb=C['can'](carrier)+b'\n';need(C['supplied_literal_carrier'](cb,plan)==carrier,'new literal protocol positive')
  for word in(True,1,0,[],None,'','3','0 1','1'*65):
   bad=copy.deepcopy(carrier);bad['records'][0][3]=word;refused(lambda bad=bad:C['supplied_literal_carrier'](C['can'](bad)+b'\n',plan))
  for records in([carrier['records'][1],carrier['records'][0]],[carrier['records'][0]]*2,[[True,1,'0'*64,'1','0']],[[1,True,'0'*64,'1','0']]):
   bad=copy.deepcopy(carrier);bad['records']=records;refused(lambda bad=bad:C['supplied_literal_carrier'](C['can'](bad)+b'\n',plan))
  refused(lambda:C['supplied_literal_carrier'](b' '+cb,plan));refused(lambda:C['supplied_literal_carrier'](b'{"schema":1,"schema":2}\n',plan))
  bad=dict(carrier,grammar='old_integer_dictionary');refused(lambda:C['supplied_literal_carrier'](C['can'](bad)+b'\n',plan))
  names.append('literal_grammar_positive_strict_types_order_duplicates_noncanonical_and_old_index_refusal')
  authority=dict(schema='ROOT_ACCEPTED_Q11_RANK4_TWO_END37_IP_FACTS_V1',root='/root',adopted=True,proof_mode='DIRECT_LITERAL_WORD_CHECK',grammar=C['LITERAL_GRAMMAR'],
   classification='FOUR_MARK_INTERSECTION_PROPERTY_FAILURE',four_mark_generation_or_nongeneration_claim=False,whole_original_credit=0,conjecture_credit=0,Lean_credit=0,
   original_job=[23,4],projection=context['projection'],Root_projection_acceptance=context['Root_projection_acceptance'],Root_unresolved_selector=carrier['selector'],
   independent_direct_result=plan['historical_result'],supplied_carrier=rr('carrier_authority_alias'),direct_checker=rr('ab99_alias',C['PARENT_SHA']),
   theorem=rr('theorem_alias'),theorem_review=rr('review_alias'),verified_IP_failure_positions=[1,2],newly_settled_positions=2)
  result=dict(schema='Q11_TWO_END37_LITERAL_DIRECT_RESULT_V1',status='VERIFIED_TWO_END37_ORIGINAL_LITERAL_RECORDS',grammar=C['LITERAL_GRAMMAR'],program=plan['literal_arithmetic_parent'],
   word_search_or_row_reduction_calls=0,proposer_or_kernel_imports=0,four_mark_generation_or_nongeneration_claim=False,whole_original_conjecture_Lean_or_measurement_credit=0,
   original_job=[23,4],projection=context['projection'],selector=carrier['selector'],plan=plan['historical_plan'],theorem=plan['theorem'],theorem_review=plan['theorem_review'],
   actual_supplied_literal_carrier=rr('carrier_result_alias'),verified_IP_failure_positions=[1,2])
  prior=dict(schema='Q11_TWO_END37_LITERAL_DIRECT_PLAN_V1',program=result['program'],context=context,original_job=[23,4],projection=context['projection'],
   Root_projection_acceptance=context['Root_projection_acceptance'],selector=carrier['selector'],records=rr('carrier_prior_alias'),theorem=plan['theorem'],theorem_review=plan['theorem_review'],
   expected_positive_positions=[1,2],selected_positions=[1,2,3])
  after=dict(schema='ROOT_ACCEPTED_Q11_RANK4_UNRESOLVED_SELECTOR_V1',root='/root',adopted=True,original_job=[23,4],projection=context['projection'],
   Root_projection_acceptance=context['Root_projection_acceptance'],previous_selector=carrier['selector'],source_adoptions=[plan['existing_adoption']],
   accepted_paid_by_kind=dict(two_end_theorem_IP_failure=[1,2]),unresolved_position_runs='NOT_A_LIVE_ELIGIBILITY_INPUT')
  refs=[plan['historical_result'],plan['historical_plan'],plan['carrier'],authority['supplied_carrier'],result['actual_supplied_literal_carrier'],prior['records'],
   plan['literal_arithmetic_parent'],authority['direct_checker'],plan['theorem'],authority['theorem'],plan['theorem_review'],authority['theorem_review']]
  def group(r):
   name=r['path'].rsplit('/',1)[-1];return('carrier'if name.startswith('carrier')else'parent'if name.startswith('ab99')else'theorem'if name.startswith('theorem')else'review'if name.startswith('review')else name)+'.json'
  joined=C['Budget'](root);joined.bind([dict(original=r,relative=group(r))for r in refs])
  need(C['validate_historical_subject'](plan,authority,result,prior,carrier,after,joined)==[1,2],'complete isolated literal historical identity chain')
  names.append('adopted_literal_result_plan_carrier_after_receipt_and_aliases_join_without_live_unpaid_query')
  for obj,key,value in[('authority','proof_mode','DIRECT_TWO_WORD_CHECK'),('authority','grammar','foreign'),('result','program',rr('wrong_source')),
   ('prior','context',dict(context,original_job=[20,4])),('carrier','selector',rr('other')),('after','source_adoptions',[rr('other')]),('after','previous_selector',rr('other'))]:
   aa,bb,cc,dd,ee=map(copy.deepcopy,(authority,result,prior,carrier,after));{'authority':aa,'result':bb,'prior':cc,'carrier':dd,'after':ee}[obj][key]=value
   refused(lambda aa=aa,bb=bb,cc=cc,dd=dd,ee=ee:C['validate_historical_subject'](plan,aa,bb,cc,dd,ee,joined))
  names.append('wrong_mode_Source_original_context_after_receipt_or_selector_refused')
  math=ArithmeticBudget();Y,F,Z=reflection_fixture(C,math);I=C['I7']
  C['direct_order37']((I,Y,I,Y),(0,1,2),'1',math);C['direct_order37']((I,Y,I,Y),(1,2,3),'0',math)
  C['direct_order37']((I,Y,I,Y),(0,1,2),'1'*5,math)
  refused(lambda:C['direct_order37']((I,I,I,I),(0,1,2),'01',math))
  minus=tuple(tuple(10*int(i==j)for j in range(7))for i in range(7))
  refused(lambda:C['direct_order37']((I,minus,I,I),(0,1,2),'1',math))
  refused(lambda:C['direct_order37']((I,Y,I,Y),(0,1,3),'1',math))
  names.append('generic_literal_prime_positive_outside_pool_identity_false_equation_and_wrong_end_refusal')
  small=ArithmeticBudget();C['power'](Y,6,small);C['power'](Y,37,small);need(small.products==12,'literalab99 twelve-product powers unchanged')
  ctx=dict(orbits=[[1,[1],[1],1]]);row=[1,1,C['digest'](ctx['orbits'][0]),'1','0'];C['validate_record_headers']([row],[1],ctx)
  refused(lambda:C['verify_records']([row],[1],ctx,math))
  names.append('generic_GL7_arithmetic_never_supplies_whole_original_model_frame_or_member_context')
 need(own.read_bytes()==ownraw and subject.read_bytes()==raw,'all whole current Sources unchanged')
 def ref(p,b):return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 print(json.dumps(dict(schema='Q11_PORTABLE_LITERAL132_GENERIC_CONTROLS_V1',status='PASS',author='/root/compact_proof_author',program=ref(own,ownraw),subject=ref(subject,raw),
  controls=len(names),names=names,original_case_or_model_calls=0,Source_or_gate_identity_transfer=False,
  complete_physical_Source_read_upper=3*len(ownraw)+2*len(raw)+4,matrix_products_generic=math.products+small.products,
  qualification='Generic GL7 literals, isolated relative IO and historical typed joins only. No corpus original case, source/caller/Root identity, adoption or paid authority is reissued.'),sort_keys=True))
if __name__=='__main__':main()
