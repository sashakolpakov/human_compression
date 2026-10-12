#!/usr/bin/env python3
"""Additive registration guard; old snapshot functions remain unchanged."""
import argparse,copy,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
BASE='audit/programme50/v1/'
def need(x,m):
 if not x:raise ValueError('PROGRAMME50: '+m)
def objects(old,cur,before,after,oldcat,cat,prior,full,reg,report):
 ids=set(old['admitted_original_ids'])|{'L050','F017'}
 need(len(ids)==50 and 'L121'not in ids,'two exact additional originals')
 need(cur['status']=='CURRENT_PROGRAMME_50_ADMITTED_OF_106_ACTIVE_ORIGINALS','current status')
 for k in ['admitted_original_ids','measured_original_ids']:need(len(cur[k])==len(set(cur[k]))==50 and set(cur[k])==ids,'50 unique originals')
 need(cur['active_original_ids']==old['active_original_ids']and len(cur['active_original_ids'])==106 and cur['archived_original_ids']==old['archived_original_ids']and len(cur['archived_original_ids'])==55,'active/archive unchanged')
 need(cur['admitted_principal_originals']==cur['currently_measured_originals']==50 and cur['accessible_pending_complete_recovery']==len(cur['accessible_pending_original_ids'])==56 and set(cur['accessible_pending_original_ids'])==set(cur['active_original_ids'])-ids,'50/56 partition')
 need(cur['retrieval_original_ids']==[]and cur['pending_source_retrieval']==0 and not cur['source_retrieval_in_scope']and not cur['all_original_proofs_recovered']and not cur['all_conjectures_resolved'],'pending obligations retained')
 need(reg['source_ids']==['L050','F017']and reg['principal_originals_added']==2 and reg['new_intake_originals']==reg['new_question_credit']==reg['new_formal_credit']==0,'exact original registration')
 a={x['original_id']:x for x in before['entries']};b={x['original_id']:x for x in after['entries']}
 need(set(a)==set(b)and len(b)==106 and {k for k in a if a[k]!=b[k]}=={'L050','F017'},'104 unchanged original records')
 need(after['admitted_principal_originals']==50 and after['accessible_pending_complete_recovery']==56 and after['current_recovery_counts']==dict(active=106,admitted=50,pending=56),'catalogue partition')
 for sid,row in b.items():
  need(row['source_access']==a[sid]['source_access']and row['historical_proof_status']==a[sid]['historical_proof_status'],'source/prior evidence unchanged')
  need((row['current_principal_recovery']['status']=='ADMITTED_AND_MEASURED')==(sid in ids),'exact recovery status')
  if sid in {'L050','F017'}:
   x=row['current_principal_recovery'];need(x['historical_admission_evidence']==a[sid]['current_principal_recovery']['historical_admission_evidence']and x['current_contract_admissions']==report['scientific_and_numerical_admissions'],'history and current admission')
   need(x['current_common_routes']==['papers/topic-lcd/v1/common/umbrella.pdf']and x['current_application_routes']==['papers/topic-lcd/v1/'+('l050'if sid=='L050'else'f017')+'/application.pdf']and x['whole_source_formalized']is False,'complete local routing')
 for k in ['added_admissions','added_measurements']:need(cur[k]==old[k]+[report['original_registration']],'prior registrations unchanged')
 need(cur['current_topic_replacements']==old['current_topic_replacements']+report['scientific_and_numerical_admissions'],'additive topic boundary')
 need(cat['entries'][:-3]==oldcat['entries']and len(cat['entries'])==len(oldcat['entries'])+3 and cat['original_ids']==sorted(oldcat['original_ids']+['L050','F017']),'unchanged prior catalogue and3 additions')
 rows=cat['entries'][-3:];need([x['id']for x in rows]==report['added_current_catalogue_ids']and report['updated_current_catalogue_ids']==[],'exact added routes')
 need([x['physical_pages']for x in rows]==[14,15,12]and[x['compiler']for x in rows]==['pdflatex','pdflatex','xelatex'],'entire authoritative papers/compiler')
 need(full['papers']==prior['papers']and full['new_editions']==prior['new_editions']+rows and full['current_topic_editions']==dict(prior['current_topic_editions'],LCD=[x['id']for x in rows]),'old build catalogue unchanged')
 return dict(status='PASS_PROGRAMME50',active=106,recovered=50,pending=56,archived=55,new_originals=['L050','F017'],unchanged_originals=104,unchanged_catalogue_rows=len(oldcat['entries']),added_paper_rows=3,scientific_pages=41,new_question_credit=0)
