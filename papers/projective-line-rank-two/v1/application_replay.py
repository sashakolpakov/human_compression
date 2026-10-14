"""Public L076 replay adapter; exact scientific programs stay unchanged."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,os,re,shutil,subprocess,time
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--replay-finite',action='store_true');a=ap.parse_args()
 S=a.study.resolve();O=a.out.resolve();need(not O.exists()and not O.is_relative_to(S),'Fresh external output');O.mkdir(parents=True)
 A=S/'corpus106_L076_projective_line_v1';V=S/'corpus106_L076_projective_line_independent_review';r=load(V/'review.json');old=S/r['independent_input']['path'];F=old.parent
 need(sha(old)==r['independent_input']['sha256']and old.stat().st_size==r['independent_input']['bytes'],'Recorded distinct execution')
 need(not(F/'finite.stderr').read_bytes()and old.read_bytes().rstrip().endswith(b'PASS_COMPLETE_L076_FINITE_CLASSIFICATION'),'Complete clean execution')
 receipt=load(F/'report.json');need(receipt['status']=='PASS_L076_CLASSIFICATION_COMPONENT','Accepted exact finite receipt')
 executed=next(x for x in receipt['commands']if x['label']=='finite');need(executed['returncode']==0 and executed['command'][-1].endswith('/corpus106_L076_projective_line_v1/certificate.g'),'Actual executed program')
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';commands=[];start=time.monotonic()
 def run(label,cmd,cwd=None,cap=60):
  t=time.monotonic()
  try:p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=cap)
  except subprocess.TimeoutExpired as e:
   (O/(label+'.stdout')).write_bytes(e.stdout or b'');(O/(label+'.stderr')).write_bytes(e.stderr or b'');raise
  (O/(label+'.stdout')).write_bytes(p.stdout);(O/(label+'.stderr')).write_bytes(p.stderr)
  commands.append(dict(label=label,command=cmd,returncode=p.returncode,seconds=time.monotonic()-t));need(p.returncode==0 and not p.stderr,'Clean '+label);return p
 data=old
 if a.replay_finite:
  gap=shutil.which('gap');need(gap,'GAP on PATH');run('finite',[gap,'-q','-T',str(A/'certificate.g')],cap=180);data=O/'finite.stdout'
 run('semantic',[sys.executable,'-B',str(A/'verify.py'),'--input',str(data),'--out',str(O/'semantic.json')])
 semantic=load(O/'semantic.json');need(semantic==load(A/'expected.json'),'Exact complete semantic table')
 run('independent',[sys.executable,'-B',str(V/'independent.py'),'--input',str(data),'--out',str(O/'independent.json')])
 independent=load(O/'independent.json');expected=load(V/'independent_report.json');expected['input_sha256']=sha(data);need(independent==expected,'Independent global orbits, graphs and scalars')
 spec=importlib.util.spec_from_file_location('unchanged_L076_verifier',A/'verify.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);text=data.read_text();damages=[]
 for label,kind,edit in [('missing_row','ROW',None),('false_class_count','ROW',lambda x:x.__setitem__(5,99)),('wrong_swap','SWAP',lambda x:x.__setitem__(5,list(range(1,x[0]+2)))),('missing_edge','ROW',lambda x:x[10][3].pop())]:
  match=re.search(r'(?:^|\n)'+kind+r'\s+(.*?)\nEND_'+kind,text,re.S);need(match is not None,'Exact damage site');value=json.loads(match[1])
  if edit is None:bad=text[:match.start()]+text[match.end():]
  else:edit(value);bad=text[:match.start()]+'\n'+kind+' '+json.dumps(value)+'\nEND_'+kind+text[match.end():]
  try:module.verify(bad)
  except(AssertionError,ValueError,KeyError,StopIteration):damages.append(label)
  else:raise ValueError('Damaged finite record accepted')
 try:module.verify(text.replace('PASS_COMPLETE_L076_FINITE_CLASSIFICATION','INCOMPLETE'))
 except AssertionError:damages.append('incomplete_execution')
 else:raise ValueError('Incomplete finite record accepted')
 guards=[]
 for program,message in [(A/'check.py',b'Use ordinary Python'),(A/'verify.py',b'Use ordinary Python'),(V/'independent.py',b'Ordinary Python required'),(Path(__file__).resolve(),b'Ordinary Python required')]:
  for mode in ['argument','environment']:
   target=O/(program.stem+'_'+mode);ee=dict(env)
   if mode=='environment':ee['PYTHONOPTIMIZE']='1'
   p=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(program),'--out',str(target)],env=ee,capture_output=True,timeout=15)
   (O/(program.stem+'_'+mode+'.stderr')).write_bytes(p.stderr);need(p.returncode!=0 and message in p.stderr and not target.exists(),'Pre-output optimization guard');guards.append([program.name,mode])
 from pypdf import PdfReader
 texts=lambda p:[page.extract_text()for page in PdfReader(p).pages]
 N=O/'native';N.mkdir();shutil.copyfile(A/'classification.tex',N/'classification.tex')
 for i in [1,2]:run('latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode','classification.tex'],N)
 need(texts(N/'classification.pdf')==texts(A/'classification.pdf')and len(texts(N/'classification.pdf'))==6,'Complete native text')
 need(not any(x in(N/'classification.log').read_text()for x in ['Warning','Overfull','Underfull']),'Clean native')
 run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','classification.pdf'],N)
 pages=sorted(N.glob('page-*.png'));need(len(pages)==6,'All native pages')
 report=dict(status='PASS_PUBLIC_L076_APPLICATION',finite_replay=a.replay_finite,acquired_finite_execution=not a.replay_finite,finite_input_sha256=sha(data),semantic_sha256=sha(O/'semantic.json'),independent_sha256=sha(O/'independent.json'),finite_fields=14,torus_cases=28,representatives=19,damaged_finite_controls=damages,optimization_guards=guards,native_pages=6,native_text_identical=True,native_raster_sha256=[sha(p)for p in pages],commands=commands,author_scientific_code_unchanged=True,runtime_text_patching=False,private_fallback=False,general_proofs_verified_by_program=False,whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-start)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
