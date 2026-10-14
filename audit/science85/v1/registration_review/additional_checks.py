import sys
if sys.flags.optimize:raise RuntimeError('Normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import ast,hashlib,json,subprocess,re,os
from pypdf import PdfReader
R=Path('/Users/sasha/medusa/math_compression');W=Path(__file__).resolve().parent
P=W.parent/'L041_publication_work'
def load(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
c=load(P/'registration_candidate.json');different=[];exact=[]
for row in c['files']:
 p=R/row['path'];actual=pin(p)
 if any(actual[k]!=row[k]for k in ['bytes','sha256']):different.append(row['path'])
 else:exact.append(row['path'])
assert set(different)<={'audit/protocol.pdf'}
before=Path(c['candidate_repository'])/'audit/protocol.pdf';after=R/'audit/protocol.pdf'
assert [p.extract_text()for p in PdfReader(before).pages]==[p.extract_text()for p in PdfReader(after).pages]
assert len(PdfReader(after).pages)==7
old=(R/'audit/science85/v1/previous/scripts/verify_snapshot.py').read_text();new=(R/'scripts/verify_snapshot.py').read_text()
expected=old.replace('    science84_history = check_previous_science84()',"    science85_history = check_previous_science85()\n    science84_history = science85_history['previous']").replace('    science72 = check_science84()','    science72 = check_science85()').replace("print('PASS: exact science83 history preserved; N010 attributed survey disposition adds one original.')","print('PASS: exact science84 history preserved; L041 corrected tetrahedral geometry adds one original.')")
def main(t):return ast.dump(next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)and n.name=='main'),include_attributes=False)
assert main(expected)==main(new)
a=load(R/'audit/recoveries/L041/v1/admission.json');man=a['new_native_manuscripts'];assert len(man)==1
assert len(PdfReader(R/man[0]['pdf']['path']).pages)==8
tex=R/man[0]['tex']['path'];inputs=re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',tex.read_text());assert inputs==['tetrahedra_section']
assert [str((tex.parent/(x+'.tex')).relative_to(R))for x in inputs]==[q['path']for q in man[0]['tex_inputs']]
links=[]
for doc in ['README.rst','audit/completion.rst']:
 for target in re.findall(r'<([^>]*recoveries/L041/v1/PUBLICATION\.rst)>',(R/doc).read_text()):
  assert ((R/doc).parent/target).is_file();links.append([doc,target])
assert len(links)==2
for name in ['protocol1.stderr','protocol2.stderr']:assert not(R/'audit/science85/v1'/name).read_bytes()
log=(R/'audit/science85/v1/protocol2.stdout').read_text();assert 'Overfull'not in log and 'LaTeX Warning:'not in log
guards=[]
for script,args in [(R/'scripts/check_science85.py',['--repo',str(R),'--preflight']),(R/'scripts/check_science85_history.py',[]),(P/'registration_drafts/integrate_science85.py',['--repo',str(R),'--operational-review',str(W),'--expected-operational-manifest','0'*64])]:
 for mode in ['argument','environment']:
  env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);cmd=[sys.executable]
  if mode=='argument':cmd.append('-O')
  else:env['PYTHONOPTIMIZE']='1'
  result=subprocess.run(cmd+[str(script)]+args,capture_output=True,env=env,timeout=15)
  assert result.returncode!=0 and b'Optimized Python is not supported'in result.stderr;guards.append([script.name,mode])
pre=subprocess.run([sys.executable,str(R/'scripts/check_science85.py'),'--repo',str(R),'--preflight'],capture_output=True,timeout=30)
(W/'preflight.stdout').write_bytes(pre.stdout);(W/'preflight.stderr').write_bytes(pre.stderr);assert pre.returncode==0 and not pre.stderr
result=dict(status='PASS_ADDITIONAL_REGISTRATION_INTERFACES',candidate_files=len(c['files']),byte_identical=len(exact),metadata_only_pdf_differences=different,all_protocol_page_text_identical=True,exact_main_AST=True,native_pages=8,literal_input=inputs,guide_links=links,native_log_clean=True,optimization_guards=guards)
(W/'additional_report.json').write_text(json.dumps(result,indent=2)+'\n')
(W/'candidate_bindings.json').write_text(json.dumps([dict(pin(R/r['path']),path=r['path'])for r in c['files']],indent=2)+'\n')
print(json.dumps(result))
