from pathlib import Path
import datetime,json,hashlib,shutil
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L019_principal_distinct';A=S/'corpus106_L019_principal_v1';D=S/'corpus106_L019_principal_independent_review'
def pin(p,base=S):
 b=p.read_bytes();return {'path':str(p.relative_to(base)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
if pin(A/'manifest.json')['sha256']!='bf7b464283603675a940bc6de5f628275ac5e4263ab4e227704e56fa4e4fc370':raise RuntimeError('edition')
a=PdfReader(A/'principal.pdf');b=PdfReader(W/'replay01/principal.pdf');same=[x.extract_text()==y.extract_text()for x,y in zip(a.pages,b.pages)]
if len(a.pages)!=2 or len(b.pages)!=2 or not all(same):raise RuntimeError('native')
save(W/'native_review.json',{'native_pages':2,'all_pages_directly_viewed':True,'native_texts_identical':same,'source_required_statements_reread':True})
D.mkdir(exist_ok=False);shutil.copy2(W/'review_draft.rst',D/'review.rst');paths={A/'manifest.json'}
for row in json.loads((A/'manifest.json').read_text())['exports']:
 p=A/row['path']
 if pin(p,A)!=row:raise RuntimeError('export')
 paths.add(p)
for row in json.loads((A/'dependencies.json').read_text()):
 p=S/row['path']
 if pin(p)!=row:raise RuntimeError('dependency')
 paths.add(p)
root=S/'topic_B_L019_balanced_pairs_root_adoption/manifest.json'
paths.add(root)
for row in json.loads(root.read_text())['exports']:paths.add(root.parent/row['path'])
for name in ['L019_section9_contract_work','L019_principal_distinct']:
 for p in (S/'reboot_20261013'/name).rglob('*'):
  if p.is_file() and '__pycache__'not in p.parts:paths.add(p)
bindings=[pin(p)for p in sorted(paths)];save(D/'bindings.json',bindings)
r={'status':'ACCEPTED_L019_COMPLETE_PRINCIPAL_RECOVERY','edition':pin(A/'manifest.json'),'reviewer':'/root/publication_recovery','author':'/root/l044_resume','independence':'Earlier source-contract audit and distinct component reviews disclosed; no new mathematical proof contribution to this assembly. Exact degree-six point-conjugacy clarification retained.','full_review':pin(D/'review.rst',D),'fresh_report':pin(W/'replay01/report.json'),'fresh_session':59227,'exit_code':0,'all_two_native_pages_directly_viewed':True,'native_texts_identical':True,'principal_routes':['Theorems1.1/9.10: allkappa>=1 and n>=2kappa+3 with exact isomorphism/duality convention.','Explicit mutually inverse extension/contraction, insertion-choice equivalence, reversal and constructive odd-boundary reduction.','All six fixed-edition stable constants1,1,7,9,35,48 from complete independent wing censuses.'],'retained_auxiliary_corrections':['P2.4 unrestricted converse false','P2.5 diagram5b order240','P2.5 diagram9 valid S7 marking','T6.4 unrestricted extension false; repaired full kernel interfaces used'],'mathematical_principal_complete':True,'recommendation':'One corrected whole-original mathematical recovery, subject to separate complete portable closure and root admission.','remaining':['Public-only full proof/certificate transport and operational review.','Root registration/admission and public commit.'],'source_table_outside_stable_range_not_new_claim':True,'L042_separate_original':True,'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None,'binding_count':len(bindings),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};save(D/'review.json',r);save(D/'manifest.json',{'status':r['status'],'exports':[pin(D/n,D)for n in ['review.rst','review.json','bindings.json']],'whole_original_credit':0});print(json.dumps({'manifest':pin(D/'manifest.json'),'bindings':len(bindings)}))
