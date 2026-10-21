"""Private science71 registration and documents; never write the public repo."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,os,re,subprocess
P=Path(__file__).resolve().parent
BASE='6e34d0505b8eb10b5ef9111ee94b5f9af81e80a2';AUD='audit/science71/v1';SCI='audit/recoveries/F002/v1';NAT='papers/recoveries/F002/v1'
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(v if isinstance(v,str)else json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def main(a):
 need(not(P/'manifest.json').exists(),'immutable proposal');repo=a.repo;W=P/'wrappers'
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact science70 baseline')
 old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(70,53,35),'old partition')
 plan=load(P/'copy_plan.json');author=plan['author_directory'];review=plan['independent_review_directory'];adoption=plan['root_review_directory'];routes={r['study_path']:r for r in plan['files']}
 def logical(n):
  r=routes[n];return dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
 def pub(n):
  if(W/n).is_file():return pin(W/n,n)
  r=next((x for x in plan['files']if x['public_path']==n),None)
  return dict(path=n,bytes=r['bytes'],sha256=r['sha256'])if r else pin(repo/n,n)
 history={}
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']:
  q=W/(AUD+'/previous/'+n);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes((repo/n).read_bytes());history[n]=pin(q,AUD+'/previous/'+n)
 write(W/(AUD+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science70 pointers and nested historical validation through programme53.'))
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(len(asts)==167,'167 prior non-main functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science70/v1/root_integration.json']+[str(x.relative_to(repo))for x in(repo/'audit/overview/v19/packet').rglob('*')if x.is_file()]
 write(P/'baseline.json',dict(commit=BASE,old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n)for n in protected]))
 inv=load(a.study/author/'program_inventory.json');roles=copy.deepcopy(inv)
 roles.update(public_bindings=[logical(author+'/'+r['path'])for r in inv['whole_files']],required_programs=[logical(author+'/'+n)for n in ['enumerate_even.g','checks.g','compare.g']],required_mathematical_data=[logical(author+'/'+n)for n in ['source_markings.g','generated_markings.g']],operational_drivers=[logical(author+'/'+n)for n in ['check.py','run.py']],retained_closure_binding=logical(author+'/retained_projective.json'),retained_public_files=plan['public_dependencies'],external_proof_cost=None,measurement=None,current_source_code_boundary='No new software-inclusive factor. Complete enumeration and literal comparison code/data are proof premises; the two drivers are operational. All older required and optional roles remain in the full acquired projective closure. Historical source software and full external proof costs remain unknown.')
 write(W/(AUD+'/whole_file_roles.json'),roles)
 native=[]
 for name,role in [('marked_search','whole common search theory'),('degree_eleven','whole application')]:
  title=re.search(r'\\title\{([^{}]+)\}',(a.study/author/(name+'.tex')).read_text()).group(1)
  native.append(dict(id='F002_'+name,title=title,tex=logical(author+'/'+name+'.tex')['path'],pdf=logical(author+'/'+name+'.pdf')['path'],tex_inputs=[],compiler='pdflatex',physical_pages=2,role=role,source_ids=['F002'],topic='Finite marked subgroups',comparison_topic_created=False,measured=False,compression_factor=None,existing_public_dependency=False))
 note='Complete principal F002 Theorem8.8: ranks four and five of every even transitive degree-eleven group give only the rank-four self-dual eleven-cell. Full ambient enumeration requires no transitive-group classification. The five literal Proposition8.4 graphs and ten suffix-orbit cells are recovered. All40 named statements are disposed; independent ancillary graph lemmas and the52tuple appendix are not separately recovered. The full previously accepted projective common/application and program closure is acquired for geometric identification. No literal theorem-set equivalence, factor, comparison topic, question answer or new Lean claim.'
 admission=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE71_GATE',source_id='F002',source_ids=['F002'],source_authors=['Maria Elisa Fernandes','Claudio Alexandre Piedade','Olivia Reade'],principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=logical(author+'/manifest.json'),distinct_review_manifest=logical(review+'/manifest.json'),root_scientific_acceptance=logical(adoption+'/manifest.json'),source_map=logical(author+'/source_map.json'),source_contract=logical(author+'/scope.json'),dependency_boundary=logical(author+'/retained_projective.json'),program_roles=pub(AUD+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(x['pdf'])for x in native],physical_pages=[2,2],retained_acquisition_files=380,retained_common=pub('papers/topic-e/v3/umbrella.pdf'),retained_application=pub('papers/topic-e/v3/psl-polytopes.pdf'),source_pages=28,source_routes=40,source_graph_rows=5,source_orbit_cells=10,finite_premises=roles['required_programs'],required_mathematical_data=roles['required_mathematical_data'],comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUD+'/root_integration.json',public_mapping=AUD+'/publication_plan/copy_plan.json',scope_note=note,roles='Root authored the new proofs and code. Enumeration_volume distinctly reviewed them, supplied descriptive source dispositions, and previously authored parts of the inherited projective theory. That older theory retains its separate distinct/root acceptance. Root then adopted the complete current review. This publication mapping is operational, not an additional scientific review.',frozen_status_overlay='The exact author pending-review status remains historical; later distinct review and root adoption provide current acceptance.')
 ap=SCI+'/admission.json';write(W/ap,admission);ad=pub(ap);rp=AUD+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['F002'],admissions=[ad],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['F002']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
 cat.update(status='CURRENT_ACCESSIBLE106_71_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=71,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=34,review_revision='Only F002 becomes an accepted principal recovery; all105 other original records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=71,measured=53,measurement_pending=18,pending=34,editorial=1))
 row=next(r for r in cat['entries']if r['original_id']=='F002');previous=copy.deepcopy(row['current_principal_recovery'])
 row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[ad],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous)
 row['next_obligation']='Any future measurement acquires both whole new papers and the complete projective dependency closure. Complete required finite code/data and operational drivers remain separate; source software and external proof costs are unknown. No factor currently exists.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured71-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_71_CORRECTED_RECOVERIES_53_MEASURED_34_PENDING_1_EDITORIAL',admitted_principal_originals=71,accessible_pending_complete_recovery=34,admitted_original_ids=sorted(old['admitted_original_ids']+['F002']),accessible_pending_original_ids=[x for x in old['accessible_pending_original_ids']if x!='F002'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured71.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 for d in native:d['admission']=ad
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('F002');sc['root_publication_gate']=AUD+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_EIGHTEEN_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(P/'native_catalogue.json',dict(new_acquisition_entries=native,new_scientific_pages=4,new_native_documents=2,retained_whole_acquisition_files=380,retained_common=admission['retained_common'],retained_application=admission['retained_application'],compiler='pdflatex',all_whole_papers_paid=True))
 summary='''F002 recovers the unique rank-four or rank-five polytope for even transitive
degree-eleven groups: the self-dual eleven-cell. Both complete new papers
(2+2 pages), the full acquired projective identification, and the required
finite census and literal comparison data remain available. Five source
graphs and ten orbit entries are checked. Auxiliary graph lemmas and the
52-tuple appendix are not separately recovered; all forty named statements
have explicit dispositions. No factor, question answer or new Lean claim.

'''
 for name in ['README.rst','audit/completion.rst','audit/protocol.tex']:
  t=(repo/name).read_text().replace('12 October 2026','13 October 2026')
  t=t.replace('70 accessible originals','71 accessible originals').replace('70 reviewed corrected principal recoveries','71 reviewed corrected principal recoveries').replace('53 are measured and seventeen','53 are measured and eighteen').replace('L018 and N011','L018, N011 and F002').replace('35 await mathematical recovery','34 await mathematical recovery').replace('There are 35 originals','There are 34 originals').replace('All seventeen source editions','All eighteen source editions').replace('None of these seventeen recoveries','None of these eighteen recoveries').replace('science70/v1/new_original_registration.json','science71/v1/new_original_registration.json').replace('106=70\\ \\text{reviewed corrected recoveries}+35','106=71\\ \\text{reviewed corrected recoveries}+34').replace('Of the 70 corrected recoveries','Of the 71 corrected recoveries')
  if name=='README.rst':t=t.replace('All eighteen source editions','The `F002 guide <papers/recoveries/F002/v1/PUBLICATION.rst>`_ gives the following recovery.\n\n'+summary+'All eighteen source editions',1)
  elif name=='audit/completion.rst':t=t.replace('The `current overview',summary+'The `current overview',1)
  else:t=t.replace('The accepted overview v19',summary+'The accepted overview v19',1)
  write(W/name,t)
 guide='''F002: even transitive markings on eleven points
===============================================

The principal result is Theorem 8.8 of Fernandes, Piedade and Reade's bound
twenty-eight-page edition. A complete search over all even involutions in A11
proves that the only rank-four or rank-five transitive C-marking is the abstract
self-dual eleven-cell. Point conjugacy and abstract marked-group isomorphism
are distinguished. The five literal source graphs and ten suffix-orbit entries
are also recovered.

Read both whole new papers and acquire the existing projective theory below.
The coverage proof establishes the exact append-IP and prefix-orbit invariants;
the application uses the entire finite execution. The search is a proof
premise, not optional validation. All 132 transitive tuples receive full subset
IP checks. The external group-polytope correspondence, end-intersection
criterion and exact GAP algorithms remain explicit inputs.

The forty-statement source map distinguishes the main classification from
ancillary proof-route statements and the 52-tuple appendix, which are not
separately recovered. This is not literal theorem-set equivalence. There is no
new factor, comparison topic, conjecture answer or Lean claim. Root authored
the new proofs/code; enumeration_volume distinctly reviewed them while
disclosing earlier projective authorship and source-disposition assistance.
Older projective acceptances remain separate and are not self-adjudicated.

'''
 for d in native:guide+='* `'+d['title']+' <'+os.path.relpath(d['pdf'],NAT)+'>`_ (two pages).\n'
 for label,n in [('Full retained projective common theory','papers/topic-e/v3/umbrella.pdf'),('Full retained PSL polytope application','papers/topic-e/v3/psl-polytopes.pdf'),('Exact admission',ap),('Source dispositions',SCI+'/author/source_map.json'),('Complete acquired dependency inventory',SCI+'/author/retained_projective.json'),('Whole program and data roles',AUD+'/whole_file_roles.json')]:guide+='* `'+label+' <'+os.path.relpath(n,NAT)+'>`_.\n'
 guide+='\nThe remaining older projective papers, programs, data and acceptances stay\nacquired through all 380 exact public bindings. Public replay reconstructs the\nentire frozen packet without private files. Source software and full external\nproof costs are unknown; no software-inclusive scalar is supplied.\n';write(W/(NAT+'/PUBLICATION.rst'),guide)
 write(W/'scripts/check_science71_history.py',(P/'history_wrapper.py').read_text());write(W/'scripts/check_science71.py',"from pathlib import Path\nimport importlib.util\ndef verify(root):\n root=Path(root).resolve()\n spec=importlib.util.spec_from_file_location('science71_plan',root/'audit/science71/v1/publication_plan/check.py')\n module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\n return module.verify(root,require_root=True)\n")
 write(P/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['F002'],counts=dict(active=106,corrected_recoveries=71,measured=53,unmeasured=18,mathematical_pending=34,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=ad,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUD+'/root_integration.json'))
 write(P/'acceptance_binding.json',dict(author_manifest=logical(author+'/manifest.json'),distinct_review_manifest=logical(review+'/manifest.json'),root_adoption_manifest=logical(adoption+'/manifest.json'),separate_roles=True))
 write(P/'documentation.diff',''.join(''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']))
 print('prepared',len(plan['files']),'logical routes;167 old functions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
