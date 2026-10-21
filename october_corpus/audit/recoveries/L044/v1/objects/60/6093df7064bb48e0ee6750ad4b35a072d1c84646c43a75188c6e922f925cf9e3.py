from pathlib import Path
import json,hashlib,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');A=S/'topic_B_L044_symmetric_central_pairs_v1';W=S/'reboot_20261013/L044_symmetric_central_pairs_distinct';D=S/'topic_B_L044_symmetric_central_pairs_independent_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def need(c,m):
 if not c:raise RuntimeError(m)
need(not D.exists(),'target exists');D.mkdir();files={}
def add(p,h=None):
 d=sha(p);need(h is None or d==h,str(p));root,base=('private_study',S) if p.is_relative_to(S) else ('public_repository',R);rel=str(p.relative_to(base));files[(root,rel)]={'root':root,'path':rel,'bytes':p.stat().st_size,'sha256':d}
for p,h in json.loads((W/'input_pins.json').read_text()).items():add(Path(p),h)
for p in W.rglob('*'):
 if p.is_file():add(p)
for a,b in [('review.rst','review.rst'),('replay_report.json','replay_report.json'),('finite01/report.json','finite_report.json')]:shutil.copy2(W/a,D/b)
put(D/'dependencies.json',{'root_locations':{'private_study':str(S),'public_repository':str(R)},'bindings':[v for k,v in sorted(files.items())]})
status='ACCEPTED_SYMMETRIC_CENTRAL_PAIR_KERNEL_EXCLUSION'
put(D/'review.json',{'status':status,'author_manifest_sha256':sha(A/'manifest.json'),'reviewer':'publication_recovery','reviewer_contributed_mathematics':False,'complete_new_proof_and_actual_acquired_interfaces_read':True,'forest_lemma_uses_no_intersection_property':True,'full_independent_S8_rank6_census_replayed':True,'finite_ordered_classes':2,'no_quotient_intersection_property_or_extension_splitting_assumed':True,'native_pages_directly_viewed':4,'whole_original_credit':0,'new_question_credit':0,'new_formal_credit':0,'measurement_credit':0})
put(D/'manifest.json',{'status':status,'exports':[{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file()],'whole_original_credit':0})
C=S/'reboot_20261013/publication_agent_checkpoint.json';old=C.read_bytes();(C.parent/'publication_agent_checkpoint_history'/(hashlib.sha256(old).hexdigest()+'.json')).write_bytes(old);c=json.loads(old);now=datetime.datetime.now(datetime.timezone.utc).isoformat();c.update(written_utc=now,updated_utc=now,current_live_handles={},all_owned_processes_terminal=True,current_assignment='Completed q5, degree16 and symmetric central-kernel distinct reviews; awaiting root next bounded review. F009 forced-residual interface awaits root review; no automatic timeout retries.');c['authoritative_live_state'].update(observed_utc=now,status='NO_OWNED_LIVE_PROCESSES',live_handles={});c['authoritative_live_state']['latest_terminal_handles']['L044_symmetric_central_pairs_distinct']=90895;c['authoritative_live_state']['terminal_receipts'].append('reboot_20261013/L044_symmetric_central_pairs_distinct/replay_report.json');c['L044_symmetric_central_pairs_distinct']={'status':'TERMINAL_PASS_ACCEPTED','session':90895,'review_manifest':str((D/'manifest.json').relative_to(S)),'review_manifest_sha256':sha(D/'manifest.json'),'whole_original_credit':0};put(C,c)
print(json.dumps({'manifest':str(D/'manifest.json'),'sha256':sha(D/'manifest.json'),'bindings':len(files),'checkpoint_sha256':sha(C)}))
