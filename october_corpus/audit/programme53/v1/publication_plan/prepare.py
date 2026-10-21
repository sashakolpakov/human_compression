#!/usr/bin/env python3
"""Private exact publication mapping; no public writes or scientific execution."""
from pathlib import Path
from copy import deepcopy
import argparse,ast,hashlib,json,re,subprocess
H=Path(__file__).resolve().parent
BASE='53d0fa5e07efab4875fe45c4cf5b0c2ab0b2e457'
SCI='papers/topic-a/extensions/hexagonal/v1';AUD='audit/topic-a/extensions/hexagonal/v1';TOP='audit/topic-a/v5';NUM=TOP+'/measurement';REG='audit/programme53/v1'
SNAP='audit/corpus/updates/accessible106-l003-measured.json';ACTIVE='audit/corpus/accessible106/updates/l003-catalogue.json';CAT='papers/catalogue_hexagonal_measured.json'
def need(v,s):
 if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def rec(p,path=None):
 b=p.read_bytes();return dict(path=str(path if path is not None else p),bytes=len(b),sha256=sha(b))
def write(n,q):
 p=H/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n')
def closure(folder,name):
 found=[]
 def visit(n):
  for x in re.findall(r'\\input\{([^{}]+)\}',(folder/n).read_text()):
   x=x if x.endswith('.tex')else x+'.tex';need('..'not in Path(x).parts and not Path(x).is_absolute(),'safe TeX input')
   if x not in found:found.append(x);visit(x)
 visit(name);return found

