#!/usr/bin/env python3
"""Exact F005 costs from accepted whole-document inputs; approval gate precedes arithmetic."""
from pathlib import Path
from fractions import Fraction
import argparse,csv,hashlib,json
H=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC']
ORDER=['written_papers','conditional_application','including_printed_programs','including_raw_programs_alternative']
def need(ok,msg):
 if not ok:raise ValueError('F005_COST_REJECT: '+msg)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def bind(root,pin):
 need(sha(root/'manifest.json')==pin,'exact accepted manifest')
 rows=read(root/'manifest.json')['exports']
 for r in rows:
  f=Path(r['path']);need(not f.is_absolute() and '..'not in f.parts,'safe export path');p=root/f
  need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'bound export '+str(f))
 return len(rows)
def inputs(a):
 p=read(H/'protocol.json');before=read(H/'protocol_before_input_acceptance.json')
 need(p['evaluation_authorized']is True and isinstance(p['input_acceptance'],dict),'distinct input acceptance required BEFORE factor evaluation')
 q=dict(p);q.update(status=before['status'],input_acceptance=None,evaluation_authorized=False)
 need(q==before,'only input acceptance metadata changed since fixed numerical protocol')
 counts_verified=bind(a.inputs,p['input_manifest_sha256']);review_verified=bind(a.input_review,p['input_acceptance']['manifest_sha256'])
 acceptance=read(a.input_review/p['input_acceptance']['review_path'])
 need(acceptance['status']==p['input_acceptance']['accepted_status'] and acceptance['factors_now_permitted_for_exact_reviewed_inputs']is True and acceptance['input_manifest_sha256']==p['input_manifest_sha256'],'actual distinct acceptance of these inputs and evaluation authority')
 c=read(a.inputs/'author_counts.json');policy=read(a.inputs/'policy.json');boundary=read(a.inputs/'source_boundary.json')
 independent=read(a.input_review/'independent_counts.json')
 need(c['documents']==independent['documents'] and c['raw_files']==independent['raw_files'],'all independent PDF/raw cells agree')
 need(c['ratio']is None and c['pdf_metric_cells']==180 and c['raw_metric_cells']==70,'exact input-only cells')
 need(list(c['documents'])==['F005','U','A1','A2','CODE1','CODE2'],'six complete documents')
 need([c['documents'][k]['pages']for k in c['documents']]==[21,5,8,4,4,3],'whole source/common/local/exception/code pages')
 need([len(c['raw_files'][g])for g in ['programs','drivers','formal']]==[3,3,1],'all whole raw files')
 need(policy['variants']==VARIANTS and policy['normalizations']==FORMS and policy['units']==UNITS,'accepted thirty-coordinate ruler')
 need(policy['scientific_acceptance']['root_manifest_sha256']==p['scientific_root_manifest_sha256'],'distinct complete science acceptance')
 need(policy['source_rows']==35 and policy['source_questions_excluded']==3,'principal/background rows and unanswered problems')
 need(policy['principal_required_programs']==1 and policy['validation_programs']==2 and policy['partial_formal_declarations']==2,'exact finite/formal scope')
 b=dict(protocol_sha256=sha(H/'protocol.json'),fixed_before_evaluation_sha256=sha(H/'protocol_before_input_acceptance.json'),input_manifest_sha256=p['input_manifest_sha256'],input_acceptance=p['input_acceptance'],scientific_root_manifest_sha256=p['scientific_root_manifest_sha256'],exports_checked=dict(inputs=counts_verified,input_review=review_verified),count_sha256=sha(a.inputs/'author_counts.json'),policy_sha256=sha(a.inputs/'policy.json'),source_boundary_sha256=sha(a.inputs/'source_boundary.json'))
 return c,policy,boundary,b,p

def fraction(n,d):
 f=Fraction(n,d);return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,exact_fraction=str(f),decimal=f'{float(f):.12f}')
def derive(c,policy,boundary,b,p):
 need(p['evaluation_authorized']is True and p['input_acceptance']is not None,'no arithmetic before accepted inputs')
 coordinates=[]
 for v in VARIANTS:
  for n in FORMS:
   for u in UNITS:
    d={k:x['metrics'][v][n][u]for k,x in c['documents'].items()};raw={k:sum(x['metrics'][n][u]for x in rows.values())for k,rows in c['raw_files'].items()}
    den={k:sum(raw['programs']if x=='raw:programs'else d[x]for x in ids)for k,ids in p['comparison_denominators'].items()}
    coordinates.append(dict(variant=v,normalization=n,unit=u,document_costs=d,raw_costs=raw,source_cost=d['F005'],common_cost=d['U'],application_cost=d['A1']+d['A2'],written_denominator=den['written_papers'],printed_program_cost=d['CODE1']+d['CODE2'],comparisons={k:fraction(d['F005'],den[k])for k in ORDER}))
 primary=next(x for x in coordinates if [x[k]for k in ['variant','normalization','unit']]==p['primary'])
 science=boundary['topic_Mix_F005_root_review/review.json']
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',topic=p['topic'],source_id='F005',original_manuscripts=1,input_bindings=b,coordinates=coordinates,coordinate_count=30,exact_fraction_count=120,combined_exact_fractions=90,conditional_exact_fractions=30,comparison_order=ORDER,primary=primary,conditional_prepaid=p['conditional_prepaid'],whole_common_once=True,whole_application_including_exception=True,cross_topic_discount=False,overlap_discount=False,raw_and_printed_alternatives=True,program_boundary=p['program_roles'],raw_file_inventory=c['raw_files'],document_pages={k:x['pages']for k,x in c['documents'].items()},source_contract_rows=35,unanswered_final_problems=3,retained_inputs=science['retained_inputs'],accepted_literal_counterexample_targets=science['accepted_literal_counterexample_targets'],accepted_qualified_counterexample_targets=science['accepted_qualified_counterexample_targets'],unresolved_literal_correspondence=science['unresolved_literal_correspondence'],unknown_costs=p['unknown_costs'],source_exclusions=policy['corrected_source_scope'],whole_source_formalized=False,finite_tests_as_uniform_proof=False,all_drivers_and_Lean_charged_in_factors=False,new_scientific_credit=0,new_question_credit=0,sawtooth_claim=False,minimal_proof_complexity_claim=False,historical_priority_claim=False,source_text_fonts_images_exported=False,interpretation='Complete declared extracted-text costs for the corrected principal contract; neither total research effort nor historical originality is inferred.')
def csv_rows(r):
 return [dict(variant=c['variant'],normalization=c['normalization'],unit=c['unit'],comparison=k,**c['comparisons'][k])for c in r['coordinates']for k in ORDER]
def save_csv(p,rows):
 with p.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--input-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists(),'fresh output');data=inputs(a);r=derive(*data);a.out.mkdir(parents=True);write(a.out/'results.json',r);write(a.out/'input_bindings.json',data[3]);save_csv(a.out/'comparisons.csv',csv_rows(r));print('120 exact comparisons generated from distinctly accepted inputs; independent numerical review pending.')
if __name__=='__main__':main()
