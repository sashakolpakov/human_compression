#!/usr/bin/env python3
"""Exact arithmetic on adopted unified-A document counts; no extraction."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import json,hashlib,csv,io
R=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(ok,msg):
 if not ok:raise ValueError('A_NUMERIC_REJECT: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext()as c:c.prec=50;d=format(Decimal(a)/Decimal(b),'.12f')
 return dict(source_cost=a,replacement_cost=b,numerator=f.numerator,denominator=f.denominator,decimal=d)
def key(v,n,u):return '/'.join((v,n,u))
def role_group(role):
 return 'required_program_or_data'if role.startswith('required')else'inherited_auxiliary'if role=='inherited_auxiliary'else'operational_runners'if role in('current_operational_driver','operational_validation_runner')else'partial_formal_files'
def derive(proto,counts,inventory,prior):
 order=proto['source_order'];apps=proto['applications'];roles={r['id']:r for r in inventory};raw=[]
 for rid,item in counts['raw_files_measured'].items():
  rule=roles[rid];need(item['file']['sha256']==rule['file']['sha256']and item['file']['bytes']==rule['file']['bytes']and item['role']==rule['role'],'whole raw identity/role; inherited public routing only')
  raw.append(dict(**rule,metrics=item['metrics'],cost_group=role_group(rule['role'])))
 groups={group:dict(files=sum(r['cost_group']==group for r in raw),literal_bytes=sum(r['file']['bytes']for r in raw if r['cost_group']==group),metrics={n:{u:sum(r['metrics'][n][u]for r in raw if r['cost_group']==group)for u in proto['units']}for n in proto['normalizations']})for group in dict.fromkeys(r['cost_group']for r in raw)}
 coords={}
 for v in proto['variants']:
  for n in proto['normalizations']:
   for u in proto['units']:
    k=key(v,n,u);d={x:z['metrics'][v][n][u]for x,z in counts['documents'].items()};source=sum(d[x]for x in order);local=sum(d[apps[x]]for x in order);whole=d['U']+local
    conditionals={x:fraction(d[x],d[apps[x]])for x in order};old=prior['coordinates'][k]
    need(all(conditionals[x]==old['conditional'][x]for x in prior['source_ids']),'all240 inherited conditional fractions unchanged')
    need(all(d[x]==value for x,value in old['document_costs'].items()),'all600 previous PDF cost cells unchanged')
    coords[k]=dict(variant=v,normalization=n,unit=u,document_costs=d,source_sum=source,whole_common=d['U'],application_sum=local,whole_written=whole,written=fraction(source,whole),conditional=conditionals,prior_whole_written=old['written'],addition=dict(source='L121',application='A9',source_cost=d['L121'],application_cost=d['A9'],extra_common_cost=0,reason='Same entire unchanged common paper is charged once within this enlarged topic.'),separate_software=dict(old_partial_printed_appendices={x:d[x]for x in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']},old_partial_printed_sum=sum(d[x]for x in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']),complete_enlarged_printed_cost=None,raw_group_costs={g:r['metrics'][n][u]for g,r in groups.items()},software_inclusive_factor=None,historical_source_software_cost=None))
 pk=key(*[proto['primary'][k]for k in ['variant','normalization','unit']]);primary=coords[pk];stages=[dict(stage=0,acquired='whole U',source_written=0,replacement_written=primary['whole_common'],required_program_data_and_external_premises_separate=True)]
 source=0;ours=primary['whole_common']
 for i,x in enumerate(order,1):source+=primary['document_costs'][x];ours+=primary['document_costs'][apps[x]];stages.append(dict(stage=i,acquired=apps[x]+' for '+x,source_written=source,replacement_written=ours,required_program_data_and_external_premises_separate=True))
 return dict(status='AUTHOR_NINE_ORIGINAL_A_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',title=proto['title'],source_ids=order,applications=apps,source_count=9,source_pages=131,whole_common_pages=23,application_pages={x:counts['documents'][apps[x]]['pages']for x in order},old_partial_printed_appendix_pages={x:counts['documents'][x]['pages']for x in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']},complete_enlarged_printed_program_representation=None,primary_coordinate=pk,coordinate_count=30,exact_fraction_count=300,inherited_conditional_fractions_preserved=240,coordinates=coords,primary=primary,whole_file_inventory=raw,whole_file_group_costs=groups,primary_acquisition=stages,software_inclusive_factors=None,optional_validation_inclusive_factors=None,historical_source_software_cost=None,full_formalization_cost=None,unknown_costs=proto['unknown_costs'],cross_topic_discount=False,new_source_credit=0,new_question_credit=0,new_formal_credit=0,no_extraction=True,no_scientific_or_formal_replay=True)
def csvtext(fields,rows):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);return s.getvalue()
def outputs(r):
 fractions=[];docs=[];raw=[]
 for k,c in r['coordinates'].items():
  fractions.append(dict(coordinate=k,comparison='written',**c['written']));fractions.extend(dict(coordinate=k,comparison=x,**f)for x,f in c['conditional'].items());docs.extend(dict(coordinate=k,document=x,cost=v)for x,v in c['document_costs'].items())
 for f in r['whole_file_inventory']:
  for n,m in f['metrics'].items():
   for u in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']:raw.append(dict(id=f['id'],path=f['file']['path'],role=f['role'],bytes=f['file']['bytes'],sha256=f['file']['sha256'],normalization=n,unit=u,cost=m[u]))
 return {'results.json':json.dumps(r,ensure_ascii=False,indent=2)+'\n','fractions.csv':csvtext(['coordinate','comparison','source_cost','replacement_cost','numerator','denominator','decimal'],fractions),'document_costs.csv':csvtext(['coordinate','document','cost'],docs),'whole_files.csv':csvtext(['id','path','role','bytes','sha256','normalization','unit','cost'],raw),'acquisition.csv':csvtext(list(r['primary_acquisition'][0]),r['primary_acquisition'])}
if __name__=='__main__':
 r=derive(load(R/'protocol.json'),load(R/'inputs/input/author_counts.json'),load(R/'inputs/input/precount/raw_inventory.json')['files'],load(R/'prior/results.json'))
 for f,s in outputs(r).items():(R/f).write_text(s)
 print(json.dumps(dict(primary=r['primary']['written'],conditionals=r['primary']['conditional'],groups={k:(v['files'],v['literal_bytes'])for k,v in r['whole_file_group_costs'].items()})))
