import sys
if sys.flags.optimize: raise RuntimeError('Unoptimized execution required')
import ast,copy,hashlib,json,subprocess
from pathlib import Path
R=Path('/Users/sasha/medusa/math_compression');P=Path(__file__).resolve().parent
BASE='4489312252d0434841786163df4475e45b61b0d1'
def need(b,s):
 if not b:raise ValueError(s)
def old(n):return subprocess.check_output(['git','show',BASE+':'+n],cwd=R)
def load(n):return json.loads((R/n).read_text())
def bind(x):
 b=(R/x['path']).read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'binding '+x['path'])
def pin(n):
 b=(R/n).read_bytes();return dict(path=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
o=json.loads(old('audit/corpus/latest.json'));n=load('audit/corpus/latest.json')
for k in ('admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids'):
 need(n[k]==o[k]+['L042'],'exact appended original '+k)
need(set(o['accessible_pending_original_ids'])-set(n['accessible_pending_original_ids'])=={'L042'} and set(n['accessible_pending_original_ids'])<=set(o['accessible_pending_original_ids']),'pending only L042')
need(n['measured_original_ids']==o['measured_original_ids'] and len(n['measured_original_ids'])==53,'measured unchanged')
need(n['refuted_principal_original_ids']==o['refuted_principal_original_ids']==['F003'],'refutation unchanged')
cat=load(n['active_catalogue']['path']);before=load(o['active_catalogue']['path']);changed=[]
need(len(cat['entries'])==len(before['entries'])==106,'106 originals')
for a,b in zip(before['entries'],cat['entries']):
 need(a['original_id']==b['original_id'],'same original order')
 if a!=b:changed.append(a['original_id'])
need(changed==['L042'],'sole original change')
counts=dict(active=106,admitted=80,refuted=1,handled=81,measured=53,measurement_pending=27,pending=24,editorial=1)
need(cat['current_recovery_counts']==counts,'exact partition')
np=load('papers/catalogue_corrected_unmeasured.json');op=json.loads(old('papers/catalogue_corrected_unmeasured.json'))
need(np['entries'][:-1]==op['entries'] and np['entries'][-1]['id']=='L042-principal','one manuscript route')
need(np['original_ids']==op['original_ids']+['L042'] and np['acquired_dependencies']==op['acquired_dependencies'],'prior native entries unchanged')
h=load('audit/science80/v1/history_routes.json');need(h['baseline_commit']==BASE,'actual Git predecessor')
for name,x in h['routes'].items():bind(x);need((R/x['path']).read_bytes()==old(name),'literal historical Git bytes '+name)
need(len(h['routes'])==8,'eight preserved files')
ot=ast.parse(old('scripts/verify_snapshot.py'));nt=ast.parse((R/'scripts/verify_snapshot.py').read_text())
def funcs(t):return {x.name:ast.dump(x,include_attributes=False)for x in t.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))and x.name!='main'}
of,nf=funcs(ot),funcs(nt);need(len(of)==187,'prior function count')
need(set(nf)-set(of)=={'check_previous_science80','check_science80'} and all(nf[k]==v for k,v in of.items()),'187 old non-main ASTs unchanged')
om=next(x for x in ot.body if isinstance(x,ast.FunctionDef)and x.name=='main');nm=copy.deepcopy(next(x for x in nt.body if isinstance(x,ast.FunctionDef)and x.name=='main'))
body=[];edits=[]
for x in nm.body:
 if isinstance(x,ast.Assign)and isinstance(x.targets[0],ast.Name):
  name=x.targets[0].id
  if name=='science80_history':need(ast.unparse(x.value)=='check_previous_science80()','history call');edits.append(name);continue
  if name=='science79_history':need(ast.unparse(x.value)=="science80_history['previous']",'history unwrapping');x.value=ast.parse('check_previous_science79()',mode='eval').body;edits.append(name)
  if name=='science72':need(ast.unparse(x.value)=='check_science80()','current call');x.value=ast.parse('check_science79()',mode='eval').body;edits.append(name)
 if isinstance(x,ast.Expr)and isinstance(x.value,ast.Call)and isinstance(x.value.func,ast.Name)and x.value.func.id=='print'and x.value.args and isinstance(x.value.args[0],ast.Constant)and x.value.args[0].value=='PASS: exact science79 history preserved; L042 explicit classification adds one original.':
  x.value.args[0].value='PASS: exact science78 history preserved; L019 complete corrected principal recovery adds one original.';edits.append('message')
 body.append(x)
