#!/usr/bin/env python3
"""Independent arithmetic only, from the accepted root input recount.
No author result functions, PDF extraction, GAP or Lean is imported/executed.
"""
import argparse,copy,csv,hashlib,json,math
from pathlib import Path
V=('raw_untrimmed','raw_selected','calibrated_selected');F=('NFC','NFKC')
M=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
IPIN='4f322184f2d3d67abfc29841567b51b984e7f6d28788b9e3a475faa0c18ae911'
RPIN='d9556ea69402dd827426fe3c204aa9eb5895f7b342d58e22644c9283383ec2af'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def frozen(p,pin):
 need(sha(p/'manifest.json')==pin,'exact manifest')
 rows=load(p/'manifest.json')['exports']
 for r in rows:need((p/r['path']).stat().st_size==r['bytes'] and sha(p/r['path'])==r['sha256'],'frozen export '+r['path'])
 return len(rows)
def reduced(n,d):
 q=math.gcd(n,d);a,b=n//q,d//q
 return {'numerator':n,'denominator':d,'reduced_numerator':a,'reduced_denominator':b,'exact_fraction':str(a) if b==1 else str(a)+'/'+str(b),'factor':n/d}
def audit(data,counted,spec):
 need(len(data['coordinates'])==data['policy_coordinates']==30,'all policy coordinates')
 need(data['source_ids']==['L012'] and data['application_ids']==['AF1'],'actual matched source')
 need(data['source_contract_rows']==33 and data['existing_principal_contracts']==1 and data['project_total_preserved']==27,'admitted credit unchanged')
 need(data['conditional_prepaid']=='The whole U_Affine and all six complete required programs have already been acquired.','conditional acquisition')
 need(data['whole_common_paper_charged_once'] and data['complete_application_charged'] and not data['cross_topic_common_discount'],'complete independent-topic denominator')
 need(data['comparison_order']==['written_papers','per_result_conditional','including_printed_program','including_raw_program_alternative'],'written first')
 for k in ['retained_external_proof_cost','catalogue_and_algorithm_construction_cost','historical_software_cost','graphics_and_formula_layout_cost','minimal_mathematical_complexity']:need(data[k] is None,'unknown '+k)
 for k in ['full_visible_text_claim','formal_source_application_claim','paired_dependency_audit_complete']:need(data[k] is False,'scope '+k)
 for k in ['new_source_credit','new_question_credit','new_formal_credit']:need(data[k]==0,'credit '+k)
 for k in ['complete_mathematical_programs','complete_auxiliary_scripts','complete_formal_files','auxiliary_list_discrepancy']:need(data[k]==spec[k],'full file inventory '+k)
 need(len(data['complete_mathematical_programs'])==6 and len(data['complete_auxiliary_scripts'])==len(data['complete_formal_files'])==3,'6+3+3 full files')
 need(data['program_boundary']==dict(required_complete_files=6,printed_appendix_pages=8,embedded_diagnostics_included=True,raw_alternative_not_additional=True,raw_metrics_summed_per_file=True,auxiliary_files_separate=3,formal_files_separate=3,auxiliary_and_formal_not_silently_added=True),'code representation and separate files')
 need(data['physical_pages']==dict(source=17,common=7,application=9,scientific_replacement=16,printed_program=8,total_input_pages=41),'all complete pages')
 need(data['raw_file_bytes']=={g:sum(r['bytes'] for r in rows.values()) for g,rows in counted['raw_records'].items()},'all actual file bytes')
 overall=[];conditional=[]
 coords=[(v,f,m) for v in V for f in F for m in M]
 for row,(v,f,m) in zip(data['coordinates'],coords):
  need((row['variant'],row['normalization'],row['unit'])==(v,f,m),'coordinate identity')
  c={k:r['variants'][v][f][m] for k,r in counted['documents'].items()};files={k:sum(r['variants'][f][m] for r in rows.values()) for k,rows in counted['raw_records'].items()}
  s,u,a,z=[c[k] for k in ['L012','U_Affine','AF1','CODE']];raw=files['complete_programs']
  expected={'document_costs':c,'source_sum':s,'common_theory':u,'all_applications':a,'written_denominator':u+a,'printed_program_cost':z,'raw_program_cost':raw,'separate_auxiliary_cost':files['complete_auxiliary_scripts'],'separate_formal_cost':files['complete_formal_files']}
  for k,x in expected.items():need(row[k]==x,'full cost '+k)
  totals={'written_papers':u+a,'including_printed_program':u+a+z,'including_raw_program_alternative':u+a+raw}
  need(row['comparisons']=={k:reduced(s,d) for k,d in totals.items()},'exact three combined fractions')
  pair={'source':'L012','application':'AF1','source_cost':s,'application_cost':a,**reduced(s,a)};need(row['per_result']==[pair],'conditional exact complete application')
  base=dict(variant=v,normalization=f,unit=m)
  for k,d in totals.items():overall.append(dict(**base,representation=k,source_cost=s,whole_common=u,application_cost=a,program_cost=d-u-a,**reduced(s,d)))
  conditional.append(dict(**base,**pair,prepaid=data['conditional_prepaid']))
 need(data['primary']==data['coordinates'][coords.index(('calibrated_selected','NFC','characters_without_whitespace'))],'exact primary coordinate')
 need(data['exact_combined_fractions']==90 and data['exact_conditional_fractions']==30,'all fraction counts')
 return overall,conditional

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--author-pin',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
 exports=frozen(a.packet,a.author_pin);i=frozen(a.packet/'inputs',IPIN);r=frozen(a.packet/'independent',RPIN)
 counted=load(a.packet/'independent/recount.json');spec=load(a.packet/'inputs/replacement_input_spec.json');result=load(a.packet/'results.json')
 review=load(a.packet/'independent/review.json');need(review['status']=='ACCEPTED_ROOT_INDEPENDENT_AFFINE_MEASUREMENT_INPUTS' and review['requested_corrections']==[],'accepted independent input review')
 for k,h in result['bindings'].items():need(sha(a.packet/k)==h,'arithmetic binding')
 tables=audit(result,counted,spec)
 for name,expected in zip(['overall_costs.csv','conditional_costs.csv'],tables):
  with (a.packet/name).open(newline='') as f:actual=list(csv.DictReader(f))
  need(actual==[{k:str(v) for k,v in row.items()} for row in expected],'all CSV cells '+name)
 controls=[]
 mutations=[('common omitted',lambda x:x['coordinates'][0].__setitem__('common_theory',0)),('program omitted',lambda x:x['complete_mathematical_programs'].pop()),('formal added to written cost',lambda x:x['coordinates'][0]['comparisons']['written_papers'].__setitem__('denominator',x['coordinates'][0]['written_denominator']+1)),('raw and printed charged together',lambda x:x['coordinates'][0]['comparisons']['including_raw_program_alternative'].__setitem__('denominator',x['coordinates'][0]['comparisons']['including_raw_program_alternative']['denominator']+x['coordinates'][0]['printed_program_cost'])),('auxiliary silently pruned',lambda x:x['complete_auxiliary_scripts'].pop()),('conditional common not prepaid',lambda x:x.__setitem__('conditional_prepaid','given common theorem')),('unknown graphic zero',lambda x:x.__setitem__('graphics_and_formula_layout_cost',0)),('exact reduced fraction wrong',lambda x:x['coordinates'][0]['comparisons']['written_papers'].__setitem__('reduced_numerator',0)),('coordinate duplicated',lambda x:x['coordinates'].__setitem__(1,copy.deepcopy(x['coordinates'][0]))),('new credit',lambda x:x.__setitem__('new_source_credit',1)),('program comparison promoted',lambda x:x['comparison_order'].reverse()),('partial application denominator',lambda x:x['coordinates'][0]['per_result'][0].__setitem__('denominator',1))]
 for name,mut in mutations:
  z=copy.deepcopy(result);mut(z)
  try:audit(z,counted,spec)
  except ValueError:controls.append(name)
  else:raise ValueError('control not rejected '+name)
 report={'status':'PASS_INDEPENDENT_AFFINE_RESULT_ARITHMETIC','author_manifest_sha256':a.author_pin,'input_manifest_sha256':IPIN,'input_review_manifest_sha256':RPIN,'frozen_exports':exports,'input_exports':i,'independent_input_review_exports':r,'PDF_cells':120,'combined_exact_fractions':90,'conditional_exact_fractions':30,'CSV_rows':120,'required_full_programs':6,'separate_full_auxiliary_scripts':3,'separate_full_formal_files':3,'negative_controls':controls,'independence':'Reviewer authored input proposal, not root numerical packet or root input review. Accepted independent input recount reused; all arithmetic and CSVs derived separately without importing author numerical functions.','no_new_extraction_GAP_Lean':True,'primary':result['primary']}
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
