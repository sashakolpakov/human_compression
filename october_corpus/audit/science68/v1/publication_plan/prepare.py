"""Prepare science68 wrappers privately; root alone installs and publishes."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent;AUDIT='audit/science68/v1';SCIENCE='audit/recoveries/L017/v1';NATIVE='papers/recoveries/L017/v1';AUTHOR='corpus106_L017_recovery';BASE='dadda0f7ba433acfcad821d529586d278fc3d2f2'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str)else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 need(not(HERE/'manifest.json').exists(),'frozen proposal');repo=a.repo;W=HERE/'wrappers'
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact baseline')
 old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(67,53,38),'science67 partition')
 plan=load(HERE/'copy_plan.json');REVIEW=plan['root_review_directory'];routes={r['study_path']:r for r in plan['files']}
 def logical(n):
  r=routes[n];return dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
 def pub(n):
  if(W/n).is_file():return pin(W/n,n)
  r=next((x for x in plan['files']if x['public_path']==n),None)
  return dict(path=n,bytes=r['bytes'],sha256=r['sha256'])if r else pin(repo/n,n)
 history={}
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']:
  dest=AUDIT+'/previous/'+n;p=W/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/n).read_bytes());history[n]=pin(p,dest)
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science67 pointers and nested historical validation through programme53.'))
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(len(asts)==161,'161 existing non-main functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science67/v1/root_integration.json']+[str(p.relative_to(repo))for p in(repo/'audit/overview/v19/packet').rglob('*')if p.is_file()]
 write(HERE/'baseline.json',dict(commit=BASE,origin_main_at_preparation=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip(),old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n)for n in protected]))
 inv=load(a.study/AUTHOR/'program_inventory.json');raw=copy.deepcopy(inv)
 raw['public_bindings']=[logical(AUTHOR+'/'+x['path'])for x in inv['current_required_raw_files_and_data']+[inv['current_operational_driver']]+inv['optional_new_validation']+inv['recomputable_record_bindings']]
 raw.update(source_software_cost=None,external_proof_cost=None,measurement=None,current_source_code_boundary='The complete 17-page source has no supplied executable listing; its Magma implementation is unknown. Two current exact programs and literal permutation data are required finite premises. Optional validation and operational files are whole and distinct. No software-inclusive factor.')
 write(W/(AUDIT+'/whole_file_roles.json'),raw)
 native=[]
 for d in load(a.study/AUTHOR/'native.json'):
  t=(a.study/AUTHOR/d['tex']).read_text();native.append(dict(id='L017_'+Path(d['tex']).stem,title=re.search(r'\\title\{([^{}]+)\}',t).group(1),tex=logical(AUTHOR+'/'+d['tex'])['path'],pdf=logical(AUTHOR+'/'+d['pdf'])['path'],tex_inputs=[],compiler='pdflatex',physical_pages=d['pages'],role='whole scientific proof component',source_ids=['L017'],topic='Absolute flags and moving lines',comparison_topic_created=False,measured=False,compression_factor=None,existing_public_dependency=routes[AUTHOR+'/'+d['pdf']]['transport']=='EXISTING_PUBLIC'))
 note='Complete corrected principal L017 recovery: all 53 dispositions, 13 named results and seven examples across the full 17-page source. Classical moving parameters/distances, characteristic-two completion and the fixed absolute are proved with explicit retained inputs. The q=4 moving graph differs from its fixed–moving union; the claimed q=7 84-vertex quartic graph is excluded by complete marking exhaustion, and the actual 168-vertex graph has full automorphism order 2^28*336. The symmetric-centralizer algorithm is replaced. Both entire earlier L023 proofs are paid. No theorem-set equivalence, new question, Lean, comparison topic or factor is claimed.'
 ad=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE68_GATE',source_id='L017',source_ids=['L017'],source_author_role='Dimitri Leemans, Klara Stokes and Philippe Tranchida; focal-group-authored source.',principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=logical(AUTHOR+'/manifest.json'),distinct_root_review_manifest=logical(REVIEW+'/manifest.json'),root_scientific_acceptance=logical(REVIEW+'/manifest.json'),source_map=logical(AUTHOR+'/source_map.json'),source_contract=logical(AUTHOR+'/scope.json'),dependency_boundary=logical(AUTHOR+'/retained_inputs.json'),program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(x['pdf'])for x in native],physical_pages=[6,4,3,3],source_pages=17,source_routes=53,named_source_results=13,reported_examples=7,finite_premises=[logical(AUTHOR+'/'+p)for p in ['finite_graphs.cpp','graph_certificate.py','automorphism_witnesses.json']],comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note=note,roles='rewrite_termination authored the current papers/programs and the earlier odd-completion proof; root distinctly reviewed the complete L017 source contract. The earlier equation proof was root-authored and enumeration_volume-reviewed. Exact prior roles remain visible; this publication proposal is operational, not a new mathematical review.',frozen_status_overlay='Earlier pending-review sentences remain exact. The later complete root review supplies current scientific acceptance without changing any frozen payload.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap);rp=AUDIT+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['L017'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['L017']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
 cat.update(status='CURRENT_ACCESSIBLE106_68_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=68,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=37,review_revision='Only L017 becomes an accepted corrected principal recovery; 105 other original records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=68,measured=53,measurement_pending=15,pending=37,editorial=1))
 row=next(x for x in cat['entries']if x['original_id']=='L017');previous=copy.deepcopy(row['current_principal_recovery']);row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous);row['next_obligation']='Any later measurement acquires all four complete papers (16 pages), two required current programs, literal data and exact whole predecessor dependencies. Retained classical proof and source software costs are unknown. Optional verification must use a symmetric boundary; no current factor.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured68-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_68_CORRECTED_RECOVERIES_53_MEASURED_37_PENDING_1_EDITORIAL',admitted_principal_originals=68,accessible_pending_complete_recovery=37,admitted_original_ids=sorted(old['admitted_original_ids']+['L017']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids']if i!='L017'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured68.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 for x in native:x['admission']=admission
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('L017');sc['root_publication_gate']=AUDIT+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_FIFTEEN_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(HERE/'native_catalogue.json',dict(new_acquisition_entries=native,complete_scientific_pages=16,new_native_documents=2,reused_whole_native_documents=2,compiler='pdflatex',all_whole_papers_paid=True))
 oldlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015, L096, L023 and L031';newlist=oldlist.replace(' and L031',', L031 and L017')
 paragraph='''The `L017 guide <papers/recoveries/L017/v1/PUBLICATION.rst>`_ acquires all four
whole papers (16 pages), including two unchanged L023 proofs. The classical
moving geometry and fixed absolute are recovered. Exact finite certificates
separate the two q=4 graphs, exclude the claimed q=7 84-vertex quartic graph,
and correct the full automorphism order of its 168-vertex example. All 53
source dispositions and retained inputs are explicit. This recovery includes
corrections; it does not assert that every original statement is true.
No factor, new question answer or Lean declaration is added.

'''
 t=(repo/'README.rst').read_text().replace('**67 accessible originals','**68 accessible originals').replace('53 are measured and fourteen ('+oldlist+')','53 are measured and fifteen ('+newlist+')').replace('38 await mathematical recovery;','37 await mathematical recovery;').replace('All fourteen source editions',paragraph+'All fifteen source editions').replace('None of these fourteen recoveries','None of these fifteen recoveries').replace('audit/science67/v1/new_original_registration.json',rp);write(W/'README.rst',t)
 summary='''L017 retains all four complete papers (16 pages), 53 source dispositions and
seven finite examples. The q=4 graph distinction, q=7 absent 84-vertex example
and corrected full automorphism order remain explicit. Two exact programs and
literal data are finite premises; classical inputs and source software costs
remain declared. No factor, new question answer or Lean declaration is added.

'''
 t=(repo/'audit/completion.rst').read_text().replace('**67 reviewed corrected principal recoveries**','**68 reviewed corrected principal recoveries**').replace('53 are measured and fourteen ('+oldlist+') are unmeasured. There are 38 originals','53 are measured and fifteen ('+newlist+') are unmeasured. There are 37 originals').replace(oldlist+' have separate scientific admissions',newlist+' have separate scientific admissions').replace('science67/v1/new_original_registration.json','science68/v1/new_original_registration.json').replace('The `current overview',summary+'The `current overview',1);write(W/'audit/completion.rst',t)
 t=(repo/'audit/protocol.tex').read_text().replace('106=67\\ \\text{reviewed corrected recoveries}+38','106=68\\ \\text{reviewed corrected recoveries}+37').replace('Of the 67 corrected recoveries','Of the 68 corrected recoveries').replace(oldlist+' are scientifically accepted but unmeasured',newlist+' are scientifically accepted but unmeasured').replace('The accepted overview v19',summary.replace('q=4','$q=4$').replace('q=7','$q=7$')+'The accepted overview v19',1);write(W/'audit/protocol.tex',t)
 guide='''L017: absolute flags and moving lines
====================================

This is the complete corrected principal recovery of Dimitri Leemans, Klara
Stokes and Philippe Tranchida, On trialities and their absolute geometries,
in the fixed 17-page draft dated 21 March 2024. Root's full independent review
accepts all 53 source dispositions, including 13 named results and seven
examples. Public registration requires the root-owned science68 gate.

The complete acquisition comprises the six-page uniform paper, four-page
finite comparison and both whole three-page L023 dependencies. The latter
are reused at their immutable public routes and remain fully charged.

The uniform proof supplies classical moving parameters and distances,
characteristic-two completion and the fixed absolute. Classical triality,
projective-linear descent and subgroup classification remain explicit inputs.
The exact finite work distinguishes the q=4 moving graph from its connected
fixed--moving union, excludes the asserted q=7 84-vertex quartic example by
complete marking exhaustion, and proves the actual 168-vertex graph has full
automorphism order 2^28 times 336. The source centralizer algorithm is corrected.
This recovery includes corrections; it does not assert that every original
statement is true.

Two whole current programs and literal permutation data are required finite
premises. Their exact field/coset and full graph-automorphism calculations are
replayed from public files. Optional GAP validation and all operational tools
remain separately inventoried; no compiler or kernel verification is claimed.
Historical Magma software and external proof costs are unknown, not zero.
Type-II trialities remain a source future-work direction. No factor, new topic,
new question answer or Lean declaration is added.

'''
 for d in native:guide+='* `'+d['title']+' <'+os.path.relpath(d['pdf'],NATIVE)+'>`_ ('+str(d['physical_pages'])+' pages).\n'
 guide+='\n`Admission <../../../../audit/recoveries/L017/v1/admission.json>`_ and\n`source dispositions <../../../../audit/recoveries/L017/v1/author/source_map.json>`_\nretain exact scope and attribution. rewrite_termination authored the current\nscience and finite programs, distinctly reviewed by root. The earlier\nodd-completion proof has the same author and its separate root review; the\nequation proof is root-authored and enumeration_volume-reviewed. This\npublication proposal adds no mathematical adjudication.\n';write(W/(NATIVE+'/PUBLICATION.rst'),guide)
 write(W/'scripts/check_science68_history.py',(HERE/'history_wrapper.py').read_text());write(W/'scripts/check_science68.py','''"""Root-gated science68 publication entry."""
from pathlib import Path
import importlib.util
def verify(root):
 root=Path(root).resolve()
 spec=importlib.util.spec_from_file_location('science68_plan',root/'audit/science68/v1/publication_plan/check.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module.verify(root,require_root=True)
''')
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['L017'],counts=dict(active=106,corrected_recoveries=68,measured=53,unmeasured=15,mathematical_pending=37,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 write(HERE/'acceptance_binding.json',dict(root_review_manifest=logical(REVIEW+'/manifest.json'),author_manifest_sha256=plan['current_pins'][AUTHOR],distinct_whole_acceptance=True,public_review_records=[logical(x['study_path'])for x in plan['files']if x['study_path'].startswith(REVIEW+'/')],role='Root independently accepted the full corrected source contract; current author does not self-review science through this operational proposal.'))
 diff=''
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']:diff+=''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))
 write(HERE/'documentation.diff',diff);print('prepared',len(plan['files']),'logical payloads;',len(asts),'old functions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
