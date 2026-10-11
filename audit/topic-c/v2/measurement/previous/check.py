#!/usr/bin/env python3
"""Author arithmetic and boundary consistency checks, not an independent recount."""
import argparse,copy,csv,json
from pathlib import Path
from fractions import Fraction
from compute import HERE,UNITS,VARIANTS,PAIRS,inputs,derive,csv_rows,need,sha

def validate(result,recount,spec):
 need(len(result['coordinates'])==30,'all thirty coordinates')
 need(result['all_four_applications_charged'] and result['complete_common_and_programs_prepaid_for_conditional_factors'],'complete boundary and conditional prepayment')
 need(result['outside_proof_cost'] is None and result['unextracted_graphic_cost'] is None and result['minimum_mathematical_complexity'] is None,'unknown external costs')
 need(result['new_source_credit']==result['new_question_credit']==0,'no credit changes')
 need(result['required_mathematical_programs']==spec['required_mathematical_programs'],'both full programs, no pruning')
 need(result['raw_program_metrics_summed_per_file'],'whole-file alternative convention')
 raw=recount['raw_program_alternative'];knownfracs=0
 for r,(variant,form,unit) in zip(result['coordinates'],[(v,f,u) for v in VARIANTS for f in ['NFC','NFKC'] for u in UNITS]):
  need((r['variant'],r['normalization'],r['unit'])==(variant,form,unit),'fixed coordinate ordering')
  c={k:v['variants'][variant][form][unit] for k,v in recount['documents'].items()};common=c['U_C'];apps=sum(c[a] for s,a in PAIRS);known=sum(c[s] for s,a in PAIRS if s in c);rp=sum(v['variants'][form][unit] for v in raw.values())
  for key,value in [('common_theory',common),('all_applications',apps),('written_denominator',common+apps),('complete_printed_program_cost',c['CODE']),('complete_raw_program_cost',rp),('complete_denominator',common+apps+c['CODE']),('raw_program_denominator',common+apps+rp),('known_source_sum',known)]:need(r[key]==value,'full arithmetic '+key)
  need(r['unknown_source']=='L108' and r['complete_source_sum'] is None and r['overall_factor'] is None,'missing source stays unknown')
  for key,den in [('complete_printed_programs',common+apps+c['CODE']),('written_papers_only',common+apps),('complete_raw_programs',common+apps+rp)]:
   q=r['overall_formulas'][key];need(q==dict(unknown_source='L108',unknown_numerator_coefficient=1,known_numerator=known,denominator=den,overall_factor=None),'program representation is alternative, never additional')
  need(len(r['per_result'])==4,'four conditional rows')
  for q,(source,app) in zip(r['per_result'],PAIRS):
   need(q['source']==source and q['application']==app and q['application_cost']==c[app],'exact paired application')
   if source=='L108':need(q['source_cost'] is q['fraction'] is q['factor'] is None,'unknown C3 numerator and factor')
   else:
    f=Fraction(c[source],c[app]);need(q['source_cost']==c[source] and q['fraction']==str(f) and q['factor']==float(f),'exact conditional ratio');knownfracs+=1
 need(result['primary']==result['coordinates'][22],'primary calibrated NFC nonspace coordinate')
 need(result['known_conditional_fractions']==knownfracs==90,'ninety known conditional fractions')
 return dict(pdf_metric_cells=270,raw_program_metric_cells=20,overall_symbolic_formulas=90,known_conditional_fractions=90,unknown_conditional_coordinates=30)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results-dir',type=Path,default=HERE);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh report')
 author,recount,spec=inputs(HERE);result=json.loads((a.results_dir/'results.json').read_text());numbers=validate(result,recount,spec)
 expected=derive(author,recount,spec);need({k:v for k,v in result.items() if k!='bindings'}==expected,'derived result reproducibility')
 for n,h in result['bindings'].items():need(sha(HERE/n)==h,'result input/compute binding')
 for name,rows in zip(['overall_costs.csv','conditional_costs.csv'],csv_rows(result)):
  with (a.results_dir/name).open(newline='') as f:actual=list(csv.DictReader(f))
  need(actual==[{k:str(v) for k,v in r.items()} for r in rows],'exact CSV '+name)
 controls=[]
 for name in ['drop_C3','drop_CODE','double_charge_programs','raw_program_pruning','missing_L108_zero','invent_overall','wrong_fraction','hide_prepaid_common','external_zero','new_credit','wrong_primary']:
  r=copy.deepcopy(result)
  if name=='drop_C3':r['coordinates'][0]['all_applications']-=r['coordinates'][0]['per_result'][2]['application_cost']
  elif name=='drop_CODE':r['coordinates'][0]['complete_denominator']=r['coordinates'][0]['written_denominator']
  elif name=='double_charge_programs':r['coordinates'][0]['overall_formulas']['complete_raw_programs']['denominator']+=r['coordinates'][0]['complete_printed_program_cost']
  elif name=='raw_program_pruning':r['required_mathematical_programs'].pop()
  elif name=='missing_L108_zero':r['coordinates'][0]['per_result'][2]['source_cost']=0
  elif name=='invent_overall':r['coordinates'][0]['overall_factor']=1.2
  elif name=='wrong_fraction':r['coordinates'][0]['per_result'][0]['fraction']='2'
  elif name=='hide_prepaid_common':r['complete_common_and_programs_prepaid_for_conditional_factors']=False
  elif name=='external_zero':r['outside_proof_cost']=0
  elif name=='new_credit':r['new_source_credit']=1
  elif name=='wrong_primary':r['primary']['variant']='raw_untrimmed'
  try:validate(r,recount,spec)
  except ValueError as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
  else:raise ValueError('mutation passed '+name)
 report=dict(status='PASS_AUTHOR_ARITHMETIC_CHECK',counts=numbers,overall_csv_rows=90,conditional_csv_rows=120,controls=controls,independent_source_recount_repeated=False,math_Lean_GAP_replayed=False,complete_input_acceptance_manifest_sha256=sha(HERE/'independent/manifest.json'),scope='Arithmetic derived from accepted measurements. Independent arithmetic and reader review remain separate.')
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(numbers))
if __name__=='__main__':main()
