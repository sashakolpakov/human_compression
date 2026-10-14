import sys
if sys.flags.optimize:raise RuntimeError('Normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json,os,re,subprocess
from pypdf import PdfReader
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--label',required=True);arg=ap.parse_args();R=arg.repo.resolve();W=Path(__file__).resolve().parent;P=W.parent/'Suzuki_refutations_publication_work';AUD='audit/principal-refutations/suzuki-subfields/v1';BASE='corrections/suzuki-subfields/v1';IDS=['L110','L114','L115']
def load(n):return json.loads((R/n).read_text())
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
spec=importlib.util.spec_from_file_location('distinct_suzuki',R/'scripts/check_suzuki_dispositions.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
h=load(AUD+'/history_routes.json')['routes'];c=load('audit/corpus/latest.json');old=load(h['audit/corpus/latest.json']['path']);cat=load(c['active_catalogue']['path']);before=load(old['active_catalogue']['path']);ids=[e['original_id']for e in cat['entries']];assert len(ids)==len(set(ids))==106
parts=[set(c[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']];assert list(map(len,parts))==[85,5,15,1];assert set.union(*parts)==set(ids);assert all(not x&y for i,x in enumerate(parts)for y in parts[i+1:]);assert parts[1]=={'F003','L029',*IDS};assert set(c['handled_mathematical_original_ids'])==parts[0]|parts[1]
for key in ['admitted_original_ids','current_science_registration','measured_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids']:assert c[key]==old[key]
assert len(c['measured_original_ids'])==53 and len(c['measurement_pending_original_ids'])==32
changed=[x['original_id']for x,y in zip(before['entries'],cat['entries'])if x!=y];assert changed==IDS
for sid in IDS:
 x=next(x for x in before['entries']if x['original_id']==sid);y=next(x for x in cat['entries']if x['original_id']==sid);d=y['current_principal_recovery'];assert d['historical_admission_evidence']==x['current_principal_recovery'];assert d['original_fully_handled']and not d['principal_contract_admitted']and not d['all_original_assertions_claimed'];assert d['scope']['source_id']==sid and d['correction_path']==BASE+'/'+sid+'/admission.json'
native=load('papers/catalogue_principal_refutations.json');prior=load(h['papers/catalogue_principal_refutations.json']['path']);assert native['entries'][:-3]==prior['entries'];assert native['original_ids']==prior['original_ids']+IDS;assert len({e['id']for e in native['entries']})==len(native['entries'])
for sid,pages,e in zip(IDS,[3,4,4],native['entries'][-3:]):
 assert e['source_ids']==[sid]and e['physical_pages']==pages and e['tex_inputs']==[];assert not re.findall(r'\\(?:input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',(R/e['tex']).read_text());assert len(PdfReader(R/e['pdf']).pages)==pages
paper=load('papers/latest_catalogue.json');oldpaper=load(h['papers/latest_catalogue.json']['path']);assert paper['corrected_unmeasured_scientific_catalogue']==oldpaper['corrected_unmeasured_scientific_catalogue']
reg=load(c['current_principal_disposition_registration']['path']);assert len(reg['individual_admissions'])==3
admissions=[load(x['path'])for x in reg['individual_admissions']];assert [a['source_id']for a in admissions]==IDS
for sid,a in zip(IDS,admissions):assert a['publication_gate']==f'audit/principal-refutations/{sid}/v1/root_integration.json'and a['principal_refutation_credit']==1
original=m.load
cases=[('lose earlier F003','audit/corpus/latest.json',lambda x:x['handled_mathematical_original_ids'].remove('F003')),('change other original',c['active_catalogue']['path'],lambda x:x['entries'][0].update(original_id='DAMAGED')),('lose source history',c['active_catalogue']['path'],lambda x:next(e for e in x['entries']if e['original_id']=='L114')['current_principal_recovery'].update(historical_admission_evidence={})),('claim all original assertions',c['active_catalogue']['path'],lambda x:next(e for e in x['entries']if e['original_id']=='L110')['current_principal_recovery'].update(all_original_assertions_claimed=True)),('change prior refutation','papers/catalogue_principal_refutations.json',lambda x:x['entries'][1].update(title='DAMAGED')),('invent native input','papers/catalogue_principal_refutations.json',lambda x:x['entries'][-1].update(tex_inputs=['missing.tex'])),('wrong operational status',AUD+'/operational_review.json',lambda x:x.update(status='PENDING')),('wrong individual admission',BASE+'/L114/admission.json',lambda x:x.update(source_id='L115')),('merged source gates',AUD+'/registration.json',lambda x:x['individual_publication_gates'].__setitem__(1,x['individual_publication_gates'][0]))]
controls=[]
for label,path,fn in cases:
 damaged=copy.deepcopy(load(path));fn(damaged)
 def mock(root,name,path=path,damaged=damaged):return copy.deepcopy(damaged)if str(name)==path else original(root,name)
 m.load=mock
 try:m.verify(R,False)
 except(ValueError,KeyError,AssertionError):controls.append(label)
 else:raise RuntimeError('Damaged input accepted '+label)
 finally:m.load=original
try:m.verify(R,True)
except FileNotFoundError as e:assert 'root_integration.json'in str(e);controls.append('no admission without final root gates')
else:raise RuntimeError('Admitted before gates')
can=json.loads((P/'registration_candidate.json').read_text());exact=[];different=[]
for row in can['files']:
 z=pin(R/row['path']);(exact if all(z[k]==row[k]for k in['bytes','sha256'])else different).append(row['path'])
assert set(different)<={'audit/protocol.pdf'}
source=Path(can['candidate_repository'])/'audit/protocol.pdf';target=R/'audit/protocol.pdf';assert [p.extract_text()for p in PdfReader(source).pages]==[p.extract_text()for p in PdfReader(target).pages];assert len(PdfReader(target).pages)==7
oldtext=(R/h['scripts/verify_snapshot.py']['path']).read_text();newtext=(R/'scripts/verify_snapshot.py').read_text();expected=oldtext.replace('    L029_disposition_history = check_previous_L029_disposition()',"    suzuki_disposition_history = check_previous_suzuki_dispositions()\n    L029_disposition_history = suzuki_disposition_history['previous']").replace('    science72 = check_L029_disposition()','    science72 = check_suzuki_dispositions()').replace("    print('PASS: exact science85 history preserved; L029 adds one separate principal refutation.')","    print('PASS: exact L029 disposition history preserved; L110, L114 and L115 add three separate principal refutations.')")
def main(t):return ast.dump(next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)and n.name=='main'),include_attributes=False)
assert main(expected)==main(newtext)
links=[]
for doc in ['README.rst','audit/completion.rst']:
 for t in re.findall(r'<([^>]*corrections/suzuki-subfields/v1/PUBLICATION\.rst)>',(R/doc).read_text()):assert((R/doc).parent/t).is_file();links.append([doc,t])
assert len(links)==2
for name in ['protocol1.stderr','protocol2.stderr']:assert not(R/AUD/name).read_bytes()
log=(R/AUD/'protocol2.stdout').read_text();assert all(t not in log for t in ['Warning','Overfull','Underfull'])
assert not any(r['path'].endswith('.md')for r in can['files'])
guards=[]
for script,args in [(R/'scripts/check_suzuki_dispositions.py',['--repo',str(R),'--preflight']),(R/'scripts/check_suzuki_history.py',[]),(P/'registration_drafts/integrate_suzuki_dispositions.py',['--repo',str(R),'--operational-review',str(W),'--expected-operational-manifest','0'*64])]:
 for mode in ['argument','environment']:
  env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);cmd=[sys.executable]
  if mode=='argument':cmd.append('-O')
  else:env['PYTHONOPTIMIZE']='1'
  r=subprocess.run(cmd+[str(script)]+args,capture_output=True,env=env,timeout=15);assert r.returncode!=0 and b'Optimized Python is not supported'in r.stderr;guards.append([script.name,mode])
r=subprocess.run([sys.executable,str(R/'scripts/check_suzuki_dispositions.py'),'--repo',str(R),'--preflight'],capture_output=True,timeout=30);(W/(arg.label+'_preflight.stdout')).write_bytes(r.stdout);(W/(arg.label+'_preflight.stderr')).write_bytes(r.stderr);assert r.returncode==0 and not r.stderr
report=dict(status='PASS_INDEPENDENT_THREE_SUZUKI_REGISTRATION',candidate=str(R),originals=106,only_changed_originals=changed,counts=dict(recoveries=85,refutations=5,handled=90,pending=15,measured=53,unmeasured=32,editorial=1),unchanged_science_registration=True,old_original_evidence_preserved=True,separate_admissions_and_gates=True,additional_controls=controls,candidate_files=len(can['files']),byte_identical_candidate_files=len(exact),metadata_only_pdf_differences=different,native_pages=[3,4,4],protocol_pages=7,exact_main_AST=True,guide_links=links,optimization_guards=guards,public_writes=False,historical_math_replay=False,census_repeated=False)
(W/(arg.label+'_report.json')).write_text(json.dumps(report,indent=2)+'\n');(W/(arg.label+'_bindings.json')).write_text(json.dumps([dict(pin(R/r['path']),path=r['path'])for r in can['files']],indent=2)+'\n');print(json.dumps(report))
