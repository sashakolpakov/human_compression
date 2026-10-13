import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized execution required')
import ast,hashlib,importlib.util,json
from pathlib import Path
R=Path('/Users/sasha/medusa/math_compression');P=Path(__file__).resolve().parent
OLD='0e58f8638f579ab859ad0e1f4b692a3a7537ceffa335a4dab622f8099050d522'
def need(b,s):
 if not b:raise ValueError(s)
def pin(p,root=R):
 b=p.read_bytes();return {'path':str(p.relative_to(root)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
p=R/'scripts/verify_snapshot.py';current=p.read_text();old=current;delta=[]
for var,fun in [('l019_corrections','check_l019_bounded_corrections'),('l019_transitive','check_l019_transitive_correction')]:
 a=f'    {var} = run_historical35_check({fun})\n';b=f'    {var} = {fun}()\n'
 need(old.count(a)==1,'exact unique call');old=old.replace(a,b);delta.append({'before':b.rstrip(),'after':a.rstrip()})
need(hashlib.sha256(old.encode()).hexdigest()==OLD,'only two lines since exact initial review')
oldast=ast.parse(old);newast=ast.parse(current)
func=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
need(func(oldast)==func(newast),'all non-main functions identical')
sp=importlib.util.spec_from_file_location('snapshot_routing_review',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def probe():
 return (load('audit/corpus/latest.json'),load('audit/overview/latest.json'),load('papers/latest_catalogue.json'),load('audit/science79/v1/new_original_registration.json'))
# The actual existing adapter replaces only the function's global load binding.
probe.__globals__['load']=m.load
load_before=m.load;result=m.run_historical35_check(probe)
paths=['audit/topic-operations/v1/previous_corpus_pointer.json','audit/topic-operations/v1/previous_overview_pointer.json','audit/topic-operations/v1/previous_catalogue.json','audit/science79/v1/new_original_registration.json']
for obj,path in zip(result,paths):need(obj==m.load(path),'exact historical route '+path)
need(m.load is load_before and probe.__globals__['load'] is load_before,'no global mutation')
need('L019' in result[0]['accessible_pending_original_ids'] and 'L019' not in result[0]['admitted_original_ids'],'historical pending premise')
now=m.load('audit/corpus/latest.json');need('L019' in now['admitted_original_ids'] and 'L019' not in now['accessible_pending_original_ids'],'current admission remains')
need(now['admitted_principal_originals']==79 and now['handled_mathematical_originals']==80 and now['accessible_pending_complete_recovery']==25,'current counts')
need('science72 = check_science79()' in current and 'science79_history = check_previous_science79()' in current,'current and history checks remain')
report={'status':'PASS_DISTINCT_TWO_LINE_HISTORICAL_ROUTING','initial_review_verifier_sha256':OLD,'delta':delta,'unchanged_nonmain_functions':len(func(oldast)),'actual_adapter_routes':paths,'historical_pending_L019':True,'current_admitted_L019':True,'global_load_unchanged':True,'mathematical_censuses_repeated':False,'bindings':[pin(R/x) for x in ['scripts/verify_snapshot.py','scripts/check_science79.py','scripts/check_science79_history.py','audit/topic-operations/v1/admission.json']+paths+['audit/corpus/latest.json']]}
(P/'check_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='bindings'}))
