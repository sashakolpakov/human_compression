import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013/L027_rank_five_work'
O=S/'corpus106_L027_rank_five_v1'
if O.exists():raise SystemExit('immutable author packet already exists')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('author_checker',W/'check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=mod.parse_finite((W/'finite01.stdout').read_bytes())
O.mkdir()
for name in ['rank_five.tex','rank_five.pdf','literal.py','finite.g','check.py','source_map.json','development.rst','prepare_packet.py']:
    shutil.copy2(W/name,O/name)
shutil.copy2(W/'literal01.json',O/'literal_expected.json')
write(O/'finite_expected.json',rows)
shutil.copy2(W/'finite01.stdout',O/'finite_initial.stdout')
write(O/'finite_initial_receipt.json',dict(status='PASS',session=71015,exit_code=0,tool_terminal_chunk='0e8896',
    command=['/opt/homebrew/bin/gap','-q','-b','finite.g'],cwd=str(W),
    output_policy='The initial leading carriage return and terminal chunk were displayed by the execution tool. The complete scientific terminal text is retained; no elapsed duration is inferred.',
    input=pin(W/'finite.g'),finite_models=16,full_subset_intersections=2048))
deps=[]
for p in [S/'sources/psl3_chiral2022.pdf',
          Path('/Users/sasha/medusa/math_compression/papers/topic-e/v3/umbrella.tex'),
          S/'reboot_20261013/L027_work/rank_five_notes.rst',
          S/'reboot_20261013/L027_work/rank_five_diagnostic.g',
          *sorted((S/'reboot_20261013/L027_work/rank_five_diagnostic01').glob('*')),
          W/'source02.png',W/'source08.png']:
    if p.is_file():deps.append(pin(p))
write(O/'dependencies.json',deps)
write(O/'scope.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',original='L027',
    claim='Complete rank-five family, Theorem 1.2 and Section 4, with explicit oriented/unbased and regular-full-group qualifications',
    author='l044_resume',root_contribution='Prior finite diagnostic and suggestion to begin with b^2 a^-1; no independent review of this new proof yet',
    native_pages=6,source_pages_directly_viewed=[2,8],
    exact_identities=67,finite_controls=16,full_subset_intersections=2048,
    whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():
        x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(deps))))
