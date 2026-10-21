import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013/L027_even_subgroups_work'
O=S/'corpus106_L027_even_subgroups_v1'
if O.exists():raise SystemExit('immutable packet exists')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('local_checker',W/'check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=mod.parse((W/'finite04.stdout').read_bytes());O.mkdir()
for name in ['even_subgroups.tex','even_subgroups.pdf','finite.g','check.py','source_map.json','development.rst','prepare_packet.py']:
    shutil.copy2(W/name,O/name)
write(O/'finite_expected.json',rows)
shutil.copy2(W/'finite04.stdout',O/'finite_initial.stdout')
write(O/'finite_initial_receipt.json',dict(status='PASS',session=52005,exit_code=0,tool_terminal_chunk='076072',
     command=['/opt/homebrew/bin/gap','-q','-b','finite.g'],cwd=str(W),input=pin(W/'finite.g'),
     rank_three_models=118,rank_four_models=61,subset_intersections=17024,
     note='Tool wait completed before final tail inspection; the complete terminal receipt is retained. No elapsed time is inferred.'))
deps=[pin(S/'sources/psl3_chiral2022.pdf')]
for pattern in ['source-*.png','finite_development*.g','finite0[1-3].stdout','finite0[1-3].stderr','diagnostic*.g','diagnostic*.stdout','diagnostic*.stderr']:
    deps.extend(pin(p) for p in sorted(W.glob(pattern)))
write(O/'dependencies.json',deps)
write(O/'scope.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',original='L027',author='l044_resume',
    claim='Complete even-characteristic Theorems5.4–5.6 with exact translation fields and actual intersection conditions',
    native_pages=4,source_pages_directly_viewed=[17,18,19,20,21],
    root_contribution='Source task assignment only; no mathematical contribution to this new component',
    whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None))
exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():x=pin(p);x['path']=str(p.relative_to(O));exports.append(x)
write(O/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(deps))))
