import sys
if sys.flags.optimize:raise RuntimeError('Normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import copy,hashlib,importlib.util,json,re,subprocess,ast,os
from pypdf import PdfReader
R=Path('/Users/sasha/medusa/math_compression');W=Path(__file__).resolve().parent;P=W.parent/'L029_publication_work';AUD='audit/principal-refutations/L029/v1';BASE='corrections/chiral-residues/v1'
spec=importlib.util.spec_from_file_location('L029_distinct',R/'scripts/check_L029_disposition.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def load(n):return json.loads((R/n).read_text())
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
h=load(AUD+'/history_routes.json')['routes'];c=load('audit/corpus/latest.json');old=load(h['audit/corpus/latest.json']['path']);cat=load(c['active_catalogue']['path']);before=load(old['active_catalogue']['path'])
ids=[x['original_id']for x in cat['entries']];assert len(ids)==len(set(ids))==106
A=set(c['admitted_original_ids']);F=set(c['refuted_principal_original_ids']);Q=set(c['accessible_pending_original_ids']);E=set(c['editorial_original_ids']);assert [len(A),len(F),len(Q),len(E)]==[85,2,18,1]
assert F=={'F003','L029'}and E=={'L022'}and A|F|Q|E==set(ids)
assert all(not x&y for i,x in enumerate([A,F,Q,E])for y in[A,F,Q,E][i+1:]);assert set(c['handled_mathematical_original_ids'])==A|F
for k in ['admitted_original_ids','measured_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','current_science_registration']:assert c[k]==old[k]
assert len(c['measured_original_ids'])==53 and len(c['measurement_pending_original_ids'])==32
changed=[x['original_id']for x,y in zip(before['entries'],cat['entries'])if x!=y];assert changed==['L029']
x=next(x for x in before['entries']if x['original_id']=='L029');y=next(x for x in cat['entries']if x['original_id']=='L029');assert y['current_principal_recovery']['historical_admission_evidence']==x['current_principal_recovery']
assert not y['current_principal_recovery']['principal_contract_admitted']and y['current_principal_recovery']['original_fully_handled']and not y['current_principal_recovery']['all_original_assertions_claimed']
native=load('papers/catalogue_principal_refutations.json');prior=load(h['papers/catalogue_principal_refutations.json']['path']);assert native['entries'][:-1]==prior['entries']and native['original_ids']==prior['original_ids']+['L029']
assert len({x['id']for x in native['entries']})==len(native['entries']);new=native['entries'][-1];assert new['source_ids']==['L029']and new['physical_pages']==5 and new['tex_inputs']==[]
assert not re.findall(r'\\(?:input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',(R/new['tex']).read_text());assert len(PdfReader(R/new['pdf']).pages)==5
# The ordinary native catalogue is preserved by both the Git-tree audit and unchanged paper pointer.
paper=load('papers/latest_catalogue.json');oldpaper=load(h['papers/latest_catalogue.json']['path']);assert paper['corrected_unmeasured_scientific_catalogue']==oldpaper['corrected_unmeasured_scientific_catalogue']
original=m.load
cases=[('lose F003','audit/corpus/latest.json',lambda x:x['handled_mathematical_original_ids'].remove('F003')),('change another original',c['active_catalogue']['path'],lambda x:x['entries'][0].update(original_id='DAMAGED')),('erase prior L029 evidence',c['active_catalogue']['path'],lambda x:next(e for e in x['entries']if e['original_id']=='L029')['current_principal_recovery'].update(historical_admission_evidence={})),('claim all L029 assertions',c['active_catalogue']['path'],lambda x:next(e for e in x['entries']if e['original_id']=='L029')['current_principal_recovery'].update(all_original_assertions_claimed=True)),('change old refutation','papers/catalogue_principal_refutations.json',lambda x:x['entries'][0].update(title='DAMAGED')),('invent native input','papers/catalogue_principal_refutations.json',lambda x:x['entries'][-1].update(tex_inputs=['missing.tex'])),('false operational acceptance',AUD+'/operational_review.json',lambda x:x.update(status='PENDING'))]
controls=[]
for label,path,fn in cases:
 damaged=copy.deepcopy(load(path));fn(damaged)
 def mock(root,name,path=path,damaged=damaged):return copy.deepcopy(damaged)if str(name)==path else original(root,name)
 m.load=mock
 try:m.verify(R,False)
 except(ValueError,KeyError,AssertionError):controls.append(label)
 else:raise RuntimeError('Damaged decoded input accepted '+label)
 finally:m.load=original
try:m.verify(R,True)
except FileNotFoundError as e:assert 'root_integration.json'in str(e);controls.append('no self admission before root gate')
else:raise RuntimeError('Admitted before root gate')
can=json.loads((P/'registration_candidate.json').read_text());different=[];exact=[]
for row in can['files']:
 z=pin(R/row['path'])
 (different if any(z[k]!=row[k]for k in['bytes','sha256'])else exact).append(row['path'])
assert set(different)<={'audit/protocol.pdf'}
source=Path(can['candidate_repository'])/'audit/protocol.pdf';target=R/'audit/protocol.pdf';assert [p.extract_text()for p in PdfReader(source).pages]==[p.extract_text()for p in PdfReader(target).pages];assert len(PdfReader(target).pages)==7
oldtext=(R/h['scripts/verify_snapshot.py']['path']).read_text();newtext=(R/'scripts/verify_snapshot.py').read_text();expected=oldtext.replace('    science85_history = check_previous_science85()',"    L029_disposition_history = check_previous_L029_disposition()\n    science85_history = L029_disposition_history['previous']").replace('    science72 = check_science85()','    science72 = check_L029_disposition()').replace("print('PASS: exact science84 history preserved; L041 corrected tetrahedral geometry adds one original.')","print('PASS: exact science85 history preserved; L029 adds one separate principal refutation.')")
def main(t):return ast.dump(next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)and n.name=='main'),include_attributes=False)
assert main(expected)==main(newtext)
for name in ['protocol1.stderr','protocol2.stderr']:assert not(R/AUD/name).read_bytes()
log=(R/AUD/'protocol2.stdout').read_text();assert 'Warning'not in log and 'Overfull'not in log and 'Underfull'not in log
links=[]
for doc in ['README.rst','audit/completion.rst']:
 for target in re.findall(r'<([^>]*corrections/chiral-residues/v1/PUBLICATION\.rst)>',(R/doc).read_text()):assert((R/doc).parent/target).is_file();links.append([doc,target])
