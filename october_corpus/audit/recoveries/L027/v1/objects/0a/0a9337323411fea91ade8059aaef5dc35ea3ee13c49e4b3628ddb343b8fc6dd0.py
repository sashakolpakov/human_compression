from pathlib import Path
import hashlib,json,shutil,importlib.util
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');W=S/'reboot_20261013/L027_odd_three_work';O=S/'corpus106_L027_odd_three_v1'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if O.exists():raise SystemExit('immutable author packet exists')
spec=importlib.util.spec_from_file_location('control',W/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
lines=m.parse((W/'finite01.stdout').read_bytes())
O.mkdir()
for name in ['odd_three.tex','odd_three.pdf','literal.py','finite.g','check.py','prepare_packet.py','build_packet_files.py']:shutil.copy2(W/name,O/name)
shutil.copy2(W/'literal01.json',O/'literal_expected.json');write(O/'finite_expected.json',lines)
write(O/'source_map.json',dict(original='L027',source=pin(S/'sources/psl3_chiral2022.pdf'),
 rows=[dict(source='Section5.1 physical11',route='Exact rank-two order classification and explicit sufficiency families; no conjugacy classification claimed'),
 dict(source='Section5.1 regular-unipotent Case2 physical11',route='Source bound 2(2,p) corrected to p in odd characteristic, four in characteristic two; final dihedral bound unchanged'),
 dict(source='Theorem5.1 physical12-15',route='Complete reducible odd rank-three subgroup classification, actual translation module and all end intersections'),
 dict(source='Theorem5.2 physical15',route='Explicit nonsingular diagonal form and retained natural Dickson alternatives; small S4/A5 types'),
 dict(source='Table3 rank2/3 rows physical21',route='All group alternatives and affine types, with the generic type row corrected'),
 dict(source='Table3 generic E_(qprime^2):D_(2k) row',route='Printed [k,4] and [k,k] replaced by [h,hprime],[h,2p],[hprime,2p], where h=order(lambda), hprime=order(-lambda), lambda+lambda^-1=2a; q5,a2 gives [3,6],[3,10],[6,10] in order300'),
 dict(source='Table3 projective-line rank3 classification attribution',route='Retained prior classifications are not re-enumerated here; the actual conic embedding and candidate types are proved')],
 retained_inputs=[dict(claim='Dickson subgroup classification in the natural projective-line embedding',attribution='Dickson; source Theorem5.2 cites Wilson25; same classical input is explicitly retained in accepted topic-e/v3'),dict(claim='String end-intersection criterion',attribution='Standard C-group criterion retained in the project common theory'),dict(claim='SO3(Fq) isomorphic to PGL2(q), odd q',attribution='Classical orthogonal/projective-line identification, also used on source physical15')],
 author='l044_resume',root_contribution='Task assignment and full-source scope direction only; no proof contribution',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
write(O/'scope.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',claim='Rank-two orders for all characteristics and complete odd rank-three subgroup alternatives, with corrected generic affine types',native_pages=5,source_pages_directly_viewed=[11,12,13,14,15,21],pending_source_obligations=['Source Section7 new exact PSU3(17) computational statement remains unpaid','Distinct review and complete principal source assembly'],whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
(O/'development.rst').write_text('Development and attribution\n===========================\n\nThe centre-axis normalization and displayed source matrices are attributed to\nLeemans--Vandenschrick. Our written argument uses their actual block action,\ntranslation kernel and complement intersections to recover all cases and correct\nthe generic affine type row. Dickson and SO3/PGL2 remain explicit retained\nclassical inputs. Finite controls are supplementary, not a universal census.\n\nThe first complete finite run (session99693) ended0 PASS with empty stderr.\nAll19 symbolic identities passed. Earlier diagnostic scripts are retained\nprivately; triangular01 emitted harmless global-variable syntax warnings. The\nfinal finite.g uses local functions and has clean stderr. Initial TeX builds\nhad ordinary unresolved references; final two passes are clean. One attempted\npre-freeze editorial command used a duplicated relative path and changed no\nfile; the subsequent absolute/current-directory edit succeeded. The conic\nparagraph explicitly includes Borel-type and unipotent subgroup exclusions.\nThe final manuscript has five pages, rather than the early anticipated four.\n\nNo new census, current-status question search, Lean work, measurement or\nwhole-original credit is claimed. Source Section7 is separately audited.\n')
paths=[S/'sources/psl3_chiral2022.pdf',W/'finite01.stdout',W/'finite01.stderr',W/'route01.rst',W/'diagnostic01.g',W/'diagnostic01.stdout',W/'diagnostic01.stderr',W/'triangular01.g',W/'triangular01.stdout',W/'triangular01.stderr']
paths.extend(sorted(W.glob('source-*.png')))
for rel in ['papers/topic-e/v3/sections/00-involutory-common.tex','papers/topic-e/v3/retained_inputs.json','papers/topic-e/v3/retained_source_maps.json','papers/topic-e/v3/provenance/independent_review.json']:
 paths.append(R/rel)
write(O/'dependencies.json',[pin(p) for p in paths])
exports=[]
for p in sorted(O.rglob('*')):
 if p.is_file():x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(paths))))