def verify(root,base=None,payload=None,allow_proposed=False):
 def path(rel):
  p=Path(rel);need(not p.is_absolute()and '..'not in p.parts,'safe route')
  for folder in [root,payload,base]:
   if folder is not None and(folder/p).is_file():return folder/p
  raise ValueError('missing route '+rel)
 def read(rel):return json.loads(path(rel).read_text())
 def bind(e):
  b=path(e['path']).read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'binding '+e['path'])
 report=read(BASE+'registration_report.json');need(allow_proposed or not report['proposal_uses_admission_templates'],'real root admissions required')
 for k in ['current_corpus','current_catalogue','active_original_catalogue','current_snapshot','original_registration']:bind(report[k])
 for e in report['scientific_and_numerical_admissions']:
  bind(e);d=read(e['path']);need(allow_proposed or d['status'].startswith(('ROOT_ADMITTED','ROOT_ACCEPTED')),'root admission')
 old=read(BASE+'previous_corpus_pointer.json');cur=read('audit/corpus/latest.json');reg=read(report['original_registration']['path']);oldcat=read(BASE+'previous_catalogue.json');cat=read('papers/latest_catalogue.json');before=read(old['active_catalogue']['path']);after=read(cur['active_catalogue']['path']);prior=read(BASE+'previous_full_catalogue.json');full=read('papers/catalogue.json')
 for k in ['snapshot','base_inventory','previous_snapshot','active_catalogue','scope_admission','scope_archive']:bind(cur[k])
 need({k:v for k,v in cur.items()if k!='snapshot'}==read(cur['snapshot']['path']),'exact snapshot')
 r=objects(old,cur,before,after,oldcat,cat,prior,full,reg,report)
 measured=[]
 for e in cur['added_measurements']:bind(e);measured+=read(e['path'])['source_ids']
 need(len(measured)==len(set(measured))and not set(measured)&set(cur['historical_admitted_ids'])and set(measured)|set(cur['historical_admitted_ids'])==set(cur['admitted_original_ids']),'no duplicate measurement credit')
 pointer=read('papers/topic-lcd/latest.json');need(pointer['catalogue_entries']==cat['entries'][-3:]and pointer['full_common_paid_once']and pointer['no_sibling_application_dependency']and not pointer['full_source_formalized']and pointer['unique_partial_Lean_declarations']==9 and pointer['software_inclusive_factor']is None,'complete LCD interface')
 for k in ['admission','measurement','reader','measurement_admission']:bind(pointer[k])
 for row in cat['entries'][-3:]:
  need(re.search(r'\\title\{([^}]+)\}',path(row['tex']).read_text()).group(1)==row['title'],'literal title');need(len(PdfReader(path(row['pdf'])).pages)==row['physical_pages'],'full page extent')
  for p in row['tex_inputs']:need(path(p).is_file(),'full TeX inputs')
 need(cat==read('papers/catalogue_lcd_measured.json'),'current manuscript pointer')
 r['proposed_admissions']=report['proposal_uses_admission_templates'];return r,(old,cur,before,after,oldcat,cat,prior,full,reg,report)
def controls(args):
 tests=[]
 edits=[('omit L050 admission',lambda a:a[1]['admitted_original_ids'].remove('L050')),('add L121',lambda a:a[1]['admitted_original_ids'].append('L121')),('free common',lambda a:a[5]['entries'][-3].update(physical_pages=0)),('substitute compiler',lambda a:a[5]['entries'][-3].update(compiler='xelatex')),('change prior original',lambda a:a[3]['entries'][0].update(title='changed')),('erase prior registration',lambda a:a[1]['added_admissions'].pop(0)),('claim full formalization',lambda a:next(x for x in a[3]['entries']if x['original_id']=='L050')['current_principal_recovery'].update(whole_source_formalized=True)),('claim question',lambda a:a[8].update(new_question_credit=1)),('wrong pending count',lambda a:a[1].update(accessible_pending_complete_recovery=55)),('alter old paper',lambda a:a[7]['papers'].pop())]
 for name,f in edits:
  a=copy.deepcopy(args);f(a)
  try:objects(*a)
  except(ValueError,KeyError,IndexError):tests.append(name)
  else:raise ValueError('accepted mutation '+name)
 return tests
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base-repo',type=Path);p.add_argument('--payload-root',type=Path);p.add_argument('--allow-proposed',action='store_true');p.add_argument('--out',type=Path);a=p.parse_args();r,args=verify(a.repo,a.base_repo,a.payload_root,a.allow_proposed);r['controls']=controls(args);s=json.dumps(r,indent=2)+'\n';print(s)
 if a.out:a.out.write_text(s)