assert len(links)==2
newpaths=[x.decode()for x in subprocess.check_output(['git','-C',str(R),'ls-files','--others','--exclude-standard','-z']).split(b'\0')if x]
transient={'audit/protocol.aux','audit/protocol.log','audit/protocol.out'};newpaths=[p for p in newpaths if p not in transient];assert all(not p.endswith('.md')for p in newpaths)
allowed=['audit/principal-refutations/L029/','corrections/chiral-residues/'];exactnames={'scripts/check_L029_disposition.py','scripts/check_L029_history.py','audit/corpus/accessible106/updates/principal-refutation-L029-catalogue.json','audit/corpus/updates/accessible106-principal-refutation-L029.json'}
assert all(p in exactnames or any(p.startswith(q)for q in allowed)for p in newpaths)
guards=[]
for script,args in [(R/'scripts/check_L029_disposition.py',['--repo',str(R),'--preflight']),(R/'scripts/check_L029_history.py',[]),(P/'registration_drafts/integrate_L029_disposition.py',['--repo',str(R),'--operational-review',str(W),'--expected-operational-manifest','0'*64])]:
 for mode in ['argument','environment']:
  env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);cmd=[sys.executable]
  if mode=='argument':cmd.append('-O')
  else:env['PYTHONOPTIMIZE']='1'
  result=subprocess.run(cmd+[str(script)]+args,capture_output=True,env=env,timeout=15);assert result.returncode!=0 and b'Optimized Python is not supported'in result.stderr;guards.append([script.name,mode])
pre=subprocess.run([sys.executable,str(R/'scripts/check_L029_disposition.py'),'--repo',str(R),'--preflight'],capture_output=True,timeout=30);(W/'preflight.stdout').write_bytes(pre.stdout);(W/'preflight.stderr').write_bytes(pre.stderr);assert pre.returncode==0 and not pre.stderr
report={'status':'PASS_INDEPENDENT_L029_REGISTRATION','originals':106,'only_changed_original':changed,'counts':{'recovered':85,'refuted':2,'handled':87,'pending':18,'measured':53,'unmeasured':32,'editorial':1},'ordinary_science_registration_unchanged':True,'ordinary_native_catalogue_unchanged':True,'old_L029_evidence_retained':True,'independent_decoded_input_controls':controls,'candidate_files':len(can['files']),'byte_identical_candidate_files':len(exact),'metadata_only_pdf_differences':different,'protocol_pages':7,'protocol_text_identity':True,'exact_main_AST':True,'new_native_pages':5,'literal_tex_inputs':[],'new_paths':len(newpaths),'new_markdown':0,'guide_links':links,'optimization_guards':guards,'public_writes':False,'historical_math_replay':False,'census_repeated':False}
(W/'independent_report.json').write_text(json.dumps(report,indent=2)+'\n');(W/'new_paths.json').write_text(json.dumps(newpaths,indent=2)+'\n');(W/'candidate_bindings.json').write_text(json.dumps([dict(pin(R/r['path']),path=r['path'])for r in can['files']],indent=2)+'\n');print(json.dumps(report))
