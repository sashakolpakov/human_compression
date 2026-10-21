#!/usr/bin/env python3
"""Complete locally projective arithmetic from accepted input integers only."""
import argparse,csv,hashlib,json
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
PINS={'inputs':'396355b0cc7fac4c1c0af5a18af4a148195b8abebdbd49699a10c7cfdf21cb74','input_review':'53338911b067231c2ae68188a22d3e630147fb82be0af814253fa040aab9237c'}
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
NORMS=('NFC','NFKC')
SOURCES=('L084','L095');APPS={'L084':'A1','L095':'A2'}
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
 a=load(root/'inputs/author_counts.json');r=load(root/'input_review/recount.json');review=load(root/'input_review/review.json');policy=load(root/'protocol.json');old=load(root/'inputs/policy.json')
 need(review['status']=='INDEPENDENTLY_ACCEPTED_LOCALLY_PROJECTIVE_MEASUREMENT_INPUTS' and review['requested_corrections']==[],'distinct inputs accepted')
 need(review['author_manifest_sha256']==PINS['inputs'],'exact reviewed inputs')
 need(sha(root/'protocol.json')==load(root/'protocol_freeze.json')['protocol_sha256'],'fixed numerical boundary')
 need(set(a['documents'])=={'L084','L095','U','TABLES','A1','A2','CODE'},'complete documents')
 for k,v in a['documents'].items():
  for f in ['pages','pdf_sha256','metrics']:need(v[f]==r['documents'][k][f],'all independent PDF counts')
 need(a['raw_files']==r['raw_files'],'all whole independent raw counts')
 need([len(a['raw_files'][k]) for k in ['programs','required_data','operational_drivers']]==[6,1,3],'complete raw classes')
 need(sum(x['bytes'] for x in a['raw_files']['required_data'].values())==39150,'entire mandatory JSON')
 pc=load(root/'inputs/protocol.json')['primary_coordinate'];need(policy['primary']==[pc[k] for k in ['variant','normalization','unit']],'accepted primary unchanged')
 return a,policy,old

def frac(n,d):
 f=Fraction(n,d);return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,exact_fraction=str(f),factor=float(f))

def derive(a,p,old):
 cc=[]
 for v in VARIANTS:
  for n in NORMS:
   for unit in UNITS:
    d={k:row['metrics'][v][n][unit] for k,row in a['documents'].items()};raw={cat:sum(row['metrics'][n][unit] for row in rr.values()) for cat,rr in a['raw_files'].items()}
    s=sum(d[k] for k in SOURCES);common=d['U']+d['TABLES'];apps=d['A1']+d['A2'];w=common+apps;data=raw['required_data'];printed=d['CODE'];rp=raw['programs']
    cc.append({'variant':v,'normalization':n,'unit':unit,'document_costs':d,'source_cost':s,'whole_common_cost':common,'application_cost':apps,'written_cost':w,'printed_program_cost':printed,'raw_program_cost':rp,'mandatory_data_cost':data,'operational_driver_cost_separate':raw['operational_drivers'],'comparisons':{'written_papers':frac(s,w),'printed_programs_plus_mandatory_data':frac(s,w+printed+data),'raw_programs_plus_mandatory_data':frac(s,w+rp+data)},'conditional_applications':{src:frac(d[src],d[APPS[src]]) for src in SOURCES},'conditional_acquisition':{'common_proof':d['U'],'common_tables':d['TABLES'],'whole_common':common,'printed_program_option':printed,'raw_program_option':rp,'mandatory_raw_data':data,'printed_total':common+printed+data,'raw_total':common+rp+data}})
 primary=next(c for c in cc if [c[k] for k in ['variant','normalization','unit']]==p['primary'])
 return {'schema':'LocallyProjective_complete_document_comparison_v1','status':'AUTHOR_NUMERICAL_COMPARISON_PENDING_DISTINCT_REVIEW','calculation_author':'enumeration_volume','input_author':'enumeration_volume','input_reviewer':'enumeration_review','numerical_independent_reviewer':None,'originals':2,'source_ids':list(SOURCES),'source_record_count':52,'historical_rows':145,'source_editions':old['primary_editions'],'primary':primary,'coordinates':cc,'coordinates_count':30,'exact_combined_fractions':90,'exact_conditional_fractions':60,'whole_common_charged_once':True,'complete_common_documents':['U','TABLES'],'all_applications_charged':True,'cross_topic_discount':False,'sibling_application_free_premise':False,'conditional_prepayment':p['conditional_formula'],'programme_boundary':{'complete_required_programs':6,'raw_program_bytes':24255,'complete_printed_program_pages':6,'required_data_files':1,'required_data_bytes':39150,'required_data_in_both_routes':True,'data_purpose':'Entire 145-row historical reconciliation data, not a subgroup-enumeration premise; no metadata or historical field pruning.','printed_program_is_data_substitute':False,'printed_and_raw_are_alternatives':True,'operational_drivers_separate':3,'driver_raw_bytes':32220,'generated_outputs_separate':11,'generated_output_bytes':3470182,'output_not_additional_enumeration_input':True,'selected_runtime_model_pins':13,'formal_files':0,'formal_declarations':0},'physical_extent':{'source_pages':{'L084':2,'L095':15},'common_proof_pages':7,'common_tables_pages':5,'application_pages':{'L084':2,'L095':3},'written_replacement_pages':17,'printed_program_pages':6,'all_input_pages':40},'unknown_costs':p['unknown_costs'],'primary_policy':'Complete calibrated selected PDF extraction, NFC, characters without whitespace; raw untrimmed and raw selected sensitivities retained.','glyph_scope':'Eight classes, 61 occurrence-bound repairs; mapsto tails remain separate from adjacent arrows. Historical erroneous counts are not corrected by glyph calibration.','graphic_scope':'L095 table rules are inline images; graphics/layout construction cost remains unknown, not zero.','source_qualification':'L084 is the complete two-page publisher erratum; L095 is the full fifteen-page July 2003 arXiv v1, not an unseen journal edition.','retained_science':'52 dispositions and exact corrections bound in inputs/scientific_source_map.json; historical g.txt is unavailable and unused.','science_and_GAP_Lean_replayed':False,'full_source_formalized':False,'new_source_credit':0,'new_question_credit':0,'public_mutations':False}

def csv_rows(r):
 out={k:[] for k in ['overall_costs','conditional_costs','document_costs','software_costs','acquisition_costs']}
 for c in r['coordinates']:
  key={k:c[k] for k in ['variant','normalization','unit']}
  for name,f in c['comparisons'].items():out['overall_costs'].append({**key,'comparison':name,**f})
  for src,f in c['conditional_applications'].items():out['conditional_costs'].append({**key,'source':src,'application':APPS[src],'prepaid':'Whole U + whole TABLES + all six programs + entire source_tables.json + retained inputs',**f})
  for k,n in c['document_costs'].items():out['document_costs'].append({**key,'document':k,'cost':n})
  for k in ['printed_program_cost','raw_program_cost','mandatory_data_cost','operational_driver_cost_separate']:out['software_costs'].append({**key,'role':k,'cost':c[k]})
  out['acquisition_costs'].append({**key,**c['conditional_acquisition']})
 return out

def write_result(out,r):
 out.mkdir(parents=True,exist_ok=False);dump(out/'results.json',r)
 for name,rows in csv_rows(r).items():
  with (out/(name+'.csv')).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output required');r=derive(*accepted_inputs());write_result(a.out,r);print(json.dumps({'primary':r['primary'],'exact_fractions':150}))
