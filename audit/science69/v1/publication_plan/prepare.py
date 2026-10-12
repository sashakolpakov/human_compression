"""Prepare science69 wrappers privately; root alone installs and publishes."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,os,re,subprocess
HERE=Path(__file__).resolve().parent;AUDIT='audit/science69/v1';SCIENCE='audit/recoveries/L018/v1';NATIVE='papers/recoveries/L018/v1';AUTHOR='corpus106_L018_complete_candidate';BASE='26a3ffbf12a5954d6ec462d854d8b13aa6b4e082'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str)else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 need(not(HERE/'manifest.json').exists(),'frozen proposal');repo=a.repo;W=HERE/'wrappers'
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact baseline')
 old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(68,53,37),'science68 partition')
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
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science68 pointers and nested historical validation through programme53.'))
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'};need(len(asts)==163,'163 existing non-main functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science68/v1/root_integration.json']+[str(p.relative_to(repo))for p in(repo/'audit/overview/v19/packet').rglob('*')if p.is_file()]
 write(HERE/'baseline.json',dict(commit=BASE,origin_main_at_preparation=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip(),old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n)for n in protected]))
 inv=load(a.study/AUTHOR/'program_inventory.json');raw=copy.deepcopy(inv)
 raw['public_bindings']=[logical(AUTHOR+'/'+x['path'])for x in inv['whole_files']+inv['required_mathematical_data']]
 raw.update(source_software_cost=None,external_proof_cost=None,measurement=None,current_source_code_boundary='The fixed 11-page source is retained privately. Its current retrieved Julia edition is distinguished from the unknown historical executed closure. All five executed C++ variants, the divisor roster and coverage assembler are whole required finite programs; all twelve mathematical data/receipt files are paid. Four optional validation programs and four operational files remain distinct. No software-inclusive factor or compiler/kernel proof is claimed.')
 write(W/(AUDIT+'/whole_file_roles.json'),raw)
 native=[]
 for d in load(a.study/AUTHOR/'scope.json')['native_documents']:
  pdf=d['path'];tex=str(Path(pdf).with_suffix('.tex'));t=(a.study/AUTHOR/tex).read_text();native.append(dict(id='L018_'+Path(tex).stem,title=re.search(r'\\title\{([^{}]+)\}',t).group(1),tex=logical(AUTHOR+'/'+tex)['path'],pdf=logical(AUTHOR+'/'+pdf)['path'],tex_inputs=[],compiler='pdflatex',physical_pages=d['pages'],role=d['role'],source_ids=['L018'],topic='Equal-area rectangle partitions',comparison_topic_created=False,measured=False,compression_factor=None,existing_public_dependency=False))
 note='Complete corrected principal L018 recovery: all 36 dispositions across the fixed 11-page source. The seven-piece lower bound and complete exact searches recover the square range through side 1000 and rectangular range through both sides 400. All 103 square and 11,126 rectangle arithmetic cases have completed exclusions. Printed shape products, perimeter conventions and a false subset-sum assertion are corrected; the rectangular orientation issue concerns the pinned current source-code edition, not an alleged counterexample to the finite conclusions. General integer existence and defect-bound questions remain unanswered. No theorem-set equivalence, new question, Lean, comparison topic or factor is claimed.'
 ad=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE69_GATE',source_id='L018',source_ids=['L018'],source_author_role='Natalia García-Colín, Dimitri Leemans, Mia Müßig and Érika Roldán; focal-group-authored source.',principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=logical(AUTHOR+'/manifest.json'),distinct_root_review_manifest=logical(REVIEW+'/manifest.json'),root_scientific_acceptance=logical(REVIEW+'/manifest.json'),source_map=logical(AUTHOR+'/source_contract.json'),source_contract=logical(AUTHOR+'/scope.json'),dependency_boundary=logical(AUTHOR+'/dependencies.json'),program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(x['pdf'])for x in native],physical_pages=[5,3],source_pages=11,source_routes=36,completed_case_routes=dict(squares=103,rectangles=11126),finite_premises=[logical(AUTHOR+'/'+x['path'])for x in inv['whole_files']if x['role']=='REQUIRED_FINITE_PROOF_PROGRAM'],required_mathematical_data=[logical(AUTHOR+'/'+x['path'])for x in inv['required_mathematical_data']],comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note=note,roles='rewrite_termination authored the science, finite programs and executions. Root supplied preliminary reading and suggested modular/coloring necessary prunes, then distinctly reviewed the complete source/proof/program contract and replayed the finite computations. This publication proposal is operational, not a new mathematical review.',frozen_status_overlay='The author pending-review sentences remain exact. The later whole root review supplies current scientific acceptance without altering any frozen payload.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap);rp=AUDIT+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['L018'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['L018']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
 cat.update(status='CURRENT_ACCESSIBLE106_69_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=69,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=36,review_revision='Only L018 becomes an accepted corrected principal recovery; 105 other original records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=69,measured=53,measurement_pending=16,pending=36,editorial=1))
 row=next(x for x in cat['entries']if x['original_id']=='L018');previous=copy.deepcopy(row['current_principal_recovery']);row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous);row['next_obligation']='Any later measurement acquires both complete papers (8 pages), all seven required programs and twelve whole data/receipt files. Historical executed source software costs are unknown. Optional verification must use a symmetric boundary; no current factor.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured69-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_69_CORRECTED_RECOVERIES_53_MEASURED_36_PENDING_1_EDITORIAL',admitted_principal_originals=69,accessible_pending_complete_recovery=36,admitted_original_ids=sorted(old['admitted_original_ids']+['L018']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids']if i!='L018'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured69.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 for x in native:x['admission']=admission
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('L018');sc['root_publication_gate']=AUDIT+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_SIXTEEN_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(HERE/'native_catalogue.json',dict(new_acquisition_entries=native,complete_scientific_pages=8,new_native_documents=2,reused_whole_native_documents=0,compiler='pdflatex',all_whole_papers_paid=True))
 oldlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015, L096, L023, L031 and L017';newlist=oldlist.replace(' and L017',', L017 and L018')
 paragraph='''The `L018 guide <papers/recoveries/L018/v1/PUBLICATION.rst>`_ gives a written
seven-piece lower bound and complete exact exclusions for squares through side
1000 and rectangles with both sides through 400. Both whole papers (8 pages),
all required programs and completed case receipts are acquired. Printed shape
products, perimeter conventions and one subset-sum assertion are corrected;
the separate code audit concerns the pinned current source edition. The two
general existence and defect questions remain unanswered. This recovery
includes corrections; it does not assert that every original statement is true.
No factor, new question answer or Lean declaration is added.

'''
 t=(repo/'README.rst').read_text().replace('**68 accessible originals','**69 accessible originals').replace('53 are measured and fifteen ('+oldlist+')','53 are measured and sixteen ('+newlist+')').replace('37 await mathematical recovery;','36 await mathematical recovery;').replace('All fifteen source editions',paragraph+'All sixteen source editions').replace('None of these fifteen recoveries','None of these sixteen recoveries').replace('audit/science68/v1/new_original_registration.json',rp);write(W/'README.rst',t)
 summary='''L018 acquires both complete papers (8 pages), all 36 source dispositions,
seven required programs and twelve whole data/receipt files. The seven-piece
bound and both finite exclusion ranges are proved. Source arithmetic and
perimeter qualifications remain explicit, as do the two unanswered general
questions. No factor, new question answer or Lean declaration is added.

'''
 t=(repo/'audit/completion.rst').read_text().replace('**68 reviewed corrected principal recoveries**','**69 reviewed corrected principal recoveries**').replace('53 are measured and fifteen ('+oldlist+') are unmeasured. There are 37 originals','53 are measured and sixteen ('+newlist+') are unmeasured. There are 36 originals').replace(oldlist+' have separate scientific admissions',newlist+' have separate scientific admissions').replace('science68/v1/new_original_registration.json','science69/v1/new_original_registration.json').replace('The `current overview',summary+'The `current overview',1);write(W/'audit/completion.rst',t)
 t=(repo/'audit/protocol.tex').read_text().replace('106=68\\ \\text{reviewed corrected recoveries}+37','106=69\\ \\text{reviewed corrected recoveries}+36').replace('Of the 68 corrected recoveries','Of the 69 corrected recoveries').replace(oldlist+' are scientifically accepted but unmeasured',newlist+' are scientifically accepted but unmeasured').replace('The accepted overview v19',summary+'The accepted overview v19',1);write(W/'audit/protocol.tex',t)
 guide='''L018: equal-area rectangle partitions
======================================

This is the complete corrected principal recovery of Natalia García-Colín,
Dimitri Leemans, Mia Müßig and Érika Roldán, There is no perfect Mondrian
partition for squares of side lengths less than 1001, in the fixed 11-page
arXiv2311.02385v1 edition. All 36 source dispositions are explicit. Scientific
acceptance is bound to the distinct root review; public registration also
requires the separate root-owned science69 gate.

The whole five-page common proof and three-page application give the real
seven-piece lower bound, exact integer-coordinate and valley search arguments,
and complete exclusions for squares through side 1000 and rectangles with
both sides through 400. All 103 square and 11,126 rectangle arithmetic cases
have completed exact exclusions. The final 840/20 and 840/21 reductions have
explicit parity, endpoint and symmetry proofs; no timeout supplies evidence
of nonexistence.

Printed shape products, the unrestricted perimeter threshold and a false
subset-sum impossibility are corrected. The orientation-list audit is tied
to the retrieved current source-code edition and is not a claim that the
original finite conclusions are false. Historical filter counts, timing
plots and runtime estimates are not reproduced or used as premises. This
recovery includes corrections; it does not assert that every original
statement is true. Integer perfect-partition existence and the general
defect-bound question remain unanswered here.

All five executed C++ variants, the complete divisor-roster program and the
coverage assembler are required finite premises. All twelve mathematical
data and receipt files are retained whole. Four optional validation programs
and four operational files are inventoried separately. The exact historical
source software closure and its costs are unknown, not zero. Ordinary compiler
and integer execution are trusted; no CP-SAT, Lean or kernel certificate is
claimed. No compression factor or new comparison topic is added.

'''
 for d in native:guide+='* `'+d['title']+' <'+os.path.relpath(d['pdf'],NATIVE)+'>`_ ('+str(d['physical_pages'])+' pages).\n'
 guide+='\n`Admission <../../../../audit/recoveries/L018/v1/admission.json>`_ and\n`source dispositions <../../../../audit/recoveries/L018/v1/author/source_contract.json>`_\nretain exact scope and attribution. rewrite_termination authored the current\nscience and finite programs; root supplied preliminary proof reading and a\nmodular-pruning suggestion, then distinctly reviewed the complete source,\nproofs and implementations and replayed the computations. This operational\npublication proposal adds no scientific or question credit.\n';write(W/(NATIVE+'/PUBLICATION.rst'),guide)
 write(W/'scripts/check_science69_history.py',(HERE/'history_wrapper.py').read_text());write(W/'scripts/check_science69.py','''"""Root-gated science69 publication entry."""
from pathlib import Path
import importlib.util
def verify(root):
 root=Path(root).resolve()
 spec=importlib.util.spec_from_file_location('science69_plan',root/'audit/science69/v1/publication_plan/check.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module.verify(root,require_root=True)
''')
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['L018'],counts=dict(active=106,corrected_recoveries=69,measured=53,unmeasured=16,mathematical_pending=36,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 write(HERE/'acceptance_binding.json',dict(root_review_manifest=logical(REVIEW+'/manifest.json'),author_manifest_sha256=plan['current_pins'][AUTHOR],distinct_whole_acceptance=True,public_review_records=[logical(x['study_path'])for x in plan['files']if x['study_path'].startswith(REVIEW+'/')],role='Root independently accepted the full corrected source contract; current author does not self-review science through this operational proposal.'))
 diff=''
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']:diff+=''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))
 write(HERE/'documentation.diff',diff);print('prepared',len(plan['files']),'logical payloads;',len(asts),'old functions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
