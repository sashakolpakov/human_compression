#!/usr/bin/env python3
"""Arithmetic on adopted complete-document counts; no extraction or proof execution."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import csv, io, json, hashlib
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(ok,msg):
 if not ok:raise ValueError(msg)
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext() as c:
  c.prec=40; value=format(Decimal(a)/Decimal(b),'.12f')
 return {'source_cost':a,'replacement_cost':b,'numerator':f.numerator,'denominator':f.denominator,'decimal':value}
def key(v,n,u):return '/'.join((v,n,u))
def derive(protocol,counts):
 order=protocol['source_order'];apps=protocol['applications'];policy=load(R/'inputs/input/policy.json')
 rawrows=[];groups={k:[] for k in ['required_programs','required_data','optional_validation','operational_drivers','partial_formal']}
 for collection,files in counts['raw_files'].items():
  for path,item in files.items():
   if collection=='programs_and_data':
    role=next(x['role'] for x in policy['programs_and_data'] if x['path']==path)
    group={'required finite proof':'required_programs','required certificate data':'required_data','validation only':'optional_validation'}[role]
   else:group={'operational_drivers':'operational_drivers','formal_files':'partial_formal'}[collection];role='operational' if group=='operational_drivers' else 'partial formal evidence'
   row={'path':path,'role':role,'group':group,**item};rawrows.append(row);groups[group].append(row)
 summaries={g:{'files':len(rows),'literal_bytes':sum(x['bytes'] for x in rows),'metrics':{n:{u:sum(x['metrics'][n][u] for x in rows) for u in protocol['units']} for n in protocol['normalizations']}} for g,rows in groups.items()}
 coordinates={}
 for v in protocol['variants']:
  for n in protocol['normalizations']:
   for u in protocol['units']:
    costs={k:row['metrics'][v][n][u] for k,row in counts['documents'].items()}
    source=sum(costs[x] for x in order);appsum=sum(costs[apps[x]] for x in order);ours=costs['U']+appsum
    coordinates[key(v,n,u)]={'variant':v,'normalization':n,'unit':u,'document_costs':costs,'source_sum':source,'whole_common':costs['U'],'application_sum':appsum,'whole_written':ours,'written':fraction(source,ours),'conditional':{x:fraction(costs[x],costs[apps[x]]) for x in order},'separate_software':{'required_printed_with_data':costs['REQUIRED'],'optional_printed':costs['VALIDATION'],'raw':{g:d['metrics'][n][u] for g,d in summaries.items()},'software_inclusive_factor':None,'historical_source_software_cost':None}}
 pk=key(*[protocol['primary'][k] for k in ['variant','normalization','unit']]);primary=coordinates[pk]
 stages=[{'stage':0,'acquired':'whole U','source_written':0,'replacement_written':primary['whole_common'],'required_software_and_external_preconditions_separate':True}]
 a=0;b=primary['whole_common']
 for i,x in enumerate(order,1):
  a+=primary['document_costs'][x];b+=primary['document_costs'][apps[x]];stages.append({'stage':i,'acquired':apps[x]+' for '+x,'source_written':a,'replacement_written':b,'required_software_and_external_preconditions_separate':True})
 return {'status':'AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW','title':protocol['title'],'source_ids':order,'applications':apps,'original_count':5,'source_pages':sum(counts['documents'][x]['pages'] for x in order),'whole_common_pages':counts['documents']['U']['pages'],'application_pages':{x:counts['documents'][apps[x]]['pages'] for x in order},'primary_coordinate':pk,'coordinate_count':30,'exact_fraction_count':180,'coordinates':coordinates,'primary':primary,'whole_file_inventory':rawrows,'whole_file_group_costs':summaries,'physical_appendices':{'required_with_data':20,'optional':7},'primary_acquisition':stages,'software_inclusive_factors':None,'historical_source_software_cost':None,'unknown_costs':protocol['unknown_costs'],'no_source_extraction':True,'no_science_replay':True,'source_registration_or_question_credit':0}
def csvtext(fields,rows):
 f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);return f.getvalue()
def outputs(result):
 fields=['coordinate','comparison','source_cost','replacement_cost','numerator','denominator','decimal'];rows=[];costrows=[]
 for k,c in result['coordinates'].items():
  rows.append({'coordinate':k,'comparison':'written',**c['written']})
  rows.extend({'coordinate':k,'comparison':x,**f} for x,f in c['conditional'].items())
  costrows.extend({'coordinate':k,'document':x,'cost':v} for x,v in c['document_costs'].items())
 rawrows=[]
 for f in result['whole_file_inventory']:
  for n,m in f['metrics'].items():
   for u in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']:
    rawrows.append({'path':f['path'],'role':f['role'],'group':f['group'],'bytes':f['bytes'],'sha256':f['sha256'],'normalization':n,'unit':u,'cost':m[u]})
 return {'results.json':json.dumps(result,indent=2,ensure_ascii=False)+'\n','fractions.csv':csvtext(fields,rows),'document_costs.csv':csvtext(['coordinate','document','cost'],costrows),'whole_files.csv':csvtext(['path','role','group','bytes','sha256','normalization','unit','cost'],rawrows),'acquisition.csv':csvtext(list(result['primary_acquisition'][0]),result['primary_acquisition'])}
def main():
 p=load(R/'protocol.json');d=derive(p,load(R/'inputs/input/author_counts.json'))
 for name,text in outputs(d).items():(R/name).write_text(text)
 print(json.dumps({'primary':d['primary']['written'],'conditionals':d['primary']['conditional'],'software_inclusive_factors':None}))
if __name__=='__main__':main()
