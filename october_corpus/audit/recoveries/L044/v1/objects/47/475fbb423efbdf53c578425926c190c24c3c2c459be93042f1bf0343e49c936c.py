from pathlib import Path
import json,hashlib,os,subprocess,datetime,sys,shutil,time
from pypdf import PdfReader
if sys.flags.optimize: raise RuntimeError('optimization forbidden')
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L044_degree_sixteen_v1';W=S/'reboot_20261013/L044_degree_sixteen_distinct'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
 if not c:raise RuntimeError(m)
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,h):need(sha(p)==h,str(p))
m=A/'manifest.json';pin(m,'38285d1766d84b08e2c78470efe0414e22e55bc7c09237615a72fc567503ed90')
exports=json.loads(m.read_text())['exports'];deps=json.loads((A/'dependencies.json').read_text());roots={k:Path(v) for k,v in deps['root_locations'].items()}
for e in exports:pin(A/e['path'],e['sha256'])
for e in deps['bindings']:pin(roots[e['root']]/e['path'],e['sha256'])
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);start=time.monotonic();put(W/'active.json',{'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'owner':'publication_recovery','author_manifest':sha(m)})
with (W/'driver.stdout').open('wb') as o,(W/'driver.stderr').open('wb') as e:r=subprocess.run([sys.executable,str(A/'check.py'),str(W/'replay01')],stdout=o,stderr=e,timeout=270,env=env)
need(r.returncode==0,'checker rc');need(not (W/'driver.stderr').read_bytes(),'driver stderr')
x=json.loads((W/'replay01/report.json').read_text());need(x['status']=='PASS','checker status')
N=W/'native01';N.mkdir();shutil.copy2(A/'degree_sixteen.tex',N/'degree_sixteen.tex')
for i in [1,2]:
 with (N/f'pass{i}.stdout').open('wb') as o,(N/f'pass{i}.stderr').open('wb') as e:
  p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','degree_sixteen.tex'],cwd=N,stdout=o,stderr=e,timeout=60,env=env)
 need(p.returncode==0,'native rc');need(not (N/f'pass{i}.stderr').read_bytes(),'native stderr')
pages=[p.extract_text() for p in PdfReader(N/'degree_sixteen.pdf').pages];expected=[p.extract_text() for p in PdfReader(A/'degree_sixteen.pdf').pages];need(pages==expected and len(pages)==3,'native pages')
log=(N/'degree_sixteen.log').read_text();warnings=[l for l in log.splitlines() if 'Overfull' in l or 'LaTeX Warning' in l];need(not warnings,str(warnings))
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(N/'page-%d.png'),str(N/'degree_sixteen.pdf')],check=True,timeout=60)
controls=[]
for name,args,extra in [('direct_O',['-O'],{}),('environment',[],{'PYTHONOPTIMIZE':'1'})]:
 out=W/('reject_'+name);e=dict(env);e.update(extra);p=subprocess.run([sys.executable,*args,str(A/'check.py'),str(out)],capture_output=True,env=e,timeout=10);need(p.returncode!=0 and not out.exists(),'optimized execution accepted');(W/(name+'.stdout')).write_bytes(p.stdout);(W/(name+'.stderr')).write_bytes(p.stderr);controls.append({'name':name,'returncode':p.returncode,'no_output_created':True})
for e in exports:pin(A/e['path'],e['sha256'])
for e in deps['bindings']:pin(roots[e['root']]/e['path'],e['sha256'])
report={'status':'PASS_DISTINCT_FRESH_DEGREE16','exports':len(exports),'bindings':len(deps['bindings']),'seconds':time.monotonic()-start,'census':x['census'],'native_pages':len(pages),'native_text_equal':True,'native_warnings':warnings,'optimization_controls':controls,'all_inputs_unchanged':True,'whole_original_credit':0}
put(W/'replay_report.json',report);put(W/'active.json',{'status':'TERMINAL_PASS','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report_sha256':sha(W/'replay_report.json')});print(json.dumps(report))
