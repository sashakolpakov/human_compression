from pathlib import Path
import sys,json,importlib.util,difflib
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();Y=S/'geometry/suzuki_incidence'
for p in ['geometry/suzuki_incidence/prime_patterns','geometry/suzuki_incidence/prime_degree_root_review','geometry/suzuki_incidence/panel_request02_root_review','geometry/suzuki_subgroups/preliminaries_review_adoption','geometry/suzuki_subgroups/rank_two_families_root_review']:
 c.packet(p)
out=Y/'prime_patterns_root01'
assert json.loads((out/'report.json').read_text())['status']=='PASS_L114_PRIME_PATTERNS_AND_ONE_ACTUAL_PANEL_CERTIFICATE'
for p in out.iterdir():
 if p.is_file():c.add(p)
for n in ['page-12.png','page-19.png']:c.add(S/'sources/older_L114_ocr'/n)
c.add(__file__)
c.finish('geometry/suzuki_incidence/prime_patterns_root_review','ACCEPTED_L114_PRIME_SPLIT_NECESSITY_AND_LOCAL_ACTIONS',dict(
 reviewer='root',author='j3_recovery',
 review=[
 'Read the entire six-page proof and independently viewed all six freshly assembled native pages. Compared original printed pages54 and61: the three necessary patterns and prime rank/rank-two claims have exactly the stated scope.',
 'The prime subgroup-cover lemma follows from the explicit proper maximal-subgroup types. For a full split torus, scalar irreducibility and Z(U)=Phi(U) give the complete point-stabilizer overgroups; covers of an involution give only order-four or prime dihedral groups.',
 'The excluded triangle is proved by conjugating its split complement and reflection, then using fixed-point uniqueness and the quantified matrix identity (z(b)wz(b))21=b. This supplies the missing exclusion without assuming the source geometric orbit-intersection step.',
 'The two possible residues of D2p exhaust the necessary cases. Shared odd torus uniqueness excludes mixed dihedral cases; involution centralizers exclude two four-groups. Two successive maximal intersections inside D2p also establish the rank bound.',
 'The exact source definitions are kept distinct from full incidence panels. Regular algebraic local actions give the third pattern; full-panel double transitivity implies thinness and flag transitivity by the base orbit argument. The general literal-source thinness implication is explicitly still unpaid.',
 'The complete rank-two classification imports yield one class for q>8 and three for q8. Root checked the elementary local-action degree arguments and the q8 exceptional torus order.',
 'Read the entire independent GF8 literal certificate reader. Fresh replay verified every group product/inverse, generator closure, pair/triple intersection and complete coset panels; six damaged records and two optimization modes were rejected. Actual panel sizes2,2,2 confirm this one retained marking and give no counterexample.',
 'Classical Suzuki matrix, maximal-subgroup and torus premises remain explicit; no ambient group census, new conjecture, Lean or whole-source credit is inferred.'
 ],native_pages=6,source_claims=['Theorem5.3 necessary list','prime-q-minus-one rank bound','prime rank-two cases of Theorem6.1'],source_credit=0))

F=S/'computation/f009';W=F/'streaming_session1229_calls_work';old=F/'streaming_session_calls_work'
assert old.exists()
for n in ['protocol.py','batch.py','controls.py','run.py','collect.py']:
 actual=''.join(difflib.unified_diff((old/n).read_text().splitlines(True),(W/n).read_text().splitlines(True),fromfile='accepted895/'+n,tofile='prefix1229/'+n))
 assert actual==(W/(n+'.diff')).read_text(),n
assert (old/'protocol.py').read_text().replace("config['completed_prefix']==895","config['completed_prefix']==1229")== (W/'protocol.py').read_text()
assert (old/'run.py').read_bytes()==(W/'run.py').read_bytes()
assert (old/'collect.py').read_bytes()==(W/'collect.py').read_bytes()
c=m.Closure()
for p in ['streaming_session1229_calls_work','streaming_session_calls_root_review','dictionary_snapshot1229_root_review','streaming_batch01_root_adoption']:
 c.packet('computation/f009/'+p)
preflight=F/'streaming_session1229_profile_preflight01.json';c.add(preflight)
pr=json.loads(preflight.read_text())
assert pr['status']=='PASS_ACTUAL_IMPORTED_RUNTIME_AND_FIXED_PREMISE_PREFLIGHT'
for row in pr['bindings']:c.binding(row)
c.add(__file__)
c.finish('computation/f009/streaming_session1229_calls_root_review','ACCEPTED_F009_N94_STREAMING_DICTIONARY_SESSION_CALLER_V1',dict(
 reviewer='root',author='finite_recoveries',
 review=[
 'Read the complete application proof, protocol initialization and all five full-file deltas. Independently reproduced each delta: protocol changes only the fixed starting prefix, batch changes its matching initial constants, controls changes its synthetic artifact template, and run/collect are byte-identical.',
 'The separately accepted202283-key snapshot and outer prefix1229 are exact premises. Dictionary validity is not used to infer outer coverage. The session writer, loader, collector and transition predicates remain unchanged.',
 'Both initial complete parses occur independently inside the bounded production batch before its first writer; equality of dictionaries/read sets and distinct object ownership are still required. This is the same induction with a newly accepted base case.',
 'The existing full-size bootstrap is historical evidence for prefix895 only. No fresh1229 bootstrap is claimed. In this edition the bounded production initialization performs the mandatory current initial acquisitions; a separate duplicate probe is unnecessary.',
 'Rebound all declared dependencies and2167 actual imported-runtime/configuration preflight bindings. Retained25 controls cover8 tiny transitions; no numerical coverage comes from those fixtures.',
 'This accepts the caller interface only. A concrete immutable two-interval owner plan, its bounds and release remain separate; no automatic successor or new source credit.'
 ],starting_prefix=1229,total_outer_roots=14476,dictionary_keys=202283,new_target_runs=0,source_credit=0))
