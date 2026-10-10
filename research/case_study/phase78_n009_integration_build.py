#!/usr/bin/env python3
"""Assemble a NEW manuscript; frozen predecessor files are read only."""
import copy, hashlib, json, re
from pathlib import Path
R=Path(__file__).resolve().parent
BASE='phase65_petrial_integration_manuscript.md'
BASE_SHA='6d302a2e7c696c916de97d2deef409c3053879999539be99a3fe72c9506205a1'
OUT='phase78_n009_integration_manuscript.md'
sha=lambda b:hashlib.sha256(b).hexdigest()
old=(R/BASE).read_text();assert sha((R/BASE).read_bytes())==BASE_SHA
s=old;edits=[]
def replace(a,b,label):
 global s
 assert s.count(a)==1,(label,s.count(a));s=s.replace(a,b);edits.append(dict(id=label,old_sha256=sha(a.encode()),new_sha256=sha(b.encode())))
def replace_between(a,b,new,label):
 start=s.index(a);end=s.index(b,start);replace(s[start:end],new,label)
replace('L035, F013, F016, L088, N013, N016 and L108.','L035, F013, F016, L088, N013, N016, L108 and N009.','intake')
replace('order-256 and J1 subgroup catalogues, Danzer\'s general construction, the stated','J1 subgroup catalogue, Danzer\'s general construction, the stated','intro_catalogue_removal')
replace('The amalgam normal-form theorem and completeness of the SmallGroups\norder-256 catalogue are retained. The **relation-pattern census derived\nfrom that catalogue** is a separately charged finite verification, not\nanother unnamed classification assumption. No main target from the four\nsource papers is accepted as background.',
'The amalgam normal-form theorem is retained. NQ\'s universal nilpotent quotient algorithm and exact finite-group/coset algorithms are retained for the new parameterized kernel census and presentation recognition. Theorem Q5.5 supplies the finite bound and Theorem Q5.6 supplies search completeness; no SmallGroups catalogue is an input. The standard string-IP criteria, finite square-quotient classification, universal geometric interpretation and infinite marked decomposition quoted by N009 are retained in their exact forms in §24. No target classification is accepted as its own background.','retained_dependency_delta')
core=(R/'phase78_n009_integration_core.md').read_text();cut=core.index('### A single finite-kernel classification')
replace('**Lemma O0 (chamber galleries and residue stabilizers).**',core[:cut]+'\n**Lemma O0 (chamber galleries and residue stabilizers).**','K_d_exact_quotient_extension')
replace('## 12. Bounded cyclic cores and all binary extension models',core[cut:]+'\n## 12. Bounded cyclic cores and all binary extension models','uniform_kernel_classifier')
seed='''**The bounded seed for the third branch.** The same universal-kernel theorem used for the order-1024 classification gives the following finite fact: every order-256 marked string C-group of type \\(\\{4,8\\}\\), with \\(r=bc,d_0=(ab)^2\\), satisfies exactly one row.

| Row | Relation pattern | Ordered marked classes |
|---|---|---:|
| I | \\([a,r^2]^2=1,\\ [a,r^4]=1\\) | 1 |
| II | \\([a,r^2]^2=r^4,\\ [a,r^4]=1\\) | 1 |
| III | \\([d_0,r^2]=r^4\\) | 1 |
| IV | \\([(r^2)^a,r]=r^4\\) | 1 |

Apply Theorems Q5.5–Q5.6 with d=3 and k=3. The universal class-five group has order 2¹⁸ and third lower-central subgroup of order 2¹³. Its invariant index-two ladder has 7, 23 and 61 kernels. Testing all 64 subset pairs for each final candidate gives 37 ordered IP markings, four with the indicated orientation of type {4,8}. Appendix A evaluates every displayed word on all four and verifies that each belongs to exactly one row, one marking per row. Section 24.3 states the complete output and the shared finite-search proof. Thus this bounded input is now conditional on exact GAP/NQ algorithms, with no abstract-group catalogue. The former SmallGroups identifiers and anchored multiplicities remain historical records in the unchanged predecessor, and are unnecessary for the relation implications used below.

'''
replace_between('**The bounded seed for the third branch.**','**Third-branch lifts.**',seed,'replace_catalogue_seed_with_shared_ladder')
branch=(R/'phase78_n009_integration_branch.md').read_text().replace('Use the common affine model of §9, in coordinates','Use the common affine model of §9 after reversing its endpoints and conjugating all three generators by b. Since the lattices are invariant under the coordinate swap, the same square and diagonal quotients have coordinates')
replace('## 24. Every source result as an explicit corollary',branch+'\n## 25. Every source result as an explicit corollary','new_N009_branch')
replace('## 25. Shared proof, retained costs and source boundaries','''**Corollary N7 — N009 principal classification and constructive statements.** The nondegenerate string C-groups of order 1024 comprise one rank-two, 125 rank-three, 105 rank-four and eight rank-five generator-set classes. Their type counts, all 107 named end-pair rows, the 106 finite universal orders and the two exceptional presentations are as recorded in §24 and Appendices F–G. The central-quotient and relator-lift mechanisms hold with the order-eight terminal boundary. The three Table 4 right-hand sides and four Table 6 orientation spellings have the stated corrections.

*Proof.* Proposition N1 excludes greater rank. Theorems Q5.5–Q5.6 and Appendix A exhaust all ordered kernels; K(a) recognizes IP and reversal gives the source equivalence. Appendix F supplies all exact presentation and marked-name adapters from the data in Appendix G. K(d), Lemma N2 and Theorems N3–N4 prove the central mechanisms. The shared square model and Frattini characters give Propositions N5–N6. The quoted prior statements are retained as specified in §24, not counted as new proofs. ∎

## 26. Shared proof, retained costs and source boundaries''','N009_corollary_and_cost_heading')
replace('cyclic-model proof, its catalogue-relative order-256 census, all FAP cuts,','cyclic-model proof, its bounded order-256 word test, all FAP cuts,','cost_seed')
replace_between('The necessary finite programs are printed in full in Appendices A–D.','L108\'s set-valued operation is included',
'''The necessary finite programs are printed in full in Appendices A–D and F–H. Appendix E's optional Petrial controls remain fully charged. Appendix A now uses the common rank/excess theorem to supply both L035's order-256 seed and N009's order-1024 exhaustion, removing the former SmallGroups order-256 completeness input. Appendices B–C retain the complete TomLib J1 subgroup table and exact algorithms; Appendix D is unchanged. Appendix F uses complete raw presentations and exact marked isomorphisms for every N009 source label and example. Appendix G prints all 72 primary named presentations and all 107 Table 6 rows; duplicate permutation arrays are unnecessary because the primary labels explicitly define these finitely presented models. Appendix H is the complete fresh replay runner. GAP/NQ and the named-presentation transcription boundary remain explicit. No source totals or label list filters the kernel search.

The new K(d) is an exact downward image-intersection theorem; the existing K(a) recognizes the quotient marking after transport to the canonical class-two base. The common forest quotient supplies the bound in all four census cases, and the same affine model supplies the center formulas. Central-involution selection, successful extension presentations and finite marked recognition still require their printed source-specific proofs. This is an actual shared theorem with two classification applications, not an identification of arbitrary finite examples with a universal matrix model.

All four previous nonseed programs are byte-identical to the reviewed predecessor; the new complete executions are separately required. Runtime versions, data hashes, logs and output certificates remain charged audit artifacts. No new Lean formalization, historical priority or numerical compression ratio is asserted. A future common measurement must count all prose, code and mathematical data, charge wrappers/outputs consistently and declare every retained background.

''','new_cost_and_dependency_boundary')
replace("toroidal classification, the older tight-family classification, N009's\norder-1024 census, and the phase46 minimal-cover exploration are not new\nintake entries.","toroidal classification, the older tight-family classification and the phase46 minimal-cover exploration remain outside this intake. N009 is a new candidate intake with the complete corrected contract in §24; its addition awaits independent review of this assembly.",'new_scope_boundary')
replace('Component approval does not approve this altered assembly.','N009 uses the complete 22-page journal primary PDF, freshly read including all 27 numbered items, all six tables and end matter. Printed pages 10 and 16 were also freshly inspected for the two table corrections. Its older component review is retained as provenance; it does not certify the new shared enumeration or the new assembly. Component approval does not approve this altered assembly.','reading_boundary')
appendix='''## Appendix A. Complete rank/excess kernel enumeration

Theorems Q5.5–Q5.6 prove the written bound and completeness of this finite search. All accepted and rejected terminal kernels receive all actual IP meets. This single program is charged once for the seed and the three order-1024 ranks; exact versioned execution is recorded by Appendix H.

```gap
'''+(R/'phase78_n009_integration_census.g').read_text()+'''```

Only the four tested seed word implications enter the infinite-parameter proof in §13. No order-1024 assertion is used to justify that seed. The original SmallGroups IDs and anchored counts are not conclusions required by the new contract.

'''
replace_between('## Appendix A. The finite completeness calculation, fully specified','## Appendix B. Complete finite construction certificate',appendix,'new_complete_Appendix_A')
extra=''
for letter,title,file,lang in [('F','Complete source presentation and marked-label recognition','phase78_n009_integration_finite.g','gap'),('G','All named presentation and source-table data','phase78_n009_integration_data.g','gap'),('H','Complete fresh mathematical replay runner','phase78_n009_integration_run.py','python')]:
 extra+='## Appendix '+letter+'. '+title+'\n\nThe following full file is part of the proof and audit cost.\n\n```'+lang+'\n'+(R/file).read_text()+'```\n\n'
