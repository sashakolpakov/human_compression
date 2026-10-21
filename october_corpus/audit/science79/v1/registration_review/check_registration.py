import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized execution required')
import ast,copy,hashlib,json,subprocess
from pathlib import Path
R=Path('/Users/sasha/medusa/math_compression');P=Path(__file__).resolve().parent;BASE='874af3649a926e09a97e62e608ba24b513e9eeec'
def need(b,s):
 if not b:raise ValueError(s)
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=R)
def load(name):return json.loads((R/name).read_text())
def bind(row):
 p=R/row['path'];b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def pin(name):
 b=(R/name).read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
oldc=json.loads(old('audit/corpus/latest.json'));newc=load('audit/corpus/latest.json')
need(set(newc['admitted_original_ids'])-set(oldc['admitted_original_ids'])=={'L019'},'one added')
need(set(oldc['admitted_original_ids'])<=set(newc['admitted_original_ids']),'none removed')
need(set(oldc['accessible_pending_original_ids'])-set(newc['accessible_pending_original_ids'])=={'L019'},'one pending removed')
need(set(newc['accessible_pending_original_ids'])<=set(oldc['accessible_pending_original_ids']),'none pending added')
need(newc['measured_original_ids']==oldc['measured_original_ids'] and len(newc['measured_original_ids'])==53,'measured unchanged')
need(newc['refuted_principal_original_ids']==oldc['refuted_principal_original_ids']==['F003'],'refutation unchanged')
need(newc['admitted_principal_originals']==79 and newc['handled_mathematical_originals']==80 and newc['accessible_pending_complete_recovery']==25,'counts')
catold=load(oldc['active_catalogue']['path']);cat=load(newc['active_catalogue']['path']);changed=[]
need(len(cat['entries'])==len(catold['entries'])==106,'106 original entries')
for a,b in zip(catold['entries'],cat['entries']):
 need(a['original_id']==b['original_id'],'same order and identity')
 if a!=b:changed.append(a['original_id'])
need(changed==['L019'],'only original L019 changed')
need(cat['current_recovery_counts']==dict(active=106,admitted=79,refuted=1,handled=80,measured=53,measurement_pending=26,pending=25,editorial=1),'partition')
oldp=json.loads(old('papers/catalogue_corrected_unmeasured.json'));newp=load('papers/catalogue_corrected_unmeasured.json')
need(newp['entries'][:-3]==oldp['entries'],'all old manuscript entries unchanged')
need(newp['original_ids']==oldp['original_ids']+['L019'],'one new manuscript original')
need(newp['acquired_dependencies']==oldp['acquired_dependencies'],'old acquired entries unchanged')
need([x['id']for x in newp['entries'][-3:]]==['L019-principal','L019-pure_bijection','L019-balanced_pairs'],'three new manuscript routes')
history=load('audit/science79/v1/history_routes.json')['routes']
for name,row in history.items():
 bind(row);need((R/row['path']).read_bytes()==old(name),'literal HEAD history '+name)
o=ast.parse(old('scripts/verify_snapshot.py'));n=ast.parse((R/'scripts/verify_snapshot.py').read_text())
func=lambda t:{x.name:ast.dump(x,include_attributes=False)for x in t.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name!='main'}
a,b=func(o),func(n);need(set(b)-set(a)=={'check_previous_science79','check_science79'},'two new wrappers');need(all(b[k]==v for k,v in a.items()),'old function AST preservation')
om=next(x for x in o.body if isinstance(x,ast.FunctionDef) and x.name=='main');nm=copy.deepcopy(next(x for x in n.body if isinstance(x,ast.FunctionDef) and x.name=='main'))
newbody=[];edits=[]
for x in nm.body:
 if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Name):
  v=x.targets[0].id
  if v=='science79_history':
   need(ast.unparse(x.value)=='check_previous_science79()','new history call');edits.append(v);continue
  if v=='science78_history':
   need(ast.unparse(x.value)=="science79_history['previous']",'history unwrap');x.value=ast.parse('check_previous_science78()',mode='eval').body;edits.append(v)
  if v=='science72':
   need(ast.unparse(x.value)=='check_science79()','new current call');x.value=ast.parse('check_science78()',mode='eval').body;edits.append(v)
 if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='print' and x.value.args and isinstance(x.value.args[0],ast.Constant) and x.value.args[0].value=='PASS: exact science78 history preserved; L019 complete corrected principal recovery adds one original.':
  x.value.args[0].value='PASS: historical L046 bounded correction preserved; L059 complete corrected principal recovery adds one original.';edits.append('message')
 newbody.append(x)
