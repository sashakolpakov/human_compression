#!/usr/bin/env python3
"""Reject changed clause boundaries or omitted required costs under Python -O."""
import argparse,copy,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('topic_c_check',HERE/'check.py');check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);a=p.parse_args();check.need(not a.out.exists(),'Output exists')
 scope=json.loads((HERE/'scope.json').read_text());check.check_scope(HERE,scope)
 def row(d,key):return next(r for r in d['source_result_rows'] if r['id']==key)
 def drop_clause(d):d['source_result_rows'].pop()
 def duplicate_clause(d):d['source_result_rows'][-1]=copy.deepcopy(d['source_result_rows'][0])
 def promote_exclusion(d):row(d,'N14')['coverage']='recovered'
 def erase_correction(d):row(d,'P4')['coverage']='recovered'
 def omit_census(d):row(d,'J9')['required_programs']=['program.construction']
 def cost_as_zero(d):next(x for x in d['sources'] if x['id']=='L108')['full_source_pdf_cost']=0
 def uncharge_program(d):d['required_programs'][1]['required_mathematics']=False
 def changed_span(d):d['proof_regions']['binary']['end_char']-=1
 cases=[('drop clause',drop_clause),('duplicate clause',duplicate_clause),('promote excluded auxiliary',promote_exclusion),('erase corrected action-kernel scope',erase_correction),('omit required census',omit_census),('unknown source cost becomes zero',cost_as_zero),('uncharge mathematical program',uncharge_program),('truncate actual proof span',changed_span)]
 result=[]
 for name,mutate in cases:
  test=copy.deepcopy(scope);mutate(test)
  try:check.check_scope(HERE,test)
  except RuntimeError as exc:result.append({'mutation':name,'rejected':True,'reason':str(exc)})
  else:raise RuntimeError('Accepted invalid mutation: '+name)
 a.out.write_text(json.dumps({'status':'PASS','optimized_python_compatible':True,'controls':result,'mathematical_proof_claim':False},indent=2)+'\n');print('PASS',len(result),'controls')
if __name__=='__main__':main()
