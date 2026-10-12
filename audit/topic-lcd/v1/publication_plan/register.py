#!/usr/bin/env python3
"""Generate an additive programme50 draft in a fresh private directory.

Actual root-created admissions are required unless --proposed-admissions is
explicitly selected. That mode copies clearly labelled admission templates and
never purports to supply root acceptance. Neither mode writes to the repository.
"""
import argparse,copy,hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE='audit/programme50/v1/'
SCI='audit/topic-lcd/v1/admission.json';NUM='audit/topic-lcd/v1/measurement/admission.json'
ACTIVE='audit/corpus/accessible106/updates/lcd-catalogue.json';SNAP='audit/corpus/updates/accessible106-lcd-measured.json'
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def pin(root,rel):
 p=root/rel;b=p.read_bytes();return dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(root,rel,x):
 p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n');return pin(root,rel)
def register(pub,payload,out,proposed=False):
 need(not out.exists()and out.resolve()!=pub.resolve()and pub.resolve()not in out.resolve().parents,'fresh private output only');out.mkdir(parents=True)
 baseline=read(HERE/'public_baseline.json')
 for x in baseline['files']:
  if x['path']=='scripts/verify_snapshot.py':continue # new root functions may have been appended; stage.py checks prior ASTs.
  need(pin(pub,x['path'])==x,'unchanged baseline '+x['path'])
 for key,f in [('previous_corpus_pointer','audit/corpus/latest.json'),('previous_catalogue','papers/latest_catalogue.json'),('previous_full_catalogue','papers/catalogue.json'),('previous_overview_pointer','audit/overview/latest.json')]:
  dest=out/(BASE+key+'.json');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pub/f,dest)
 shutil.copy2(pub/'README.rst',out/(BASE+'previous_README.rst'))
 for path,template in [(SCI,'admission_template.json'),(NUM,'measurement_admission_template.json')]:
  src=HERE/template if proposed else payload/path;need(src.is_file(),'root admission exists: '+str(src));d=read(src)
  need(d['source_ids']==['L050','F017'],'exact source admission')
  need(proposed or d['status'].startswith(('ROOT_ADMITTED','ROOT_ACCEPTED')),'actual root admission status')
  dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
 admissions=[pin(out,SCI),pin(out,NUM)]
 rows=copy.deepcopy(read(HERE/'catalogue_rows.json')['entries'])
 for x in rows:
  x['status']='PROPOSED_CURRENT_EDITION'if proposed else'ROOT_ADMITTED_CURRENT_EDITION';x['measurement_status']='proposed_registration'if proposed else'admitted';x['catalogue_role']='current'
 def payloadpin(rel):return pin(payload,rel)
 pointer=dict(status='PROPOSED_CURRENT_LCD_EDITION'if proposed else'CURRENT_ACCEPTED_PRINCIPAL_CONTRACTS_AND_MANUSCRIPT_MEASUREMENT',edition='v1',source_ids=['L050','F017'],admission=admissions[0],measurement_admission=admissions[1],measurement=payloadpin('audit/topic-lcd/v1/measurement/packet/results.json'),reader=payloadpin('audit/topic-lcd/v1/measurement/packet/reader.pdf'),catalogue_entries=rows,full_common_paid_once=True,no_sibling_application_dependency=True,unique_partial_Lean_declarations=9,full_source_formalized=False,software_inclusive_factor=None)
 ptr=save(out,'papers/topic-lcd/latest.json',pointer)
 reg=dict(status='PROPOSED_L050_F017_REGISTRATION_FOR_ROOT_REVIEW'if proposed else'ROOT_ADMITTED_L050_F017_CORRECTED_PRINCIPAL_CONTRACTS_WITH_MEASUREMENT',source_ids=['L050','F017'],principal_originals_added=2,new_intake_originals=0,new_question_credit=0,new_formal_credit=0,source_retrieval_in_scope=False,current_admissions=admissions,source_dispositions=dict(L050=54,F017=104),scope='Complete corrected principal contracts and exact ancillary dispositions. Retained mathematical inputs and unresolved source questions remain explicit; L121 is not registered.',measurement_boundary='Full U14+A_L05015+A_F01712. Concrete software excluded symmetrically; 83 required contents remain acquired mathematical premises. All102 whole contents/127 occurrences disclosed separately; software-inclusive and pooled factors null.')
 regpin=save(out,BASE+'new_original_registration.json',reg)
 old=read(pub/'audit/corpus/latest.json');before=read(pub/old['active_catalogue']['path']);after=copy.deepcopy(before)
 targets={'L050':'l050','F017':'f017'}
 for row in after['entries']:
  sid=row['original_id']
  if sid not in targets:continue
  d=row['current_principal_recovery'];d.update(status='ADMITTED_AND_MEASURED',latest_admission_references=admissions,current_contract_admissions=admissions,current_topic_edition=ptr,current_common_routes=['papers/topic-lcd/v1/common/umbrella.pdf'],current_application_routes=['papers/topic-lcd/v1/'+targets[sid]+'/application.pdf'],whole_source_formalized=False)
  d['scope']=('Complete corrected L050 Theorem1(a–d), tables and module bridges; exact54 dispositions. Classical graph/group/code-table inputs retained; full253 graph uniqueness and the other15-dimensional constructions remain unresolved.'if sid=='L050'else'Complete corrected F017 principal contract and104 dispositions, including shared scalar counts, ranks, SRG/Paley and odd-graph bridges; specified distance/spectrum/classification inputs retained and general further-family/decoding questions unclaimed.')
  row['next_obligation']='Recovered and measured in the accepted LCD edition; unresolved questions and retained external costs are not represented as solved or zero.'
  row['proposed_theory_or_block']='LCD: shared incidence, projection and graph-code theory'
 after.update(status='PROPOSED_ACCESSIBLE106_CATALOGUE_AFTER_LCD'if proposed else'CURRENT_ACCESSIBLE106_CATALOGUE_AFTER_LCD',admitted_principal_originals=50,accessible_pending_complete_recovery=56,recovery_snapshot=admissions[0],review_revision='Two existing originals L050/F017; all104 other current records byte-equivalent as JSON objects.',previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=50,pending=56),new_proof_credit=2)
 # Preserve exact established top-level count-key spelling as well.
 for k in ['admitted_principal_original_count','admitted_originals','admitted_count']:
  if k in after:after[k]=50
 for k in ['pending_originals','pending_count']:
  if k in after:after[k]=56
 active=save(out,ACTIVE,after)
 cur=copy.deepcopy(old);cur.pop('snapshot',None);cur.update(status='CURRENT_PROGRAMME_50_ADMITTED_OF_106_ACTIVE_ORIGINALS',admitted_principal_originals=50,currently_measured_originals=50,accessible_pending_complete_recovery=56,previous_snapshot=old['snapshot'],active_catalogue=active)
 for k in ['admitted_original_ids','measured_original_ids']:cur[k]=sorted(cur[k]+['L050','F017'])
 cur['accessible_pending_original_ids']=[x for x in cur['accessible_pending_original_ids']if x not in targets]
 for k in ['added_admissions','added_measurements']:cur[k]=old[k]+[regpin]
 cur['current_topic_replacements']=old['current_topic_replacements']+admissions
 snap=save(out,SNAP,cur);cur['snapshot']=snap;current=save(out,'audit/corpus/latest.json',cur)
 cat=read(pub/'papers/latest_catalogue.json');cat['previous_catalogue']=pin(out,BASE+'previous_catalogue.json');cat['entries']+=rows;cat['original_ids']=sorted(cat['original_ids']+['L050','F017']);cat['new_principal_originals']+=2;cat['active_source_catalogue']=active;cat['LCD_current_edition']=ptr
 save(out,'papers/catalogue_lcd_measured.json',cat);catpin=save(out,'papers/latest_catalogue.json',cat)
 full=read(pub/'papers/catalogue.json');full['new_editions']+=rows;full['current_topic_editions']['LCD']=[x['id']for x in rows];save(out,'papers/catalogue.json',full)
 report=dict(status='PROPOSED_PROGRAMME50_REGISTRATION_AWAITING_ROOT_PUBLICATION_REVIEW',proposal_uses_admission_templates=proposed,current_corpus=current,current_catalogue=catpin,active_original_catalogue=active,current_snapshot=snap,original_registration=regpin,scientific_and_numerical_admissions=admissions,added_current_catalogue_ids=[x['id']for x in rows],updated_current_catalogue_ids=[],changed_originals=['L050','F017'],new_originals=['L050','F017'],baseline_commit=baseline['public_head'],expected_partition=dict(recovered=50,pending=56,active=106,archived=55,topics=19))
 save(out,BASE+'registration_report.json',report);return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--payload-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--proposed-admissions',action='store_true');a=p.parse_args();print(json.dumps(register(a.public_root,a.payload_root,a.out,a.proposed_admissions),indent=2))