nm.body=newbody;need(ast.dump(nm,include_attributes=False)==ast.dump(om,include_attributes=False),'main only exact reviewed changes')
other=lambda t:[ast.dump(x,include_attributes=False)for x in t.body if not isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))];need(other(o)==other(n),'all nonfunction AST nodes unchanged')
ad=load('audit/recoveries/L019/v1/admission.json');scope=load('audit/recoveries/L019/v1/scope_routes.json');prop=load('audit/recoveries/L019/v1/admission_proposal.json')
need(len(ad['principal_claims'])==3 and ad['principal_claims']==scope['principal_contract'],'three exact claims')
need(len(ad['intermediate_corrections'])==4 and ad['intermediate_corrections']==scope['retained_auxiliary_corrections'],'four exact corrections')
for k in prop:
 if k not in ['status','manuscripts']:need(ad[k]==prop[k],'reviewed proposal '+k)
need(ad['new_native_manuscripts']==prop['manuscripts'],'three unchanged manuscripts')
need(ad['whole_original_credit']==0 and ad['publication_gate_remaining'] and ad['source_ids']==['L019'],'gated sole credit')
need(ad['counts']['boundary_classes']==[1,1,7,9,35,48] and ad['counts']['rooted_wings']==[1,1,6,3,11,19],'finite theorem data')
for x in ad['new_native_manuscripts']:bind(x['tex']);bind(x['pdf'])
for chain in [ad['component_acceptance']['complete']]+list(ad['complete_acquired_proofs'].values()):
 for row in chain.values():bind(row)
for k in ['portable_report','portable_transport','portable_checker','portable_adaptation']:bind(ad[k])
t=load(ad['portable_transport']['path']);payloads={x['public_path']:x for x in t['files']if 'public_path'in x}
for path,x in payloads.items():
 b=(R/path).read_bytes();need(hashlib.sha256(b).hexdigest()==x.get('stored_sha256',x['sha256']),'payload '+path)
need(len(payloads)==4660 and len(t['files'])==6652 and len(t['packets'])==439,'transport scope')
need(sum(x['transport'].endswith('HASH_ONLY')for x in t['files'])==45,'exact documentary omissions')
need('audit/science79/v1/new_original_registration.json' in (R/'README.rst').read_text(),'correct README science link')
files=['scripts/check_science79.py','scripts/check_science79_history.py','scripts/verify_snapshot.py','README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','audit/science79/v1/history_routes.json','audit/science79/v1/narrative_delta.json','audit/science79/v1/new_original_registration.json','audit/science79/v1/operational_review.json','audit/recoveries/L019/v1/admission.json','audit/recoveries/L019/v1/scope_routes.json','audit/recoveries/L019/v1/admission_proposal.json',newc['active_catalogue']['path'],newc['snapshot']['path'],'papers/recoveries/L019/v1/PUBLICATION.rst']
files+=list(history[k]['path']for k in history)
report={'status':'PASS_REGISTRATION_ONLY_INDEPENDENT_CHECK','base_commit':BASE,'changed_originals':changed,'counts':cat['current_recovery_counts'],'old_verifier_functions_preserved':len(a),'main_exact_reviewed_changes':edits,'history_files_literal_HEAD_matches':len(history),'public_payloads_rehashed':len(payloads),'new_manuscript_routes':3,'principal_claims':3,'auxiliary_corrections':4,'bindings':[pin(f)for f in files]}
(P/'check_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='bindings'}))
