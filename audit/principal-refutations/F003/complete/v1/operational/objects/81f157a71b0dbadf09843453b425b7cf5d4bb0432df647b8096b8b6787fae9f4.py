from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_source_completion/source_synthesis_v1')
O=S/'geometry/suzuki_source_completion/source_synthesis_root01'
for p in O.rglob('*'):
 if p.is_file():c.add(p)
c.add(Path(__file__))
r=json.loads((O/'report.json').read_text())
if r['status']!='PASS_F003_SOURCE_ASSEMBLY':raise ValueError('Replay failed')
c.finish('geometry/suzuki_source_completion/source_synthesis_root_review','ACCEPTED_F003_COMPLETE_SOURCE_TREATMENT',dict(
 reviewer='root',author='j3_recovery',
 source='Spiga, arXiv:2010.04080v1,8 October2020; fixed four-page edition',
 mathematical_review=[
 'Read all four source pages in full extracted text and native images; compared all19 claim dispositions with the source. Viewed the fresh cover and all six supplement pages; read the entire unchanged accepted principal proof in TeX.',
 'The involution translate is a bijection because (xJ)^2=1 iff xJx=J. Symplecticity gives the equivalent symmetry condition. The retained involution count yields q^3-q^2+q, not q.',
 'An alternating Frobenius-semilinear defect vanishing on orthogonal pairs has only its14 and23 basis values, equal by the orthogonal pair(e1+e2,e3+e4). Hence D(u,v)=f(u,v)^t r. Conversely this formula vanishes on the required domain.',
 'Checked all ten equations from the four orthogonal basis products, the two four-coordinate defects, and their equality as off-diagonal symmetric symplectic equations. This proves the corrected symmetric-matrix membership criterion conditional on the explicitly quoted Wilson characterization.',
 'Checked every algebraic branch of the stronger system, its exhaustive choice of five entries, and the converse for J and the diagonal torus. The first branch contradicts CG+BI=1; the last uses2t^2=q and the inverse Frobenius exponent2t.',
 'The binary matrix has symmetric symplectic identity, zero four orthogonal defects and equal nonzero remaining defects, giving a uniform intermediate counterexample. This is separate from the accepted polytope construction.',
 'Endpoint normalization is valid. With endpoints in the smaller set Z, excluding J places them in T and the generated group lies in T semidirect C2. This is a conditional recovery only; replacing genuine X membership by Z membership is exactly the invalid step.',
 'Wilson characterization, classical Suzuki structure, quoted inaccessible Hubard-Leemans reduction and polytope reconstruction remain attributed premises. The excluded chapter gains no source credit. The accepted principal counterexample and its exact arithmetic are imported unchanged, not rerun or counted twice.'
 ],
 fresh_validation=dict(report=c.add(O/'report.json'),dependencies=129,source_claims=19,volume_pages=12,supplement_pages=6,imported_principal_pages=5,damage_rejections=6,optimization_rejections=2,complete_drawing_streams_and_glyph_programs_checked=True),
 fixed_source_claims_complete=True,remaining_fixed_source_claims=[],
 completion_disposition='Complete source treatment after principal refutation, with valid conditional arguments and explicit borrowed premises. Not an ordinary recovery of the false theorem.',
 new_ordinary_recovery_credit=0,new_principal_refutation_credit=0,new_open_conjecture_credit=0,
 registration_pending=True,new_group_searches=0,
 limits=['No claim about later source editions or historical priority.','No classification of every chiral Suzuki polytope.','No new Lean verification or compression measurement.']))
