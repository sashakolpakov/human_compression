"""UNRUN parameterized controls for relative replay IO and historical subject joins.
Author /root/prime_theory_audit. Isolated temporary DATA and identity matrices
only; no original G2 marking, corpus case, gate or Root adoption is evaluated.
"""
import argparse,hashlib,json,os,resource,sys,tempfile,time
from pathlib import Path
START=time.monotonic()
def need(ok,why):
 if not ok:raise ValueError(why)
def refused(call):
 try:call()
 except(ValueError,KeyError,TypeError,IndexError):return
 raise ValueError('invalid synthetic input accepted')
def main():
 need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
      and not sys.flags.optimize,'minimal synthetic EBS interpreter')
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--self-sha256',required=True)
 ap.add_argument('--program',nargs=2,required=True);a=ap.parse_args()
 own=Path(__file__).resolve(strict=True);ownraw=own.read_bytes()
 need(len(ownraw)<=16384 and hashlib.sha256(ownraw).hexdigest()==a.self_sha256,'exact control Source')
 subject=Path(a.program[0]);raw=subject.read_bytes()
 need(subject.is_absolute() and subject.resolve(strict=True)==subject and len(raw)<=65536
      and hashlib.sha256(raw).hexdigest()==a.program[1],'exact new checker Source')
 ns={'__name__':'portable_integer_batch_synthetic_only','__file__':str(subject)}
 exec(compile(raw,str(subject),'exec'),ns);names=[]
 for text in('/private/tmp/absolute','../escape','a/../b','./x','.git/x','.lake/x','__pycache__/x','a//b',''):
  refused(lambda text=text:ns['relative'](text))
 names.append('relative_paths_refuse_absolute_traversal_build_and_noncanonical_forms')
 with tempfile.TemporaryDirectory(prefix='q11_relative_controls_',dir='/private/tmp')as td:
  root=Path(td).resolve(strict=True);path=root/'value.json';body=b'{"x":1}\n';path.write_bytes(body)
  sha=hashlib.sha256(body).hexdigest();original=dict(path='/historical/original/value.json',bytes=len(body),sha256=sha)
  alias=dict(original,path='/historical/retained/value.json');physical=dict(path='value.json',bytes=len(body),sha256=sha)
  b=ns['Budget'](root);b.bind([dict(original=original,relative='value.json'),dict(original=alias,relative='value.json')])
  need(ns['same_mapped_object'](b,original,alias) and b.read(original)==body and b.read(alias)==body,
       'explicit whole alias reads one relative object')
  need(len(b.refs)==1 and b.bytes==len(body),'cache shares only complete physical identity')
  refused(lambda:ns['same_mapped_object'](b,original,dict(original,path='/not/in/map')))
  refused(lambda:b.read(dict(original,path=str(path))))
  names.append('both_complete_aliases_required_and_no_original_machine_fallback')
  refused(lambda:b.bind([dict(original=original,relative='value.json')]*2))
  b.bind([dict(original=original,relative='value.json'),dict(original=alias,relative='value.json')]);b.recheck()
  need(b.bytes==2*len(body),'fresh whole final read counted')
  path.write_bytes(b'{"x":2}\n');refused(b.recheck);path.write_bytes(body)
  names.append('whole_physical_hashes_and_final_recheck_detect_mutation')
  outside=root/'outside.json';outside.write_bytes(body);link=root/'link.json';link.symlink_to(outside)
  other=ns['Budget'](root);refused(lambda:other.physical(dict(physical,path='link.json')))
  names.append('symlink_input_is_refused_even_with_same_content')
  def rr(name,sha='a'*64):return dict(path='/synthetic/'+name,bytes=1,sha256=sha)
  context=dict(original_job=[23,4],projection=rr('projection'),Root_projection_acceptance=rr('projection_acceptance'))
  plan=dict(context=context,expected_positions=[1,2],expected_count=2,literal_arithmetic_parent=rr('old9f',ns['PARENT_SHA']),
            theorem=rr('theorem'),theorem_review=rr('review'),historical_result=rr('result'),historical_plan=rr('plan'),carrier=rr('carrier'))
  carrier=dict(schema='Q11_TWO_END37_SUPPLIED_WORDS_V1',dictionary=ns['DICTIONARY'],original_job=[23,4],projection=context['projection'],
               selector=rr('selector'),records=[[1,1,'0'*64,1,120],[2,2,'1'*64,2,119]])
  cb=ns['can'](carrier)+b'\n';need(ns['supplied_index_carrier'](cb,plan)==carrier,'synthetic canonical carrier')
  refused(lambda:ns['supplied_index_carrier'](b' '+cb,plan))
  refused(lambda:ns['supplied_index_carrier'](b'{"schema":1,"schema":2}\n',plan))
  import copy
  for rows in([carrier['records'][1],carrier['records'][0]],[carrier['records'][0]]*2,[[True,1,'0'*64,1,1]],[[1,1,'0'*64,True,1]],[[1,1,'0'*64,121,1]]):
   bad=copy.deepcopy(carrier);bad['records']=rows;refused(lambda bad=bad:ns['supplied_index_carrier'](ns['can'](bad)+b'\n',plan))
  names.append('canonical_carrier_context_sorted_positions_and_integer_word_types')
  authority=dict(schema='ROOT_ACCEPTED_Q11_RANK4_TWO_END37_IP_FACTS_V1',root='/root',adopted=True,proof_mode='DIRECT_TWO_WORD_CHECK',
   classification='FOUR_MARK_INTERSECTION_PROPERTY_FAILURE',four_mark_generation_or_nongeneration_claim=False,
   whole_original_credit=0,conjecture_credit=0,Lean_credit=0,original_job=[23,4],projection=context['projection'],
   Root_projection_acceptance=context['Root_projection_acceptance'],Root_unresolved_selector=carrier['selector'],
   independent_direct_result=plan['historical_result'],supplied_carrier=rr('carrier_alias'),direct_checker=rr('old9f_alias',ns['PARENT_SHA']),
   theorem=rr('theorem_alias'),theorem_review=rr('review_alias'),verified_IP_failure_positions=[1,2],newly_settled_positions=2)
  result=dict(schema='Q11_TWO_END37_DIRECT_RESULT_V1',status='VERIFIED_TWO_END37_ORIGINAL_RECORDS',program=plan['literal_arithmetic_parent'],
   word_search_or_row_reduction_calls=0,proposer_or_kernel_imports=0,four_mark_generation_or_nongeneration_claim=False,
   whole_original_conjecture_Lean_or_measurement_credit=0,original_job=[23,4],projection=context['projection'],
   selector=carrier['selector'],plan=plan['historical_plan'],theorem=plan['theorem'],theorem_review=plan['theorem_review'],verified_IP_failure_positions=[1,2])
  prior=dict(schema='Q11_TWO_END37_DIRECT_PLAN_V1',program=result['program'],context=context,original_job=[23,4],projection=context['projection'],
   Root_projection_acceptance=context['Root_projection_acceptance'],selector=carrier['selector'],records=rr('carrier_plan_alias'),
   theorem=plan['theorem'],theorem_review=plan['theorem_review'],expected_positive_positions=[1,2],selected_positions=[1,2,3])
  refs=[plan['historical_result'],plan['historical_plan'],plan['carrier'],authority['supplied_carrier'],prior['records'],
        plan['literal_arithmetic_parent'],authority['direct_checker'],plan['theorem'],authority['theorem'],plan['theorem_review'],authority['theorem_review']]
  def group(ref):
   name=ref['path'].rsplit('/',1)[-1]
   return ('carrier' if name.startswith('carrier') else 'parent' if name.startswith('old9f') else 'theorem' if name.startswith('theorem') else 'review' if name.startswith('review') else name)+'.json'
  joined=ns['Budget'](root);joined.bind([dict(original=r,relative=group(r))for r in refs])
  need(ns['validate_historical_subject'](plan,authority,result,prior,carrier,joined)==[1,2],'exact synthetic historical identity chain')
  names.append('historical_adoption_result_plan_carrier_alias_joins_positive')
  mutations=[('authority','proof_mode','EXISTING_CHECKED_PROPER_ENDS'),('authority','verified_IP_failure_positions',[1]),
             ('authority','projection',rr('other_projection')),('result','program',rr('new_source')),
             ('prior','context',dict(context,original_job=[20,4])),('carrier','selector',rr('other_selector'))]
  for obj,key,value in mutations:
   aa,bb,cc,dd=map(copy.deepcopy,(authority,result,prior,carrier));target={'authority':aa,'result':bb,'prior':cc,'carrier':dd}[obj];target[key]=value
   refused(lambda aa=aa,bb=bb,cc=cc,dd=dd:ns['validate_historical_subject'](plan,aa,bb,cc,dd,joined))
  names.append('wrong_old_mode_Source_context_position_or_selector_is_refused')
  math=ns['Budget'](root);ns['power'](ns['I7'],6,math);ns['power'](ns['I7'],37,math)
  need(math.products==12,'literal old9f12-product prime powers')
  refused(lambda:ns['direct_order37']((ns['I7'],)*4,(0,1,2),1,math))
  for index in(0,True,121):refused(lambda index=index:ns['word_from_index'](index))
  names.append('unchanged_integer_dictionary_bounds_and_identity_prime_refusal')
 need(own.read_bytes()==ownraw and subject.read_bytes()==raw,'all full Sources unchanged')
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
 need(rss<128*2**20 and time.monotonic()-START<125,'bounded128MiB125s generic controls')
 print(json.dumps(dict(schema='Q11_PORTABLE_INTEGER_BATCH_GENERIC_CONTROLS_V1',status='PASS',author='/root/prime_theory_audit',
  program=dict(path=str(own),bytes=len(ownraw),sha256=hashlib.sha256(ownraw).hexdigest()),
  subject=dict(path=str(subject),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),controls=len(names),names=names,
  original_case_or_model_calls=0,Source_or_gate_identity_transfer=False,
  complete_physical_Source_read_upper=3*len(ownraw)+2*len(raw)+4,
  qualification='Synthetic relative IO,whole alias joins,protocol refusals and identity-matrix arithmetic only; no original corpus case or Root authority.'),sort_keys=True))
if __name__=='__main__':main()
