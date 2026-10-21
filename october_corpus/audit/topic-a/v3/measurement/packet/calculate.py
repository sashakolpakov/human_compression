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
def derive(proto,counts,inventory):
 order=proto['source_order'];apps=proto['applications'];roles={r['id']:r for r in inventory};raw=[]
 for rid,item in counts['raw_files_measured'].items():
  rule=roles[rid];need(item['file']==rule['file']and item['role']==rule['role'],'whole raw identity/role');raw.append(dict(**rule,metrics=item['metrics']))
 groups={role:dict(files=sum(r['role']==role for r in raw),literal_bytes=sum(r['file']['bytes']for r in raw if r['role']==role),metrics={n:{u:sum(r['metrics'][n][u]for r in raw if r['role']==role)for u in proto['units']}for n in proto['normalizations']})for role in dict.fromkeys(r['role']for r in raw)}
 coords={}
 for v in proto['variants']:
  for n in proto['normalizations']:
   for u in proto['units']:
    d={x:z['metrics'][v][n][u]for x,z in counts['documents'].items()};s=sum(d[x]for x in order);a=sum(d[apps[x]]for x in order);whole=d['U']+a
    coords[key(v,n,u)]=dict(variant=v,normalization=n,unit=u,document_costs=d,source_sum=s,whole_common=d['U'],application_sum=a,whole_written=whole,written=fraction(s,whole),conditional={x:fraction(d[x],d[apps[x]])for x in order},separate_software=dict(printed_appendices={x:d[x]for x in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']},printed_sum=sum(d[x]for x in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']),raw_group_costs={g:r['metrics'][n][u]for g,r in groups.items()},software_inclusive_factor=None,historical_source_software_cost=None))
 pk=key(*[proto['primary'][k]for k in ['variant','normalization','unit']]);primary=coords[pk];stages=[dict(stage=0,acquired='whole U',source_written=0,replacement_written=primary['whole_common'],required_program_data_and_external_premises_separate=True)]
 s=0;a=primary['whole_common']
 for i,x in enumerate(order,1):s+=primary['document_costs'][x];a+=primary['document_costs'][apps[x]];stages.append(dict(stage=i,acquired=apps[x]+' for '+x,source_written=s,replacement_written=a,required_program_data_and_external_premises_separate=True))
 return dict(status='AUTHOR_UNIFIED_A_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',title=proto['title'],source_ids=order,applications=apps,source_count=8,source_pages=119,whole_common_pages=23,application_pages={x:counts['documents'][apps[x]]['pages']for x in order},printed_appendix_pages={x:counts['documents'][x]['pages']for x in ['CODE_A','CODE_AFFINE','CODE_DIAGRAM']},primary_coordinate=pk,coordinate_count=30,exact_fraction_count=270,coordinates=coords,primary=primary,whole_file_inventory=raw,whole_file_group_costs=groups,primary_acquisition=stages,software_inclusive_factors=None,optional_validation_inclusive_factors=None,historical_source_software_cost=None,full_formalization_cost=None,unknown_costs=proto['unknown_costs'],cross_topic_discount=False,new_source_credit=0,new_question_credit=0,new_formal_credit=0,no_extraction=True,no_scientific_or_formal_replay=True)
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
 r=derive(load(R/'protocol.json'),load(R/'inputs/input/author_counts.json'),load(R/'inputs/input/raw_inventory.json'))
 for f,s in outputs(r).items():(R/f).write_text(s)
 print(json.dumps(dict(primary=r['primary']['written'],conditionals=r['primary']['conditional'],groups={k:(v['files'],v['literal_bytes'])for k,v in r['whole_file_group_costs'].items()})))
