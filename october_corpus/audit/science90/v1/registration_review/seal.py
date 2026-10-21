import sys,json,hashlib,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
S=Path('/Users/sasha/medusa/research/leemans');W=S/'geometry/chiral_atlases/publication_work';R=Path('/Users/sasha/medusa/math_compression');D=W/'registration_root_review'
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
assert not D.exists();z=json.loads((W/'registration_root_preflight01.stdout').read_text());assert z['status']=='PASS_SCIENCE90_L070_RECOVERY' and not(W/'registration_root_preflight01.stderr').read_bytes();assert z['counts']['corrected_recoveries']==90 and z['predecessor_paths']==41813
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()=='73a899be01768df4e8f5079426a3c82b6d876434'
paths=set(subprocess.check_output(['git','diff','HEAD','--name-only','-z'],cwd=R).decode().split('\0'))|set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=R).decode().split('\0'));paths.discard('')
allowed={'README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py','scripts/check_science90.py','audit/protocol.tex','audit/protocol.pdf','audit/corpus/accessible106/updates/science90-L070-catalogue.json','audit/corpus/updates/accessible106-science90-L070.json'}
assert all(n in allowed or n.startswith(('audit/science90/','audit/recoveries/L070/','papers/recoveries/L070/'))for n in paths)
bindings=[pin(R/n)for n in sorted(paths)]
D.mkdir()
for name,p in [('installed_preflight.json',W/'registration_root_preflight01.stdout'),('installation_handoff.json',W/'registration_handoff01.json'),('installer.py',W/'registration90_drafts/install_science90.py'),('checker.py',W/'registration90_drafts/check_science90.py'),('finalize.py',W/'finalize_science90.py'),('protocol_page5.png',W/'protocol_page5_root.png'),('seal.py',Path(__file__))]:shutil.copyfile(p,D/name)
put(D/'dependencies.json',bindings)
put(D/'review.json',dict(status='ACCEPTED_SCIENCE90_REGISTRATION',reviewer='/root',registration_author='/root/l070_publication',utc=datetime.now(timezone.utc).isoformat(),source_ids=['L070'],baseline='73a899be01768df4e8f5079426a3c82b6d876434',scientific_acceptance='4720efe6602ba25047dc7546c67734850fcf95485d839f280e7a4fdfbf6688da',operational_acceptance='7f14c5d4be456642367b6b711fa2e746ac287e0420c81fd9f5168f2857b4a09f',read=['Complete concrete installer and registration checker; exact handoff and native/source admission proposal.','All twenty-one documentary replacements, full current counts and source qualifications; the actual new L070 protocol page was rendered and directly viewed.','The new verifier main checks the accepted predecessor bytes and current transition; all209 previous non-main functions are unchanged. The old main is preserved. Historical mathematical replays are acquired, explicitly not rerun.','The operational wrapper maps all4032 original review bindings bijectively to exact public bytes. The segmented transport is bound by whole pack files and the independently passed full portable replay; no incomplete flat descriptor is substituted.','The actual installed preflight verifies all41813 predecessor paths, source/native/catalogue joins, disjoint106-original partition and18 negative admission controls. All non-L070 source records and measurements are unchanged.'],fresh_validation=dict(session=18901,exit_code=0,report=z,protocol_pages=8,protocol_layout_warnings=False,changed_source_page_directly_viewed=5,new_censuses=0,new_group_calls=0),decision='Accept the exact installed L070 registration, adding one corrected principal recovery. Final source/shared root gates, tracked manifest, commit and remote publication follow separately.',counts=z['counts'],new_measurements=0,new_question_credit=0,new_Lean_credit=0,whole_intake_complete=False,network='Current ordinary fetch failed DNS; sandbox escalation was rejected. No claim of remote publication is made by this local review.',candidate_files=len(bindings),all_source_assertions_reproved=False,scope='Fixed twelve-page source,46 clauses,16 complete manuscripts totaling41pages; prior mathematical, computational and documentary premises remain explicit. Remaining valid obligations of principal-refuted sources are not treated as whole recoveries.'))
exports=[]
for p in sorted(D.iterdir()):
 q=pin(p);q['path']=p.name;exports.append(q)
put(D/'manifest.json',dict(status='ACCEPTED_SCIENCE90_REGISTRATION',exports=exports));print(json.dumps(pin(D/'manifest.json')))
