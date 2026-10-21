import hashlib,importlib.util,json,shutil
from pathlib import Path
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression')
W=S/'reboot_20261013/L027_odd_four_work';O=S/'corpus106_L027_odd_four_v1'
if O.exists():raise SystemExit('immutable packet exists')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('local',W/'check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
initial=(W/'finite01.stdout').read_text().replace('\r','').replace('PASS_ALL_ODD_FOUR_CONTROLS','').strip()
extra=(W/'extension01.stdout').read_text().replace('\r','').replace('PASS_EXTENSION_CONTROL','').strip()
combined=(initial+'\n'+extra+'\nPASS_ALL_ODD_FOUR_CONTROLS\n').encode();rows=mod.parse(combined)
O.mkdir()
for name in ['odd_four.tex','odd_four.pdf','finite.g','literal.py','check.py','source_map.json','development.rst','prepare_packet.py']:
 shutil.copy2(W/name,O/name)
shutil.copy2(W/'literal01.json',O/'literal_expected.json');write(O/'finite_expected.json',rows)
(O/'initial_combined_receipt.stdout').write_bytes(combined)
write(O/'initial_receipt_map.json',dict(status='EXACT_CONCATENATION_OF_TWO_COMPLETED_CONTROLS',
 controls=[dict(script=pin(W/'finite_initial13.g'),stdout=pin(W/'finite01.stdout'),stderr=pin(W/'finite01.stderr'),session=63235,terminal_chunk='83be8b',exit_code=0),
           dict(script=pin(W/'extension_control.g'),stdout=pin(W/'extension01.stdout'),stderr=pin(W/'extension01.stderr'),tool_chunk='0d6792',exit_code=0)],
 operation='Remove each terminal marker, concatenate 13 original model rows and one extension model row, add the full terminal marker; final frozen checker freshly executes all14 together.'))
paths=[S/'sources/psl3_chiral2022.pdf',W/'source-01.png',W/'source-02.png',W/'finite_initial13.g',W/'finite01.stdout',W/'finite01.stderr',W/'extension_control.g',W/'extension01.stdout',W/'extension01.stderr',
 R/'papers/topic-e/v3/sections/00-involutory-common.tex',R/'papers/topic-e/v3/programs/required_finite.g',
 R/'papers/topic-e/v3/reports/program_logs/program_required_finite.stdout',R/'papers/topic-e/v3/provenance/independent_review.json',
 R/'papers/topic-e/v3/manifest.json',R/'audit/topic-e/v3/admission.json']
write(O/'dependencies.json',[pin(p) for p in paths])
write(O/'scope.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',original='L027',author='l044_resume',
 claim='Complete odd rank4 classification with directly regular alternatives and regular rank bound',
 native_pages=3,source_pages_directly_viewed=[16,17],
 acquired_result='Accepted Topic E projective classification; its finite census is not repeated',
 root_contribution='Source/task assignment only; no mathematical contribution to this new component',
 whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
exports=[]
for p in sorted(O.rglob('*')):
 if p.is_file():x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(paths))))
