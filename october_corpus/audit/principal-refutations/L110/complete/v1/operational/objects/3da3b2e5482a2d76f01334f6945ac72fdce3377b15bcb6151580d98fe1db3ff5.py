from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence';F=S/'computation/f012'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_incidence/source_synthesis');O=Y/'source_synthesis_root01';r=json.loads((O/'report.json').read_text())
assert r['status']=='PASS_L114_COMPLETE_SOURCE_ASSEMBLY' and (r['source_claims'],r['volume_pages'],r['exact_proof_imports'])==(61,68,28)
for p in O.rglob('*'):
    if p.is_file():c.add(p)
c.add(__file__)
c.finish('geometry/suzuki_incidence/source_synthesis_root_review','ACCEPTED_L114_COMPLETE_FIXED_SOURCE_TREATMENT',dict(author='j3_recovery',reviewer='root',source_id='L114',source_claims=61,complete_volume_pages=68,source_completion_accepted=True,public_registration_pending=True,review=[
 'Read the full five-page source overview, five-page realization proof and all61 source-claim dispositions. All ten new native pages were viewed after fresh compilation. Previously independently accepted general and finite components are acquired without repeating scientific searches; their original provenance remains in the complete68-page volume.',
 'Verified the common split-dihedral uniqueness and simultaneous alignment arguments, involution obstruction, trace parametrization of odd-order classes, all three prime-case realizations, composite pattern constructions and every RWPRI subset. The full mixed central pattern is forced into the standard coordinates and fails maximality in every realization. The closing existence question is disposed separately for bare intersections and RWPRI.',
 'Checked the explicit parabolic-product proof of the surviving flag-transitivity remarks and the local-action degree/size exclusions for the displayed composite patterns. Those exclusions are not used to reassert the refuted exhaustive classification. All four literal preliminary errors and the corrected rank-two scalar families remain visible.',
 'The two earlier independently acquired nonthin matrix markings dispose of both prime thinness clauses under the source algebraic local definition. The independently accepted coordinate family refutes the unbounded-rank and composite-rank-three exclusions with precisely the geometry/pregeometry scope proved. Stronger full-incidence-residue or flag-transitivity variants are left distinct.',
 'Fresh assembly passed1243bindings,13accepted gates,28exact proof imports,all68native page drawing streams and glyph programs,complete native rebuilds and eight damage/optimization controls. These checks verify assembly, not a substitute for the mathematical review above.',
 'Classical Suzuki structure, the source-quoted dihedral catalogue and Aschbacher theorem remain attributed premises. Excluded originals L109/L123 gain no intake credit. This completes the fixed L114 source treatment after its already registered principal refutation; public registration is pending. It adds no ordinary recovery, second refutation, new conjecture count, Lean or compression measurement.'
 ]))
c=m.Closure();c.packet('computation/f012/singleton_quotient_work');c.add(__file__)
c.finish('computation/f012/singleton_quotient_root_review','ACCEPTED_F012_NO_ALL_SINGLETON_BIPARTITE_QUOTIENT',dict(author='finite_recoveries',reviewer='root',review=[
 'Read the complete two-page proof and both native pages. Acquired the earlier independently accepted Gram and weighted quotient results, including the exact c=3 tight-table case. No enumerator or external graph classification is used.',
 'Independently checked connectedness from4regularity on9vertices; the weighted neighbour equations force opposite equal weights with a+b+c=3. The(1,1,1)case forces an isolatedK5, and the(2,1,0)form propagates across every edge.',
 'The propagated form has9vertices,18edges,12faces and connected vertex links. The face adjacency graph is connected, so overF2 the two boundary ranks areV−1 andF−1. Their composition vanishes, forcing Euler characteristic at most2, contrary to3. No orientability assumption or surface classification enters.',
 'In the remaining form every actual triangle block occurs three times and each point lies in two blocks. This yields a connected simple cubic graph on6vertices. A triangle forces c=t=3 for two incident edge-points, contradicting the acquired tight table. The complement classification reduces the remaining triangle-free case toK3,3; star pairings within either side would pair an odd number9 of occurrences.',
 'Interchanging the two incidence parts gives the same obstruction. This excludes only the all-singleton quotient in each part; one,two or three double classes remain. It grants no complete bipartite exclusion, production pruning, source completion, conjecture, Lean or compression credit.'
 ]))
