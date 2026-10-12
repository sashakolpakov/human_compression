"""Prepare science67 wrappers privately on exact science66; root alone installs."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;AUDIT='audit/science67/v1';SCIENCE='audit/recoveries/L031/v1';NATIVE='papers/recoveries/L031/v1';BASE='2783b3c3c03aa71dcf3c3cb9b30a2b0b9055d939';AUTHOR='corpus106_L031_recovery'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 need(not(HERE/'manifest.json').exists(),'frozen proposal');repo=a.repo;W=HERE/'wrappers'
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact baseline')
 old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(66,53,39),'science66 counts')
 plan=load(HERE/'copy_plan.json');REVIEW=plan['root_review_directory'];routes={r['study_path']:r for r in plan['files']}
 def logical(n):
  r=routes[n];return dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
 def pub(n):
  if (W/n).is_file():return pin(W/n,n)
  r=next((x for x in plan['files'] if x['public_path']==n),None)
  return dict(path=n,bytes=r['bytes'],sha256=r['sha256']) if r else pin(repo/n,n)
 history={}
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']:
  dest=AUDIT+'/previous/'+n;p=W/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/n).read_bytes());history[n]=pin(p,dest)
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science66 pointers and nested historical validation through programme53.'))
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'};need(len(asts)==159,'159 prior functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science66/v1/root_integration.json']+[str(p.relative_to(repo)) for p in (repo/'audit/overview/v19/packet').rglob('*') if p.is_file()]
 write(HERE/'baseline.json',dict(commit=BASE,origin_main_at_preparation=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip(),old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n) for n in protected]))
 inv=load(a.study/AUTHOR/'program_inventory.json');roles=copy.deepcopy(inv)
 for r in roles['whole_executable_files']:r['public_binding']=logical(AUTHOR+'/'+r['path'])
 roles.update(source_software_cost=None,external_proof_cost=None,measurement=None,current_source_code_boundary='Complete12-page source has no executable listing; historical Magma code remains unknown. The retained optional oracle and all operational scripts are whole files, not mathematical premises. No software-inclusive factor.')
 write(W/(AUDIT+'/whole_file_roles.json'),roles)
 native=[]
 for d in load(a.study/AUTHOR/'native_documents.json')['documents']:
  t=(a.study/AUTHOR/d['tex']).read_text();native.append(dict(id='L031_'+Path(d['tex']).stem,title=re.search(r'\\title\{([^{}]+)\}',t).group(1),tex=logical(AUTHOR+'/'+d['tex'])['path'],pdf=logical(AUTHOR+'/'+d['pdf'])['path'],tex_inputs=[],compiler='pdflatex',physical_pages=d['pages'],role='whole scientific proof component',source_ids=['L031'],topic='Characteristic-two symmetry markings',comparison_topic_created=False,measured=False,compression_factor=None,existing_public_dependency=routes[AUTHOR+'/'+d['pdf']]['transport']=='EXISTING_PUBLIC'))
 note='Complete corrected principal L031 recovery: all57 dispositions across the complete12-page source; seven whole native papers total23pages. Positive q>=4 construction gives both orthogonal types and odd symplectic groups; exact binary existence dimensions3,4,5 and exclusion d>=6 replace the printed binary exclusion. The unrestricted binary Proposition3.3 is refuted. Literal four-matrix rank4 family has plus-type first-three subgroup, while full Sp4 generation/IP are proved. Complete low-dimensional spectrum uses the acquired L011 obstruction and separately reviewed centralizer bound. The source primitive-parameter instruction is replaced by an explicit endpoint trace proof. Classical symmetry generation, Dickson maximality/character, Arf and Klein facts remain external inputs. Source questions stay recorded without present-day status or new answer. No theorem-set equivalence, finite premise, new factor or Lean claim.'
 ad=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE67_GATE',source_id='L031',source_ids=['L031'],source_author_role='P. A. Brooksbank, J. T. Ferrara and D. Leemans; focal-group-authored source.',principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=logical(AUTHOR+'/manifest.json'),distinct_root_review_manifest=logical(REVIEW+'/manifest.json'),root_scientific_acceptance=logical(REVIEW+'/manifest.json'),source_map=logical(AUTHOR+'/source_map.json'),source_contract=logical(AUTHOR+'/source_contract.json'),dependency_boundary=logical(AUTHOR+'/dependencies.json'),migration=logical(AUTHOR+'/migration.json'),program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(d['pdf']) for d in native],physical_pages=[5,3,5,2,2,2,4],source_pages=12,source_routes=57,principal_targets=4,finite_premises=[],comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note=note,roles='Enumeration_volume authored the three current papers and the earlier acquired L011 obstruction; root distinctly reviewed those. Root authored the two binary and centralizer companions, independently reviewed by enumeration_volume. Exact earlier attributions/reviews remain. This operational proposal is not self-adjudication.',frozen_status_overlay='The exact later complete root review governs scientific acceptance; earlier pending author/review sentences remain immutable.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap);rp=AUDIT+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['L031'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['L031']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
 cat.update(status='CURRENT_ACCESSIBLE106_67_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=67,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=38,review_revision='Only L031 becomes an accepted corrected principal recovery;105 other original records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=67,measured=53,measurement_pending=14,pending=38,editorial=1))
 row=next(r for r in cat['entries'] if r['original_id']=='L031');previous=copy.deepcopy(row['current_principal_recovery'])
 row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous)
 row['next_obligation']='Any later measurement must acquire all seven complete native papers23pages, including the full reused L011 obstruction, and retain external proof/software unknowns. No required finite program. No literal theorem-set equivalence or new question credit.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured67-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_67_CORRECTED_RECOVERIES_53_MEASURED_38_PENDING_1_EDITORIAL',admitted_principal_originals=67,accessible_pending_complete_recovery=38,admitted_original_ids=sorted(old['admitted_original_ids']+['L031']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids'] if i!='L031'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured67.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 for r in native:r['admission']=admission
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('L031');sc['root_publication_gate']=AUDIT+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_FOURTEEN_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(HERE/'native_catalogue.json',dict(new_acquisition_entries=native,complete_scientific_pages=23,new_native_documents=6,reused_whole_native_documents=1,compiler='pdflatex',all_whole_papers_paid=True))
 oldlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015, L096 and L023';newlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015, L096, L023 and L031'
 t=(repo/'README.rst').read_text().replace('**66 accessible originals','**67 accessible originals').replace('53 are measured and thirteen ('+oldlist+')','53 are measured and fourteen ('+newlist+')').replace('39 await mathematical recovery;','38 await mathematical recovery;')
 insert='The `L031 guide <'+NATIVE+'/PUBLICATION.rst>`_ acquires seven complete native papers\n(23 pages), including the unchanged four-page L011 obstruction. Larger fields\nhave all stated symmetry ranks and both orthogonal types. The binary boundary\nis corrected to dimensions 3, 4 and 5; the unrestricted binary intersection\nclaim and the displayed matrices\' intermediate type are corrected explicitly.\nAll 57 source dispositions and retained classical inputs are visible. There\nis no required finite program, new question answer or new factor.\n\nAll fourteen source editions, complete proof packets and distinct reviews are recorded'
 need('All thirteen source editions, complete proof packets and distinct reviews are recorded' in t,'reader insertion');t=t.replace('All thirteen source editions, complete proof packets and distinct reviews are recorded',insert).replace('None of these thirteen recoveries','None of these fourteen recoveries').replace('audit/science66/v1/new_original_registration.json',rp);write(W/'README.rst',t)
 t=(repo/'audit/completion.rst').read_text().replace('**66 reviewed corrected principal recoveries**','**67 reviewed corrected principal recoveries**').replace('53 are measured and thirteen ('+oldlist+') are unmeasured. There are 39 originals','53 are measured and fourteen ('+newlist+') are unmeasured. There are 38 originals').replace(oldlist+' have separate scientific admissions',newlist+' have separate scientific admissions').replace('science66/v1/new_original_registration.json','science67/v1/new_original_registration.json')
 t=t.replace('The `current overview','L031 acquires the whole 23-page corrected proof closure and all 57 source\ndispositions, including exact reused L011 theory. Binary existence/intersection\nand literal-matrix type corrections are explicit; larger-field existence and\nthe complete low-dimensional spectrum are proved. Classical inputs and unknown\nsource software remain; no finite premise, factor or new question is added.\n\nThe `current overview',1)
 t=t.replace('L044 and L096\nremain pending; their partial results receive no whole-original credit here.','L044 remains pending. L096 received its later corrected scientific admission\nwithout a manuscript factor; its earlier partial results remain historical.')
 write(W/'audit/completion.rst',t)
 t=(repo/'audit/protocol.tex').read_text().replace('106=66\\ \\text{reviewed corrected recoveries}+39','106=67\\ \\text{reviewed corrected recoveries}+38').replace('Of the 66 corrected recoveries','Of the 67 corrected recoveries').replace(oldlist+' are scientifically accepted but unmeasured',newlist+' are scientifically accepted but unmeasured')
 t=t.replace('The accepted overview v19','L031 acquires seven whole native papers, totalling 23 pages, with the earlier\nfour-page L011 obstruction retained byte-for-byte. The exact binary existence\nboundary, binary intersection counterexample and plus-type intermediate group\ncorrect the corresponding source clauses. All larger-field ranks, both Witt\ntypes and the complete low-dimensional spectrum are recovered. All 57 source\ndispositions retain explicit classical proof costs; no finite computation is\na premise. Source questions remain recorded without new answer or status claim.\nNo measurement, comparison topic or Lean declaration is added.\n\nThe accepted overview v19',1);write(W/'audit/protocol.tex',t)
 guide='''L031: characteristic-two symmetry markings
==========================================

This is the complete corrected principal recovery of Peter A. Brooksbank,
J. T. Ferrara and Dimitri Leemans, in the fixed twelve-page arXiv:1709.02219v2
edition. Exact whole-source root acceptance is bound in the admission. Public
registration requires the separate root-owned science67 integration gate.

All seven whole native papers are acquired: new support and endpoint theory (5 pages),
literal four-matrix proof (3), source interfaces (5), binary boundary (2), binary
exclusion (2), rank bound (2) and existing L011 obstruction (4). The final paper
is reused at its immutable published route; all four pages remain a proof
premise. The L011 classification application and its finite exceptional cases
are not premises here.

For every q>=4 the full larger-field construction supplies both even orthogonal
types and the odd symplectic groups. The binary existence dimensions are
exactly 3, 4 and 5, with exclusion for d>=6 under the source radical hypothesis.
The unrestricted binary intersection proposition is refuted explicitly.
The literal rank-four matrices generate Sp4(q), with full IP and a plus-type
first-three subgroup. Complete low-dimensional exclusion and the rank-five
upper bound close the spectrum. All 57 dispositions preserve the remaining
source qualifications; corrected recovery is not literal theorem equivalence.

Classical symmetry generation, Dickson/Arf and the inherited Klein/natural
module inputs remain external acquisitions. No finite computation is a proof
premise; the whole optional binary oracle and all operational scripts are
inventoried separately. Historical Magma software is unknown, not zero.
Section 7 questions remain source records, with no new answer, priority or
present-day open-status assertion. No factor, new topic or Lean claim follows.

'''
 import os
 for d in native:guide+='* `'+d['title']+' <'+os.path.relpath(d['pdf'],NATIVE)+'>`_ ('+str(d['physical_pages'])+' pages).\n'
 guide+='\n`Admission <../../../../audit/recoveries/L031/v1/admission.json>`_ and\n`source dispositions <../../../../audit/recoveries/L031/v1/author/source_map.json>`_\nretain exact scope and attribution. Root authored the binary/rank-bound papers,\nindependently reviewed by enumeration_volume. Enumeration_volume authored the\nthree new papers and earlier L011 obstruction, distinctly reviewed by root.\nThis operational publication proposal claims no independent mathematical review.\n'
 write(W/(NATIVE+'/PUBLICATION.rst'),guide)
 write(W/'scripts/check_science67_history.py',(HERE/'history_wrapper.py').read_text())
 write(W/'scripts/check_science67.py','''"""Root-gated entry into the immutable science67 publication proposal."""
from pathlib import Path
import importlib.util
def verify(root):
 root=Path(root).resolve()
 spec=importlib.util.spec_from_file_location('science67_plan',root/'audit/science67/v1/publication_plan/check.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module.verify(root,require_root=True)
''')
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['L031'],counts=dict(active=106,corrected_recoveries=67,measured=53,unmeasured=14,mathematical_pending=38,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 diff=''
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']:diff+=''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))
 write(HERE/'documentation.diff',diff);print('prepared',len(plan['files']),'logical payloads;',len(asts),'old functions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
