#!/usr/bin/env python3
"""Check all arithmetic and declared boundaries; not an independent source recount."""
import argparse,copy,csv,json
from pathlib import Path
from fractions import Fraction
from compute import HERE,UNITS,VARIANTS,PAIRS,inputs,derive,csv_rows,need,sha

def validate(r,recount,spec):
 need(r['policy_coordinates']==len(r['coordinates'])==30,'all thirty policy coordinates')
 need(r['comparison_order']==['written_papers','per_result_conditional','including_printed_program','including_raw_program_alternative'],'written first, conditional and code separate')
 need(r['whole_common_paper_charged_once'] and r['all_three_complete_applications_charged'] and not r['cross_topic_common_discount'],'whole topic with no cross-topic discount')
 need(r['conditional_prepaid']=='Whole U_D and the whole complete programme boundary, including five required programs and three complete diagnostics; not a selected local fraction.','explicit conditional acquisition')
 need(r['program_boundary']==dict(complete_programs=8,required=5,diagnostic=3,complete_drivers_separate=2,printed_representation='Whole 12-page appendix, counted once',raw_representation='All eight complete raw programs, alternative to printed appendix, never additional',raw_metrics_summed_per_file=True,no_diagnostic_pruning=True,drivers_not_added_to_any_comparison=True),'complete program and driver roles')
 need(r['complete_mathematical_programs']==spec['complete_mathematical_programs'] and r['complete_drivers']==spec['complete_drivers'],'all unchanged full raw files')
 need(all(r[k] is None for k in ['retained_external_proof_cost','catalogue_and_algorithm_construction_cost','historical_software_cost','graphics_and_formula_layout_cost','minimal_mathematical_complexity']),'unknown costs not zero')
 need(r['new_source_credit']==r['new_question_credit']==0 and r['source_contract_rows']==37,'scope unchanged')
 need(r['full_visible_text_claim'] is False and r['formal_source_application_claim'] is False,'no visible-text or end-to-end formal overclaim')
 need(r['physical_pages']==dict(source=26,common=6,applications=[5,6,2],scientific_replacement=19,printed_program=12,total_input_pages=57),'physical extents separate')
 need(r['source_to_application_sequence']==[dict(source=s,application=a,source_pages=recount['documents'][s]['pages'],application_pages=recount['documents'][a]['pages']) for s,a in PAIRS],'all pairs')
 raw=recount['raw_records']['raw_program_alternative'];drivers=recount['raw_records']['full_drivers_separate'];classifications={Path(p['path']).name:p['classification'] for p in spec['complete_mathematical_programs']};fraction_count=0
 for c,(v,n,u) in zip(r['coordinates'],[(v,n,u) for v in VARIANTS for n in ['NFC','NFKC'] for u in UNITS]):
  need((c['variant'],c['normalization'],c['unit'])==(v,n,u),'fixed coordinate order')
  costs={k:d['variants'][v][n][u] for k,d in recount['documents'].items()};source=sum(costs[s] for s,a in PAIRS);common=costs['U_D'];apps=sum(costs[a] for s,a in PAIRS);printed=costs['CODE'];rawcost=sum(p['variants'][n][u] for p in raw.values());drivercost=sum(p['variants'][n][u] for p in drivers.values())
  for key,value in [('document_costs',costs),('source_sum',source),('common_theory',common),('all_applications',apps),('written_denominator',common+apps),('printed_program_cost',printed),('raw_program_cost',rawcost),('separate_driver_cost',drivercost)]:need(c[key]==value,'complete document arithmetic '+key)
  need(c['raw_program_role_costs']=={role:sum(p['variants'][n][u] for name,p in raw.items() if classifications[name]==role) for role in ['required','diagnostic']},'full raw program roles')
  def test(q,nn,dd):
   f=Fraction(nn,dd);need(q==dict(numerator=nn,denominator=dd,reduced_numerator=f.numerator,reduced_denominator=f.denominator,exact_fraction=str(f),factor=float(f)),'exact numerator/denominator/reduced fraction/decimal')
  need(set(c['comparisons'])=={'written_papers','including_printed_program','including_raw_program_alternative'},'three declared representations')
  for key,den in [('written_papers',common+apps),('including_printed_program',common+apps+printed),('including_raw_program_alternative',common+apps+rawcost)]:test(c['comparisons'][key],source,den);fraction_count+=1
  need(len(c['per_result'])==3,'three complete conditional applications')
  for q,(s,a) in zip(c['per_result'],PAIRS):
   need(q['source']==s and q['application']==a and q['source_cost']==costs[s] and q['application_cost']==costs[a],'paired source/local full cost')
   test({k:q[k] for k in ['numerator','denominator','reduced_numerator','reduced_denominator','exact_fraction','factor']},costs[s],costs[a]);fraction_count+=1
 need(r['primary']==r['coordinates'][22],'declared primary NFC nonspace calibrated coordinate')
 need(r['exact_combined_fractions']==r['exact_conditional_fractions']==90 and fraction_count==180,'all exact fractions')
 return dict(pdf_metric_cells=240,raw_program_driver_metric_cells=100,policy_coordinates=30,combined_fractions=90,conditional_fractions=90)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results-dir',type=Path,default=HERE);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh report')
 author,recount,spec=inputs(HERE);r=json.loads((a.results_dir/'results.json').read_text());summary=validate(r,recount,spec)
 need({k:v for k,v in r.items() if k!='bindings'}==derive(author,recount,spec),'deterministic derivation')
 for n,h in r['bindings'].items():need(sha(HERE/n)==h,'bound input/script')
 for name,rows in zip(['overall_costs.csv','conditional_costs.csv'],csv_rows(r)):
  with (a.results_dir/name).open(newline='') as f:actual=list(csv.DictReader(f))
  need(actual==[{k:str(v) for k,v in row.items()} for row in rows],'exact CSV values '+name)
 controls=[]
 for label in ['drop_common','drop_D3','drop_printed_program','prune_diagnostics','double_charge_printed_and_raw','add_drivers_silently','wrong_fraction','wrong_conditional_pair','hide_prepayment','cross_topic_discount','classical_cost_zero','historical_software_zero','source_credit','full_visible_text','wrong_primary','wrong_coordinate']:
  x=copy.deepcopy(r);c=x['coordinates'][0]
  if label=='drop_common':c['common_theory']=0
  elif label=='drop_D3':c['all_applications']-=c['per_result'][2]['application_cost']
  elif label=='drop_printed_program':c['comparisons']['including_printed_program']['denominator']=c['written_denominator']
  elif label=='prune_diagnostics':x['complete_mathematical_programs']=[p for p in x['complete_mathematical_programs'] if p['classification']=='required']
  elif label=='double_charge_printed_and_raw':c['comparisons']['including_raw_program_alternative']['denominator']+=c['printed_program_cost']
  elif label=='add_drivers_silently':c['comparisons']['written_papers']['denominator']+=c['separate_driver_cost']
  elif label=='wrong_fraction':c['comparisons']['written_papers']['exact_fraction']='12'
  elif label=='wrong_conditional_pair':c['per_result'][0]['application']='D2'
  elif label=='hide_prepayment':x['conditional_prepaid']='Only local cost matters.'
  elif label=='cross_topic_discount':x['cross_topic_common_discount']=True
  elif label=='classical_cost_zero':x['retained_external_proof_cost']=0
  elif label=='historical_software_zero':x['historical_software_cost']=0
  elif label=='source_credit':x['new_source_credit']=1
  elif label=='full_visible_text':x['full_visible_text_claim']=True
  elif label=='wrong_primary':x['primary']=x['coordinates'][0]
  elif label=='wrong_coordinate':c['normalization']='NFKC'
  try:validate(x,recount,spec)
  except ValueError as e:controls.append(dict(name=label,rejected=True,reason=str(e)))
  else:raise ValueError('accepted corruption '+label)
 report=dict(status='PASS_AUTHOR_ARITHMETIC_AND_BOUNDARY_CONTROLS',counts=summary,controls=controls,input_review_manifest_sha256=sha(HERE/'independent/manifest.json'),source_reextraction_repeated=False,full_formal_or_census_repeated=False,independent_arithmetic_review=False,scope='All 180 exact fractions from accepted full-document inputs; no new mathematical claims.')
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main()
