#!/usr/bin/env python3
"""Exact three-source whole-manuscript arithmetic from accepted fixed counts."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import json,hashlib,csv,io
R=Path(__file__).resolve().parent
PROTOCOL='6d01ade4ebea419a10cafa01da2d29570fe7a5d0efd045ae0a5e0a0c6fba99a2'
def need(x,m):
 if not x:raise ValueError('MIX3_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def key(v,n,u):return '/'.join([v,n,u])
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext()as c:c.prec=50;d=format(Decimal(a)/Decimal(b),'.12f')
 return dict(source_cost=a,replacement_cost=b,numerator=f.numerator,denominator=f.denominator,exact_fraction=str(f),decimal=d)
def bound(r,root):
 p=Path(r['path']);need(not p.is_absolute()and'..'not in p.parts,'safe export path');b=(root/p).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'exact '+str(p))
def inputs():
 p=load(R/'protocol.json');need(sha((R/'protocol.json').read_bytes())==PROTOCOL==load(R/'protocol_freeze.json')['protocol']['sha256'],'fixed protocol before evaluation')
 for r in p['input_bindings']:
  bound(r,R);base=(R/r['path']).parent
  for x in load(base/'manifest.json')['exports']:bound(x,base)
 need(load(R/'inputs/input_adoption/adoption.json')['status']=='ROOT_ACCEPTED_THREE_SOURCE_MIXES_MEASUREMENT_INPUTS','distinct input authority')
 n=load(R/'inputs/input/author_counts.json');o=load(R/'inputs/input/retained_counts.json');pol=load(R/'inputs/input/policy.json');rev=load(R/'inputs/input_review/recount.json')
 need(n['retained_accepted_inputs']==o and n['retained_cells_unchanged']and not n['retained_PDFs_reextracted'],'all original input objects unchanged')
 need([n[k]for k in ['new_PDF_cells','new_raw_cells','retained_PDF_cells','retained_raw_cells']]==[120,40,330,130],'exact620 cells')
 need(n['whole_topic_boundary']==pol['whole_topic_boundary']and p['applications']==pol['whole_topic_boundary']['applications'],'complete paid bundles')
 for k,r in n['documents'].items():need(r['metrics']==rev['new_metrics'][k],'independently accepted new full vectors')
 docs={**o['documents'],**n['documents']};raw={g:{**o['raw_files'][g],**n['raw_files'][g]}for g in ['programs','drivers','formal']}
 need(len(docs)==15 and sum(r['pages']for r in docs.values())==114,'full15PDF114physicalpage inventory');need([len(raw[g])for g in raw]==[8,6,3],'whole17files')
 for g in raw:need(set(o['raw_files'][g]).isdisjoint(n['raw_files'][g]),'whole unique files')
 need(p['program_roles']==pol['software_boundary'],'unchanged required/optional/driver/formal identities')
 return p,docs,raw

def derive(p,docs,raw):
 roles=p['program_roles'];req=[r['path']for r in roles['required_full_programs']];opt=[r['path']for r in roles['optional_full_programs']]
 need(len(req)==2 and len(opt)==6 and set(req+opt)==set(raw['programs']),'exact proof vs validation roster')
 roster=[]
 for group,rs in raw.items():
  for path,row in rs.items():
   role=('required_finite_certificate'if path in req else'optional_validation')if group=='programs'else'operational_driver'if group=='drivers'else'partial_formal_evidence'
   roster.append(dict(path=path,group=role,inherited_role=row['role'],bytes=row['bytes'],sha256=row['sha256'],metrics=row['metrics']))
 groups={}
 for g in ['required_finite_certificate','optional_validation','operational_driver','partial_formal_evidence']:
  rows=[r for r in roster if r['group']==g];groups[g]=dict(files=len(rows),literal_bytes=sum(r['bytes']for r in rows),metrics={n:{u:sum(r['metrics'][n][u]for r in rows)for u in p['units']}for n in p['normalizations']})
 coords={}
 for v in p['variants']:
  for n in p['normalizations']:
   for u in p['units']:
    c={k:row['metrics'][v][n][u]for k,row in docs.items()};source=sum(c[k]for k in p['source_ids']);common=sum(c[k]for k in p['common_documents']);app={k:sum(c[j]for j in js)for k,js in p['applications'].items()};den=common+sum(app.values());f=fraction(source,den)
    inv={g:row['metrics'][n][u]for g,row in groups.items()};inv.update(required_printed_alternative=c['REQ'],partial_optional_printed_inventory=c['VAL'],historical_mixed_printed_inventory=c['CODE1']+c['CODE2'],full_optional_printed_representation=None,software_inclusive_factor=None,original_software_cost=None)
    coords[key(v,n,u)]=dict(variant=v,normalization=n,unit=u,document_costs=c,source_sum=source,whole_common=common,application_bundles=app,application_sum=sum(app.values()),whole_written=den,written=f,conditional={k:fraction(c[k],app[k])for k in p['source_ids']},separate_inventory=inv)
 primary=coords[p['primary_coordinate']];stages=[dict(stage=0,label='Acquire all three common papers',sources_acquired=[],replacement_written=primary['whole_common'],source_written=0,whole_common_acquired=True,required_certificates_prepaid=True)]
 ss=0;aa=primary['whole_common']
 for i,k in enumerate(p['source_ids'],1):
  ss+=primary['document_costs'][k];aa+=primary['application_bundles'][k];stages.append(dict(stage=i,label=k,sources_acquired=p['source_ids'][:i],replacement_written=aa,source_written=ss,whole_common_acquired=True,required_certificates_prepaid=True))
 return dict(status='AUTHOR_NUMERICAL_PACKET_PENDING_DISTINCT_REVIEW',topic=p['topic'],source_ids=p['source_ids'],source_count=3,common_documents=p['common_documents'],application_documents=p['applications'],coordinate_count=30,exact_fraction_count=120,primary_coordinate=p['primary_coordinate'],primary=primary,coordinates=coords,complete_document_metric_vectors={k:r['metrics']for k,r in docs.items()},document_pages={k:r['pages']for k,r in docs.items()},source_pages=62,whole_common_pages=13,application_pages={k:sum(docs[j]['pages']for j in js)for k,js in p['applications'].items()},inventory_pages=114,whole_file_inventory=roster,whole_file_group_costs=groups,required_files=req,optional_files=opt,mandatory_nonprogram_data_files=[],historical_printed_inventories=['CODE1','CODE2'],partial_optional_printed_inventory='VAL',required_printed_alternative='REQ',required_printed_coverage={'REQ':['topic_Mix_F005_recovery/check_coprime.g','topic_Mix_L016_recovery/base_certificate.g'],'CODE1':['topic_Mix_F005_recovery/check_coprime.g']},full_required_only_printed_representation='REQ',new_optional_programs_have_printed_representation=False,conditional_prepaid=p['conditional_prepaid'],source_scope=p['source_scope'],source_scope_limits=['Three final F005 problems remain unanswered.','L016 literal thin-only Lemma3.5 is corrected under faithfulness; its ancillary smallest-example/Atlas census and further-cover questions remain outside principal recovery.','F007 page25 chain-class paragraph is not recovered; Problems1/2 remain unanswered. Problem3 has the stated natural reconstruction result and finite connected-flag-graph arbitrary-isomorphism result, with no general infinite/priority claim.'],software_inclusive_factors=None,optional_validation_inclusive_factors=None,historical_source_software_cost=None,unknown_costs=p['unknown_costs'],partial_formal_files=3,partial_formal_declarations=12,full_source_formalized=False,whole_common_paid_once=True,overlap_discount=False,cross_topic_discount=False,required_certificates_not_optional=True,source_and_replacement_programs_excluded=True,new_source_credit=0,new_question_credit=0,new_formal_credit=0,sawtooth_claim=False,node_count_complexity_factor=False,source_cells_unchanged=450,raw_cells_unchanged=170,source_extraction_repeated=False,scientific_programs_reexecuted=False,primary_acquisition=stages,author_role=p['author_role'])

def outputs(r):
 rows=[];docs=[];files=[];acq=[]
 for k,c in r['coordinates'].items():
  for label,f in [('whole_topic',c['written'])]+[(s,c['conditional'][s])for s in r['source_ids']]:rows.append(dict(coordinate=k,comparison=label,**f))
  for d,n in c['document_costs'].items():docs.append(dict(coordinate=k,document=d,cost=n,physical_pages=r['document_pages'][d]))
 for f in r['whole_file_inventory']:
  for n,metrics in f['metrics'].items():
   for u,cost in metrics.items():
    if u!='collapsed_text_sha256':files.append(dict(path=f['path'],role=f['group'],literal_bytes=f['bytes'],sha256=f['sha256'],normalization=n,unit=u,cost=cost))
 for s in r['primary_acquisition']:acq.append(dict(stage=s['stage'],label=s['label'],whole_common_paid=s['whole_common_acquired'],source_written=s['source_written'],replacement_written=s['replacement_written'],required_certificates_prepaid=s['required_certificates_prepaid']))
 out={'results.json':json.dumps(r,ensure_ascii=False,indent=2)+'\n'}
 for name,rr in [('fractions.csv',rows),('document_costs.csv',docs),('whole_files.csv',files),('acquisition.csv',acq)]:
  s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr);out[name]=s.getvalue()
 return out
if __name__=='__main__':
 p,d,r=inputs();j=derive(p,d,r)
 for name,text in outputs(j).items():(R/name).write_text(text)
 print(json.dumps(j['primary'],indent=2))
