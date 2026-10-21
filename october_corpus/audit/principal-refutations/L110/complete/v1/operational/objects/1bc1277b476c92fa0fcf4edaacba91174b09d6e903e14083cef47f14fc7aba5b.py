from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

c=m.Closure()
for p in ['geometry/suzuki_incidence/prime_degree',
          'geometry/suzuki_subgroups/preliminaries_review_adoption',
          'geometry/suzuki_subgroups/rank_two_families_root_review']:
    c.packet(p)
fresh=S/'geometry/suzuki_incidence/prime_degree_root01'
assert json.loads((fresh/'report.json').read_text())['status']=='PASS_L114_PRIME_DEGREE_INPUTS_AND_NATIVE_ASSEMBLY'
for p in fresh.iterdir():
    if p.is_file():c.add(p)
c.add(__file__)
c.finish('geometry/suzuki_incidence/prime_degree_root_review',
 'ACCEPTED_L114_PRIME_DEGREE_RANK_OBSTRUCTION',dict(
 reviewer='root',author='j3_recovery',source_claims=['Theorem5.4','subgroup form of Lemma4.1'],
 review=[
 'Read the complete proof and viewed all three freshly compiled native pages. Directly inspected original printed pages46 and55: the subgroup condition includes the empty subset, and the conclusion excludes rank at least three.',
 'The axiom at the complement of a single type proves every added intersection is strict. The point-stabilizer exclusion uses its central elementary abelian group and the explicit classical maximal-subgroup list; a smaller simple subfield group has insufficient Sylow-two order.',
 'In prime field degree, coprimality and torus uniqueness force the stated proper overgroups. The point-stabilizer quotient of odd order cannot contain a nontrivial split dihedral subgroup.',
 'For a nonsplit maximal parabolic all other intersections are cyclic two-groups. A successive maximal intersection supplies an involution, whose unique cyclic four-group forces a repeated intersection. For the split normalizer with composite odd kernel, successive maximal intersections similarly force a repeated intersection inside that kernel.',
 'The empty-subset axiom supplies a maximal parabolic, and all its possible types are excluded. No flag-transitivity assumption or finite example is used as a necessity argument.',
 'Classical Suzuki subgroup, torus and ovoid premises remain attributed imports. This component does not dispose of composite-degree lemmas or the remaining realization assertions.'
 ],native_pages=3,finite_targets=0,source_credit=0))

c=m.Closure()
for p in ['diagram_audit','diagram_audit_distinct_review']:
    c.packet('geometry/suzuki_subgroups/'+p)
c.add(__file__)
c.finish('geometry/suzuki_subgroups/diagram_labels_root_adoption',
 'ACCEPTED_L115_FOUR_DIAGRAM_LABEL_CORRECTIONS',dict(
 reviewer='root',author='l070_publication',distinct_reviewer='finite_recoveries',
 review=[
 'Read both complete propositions and the complete distinct review. Directly viewed the bound original page118 to check the printed subgroup orientation and QPRI labels; the distinct reviewer also freshly viewed definition pages99 and100.',
 'The source convention puts the opposite parabolic index minus one at each diagram vertex. Orders52,20 and intersection4 therefore give4,12; element counts560,1456 independently determine the orientation.',
 'For the order-eight abelian parabolic, its cyclic-four intersection may be conjugated into the accepted root coordinates. Its normalizer R has order16, and P/R is elementary abelian of order4. Its three lines give three distinct saturated chains H<R<P_i<P<B<G, so uniqueness fails.',
 'The distinct review explicitly supplies the cyclic-four conjugacy justification and fresh finite-field controls. The local double-transitivity assertion and all graph girth/diameter values remain separate.',
 'Adopt only corrections to residue orders in diagrams25,26 and quasi-primitivity in27,29. No whole-source or numerical-table completion is inferred.'
 ],diagrams=[25,26,27,29],source_credit=0,graph_censuses=0))

E=S/'geometry/sporadic_polytopes/endpoint_method_work'
c=m.Closure()
for p in ['ru_remaining_five_root_review','ru_remaining_early_returned_work',
          'ru_remaining_early_returned_distinct_review','ru_pair2_early_root_adoption']:
    c.packet('geometry/sporadic_polytopes/endpoint_method_work/'+p)
for row in json.loads((E/'ru_remaining_early_returned_distinct_review/bindings.json').read_text()):c.binding(row)
request=E/'ru_early_pair3_returned_request01.json';c.add(request)
for row in json.loads(request.read_text())['inputs']:c.binding(row)
producer=E/'ru_early_transversal_pair3_01/receipt.json';c.add(producer)
pr=json.loads(producer.read_text())
for row in pr['outputs']:c.binding(row)
out=E/'ru_early_pair3_returned_root01'
r=json.loads((out/'report.json').read_text());receipt=json.loads((out/'receipt.json').read_text())
assert r['status']=='PASS_COMPLETE_RU_REMAINING_EARLY_CELL_ACQUISITION'
assert (r['cell'],r['double_cosets'],r['dual'],r['self_dual'],r['ordered'])==([3,2],1383,1172,100,2244)
assert receipt['status']=='PASS' and receipt['returncode']==0 and receipt['child_reaped'] and receipt['inputs_unchanged']
assert all(receipt[k] is None for k in ['postcheck_error','resource_stop','supervision_error'])
for p in out.iterdir():
    if p.is_file():c.add(p)
c.add(__file__)
c.finish('geometry/sporadic_polytopes/endpoint_method_work/ru_pair3_early_root_adoption',
 'ACCEPTED_L026_RU_EARLY_CELL_PAIR3_CLASS2',dict(
 reviewer='root',author='l070_publication',profile_distinct_reviewer='finite_recoveries',
 review=[
 'Read the returned-acquisition predicate, full owner and complete distinct profile review. The latter reconstructs exact deltas against the previously accepted pair2 reader and verifies unchanged monitor and audit hook.',
 'The actual root reader returned cleanly in29.54seconds, peak155697152 sampled RSS bytes, with its child reaped and inputs unchanged. It acquired the complete clean producer, exact singleton cell, closed journal, raw byte slice, compact records and all1390 output bindings.',
 'Freshly rebound the concrete24153-input request, distinct-review closure, producer outputs and root acquisition. No GAP census was repeated.',
 'This accepts the cell only. The full Ru source comparison remains incomplete until the four remaining middle-class-two cells and final join have been acquired.'
 ],cell=[3,2],double_cosets=1383,dual=1172,self_dual=100,ordered=2244,
 total_complete_cells=12,total_cells=16,total_double_cosets=10858,total_dual=8115,
 total_self_dual=352,total_ordered=15878,remaining_cells=[[4,2],[5,2],[7,2],[8,2]],
 fresh_gap_calls=0,source_credit=0))
