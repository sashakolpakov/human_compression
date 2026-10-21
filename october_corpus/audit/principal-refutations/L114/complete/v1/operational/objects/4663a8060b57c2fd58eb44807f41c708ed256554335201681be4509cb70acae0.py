from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');E=S/'geometry/sporadic_polytopes/endpoint_method_work'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_subgroups/preliminaries');c.packet('geometry/suzuki_subgroups/preliminaries_distinct_review');c.add(Path(__file__))
r=json.loads((S/'geometry/suzuki_subgroups/preliminaries_distinct_review/review.json').read_text())
if r['author']!='root' or r['reviewer']!='l070_publication' or r['status']!='ACCEPTED_L115_PRELIMINARY_RESULTS_WITH_DOMAIN_CORRECTION' or r['source_statement_count']!=11:raise ValueError('distinct review scope')
c.finish('geometry/suzuki_subgroups/preliminaries_review_adoption','ADOPTED_L115_DISTINCTLY_REVIEWED_PRELIMINARY_RESULTS',dict(
 author='root',reviewer='l070_publication',adopter='root',
 review=['Adopts the distinct agent review of the root-authored five-page proof; root authorship is not described as independent review.',
 'The reviewer checked all five native proof pages and source printed pages99–105, all eleven stated source lemmas, and the exact scope correction in Lemma3.2. Properness of every parabolic follows from firmness; the rank argument is not an unsupported truncation step.',
 'Fresh independent controls passed50 odd exponents,240 subfield parameters, the actual q8 point stabilizer and34 cyclic semidirect actions. The prior harness failure at FactorsInt(1) is retained without credit.',
 'The common proof uses Frattini lifting, affine averaging with possibly nonfaithful action, full scalar irreducibility and a unique-overgroup geometric obstruction. The classical Suzuki model, ovoid and maximal-subgroup theorem remain attributed premises.'
 ],
 source_statements=r['source_statements'],source_statement_count=11,
 scope='Surviving L115 preliminary results only. Remaining families, tables and global counts remain unpaid; no whole-source, open-conjecture, Lean or compression credit.',source_completion_credit=0))

c=m.Closure();c.packet('geometry/sporadic_polytopes/endpoint_method_work/ru_early_returned_work');c.packet('geometry/sporadic_polytopes/endpoint_method_work/ru_remaining_returned_profile_root_review')
W=E/'ru_early_returned_work';old=E/'ru_remaining_returned_work'
for n in ['monitor.py','single_process.py']:
 if (W/n).read_bytes()!=(old/n).read_bytes():raise ValueError('unchanged supervision')
c.add(Path(__file__))
c.finish('geometry/sporadic_polytopes/endpoint_method_work/ru_early_returned_profile_root_review','ACCEPTED_L026_RU_EARLY_RETURNED_CELL_ACQUISITION_PROFILE',dict(
 reviewer='root',author='l070_publication',
 review=['Read complete reader, request builder, owner and all three diffs from the accepted remaining-cell profile. Changes are the producer/method bindings, exact earlier-cut output directory, singleton2/2 selector and report names.',
 'The direct-PID monitor and process-creation-denying audit hook are byte-identical to the accepted predecessor. Literal candidate predicates, complete-byte inventory/journal checks and mathematical count derivation are unchanged and retain their acquired review.',
 'A concrete request can only be prepared after the exact accepted producer returns cleanly and completely. The reader reacquires all original input/output bindings, the full literal inventory and every candidate, exact stdout slice and per-cell/container identities, then rechecks all bytes.',
 'Bounds remain180seconds,512MiB sampled RSS,8MiB per file,4GiB launch reserve and2GiB emergency floor. It launches no GAP target and cannot continue a failed production call.'
 ],
 cell=[2,2],scope='Read-only returned-evidence profile only. No returned count or source credit. A concrete clean-producer request and distinct root acquisition remain required.',target_runs=0,source_credit=0))