def prepare(study,repo):
 need(not(H/'manifest.json').exists(),'preserve freeze');need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE,'fixed baseline')
 corpus=load(repo/'audit/corpus/latest.json');need(corpus['currently_measured_originals']==52 and corpus['accessible_pending_complete_recovery']==53,'programme52 baseline')
 paths=['README.rst','audit/protocol.tex','audit/protocol.pdf','audit/completion.rst','papers/catalogue.json','papers/latest_catalogue.json','papers/topic-a/latest.json','papers/topic-affine/latest.json','audit/corpus/latest.json','audit/overview/latest.json','audit/overview/v18/packet/results.json','scripts/verify_snapshot.py','scripts/build_papers.py',corpus['active_catalogue']['path']]
 paths=[p for p in paths if(repo/p).exists()]
 for n in paths:
  d=H/'baseline'/n;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes((repo/n).read_bytes())
 funcs={n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(len(funcs)==133,'133 prior non-main functions')
 write('baseline.json',dict(commit=BASE,files=[rec(repo/n,n)for n in paths],prior_nonmain_ASTs=funcs))
 pk=[('science','topic_A_L003_complete_assembly',SCI,'36d0f873b3e53ff7ccf09d994efa33b3fe4fe730d5f4c02cbaa66e063ec34e39'),('science_adoption','topic_A_L003_complete_root_review',AUD+'/root_review','f6eec52be2d15b1bab922e38e7018ad8fb18dffc3d3dda7b72e24858de872bf9'),('numbers','topic_A_L003_measurement_results',NUM+'/packet','524b5f73c007e5ba783920859874fe3cb8b5ce7a73d28929b82bf94678e9e31f'),('numeric_review','topic_A_L003_numerical_independent_review',NUM+'/independent_review','2ff490f6744b5edce0307861dbb9d16dec2029efbb4251d80120c405729dfad5'),('numeric_adoption','topic_A_L003_numerical_root_adoption',NUM+'/root_adoption','22c8ee3758140daabe9f01ae3d4701b36340c5b7d293695a76e065549bff3b3c')]
 pk.append(('overview_review','corpus106_overview_v19_root_review','audit/overview/v19/independent_review','066bf2043811e7993d4161ed7e92507df17d4ad0a352a9ee3f8ced11175e55c2'))
 ov=study/'corpus106_overview_v19_candidate/manifest.json'
 if ov.exists():pk.append(('overview','corpus106_overview_v19_candidate','audit/overview/v19/packet',sha(ov.read_bytes())))
 files=[];packets=[]
 for role,origin,dest,pin in pk:
  p=study/origin;m=p/'manifest.json';need(sha(m.read_bytes())==pin,'immutable '+role);data=load(m)
  for r in data['exports']+[rec(m,'manifest.json')]:
   need(rec(p/r['path'],r['path'])==r,'bound payload '+origin+'/'+r['path']);files.append(dict(role=role,study_path=origin+'/'+r['path'],public_path=dest+'/'+r['path'],bytes=r['bytes'],sha256=r['sha256']))
  packets.append(dict(role=role,study_directory=origin,public_directory=dest,manifest_sha256=pin,exports=len(data['exports'])))
 need(len(files)==len({x['public_path']for x in files}),'unique destinations');write('copy_plan.json',dict(packets=packets,files=files,primary_assets_copied=False,numerical_adoption_pending=False))
 catalogue=load(repo/'papers/catalogue.json');allrows={z['id']:z for z in catalogue['papers']+catalogue.get('new_editions',[])};oldids=catalogue['current_topic_editions']['A'];need(len(oldids)==10,'A9 native routes')
 reused={};rows=[]
 for ident in oldids[:9]:
  z=deepcopy(allrows[ident]);z['measurement_admission']=TOP+'/admission.json';rows.append(z)
  for n in [z['tex'],z['pdf']]+z.get('tex_inputs',[]):reused[n]=rec(repo/n,n)
 names=[('inputs/base/shared_supplement','U_HEX','umbrella_addition',14,'xelatex',[]),('inputs/shared_structures/shared_structures','U_STRUCT','umbrella_addition',4,'xelatex',[]),('inputs/base/l121_adapter','A9','application',1,'xelatex',['L121']),('hexagonal_extensions','A10_MAIN','application',7,'xelatex',['L003']),('inputs/finite_structures/structural_completion','A10_STRUCT','application_companion',4,'pdflatex',['L003']),('inputs/correlations/correlation_reduction','A10_CORR','application_companion',4,'pdflatex',['L003']),('inputs/order768/order768','A10_768','application_companion',2,'pdflatex',['L003'])]
 assembly=study/'topic_A_L003_complete_assembly'
 for stem,appid,role,pg,compiler,sids in names:
  f=assembly/(stem+'.tex');title=re.search(r'\\title\{([^{}]+)\}',f.read_text()).group(1);folder=f.parent;rel=Path(stem).parent;ins=[str(rel/n)for n in closure(folder,f.name)]
  rows.append(dict(id='topic-a/extensions/hexagonal/v1/'+appid.lower(),topic='A',application_id=appid,title=title,title_origin='literal accepted TeX title',role=role,source_contracts=sids,tex=SCI+'/'+stem+'.tex',pdf=SCI+'/'+stem+'.pdf',tex_inputs=[SCI+'/'+n for n in ins],compiler=compiler,physical_pages=pg,review_record=REG+'/catalogue_review.json',admission=AUD+'/admission.json',measurement_admission=TOP+'/admission.json',status='CURRENT_ACCEPTED_SCIENTIFIC_BYTES',required_whole_content_inventory=TOP+'/raw_routes.json'))
 need(len(rows)==16 and sum(z['physical_pages']for z in rows)==104,'complete16 native scientific PDFs104pages')
 write('catalogue_additions.json',dict(entries=rows,new_entries=rows[9:],unchanged_native_documents=9,unchanged_pages=68,new_native_documents=7,new_pages=36,total_pages=104,convenience_bundles_not_canonical_or_counted_twice=True,old_L121_complete_paper_historical=True))
 mapping={f['study_path']:f['public_path']for f in files}
 for r in load(assembly/'copy_routes.json'):mapping[r['source']]=SCI+'/'+r['destination']
 inv=load(study/'topic_A_L003_measurement_inputs/precount/raw_inventory.json');occ=[]
 for r in inv['occurrences']:
  z=r.get('current_exact_copy',r)
  if z['root']=='public':public=z['path'];reused[public]=rec(repo/public,public)
  else:
   if z['path'].startswith('topic_A_L121_application/'):
    public=z['path'].replace('topic_A_L121_application/','papers/topic-a/extensions/locally-toroidal/v1/',1);reused[public]=rec(repo/public,public);need(reused[public]['sha256']==z['sha256'],'unchanged L121 raw')
   else:
    need(z['path']in mapping,'unmapped whole raw occurrence '+z['path']);public=mapping[z['path']]
  occ.append(dict(r,public_path=public))
 contents=[]
 for r in inv['contents']:
  content_paths=sorted({o['public_path']for o in occ if o['occurrence_id']in r['occurrence_ids']});contents.append(dict(r,public_paths=content_paths,canonical_public_path=content_paths[0]))
 need(len(occ)==253 and len(contents)==203 and sum(x['mathematical_premise']for x in contents)==99,'all raw content roles')
 write('raw_routes.json',dict(occurrences=occ,contents=contents,occurrence_count=253,whole_content_count=203,required_whole_contents=99,accounting_class_counts=inv['disjoint_content_class_counts'],roles_overlap=True,classes_disjoint=True,software_inclusive_factor=None))
 write('reused_science.json',dict(files=list(reused.values()),native_PDFs=9,native_pages=68,public_copy_requested=False,old_U_and_eight_applications_unchanged=True))
 current=deepcopy(catalogue);existing=set(allrows)
 for z in rows[9:]:need(z['id']not in existing,'new canonical id');current['new_editions'].append(z)
 current['current_topic_editions']['A']=[z['id']for z in rows];write('proposed/papers/catalogue.json',current)
 active=load(repo/corpus['active_catalogue']['path']);nextactive=deepcopy(active)
 for z in nextactive['entries']:
  oid=z['original_id']
  if oid=='L003':
   z['historical_admission_evidence']=deepcopy(z.get('current_principal_recovery'));z['current_principal_recovery']=dict(status='ADMITTED_AND_MEASURED',topic='A',source_dispositions=125,source_table_rows=73,whole_source_formalized=False,latest_admission_references=[AUD+'/admission.json',TOP+'/admission.json'],common_papers=[rows[0]['pdf'],rows[9]['pdf'],rows[10]['pdf']],application_bundle=[x['pdf']for x in rows if x['application_id'].startswith('A10')],required_whole_content_inventory=TOP+'/raw_routes.json',corrected_not_literal_contract=True,new_question_credit=0)
   z['principal_results_to_recover']['summary']='Complete corrected principal contract accepted: literal universal marked presentations/local periods, all73 table rows with exact structural dispositions, correlation reductions and isolated order768/genus4 case. Printed order/local-word/nonsplitting corrections and experimental diagram5 geometry remain explicit.'
   z['principal_results_to_recover']['scope_status']='COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_ACCEPTED';z['next_obligation']='No pending principal recovery obligation. Preserve all125 dispositions, exact source corrections, retained inputs and unproved experimental/question claims. Measurement charges all common3/native application4 papers.'
  elif oid in ['L032','L034','F016','F013','L035','N009','L128','L012','L121']:
   z['current_measurement_extension']={'topic_admission':TOP+'/admission.json','whole_common_pages':[23,14,4],'current_A10_numeric_packet':NUM+'/packet/results.json','source_credit_unchanged':True}
   if oid=='L121':z['current_measurement_extension'].update(application=SCI+'/inputs/base/l121_adapter.pdf',application_pages=1,moved_proofs_fully_paid=SCI+'/inputs/base/shared_supplement.pdf')
 nextactive.update(status='PROPOSED_ACCESSIBLE106_PROGRAMME53',admitted_principal_originals=53,accessible_pending_complete_recovery=52,current_recovery_counts=dict(active=106,admitted=53,pending=52,editorial=1));write('proposed/audit/corpus/active_catalogue.json',nextactive)
 nxt=deepcopy(corpus);nxt.update(status='PROPOSED_PROGRAMME_53_MEASURED_52_MATHEMATICAL_PENDING_1_EDITORIAL',admitted_principal_originals=53,currently_measured_originals=53,accessible_pending_complete_recovery=52,accessible_pending_original_ids=sorted(set(corpus['accessible_pending_original_ids'])-{'L003'}))
 for key in ['admitted_original_ids','measured_original_ids']:nxt[key]=sorted(corpus[key]+['L003'])
 write('proposed/audit/corpus/next.json',nxt)
 latest=load(repo/'papers/latest_catalogue.json');nl=deepcopy(latest);nl['entries'].extend(rows[9:]);nl['original_ids']=sorted(set(nl['original_ids'])|{'L003'});nl['new_principal_originals']+=1;nl['status']='PROPOSED_CURRENT_MANUSCRIPT_CATALOGUE_53';write('proposed/papers/latest_catalogue.json',nl)
 history={n:rec(repo/n,REG+'/previous/'+n)for n in paths if not n.startswith('scripts/')and n!='audit/overview/v18/packet/results.json'}
 write('history_routes.json',dict(routes=history,baseline_commit=BASE,purpose='Exact previous current pointers/docs for unchanged legacy guards; no broad exclusions.'))
 write('integration_requirements.json',dict(root_only_public_writer=True,base_commit=BASE,paths=dict(science=SCI,science_audit=AUD,topic=TOP,numbers=NUM,programme=REG,snapshot=SNAP,active_catalogue=ACTIVE,current_papers=CAT,overview='audit/overview/v19'),new_original_registration=dict(path=REG+'/new_original_registration.json',source_ids=['L003'],add_to=['added_admissions','added_measurements']),full_topic_replacement=dict(path=TOP+'/admission.json',source_ids=['L032','L034','F016','F013','L035','N009','L128','L012','L121','L003'],add_only_to='current_topic_replacements'),partition=dict(active=106,measured=53,mathematical_pending=52,editorial=1,archived=55,topics=19),old_nonmain_functions=133,overview=dict(fractions=72,bars_per_format=163,unchanged_other_topics=18,unchanged_individuals=51,changed_conditional='L121',new_conditional='L003'),numerical_adoption_pending=False,whole_source_root_accepted=True,no_L044_or_L096_credit=True,public_mutations=False))
 return dict(payload_files=len(files),packets=len(packets),reused_files=len(reused),native_scientific_PDFs=16,native_pages=104,whole_raw_contents=203,raw_occurrences=253)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();print(json.dumps(prepare(a.study_root,a.repo),indent=2))
