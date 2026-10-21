from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_incidence/local_rank_v1')
r=json.loads((Y/'local_rank_root01/report.json').read_text());assert r['status']=='PASS_EXACT_INPUTS_AND_NATIVE_PROOF_ASSEMBLY' and r['native_pages']==3
for p in (Y/'local_rank_root01').iterdir():
 if p.is_file():c.add(p)
c.add(__file__)
c.finish('geometry/suzuki_incidence/local_rank_root_review','ACCEPTED_L114_UNBOUNDED_ALGEBRAIC_LOCAL_RANK_COUNTERFAMILY',dict(author='j3_recovery',reviewer='root',native_pages=3,review=[
 'Read the entire proof and retained scalar/subfield interfaces. Fresh25 exact bindings and identical three-page native assembly passed. All three new proof pages and freshly rendered source pages44–46 were viewed directly. The source explicitly quantifies over pregeometries of arbitrary rank and defines its local condition on algebraic residues at subflags of the distinguished chamber.',
 'Distinct odd relative prime degrees supply commuting Frobenius automorphisms, each fixing all other chosen vectors and moving its own. Applying these automorphisms minus identity proves both linear independence and every required intersection of the coordinate span with the selected subfields.',
 'For Q_W=Z_W B_t, all intermediate overgroups containing B_t correspond exactly to Ft-subspaces containing Ft, because the central translations are additive and H_t supplies all nonzero scalars. Thus deleting one coordinate is a maximal subgroup inclusion even though its index t is composite. Membership in a subfield is exactly membership of the central parameter.',
 'Every proper type subset is checked: without the soluble parabolic use a prime-degree simple subfield inclusion, at the final simple subfield use its maximal point stabilizer, and with the soluble parabolic use the one-dimensional quotient. All rank-one algebraic actions are either the classical Suzuki action on t^2+1 points or the full affine action on Ft, hence doubly transitive.',
 'The k=2 example is a rank3 geometry with composite q-1; every incident pair extends via its common representative. Arbitrary k gives pregeometries of unbounded rank. This refutes the two additional literal source assertions without claiming flag transitivity, full-panel local transitivity or higher-rank geometry. Parameters q=2^45 and2^315 give concrete symbolic examples, not enumerated ambient groups.',
 'Root suggested the Frobenius-isolation verification during drafting; the construction and full proof were authored by j3_recovery. Classical group structure and the previously accepted scalar-subspace theory remain attributed premises. No priority, open-conjecture, new original/principal count, Lean or compression credit is asserted.'
]))
