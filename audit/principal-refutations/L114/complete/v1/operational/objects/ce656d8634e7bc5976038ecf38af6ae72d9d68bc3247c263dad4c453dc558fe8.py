from pathlib import Path
import importlib.util, json, sys
sys.dont_write_bytecode = True
S=Path('/Users/sasha/medusa/research/leemans'); Y=S/'geometry/suzuki_incidence'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure()
c.packet('geometry/suzuki_incidence/normalizer_restrictions')
out=Y/'normalizer_restrictions_root01'
r=json.loads((out/'report.json').read_text())
assert r['status']=='PASS_L114_NORMALIZER_RESTRICTIONS_INPUTS_AND_NATIVE_ASSEMBLY' and r['native_pages']==5
for p in out.iterdir():
 if p.is_file(): c.add(p)
c.add(__file__)
c.finish('geometry/suzuki_incidence/normalizer_restrictions_root_review','ACCEPTED_L114_GENERAL_NORMALIZER_RESTRICTIONS',dict(
 reviewer='root',author='j3_recovery',native_pages=5,
 review=[
 'Read the entire proof, checked its general arguments, and directly viewed all five freshly assembled native pages. The recorded fresh audit checks 25 declared dependencies and 18 exports; it is not itself the mathematical proof.',
 'The residual maximal-intersection condition passes to induced residues. Cyclic induction gives distinct prime indices; the odd-dihedral induction treats both disjoint reflection cosets and full prime-primary rotation parts, proving maximality of every parabolic without borrowing the whole earlier classification.',
 'The affine subgroup normalizer is proved inside the unique point stabilizer using the explicit two coordinate commutators. Self-normalization and one conjugacy class inside the subfield then give exactly one containing subfield of that size.',
 'Full nonsplit normalizers are excluded by two successive maximal intersections. Equal subfield sizes are treated by the opposite-torus product; distinct maximal field indices give the strict size contradiction. The point-stabilizer and prime-degree exclusions remain explicit previously acquired inputs.',
 'For the full split normalizer, two dihedral intersections force two subfields. Different sizes contradict prime-index estimates; equal sizes use the affine uniqueness lemma rather than assuming different parabolics imply different field degrees.',
 'The resulting rank bound and the composite-degree rank-three necessary pattern follow by the exhaustive full-torus overgroups. The prime quotient of a geometric series forces a prime-power field degree.',
 'Source Lemma4.5 is used as a uniform upper bound, not an existence assertion for every q. The necessary pattern is not a sufficiency claim. Remaining thinness and candidate-list corrections are separate; classical Suzuki structure remains attributed.'
 ],source_credit=0))
c=m.Closure();P=Y/'remaining_markings_request01'
c.packet('geometry/suzuki_incidence/remaining_markings_request01')
c.packet('geometry/suzuki_incidence/panel_request02_root_review')
assert (P/'run.py').read_bytes()==(Y/'panel_request02/run.py').read_bytes()
req=json.loads((P/'request.json').read_text())
for b in req['bindings']:c.binding(b)
assert req['deadline_seconds']==10 and req['output_cap_bytes']==1048576
c.add(__file__)
c.finish('geometry/suzuki_incidence/remaining_markings_request01_root_review','ACCEPTED_L114_EIGHT_RETAINED_MARKINGS_SINGLE_REQUEST',dict(
 reviewer='root',author='j3_recovery',
 review=[
 'Read the complete fixed-recipe calculation, explanatory proof, and owner. The owner is byte-identical to the acquired panel request02 owner, with unchanged one-invocation limits and final input/output checks.',
 'The eight pairs are exactly (2,5),(2,7),(2,13),(5,7),(5,13),(7,7),(7,13),(13,13). The already acquired (5,5) marking is excluded. Only the retained small groups and 24 literal coset panels are constructed; there is no ambient group census or search for new markings.',
 'The program validates the intended group orders and intersections before listing complete coset panels. Any enlarged panel requires a separate exact application of the source hypotheses; no counterexample or source completion is granted by this request.'
 ],deadline_seconds=10,output_cap_bytes=1048576,permitted_calls=1,automatic_successor=False,source_credit=0))