replace('## References and exact source versions',extra+'## References and exact source versions','new_complete_appendices')
s+='''
[GLP18] Y. Gomi, M. L. Loyola and M. L. A. N. De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics **13**(1) (2018), 1–22, DOI [10.55016/ojs/cdm.v13i1.62475](https://doi.org/10.55016/ojs/cdm.v13i1.62475). [Primary journal PDF](https://cdm.ucalgary.ca/article/download/62475/46803), SHA256 `0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda`.

Its quoted standard intersection criteria are attributed to M. Conder and D. Oliveros, *The intersection condition for regular polytopes*, JCTA **120** (2013), 1291–1304. The universal and finite square-quotient inputs are quoted from McMullen–Schulte, *Abstract Regular Polytopes* (2002), the latter on pp. 364–365, 368. Its exceptional infinite decomposition is quoted from McMullen–Schulte, *Regular polytopes from twisted Coxeter groups and unitary reflexion groups*, Advances in Mathematics **82** (1990), 35–87. Those earlier proofs are retained in the precise quoted forms; no claim of fresh acquisition or rederivation is made.

The named-object data are credited to M. I. Hartley's Atlas of Small Regular Polytopes; Appendix G records the exact primary URL and snapshot hash for every defining presentation. The URL may contain a catalogue identifier, but replay neither calls SmallGroups nor assumes a catalogue is complete. The entire new finite search and recognition were run with GAP 4.15.1 and NQ 2.5.11. Existing software/background inputs for the other branches are unchanged.
'''
(R/OUT).write_text(s)
# Exact inherited spans: no prior source adapter may silently disappear.
ledger=json.loads((R/'phase65_petrial_integration_ledger.json').read_text())
old_contracts=ledger['contracts'];contracts=[];spanrows=[]
for row in old_contracts:
 r=copy.deepcopy(row);p=r['integrated_proof_span'];chunk=old[p['start_codepoint']:p['end_codepoint_exclusive']];assert sha(chunk.encode())==p['sha256_utf8']
 assert s.count(chunk)==1,(r['integration_id'],s.count(chunk));a=s.index(chunk)
 r['previous_replacement_file']=BASE;r['previous_integration_proof_span']=p;r['replacement_file']=OUT
 r['integrated_proof_span']=dict(start_codepoint=a,end_codepoint_exclusive=a+len(chunk),sha256_utf8=sha(chunk.encode()))
 r['extension_status']='new_assembly_pending_independent_review; exact_phase65_adapter_preserved'
 contracts.append(r);spanrows.append(dict(id=r['integration_id'],sha256=p['sha256_utf8']))
