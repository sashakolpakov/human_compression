import datetime,hashlib,json,shutil
from pathlib import Path
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L019_balanced_pairs_distinct';A=S/'topic_B_L019_balanced_pairs_v1';D=S/'topic_B_L019_balanced_pairs_independent_review'
def pin(p,base=S):
 b=p.read_bytes();return {'path':str(p.relative_to(base)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
if pin(A/'manifest.json')['sha256']!='1ef6054e29bd9e34358cb24d90fcb23844b66129ed4ead280905d5fc4876cfd4':raise RuntimeError('edition')
report=json.loads((W/'replay01/report.json').read_text());independent=json.loads((W/'independent_audit.json').read_text());native=json.loads((W/'native_review.json').read_text())
if report['status']!='PASS' or len(report['fresh_complete_censuses'])!=6 or independent['status']!='PASS' or not native['all_pages_directly_viewed']:raise RuntimeError('review incomplete')
D.mkdir(exist_ok=False);shutil.copy2(W/'review_draft.rst',D/'review.rst')
paths={A/'manifest.json'}
for row in json.loads((A/'manifest.json').read_text())['exports']:
 p=A/row['path'];actual=pin(p,A)
 if actual!=row:raise RuntimeError('export '+row['path'])
 paths.add(p)
for row in json.loads((A/'dependencies.json').read_text()):
 p=S/row['path'];actual=pin(p)
 if actual!=row:raise RuntimeError('binding '+row['path'])
 paths.add(p)
for p in W.rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:paths.add(p)
paths.add(S/'reboot_20261013/L019_balanced_pair_working_audit/report.json')
bindings=[pin(p)for p in sorted(paths)];save(D/'bindings.json',bindings)
r={'status':'ACCEPTED_L019_BALANCED_PAIR_FINITE_BASES','author':'/root/l044_resume','reviewer':'/root/publication_recovery','edition':pin(A/'manifest.json'),'independence':'Reviewer read the working proof and requested explicit degree-six rooted point-conjugacy convention; no new mathematical proof step contributed. Earlier source-contract and acquired-component reviews disclosed. Rooted-orbit/leaf/balanced-pair audits are supplementary independent controls.','full_review':pin(D/'review.rst',D),'fresh_validation':{'report':pin(W/'replay01/report.json'),'session_id':75517,'exit_code':0,'complete_censuses':report['fresh_complete_censuses'],'exports':97,'bindings':116,'optimization_guards':2,'malformed_literal_guards':3,'all_native_pages_directly_viewed':True,'native_pages':3,'native_texts_identical':True},'independent_controls':{'report':pin(W/'independent_audit.json'),'literal_degree6_rooted_orbit_union':720,'direct_leaf_extension_subset_pairs':1616,'actual_balanced_pairs_and_class_distinctions':101,'executed_receipts_rehashed':6,'all_literal_Read_targets_retained':True},'accepted_scope':['Uniform unique balanced pure-pair and unordered rooted-wing bijection at degree2*kappa+3/rankkappa+3.','Complete rooted-wing counts1,1,6,3,11,19 in degrees2,4,6,8,10,12.','All six source stable constants1,1,7,9,35,48, plus actual class representatives and transfer through the acquired stability theorem.'],'qualifications':['No abstract outer-Aut(S6) quotient of degree-six wings.','No external atlas completeness premise.','All capped/failed attempts and unused v4 remain historical, without count credit.','Does not certify source Table1 cells outside the declared stable ranges.','Whole-original principal assembly/admission remains separate.'],'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None,'binding_count':len(bindings),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
save(D/'review.json',r);save(D/'manifest.json',{'status':r['status'],'exports':[pin(D/x,D)for x in ['review.rst','review.json','bindings.json']],'whole_original_credit':0});print(json.dumps({'manifest':pin(D/'manifest.json'),'bindings':len(bindings)}))
