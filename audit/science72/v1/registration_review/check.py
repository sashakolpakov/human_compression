from pathlib import Path
import ast,hashlib,json,importlib.util
S=Path(__file__).resolve().parents[2];R=S.parents[1]/'math_compression';W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
a=load(R/'audit/recoveries/L071/v1/admission.json');scope=load(R/'audit/recoveries/L071/v1/scope_routes.json');cur=load(R/'audit/corpus/latest.json');history=load(R/'audit/science72/v1/history_routes.json')['routes'];old=load(R/history['audit/corpus/latest.json']['path'])
assert scope==load(S/'reboot_20261013/L071_integration_work/scope_routes.json')
assert [r['id'] for r in scope['routes']]==['C'+str(i).zfill(2) for i in range(1,16)]
assert {p for r in scope['routes'] for p in r['physical_pages']}==set(range(1,15))
assert a['explicit_corrections']==scope['explicit_corrections']
assert a['whole_original_credit']==scope['whole_original_credit']==0
assert a['publication_gate']=='audit/science72/v1/root_integration.json'
assert a['literal_theorem_sets_equivalent'] is a['all_original_assertions_claimed'] is False
assert cur['admitted_original_ids']==sorted(old['admitted_original_ids']+['L071'])
assert set(cur['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L071'}
assert len(cur['admitted_original_ids'])==72 and len(cur['accessible_pending_original_ids'])==33
for k in ['measured_original_ids','active_original_ids','archived_original_ids','editorial_original_ids','added_measurements','current_topic_replacements']:assert cur[k]==old[k]
newrows=load(R/cur['active_catalogue']['path'])['entries'];oldrows=load(R/old['active_catalogue']['path'])['entries'];assert len(newrows)==len(oldrows)==106
assert [x['original_id'] for x in newrows]==[x['original_id'] for x in oldrows]
assert sum(x==y for x,y in zip(newrows,oldrows))==105
newrow=next(x for x in newrows if x['original_id']=='L071');oldrow=next(x for x in oldrows if x['original_id']=='L071')
assert {k for k in newrow if newrow[k]!=oldrow[k]}=={'current_principal_recovery','next_obligation'}
assert newrow['current_principal_recovery']['historical_admission_evidence']==oldrow['current_principal_recovery']
records={}
def walk(x):
 if isinstance(x,dict):
  if 'logical_path' in x and 'path' in x:records[x['path']]=x
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(a);walk(scope)
for row in records.values():
 p=R/row['path'];assert p.stat().st_size==row.get('stored_bytes',row['bytes']) and sha(p)==row.get('stored_sha256',row['sha256']),str(p)
# Independently establish that every original top-level syntax node remains,
# apart from main and precisely the two newly inserted transition functions.
ot=ast.parse((R/history['scripts/verify_snapshot.py']['path']).read_text());nt=ast.parse((R/'scripts/verify_snapshot.py').read_text())
added={'check_previous_science72','check_science72'}
def nodes(t,exclude):return [ast.dump(n,include_attributes=False) for n in t.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in exclude)]
assert nodes(ot,{'main'})==nodes(nt,{'main'}|added)
for name,d in a['component_acceptance'].items():
 assert set(d)=={'author','distinct_review','root_adoption'}
 for x in d.values():assert sha(R/x['path'])==x['sha256']
modulepath=R/'scripts/check_science72.py';sp=importlib.util.spec_from_file_location('science72_distinct',modulepath);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);preflight=m.verify(R,require_root=False)
(W/'preflight.json').write_text(json.dumps(preflight,indent=2)+'\n')
report={'status':'PASS_DISTINCT_L071_SOURCE_ROUTE_AND_REGISTRATION_AUDIT','source_routes':15,'all_source_physical_pages_accounted_for':14,'four_exact_review_chains':True,'public_logical_bindings_checked':len(records),'other_original_rows_unchanged':105,'only_L071_fields_changed':['current_principal_recovery','next_obligation'],'historical_L071_record_preserved':True,'old_top_level_ASTs_preserved':True,'credit_still_requires_root_gate':True,'whole_original_credit':0,'public_read_only':True,'new_measurements':0,'preflight':preflight,'public_input_pins':[{ 'path':p,'sha256':sha(R/p),'bytes':(R/p).stat().st_size} for p in ['audit/recoveries/L071/v1/admission.json','audit/recoveries/L071/v1/scope_routes.json','audit/science72/v1/new_original_registration.json','audit/corpus/latest.json','scripts/check_science72.py','scripts/check_science72_history.py','scripts/verify_snapshot.py',cur['active_catalogue']['path']]]}
(W/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='public_input_pins'},indent=2))