# Full source-item inventory, including retained statements and explicit corrections.
coverage=json.loads((R/'phase24_N009_coverage.json').read_text())
section_map={
 'Definition 2.1':'24.1','Lemma 2.2':'24.1','Lemma 2.3':'24.1','Lemma 2.4':'24.1','Lemma 2.5':'24.1','Definition 2.6':'24.3','Theorem 2.7':'24.1','Lemma 2.8':'24.1',
 'Lemma 3.1':'24.1','Lemma 3.2':'24.1','Corollary 3.3':'24.2','Lemma 3.4':'24.2','Lemma 3.5':'24.2','Theorem 3.6':'24.2','Corollary 3.7':'24.2','Theorem 3.8':'24.2','Example 3.9':'24.4',
 'Definition 4.1':'24.5','Theorem 4.2':'24.5','Example 4.3':'24.5','Example 4.4':'24.5','Example 4.5':'24.5','Lemma 5.1':'24.6','Lemma 5.2':'24.6','Theorem 5.3':'24.6','Lemma 5.4':'24.6','Theorem 5.5':'24.6',
 'Table 1':'24.2','Table 2':'24.4','Table 3':'24.4','Table 4':'24.4','Table 5':'24.3','Table 6':'24.3'}
for i,row in enumerate(coverage['numbered_statements']+coverage['tables'],1):
 sec=section_map[row['id']];a=s.index('### '+sec+'.');m=re.search(r'\n##[#]? ',s[a+1:]);b=a+1+m.start() if m else len(s)
 r=dict(integration_id='N009.'+str(i),paper='N009',source_reference=row['id'],source_pdf='sources/phase17_gomi_loyola2018.pdf',source_pdf_sha256='0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda',source_text_sha256='091caf4266f2ac595aec76def47d451700fff7c80f6d0f3eabeee2e6f31f38e7',component_contract=row,common_result=['K(a)','K(d)','Q5.3','Q5.5','Q5.6','N1–N6'],replacement_file=OUT,integrated_proof_span=dict(start_codepoint=a,end_codepoint_exclusive=b,sha256_utf8=sha(s[a:b].encode())),integration_status='author_assembled_pending_independent_review',retained_inputs=row.get('retained_inputs',[]),full_dependency_closure_certified=False)
 r['component_contract']=copy.deepcopy(row);r['component_contract']['historical_evidence_only']=r['component_contract'].pop('evidence',[])
 r['full_source_formulation_normalized']=row['exact_target'];r['printed_pages']=row['printed_pages'];r['literal_or_scoped']=row['status']
 r['historical_component_adapter_is_not_new_proof_dependency']=True
 contracts.append(r)
