from pathlib import Path
import importlib.util,json,hashlib,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_incidence/nonthin_application02')
r=json.loads((Y/'nonthin_root01/report.json').read_text())
assert r['status']=='PASS_L114_ONE_NONTHIN_SZ8_WITNESS' and r['native_pages']==3
for p in (Y/'nonthin_root01').iterdir():
 if p.is_file():c.add(p)
c.add(__file__)
c.finish('geometry/suzuki_incidence/nonthin_root_review','ACCEPTED_L114_Q8_LITERAL_THINNESS_COUNTEREXAMPLE',dict(author='j3_recovery',reviewer='root',review=[
 'Read the full proof, polynomial-arithmetic reader and source-definition comparison. Fresh complete finite and native checks passed; directly viewed all three newly assembled pages. The revised source convention is correctly left cosets, and the reader verifies each displayed extra representative against the complete panel.',
 'The explicit Suzuki recipes prove ambient membership. Prime product orders give dihedral parabolics of orders14,10,26; order gcds and distinct shared involutions give pair intersections2 and triple1. Maximal D14 and prime local indices give every RWPRI condition; algebraic rank-one residues are the two-point regular C2 action.',
 'The identity (ac)^2(ab)^3a=(bc)^6 supplies the third incident coset. Its order and the relation |ac|=5 exclude equality with either standard coset. Pairwise incidence extends all smaller flags in rank3, while absence of a common representative disproves flag transitivity.',
 'Complete literal panels have sizes3,3,3 and two common-representative chambers each. The separately required stronger actual-panel local-transitivity or flag-transitivity hypotheses are not claimed. This refutes only the literal q8 clause in the fixed edition; the q>8 branch remains unpaid.',
 'No new manuscript, principal refutation, open-conjecture, Lean or compression credit is issued.'
],actual_panel_sizes=[3,3,3],native_pages=3))
P=Y/'prime32_request01';c=m.Closure();c.packet('geometry/suzuki_incidence/prime32_request01')
req=json.loads((P/'request.json').read_text())
assert hashlib.sha256((P/'manifest.json').read_bytes()).hexdigest()=='8c1d86dad541beaf3fee702db74fbb37aa524b51717a3317cc048733fc3e4460'
assert hashlib.sha256((P/'request.json').read_bytes()).hexdigest()=='647dd7cdd589771e50be87298907dd4a33e34df0abb1de2bd8b0c124a1ef08e9'
for row in req['bindings']:c.binding(row)
assert (P/'run.py').read_bytes()==(Y/'fixed_pair_request01/run.py').read_bytes()
assert req['deadline_seconds']==30 and req['output_cap_bytes']==1048576 and req['authorized_invocations']==1 and req['automatic_successor'] is False
c.packet('geometry/suzuki_incidence/nonthin_root_review');c.add(__file__)
c.finish('geometry/suzuki_incidence/prime32_request01_root_review','ACCEPTED_L114_ONE_PRESCRIBED_SZ32_PANEL_REQUEST',dict(author='j3_recovery',reviewer='root',request_sha256='647dd7cdd589771e50be87298907dd4a33e34df0abb1de2bd8b0c124a1ef08e9',review=[
 'Read the complete target, mathematical argument, request and unchanged supervising owner. One248-candidate prescription in the retained F32 matrix model; no ambient-group or full involution enumeration. Pair and panel bounds follow from exact dihedral orders and verified intersections.',
 'The separate source branch applies because32-1=31 is prime. Maximal D62 and prime local indices give the same literal hypotheses as the accepted q8 witness if a returned candidate passes independent verification.',
 'One30second invocation,1MiB output,4GiB launch reserve and2GiB floor, exact initial/final hashes and owned-child cleanup. A negative scan concerns only this prescribed family. Any returned witness requires a separate reader and source-application proof. No automatic successor or mathematical credit.'
],authorized_invocations=1,automatic_successor=False))
