"""Prepare a private L041 proposal; never install or grant acceptance."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
from pathlib import Path
import argparse,hashlib,json,re,shutil
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression'
B='audit/recoveries/L041/v1';A='corpus106_L041_decorated_geometry_v2'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,base):
 b=p.read_bytes();return dict(path=str(p.relative_to(base)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--replay',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();O=a.stage.resolve();I=a.out.resolve();need(not I.exists(),'Fresh proposal');I.mkdir(parents=True)
T=load(O/B/'transport.json');report=load(a.replay/'report.json');need(report['status']=='PASS_PUBLIC_L041_CLOSURE','Exact public replay')
rows={(r['origin'],r['path']):r for r in T['files']}
def logical(path,origin='study'):
 r=rows[origin,path];need('public_path'in r,'Retained scientific payload');return dict(path=r['public_path'],bytes=r['stored_bytes'],sha256=r['stored_sha256'],encoding=r['encoding'],decoded_bytes=r['bytes'],decoded_sha256=r['sha256'])
source=load(S/A/'source_map.json');scope=load(S/A/'scope.json');provenance=load(S/A/'provenance.json')
need(source['numbered_statements']==20 and len(source['rows'])==28 and source['questions']==dict(explicit_open_questions_found=0,new_answers_claimed=0),'Exact source-disposition inventory')
for src,name in [(a.replay/'report.json','portable_report.json'),(W/'native_visual_review01.json','native_visual_review.json')]:shutil.copyfile(src,O/B/name)
for name in ['source_map.json','scope.json','provenance.json']:shutil.copyfile(S/A/name,O/B/name)
native=logical(A+'/decorated_points.tex');included=logical(A+'/tetrahedra_section.tex')
need(re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(S/A/'decorated_points.tex').read_text())==['tetrahedra_section.tex'],'Exact immediate source input')
need(Path(native['path']).parent/'tetrahedra_section.tex'==Path(included['path'])and included['encoding']=='identity','Buildable adjacent native input')
manuscript=dict(id='L041-decorated-points',title='Decorated points and tetrahedral geometries',tex=native,pdf=logical(A+'/decorated_points.pdf'),tex_inputs=[included],physical_pages=8)
native_inventory=dict(status='EXACT_LITERAL_NATIVE_INPUT_INVENTORY',manuscripts=[manuscript],acquired_manuscripts=[dict(title='Residue stabilizers and distinguished generators',tex=logical('corpus106_L052_residue_theory_v1/residue_theory.tex'),pdf=logical('corpus106_L052_residue_theory_v1/residue_theory.pdf'),physical_pages=8,already_published=True)],additional_public_common_collection='audit/topic-chamber/v2/admission.json',reading_inventory_is_not_a_measurement=True)
save(O/B/'native_input_inventory.json',native_inventory);save(I/'native_input_inventory.json',native_inventory)
chain={role:logical(name+'/manifest.json')for role,(name,h)in zip(['author','distinct_review','root_adoption'],T['entry_roots'])}
pending=T['principal_review_pending']or len(chain)<3
adapt=dict(status='EXPLICIT_PUBLIC_L041_REPLAY_ADAPTER',original_author_code_unchanged=True,runtime_text_patching=False,private_fallback=False,
 operations=['Verify every exact manifest export, explicit dependency and nested metadata identity before replay.','Restore all scientific files using exact Git-tracked public reuse or new lossless payloads.','Preserve seven source/documentary omissions and one explicit original Python runtime identity.','Run the unchanged check_decorations.py and compare its complete expected output for q=4,7,13,19,25.','Rebuild all eight native pages with the literal adjacent tetrahedra_section.tex.','Acquire the previously accepted L052 and topic-chamber proofs/Lean checks without repeating their mathematical work.'],
 runtime_treatment=T['runtime_treatment'],accepted_general_proof_checked_by_program=False,whole_original_credit=0)
save(I/'portable_adaptation.json',adapt);save(O/B/'portable_adaptation.json',adapt)
scope_routes=dict(status='PENDING_FINAL_PRINCIPAL_ACCEPTANCE'if pending else'ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING',original='L041',principal_contract='Uniform recovery of the fixed source tetrahedral hypertope families, with explicit corrections to coordinates, periods and two ancillary remarks.',source_rows=source['rows'],retained_inputs=scope['retained_inputs'],parameters=scope['general_result'],finite_cases_are_controls_only=True,source_questions=source['questions'],whole_original_credit=0,new_question_credit=0,new_Lean=0,new_measurements=0)
save(I/'scope_routes.json',scope_routes);save(O/B/'scope_routes.json',scope_routes)
refs={name:pin(O/B/name,O)for name in ['transport.json','portable_policy.json','portable_check.py','application_replay.py','portable_report.json','native_visual_review.json','native_input_inventory.json','portable_adaptation.json','scope_routes.json']}
proposal=dict(status='PRIVATE_PROPOSAL_AWAITING_DISTINCT_REVIEW_AND_ROOT_ADOPTION'if pending else'ROOT_MATHEMATICS_ACCEPTED_PRIVATE_PUBLICATION_PROPOSAL',original='L041',source_edition=source['edition'],source_identity=source['source'],source_url=source['source_url'],fixed_source_pages=21,
 principal_contract=scope_routes['principal_contract'],principal_formulations=['The fixed field family and its complete tetrahedral hypertope geometry','Exact rank-two and rank-three residues, two chamber orbits and full regular/chiral distinction','Proper and improper correlations','Complete translation kernels and literal source corrections'],
 component_acceptance=dict(complete=chain),acceptance_pending=pending,acceptance_roles='Root authored the new argument; l044 owns its final distinct review. Publication_recovery prepares the exact public closure and is not a substitute mathematical reviewer. Root alone integrates and admits public credit.',
 complete_acquired_proofs={p['origin']+':'+p['path']:logical(p['path'],p['origin'])for p in T['packets']},published_common_admission=logical('audit/topic-chamber/v2/admission.json','public'),
 manuscript=manuscript,source_disposition_rows=28,numbered_source_statements=20,source_qualifications=source['rows'],retained_inputs=scope['retained_inputs'],**refs,
 literal_source_contract=logical(A+'/source_map.json'),literal_scope=logical(A+'/scope.json'),requirements=['Ordinary Python3 with pypdf','pdflatex and Ghostscript on PATH','Git-tracked public predecessor evidence'],
 principal_originals_added=1,whole_original_credit=0,new_question_credit=0,new_Lean_declarations=0,new_measurements=0,measured=False,whole_source_formalized=False,compression_factor=None,software_inclusive_factor=None,publication_gate_remaining=True,
 required_predecessor=dict(recoveries=84,principal_refutations=1,handled_mathematical_originals=85,pending_mathematical_originals=20,measured_recoveries=53,unmeasured_recoveries=31),
 proposed_register_after=dict(recoveries=85,principal_refutations=1,handled_mathematical_originals=86,pending_mathematical_originals=19,measured_recoveries=53,unmeasured_recoveries=32),
 predecessor_science='science84 / N010, commit '+T['baseline'],document_inventory_not_measurement='Eight new manuscript pages; all acquired proofs and software remain additional costs. Five finite fields are controls, not a finite proof of the infinite family.',
 replay_command='python '+B+'/portable_check.py --repo . --out NEW_DIRECTORY --expected-transport '+refs['transport.json']['sha256']+' --expected-policy '+refs['portable_policy.json']['sha256']+' --expected-adapter '+refs['application_replay.py']['sha256'])
save(I/'admission_proposal.json',proposal);save(O/B/'admission_proposal.json',proposal)
guide='''L041: decorated points and tetrahedral geometries
=================================================

This private proposal concerns Catalano, Fernandes, Hubard and Leemans,
Hypertopes with tetrahedral diagram, Electronic Journal of Combinatorics
25(3) (2018), P3.22. The fixed source has 21 pages. The author source map
routes all 20 numbered statements and the associated remarks in 28 rows.
Final distinct review and root adoption are still required for this draft.

Reading route
-------------

Read papers/recoveries/L041/v1/decorated-points/decorated_points.pdf and
its complete source, decorated_points.tex. The exact tetrahedra_section.tex
is beside it, so the literal input builds directly. The new manuscript has
eight pages. Its accepted L052 residue theory and complete topic-chamber/v2
collection remain additional acquired proofs; native_input_inventory.json
and the manifest inventory give exact routes. This is no compression measure.

The general argument covers primes p != 3, q=p for p=1 mod3 and q=p^2
for p=2 mod3, with both primitive cube roots. The five finite fields
4,7,13,19,25 are executable controls, not an exhaustion of the family.
The triangular Euclidean presentation/translation lattice and previously
accepted chamber/reflection theory remain explicit inputs.

Source qualifications
---------------------

The determinant model repairs the printed disconnected coordinate rule;
q=13 is an explicit discrepancy. Complete translation lattices replace
the insufficient prime-field period labels; p=19,e=7 has printed norm57
but actual index19. The q=4 full correlation group is S5 times S4.
The literal finite-index assertion inside the infinite hyperbolic group
is rejected without silently replacing it by a quotient interpretation.
The isolated matrix entry is corrected. All exact statement-level
qualifications and source pages remain in source_map.json and scope_routes.json.
No new historical priority, open-question answer, Lean result or measurement
is claimed. Frozen author metadata retains its original pending wording.

Transport and replay
--------------------

All scientific bytes, historical editions, code, controls and review evidence
are retained exactly. Every reused public object is Git tracked, so an ordinary
clean checkout is sufficient. Seven original articles/texts/source-page renders
are documentary hash-only records; portable_policy.json lists them individually.
The one external Python binary pin is explicitly a historical runtime identity.
It is not copied or invented as a study file; replay uses the caller's ordinary
Python with pypdf, pdflatex and Ghostscript. No private proof fallback, runtime
text patching or omitted scientific input is allowed.

The portable checker rehashes and restores the complete closure, verifies every
declared metadata pin, runs the unchanged five-field controls and guards, and
rebuilds all eight native pages. It does not repeat acquired censuses or Lean,
and it cannot replace the mathematical reviews. The exact command is:

  '''+proposal['replay_command']+'''

Integration boundary
--------------------

Only L041 would change in the 106-entry catalogue. After all mathematical,
operational and registration gates, the proposed counts are 85 recoveries
plus the existing F003 refutation: 86 handled,19 pending within the105
mathematical originals. The53 measured recoveries and every old row/history
guard must stay unchanged. Root is the sole public writer; this package
neither installs files nor grants that increment.
'''
for p in [I/'PUBLICATION.rst',O/B/'PUBLICATION.rst']:p.write_text(guide)
plan='''Private science85 plan (not an installer)
========================================

Await exact final L041 distinct review and root adoption; add their complete
exports/dependencies to a new stage and replay it. Preserve stage01 unchanged.
Root then performs a separate operational review before any registration.
Use science84/N010 commit '''+T['baseline']+''' as predecessor, subject to the
root's exact baseline confirmation. No public mutation has been made here.

Once authorized for concrete registration, preserve the predecessor mutable
catalogue/README/index/protocol/verifier pointers exactly; add L041 evidence
only, update86/105 handled19pending and leave53measurements unchanged.
Retain all prior non-main verifier ASTs and route historical pointer checks
to their exact archived editions. Add source, manuscript, native-input and
scope checks plus malformed admission controls. Build the protocol natively,
then obtain distinct registration review and root's full historical snapshot
before commit/push. Do not repeat any accepted census or Lean compilation.
'''
(I/'science85_plan.rst').write_text(plan)
files=[pin(p,O)for p in sorted(O.rglob('*'))if p.is_file()]
save(W/(O.name+'_manifest.json'),dict(status='PRIVATE_PROVISIONAL_STAGE',files=files,scientific_acceptance_pending=pending,public_writes=False))
save(I/'handoff.json',dict(status='PROVISIONAL_OPERATIONAL_PREPARATION_REVIEW_PENDING',stage=str(O),proposal=pin(I/'admission_proposal.json',I),guide=pin(I/'PUBLICATION.rst',I),plan=pin(I/'science85_plan.rst',I),stage_manifest=pin(W/(O.name+'_manifest.json'),W),portable_replay=pin(a.replay/'report.json',a.replay),public_writes=False))
print(json.dumps(dict(status=proposal['status'],stage_files=len(files),proposal=str(I/'admission_proposal.json'))))
