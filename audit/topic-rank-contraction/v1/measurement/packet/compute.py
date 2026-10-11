#!/usr/bin/env python3
"""L037 exact arithmetic from two immutable, accepted input packets; no extraction."""
import argparse,csv,hashlib,json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
PINS={'inputs':'4df2508c988ca14e00c550a8da68d485c3631061bbf19888b86f521886deefaf','input_review':'4b0e9d254043c5414bc5281607a994bf52e0190c79c59ca0a50c89ab65708b4a'}
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
NORMALIZATIONS=('NFC','NFKC')

def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def accepted_inputs(root=HERE):
 for folder,h in PINS.items():
  need(sha(root/folder/'manifest.json')==h,'accepted immutable manifest '+folder)
  for e in load(root/folder/'manifest.json')['exports']:
   p=root/folder/e['path'];need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'unchanged export '+str(p))
 a=load(root/'inputs/author_counts.json');r=load(root/'input_review/recount.json');review=load(root/'input_review/review.json');policy=load(root/'protocol.json')
 need(review['status']=='ACCEPTED_UNCHANGED' and review['findings']==[],'independent inputs accepted')
 need(review['author_manifest_sha256']==PINS['inputs'],'exact reviewed inputs')
 need(sha(root/'protocol.json')==load(root/'protocol_freeze.json')['protocol_sha256'],'fixed numerical boundary')
 need(set(a['documents'])=={'L037','U','A1','CODE'} and a['documents']==r['document_counts'],'all independent document counts')
 for cat,rs in a['raw_files'].items():
  for path,row in rs.items():
   other=r['raw_counts'][path]
   need(other['category']==cat and all(other[k]==row[k] for k in ['sha256','bytes','metrics']),'whole raw counts and roles')
 need(len(r['raw_counts'])==3 and a['source_rows']==22 and a['proof_contexts']==20,'complete scope')
 return a,policy

def frac(n,d):
 f=Fraction(n,d);return {'numerator':n,'denominator':d,'reduced_numerator':f.numerator,'reduced_denominator':f.denominator,'exact_fraction':str(f),'factor':float(f)}

def derive(a,policy):
 coords=[]
 for variant in VARIANTS:
  for norm in NORMALIZATIONS:
   for unit in UNITS:
    costs={k:v['metrics'][variant][norm][unit] for k,v in a['documents'].items()}
    raw={cat:sum(v['metrics'][norm][unit] for v in rows.values()) for cat,rows in a['raw_files'].items()}
    s,u,app,p=[costs[k] for k in ('L037','U','A1','CODE')]
    coords.append({'variant':variant,'normalization':norm,'unit':unit,'document_costs':costs,'written_cost':u+app,'printed_program_cost':p,'raw_program_cost':raw['programs'],'driver_cost_separate':raw['drivers'],'formal_file_cost_separate':raw['formal'],'conditional_acquisition':{'whole_common':u,'complete_printed_program_option':p,'complete_raw_program_option':raw['programs'],'printed_total':u+p,'raw_total':u+raw['programs']},'comparisons':{'written_papers':frac(s,u+app),'including_printed_program':frac(s,u+app+p),'including_raw_program_alternative':frac(s,u+app+raw['programs'])},'conditional_application':frac(s,app)})
 primary=next(c for c in coords if [c[k] for k in ['variant','normalization','unit']]==policy['primary'])
 sensitive={v:{norm:{name:{'minimum':min(c['comparisons'][name]['factor'] for c in coords if c['variant']==v and c['normalization']==norm),'maximum':max(c['comparisons'][name]['factor'] for c in coords if c['variant']==v and c['normalization']==norm)} for name in ['written_papers','including_printed_program','including_raw_program_alternative']} for norm in NORMALIZATIONS} for v in VARIANTS}
 return {'schema':'L037_complete_document_comparison_v1','status':'AUTHOR_NUMERICAL_COMPARISON_PENDING_DISTINCT_REVIEW','calculation_author':'enumeration_volume','input_author':'enumeration_review','input_reviewer':'enumeration_volume','numerical_independent_reviewer':None,'role_disclosure':'The numerical author independently reviewed inputs but does not independently accept this new calculation. Root numerical review remains necessary.','source_id':'L037','source_edition':'arXiv:1812.01055v2, 3 May 2019','source_rows':22,'proof_contexts':20,'originals':1,'primary':primary,'coordinates':coords,'coordinates_count':30,'exact_combined_fractions':90,'exact_conditional_fractions':30,'sensitivity_ranges':sensitive,'whole_common_charged_once':True,'all_application_pages_charged':True,'conditional_prepayment':'Acquire the entire local common paper U and the complete declared program before comparing source/application.','old_Topic_B_common_free_premise':False,'cross_topic_discount':False,'programme_boundary':{'complete_programs':1,'local_finite_certificate_programs':1,'uniform_required_programs':0,'printed_pdf_pages':1,'raw_bytes':2680,'printed_and_raw_are_alternatives':True,'driver_files_separate':1,'driver_raw_bytes':6950,'Lean_files_separate':1,'Lean_raw_bytes':1727,'scoped_declarations':4,'full_source_formalized':False,'required_finite_role':'Literal matrix and three A11 example certificates; includes doubled-edge validation.','uniform_proof_does_not_depend_on_finite_output':True},'physical_extent':{'source_pages':6,'common_pages':3,'application_pages':5,'written_replacement_pages':8,'printed_program_pages':1,'all_input_pages':15},'primary_policy':'Complete raw untrimmed extraction, NFC, characters without whitespace. Selected and calibrated coordinates are sensitivities.','diagram_policy':'All 264 XYCIRC events retain literal /c16 through /c23 strings in every coordinate. No replacement by circles or deletion; full graphical/layout cost remains unknown.','glyph_sensitivity':'Eight occurrence-bound CMEX bracket-component repairs affect text hashes but not the five metric values. Each component is preserved.','retained_external_proof_cost':None,'full_graphic_layout_cost':None,'historical_software_cost':None,'full_formalization_cost':None,'minimal_mathematical_complexity':None,'full_visible_text_claim':False,'source_question':'Conjecture 5.1 is unresolved by this work.','new_source_credit':0,'new_question_credit':0,'new_formal_credit':0,'public_mutations':False}

def rows(result):
 overall=[];conditional=[];documents=[];software=[]
 for c in result['coordinates']:
  k={x:c[x] for x in ['variant','normalization','unit']}
  for name,f in c['comparisons'].items():overall.append({**k,'comparison':name,**f})
  conditional.append({**k,'source':'L037','application':'A1','prepaid':result['conditional_prepayment'],**c['conditional_application']})
  for key,value in c['document_costs'].items():documents.append({**k,'document':key,'cost':value})
  for name in ['printed_program_cost','raw_program_cost','driver_cost_separate','formal_file_cost_separate']:software.append({**k,'role':name,'cost':c[name]})
 return dict(overall_costs=overall,conditional_costs=conditional,document_costs=documents,software_costs=software)

def write_csv(path,records):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)

def write_result(out,result):
 out.mkdir(parents=True,exist_ok=False);dump(out/'results.json',result)
 for name,records in rows(result).items():write_csv(out/(name+'.csv'),records)

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output required');r=derive(*accepted_inputs());write_result(a.out,r);print(json.dumps({'primary':r['primary'],'exact_fractions':120}))
if __name__=='__main__':main()
