"""Prepare science66 wrappers privately on exact science65; root alone integrates."""
from pathlib import Path
import argparse,ast,copy,difflib,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
AUDIT='audit/science66/v1';SCIENCE='audit/recoveries/L023/v1';NATIVE='papers/recoveries/L023/v1'
BASE='710ccb5fb6fa016669871ded2ccf43495e1f2670';AUTHOR='corpus106_L023_complete_candidate';REVIEW='corpus106_L023_complete_root_review'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main(a):
 need(not(HERE/'manifest.json').exists(),'proposal frozen');repo=a.repo;W=HERE/'wrappers'
 need(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==BASE,'exact committed baseline')
 old=load(repo/'audit/corpus/latest.json');need((old['admitted_principal_originals'],old['currently_measured_originals'],old['accessible_pending_complete_recovery'])==(65,53,40),'science65')
 plan=load(HERE/'copy_plan.json');routes={r['study_path']:r for r in plan['files']}
 def logical(n):
  r=routes[n];return dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])
 def pub(n):
  if (W/n).is_file():return pin(W/n,n)
  r=next((x for x in plan['files'] if x['public_path']==n),None)
  return dict(path=n,bytes=r['bytes'],sha256=r['sha256']) if r else pin(repo/n,n)
 history={}
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py']:
  dest=AUDIT+'/previous/'+n;p=W/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/n).read_bytes());history[n]=pin(p,dest)
 write(W/(AUDIT+'/history_routes.json'),dict(base_commit=BASE,routes=history,scope='Exact science65 current pointers and nested history through programme53.'))
 asts={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'};need(len(asts)==157,'157 prior functions')
 protected=['papers/catalogue.json','scripts/build_papers.py','audit/overview/latest.json','audit/overview/v19/admission.json','audit/science65/v1/root_integration.json']+[str(p.relative_to(repo)) for p in (repo/'audit/overview/v19/packet').rglob('*') if p.is_file()]
 write(HERE/'baseline.json',dict(commit=BASE,origin_main_at_preparation=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip(),old_nonmain_ASTs=asts,history=history,old_catalogue=old['active_catalogue'],protected_files=[pin(repo/n,n) for n in protected]))
 inv=load(a.study/AUTHOR/'program_inventory.json');roles=copy.deepcopy(inv)
 for r in roles['whole_files']:r['public_binding']=logical(AUTHOR+'/'+r['path'])
 roles.update(source_software_cost=None,external_proof_cost=None,software_inclusive_factor=None,measurement=None,current_source_code_boundary='The source mentions Magma but supplies no full executable listing. Unknown historical software is not zero; optional validation requires symmetric treatment before any later factor.')
 write(W/(AUDIT+'/whole_file_roles.json'),roles)
 native=[]
 for d in load(a.study/AUTHOR/'native_acquisition.json')['documents']:
  t=(a.study/AUTHOR/d['tex']).read_text();native.append(dict(id='L023_'+d['key'],title=re.search(r'\\title\{([^{}]+)\}',t).group(1),tex=logical(AUTHOR+'/'+d['tex'])['path'],pdf=logical(AUTHOR+'/'+d['pdf'])['path'],tex_inputs=[],compiler='pdflatex',physical_pages=d['pages'],role='current source contract' if d['key']=='contract' else 'whole scientific proof component',source_ids=['L023'],topic='Wilson trialities and rank-four geometry',comparison_topic_created=False,measured=False,compression_factor=None,externaldocument_dependency=None))
 note='Complete corrected principal L023 recovery:70 dispositions,all 10 numbered source items,and all 12 finite table rows. Whole 3-page contract plus4+3+1+5+3 scientific pages are acquired. Uniform odd-PSL completion proves actual infinitely many rank-four geometries; it does not restore false unrestricted Lemma 7. Exact digonal/dihedral/Class III counterexamples,three corrected even table rows,primitivity/nonscalar limits,and ancillary borrowed Borel-parity correction stay explicit. The even Class III family and classifications remain named retained inputs. The final broad flag-transitive question is answered by attributed later Leemans–Stokes–Tranchida L015 work,not a new question claim or a completion proof premise. No theorem-set equivalence,measurement,new Lean or factor.'
 ad=dict(status='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE66_GATE',source_id='L023',source_ids=['L023'],source_author_role='Dimitri Leemans and Klara Stokes; focal-group-authored source.',principal_originals_added=1,measured=False,measurement_status='pending',compression_factor=None,software_inclusive_factor=None,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,theorem_sets_equivalent=False,author_manifest=logical(AUTHOR+'/manifest.json'),distinct_root_review_manifest=logical(REVIEW+'/manifest.json'),root_scientific_acceptance=logical(REVIEW+'/manifest.json'),source_map=logical(AUTHOR+'/source_map.json'),dependency_boundary=logical(AUTHOR+'/components.json'),source_ledger=logical(AUTHOR+'/source_map.json'),retained_inputs=logical(AUTHOR+'/retained_inputs.json'),historical_question=logical(AUTHOR+'/historical_question.json'),historical_answer_public_bindings=plan['public_dependencies'],program_roles=pub(AUDIT+'/whole_file_roles.json'),whole_scientific_manuscripts=[pub(d['pdf']) for d in native],physical_pages=[3,4,3,1,5,3],source_pages=13,source_routes=70,numbered_source_items=10,finite_table_rows=12,comparison_topic_created=False,current_measurements_changed=False,publication_gate=AUDIT+'/root_integration.json',public_mapping=AUDIT+'/publication_plan/copy_plan.json',scope_note=note,roles='Root authored cubic,polynomial and elementary components. rewrite_termination distinctly reviewed cubic/elementary and authored symmetry/completion plus this assembly/proposal. enumeration_volume reviewed polynomial. Root distinctly accepted symmetry/completion and the whole corrected contract. All earlier roles remain disclosed; no self-adjudication.',frozen_status_overlay='Exact later root complete review governs acceptance; all historical author/reviewer pending sentences remain immutable.')
 ap=SCIENCE+'/admission.json';write(W/ap,ad);admission=pub(ap);rp=AUDIT+'/new_original_registration.json'
 write(W/rp,dict(status='ROOT_ACCEPTED_CORRECTED_SCIENCE_PUBLIC_REGISTRATION_PROPOSAL',source_ids=['L023'],admissions=[admission],principal_originals_added=1,measurement_originals_added=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,comparison_topics_added=0,compression_factor=None,previous_registration=old['current_science_registration']))
 unmeasured=sorted(old['measurement_pending_original_ids']+['L023']);cat=copy.deepcopy(load(repo/old['active_catalogue']['path']))
 cat.update(status='CURRENT_ACCESSIBLE106_66_CORRECTED_RECOVERIES_53_MEASURED',admitted_principal_originals=66,currently_measured_originals=53,measurement_pending_original_ids=unmeasured,accessible_pending_complete_recovery=39,review_revision='Only L023 becomes an accepted complete corrected principal recovery;105 other records unchanged.',new_proof_credit=1,new_question_credit=0,previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=66,measured=53,measurement_pending=13,pending=39,editorial=1))
 row=next(r for r in cat['entries'] if r['original_id']=='L023');previous=copy.deepcopy(row['current_principal_recovery'])
 row['current_principal_recovery']=dict(status='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING',latest_admission_references=[admission],principal_contract_admitted=True,measured=False,compression_factor=None,whole_source_formalized=False,theorem_sets_equivalent=False,new_question_credit=0,scope=note,historical_admission_evidence=previous)
 row['next_obligation']='Any later measurement acquires the complete 19 current native pages,whole required polynomial and fixed-matrix programs,and explicit retained inputs. Historical software/external proof costs remain unknown. The current corrected source disposition governs; no literal theorem-set equivalence or new question credit.'
 cp='audit/corpus/accessible106/updates/corrected-unmeasured66-catalogue.json';write(W/cp,cat)
 c=copy.deepcopy(old);c.update(status='CURRENT_PROGRAMME_66_CORRECTED_RECOVERIES_53_MEASURED_39_PENDING_1_EDITORIAL',admitted_principal_originals=66,accessible_pending_complete_recovery=39,admitted_original_ids=sorted(old['admitted_original_ids']+['L023']),accessible_pending_original_ids=[i for i in old['accessible_pending_original_ids'] if i!='L023'],measurement_pending_original_ids=unmeasured,scientific_unmeasured_original_ids=unmeasured,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pub(cp),current_science_registration=pub(rp));c['added_admissions'].append(pub(rp));c.pop('snapshot',None)
 sp='audit/corpus/updates/accessible106-corrected-unmeasured66.json';write(W/sp,c);c['snapshot']=pub(sp);write(W/'audit/corpus/latest.json',c)
 for r in native:r['admission']=admission
 sc=load(repo/'papers/catalogue_corrected_unmeasured.json');sc['entries'].extend(native);sc['original_ids'].append('L023');sc['root_publication_gate']=AUDIT+'/root_integration.json';write(W/'papers/catalogue_corrected_unmeasured.json',sc)
 papers=load(repo/'papers/latest_catalogue.json');papers['status']='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_THIRTEEN_CORRECTED_UNMEASURED';papers['active_source_catalogue']=pub(cp);papers['corrected_unmeasured_scientific_catalogue']=pub('papers/catalogue_corrected_unmeasured.json');write(W/'papers/latest_catalogue.json',papers)
 write(HERE/'native_catalogue.json',dict(new_documents=native,complete_scientific_pages=19,compiler='pdflatex',all_whole_papers_paid=True))
 oldlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015 and L096';newlist='N014, L024, L102, F011, F008, L039, L013, L011, L025, L122, L015, L096 and L023'
 t=(repo/'README.rst').read_text().replace('**65 accessible originals','**66 accessible originals').replace('53 are measured and twelve ('+oldlist+')','53 are measured and thirteen ('+newlist+')').replace('40 await mathematical recovery;','39 await mathematical recovery;')
 insert='The `L023 guide <'+NATIVE+'/PUBLICATION.rst>`_ binds all six native documents\n(19 pages), all 70 source dispositions and twelve exact finite table rows.\nThe uniform odd-projective-linear family consists of actual geometries; false\nunrestricted construction claims remain explicitly refuted. The three even\nfinite rows and borrowed multiplier parity are corrected. The final broad\nflag-transitive question is answered by the attributed later L015 work of\nLeemans, Stokes and Tranchida, with no new question credit here. Required\nsoftware and retained classification/even-family premises remain visible.\n\nAll thirteen source editions, complete proof packets and distinct reviews are recorded'
 need('All twelve source editions, complete proof packets and distinct reviews are recorded' in t,'reader insertion');t=t.replace('All twelve source editions, complete proof packets and distinct reviews are recorded',insert).replace('None of these twelve recoveries','None of these thirteen recoveries').replace('audit/science65/v1/new_original_registration.json',rp);write(W/'README.rst',t)
 t=(repo/'audit/completion.rst').read_text().replace('**65 reviewed corrected principal recoveries**','**66 reviewed corrected principal recoveries**').replace('53 are measured and twelve ('+oldlist+') are unmeasured. There are 40 originals','53 are measured and thirteen ('+newlist+') are unmeasured. There are 39 originals').replace(oldlist+' have separate scientific admissions',newlist+' have separate scientific admissions').replace('science65/v1/new_original_registration.json','science66/v1/new_original_registration.json')
 t=t.replace('The `current overview','L023 adds its complete 19-page corrected contract/proof closure, all 70\ndispositions and twelve finite rows. Uniform odd-PSL completion, precise\ncounterexamples, corrected even counts and retained classifications are\nseparate. Its final broad question is attributed to later accepted L015,\nwith no new question credit, formalization or factor.\n\nThe `current overview',1);write(W/'audit/completion.rst',t)
 t=(repo/'audit/protocol.tex').read_text().replace('106=65\\ \\text{reviewed corrected recoveries}+40','106=66\\ \\text{reviewed corrected recoveries}+39').replace('Of the 65 corrected recoveries','Of the 66 corrected recoveries').replace(oldlist+' are scientifically accepted but unmeasured',newlist+' are scientifically accepted but unmeasured')
 t=t.replace('The accepted overview v19','L023 acquires the complete three-page current contract and five whole\nscientific components of four, three, one, five and three pages. All 70\nsource dispositions and twelve finite rows are explicit. The odd-PSL family\nis uniformly completed; false unrestricted assertions remain refuted.\nIts broad final question is answered by separately attributed later L015\nwork, without new question credit. Required code and retained classifications\nremain visible. No comparison topic or factor is created.\n\nThe accepted overview v19',1);write(W/'audit/protocol.tex',t)
 guide='''L023: maps with Wilson trialities and corrected geometries
===========================================================

This is the complete corrected principal recovery of Dimitri Leemans and
Klara Stokes, fixed arXiv:2208.08215v2 (9 September 2022), thirteen source pages.
Root scientific acceptance is bound in the admission. Public registration
requires the separate root-owned science66 integration gate.

All six whole native documents are acquired: current contract 3, cubic generation 4,
polynomial equations 3, elementary boundary 1, symmetry/counterexamples 5 and uniform
odd-PSL completion 3 pages. No component is an unpaid citation. The source's false
unrestricted Lemma 7 is refuted even by a faithful Class III map; actual infinitely
many geometries are established separately. Dihedral/digonal exceptions, the
three even table corrections, primitive/nonscalar qualifications and ancillary
borrowed Borel parity correction remain explicit. This recovery includes corrections; it does not assert that every original
statement is true.

The final broad flag-transitive existence question is answered by the accepted
later L015 work of Dimitri Leemans, Klara Stokes and Philippe Tranchida, including
its separately accepted generation repair. This is an attributed later answer,
not a new question credit or premise of the odd-PSL completion proof.

The whole polynomial GAP program and fixed SL2(8) Python certificate are required.
All other optional diagnostics and operational runners are inventoried. Retained
classification/even-family inputs and source Magma costs are not assumed zero.
No primary source PDF/text is redistributed. No new numerical factor, measured
original, comparison topic or Lean declaration follows.

'''
 for d in native:guide+='* `'+d['title']+' <'+str(Path(d['pdf']).relative_to(NATIVE))+'>`_ ('+str(d['physical_pages'])+(' page' if d['physical_pages']==1 else ' pages')+').\n'
 guide+='\n`Admission <../../../../audit/recoveries/L023/v1/admission.json>`_ and\n`source dispositions <../../../../audit/recoveries/L023/v1/author/source_map.json>`_\nretain the exact accepted scope and attribution.\n'
 guide+='\nRoot authored cubic/polynomial/elementary pieces; rewrite_termination reviewed\ncubic/elementary and authored symmetry/completion/current assembly/proposal.\nEnumeration_volume reviewed polynomial; root distinctly reviewed the new\nsymmetry/completion and complete corrected contract. No self-acceptance.\n'
 write(W/(NATIVE+'/PUBLICATION.rst'),guide)
 write(HERE/'registration_proposal.json',dict(status='PRIVATE_PROPOSAL_ROOT_INTEGRATION_REQUIRED',base_commit=BASE,new_originals=['L023'],counts=dict(active=106,corrected_recoveries=66,measured=53,unmeasured=13,mathematical_pending=39,editorial=1,archived=55,comparison_topics=19),corpus_pointer=pub('audit/corpus/latest.json'),active_catalogue=pub(cp),snapshot=pub(sp),papers_pointer=pub('papers/latest_catalogue.json'),new_registration=pub(rp),admission=admission,unchanged_measurement_overview='audit/overview/v19/admission.json',new_factors=0,root_integration_route=AUDIT+'/root_integration.json'))
 diff=''
 for n in ['README.rst','audit/completion.rst','audit/protocol.tex','papers/latest_catalogue.json']:diff+=''.join(difflib.unified_diff((repo/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='old/'+n,tofile='proposed/'+n))
 write(HERE/'documentation.diff',diff);print('prepared',len(plan['files']),'payloads;',len(asts),'old functions')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study',required=True,type=Path);p.add_argument('--repo',required=True,type=Path);main(p.parse_args())
