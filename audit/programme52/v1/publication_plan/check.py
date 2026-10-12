#!/usr/bin/env python3
"""Bounded exact-copy/registration review; no scientific, font, GAP or Lean replay."""
from pathlib import Path
from copy import deepcopy
import argparse,ast,json,hashlib
from prepare import H,SCI,AUD,TOP,NUM,REG,SNAP,ACTIVE,PAPERS,BASE,load,need,sha

def bind(p,z):
 b=p.read_bytes();need(len(b)==z['bytes']and sha(b)==z['sha256'],'exact '+str(p))
def semantic(corpus,active,cat,latest,pointer,reg,raw,oldcorpus,oldactive,oldcat,oldlatest,rows):
 need((corpus['currently_measured_originals'],corpus['accessible_pending_complete_recovery'],corpus['editorial_originals'],corpus['archived_unavailable_originals'])==(52,53,1,55),'52/53/1/55 partition')
 need(corpus['editorial_original_ids']==['L022']and corpus['editorial_factor']is None and corpus['source_retrieval_in_scope']is False,'editorial/archive policy')
 for key in ['admitted_original_ids','measured_original_ids']:need(set(corpus[key])==set(oldcorpus[key])|{'L047'}and len(corpus[key])==52,'only new measured L047')
 need(set(corpus['accessible_pending_original_ids'])==set(oldcorpus['accessible_pending_original_ids'])-{'L047'},'only L047 removed from pending')
 need(reg['source_ids']==reg['admitted_source_ids']==reg['measured_source_ids']==['L047'],'new registration must exclude five old sources')
 for key in ['added_measurements','added_admissions']:need(corpus[key][:-1]==oldcorpus[key]and corpus[key][-1]['path']==REG+'/new_original_registration.json','single registration appended')
 need(corpus['current_topic_replacements'][:-1]==oldcorpus['current_topic_replacements']and corpus['current_topic_replacements'][-1]['path']==TOP+'/admission.json','full B admission only topic replacement')
 before={r['original_id']:r for r in oldactive['entries']};after={r['original_id']:r for r in active['entries']};need(set(before)==set(after)and [k for k in before if before[k]!=after[k]]==['L047'],'105 unrelated original objects unchanged')
 new=after['L047']['current_principal_recovery'];need(new['status']=='ADMITTED_AND_MEASURED'and new['source_dispositions']==58 and new['ancillary_reports_not_regenerated']==23 and not new['whole_source_formalized'],'literal corrected contract and scope')
 need(cat['papers']==oldcat['papers']and cat['new_editions'][:len(oldcat['new_editions'])]==oldcat['new_editions'],'all historical catalogue rows preserved')
 need(cat['new_editions'][len(oldcat['new_editions']):]==rows and cat['current_topic_editions']['B']==[r['id']for r in rows],'all eight actual current B science routes')
 need({k:v for k,v in cat['current_topic_editions'].items()if k!='B'}=={k:v for k,v in oldcat['current_topic_editions'].items()if k!='B'},'other current science untouched')
 need(latest['entries'][:len(oldlatest['entries'])]==oldlatest['entries']and latest['entries'][len(oldlatest['entries']):]==rows,'all prior current catalogue entries unchanged')
 need(set(latest['original_ids'])==set(oldlatest['original_ids'])|{'L047'},'single source identity in paper metadata')
 need(pointer['originals']==['N001','N003','N008','L030','L040','L047']and len(pointer['common_papers'])==2 and len(pointer['applications'])==6,'whole common and six apps')
 need(pointer['whole_written_expansion']and pointer['software_inclusive_factor']is None,'expansion and symmetry')
 need([raw[k]for k in ['required_or_auxiliary','optional','operational','partial_formal_files','partial_declarations','new_declarations']]==[8,2,5,2,14,0],'whole file roles')
 need(len(raw['files'])==len({z['file']['sha256']for z in raw['files']})==17,'17 unique contents')
 need(next(z for z in raw['files']if z['id']=='NEW_PROGRAM_6')['mathematical_premise'],'run.g is required roster')
 need([r['physical_pages']for r in rows]==[16,3,4,4,5,11,10,3]and sum(r['physical_pages']for r in rows)==56,'full56 scientific pages')
 need(all(r['compiler']=='xelatex'and r['review_record']==REG+'/catalogue_review.json'for r in rows),'literal compiler/review routes')

