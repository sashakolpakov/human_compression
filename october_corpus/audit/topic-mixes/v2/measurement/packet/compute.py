#!/usr/bin/env python3
"""Enlarged Mixes: exact manuscript ratios and separate full-file inventories."""
from pathlib import Path
from fractions import Fraction
import argparse,csv,hashlib,json
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];NORMALS=['NFC','NFKC'];ORDER=['whole_topic','conditional_MX1','conditional_MX2']
PROTOCOL_SHA='e2e29c0235655486531beb9ba04ca150bfd62edba7ad8ccdec8560ee4e37fc44'
def need(ok,msg):
 if not ok:raise ValueError('MIXES_NUMBERS_REJECT: '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def manifest(root,pin):
 need(sha(root/'manifest.json')==pin,'exact manifest '+str(root))
 m=read(root/'manifest.json')
 for x in m['exports']:
  rel=Path(x['path']);need(not rel.is_absolute()and'..'not in rel.parts,'safe export path');f=root/rel
  need(f.stat().st_size==x['bytes']and sha(f)==x['sha256'],'exact export '+str(f))
 return len(m['exports'])
def load_inputs(inputs,prior,review):
 need(sha(HERE/'protocol.json')==PROTOCOL_SHA,'fixed numerical protocol')
 p=read(HERE/'protocol.json');need(p['evaluation_authorized']is True,'distinct input authority')
 checked={'inputs':manifest(inputs,p['input_manifest']['sha256']),'prior_inputs':manifest(prior,p['prior_input_manifest']['sha256']),'distinct_input_review':manifest(review,p['input_acceptance_manifest']['sha256'])}
 r=read(review/'review.json');need(r['status']==p['accepted_review_status']and r['proposal_manifest']['sha256']==p['input_manifest']['sha256'],'actual input acceptance')
 need(r['measurement_conditions']['software_inclusive_ratio']is None and r['measurement_conditions']['conditional_requires_whole_common_and_required_premises']is True,'accepted symmetric boundary')
 n=read(inputs/'author_counts.json');o=read(prior/'author_counts.json');policy=read(inputs/'policy.json');ind=read(review/'independent_recount.json')
 need(n['retained_accepted_inputs']==o and n['retained_cells_unchanged']is True and n['retained_PDFs_reextracted']is False,'exact old cells without re-extraction')
 need(n['new_pdf_metric_cells']==150 and n['new_raw_metric_cells']==60 and o['pdf_metric_cells']==180 and o['raw_metric_cells']==70,'all input cells retained')
 for k,row in n['documents'].items():
  for v in VARIANTS:
   for norm in NORMALS:
    for u in UNITS:need(row['metrics'][v][norm][u]==ind['documents'][k][v][norm][u],'independent reviewed PDF cell')
 for group,rows in n['raw_files'].items():
  for path,row in rows.items():
   for norm in NORMALS:
    for u in UNITS:need(row['metrics'][norm][u]==ind['raw_files'][path][norm][u],'independent reviewed raw cell')
 need(policy['whole_topic_boundary']['required_raw_programs']==p['required_files'],'two whole required files')
 docs={}
 for k,row in o['documents'].items():docs[{'U':'U0','CODE1':'OLD_CODE1','CODE2':'OLD_CODE2'}.get(k,k)]=row
 docs.update(n['documents']);need(len(docs)==11,'eleven document inventories')
 need({k:docs[k]['pages']for k in docs}=={'F005':21,'U0':5,'A1':8,'A2':4,'OLD_CODE1':4,'OLD_CODE2':3,'L016':12,'U1':4,'REQ':2,'VAL':3,'A3':6},'complete document boundary')
 raw={g:{**o['raw_files'][g],**n['raw_files'][g]}for g in ['programs','drivers','formal']}
 need([len(raw[g])for g in raw]==[6,5,2],'complete thirteen raw files')
 need(set(raw['programs'])==set(p['required_files']+p['optional_files']),'two required/four optional files')
 binding=dict(protocol_sha256=PROTOCOL_SHA,input_manifest=p['input_manifest'],prior_input_manifest=p['prior_input_manifest'],input_acceptance_manifest=p['input_acceptance_manifest'],input_review_sha256=sha(review/'review.json'),new_counts_sha256=sha(inputs/'author_counts.json'),prior_counts_sha256=sha(prior/'author_counts.json'),exports_verified=checked,root_independent_cells=460,primary_text_reextracted=False)
 return docs,raw,p,binding

def ratio(a,b):
 f=Fraction(a,b);return dict(numerator=a,denominator=b,reduced_numerator=f.numerator,reduced_denominator=f.denominator,exact_fraction=str(f),decimal=f'{float(f):.12f}')
def derive(docs,raw,p,b):
 need(p['evaluation_authorized']is True and p['software_inclusive_factor']is None,'accepted written-only evaluation')
 coordinates=[]
 for var in VARIANTS:
  for norm in NORMALS:
   for unit in UNITS:
    costs={k:x['metrics'][var][norm][unit]for k,x in docs.items()}
    filecosts={k:{path:row['metrics'][norm][unit]for path,row in rows.items()}for k,rows in raw.items()}
    inventories={'required_raw':sum(filecosts['programs'][f]for f in p['required_files']),'optional_raw':sum(filecosts['programs'][f]for f in p['optional_files']),'drivers':sum(filecosts['drivers'].values()),'formal':sum(filecosts['formal'].values()),'required_printed_alternative':costs['REQ'],'new_optional_printed_inventory':costs['VAL'],'historical_mixed_appendices_inventory':costs['OLD_CODE1']+costs['OLD_CODE2']}
    comparisons={k:ratio(sum(costs[x]for x in d['numerator']),sum(costs[x]for x in d['denominator']))for k,d in p['comparison_definitions'].items()}
    coordinates.append(dict(variant=var,normalization=norm,unit=unit,document_costs=costs,source_cost=sum(costs[x]for x in p['source_documents']),common_cost=sum(costs[x]for x in p['common_documents']),application_costs={k:sum(costs[x]for x in a['documents'])for k,a in p['applications'].items()},written_denominator=sum(costs[x]for x in ['U0','U1','A1','A2','A3']),separate_inventory_costs=inventories,raw_file_costs=filecosts,comparisons=comparisons))
 primary=next(c for c in coordinates if [c[k]for k in ['variant','normalization','unit']]==p['primary'])
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',topic=p['topic'],originals=p['originals'],original_count=2,input_bindings=b,coordinate_count=30,exact_fraction_count=90,whole_topic_fraction_count=30,conditional_fraction_count=60,comparison_order=ORDER,primary=primary,coordinates=coordinates,document_pages={k:r['pages']for k,r in docs.items()},complete_document_metric_vectors={k:r['metrics']for k,r in docs.items()},whole_raw_file_inventory=raw,required_files=p['required_files'],optional_files=p['optional_files'],conditional_prepaid=p['conditional_prepaid'],common_documents=p['common_documents'],application_documents=p['applications'],comparison_kind=p['comparison_kind'],source_dispositions=p['source_dispositions'],source_scope_limits=p['remaining_scope_limits'],software_inclusive_factor=None,historical_software_cost=None,optional_validation_symmetric_exclusion=True,raw_and_printed_alternatives=True,required_finite_premises_not_optional=True,whole_umbrellas_charged_once=True,overlap_discount=False,cross_topic_discount=False,partial_formal_declarations=6,end_to_end_formalization=False,unknown_costs=p['unknown_costs'],source_executable_listing_present=False,new_source_credit=0,new_question_credit=0,source_text_fonts_images_exported=False,sawtooth_claim=False,theorem_node_complexity_factor=False,historical_originality_inference=False,old_F005_inclusive_factors='Preserved only in their immutable historical packet; not recomputed or relabelled under the current symmetric policy.')
def csv_rows(r):return [dict(variant=c['variant'],normalization=c['normalization'],unit=c['unit'],comparison=k,**c['comparisons'][k])for c in r['coordinates']for k in ORDER]
def write_csv(p,rows):
 with p.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def evaluate(inputs,prior,review,out):
 need(not out.exists(),'fresh numeric output');data=load_inputs(inputs,prior,review);r=derive(*data);out.mkdir(parents=True);write(out/'results.json',r);write(out/'input_bindings.json',data[3]);write_csv(out/'comparisons.csv',csv_rows(r));return r
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--inputs',type=Path,required=True);a.add_argument('--prior-inputs',type=Path,required=True);a.add_argument('--input-review',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();r=evaluate(x.inputs,x.prior_inputs,x.input_review,x.out);print(json.dumps(r['primary'],indent=2))
