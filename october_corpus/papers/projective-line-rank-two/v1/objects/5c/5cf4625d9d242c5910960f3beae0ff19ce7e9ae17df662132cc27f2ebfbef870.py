"""Replay the bounded classification certificate and build its complete proof."""
import sys
if sys.flags.optimize:raise RuntimeError('Use ordinary Python')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,time,re
P=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise ValueError(m)
def pin(p):return dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();S=a.study.resolve();O=a.out.resolve();need(not O.exists(),'Fresh output');t=time.monotonic()
 for r in json.loads((P/'dependencies.json').read_text()):need(pin(S/r['path'])=={k:r[k]for k in ['bytes','sha256']},'Exact source/development input')
 if(P/'manifest.json').exists():
  for r in json.loads((P/'manifest.json').read_text())['exports']:need(pin(P/r['path'])=={k:r[k]for k in ['bytes','sha256']},'Exact frozen export')
 O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';commands=[]
 def run(cmd,label,cwd=O,cap=180):
  start=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=cap);(O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr);commands.append(dict(label=label,command=cmd,returncode=r.returncode,seconds=time.monotonic()-start));need(r.returncode==0 and not r.stderr,'Clean terminal '+label);return r
 gap=shutil.which('gap');need(gap,'GAP on PATH');r=run([gap,'-q','-T',str(P/'certificate.g')],'finite');need(r.stdout.rstrip().endswith(b'PASS_COMPLETE_L076_FINITE_CLASSIFICATION'),'Complete finite marker')
 run([sys.executable,'-B',str(P/'verify.py'),'--input',str(O/'finite.stdout'),'--out',str(O/'semantic.json')],'semantic')
 actual=json.loads((O/'semantic.json').read_text());need(actual==json.loads((P/'expected.json').read_text()),'Exact independently checked semantic inventory')
 spec=importlib.util.spec_from_file_location('literal_L076',P/'verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);text=r.stdout.decode();damages=[]
 for label,kind,edit in [('missing_row','ROW',None),('false_class_count','ROW',lambda x:x.__setitem__(5,99)),('wrong_swap','SWAP',lambda x:x.__setitem__(5,list(range(1,x[0]+2)))),('missing_edge','ROW',lambda x:x[10][3].pop())]:
  match=re.search(r'(?:^|\n)'+kind+r'\s+(.*?)\nEND_'+kind,text,re.S);need(match is not None,'Damage site');value=json.loads(match[1])
  if edit is None:bad=text[:match.start()]+text[match.end():]
  else:edit(value);bad=text[:match.start()]+'\n'+kind+' '+json.dumps(value)+'\nEND_'+kind+text[match.end():]
  try:m.verify(bad)
  except(AssertionError,ValueError,KeyError,StopIteration):damages.append(label)
  else:raise ValueError('Damaged certificate accepted '+label)
 try:m.verify(text.replace('PASS_COMPLETE_L076_FINITE_CLASSIFICATION','INCOMPLETE'))
 except AssertionError:damages.append('incomplete_execution')
 else:raise ValueError('Incomplete execution accepted')
 guards=[]
 for f in ['check.py','verify.py']:
  for mode in ['argument','environment']:
   ee=dict(env);target=O/(f+'_'+mode)
   if mode=='environment':ee['PYTHONOPTIMIZE']='1'
   c=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(P/f),'--out',str(target)],env=ee,capture_output=True,timeout=10)
   (O/(f+'_'+mode+'.stderr')).write_bytes(c.stderr);need(c.returncode!=0 and b'Use ordinary Python'in c.stderr and not target.exists(),'Pre-output optimization guard');guards.append([f,mode])
 native=None
 if a.render:
  from pypdf import PdfReader
  N=O/'native';N.mkdir();shutil.copyfile(P/'classification.tex',N/'classification.tex')
  for i in [1,2]:run(['pdflatex','-halt-on-error','-interaction=nonstopmode','classification.tex'],'latex'+str(i),N,60)
  texts=lambda f:[p.extract_text()for p in PdfReader(f).pages]
  pages=texts(N/'classification.pdf');need(len(pages)==6,'Complete six-page proof');need(not any(s in(N/'classification.log').read_text()for s in ['Warning','Overfull','Underfull']),'Clean native proof')
  if(P/'classification.pdf').exists():need(pages==texts(P/'classification.pdf'),'Exact native text')
  run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','classification.pdf'],'render',N,60);native=dict(pages=6,text_identical=(P/'classification.pdf').exists())
 report=dict(status='PASS_L076_CLASSIFICATION_COMPONENT',finite_fields=14,torus_cases=28,geometry_representatives=19,independent_swap_checks=4,damage_controls=damages,optimization_guards=guards,native=native,commands=commands,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None,seconds=time.monotonic()-t)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
