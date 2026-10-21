from pathlib import Path
import json,hashlib,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L044_degree_sixteen_v1';W=S/'reboot_20261013/L044_degree_sixteen_distinct';D=S/'topic_B_L044_degree_sixteen_independent_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def need(c,m):
 if not c:raise RuntimeError(m)
need(not D.exists(),'frozen target exists');D.mkdir();files={}
def add(p,root='private_study',base=S,expected=None):
 h=sha(p);need(expected is None or expected==h,str(p));rel=str(p.relative_to(base));files[(root,rel)]={'root':root,'path':rel,'bytes':p.stat().st_size,'sha256':h}
add(A/'manifest.json')
for e in json.loads((A/'manifest.json').read_text())['exports']:add(A/e['path'],expected=e['sha256'])
deps=json.loads((A/'dependencies.json').read_text());roots={k:Path(v) for k,v in deps['root_locations'].items()}
for e in deps['bindings']:add(roots[e['root']]/e['path'],e['root'],roots[e['root']],e['sha256'])
# Root's adoption appeared after the immutable author dependency collection.
for p in (S/'topic_B_L044_binary_blocks_root_adoption').rglob('*'):
 if p.is_file():add(p)
for p in W.rglob('*'):
 if p.is_file():add(p)
shutil.copy2(W/'review.rst',D/'review.rst');shutil.copy2(W/'replay_report.json',D/'replay_report.json')
put(D/'dependencies.json',{'root_locations':{k:str(v) for k,v in roots.items()},'bindings':[v for k,v in sorted(files.items())]})
status='ACCEPTED_DEGREE_SIXTEEN_EXCLUSION_AND_CONDITIONAL_DOUBLE_OMISSION_BRANCH'
put(D/'review.json',{'status':status,'author_manifest_sha256':sha(A/'manifest.json'),'reviewer':'publication_recovery','reviewer_contributed_mathematics':False,'complete_new_proof_code_and_actual_acquired_interfaces_read':True,'fresh_full_exhaustion':True,'reference_calls':20478,'subset_pair_comparisons':5413998,'complete_families':8288,'transitive_families':0,'fresh_native_pages_directly_viewed':3,'conditional_binary_hypothesis_preserved':True,'whole_original_credit':0,'new_question_credit':0,'new_formal_credit':0,'measurement_credit':0})
put(D/'manifest.json',{'status':status,'exports':[{'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file()],'whole_original_credit':0})
C=S/'reboot_20261013/publication_agent_checkpoint.json';old=C.read_bytes();(C.parent/'publication_agent_checkpoint_history'/(hashlib.sha256(old).hexdigest()+'.json')).write_bytes(old);c=json.loads(old);c.update(written_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),current_live_handles={},all_owned_processes_terminal=True);c['L044_degree16_distinct'].update(status='TERMINAL_PASS_ACCEPTED',review_manifest=str((D/'manifest.json').relative_to(S)),review_manifest_sha256=sha(D/'manifest.json'),replay_report_sha256=sha(W/'replay_report.json'));c['next_review']='Await root new bounded review; F009 forced-residual packet awaiting distinct root review; all old jobs terminal, no unchanged retries.';put(C,c)
print(json.dumps({'manifest':str(D/'manifest.json'),'sha256':sha(D/'manifest.json'),'bindings':len(files),'checkpoint_sha256':sha(C)}))
