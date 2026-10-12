"""Private science-only registration proposal; never modifies the public checkout."""
from pathlib import Path
import argparse, ast, copy, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent
BASE='fb1860a5a3cc1009205d0aac56b5f89f975cc9bd'
AUDIT='audit/science56/v1'
NATIVE='papers/topic-g/extensions/local-primitivity/v1'
SCIENCE='audit/topic-g/extensions/local-primitivity/v1'
PACKETS=[('L102_author','topic_G_L102_recovery',SCIENCE+'/author','132a6e17b80b3bbc82b00da1620a77e5806adde551e80b7a7b78718100cb77ac'),('L102_review','topic_G_L102_root_review',SCIENCE+'/root_review','1a8c03aad8f3217333d4f9be3a7c88694275aac15b2b6a518f0db7a8d8386408')]
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def binding(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(obj if isinstance(obj,str)else json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def title(p):return re.search(r'\\title\{([^{}]+)\}',p.read_text()).group(1)
def main(study,repo):
 need(not(HERE/'manifest.json').exists(),'immutable proposal')
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact baseline')
 W=HERE/'wrappers';files=[];packets=[]
 for key,directory,public,pin in PACKETS:
  p=study/directory; m=load(p/'manifest.json');b=binding(p/'manifest.json',public+'/manifest.json');need(b['sha256']==pin,'accepted manifest')
  packets.append(dict(id=key,study_directory=directory,manifest=b,exports=len(m['exports'])))
  for e in [binding(p/'manifest.json','manifest.json')]+m['exports']:
   logical=e['path'];need(binding(p/logical,logical)==e,'whole frozen file')
   dst=NATIVE+'/'+logical if key=='L102_author'and Path(logical).suffix in ['.tex','.pdf']else public+'/'+logical
   need(not dst.endswith('.md'),'no Markdown route')
   files.append(dict(packet=key,logical_path=logical,study_path=directory+'/'+logical,public_path=dst,bytes=e['bytes'],sha256=e['sha256']))
 need(len(files)==47 and len({r['public_path']for r in files})==47,'complete unique47 files')
 write(HERE/'copy_plan.json',dict(base_commit=BASE,packets=packets,files=files))
 history={}
 historical=['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']
 for name in historical:
  dst=AUDIT+'/previous/'+name;t=W/dst;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes((repo/name).read_bytes());history[name]=binding(t,dst)
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science55 and nested programme53 reader/current routes. Original guards run through a private read-only overlay.'))
 old=load(repo/'audit/corpus/latest.json');oldcat=load(repo/old['active_catalogue']['path'])
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(asts)==137,'137 prior functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','papers/topic-g/latest.json']
 protected=[p for p in protected if(repo/p).is_file()]
 for base in ['audit/overview/v19/packet','audit/topic-g/v2','papers/topic-g/v2','audit/science55/v1']:
  protected.extend(str(p.relative_to(repo))for p in(repo/base).rglob('*')if p.is_file())
 tracked=set(subprocess.check_output(['git','-C',str(repo),'ls-files'],text=True).splitlines())
 protected=sorted(set(protected)&tracked)
 write(HERE/'baseline.json',dict(commit=BASE,old_nonmain_ASTs=asts,protected_files=[binding(repo/p,p)for p in protected],old_catalogue=old['active_catalogue'],history=history,counts=dict(active=106,reviewed=55,measured=53,unmeasured=2,pending=50,editorial=1,archived=55,topics=19)))
 def pub(path):
  if(W/path).is_file():return binding(W/path,path)
  r=next((r for r in files if r['public_path']==path),None)
  return dict(path=path,bytes=r['bytes'],sha256=r['sha256'])if r else binding(repo/path,path)
 def author(name):return next(r['public_path']for r in files if r['packet']=='L102_author'and r['logical_path']==name)
 author_manifest=packets[0]['manifest'];review_manifest=packets[1]['manifest']
 inv=load(study/'topic_G_L102_recovery/program_inventory.json')
 roles=copy.deepcopy(inv)
 roles['whole_files']=[dict(r,public_path=author(r['path']))for r in inv['whole_files']]
 roles.update(original_id='L102',software_inclusive_factor=None,no_cost_evaluation=True,role_sums_not_disjoint_costs=True)
 write(W/(AUDIT+'/whole_file_roles.json'),roles)
 ad=dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE56_GATE',source_id='L102',source_ids=['L102'],principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=author_manifest,distinct_root_review_manifest=review_manifest,root_scientific_acceptance=review_manifest,source_map=pub(author('source_map.json')),scope=pub(author('scope.json')),retained_inputs=pub(author('dependencies.json')),required_program_inventory=pub(AUDIT+'/whole_file_roles.json'),whole_common=[pub(NATIVE+'/local_actions.pdf')],whole_applications=[pub(NATIVE+'/linear_spaces.pdf')],physical_pages=[14,8],source_pages=22,source_routes=35,comparison_topic_created=False,current_G_measurement_changed=False,public_mapping=AUDIT+'/publication_plan/copy_plan.json',publication_gate=AUDIT+'/root_integration.json',roles='rewrite_termination authored L102 science and this publication proposal; root distinctly read/replayed the science. Publication integration review remains separate root work.',scope_note='Complete corrected principal source adjudication with named retained large classifications. Actual acting-group converses, circle exceptions, Hermitian quotient action and WBS local actions are corrected. General affine line-size maximality is proved; Feit bound through10^10 and small G2 roster are complete finite premises. This is not equivalence with all literal source statements.',frozen_status_overlay='Earlier unreviewed/private labels in exact author bytes are historical author-stage wording; distinct root review supplies acceptance without editing those bytes.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap)
 registration=dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['L102'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration'])
 rp=AUDIT+'/new_original_registration.json';write(W/rp,registration)
 summary='Complete corrected local-primitive/locally-two-transitive linear-space classification. Uniform local-action, semilinear spread descent, affine structure rigidity, full WBS and circle analysis, exact acting-group converses and complete Feit finite bound. Large named classifications remain retained premises; literal source corrections are explicit.'
 cat=copy.deepcopy(oldcat)
 cat.update(status='CURRENT_ACCESSIBLE106_56_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=56,currently_measured_originals=53,measurement_pending_original_ids=['L024','L102','N014'],accessible_pending_complete_recovery=49,review_revision='Only L102 changes from mathematical pending to accepted corrected principal recovery; all105 other original records are exact.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=56,measured=53,measurement_pending=3,pending=49,editorial=1))
 row=next(e for e in cat['entries']if e['original_id']=='L102');prior=copy.deepcopy(row['current_principal_recovery'])
 row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=summary,historical_admission_evidence=prior)
 row['principal_results_to_recover'].update(summary=summary,scope_status='COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_ACCEPTED',complete_source_proof_read_in_this_inventory=True,current_full_source_review=review_manifest)
 row['next_obligation']='Prepare a complete symmetric measurement-input boundary and distinct review before evaluating any factor; retain all large classification premises and both required finite programs.'
 row['proposed_theory_or_block']='Topic G local-primitivity scientific extension; measured G boundary unchanged.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured56-catalogue.json';write(W/cp,cat)
 corpus=copy.deepcopy(old)
 corpus.update(status='CURRENT_PROGRAMME_56_CORRECTED_RECOVERIES_53_MEASURED_49_PENDING_1_EDITORIAL',admitted_principal_originals=56,accessible_pending_complete_recovery=49,admitted_original_ids=sorted(old['admitted_original_ids']+['L102']),accessible_pending_original_ids=[x for x in old['accessible_pending_original_ids']if x!='L102'],measurement_pending_original_ids=['L024','L102','N014'],scientific_unmeasured_original_ids=['L024','L102','N014'],previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp))
 corpus['added_admissions'].append(pub(rp));corpus.pop('snapshot',None)
 snap='audit/corpus/updates/accessible106-corrected-unmeasured56.json';write(W/snap,corpus);corpus['snapshot']=pub(snap);write(W/'audit/corpus/latest.json',corpus)
 inputs=[r['public_path']for r in files if r['public_path'].startswith(NATIVE+'/')and r['public_path'].endswith('.tex')]
 docs=[]
 for key,stem,role,pages in [('L102_U','local_actions','common',14),('L102_A','linear_spaces','application',8)]:
  docs.append(dict(id=key,topic='G',comparison_topic_created=False,title=title(study/'topic_G_L102_recovery'/(stem+'.tex')),role=role,source_ids=['L102'],tex=NATIVE+'/'+stem+'.tex',pdf=NATIVE+'/'+stem+'.pdf',tex_inputs=[p for p in inputs if p!=NATIVE+'/'+stem+'.tex'],compiler='xelatex',physical_pages=pages,admission=admission,measured=False,compression_factor=None,build_order=['local_actions','linear_spaces'],externaldocument_dependency='local_actions.aux'if role=='application'else None))
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(docs);sc['original_ids'].append('L102');sc['root_publication_gate']=AUDIT+'/root_integration.json'
 sci='papers/catalogue_corrected_unmeasured.json';write(W/sci,sc)
 pc=load(repo/'papers/latest_catalogue.json');pc['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_THREE_CORRECTED_UNMEASURED';pc['active_source_catalogue']=pub(cp);pc['corrected_unmeasured_scientific_catalogue']=pub(sci);write(W/'papers/latest_catalogue.json',pc)
 write(HERE/'native_catalogue.json',dict(new_documents=docs,build_shared_directory=True,build_order=['local_actions','linear_spaces'],complete_scientific_pages=22))
 text=(repo/'README.rst').read_text();text=text.replace('**55 accessible originals','**56 accessible originals').replace('53 are measured and two (N014 and L024) await measurement.','53 are measured and three (N014, L024 and L102) await measurement.').replace('50 await mathematical recovery;','49 await mathematical recovery;')
 before='Both source editions, complete proof packets and distinct reviews are recorded'
 insertion='The `L102 guide <'+NATIVE+'/PUBLICATION.rst>`_ gives the complete fourteen-page\nlocal-action theory and eight-page linear-space application. Both finite premises\nand all retained classification inputs are explicit; corrected source assertions\nare distinguished from literal theorem-set equivalence.\n\nAll three source editions, complete proof packets and distinct reviews are recorded'
 need(before in text,'README three-guide insertion');text=text.replace(before,insertion).replace('audit/science55/v1/new_original_registration.json',rp).replace('Neither recovery has a compression factor.','None of these three recoveries has a compression factor.').replace("five-original boundary, and L024 creates no comparison topic.","five-original boundary; L102 leaves G's measured boundary unchanged, and L024\ncreates no comparison topic.")
 write(W/'README.rst',text)
 text=(repo/'audit/completion.rst').read_text().replace('**55 reviewed corrected principal recoveries**','**56 reviewed corrected principal recoveries**').replace('53 are measured and two (N014 and L024) are unmeasured. There are 50 originals','53 are measured and three (N014, L024 and L102) are unmeasured. There are 49 originals').replace('N014 and L024 have separate scientific admissions','N014, L024 and L102 have separate scientific admissions').replace('science55/v1/new_original_registration.json','science56/v1/new_original_registration.json');write(W/'audit/completion.rst',text)
 text=(repo/'audit/protocol.tex').read_text().replace('106=55\\ \\text{reviewed corrected recoveries}+50','106=56\\ \\text{reviewed corrected recoveries}+49').replace('Of the 55 corrected recoveries','Of the 56 corrected recoveries').replace('N014 and L024 are scientifically accepted but unmeasured; neither is included','N014, L024 and L102 are scientifically accepted but unmeasured; none is included');write(W/'audit/protocol.tex',text)
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['L102'],counts=dict(active=106,corrected_recoveries=56,measured=53,unmeasured=3,mathematical_pending=49,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(snap),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_comparison_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 print(json.dumps(dict(files=len(files),packets=2,native_pages=[14,8],prior_functions=len(asts))))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();main(a.study,a.repo)
