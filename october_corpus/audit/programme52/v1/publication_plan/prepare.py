#!/usr/bin/env python3
"""Prepare exact B6 routes and bounded registration metadata privately."""
from pathlib import Path
from copy import deepcopy
import argparse,ast,hashlib,json,re,subprocess
H=Path(__file__).resolve().parent
SCI='papers/topic-b/extensions/transitive-rank/v1';AUD='audit/topic-b/extensions/transitive-rank/v1';TOP='audit/topic-b/v4';NUM=TOP+'/measurement';REG='audit/programme52/v1';SNAP='audit/corpus/updates/accessible106-l047-measured.json';ACTIVE='audit/corpus/accessible106/updates/l047-catalogue.json';PAPERS='papers/catalogue_transitive_rank_measured.json'
BASE='e28e103708e186d2db463de792ee33b6dc07e01b'
def need(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def rec(p,path=None):
 b=p.read_bytes();return dict(path=str(path if path is not None else p),bytes=len(b),sha256=sha(b))
def write(n,q):
 p=H/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n')
def texclosure(folder,name):
 found=[]
 def walk(n):
  for x in re.findall(r'\\input\{([^{}]+)\}',(folder/n).read_text()):
   x=x if x.endswith('.tex')else x+'.tex'
   need('..'not in Path(x).parts and not Path(x).is_absolute(),'safe TeX input')
   if x not in found:found.append(x);walk(x)
 walk(name);return found

def prepare(study,repo):
 need(not(H/'manifest.json').exists(),'preserve frozen proposal')
 need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE,'fixed documentation baseline')
 corpus=load(repo/'audit/corpus/latest.json');need(corpus['currently_measured_originals']==51 and corpus['accessible_pending_complete_recovery']==54,'programme51 baseline')
 paths=['papers/catalogue.json','papers/latest_catalogue.json','papers/topic-b/latest.json','audit/corpus/latest.json','audit/overview/latest.json','audit/overview/v17/packet/results.json','README.rst','audit/protocol.tex','audit/protocol.pdf','audit/completion.rst','scripts/verify_snapshot.py','scripts/build_papers.py',corpus['active_catalogue']['path'],'scripts/check_current_documentation.py','audit/documentation/v1/admission.json']
 for name in paths:
  dst=H/'baseline'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((repo/name).read_bytes())
 funcs={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(funcs)==130,'all130 baseline functions')
 write('baseline.json',dict(commit=BASE,files=[rec(repo/n,n)for n in paths],prior_nonmain_ASTs=funcs))
 packets=[('science','topic_B_L047_candidate_v2',SCI,'e3a0d89b44034eff597d604e1b7b3b01a2ea5e33a2d25af8640e76cf765b5623'),('scientific_review','topic_B_L047_independent_review',AUD+'/scientific_review','abdaea3184da3d09f91f66fb95e17c584748c85f3a9a42a48bdef15bff32c46e'),('scientific_adoption','topic_B_L047_root_adoption',AUD+'/root_adoption','4b140c70be7ca5f61c9e400233ef187a76a18a6e834eb798485cac0b2a4034d8'),('numbers','topic_B_L047_measurement_results',NUM+'/packet','eaa3f62b0cea99890ed73f2816212423cde2a48dec43a8aaca756b4d6e7a9118')]
 packets.append(('overview_author','corpus106_overview_v18_candidate_v2','audit/overview/v18/packet','7a4d46b0bc00aa2a84a4cc76f5668ac677124caa8e8a0a1a149bce3073efa5fe'))
 if(H/'numerical_acceptance.json').exists():
  packets.extend((x['role'],x['study_directory'],x['public_directory'],x['manifest_sha256'])for x in load(H/'numerical_acceptance.json')['packets'])
 routes=[];prs=[]
 for role,d,dest,pin in packets:
  root=study/d;m=root/'manifest.json';need(sha(m.read_bytes())==pin,'frozen '+role);mm=load(m)
  for z in mm['exports']+[rec(m,'manifest.json')]:
   b=(root/z['path']).read_bytes();need(len(b)==z['bytes']and sha(b)==z['sha256'],'export '+d+'/'+z['path']);routes.append(dict(role=role,study_path=d+'/'+z['path'],public_path=dest+'/'+z['path'],bytes=z['bytes'],sha256=z['sha256']))
  prs.append(dict(role=role,study_directory=d,public_directory=dest,manifest_sha256=pin,exports=len(mm['exports'])))
 need(len(routes)==len({z['public_path']for z in routes}),'unique destinations')
 write('copy_plan.json',dict(packets=prs,files=routes,primary_assets_copied=False,numerical_root_adoption_pending=not(H/'numerical_acceptance.json').exists()))
 stems=['umbrella','inductively-minimal-geometries','maximal-symmetric-markings','frattini-coordinate-geometries','disjoint-subset-geometries','high-rank-symmetric-markings'];oids=['','N001','N003','N008','L030','L040'];pages=[16,3,4,4,5,11];rows=[];reused={}
 for stem,oid,pg in zip(stems,oids,pages):
  root=repo/'papers/topic-b/v3';name=stem+'.tex';title=re.search(r'\\title\{([^{}]*)\}',(root/name).read_text()).group(1);ins=texclosure(root,name)
  row=dict(id='topic-b/v3/'+stem,topic='B',title=title,title_origin='literal accepted TeX',role='application'if oid else'umbrella',application_id='B'+str(oids.index(oid))if oid else'U_B',source_contracts=[oid]if oid else[],tex='papers/topic-b/v3/'+name,pdf='papers/topic-b/v3/'+stem+'.pdf',tex_inputs=['papers/topic-b/v3/'+n for n in ins],compiler='xelatex',physical_pages=pg,review_record=REG+'/catalogue_review.json',admission='audit/topic-b/v3/admission.json',measurement_admission=TOP+'/admission.json',status='CURRENT_ACCEPTED_SCIENTIFIC_BYTES')
  rows.append(row)
  for f in [row['tex'],row['pdf']]+row['tex_inputs']:reused[f]=rec(repo/f,f)
 for stem,role,appid,pg in [('string_rank_theory','umbrella_addition','U_B6',10),('transitive_string_groups','application','B6',3)]:
  root=study/'topic_B_L047_candidate_v2';title=re.search(r'\\title\{([^{}]*)\}',(root/(stem+'.tex')).read_text()).group(1)
  rows.append(dict(id='topic-b/extensions/transitive-rank/v1/'+stem.replace('_','-'),topic='B',title=title,title_origin='literal accepted TeX',role=role,application_id=appid,source_contracts=['L047']if appid=='B6'else[],tex=SCI+'/'+stem+'.tex',pdf=SCI+'/'+stem+'.pdf',tex_inputs=[SCI+'/'+n for n in texclosure(root,stem+'.tex')],compiler='xelatex',physical_pages=pg,review_record=REG+'/catalogue_review.json',admission=AUD+'/admission.json',measurement_admission=TOP+'/admission.json',status='CURRENT_ACCEPTED_SCIENTIFIC_BYTES'))
 need(len(rows)==8 and sum(x['physical_pages']for x in rows)==56,'full8 scientific documents56pages')
 write('catalogue_additions.json',dict(entries=rows,old_canonical_B_v2_rows_preserved=True,old_v3_scientific_bytes_unchanged=True,printed_programs_separate=[dict(pdf='papers/topic-b/v3/program-appendix.pdf',pages=7),dict(pdf=SCI+'/program-appendix.pdf',pages=7)]))
 r=load(study/'topic_B_L047_measurement_results/results.json');raw=[]
 for z in r['whole_file_inventory']:
  f=z['file'];name=f['path'].replace('topic_B_L047_candidate_v2/',SCI+'/');q=dict(z,public_path=name);raw.append(q)
  if name.startswith('papers/topic-b/v3/'):
   need(rec(repo/name,name)['sha256']==f['sha256'],'unchanged old raw');reused[name]=rec(repo/name,name)
 for n in ['program-appendix.pdf','program-appendix.tex','scope.json','manifest.json']:
  path='papers/topic-b/v3/'+n;reused[path]=rec(repo/path,path)
 write('raw_roles.json',dict(files=raw,required_or_auxiliary=8,optional=2,operational=5,partial_formal_files=2,partial_declarations=14,new_declarations=0,software_inclusive_factor=None,external_software=SCI+'/external_software.json',archival_review_tools=r['archival_audit_tools'],replicas_in_retained_common_not_double_counted=True))
 write('reused_science.json',dict(files=list(reused.values()),scientific_PDFs=6,scientific_pages=43,old_common_pages=16,old_application_pages=27,public_copy_requested=False))
 cat=load(repo/'papers/catalogue.json');cc=deepcopy(cat);existing={z['id']for z in cat['papers']+cat.get('new_editions',[])}
 for row in rows:need(row['id']not in existing,'new canonical current route');cc['new_editions'].append(row)
 cc['current_topic_editions']['B']=[z['id']for z in rows];write('proposed/papers/catalogue.json',cc)
 current=deepcopy(corpus);pending=set(corpus['accessible_pending_original_ids']);need('L047'in pending,'one new original')
 current.update(status='PROPOSED_PROGRAMME_52_MEASURED_53_MATHEMATICAL_PENDING_1_EDITORIAL',admitted_principal_originals=52,currently_measured_originals=52,accessible_pending_complete_recovery=53,accessible_pending_original_ids=sorted(pending-{'L047'}))
 for key in ['admitted_original_ids','measured_original_ids']:current[key]=sorted(corpus[key]+['L047'])
 current['publication_pending']=True;current['pending_root_routes']=[AUD+'/admission.json',TOP+'/admission.json',REG+'/new_original_registration.json'];write('proposed/audit/corpus/next.json',current)
 active=load(repo/corpus['active_catalogue']['path']);nextactive=deepcopy(active)
 for z in nextactive['entries']:
  if z['original_id']=='L047':
   z['historical_admission_evidence']=deepcopy(z.get('current_principal_recovery'));z['current_principal_recovery']=dict(status='ADMITTED_AND_MEASURED',topic='B',source_dispositions=58,whole_source_formalized=False,latest_admission_references=[AUD+'/admission.json',TOP+'/admission.json'],common_papers=['papers/topic-b/v3/umbrella.pdf',SCI+'/string_rank_theory.pdf'],application=SCI+'/transitive_string_groups.pdf',required_programs=8,optional_validation=2,source_corrections=['Table1 order36 type [3,2,3]','Ordered versus unordered wreath markings and global duality distinguished','Parent rank and maximal parabolic rank kept separate'],ancillary_reports_not_regenerated=23,new_question_credit=0)
   z['principal_results_to_recover']['summary']='Accepted corrected principal transitive string-C-group rank bound, sharp imprimitive equality classification, complete primitive exception list and alternating-parabolic corollaries. Exact58-row disposition map retained;23 finer ancillary Table3 reports remain attributed, not regenerated.'
   z['principal_results_to_recover']['scope_status']='COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_ACCEPTED';z['next_obligation']='No further principal-contract recovery obligation; preserve the23 attributed ancillary reports, all external premises and exact source corrections. Current full written comparison is an expansion.'
 nextactive.update(status='PROPOSED_ACCESSIBLE106_PROGRAMME52',admitted_principal_originals=52,accessible_pending_complete_recovery=53,current_recovery_counts=dict(active=106,admitted=52,pending=53,editorial=1));write('proposed/audit/corpus/active_catalogue.json',nextactive)
 latest=load(repo/'papers/latest_catalogue.json');newlatest=deepcopy(latest);newlatest['entries'].extend(rows);newlatest['original_ids']=sorted(set(latest['original_ids'])|{'L047'});newlatest['new_principal_originals']=latest['new_principal_originals']+1;newlatest['status']='PROPOSED_CURRENT_MANUSCRIPT_CATALOGUE_52';newlatest['unified_B_current_edition']=dict(proposed_pointer='papers/topic-b/latest.json',prior_pointer=latest['unified_B_current_edition']);write('proposed/papers/latest_catalogue.json',newlatest)
 history={}
 for name in ['README.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/catalogue.json','papers/latest_catalogue.json','papers/topic-b/latest.json','audit/overview/latest.json']:
  dest=REG+'/previous/'+name;history[name]=rec(repo/name,dest)
 write('history_routes.json',dict(routes=history,baseline_commit=BASE,purpose='Run unchanged programme51 and current documentation guards against the exact previous current documents and pointers. Preserve all130 old non-main ASTs. No broad path exemptions.'))
 write('integration_requirements.json',dict(root_only_public_writer=True,new_original_registration=dict(path=REG+'/new_original_registration.json',source_ids=['L047'],add_to=['added_admissions','added_measurements']),full_topic_replacement=dict(path=TOP+'/admission.json',source_ids=r['source_ids'],add_only_to='current_topic_replacements'),source_and_factor_credit_separate=True,paths=dict(science=SCI,science_audit=AUD,numbers=NUM,topic=TOP,programme=REG,snapshot=SNAP,active_catalogue=ACTIVE,current_papers=PAPERS,overview='audit/overview/v18'),partition=dict(active=106,measured=52,mathematical_pending=53,editorial=1,archived=55,topics=19),old_scientific_frozen_files_unchanged=True,old_nonmain_functions=130,new_catalogue_review='PASS plus artifacts derived solely from already accepted exact science bindings; metadata compatibility, not new mathematical adjudication',overview_preservation=dict(other_whole_topics=18,old_individuals=51,new_conditional='L047',new_whole='B',expected_fractions=71,expected_graph_rectangles=161),pending_numerical_adoption=not(H/'numerical_acceptance.json').exists()))
 write('state.json',dict(status='PRIVATE_PREPARATION',base_commit=BASE,exact_payload_routes=len(routes),packet_count=len(prs),reused_public_files=len(reused),scientific_documents=8,scientific_pages=56,numerical_adoption_pending=not(H/'numerical_acceptance.json').exists(),public_mutations=False))
 return load(H/'state.json')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();print(json.dumps(prepare(a.study_root,a.repo),indent=2))