nm.body=body;need(ast.dump(nm,include_attributes=False)==ast.dump(om,include_attributes=False),'exact main changes only')
other=lambda t:[ast.dump(x,include_attributes=False)for x in t.body if not isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))]
need(other(ot)==other(nt),'all other top-level ASTs unchanged')
a=load('audit/recoveries/L042/v1/admission.json');s=load('audit/recoveries/L042/v1/scope_routes.json');p=load('audit/recoveries/L042/v1/admission_proposal.json')
for k in p:
 if k not in ('status','manuscripts'):need(a[k]==p[k],'immutable reviewed proposal '+k)
need(a['new_native_manuscripts']==p['manuscripts'],'exact manuscript')
need(a['principal_claims']==s['principal_claims']and len(s['principal_claims'])==4,'four claims')
need(a['intermediate_corrections']==s['qualifications']and len(s['qualifications'])==3,'three qualifications')
need(a['ancillary_scope']==s['ancillary_scope'] and not a['all_original_assertions_claimed'],'ancillary boundary')
need(a['counts']==dict(defect_family_counts=[1,1,7,9],source_diagrams=18,complete_base_matches=18,subdivision_controls=108),'exact finite controls')
need(a['whole_original_credit']==0 and a['publication_gate_remaining']and a['source_ids']==['L042'],'root-only gate')
need(a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and a['compression_factor']is a['software_inclusive_factor']is None and not a['measured'],'no added metrics or questions')
for m in a['new_native_manuscripts']:bind(m['tex']);bind(m['pdf'])
for x in list(a['component_acceptance']['complete'].values())+list(a['complete_acquired_proofs'].values()):bind(x)
for k in ('portable_transport','portable_checker','portable_report','portable_adaptation','source_figure_records','exact_diagram_report'):bind(a[k])
t=load(a['portable_transport']['path']);payloads={x['public_path']:x for x in t['files']if 'public_path'in x}
for name,x in payloads.items():
 b=(R/name).read_bytes();need(hashlib.sha256(b).hexdigest()==x.get('stored_sha256',x['sha256']),'payload '+name)
need(len(payloads)==4702 and len(t['files'])==6712 and len(t['packets'])==441,'full transport sizes')
need(sum(x['transport'].endswith('HASH_ONLY')for x in t['files'])==49,'exact documentary omissions')
readme=(R/'README.rst').read_text();need('audit/science80/v1/new_original_registration.json' in readme and '**80 accessible originals' in readme and 'Thus 81 of 105' in readme,'current public prose')
files=['scripts/check_science80.py','scripts/check_science80_history.py','scripts/verify_snapshot.py','README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','audit/science80/v1/history_routes.json','audit/science80/v1/narrative_delta.json','audit/science80/v1/new_original_registration.json','audit/science80/v1/operational_review.json','audit/science80/v1/registration_parameters.json','audit/recoveries/L042/v1/admission.json','audit/recoveries/L042/v1/scope_routes.json','audit/recoveries/L042/v1/admission_proposal.json',n['active_catalogue']['path'],n['snapshot']['path'],'papers/recoveries/L042/v1/PUBLICATION.rst']+[x['path']for x in h['routes'].values()]
out=dict(status='PASS_REGISTRATION_ONLY_INDEPENDENT_CHECK',base_commit=BASE,changed_originals=changed,counts=counts,old_verifier_functions_preserved=len(of),main_exact_reviewed_changes=edits,history_files_literal_Git_matches=8,public_payloads_rehashed=len(payloads),new_manuscript_routes=1,principal_claims=4,qualifications=3,bindings=[pin(f)for f in files])
(P/'check_report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='bindings'}))
