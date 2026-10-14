from pathlib import Path
import hashlib,json,shutil,importlib.util
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L027_rank_obstruction_work';O=S/'corpus106_L027_rank_obstruction_v1'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if O.exists():raise SystemExit('immutable author packet exists')
spec=importlib.util.spec_from_file_location('control',W/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
lines=m.parse((W/'finite01.stdout').read_bytes())
O.mkdir()
for name in ['rank_obstruction.tex','rank_obstruction.pdf','literal.py','finite.g','check.py','prepare_packet.py']:shutil.copy2(W/name,O/name)
shutil.copy2(W/'literal01.json',O/'literal_expected.json');write(O/'finite_expected.json',lines)
write(O/'source_map.json',dict(original='L027',source=pin(S/'sources/psl3_chiral2022.pdf'),
 rows=[dict(source='Theorem1.3, physical2; Section6 physical22-23',route='Entire uniform rank obstruction, including PSU3(2)'),
       dict(source='Lemma2.3 physical4-5',route='Actual indexed IP gives both directly regular ends and exact index2'),
       dict(source='Lemma6.1 physical22',route='Proper normal direct product explicitly proved from indexed IP'),
       dict(source='Lemma6.2 physical22, attributed to Schulte-Weiss',route='Four interval relations give a short direct proof; original attribution retained'),
       dict(source='Even rank6, physical23',route='Corrected point/line orientation argument using actual elation centres and distant commutation'),
       dict(source='Odd rank6, physical23',route='Actual Heisenberg dual orientation and explicit projective-scalar removal'),
       dict(source='Simplex alternative q=5, physical22',route='Characteristic5, with extension fields included; A7 order excludes every ambient group'),
       dict(source='PSU3(2) historical no-chiral census',route='Not acquired as a complete census; elementary no-commuting-involutions proof covers every rank required by Theorem1.3')],
 retained_inputs=['Classical chiral group characterization','Simplicity and order formulas for PSL3/PSU3','Coxeter A6 rotation presentation A7','Separately reviewed complete regular subgroup normal forms'],
 author='l044_resume',root_contribution='Assignment and source-scope direction only; no mathematical contribution to this component',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
write(O/'scope.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',claim='No chiral rank greater than5 for PSL3(q) and PSU3(q), all q>=2',native_pages=4,source_pages_directly_viewed=[22,23],pending_source_obligations=['Broader odd rank3 and rank2 subgroup clauses','Small historical chiral censuses and unitary examples'],whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
(O/'development.rst').write_text('Development and attribution\n===========================\n\nThe initial route is retained privately. The first native build had ordinary\nunresolved references and one wide matrix display; a second pass and a\ntwo-row display corrected them before freezing. All15 exact identities and\nall bounded GAP controls passed their first execution. The GAP session32539\nended0, terminal b7f4ad. The whole proof is written; these controls are not a\nuniversal census. No prior bounded target was repeated or claimed as new.\n\nThe odd normal-form component has a completed distinct acceptance, while\nits separate root adoption may follow this freeze. The even component is\nroot adopted. Their exact proofs and review manifests are acquired below.\n')
paths=[S/'sources/psl3_chiral2022.pdf',W/'source-01.png',W/'source-02.png',W/'finite01.stdout',W/'finite01.stderr',W/'route01.rst']
for name in ['corpus106_L027_even_subgroups_v1','corpus106_L027_odd_four_v2']:
 P=S/name;paths.extend([P/'manifest.json',P/'dependencies.json',P/('even_subgroups.tex' if 'even' in name else 'odd_four.tex')])
for name in ['corpus106_L027_even_subgroups_independent_review','corpus106_L027_even_subgroups_root_adoption','corpus106_L027_odd_four_independent_review']:
 P=S/name;paths.extend([P/'manifest.json',P/'dependencies.json',P/'review.json'])
 if (P/'review.rst').exists():paths.append(P/'review.rst')
write(O/'dependencies.json',[pin(p) for p in paths])
exports=[]
for p in sorted(O.rglob('*')):
 if p.is_file():x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(paths))))
