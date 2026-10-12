"""Prepare a private N011 science-only successor to exact public science69."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent
AUDIT='audit/science70/v1';SCIENCE='audit/recoveries/N011/v1';NATIVE='papers/recoveries/N011/v1'
AUTHOR='corpus106_N011_recovery';BASE='6b0ca7eacea91a764f527b1945837cc64bedf720'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str)else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 need(not(HERE/'manifest.json').exists(),'frozen proposal');repo=a.repo;W=HERE/'wrappers'
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact baseline')
 old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(69,53,36),'science69 partition')
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
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science69 pointers and nested historical validation through programme53.'))
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(len(asts)==165,'165 existing non-main functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science69/v1/root_integration.json']+[str(p.relative_to(repo))for p in(repo/'audit/overview/v19/packet').rglob('*')if p.is_file()]
 write(HERE/'baseline.json',dict(commit=BASE,origin_main_at_preparation=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip(),old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n)for n in protected]))
 inv=load(a.study/AUTHOR/'program_inventory.json');raw=copy.deepcopy(inv)
 raw['public_bindings']=[logical(AUTHOR+'/'+x['path'])for x in inv['files']]+[logical(AUTHOR+'/'+inv['optional_result'])]
 raw.update(source_software_cost=None,external_proof_cost=None,measurement=None,current_source_code_boundary='The full13-page source has mathematical matrices but no executable listing. The symbolic Python check is optional validation, not a proof premise. The complete operational driver and optional output are retained. Historical source software and external complete proof costs remain unknown. No software-inclusive factor is created.')
 write(W/(AUDIT+'/whole_file_roles.json'),raw)
 native=[]
 for d in load(a.study/AUTHOR/'native.json')['documents']:
  t=(a.study/AUTHOR/d['tex']).read_text();native.append(dict(id='N011_'+Path(d['tex']).stem,title=re.search(r'\\title\{([^{}]+)\}',t).group(1),tex=logical(AUTHOR+'/'+d['tex'])['path'],pdf=logical(AUTHOR+'/'+d['pdf'])['path'],tex_inputs=[],compiler='pdflatex',physical_pages=d['pages'],role='whole common theory'if d['pages']==2 else'whole application',source_ids=['N011'],topic='Finite linear involution generation',comparison_topic_created=False,measured=False,compression_factor=None,existing_public_dependency=False))
 note='Complete corrected principal N011 recovery on the intended domain n>=2: both GL and PGL classifications, all twelve table rows, all four constructive branches and the retained-criterion polytope consequence. All57 source dispositions across13 pages are explicit. Degree-one scope, determinant sign, matrix entry, conjugator and whole-product-square corrections are disclosed. Simple-group classification, the PGL2 theorem, integral GL generation and the polytope criterion remain named external inputs with unknown full proof costs. No literal theorem-set equivalence, new question, Lean, comparison topic or factor is claimed.'
 ad=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE70_GATE',source_id='N011',source_ids=['N011'],source_authors=['Irina A. Markovskaya','Yakov N. Nuzhin'],principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=logical(AUTHOR+'/manifest.json'),distinct_root_review_manifest=logical(REVIEW+'/manifest.json'),root_scientific_acceptance=logical(REVIEW+'/manifest.json'),source_map=logical(AUTHOR+'/source_map.json'),source_contract=logical(AUTHOR+'/scope.json'),dependency_boundary=logical(AUTHOR+'/retained_inputs.json'),program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(x['pdf'])for x in native],physical_pages=[2,7],source_pages=13,source_routes=57,source_table_rows=12,finite_premises=[],required_mathematical_data=[],comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note=note,roles='rewrite_termination authored both current manuscripts and the optional symbolic validation. Root distinctly reviewed the complete source, proofs, programs and fresh native replay. Enumeration_volume prepared this operational publication proposal; this is not a new independent mathematical review.',frozen_status_overlay='Exact pending-review author bytes are preserved. The later whole root review supplies current scientific acceptance.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap);rp=AUDIT+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['N011'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['N011']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
 cat.update(status='CURRENT_ACCESSIBLE106_70_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=70,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=35,review_revision='Only N011 becomes an accepted corrected principal recovery; 105 other original records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=70,measured=53,measurement_pending=17,pending=35,editorial=1))
 row=next(x for x in cat['entries']if x['original_id']=='N011');previous=copy.deepcopy(row['current_principal_recovery']);row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous);row['next_obligation']='Any later measurement acquires both whole papers (2+7 pages) and the named retained external inputs. Optional symbolic validation and its output, and the complete operational driver, remain separately inventoried. Source software and external complete proof costs are unknown; no current factor.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured70-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_70_CORRECTED_RECOVERIES_53_MEASURED_35_PENDING_1_EDITORIAL',admitted_principal_originals=70,accessible_pending_complete_recovery=35,admitted_original_ids=sorted(old['admitted_original_ids']+['N011']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids']if i!='N011'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured70.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 for x in native:x['admission']=admission
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('N011');sc['root_publication_gate']=AUDIT+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_SEVENTEEN_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(HERE/'native_catalogue.json',dict(new_acquisition_entries=native,complete_scientific_pages=9,new_native_documents=2,reused_whole_native_documents=0,compiler='pdflatex',all_whole_papers_paid=True))
 oldlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015, L096, L023, L031, L017 and L018';newlist=oldlist.replace(' and L018',', L018 and N011')
 paragraph='''The `N011 guide <papers/recoveries/N011/v1/PUBLICATION.rst>`_ supplies the
whole two-page root-parameter theory and seven-page finite linear application
for the GL and PGL classifications on their intended domain n >= 2. All twelve
table rows and four constructive branches are covered. Literal intermediate
matrix expressions are corrected; the external classification and polytope
inputs remain explicit. Symbolic checks are optional validation. No factor,
new question answer or Lean declaration is added.

'''
 t=(repo/'README.rst').read_text().replace('**69 accessible originals','**70 accessible originals').replace('53 are measured and sixteen ('+oldlist+')','53 are measured and seventeen ('+newlist+')').replace('36 await mathematical recovery;','35 await mathematical recovery;').replace('All sixteen source editions',paragraph+'All seventeen source editions').replace('None of these sixteen recoveries','None of these seventeen recoveries').replace('audit/science69/v1/new_original_registration.json',rp);write(W/'README.rst',t)
 summary='''N011 acquires both complete papers (2+7 pages) and all 57 source dispositions.
Both finite linear classifications and all twelve table rows are recovered on
their intended domain n >= 2, with intermediate literal corrections disclosed.
External classification inputs remain retained; optional symbolic validation
is not a finite proof premise. No factor, question or Lean claim is added.

'''
 t=(repo/'audit/completion.rst').read_text().replace('**69 reviewed corrected principal recoveries**','**70 reviewed corrected principal recoveries**').replace('53 are measured and sixteen ('+oldlist+') are unmeasured. There are 36 originals','53 are measured and seventeen ('+newlist+') are unmeasured. There are 35 originals').replace(oldlist+' have separate scientific admissions',newlist+' have separate scientific admissions').replace('science69/v1/new_original_registration.json','science70/v1/new_original_registration.json').replace('The `current overview',summary+'The `current overview',1);write(W/'audit/completion.rst',t)
 t=(repo/'audit/protocol.tex').read_text().replace('106=69\\ \\text{reviewed corrected recoveries}+36','106=70\\ \\text{reviewed corrected recoveries}+35').replace('Of the 69 corrected recoveries','Of the 70 corrected recoveries').replace(oldlist+' are scientifically accepted but unmeasured',newlist+' are scientifically accepted but unmeasured').replace('The accepted overview v19',summary.replace('n >= 2',' $n\\geq2$')+'The accepted overview v19',1);write(W/'audit/protocol.tex',t)
 guide='''N011: finite general linear groups
===================================

This is the complete corrected principal recovery of Irina A. Markovskaya and
Yakov N. Nuzhin, in the fixed thirteen-page 2025 source edition. All 57 source
dispositions, both GL and PGL classifications, all twelve table rows and the
four constructive branches are explicit. The intended degree domain is n >= 2.
Scientific acceptance is supplied by the distinct root review. Current public
registration additionally requires the separate root-owned science70 gate.

The two-page common paper proves root-parameter recognition and fixed-space
obstructions. The seven-page application supplies all finite linear parameter
branches, small exceptions and the regular-polytope consequence. The original
source matrices and obstructions retain their authorship. Intermediate sign,
matrix-entry, conjugator and product-square expressions are corrected. These
corrections do not refute the intended principal classifications, and no
equivalence with every literal source assertion is claimed.

The simple-group classification, PGL2 generation theorem, integral GL theorem
and rank-three polytope criterion remain named retained inputs. Their complete
proof costs and historical software costs are unknown, not zero. The broad
rank-two Levchuk assertions are retained background rather than premises of
the replacement construction. No required finite search or data premise is
introduced. The complete symbolic program is optional validation, with its
whole output and the operational replay driver preserved separately. No
measurement, comparison topic, new question answer or Lean claim is added.

'''
 for d in native:guide+='* `'+d['title']+' <'+os.path.relpath(d['pdf'],NATIVE)+'>`_ ('+str(d['physical_pages'])+' pages).\n'
 guide+='\n`Admission <../../../../audit/recoveries/N011/v1/admission.json>`_,\n`source dispositions <../../../../audit/recoveries/N011/v1/author/source_map.json>`_\nand `retained inputs <../../../../audit/recoveries/N011/v1/author/retained_inputs.json>`_\ncarry the exact boundary. rewrite_termination authored the current science and\noptional validation; root distinctly reviewed it. Enumeration_volume prepared\nthis operational publication mapping without claiming a new scientific review.\n';write(W/(NATIVE+'/PUBLICATION.rst'),guide)
 write(W/'scripts/check_science70_history.py',(HERE/'history_wrapper.py').read_text());write(W/'scripts/check_science70.py','''"""Root-gated science70 publication entry."""
from pathlib import Path
import importlib.util
def verify(root):
 root=Path(root).resolve()
 spec=importlib.util.spec_from_file_location('science70_plan',root/'audit/science70/v1/publication_plan/check.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module.verify(root,require_root=True)
''')
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['N011'],counts=dict(active=106,corrected_recoveries=70,measured=53,unmeasured=17,mathematical_pending=35,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 write(HERE/'acceptance_binding.json',dict(root_review_manifest=logical(REVIEW+'/manifest.json'),author_manifest_sha256=plan['current_pins'][AUTHOR],distinct_whole_acceptance=True,public_review_records=[logical(x['study_path'])for x in plan['files']if x['study_path'].startswith(REVIEW+'/')],role='Root distinctly accepted the complete corrected principal contract; this operational proposal is not a further mathematical review.'))
 diff=''
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']:diff+=''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))
 write(HERE/'documentation.diff',diff);print('prepared',len(plan['files']),'payloads;',len(asts),'old functions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
