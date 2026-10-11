#!/usr/bin/env python3
"""Whole manuscript fractions from accepted, unchanged listing-excluded counts."""
import csv, io, json
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(ok,msg):
 if not ok:raise ValueError(msg)
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext() as c:c.prec=40;d=format(Decimal(a)/Decimal(b),'.12f')
 return {'source_cost':a,'replacement_cost':b,'numerator':f.numerator,'denominator':f.denominator,'decimal':d}
def derive(p,counts,baseline):
 topics={};fractions=0;documents={}
 mapping={'raw_without_listings':'raw_untrimmed','selected_without_listings':'raw_selected','calibrated_selected_without_listings':'calibrated_selected'}
 for topic,boundary in p['topics'].items():
  ids=boundary['sources']+boundary['common']+[a for bundle in boundary['applications'].values() for a in bundle]
  rows={};variants=p['variants']+(['text_only_without_listings'] if topic=='Operations' else [])
  for variant in variants:
   for norm in p['normalizations']:
    for unit in p['units']:
     values={};old={}
     for ident in ids:
      key=topic+'/'+ident
      if variant=='text_only_without_listings':
       values[ident]=counts['Operations_text_only_sensitivity'][key]['metrics'][norm][unit];old[ident]=baseline[key]['text_only_sensitivity']['metrics'][norm][unit]
      else:
       values[ident]=counts['documents'][key]['metrics'][variant][norm][unit];old[ident]=baseline[key]['metrics'][mapping[variant]][norm][unit]
     common=sum(values[x] for x in boundary['common']);apps={s:sum(values[a] for a in bundle) for s,bundle in boundary['applications'].items()};source=sum(values[x] for x in boundary['sources']);written=common+sum(apps.values())
     for ident in ids:
      if ident not in ('L008','L028','N006'):need(values[ident]==old[ident],'unmasked source/replacement unchanged')
     key='/'.join((variant,norm,unit));row={'variant':variant,'normalization':norm,'unit':unit,'document_costs':values,'pre_listing_document_costs':old,'excluded_cost_by_document':{x:old[x]-values[x] for x in ids},'source_sum':source,'common_sum':common,'application_bundle_costs':apps,'whole_written':written,'written':fraction(source,written),'conditional':{s:fraction(values[s],apps[s]) for s in boundary['sources']},'software_inclusive_factor':None,'historical_source_software_cost':None};rows[key]=row;fractions+=1+len(boundary['sources'])
     for ident in ids:documents[topic+'/'+ident+'/'+key]=values[ident]
  primary='/'.join(p['primary'][k] for k in ['variant','normalization','unit']);topics[topic]={'scope':boundary,'coordinate_count':len(rows),'coordinates':rows,'primary_coordinate':primary,'primary':rows[primary]}
 return {'status':'AUTHOR_MATCHED_BOUNDARY_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW','topics':topics,'standard_coordinates_per_topic':30,'Operations_extra_text_only_coordinates':10,'exact_fractions':fractions,'document_cells':len(documents),'document_costs':documents,'whole_file_roster':load(R/'inputs/input/unchanged_software.json')['records'],'whole_file_count':46,'software_inclusive_factors':None,'historical_source_software_cost':None,'full_graphics_external_proofs_and_formalization':None,'programme_recovered':43,'programme_pending':63,'new_source_credit':0,'new_question_credit':0,'no_new_extraction_or_science_replay':True}
def csvtext(fields,rows):
 f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);return f.getvalue()
def outputs(d):
 fractions=[];topics=[];apps=[]
 for name,topic in d['topics'].items():
  for coord,c in topic['coordinates'].items():
   fractions.append({'topic':name,'coordinate':coord,'comparison':'whole',**c['written']})
   fractions.extend({'topic':name,'coordinate':coord,'comparison':s,**f} for s,f in c['conditional'].items())
  p=topic['primary'];topics.append({'topic':name,'common':p['common_sum'],'application_sum':sum(p['application_bundle_costs'].values()),**p['written']})
  apps.extend({'topic':name,'source':s,'application_bundle':'+'.join(topic['scope']['applications'][s]),**f} for s,f in p['conditional'].items())
 inventory=[{'topic':r['topic'],'category':r['category'],'path':r['file']['path'],'bytes':r['file']['bytes'],'sha256':r['file']['sha256']} for r in d['whole_file_roster']]
 return {'results.json':json.dumps(d,indent=2,ensure_ascii=False)+'\n','fractions.csv':csvtext(['topic','coordinate','comparison','source_cost','replacement_cost','numerator','denominator','decimal'],fractions),'topics.csv':csvtext(['topic','common','application_sum','source_cost','replacement_cost','numerator','denominator','decimal'],topics),'applications.csv':csvtext(['topic','source','application_bundle','source_cost','replacement_cost','numerator','denominator','decimal'],apps),'document_costs.csv':csvtext(['coordinate','cost'],[{'coordinate':k,'cost':v} for k,v in d['document_costs'].items()]),'whole_files.csv':csvtext(['topic','category','path','bytes','sha256'],inventory)}
def main():
 d=derive(load(R/'protocol.json'),load(R/'inputs/input/author_counts.json'),load(R/'inputs/input/baseline_documents.json'))
 for name,text in outputs(d).items():(R/name).write_text(text)
 print(json.dumps({k:v['primary']['written'] for k,v in d['topics'].items()}))
if __name__=='__main__':main()
