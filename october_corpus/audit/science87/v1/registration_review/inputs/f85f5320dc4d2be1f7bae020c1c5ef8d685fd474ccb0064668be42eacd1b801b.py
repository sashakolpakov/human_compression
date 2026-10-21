#!/usr/bin/env python3
"""Freeze the already checked private science87 registration; no public writes."""
import hashlib,json,pathlib,re,subprocess
if not __debug__: raise SystemExit('Optimized execution is not allowed')
C=pathlib.Path(__file__).resolve().parent
R=pathlib.Path('/Users/sasha/medusa/math_compression')
T=C/'trial02'; D=C/'registration_drafts_v2'
BASE='ade9feeb7f8feaffa8f773932d57a50e60cb64c2'
def load(p): return json.loads(p.read_text())
def pin(p,base=C):
 b=p.read_bytes();return dict(path=str(p.relative_to(base)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(p,d):
 if p.exists(): raise RuntimeError('Refuse overwrite: '+str(p))
 p.write_text(json.dumps(d,indent=2)+'\n')
def git(root,*a): return subprocess.check_output(['git','-C',str(root),*a])
assert git(R,'rev-parse','HEAD').decode().strip()==BASE
assert not git(R,'status','--porcelain')
assert git(T,'rev-parse','HEAD').decode().strip()==BASE
pre=load(C/'preflight_trial02b/receipt.json')
assert pre['status']=='TERMINAL_PASS' and pre['returncode']==0
pr=load(C/'preflight_trial02b/stdout')
assert len(pr['controls'])==19 and pr['old_verifier_functions_preserved']==203 and pr['predecessor_paths']==36504
params=load(T/'audit/science87/v1/registration_parameters.json')
assert params['source_ids']==['L027','L036','L046','L063','L064','L076']
for sid,d in params['catalogue_dispositions'].items():
 assert d['original_fully_handled']==(sid in ['L027','L076'])
assert not (T/'audit/science87/v1/root_integration.json').exists()
assert not (T/'audit/science87/v1/registration_review').exists()
links=[]
for rel in ['README.rst','audit/completion.rst']:
 old=T/'audit/science87/v1/previous'/rel; new=T/rel
 pat=r'<([^<>\n]+)>`_'
 for target in sorted(set(re.findall(pat,new.read_text()))-set(re.findall(pat,old.read_text()))):
  if '://' in target or target.startswith('mailto:'): continue
  local=target.split('#',1)[0]
  if not local: continue
  resolved=(new.parent/local).resolve()
  assert resolved.is_relative_to(T.resolve()) and resolved.exists(),(rel,target)
  links.append(dict(document=rel,target=target,resolved=str(resolved.relative_to(T.resolve()))))
# Preserve logical identities of earlier pinned working editions without rebinding them.
aliases=[]
repair=load(C/'link_repair_trial02/report.json')
for change in repair['changes']:
 before=change['before']; after=change['after']
 assert pin(C/before['path'])==before
 assert pin(C/after['path'])==after
 aliases.append(dict(logical_path=after['path'],bytes=before['bytes'],sha256=before['sha256'],retained_exact_file=before['path']))
dump(C/'historical_aliases_v3.json',dict(status='EXACT_RETAINED_HISTORICAL_EDITION_ALIASES',aliases=aliases,records_unchanged=['trial01_successor_changes.json','candidate_manifest_v2.json','candidate_v2.diff'],reason='The preserved earlier records predate the L027 guide-link correction.'))
changed=[x.decode() for x in git(T,'diff','--name-only','-z').split(b'\0') if x]
added=[x.decode() for x in git(T,'ls-files','--others','--exclude-standard','-z').split(b'\0') if x]
assert len(changed)==9
files=[pin(T/x,T) for x in sorted(set(changed+added))]
dump(C/'candidate_manifest_v3.json',dict(status='PRIVATE_SCIENCE87_CANDIDATE_AWAITING_DISTINCT_REGISTRATION_AND_ROOT_GATES',baseline=BASE,files=files,public_writes=False))
(C/'candidate_v3.diff').write_bytes(git(T,'diff','--no-ext-diff'))
native=sorted((C/'native_trial02').glob('page-*.png'));assert len(native)==8
assert load(C/'native_trial02/receipt.json')['status']=='TERMINAL_PASS'
assert not re.search(r'Warning|Overfull|Underfull', (T/'audit/protocol.log').read_text())
guards=load(C/'guards_trial02/report.json');assert len(guards['cases'])==6
docs=load(C/'documentary_controls01.json');assert len(docs['checks'])==7
syms=load(C/'history_symlink_control01.json');assert syms['status']=='PASS' and syms['literal_symlinks']==2
dump(C/'final_controls_v3.json',dict(status='PASS_PRIVATE_SCIENCE87_HANDOFF',baseline=BASE,preflight=pin(C/'preflight_trial02b/receipt.json'),counts=pr['counts'],old_functions=203,predecessor_paths=36504,malformed_controls=19,optimization_guards=6,documentary_identity_controls=7,preserved_symlinks=2,new_local_links=links,protocol_pages=8,protocol_pages_directly_viewed=8,native_log_warnings=0,mathematical_censuses_repeated=0,new_measurements=0,new_question_credit=0,new_Lean_credit=0,public_writes=False,final_root_gates_written=False))
drafts=[pin(p) for p in sorted(D.iterdir()) if p.is_file()]
assert len(drafts)==5
dump(C/'registration_drafts_v3_manifest.json',dict(status='EXACT_PRIVATE_REGISTRATION_DRAFTS',files=drafts))
selected=set()
rootnames=['freeze_handoff_v3.py','verify_handoff.py','REGISTRATION_v3.rst','configure_bundle.py','bundle_config01.json','prepare_bundle.py','prepare_bundle_v2.py','prepare_registration.py','prepare_registration_v2.py','record_command.py','control_history_symlinks.py','history_symlink_control01.json','documentary_controls01.json','trial01_successor_changes.json','historical_aliases_v3.json','candidate_manifest_v2.json','candidate_v2.diff','candidate_manifest_v3.json','candidate_v3.diff','final_controls_v3.json','registration_drafts_v3_manifest.json']
selected.update(C/x for x in rootnames)
selected.update(C.glob('successor_*.diff'))
dirs=['bundle02','registration_drafts_v2','registration_drafts_trial01_preserved','link_repair_trial02','bundle02_receipt','clone_trial02','parameters_v2_receipt','install_trial01','preflight_trial01','install_trial02','preflight_trial02','preflight_trial02b','native_trial02','guards_trial02']
for name in dirs:
 selected.update(p for p in (C/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
selected.add(C/'bundle01/stage_manifest.json')
dump(C/'handoff_v3_manifest.json',dict(status='PRIVATE_REGISTRATION_HANDOFF_READY_FOR_DISTINCT_REVIEW_AND_ROOT_INSTALL',baseline=BASE,files=[pin(p) for p in sorted(selected)],candidate_manifest=pin(C/'candidate_manifest_v3.json'),public_writes=False))
ready=dict(status='READY_PRIVATE_SCIENCE87_HANDOFF_NO_PUBLIC_ADMISSION',baseline=BASE,manifest=pin(C/'handoff_v3_manifest.json'),candidate=pin(C/'candidate_manifest_v3.json'),drafts=pin(C/'registration_drafts_v3_manifest.json'),bundle=pin(C/'bundle02/stage_manifest.json'),controls=pin(C/'final_controls_v3.json'),guide=pin(C/'REGISTRATION_v3.rst'),private_candidate=str(T),reviewer='l044_resume',install_command=['/Users/sasha/.venvs/global/bin/python',str(D/'integrate_science87.py'),'--repo',str(R),'--bundle',str(C/'bundle02'),'--allow-public-write','--build-protocol'],root_preflight_command=['/Users/sasha/.venvs/global/bin/python',str(R/'scripts/check_science87.py'),'--repo',str(R),'--preflight'],verify_handoff_command=['/Users/sasha/.venvs/global/bin/python',str(C/'verify_handoff.py'),'--candidate',str(T)],root_only_actions=['public installation','final gates','full historical snapshot','commit','push'],owned_live_sessions=[],public_writes=False,new_measurements=0,new_question_credit=0,new_Lean_credit=0)
dump(C/'ready_v3.json',ready)
print(json.dumps(dict(ready=pin(C/'ready_v3.json'),manifest=ready['manifest'],candidate_files=len(files),handoff_files=len(selected),new_links=len(links))))