def verify(study,repo,mapped=None):
 if(H/'manifest.json').exists():
  for z in load(H/'manifest.json')['exports']:bind(H/z['path'],z)
 base=load(H/'baseline.json');need(base['commit']==BASE,'exact baseline')
 for z in base['files']:bind(H/'baseline'/z['path'],z)
 asts={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(base['prior_nonmain_ASTs'])==130 and all(asts.get(k)==v for k,v in base['prior_nonmain_ASTs'].items()),'all130 old non-main ASTs preserved')
 plan=load(H/'copy_plan.json');need(not plan['numerical_root_adoption_pending'],'adopted arithmetic')
 for z in plan['files']:bind((mapped/z['public_path'])if mapped else(study/z['study_path']),z)
 for z in load(H/'reused_science.json')['files']:bind(repo/z['path'],z)
 target=mapped or H/'wrappers'
 if not mapped:
  for z in load(H/'wrapper_routes.json')['files']:bind(H/z['proposal_path'],z)
 rows=load(H/'catalogue_additions.json')['entries'];raw=load(H/'raw_roles.json');new=[load(target/n)for n in ['audit/corpus/latest.json',ACTIVE,'papers/catalogue.json','papers/latest_catalogue.json','papers/topic-b/latest.json',REG+'/new_original_registration.json']];oldcorpus=load(H/'baseline/audit/corpus/latest.json');oldactive=load(H/'baseline'/oldcorpus['active_catalogue']['path']);oldcat=load(H/'baseline/papers/catalogue.json');oldlatest=load(H/'baseline/papers/latest_catalogue.json')
 semantic(*new,raw,oldcorpus,oldactive,oldcat,oldlatest,rows)
 review=load(target/REG/'catalogue_review.json');need(review['status']=='PASS','canonical legacy schema');expected={n for row in rows for n in [row['tex'],row['pdf']]+row['tex_inputs']};need(expected=={z['path']for z in review['artifacts']},'all36 derived science artifact bindings')
 for z in review['artifacts']:
  if mapped:bind(mapped/z['path'],z)
  else:
   entry=next((q for q in plan['files']if q['public_path']==z['path']),None);bind(study/entry['study_path']if entry else repo/z['path'],z)
 controls=[]
 mutations=[('register old originals twice',5,lambda q:q.update(source_ids=['N001','L047'])),('wrong52 count',0,lambda q:q.update(currently_measured_originals=51)),('editorial factor zero',0,lambda q:q.update(editorial_factor=0)),('reuse missing common for free',4,lambda q:q['common_papers'].pop()),('drop sixth application',4,lambda q:q['applications'].pop()),('software factor invented',4,lambda q:q.update(software_inclusive_factor=1)),('principal scope enlarged',1,lambda q:next(r for r in q['entries']if r['original_id']=='L047')['current_principal_recovery'].update(ancillary_reports_not_regenerated=0)),('measured filter inconsistent',1,lambda q:next(r for r in q['entries']if r['original_id']=='L047')['current_principal_recovery'].update(status='ROOT_SCIENCE_ONLY')),('historical catalogue row changed',2,lambda q:q['new_editions'][0].update(title='changed')),('wrongcurrentBscope',2,lambda q:q['current_topic_editions']['B'].pop()),('old current row changed',3,lambda q:q['entries'][0].update(title='changed')),('claim compression',4,lambda q:q.update(whole_written_expansion=False))]
 for label,i,fn in mutations:
  q=deepcopy(new);fn(q[i])
  try:semantic(*q,raw,oldcorpus,oldactive,oldcat,oldlatest,rows)
  except(ValueError,KeyError,TypeError):controls.append(label)
  else:raise ValueError('accepted mutation '+label)
 return dict(status='PASS_BOUNDED_PRIVATE_PUBLICATION_PROPOSAL'if not mapped else'PASS_MAPPED_PUBLIC_PAYLOAD_AND_REGISTRATION',payload_files=len(plan['files']),packets=len(plan['packets']),reused_files=len(load(H/'reused_science.json')['files']),science_routes=8,science_pages=56,derived_catalogue_bindings=36,measured=52,mathematical_pending=53,editorial=1,archived=55,other_active_records_unchanged=105,old_nonmain_ASTs=130,controls=controls,no_source_extraction_or_scientific_replay=True,root_public_writer_only=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--mapped-public-root',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh report');q=verify(a.study_root,a.repo,a.mapped_public_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
