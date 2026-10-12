#!/usr/bin/env python3
"""Single additional original, complete routes, exact unchanged historical records."""
import argparse,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader

def need(x,m):
 if not x:raise ValueError('PROGRAMME48: '+m)
def verify(root):
 def read(p):return json.loads((root/p).read_text())
 def bind(e):
  p=Path(e['path']);need(not p.is_absolute()and '..'not in p.parts,'unsafe binding');b=(root/p).read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'binding '+str(p))
 base='audit/programme48/v1/';report=read(base+'registration_report.json');old=read(base+'previous_corpus_pointer.json');cur=read('audit/corpus/latest.json');ids=set(old['admitted_original_ids'])|{'L126'}
 for k in ['current_corpus','current_catalogue','active_original_catalogue','current_snapshot','original_registration']:bind(report[k])
 for e in report['scientific_and_numerical_admissions']:bind(e)
 need(cur['status']=='CURRENT_PROGRAMME_48_ADMITTED_OF_106_ACTIVE_ORIGINALS'and len(old['admitted_original_ids'])==47 and 'L126'not in old['admitted_original_ids'],'48 status')
 for k in ['admitted_original_ids','measured_original_ids']:need(len(cur[k])==len(set(cur[k]))==48 and set(cur[k])==ids,'unique originals')
 need(cur['admitted_principal_originals']==cur['currently_measured_originals']==48 and cur['active_original_ids']==old['active_original_ids']and len(cur['active_original_ids'])==106 and cur['archived_original_ids']==old['archived_original_ids']and len(cur['archived_original_ids'])==55,'active catalogue boundary')
 need(cur['accessible_pending_complete_recovery']==len(cur['accessible_pending_original_ids'])==58 and set(cur['accessible_pending_original_ids'])==set(cur['active_original_ids'])-ids and cur['retrieval_original_ids']==[]and cur['pending_source_retrieval']==0 and cur['measurement_pending_original_ids']==[]and not cur['source_retrieval_in_scope']and not cur['all_original_proofs_recovered']and not cur['all_conjectures_resolved'],'pending work preserved')
 for k in ['snapshot','base_inventory','previous_snapshot','active_catalogue','scope_admission','scope_archive']:bind(cur[k])
 need({k:v for k,v in cur.items()if k!='snapshot'}==read(cur['snapshot']['path']),'immutable current snapshot')
 for k in ['added_admissions','added_measurements']:need(cur[k]==old[k]+[report['original_registration']],'historical registrations changed')
 need(cur['current_topic_replacements']==old['current_topic_replacements']+report['scientific_and_numerical_admissions'],'topic replacement')
 for k in ['added_admissions','added_measurements','access_additions','current_topic_replacements']:
  for e in cur[k]:bind(e)
 reg=read(report['original_registration']['path']);need(reg['source_ids']==['L126']and reg['principal_originals_added']==1 and reg['new_intake_originals']==reg['new_question_credit']==reg['new_formal_credit']==0,'only one admitted original')
 measured=[s for e in cur['added_measurements']for s in read(e['path'])['source_ids']];need(len(measured)==len(set(measured))and not set(measured)&set(cur['historical_admitted_ids'])and set(measured)|set(cur['historical_admitted_ids'])==ids,'no duplicate measurement credit')
 before={x['original_id']:x for x in read(old['active_catalogue']['path'])['entries']};after={x['original_id']:x for x in read(cur['active_catalogue']['path'])['entries']};need(len(after)==106 and set(after)==set(before)and {k for k in before if before[k]!=after[k]}=={'F010','L126'},'104 exact unchanged original records')
 for sid,row in after.items():
  now=row['current_principal_recovery'];need(row['active']and row['original_count']==1 and row['source_access']==before[sid]['source_access']and row['historical_proof_status']==before[sid]['historical_proof_status']and(now['status']=='ADMITTED_AND_MEASURED')==(sid in ids),'source/status '+sid)
  if sid in ['F010','L126']:
   need(now['historical_admission_evidence']==before[sid]['current_principal_recovery']['historical_admission_evidence']and now['current_contract_admissions']==report['scientific_and_numerical_admissions'],'prior evidence/current admission')
   need(now['current_application_routes']==['papers/topic-representation/v3/packet/volume/'+('finite-normal-pairs'if sid=='F010'else'representations-by-incidence')+'.pdf']and now['current_common_routes']==['papers/topic-representation/v3/packet/volume/umbrella.pdf'],'current manuscript route');bind(now['current_topic_edition'])
 oldcat=read(base+'previous_catalogue.json');cat=read('papers/latest_catalogue.json');need(cat==read('papers/catalogue_representation_measured.json')and len(cat['entries'])==84 and cat['entries'][:80]==oldcat['entries']and cat['original_ids']==sorted(oldcat['original_ids']+['L126'])and cat['new_principal_originals']==21 and cat['active_source_catalogue']==cur['active_catalogue'],'whole current catalogue')
 rows=cat['entries'][80:];need([x['id']for x in rows]==report['added_current_catalogue_ids']and report['updated_current_catalogue_ids']==[],'four additional paper rows')
 for row in rows:
  title=re.search(r'\\title\{([^}]+)\}',(root/row['tex']).read_text());need(title and row['title']==title.group(1)and len(PdfReader(root/row['pdf']).pages)==row['physical_pages'],'literal title/full PDF')
  for path in row['tex_inputs']:need((root/path).is_file(),'all TeX dependencies')
 pointer=read('papers/topic-representation/latest.json');need(pointer['source_ids']==['F010','L126']and pointer['catalogue_entries']==rows and pointer['no_sibling_application_dependency']and pointer['full_common_paid_once'],'current Representation pointer')
 for k in ['admission','measurement','reader','measurement_admission']:bind(pointer[k])
 full=read('papers/catalogue.json');prior=read(base+'previous_full_catalogue.json');need(full['papers']==prior['papers']and full['new_editions']==prior['new_editions']+rows[:3]and full['current_topic_editions']==dict(prior['current_topic_editions'],Representation=[r['id']for r in rows[:3]]),'append-only build catalogue')
 return dict(status='PASS_PROGRAMME48',active=106,recovered=48,pending=58,archived=55,new_originals=['L126'],unchanged_originals=104,unchanged_catalogue_rows=80,added_paper_rows=4,new_question_credit=0)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);print(json.dumps(verify(p.parse_args().repo),indent=2))
