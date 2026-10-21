from pathlib import Path
import json,hashlib,os,subprocess,datetime,sys,shutil,time
from pypdf import PdfReader
if sys.flags.optimize:raise RuntimeError('optimization forbidden')
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L044_symmetric_central_pairs_v1';W=S/'reboot_20261013/L044_symmetric_central_pairs_distinct'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
 if not c:raise RuntimeError(m)
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
files={}
def pin(p,h):
 need(sha(p)==h,str(p));files[str(p)]=h
m=A/'manifest.json';pin(m,'c31d4ccca190e8b7d43909017e90ad50f48be487e26d66b74c241e6ac55fa454')
exports=json.loads(m.read_text())['exports'];deps=json.loads((A/'dependencies.json').read_text());roots={'private_study':S,'public_repository':Path('/Users/sasha/medusa/math_compression')};acquired=0
for e in exports:pin(A/e['path'],e['sha256'])
for e in deps['bindings']:
 p=roots[e.get('root','private_study')]/e['path'];pin(p,e['sha256'])
 if p.name=='manifest.json':
  for q in json.loads(p.read_text()).get('exports',[]):pin(p.parent/q['path'],q['sha256']);acquired+=1
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);start=time.monotonic();put(W/'active.json',{'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'publication_recovery','author_manifest':sha(m)})
with (W/'driver.stdout').open('wb') as o,(W/'driver.stderr').open('wb') as e:p=subprocess.run([sys.executable,str(A/'finite/check.py'),'--out',str(W/'finite01')],stdout=o,stderr=e,timeout=260,env=env)
need(p.returncode==0,'checker rc');need(not (W/'driver.stderr').read_bytes(),'driver stderr');x=json.loads((W/'finite01/report.json').read_text());need(x['status']=='COMPLETE_SYMMETRIC_EIGHT_INDEPENDENT_RANK_SIX','checker status')
N=W/'native01';N.mkdir();shutil.copy2(A/'symmetric_central_pairs.tex',N/'symmetric_central_pairs.tex')
for i in [1,2]:
 with (N/f'pass{i}.stdout').open('wb') as o,(N/f'pass{i}.stderr').open('wb') as e:p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','symmetric_central_pairs.tex'],cwd=N,stdout=o,stderr=e,timeout=60,env=env)
 need(p.returncode==0,'native rc');need(not (N/f'pass{i}.stderr').read_bytes(),'native stderr')
pages=[p.extract_text() for p in PdfReader(N/'symmetric_central_pairs.pdf').pages];expected=[p.extract_text() for p in PdfReader(A/'symmetric_central_pairs.pdf').pages];need(pages==expected and len(pages)==4,'native pages')
log=(N/'symmetric_central_pairs.log').read_text();warnings=[l for l in log.splitlines() if 'Overfull' in l or 'LaTeX Warning' in l];need(not warnings,str(warnings))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(N/'page-%d.png'),str(N/'symmetric_central_pairs.pdf')],check=True,timeout=60)
controls=[]
for name,args,extra in [('direct_O',['-O'],{}),('environment',[],{'PYTHONOPTIMIZE':'1'})]:
 out=W/('reject_'+name);e=dict(env);e.update(extra);p=subprocess.run([sys.executable,*args,str(A/'finite/check.py'),'--out',str(out)],capture_output=True,env=e,timeout=10);need(p.returncode!=0 and not out.exists(),'optimized execution accepted');(W/(name+'.stdout')).write_bytes(p.stdout);(W/(name+'.stderr')).write_bytes(p.stderr);controls.append({'name':name,'returncode':p.returncode,'no_output_created':True})
for p,h in files.items():need(sha(Path(p))==h,'input changed '+p)
report={'status':'PASS_DISTINCT_FRESH_SYMMETRIC_CENTRAL_PAIRS','exports':len(exports),'bindings':len(deps['bindings']),'acquired_export_occurrences':acquired,'unique_inputs':len(files),'seconds':time.monotonic()-start,'finite_report':x,'native_pages':len(pages),'native_text_equal':True,'native_warnings':warnings,'optimization_controls':controls,'all_inputs_unchanged':True,'whole_original_credit':0}
put(W/'replay_report.json',report);put(W/'input_pins.json',files);put(W/'active.json',{'status':'TERMINAL_PASS','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report_sha256':sha(W/'replay_report.json')});print(json.dumps(report))