ledger.update(contracts=contracts,candidate_source_ids=ledger['candidate_source_ids']+['N009'],source_count_admitted=0,ratio=None,status='author_assembly_pending_independent_review',manuscript=dict(path=OUT,sha256=sha((R/OUT).read_bytes())),new_source_complete_numbered_items=27,new_source_complete_tables=6,new_dependency_delta='SmallGroups order256 completeness removed; universal kernel theorem and complete fresh GAP/NQ search replace it. Exact primary named presentations replace duplicate permutation arrays.',new_source_scope_records=coverage['other_scope'])
# Record dependency removal in the live ledger, retaining the old record only as history.
removed=[x for x in ledger['retained_background']['Unified'] if x['id']=='B-retained-6']
assert len(removed)==1
ledger['retained_background']['Unified']=[x for x in ledger['retained_background']['Unified'] if x['id']!='B-retained-6']
ledger['historical_removed_background']=removed
for r in contracts:
 if r.get('integration_id')=='U.D3':
  r['historical_previous_imports']=copy.deepcopy(r['selected_imported_inputs'])
  r['selected_imported_inputs']=[x for x in r['selected_imported_inputs'] if x['id']!='B-retained-6']+[dict(id='N009-algorithms',source_label='GAP_NQ_exact_algorithms')]
  r['common_result']='Q3.1,Q5.5,Q5.6,Q6.1,Q7.1,Appendix A'
