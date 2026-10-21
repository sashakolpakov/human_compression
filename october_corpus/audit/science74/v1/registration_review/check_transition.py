from pathlib import Path
import json,hashlib,ast,difflib,subprocess
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/F006_publication_work';R=W/'review_repo01';O=S/'reboot_20261013/F006_registration_distinct'
def load(p):return json.loads(p.read_text())
h=load(R/'audit/science74/v1/history_routes.json')['routes']; old=load(R/h['audit/corpus/latest.json']['path']);cur=load(R/'audit/corpus/latest.json')
assert set(cur['admitted_original_ids'])-set(old['admitted_original_ids'])=={'F006'}
assert set(old['accessible_pending_original_ids'])-set(cur['accessible_pending_original_ids'])=={'F006'}
sets=[set(cur[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']]
assert list(map(len,sets))==[74,1,30,1] and len(set.union(*sets))==106 and sum(map(len,sets))==106
oc=load(R/old['active_catalogue']['path']);nc=load(R/cur['active_catalogue']['path'])
om={r['original_id']:r for r in oc['entries']};nm={r['original_id']:r for r in nc['entries']};assert set(om)==set(nm)
assert [k for k in om if om[k]!=nm[k]]==['F006']
assert nm['F006']['current_principal_recovery']['historical_admission_evidence']==om['F006']['current_principal_recovery']
changed=[k for k in cur if cur[k]!=old.get(k)]
assert set(changed)=={'status','admitted_principal_originals','accessible_pending_complete_recovery','handled_mathematical_originals','handled_mathematical_original_ids','admitted_original_ids','accessible_pending_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','previous_snapshot','active_catalogue','current_science_registration','added_admissions','snapshot'}
assert cur['added_admissions'][:-1]==old['added_admissions']
for k in ['measured_original_ids','added_measurements','current_topic_replacements','principal_refutation_admissions']:assert old[k]==cur[k]
a=load(R/'audit/recoveries/F006/v1/admission.json');routes=load(R/'audit/recoveries/F006/v1/scope_routes.json');assert len(routes['rows'])==24
assert (R/a['source_routes']['path']).read_bytes()==(R/'audit/recoveries/F006/v1/scope_routes.json').read_bytes()
assert (R/'audit/recoveries/F006/v1/checker/portable.py').read_bytes()==(S/'reboot_20261013/F006_portable_check.py').read_bytes()
oldtree=ast.parse((R/h['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((R/'scripts/verify_snapshot.py').read_text())
def nods(t,exc):return [ast.dump(n,include_attributes=False)for n in t.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in exc)]
assert nods(oldtree,{'main'})==nods(newtree,{'main','check_previous_science74','check_science74'})
of=[n for n in oldtree.body if isinstance(n,ast.FunctionDef)and n.name!='main'];assert len(of)==175
oldmain=next(n for n in oldtree.body if isinstance(n,ast.FunctionDef)and n.name=='main');newmain=next(n for n in newtree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
class Rename(ast.NodeTransformer):
 def visit_Name(self,n):
  if n.id in {'check_previous_science73','check_science73'}:n.id=n.id.replace('73','74')
  return n
assert ast.dump(Rename().visit(oldmain),include_attributes=False)==ast.dump(newmain,include_attributes=False)
assert a['whole_original_credit']==0 and not (R/'audit/science74/v1/root_integration.json').exists()
for n in ['README.rst','audit/completion.rst','audit/protocol.tex']:
 diff=''.join(difflib.unified_diff((R/h[n]['path']).read_text().splitlines(True),(R/n).read_text().splitlines(True),fromfile='old/'+n,tofile='new/'+n));(O/(Path(n).name+'.diff')).write_text(diff);print(diff)
assert len(PdfReader(R/'audit/protocol.pdf').pages)==6
for p in a['new_native_manuscripts']:assert len(PdfReader(R/p['pdf']['path']).pages)==p['physical_pages']
pre=subprocess.run(['/Users/sasha/.venvs/global/bin/python',str(R/'scripts/check_science74.py'),'--repo',str(R),'--preflight'],capture_output=True,text=True);assert pre.returncode==0 and not pre.stderr; (O/'preflight_report.json').write_text(pre.stdout)
rep=dict(status='PASS_INDEPENDENT_EXACT_F006_TRANSITION',partition=[74,1,30,1],changed_originals=['F006'],unchanged_originals=105,changed_latest_keys=changed,old_nonmain_functions=175,main_changes='Only two dispatcher calls renamed 73 to74',source_routes=24,immediate_documents=9,immediate_pages=21,prior_measurements_unchanged=True,final_credit_requires_absent_root_gate=True)
(O/'exact_transition_report.json').write_text(json.dumps(rep,indent=2)+'\n');print(json.dumps(rep))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r95','-dFirstPage=1','-dLastPage=3','-sOutputFile='+str(O/'protocol-page-%d.png'),str(R/'audit/protocol.pdf')],check=True)
