from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
items=[('computation/f012','bipartite_gram_work','bipartite_gram_root01','bipartite_gram_root_review','ACCEPTED_F012_BIPARTITE_GRAM_NECESSARY_CONDITIONS','finite_recoveries',[
 'Read the full two-page proof and acquired local hypotheses. Fresh exact input and native-assembly check passed24 bindings and two identical proof pages; both new pages viewed directly.',
 'The local inequality d>=2u+c-6 follows from the acquired u<=2 and two-unit lemmas, the c=5 lower bound, and the c=6 sum of hexagon distances. Every c and u case is covered. Double counting gives135 common incidences,54 unit corners and27 opposite corners; summing36 nonnegative slacks forces every pair tight.',
 'The eighteen alternating triples give rows of weight6 and columns of weight3. Off-diagonal Gram entries count cost-two corners, hence BB^T/3=2J-U with diagonal2 and off-diagonal0,1,2. The row sum is6 and positive semidefiniteness is immediate. Equality of Gram inner product2 forces identical incidence rows; three-point columns bound each class by3.',
 'This is a necessary constraint in the bipartite incidence subcase. It is neither an exclusion of that subcase nor a production pruning rule, and launches no enumeration. No source completion or new conjecture claim follows.'
 ]),('geometry/suzuki_incidence','nonthin32_application','nonthin32_root01','nonthin32_root_review','ACCEPTED_L114_PRIME_GREATER_THAN_SEVEN_LITERAL_THINNESS_COUNTEREXAMPLE','j3_recovery',[
 'Read the complete two-page source proof and independent polynomial, matrix, group and panel readers. Fresh25-dependency/17-export/native replay passed, including eleven rejected damages and two optimization guards. Both new native pages viewed.',
 'The matrix recipes establish Suzuki membership. Product orders31,31,41 are exact. Equal62-order parabolics cannot coincide because that would place bc of order41 in a group of order62; their intersection is the shared maximal C2. Remaining intersections follow from orders, and the triple is trivial.',
 'Maximal D62, prime indices and trivial triple establish every literal RWPRI condition and the source algebraic two-point residues. The identity (ac)^15(ab)^15a=(bc)^20 gives the extra chamber. Equality with a standard coset contradicts the order31 relation. Literal full-panel enumeration gives3,3,3 and verifies the three displayed representatives.',
 'Because32-1=31>7 is prime, this separately refutes the second thinness branch of source Theorem6.1. It does not refute a reformulation requiring flag transitivity or two-transitivity on actual panels. The previously accepted rank bound and rank-two count are unchanged.',
 'No ambient census or discovery scan was replayed. This is an additional claim disposition in an original already having a principal refutation; no whole-original, additional principal, conjecture, Lean or compression credit.'
 ])]
for base,author,out,review,status,agent,notes in items:
 c=m.Closure();c.packet(base+'/'+author)
 for p in (S/base/out).iterdir():
  if p.is_file():c.add(p)
 c.add(__file__)
 if base.startswith('computation'):c.add('/private/tmp/check_bipartite_gram_root.py')
 c.finish(base+'/'+review,status,dict(author=agent,reviewer='root',native_pages=2,review=notes))