ledger['retained_background']['N009']=[dict(id='N009-algorithms',statement='Exact GAP finite-group/Todd–Coxeter and NQ universal nilpotent-quotient algorithms'),dict(id='N009-IP',statement='Quoted standard prefix/suffix string-IP criteria; exact all-subset tests used in every finite certificate'),dict(id='N009-universal',statement='Quoted geometric universal-group interpretation'),dict(id='N009-square',statement='Quoted finite smooth [4,4] quotient classification, with both dihedral decompositions'),dict(id='N009-infinite',statement='Quoted marked infinite universal decomposition (N6)'),dict(id='N009-labels',statement='72 primary named complete marked presentations as data, not a completeness theorem')]
for row in ledger['detailed_two_group_clause_rows']:
 if 'Order-256 catalogue' in row.get('source_specific_proof_cost',''):
  row['historical_previous_source_specific_proof_cost']=row['source_specific_proof_cost']
  row['source_specific_proof_cost']=row['source_specific_proof_cost'].replace('Order-256 catalogue and exhaustive relation census','Shared universal-kernel theorem and exhaustive order-256 word test')
ledger['source_versions']['N009']=dict(title='String C-groups of order 1024',authors=['Y. Gomi','M. L. Loyola','M. L. A. N. De Las Peñas'],journal='Contributions to Discrete Mathematics 13(1) (2018), 1–22',doi='10.55016/ojs/cdm.v13i1.62475',primary_pdf='sources/phase17_gomi_loyola2018.pdf',sha256='0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda',fresh_read='All text, all 27 numbered items and six tables; PDF pp10 and16 visually checked.')
ledger['new_fresh_source_reading']='Complete N009 primary; complete reviewed central, kernel, rank3, label, center/exception and examples arguments; all new finite code executed fresh.'
ledger['common_core'].extend([dict(id='Kd',statement='Exact quotient image intersection iff N intersect AB=(N intersect A)(N intersect B)',actual_users=['N009 Lemmas3.1/3.2','N009 central quotient mechanism']),dict(id='Q55',statement='Every finite forest-marked two-group at excess k is one of finitely many universal invariant kernels; IP is exactly the kernel profile criterion.',actual_users=['L035 bounded seed','N009 all nondegenerate ranks'])])
(R/'phase78_n009_integration_ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
def sections(text):
 starts=list(re.finditer(r'^## (\d+)\. .*$',text,re.M));return {int(m[1]):text[m.start():(starts[j+1].start() if j+1<len(starts) else text.index('## Appendix A'))] for j,m in enumerate(starts)}
os=sections(old);ns=sections(s);preserved=[]
for n in range(1,24):
 if os[n]==ns[n]:preserved.append(dict(section=n,sha256=sha(os[n].encode())))
assert [x['section'] for x in preserved]==[3,4,5,6,7,8,9,10,12,14,15,16,17,18,19,20,21,22,23]
blocks=re.findall(r'^```(gap|python)\n(.*?)^```',s,re.M|re.S)
oldblocks=re.findall(r'^```(gap|python)\n(.*?)^```',old,re.M|re.S)
assert len(blocks)==8 and blocks[1:5]==oldblocks[1:5]
code=[dict(language=lang,bytes=len(code.encode()),sha256=sha(code.encode())) for lang,code in blocks]
assembly=dict(status='assembled_author_pending_review',base=dict(path=BASE,sha256=BASE_SHA),manuscript=ledger['manuscript'],edits=edits,all_87_prior_source_adapters_byte_identical=spanrows,hash_preserved_sections=preserved,changed_proof_sections=[2,11,13],new_proof_section=24,old_programs_B_C_D_E_byte_identical=True,code_appendices=code,new_source_numbered_items=27,new_source_tables=6,contract_rows=len(contracts),source_count_admitted=0,ratio=None,primary_source_exports=False)
(R/'phase78_n009_integration_assembly.json').write_text(json.dumps(assembly,indent=2)+'\n')
print(json.dumps(dict(manuscript_bytes=(R/OUT).stat().st_size,manuscript_sha256=ledger['manuscript']['sha256'],contracts=len(contracts),prior_adapter_spans=87,preserved_sections=len(preserved),full_programs=len(blocks))))
