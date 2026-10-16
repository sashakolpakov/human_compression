from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/primitive_pairs'
A=P/'source_synthesis';O=P/'source_synthesis_root_fresh01'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/primitive_pairs/source_synthesis')
for gate in ['character_application_root_review','table_application_root_review','algorithm_scope_review_adoption','m11_application_root_review']:
 c.packet('geometry/primitive_pairs/'+gate)
for p in O.rglob('*'):
 if p.is_file():c.add(p)
r=json.loads((O/'report.json').read_text())
if r['status']!='PASS_L036_COMPLETE_SOURCE_ASSEMBLY' or r['source_claims']!=35 or r['volume_pages']!=24:raise ValueError('replay gate')
c.add(Path(__file__))
c.finish('geometry/primitive_pairs/source_synthesis_root_review','ACCEPTED_L036_COMPLETE_CORRECTED_SOURCE_TREATMENT',dict(
 reviewer='root',author='j3_recovery',source_id='L036',review=[
 'Read the complete four-page synthesis, all35 source-claim entries and the twelve group-specific input routes. The six constituent proofs and computational applications retain their previously accepted mathematical reviews; they were not reacquired as new targets.',
 'The double-coset parameter set is a complete classification under automorphisms of the distinguished group, including interchange for equal maximal classes. The identity diagonal is removed. The rank-two coset argument proves firmness, connectivity and primitivity. No higher-rank transitivity or arbitrary graph-isomorphism classification is inferred.',
 'Burnside counting uses the complete maximal-subgroup action of Aut(G). Five complete character routes, six complete automorphism-group mark routes and the accepted L073 import account for all twelve groups. The exact corrected Ru count556287 and total568220 have the same group equivalence as the source. Library completeness, named group structures and classical subgroup classifications remain explicit borrowed premises.',
 'All308 suborbit cells,37 M11 geometry rows and70 design entries are accounted for. The two M23 labels and four typed-diameter corrections retain their explicit witnesses. The corrected general coset algorithm preserves the second subgroup when a core is present. The order-four counterexample distinguishes that defect from the printed variable typo.',
 'The fixed article receives an exact mathematical parameter set and all its printed finite invariants. Its external downloadable representative files are explicitly unverified and are not premises. Historical runtimes, separate code examples, proposed higher-rank work and speculation about earlier errors are not promoted into recovered theorems or solved conjectures.',
 'Fresh root replay passed651 dependency bindings, twelve input joins, seven damaged assemblies, both optimization guards and eight native TeX entrypoints. All23 imported page streams and font programs match. Directly inspected the freshly rendered cover and four synthesis pages; prior component page inspections remain valid under these exact imports.',
 'The M11 publication citation now correctly points to Section2 physical page3, and its GL2(3) heading is plain. Recorded text deltas preserve all mathematics. No new ordinary recovery, duplicate principal refutation, Lean declaration, conjecture answer or compression measurement is awarded.'
 ],complete_fixed_source_mathematics=True,external_representative_files_verified=False,expanded_representative_catalogue=False,
 public_registration='Pending independent portable publication review and registration.',principal_disposition='principal_statement_refuted',target_reexecuted=False,new_principal_refutation_credit=0))
