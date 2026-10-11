#!/usr/bin/env python3
"""Exact fractions from independently accepted whole-document input counts."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,json,hashlib,csv
HERE=Path(__file__).resolve().parent
TOPICS={'Matching':dict(source='F015',common='U_M',application='M1',program='M_CODE'),'ChiralEnumeration':dict(source='L028',common='U_CE',application='CE1',program='CE_CODE')}
def need(ok,message):
 if not ok:raise ValueError('ADDITIONAL_COMPARISON_REJECT: '+message)
def sha(b):return hashlib.sha256(b).hexdigest()
def frac(n,d):
 f=Fraction(n,d)
 with localcontext() as c:c.prec=40;value=str(Decimal(n)/Decimal(d))
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=value)
def load(root,protocol):
 data={}
 for k,row in protocol['bindings'].items():
  b=(root/row['path']).read_bytes();need(sha(b)==row['sha256'] and len(b)==row['bytes'],'exact accepted input '+k);data[k]=json.loads(b)
 need(data['author_inputs']['status']=='AUTHOR_FROZEN_PENDING_DISTINCT_INPUT_REVIEW' and data['independent_input_review']['status']=='ROOT_ACCEPTED_INPUTS','distinct accepted input; original status immutable')
 need(data['independent_input_review']['author_manifest_sha256']==protocol['bindings']['author_inputs']['sha256'],'independent review exact input')
 return data

def compute(p,d):
 need(p['original_manuscripts']==2 and not p['cross_topic_discount'] and p['full_code_charge_once'],'two topics, independently paid')
 c=d['counts'];rows=[]
 for variant in p['variants']:
  for normalization in p['normalizations']:
   for unit in p['units']:
    for topic,ids in TOPICS.items():
     values={name:c['documents'][key]['metrics'][variant][normalization][unit] for name,key in ids.items()}
     raw={category:sum(x['metrics'][normalization][unit] for x in files.values() if x['topic']==topic) for category,files in c['raw_files'].items()}
     n=values['source'];written=values['common']+values['application'];ratios=dict(written=frac(n,written),including_printed_programs=frac(n,written+values['program']),including_raw_programs=frac(n,written+raw['complete_programs']),conditional_application=frac(n,values['application']))
     rows.append(dict(topic=topic,source_id=ids['source'],variant=variant,normalization=normalization,unit=unit,document_costs=values,raw_costs=raw,written_denominator=written,comparisons=ratios,conditional_acquisition=dict(common_key=ids['common'],whole_common_cost=values['common'],whole_printed_program_cost=values['program'],whole_raw_program_cost=raw['complete_programs'],printed_and_raw_are_alternatives=True)))
 primary={t:next(r for r in rows if r['topic']==t and all(r[k]==v for k,v in p['primary'].items())) for t in TOPICS}
 return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',original_manuscripts=2,source_ids=['F015','L028'],independent_topics=2,coordinates_per_topic=30,exact_fractions=240,rows=rows,primary=primary,source_contracts_unchanged=True,old_27_original_report_unchanged=True,unknown_costs=dict(retained_external=None,graphics=None,historical_software=None,full_formalization=None),new_source_credit=0,new_question_credit=0,full_formalization_claim=False)

def write_outputs(out,r):
 (out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
 with (out/'comparisons.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['topic','source','variant','normalization','unit','comparison','numerator','denominator','decimal'])
  for row in r['rows']:
   for k,v in row['comparisons'].items():w.writerow([row['topic'],row['source_id'],row['variant'],row['normalization'],row['unit'],k,v['numerator'],v['denominator'],v['decimal']])

def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True)
 p=json.loads((HERE/'protocol.json').read_text());r=compute(p,load(args.study_root,p));write_outputs(args.out,r)
 print(json.dumps({k:{kind:v['decimal'] for kind,v in x['comparisons'].items()} for k,x in r['primary'].items()},indent=2))
if __name__=='__main__':main()
