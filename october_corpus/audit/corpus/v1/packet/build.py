#!/usr/bin/env python3
"""Reconcile all fixed 161 original IDs; never infer access from a filename alone."""
from pathlib import Path
import argparse,collections,csv,hashlib,json,re,subprocess,unicodedata
from pypdf import PdfReader
SHA=lambda b:hashlib.sha256(b).hexdigest()
P=Path(__file__).resolve().parent
TOPICS={
'A':(['L032','L034','F013','F016','L035','N009'],'topic-a'),
'B':(['N001','N003','N008','L030'],'topic-b'),
'C':(['L088','N013','L108','F014'],'topic-c'),
'D':(['L066','L074','L104'],'topic-d'),
'E':(['L083','L079','L021'],'topic-e'),
'Affine':(['L012'],'topic-affine'),'F':(['L014'],'topic-f'),
'G':(['L009','L092'],'topic-g'),'Representation':(['F010'],'topic-representation'),
'Chamber':(['L008','N016'],'topic-chamber')}
OVERRIDES={
'L009':['sources/linear_triality2026_published.pdf'],
'L028':['sources/phase282_L028_revised.pdf'],
'L029':['sources/phase276_residual_chiral_published.pdf'],
'N001':['sources/phase16_N001_browser_record.txt'],
'L108':['sources/phase25_L108_rendered_primary.txt'],
'N003':['sources/network_independent_generators.pdf'],
'N005':['corpus161_inventory_v1/private_sources/N005_arxiv2505.24662v1.html'],
'N006':['sources/phase283_geometry_wreath.pdf'],
'N007':['sources/phase283_j_diagonals.pdf'],
'N008':['sources/phase16_frattini_geometries.pdf'],
'N009':['sources/phase17_gomi_loyola2018.pdf'],
'N010':['sources/phase18_schulte_weiss_2006.pdf'],
'N011':['sources/phase20_markovskaya_nuzhin2025.pdf'],
'N012':['sources/phase22_markovskaya_thesis.pdf'],
'N013':['sources/phase26_montero_weiss2020.pdf'],
'N014':['sources/phase27_halving_current_arxiv.pdf'],
'N016':['phase57_ten_source_measurement_sources/N016.pdf']}
LATER={
'L028':('full_author_candidate_pending_independent_review',['phase282_manifest.json','phase282_scope.json','phase282_source_ledger.json','phase282_proof_map.json'],'Complete corrected connected chiral-enumeration theory, exact algorithm/orbits and declared classification outputs; no empirical timing replay.','Independent complete review of phase282 and its revised source, then canonical admission if accepted.'),
'F015':('full_author_candidate_pending_independent_review',['phase278_manifest.json','phase278_contract.json','phase278_source_ledger.json'],'All eight matching/halved families; corrected 120-cell presentation requires twenty extra orbital relations, with literal-source infinitude separately proved.','Independent complete review of phase278, retained construction inputs and all exceptional orbit completeness.'),
'L029':('partial_replacement_with_explicit_remaining_lemma',['phase276_manifest.json','phase276_contract.json','phase276_source_ledger.json'],'Thin C+-geometry chamber-component reduction and full rank-three conclusion; seven-object auxiliary counterexample is outside main hypotheses.','Prove or refute the principal all-rank exclusion of additional gallery components, equivalently A=G; do not promote the component reduction.'),
'L059':('partial_replacement_historical_census_unpaid',['phase177_export.json','phase177_L059_contract.json','phase177_rank_two_graphs.md'],'Complete faithful-marking classification over a fixed bipartite graph and a new 69-marking bounded census.','Recover the historical cubic/quartic input lists, all printed Max/Norm table cells and M12 witness; new five-graph census is not a substitute.'),
'L126':('partial_corrected_replacement',['phase197_positive_manifest.json','phase197_source_contract.json','phase196_manifest.json','phase197_review196_export.json'],'Recognizable extensions recover declared positive families; projective tuple twins and free-basis symmetries require explicit source corrections.','Reconcile every source principal family with phase197; complete corrected projective faithfulness/field-selection replacement and independent whole-contract review.'),
'L068':('admitted_corrected_source_component',['phase179_manifest.json','phase179_L068_contract.md','phase179_source_ledger.json','research/case_study/phase189_L068_overlay.json'],'Independently accepted literal P and explicitly repaired Q, both stabilizer lattices and full17-row graph-object bridge; literal Q is not a geometry.','Rework accepted complete corrected proof into a canonical source application; retain source correction and exact17-row boundary. No new mathematical rederivation is needed for already accepted clauses.'),
'L073':('partial_census_with_source_table_gap',['phase164_enumeration_ledger.json','research/case_study/phase181_registry_overlay.json','phase180_export.json','phase180_failure_inventory.json'],'Numerical M22 census and geometric shadow reconstruction; literal source-label/table matching is a separate contract.','Complete exact old-label/subscript-to-shadow table matching and all remaining named row invariants; numerical agreement alone is insufficient.'),
'N006':('no_replacement',['sources/phase283_geometry_wreath.pdf','sources/phase283_geometry_wreath.txt'],'Twisting and wreath-product geometry preservation under exact admissibility; sporadic almost-simple examples.','Read all theorem hypotheses/proofs and classify required finite examples; reuse typed-Helly and action reconstruction only through proved interfaces.'),
'N007':('no_replacement',['sources/phase283_j_diagonals.pdf','sources/phase283_j_diagonals.txt'],'Pair-orbit Coxeter j-diagonal twisting, regular-hypertope preservation, finite tree diagrams and extension operation.','Recover each construction and finiteness/regularity assertion from exact presentation and parabolic intersection hypotheses; previous stopped status is obsolete as a goal boundary.')}
MANUAL_TARGETS={
'L003':('Toroidal extensions','All principal hexagonal-extension constructions and their geometric realizations, in addition to the separately answered source questions.','Reconcile all source tables/families; previously proved universal-group and finite-existence answers do not replace the whole main-result contract.'),
'L043':('E: projective matrix and field-orbit theory','Complete regular/chiral PSL2 classification in all source field cases; Conjectures6.1/6.2 remain separate previously addressed targets.','Reuse primitive-character, subfield/transvection and trace proofs; recover every published principal classification branch and audit exact retained Dickson inputs.'),
'L031':('Orthogonal reflection and supported kernels','All-rank orthogonal characteristic-two string C-group constructions with exact field/rank/label hypotheses.','Verify generation and full parabolic intersections for every printed parameter range; finite proper-torus failures show that full-torus hypotheses cannot be silently weakened.'),
'L038':('Permutation string constructions','Complete alternating-group rank spectrum and construction ranges.','Recover the source marked permutations, generation, full IP and rank bounds; no extrapolation from conditional generic mechanisms.'),
'L050':('Codes from graph adjacency','All stated LCD code constructions, parameters and classification/comparison tables from McLaughlin subgraphs.','Reuse the existing algebraic hull criterion, then pay every graph identification, rank/distance computation and parameter-table claim.'),
'L063':('D/E: rank-two subgroup geometry enumeration','Complete second-part PSL2 rank-two geometry classification and its case tables; L064 is a separately indexed appendix.','Recover all subgroup-pair orbits, invariant columns and table labels; generic orbit encoding is not a full census.'),
'L076':('D/E: rank-two subgroup geometry enumeration','Complete first-part PSL2 rank-two classification and all stated parameter families.','Audit the full source and exact classification boundary, then share subgroup/fiber theory with L063/L064 without ignoring exceptional cases.'),
'L071':('Marked-action orbit enumeration','All correctness/exhaustiveness results and declared exact regular-polytope classification outputs for fixed automorphism groups.','Compare with existing marked-coordinate/orbit proof bank and L028; retain exact old outputs and separate timings from mathematical coverage.'),
'L046':('Marked-action orbit enumeration','Exact regular-map enumeration algorithm, equivalences and declared classifications.','Read full algorithm proof and enumerate its actual outputs, not just generic pairs-of-generators theory.'),
'L096':('Intersection recognition','The full recursive intersection-property algorithm and its correctness/results.','Prove the precise recursion and all stated outputs from existing intersection lemmas; current generic encoding is not full recovery.'),
'L110':('D: arbitrary-Borel Suzuki recognition','All eleven high-rank RWPRI pre-geometry constructions and exhaustive classification.','Reuse arbitrary-Borel generation/recognition components, but finish all subgroup configurations, rank cases and source table identifications.'),
'L114':('D: Suzuki subgroup fibers','Complete rank-three Suzuki geometry classification with all parameter/orbit cases.','Reconcile previously proved corrections and partial enumeration with the full main classification; source question answers do not pay the classification.'),
'L115':('D: Suzuki subgroup fibers','Complete rank-two Suzuki geometry classification.','Replace the existing finite sampled subfamily by all subgroup-pair types, conjugacy equivalence, field subgroups and exact parameter counts.'),
'L128':('Representation and diagram actions','Realize arbitrary finite prescribed diagram-symmetry groups by regular hypertopes.','Read the exact source main theorem and construction; prove recognition, intersection/geometry and full symmetry upper bound rather than mere group embedding.'),
'F003':('E/D: projective and Suzuki centralizers','The all-parameter rank-three bound for chiral Suzuki polytopes.','Recover the complete short historical theorem with its exact generation/centralizer hypotheses; this historically answers the prior question and is not new conjecture credit.'),
'F005':('Supported kernels and cover intersections','Necessary and sufficient polytopality criteria for mixes of polytopes/maniplexes.','Read full criteria, prove actual intersection equivalences and all examples using existing kernel-product theory; preserve any converse restrictions.'),
'F006':('Reflection groups and rank spectra','Exact abstract-regular-polytope ranks for the finite irreducible Coxeter groups.','Recover every classical/exotic marking, classification and exceptional rank case; do not replace with a mere bound.'),
'F007':('Chamber/flag kernels','Full faithfulness characterization for maniplexes and principal constructions/counterexamples.','Read exact all-rank hypotheses and relate flag-kernel interfaces to each principal statement; no blanket polytopality assumption.'),
'N005':('Coset operations and typed Helly','Free products, compatible amalgams, admissible HNN and semidirect/twisting geometry preservation; complete stated applications to Shephard/Artin-Tits constructions.','Bind one exact edition, read all proof hypotheses and pay normal-form and application arguments. The HTML version stamp and rendered internal date differ; do not infer a revised priority date.'),
'N014':('C: parity-compatible halving','Complete generalized halving construction, geometric preservation and toroid applications, under exact corrected parity conditions.','Reconcile the broad v1 residual-connectivity counterexample with the intended positive theorem and later source edition; complete principal applications before full credit.'),
'N010':('Multi-topic problem survey','All mathematical statements and open-problem statuses across this survey; Problem30 progress is only a component.','Inventory every numbered problem with current evidence; do not mark the original fully replaced because a few problems are answered.'),
'N011':('Linear reflection generation','Both general GL/PGL three-involution generation theorems in their exact dimensions and fields.','The source theorem is currently retained; independently rederive all stated matrix cases and polytope adapters before claiming compression.'),
'N012':('Linear reflection generation','Complete thesis principal generation and regular rank-three polytope results over finite fields and integers.','Read full theorem structure and proofs; existing selected-page retention is not a thesis replacement.'),
'L120':('Multi-topic classification survey','All survey classifications, constructions and open-question status, with source theorem origins preserved.','Separate summarized old results from new survey claims; full statement/proof/retained-input closure remains unpaid.'),
'L022':('Commemorative preface','Complete two-page authored editorial; no new mathematical principal theorem has been identified.','Retain this original in the 161 accounting, explicitly classify its editorial content, and avoid manufacturing a theorem-compression credit.')}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--public',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();study=a.study;public=a.public;out=a.out;out.mkdir(parents=True,exist_ok=True)
 regpath=public/'audit/source_registry.json';reg=json.loads(regpath.read_text());lit=json.loads((public/'research/case_study/literature_inventory.json').read_text());litmap={x['id']:x for x in lit['entries']};completion=json.loads((public/'audit/completion.json').read_text());contracts={x['source_id']:x for x in completion['contracts']}
 additional_authors={}
 for fn in ['phase6_network_intake.json','phase16_frattini_geometry_intake.json','phase17_k1_source_intake.json','phase18_schulte_weiss_intake.json','phase20_linear_rank3_intake.json']:
  path=study/fn
  if not path.exists():continue
  j=json.loads(path.read_text())
  for row in j.get('rows',[]):
   if row.get('authors'):additional_authors[row['id']]=row['authors']
 additional_authors.update(N001=['F. Buekenhout','P. Cara'],N002=['P. Cara','S. Lehman','D. V. Pasechnik'],N003=['P. J. Cameron','P. Cara'],N008=['Claude Archer','Philippe Cara','Jan Krempa'],N009=['Yasushi Gomi','Mark L. Loyola','Ma. Louise Antonette N. De Las Peñas'],N010=['Egon Schulte','Asia Ivić Weiss'],N011=['Irina A. Markovskaya','Yakov N. Nuzhin'],N012=['Irina A. Markovskaya'],N013=['Antonio Montero','Asia Ivić Weiss'],N014=['Claudio Alexandre Piedade','Philippe Tranchida'],N015=['Wei-Juan Zhang'],N016=['Gabe Cunningham'])
 inputs={};pdfcache={};bad=[];rows=[]
 annotations=json.loads((P/'source_reading_annotations.json').read_text())['entries']
 def binding(ns,path):
  root=study if ns=='study' else public;p=root/path
  if not p.is_file():return None
  b=p.read_bytes();r={'namespace':ns,'path':str(path),'bytes':len(b),'sha256':SHA(b)};inputs[ns,str(path)]=r;return r
 def evidence(path,role):
  opts=[('public',path),('study',path.removeprefix('research/case_study/')),('public','research/case_study/'+path)]
  for ns,x in opts:
   r=binding(ns,x)
   if r:return dict(r,role=role)
  return {'path':path,'role':role,'available_local':False,'archive_note':'Historical registry path; absent current file, archive/private resolution remains explicit.'}
 def source(path,id,origin):
  p=study/path;r=binding('study',path)
  if not r:return None
  b=p.read_bytes()
  if path.endswith('.pdf'):
   if not b.startswith(b'%PDF-'):bad.append(dict(r,claimed_id=id,reason='not_pdf_magic'));return None
   if str(p) not in pdfcache:
    try:
     reader=PdfReader(p);texts=[x.extract_text() or '' for x in reader.pages];pdfcache[str(p)]={'pages':len(texts),'texts':texts}
    except Exception as e:bad.append(dict(r,claimed_id=id,reason='parser_failure',detail=str(e)));return None
   cache=pdfcache[str(p)];txt=cache['texts'][0];refs=[]
   for i,t in enumerate(cache['texts']):
    for m in re.finditer(r'(?m)^\s*(Theorem|Proposition|Corollary|Lemma|Problem|Conjecture)\s+([A-Z]|\d+(?:\.\d+)*)(?:\.|\b)',t):
     label=m.group(1)+' '+m.group(2)
     if not any(z['label']==label for z in refs):refs.append({'label':label,'physical_page':i+1,'reading_status':'machine_located_not_all_manually_read'})
   edition=re.search(r'arXiv\s*:\s*([\w./-]+(?:v\d+)?)',txt)
   return dict(r,representation='primary_pdf',usable=True,identity_basis=origin,pages=cache['pages'],edition_mark=edition.group(1) if edition else None,first_page_text_sha256=SHA(txt.encode()),machine_located_named_statements=refs)
  representation='complete_authored_browser_rendering' if id in ['N001','L108'] else 'primary_publisher_html' if id=='L022' else 'primary_arxiv_html' if id=='N005' else 'retained_source_text'
  z=dict(r,representation=representation,usable=True,identity_basis=origin,pages=None,edition_mark=None,machine_located_named_statements=[])
  if id=='N001':z.update(authored_body_lines=[181,220],body_scope='All seven article pages, eleven references and addresses; lines221 onward repeat a website widget and are not source body.',original_pdf_available=False)
  if id=='L108':z.update(authored_body_lines=[1,36],body_scope='All seven article pages, references and addresses.',original_pdf_available=False)
  if id=='N005':z.update(source_url='https://arxiv.org/html/2505.24662v1',edition_mark='arXiv2505.24662v1; page header May30,2025; rendered internal date August24,2026',access_evidence='Fresh legitimate full HTML retrieval 2026-10-11; body has six sections and references. No edition-priority inference.')
  return z
 for old in reg['entries']:
  id=old['id'];entry=litmap.get(id,{});assets=[]
  for p in OVERRIDES.get(id,[]):
   s=source(p,id,'Exact later scoped proof/input binding or freshly checked actual primary identity')
   if s:assets.append(s)
  for x in entry.get('assets',[]):
   fn=x.get('filename')
   if fn and fn not in [s['path'] for s in assets]:
    s=source(fn,id,'Immutable intake asset, title identity previously audited; fresh actual bytes/PDF parse')
    if s:
     s['intake_expected_sha256']=x.get('sha256');s['matches_intake_hash']=s['sha256']==x.get('sha256');s['source_url']=x.get('url');assets.append(s)
  accessible=bool(assets)
  citation=old['citation'];authors=additional_authors.get(id)
  if authors is None:
   if id.startswith('L'):
    pre=citation.split(old['title'])[0].strip()
    co=pre.removeprefix('with ').strip(' ,') if pre.startswith('with ') else ''
    authors=['Dimitri Leemans']+([co] if co else [])
    author_basis='Catalogue citation; coauthor string retained exactly without guessing full-name expansions.'
   else:
    pre=re.split(r'\(\d{4}\)',citation)[0].strip(' .');authors=[pre] if pre else [];author_basis='Original intake bibliographic citation; exact names/initials retained.'
  else:author_basis='Named source/intake bibliography; authorship not inferred from network membership.'
  if len(authors)==1 and id.startswith('F'):authors=[x.strip() for x in re.split(r',?\s+and\s+|,\s*',authors[0]) if x.strip()]
  elif id.startswith('L') and len(authors)>1:authors=authors[:1]+[x.strip() for x in re.split(r',?\s+and\s+|,\s*',authors[1]) if x.strip()]
  ev=[evidence('research/case_study/literature_inventory.json','immutable intake identity'),evidence('audit/source_registry.json','historical status snapshot')]
  proofev=[]
  for e in old.get('evidence',[]):
   if e['file'].endswith('literature_inventory.json'):continue
   proofev.append(evidence(e['file'],e.get('kind','prior proof evidence')))
  topic=None;slug=None
  for t,(ids,s) in TOPICS.items():
   if id in ids:topic=t;slug=s
  contract=contracts.get(id);later=LATER.get(id)
  if contract:
   status='full_admitted_principal_contract';summary=contract['current_contract_summary'];nextwork='Preserve the exact admitted main-result contract and its source corrections; compare every remaining original principal claim before any broader whole-assertion claim. Source-specific complete Lean formalization remains separately scoped.'
   for path in [f'audit/{slug}/v2/admission.json',f'papers/{slug}/v2/scope.json',f'papers/{slug}/v2/source_contract_map.json',f'audit/{slug}/v2/formal_inventory.json']:
    if (public/path).is_file():proofev.insert(0,evidence(path,'current canonical proof/contract admission'))
  elif later:
   status,paths,summary,nextwork=later
   proofev=[evidence(p,'later proof packet superseding stale registry label') for p in paths]+proofev
  elif old['encoded'] or old['rederived'] or old['status'] in ['proposed_new_result','partial_progress','conditional_component','generic_encoding','finite_subfamily_reproduced']:
   status='partial_or_question_only_existing_proof';summary='; '.join(t.get('reference','')+': '+t.get('scope','') for t in old['exact_target']);nextwork='; '.join(old.get('remaining_work',[])) or 'Define and recover the complete original principal contract; existing components or question answers do not constitute full recovery.'
  else:
   status='no_replacement';summary=None;nextwork='Read exact principal statements and all required proof inputs; choose a complete recovery contract and test a shared-theory route.' if accessible else 'Obtain or locate a usable complete original; read its exact principal statements. This remains a target, not an excluded manuscript.'
  grouping=topic or 'unassigned_pending_source_reading'
  explicit=MANUAL_TARGETS.get(id)
  if explicit:grouping,target,nextwork=explicit
  elif contract:target=contract['current_contract_summary']
  elif later:target=later[2]
  elif old['exact_target']:target='Existing assessed component: '+'; '.join(t.get('reference','') for t in old['exact_target'])+'. Full principal statement audit remains pending.'
  else:target=None
  mpath=f'audit/{slug}/v2/measurement/admission.json' if slug else None
  if topic=='E':mpath='audit/topic-e/v2/measurement_admission.json'
  measurement={'status':'not_measured_for_complete_replacement','admission':None,'unknown_external_costs':True,'node_count_factor_forbidden':True}
  if mpath and (public/mpath).is_file():measurement.update(status='existing_topic_whole_document_audit_with_exact_contract_and_sensitivities',admission=binding('public',mpath),source_original_pdf_missing=id in ['N001','L108'],scope_note='Read exact policy; printed programmes separate from written comparison, conditional source/application prepays full topic common theory. No new factor calculated here.')
  if id in ['N001','L108']:measurement.update(status='original_PDF_absent_full_authored_rendering_accessible_additive_measurement_pending',source_original_pdf_missing=True)
  row={'original_id':id,'authors':authors,'author_evidence':author_basis,'title':old['title'],'year':old['year'],'year_evidence':'Frozen bibliography; null means unverified publication year, not undated source','edition':assets[0].get('edition_mark') if assets else None,'citation':citation,'origin':old['origin'],'unique_original_count':1,'genuine_duplicate_original_id':None,'source_access':{'accessible':accessible,'usable_representations':assets,'historical_access':old['access_coverage'],'source_urls':old['primary_urls'],'pending_retrieval':not accessible,'public_primary_redistribution':False},'principal_results_to_recover':{'summary':target,'scope_status':'existing_accepted_main_contract' if contract else 'bounded_source_or_proof_packet_target' if target else 'principal_statement_reading_pending','machine_statement_candidates':assets[0].get('machine_located_named_statements',[]) if assets else [],'complete_source_proof_read_in_this_inventory':False,'prior_reading_evidence':old['access_coverage']},'proof':{'status':status,'current_complete_canonical_topic':topic,'principal_contract_admitted':bool(contract),'all_original_assertions_claimed':False,'summary':summary,'evidence':proofev,'historical_status_label':old['status'],'historical_remaining_work_not_silently_adopted':old.get('remaining_work',[])},'proposed_theory_or_block':grouping,'measurement':measurement,'next_obligation':nextwork,'target_remains_active':True,'metadata_and_evidence':ev}
  row['proof']['component_acceptance_note']='Main-contract admission explicitly bound.' if contract else 'Exact existing packet evidence is bound; this inventory does not independently reaccept every partial proof or establish novelty.'
  if old['status']=='generic_encoding' and not contract and not later:row['proof']['status']='encoding_only_no_complete_replacement_proof'
  elif old['status']=='conditional_component' and not contract and not later:row['proof']['status']='conditional_component_missing_source_specific_hypotheses'
  annotation=annotations.get(id)
  if annotation:
   row['principal_results_to_recover'].update(summary=annotation['principal_summary'],scope_status='bounded_primary_statement_reading_not_proof_recovery',inventory_reading=annotation)
   row['proposed_theory_or_block']=annotation['proposed_theory'];row['next_obligation']=annotation['next_obligation']
   if annotation.get('edition'):row['edition']=annotation['edition']
   if annotation.get('year'):
    row['year']=annotation['year'];row['year_evidence']=annotation['year_kind'];row['historical_bibliographic_year']=old['year']
  if not row['edition']:
   row['edition']='Exact retained source bytes bound below; publisher/preprint edition label pending bibliographic verification.' if accessible else 'Complete source edition unavailable; frozen bibliographic citation retained.'
  if accessible:
   row['programme_status']='admitted_main_contract_with_scoped_formal_and_measurement_work' if contract else 'pending_principal_recovery_compression_and_measurement'
  else:row['programme_status']='pending_complete_source_retrieval_then_recovery_compression_and_measurement'
  row['source_access']['availability_evidence_category']='complete_original_available' if accessible else 'prior_failed_fulltext_search' if 'after_search' in old['access_coverage']['retrieval_status'] else 'only_partial_primary_or_preview_retained_complete_body_unlocated'
  row['source_access']['fresh_unavailability_exhaustion_claim']=False
  row['formalization_status']='Existing scoped declarations only; full source-specific Lean obligations must be identified and completed separately.'
  row['principal_results_to_recover']['bibliographic_target_if_unread']=None if row['principal_results_to_recover']['summary'] else 'Recover the main results of '+row['title']+'; exact theorem statement reading remains pending, with no theorem invented from the title.'
  rows.append(row)
 # Reject tempting filename-based false positives explicitly.
 for id in ['L004','L049','L051','L053','L055','L057','L061','L065','L072','L085','L089','L097','L098','L101','L111','L116','L123']:
  paths=[f'sources/catalogue_{id}.pdf'] if id!='L085' else ['sources/phase5_L085.pdf','sources/phase5_L085_ulb.pdf']
  for path in paths:
   b=binding('study',path)
   if not b:continue
   raw=(study/path).read_bytes()
   if not raw.startswith(b'%PDF-'):bad.append(dict(b,claimed_id=id,reason='HTML/error/empty response under PDF filename'))
   else:
    actual='L104' if id in ['L097','L098','L101'] else 'L110' if id=='L123' else None
    if actual:bad.append(dict(b,claimed_id=id,reason='Actual first-page title is a different original',actual_original=actual))
 stats={'original_ids':len(rows),'accessible_originals':sum(x['source_access']['accessible'] for x in rows),'unavailable_originals_still_targets':sum(not x['source_access']['accessible'] for x in rows),'proof_statuses':dict(collections.Counter(x['proof']['status'] for x in rows)),'historical_registry_accessible':reg['counts']['retrieved_full_text'],'newly_resolved_access_ids':[x['original_id'] for x in rows if x['source_access']['accessible'] and not x['source_access']['historical_access']['retrieved_full_text']],'previous_access_missing_local_ids':[x['original_id'] for x in rows if not x['source_access']['accessible'] and x['source_access']['historical_access']['retrieved_full_text']],'with_primary_PDF':sum(any(s['representation']=='primary_pdf' for s in x['source_access']['usable_representations']) for x in rows),'non_PDF_full_originals':[x['original_id'] for x in rows if x['source_access']['accessible'] and not any(s['representation']=='primary_pdf' for s in x['source_access']['usable_representations'])],'genuine_duplicate_ids_confirmed':[],'accessible_pending_complete_recovery':sum(x['source_access']['accessible'] and not x['proof']['principal_contract_admitted'] for x in rows),'available_principal_targets_with_summary':sum(x['source_access']['accessible'] and bool(x['principal_results_to_recover']['summary']) for x in rows)}
 result={'schema':'human_compression.all161_original_inventory.v1','status':'AUTHOR_RECONCILIATION_PENDING_INDEPENDENT_REVIEW','as_of':'2026-10-11','scope':'All immutable 161 indexed originals remain targets. Access, existing proof scope, measurement and pending reading are independent axes. A full admitted principal contract is not every-assertion equivalence or full Lean formalization.','snapshot_commit':subprocess.check_output(['git','-C',str(public),'rev-parse','HEAD'],text=True).strip(),'statistics':stats,'entries':rows,'rejected_source_artifacts':bad,'immutable_inputs':list(inputs.values()),'original_identity_qualifications':[{'ids':['L007','L127'],'status':'distinct_indexed_titles_not_merged','reason':'Accepted17-page chiral3-polytope source is not a substitute for separately listed13-page tight-polyhedron preprint.'},{'ids':['L063','L064'],'status':'article_and_separately_indexed_appendix','reason':'Count each original once; do not infer a duplicate edition from shared authors/title stem.'},{'ids':['L097','L098','L101','L104'],'status':'mislabelled_duplicate_downloads_not_duplicate_originals','reason':'The first three catalogue files contain the L104 J2 article; their intended originals remain retrieval targets.'},{'ids':['L123','L110'],'status':'mislabelled_duplicate_download_not_duplicate_original','reason':'The L123-named artifact contains L110, not the indexed Sz8 paper.'}],'new_source_credit':0,'new_question_credit':0,'new_ratios':None}
 (out/'inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 with (out/'inventory.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['id','year','authors','title','accessible','source_representation','primary_path','source_sha256','proof_status','topic_or_block','principal_target','measurement_status','next_obligation']);w.writeheader()
  for x in rows:
   s=x['source_access']['usable_representations'];first=s[0] if s else {};w.writerow({'id':x['original_id'],'year':x['year'],'authors':'; '.join(x['authors']),'title':x['title'],'accessible':x['source_access']['accessible'],'source_representation':first.get('representation'),'primary_path':first.get('path'),'source_sha256':first.get('sha256'),'proof_status':x['proof']['status'],'topic_or_block':x['proposed_theory_or_block'],'principal_target':x['principal_results_to_recover']['summary'],'measurement_status':x['measurement']['status'],'next_obligation':x['next_obligation']})
 (out/'summary.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
