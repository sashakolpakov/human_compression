"""Replay the balanced-pair inputs, positive checks and optional complete census."""
import argparse,ast,hashlib,importlib.util,json,os,shutil,subprocess,sys
from pathlib import Path
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('normal Python required')
HERE=Path(__file__).resolve().parent
def need(x,msg):
 if not x:raise ValueError(msg)
def run(cmd,cwd,name,out,env,timeout=120):
 t=subprocess.run(cmd,cwd=cwd,capture_output=True,env=env,timeout=timeout)
 (out/(name+'.stdout')).write_bytes(t.stdout);(out/(name+'.stderr')).write_bytes(t.stderr)
 need(t.returncode==0 and not t.stderr,name+' execution')
 return t.stdout

def main():
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--replay-census',action='store_true');a=p.parse_args()
 out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
 exports=json.loads((HERE/'manifest.json').read_text())['exports'];deps=json.loads((HERE/'dependencies.json').read_text())
 for base,rows in [(HERE,exports),(a.study,deps)]:
  for row in rows:
   b=(base/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 for tag,args,childenv in [('argument',[sys.executable,'-O',str(HERE/'check.py')],env),('environment',[sys.executable,str(HERE/'check.py')],dict(env,PYTHONOPTIMIZE='1'))]:
  r=subprocess.run(args,env=childenv,capture_output=True,timeout=15);(out/(tag+'.stderr')).write_bytes(r.stderr);need(r.returncode!=0 and b'normal Python required' in r.stderr,'guard '+tag)
 # Fresh private copies retain the historical helpers unchanged; no packet mutation.
 work=out/'data';work.mkdir()
 for n in range(2,13,2):
  name=f'n{n}_run03' if n==12 else f'n{n}_run01';shutil.copytree(HERE/name,work/name)
 for name in ['verify_arrays.py','prepare_positive_checks.py','positive_checks.g','small_independent_v2.g']:
  shutil.copy2(HERE/name,work/name)
 run([sys.executable,'verify_arrays.py'],work,'arrays',out,env)
 fresh=json.loads((work/'arrays_report.json').read_text());expected=json.loads((HERE/'arrays_report.json').read_text());need(fresh==expected,'literal outputs changed')
 run([sys.executable,'prepare_positive_checks.py'],work,'positive_inputs',out,env)
 need((work/'positive_inputs.g').read_bytes()==(HERE/'positive_inputs.g').read_bytes(),'positive inputs changed')
 b=run(['/opt/homebrew/bin/gap','-q','-T','positive_checks.g'],work,'positive',out,env)
 need(b.count(b'COMPLETE_POSITIVE_CHECKS|41|101|')==1,'positive completion')
 b=run(['/opt/homebrew/bin/gap','-q','-T','small_independent_v2.g'],work,'labelled',out,env)
 need(b.count(b'COMPLETE_LABELLED|')==1,'labelled completion')
 spec=importlib.util.spec_from_file_location('arrays',HERE/'verify_arrays.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 ts=[tuple(tuple(x-1 for x in g) for g in ast.literal_eval(l.split('|',1)[1])) for l in b.decode().splitlines() if l.startswith('LABELLED|')]
 need({v.canon(t,0) for t in ts}=={v.canon(t,0) for t in v.load_run(HERE,6)},'labelled census classes');labelled_count=len(ts)
 damaged=0
 for t in [((0,0),),((1,0,2),(0,2,1),(2,1,0)),((1,0,2,3),)]:
  try:v.canon(t,0)
  except ValueError:damaged+=1
 need(damaged==3,'literal malformed controls')
 census=[]
 if a.replay_census:
  for n in range(2,13,2):
   cw=out/f'census{n}';cw.mkdir();(cw/'parameters.g').write_text(f'n:={n};;\n');shutil.copy2(HERE/'enumerate_v3.g',cw/'enumerate.g')
   b=run(['/opt/homebrew/bin/gap','-q','-T','enumerate.g'],cw,f'census{n}',out,env,600)
   need(b.count(b'COMPLETE_ANCHORED_CRITICAL_WINGS|')==1,'census completion')
   ts=[tuple(tuple(x-1 for x in g) for g in ast.literal_eval(l.split('|',1)[1])) for l in b.decode().splitlines() if l.startswith('SOLUTION|')]
   need({v.canon(t,0) for t in ts}=={v.canon(t,0) for t in v.load_run(HERE,n)},'fresh complete census')
   need(len(ts)==len({v.canon(t,0) for t in ts}),'fresh duplicate');census.append({'degree':n,'wings':len(ts)})
 if a.render:
  shutil.copy2(HERE/'balanced_pairs.tex',out/'balanced_pairs.tex')
  for i in [1,2]:run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','balanced_pairs.tex'],out,f'native{i}',out,env,30)
  log=(out/'balanced_pairs.log').read_text();need('Overfull' not in log and 'LaTeX Warning:' not in log,'native warning')
 report={'status':'PASS','exports':len(exports),'bindings':len(deps),'optimization_guards':2,'malformed_literal_guards':damaged,'labelled_degree6_survivors':labelled_count,'wing_counts':fresh['wing_counts'],'boundary_counts':fresh['boundary_counts'],'positive_wings':41,'positive_glued_markings':101,'fresh_complete_censuses':census,'whole_original_credit':0}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
