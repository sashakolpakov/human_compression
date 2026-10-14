"""Explicit source-free adapter for unchanged L045 assembly mathematics."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
import argparse,copy,json,os,shutil,subprocess
from pathlib import Path

def need(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def main():
 a=argparse.ArgumentParser();a.add_argument('--study',type=Path,required=True);a.add_argument('--author',type=Path,required=True);a.add_argument('--out',type=Path,required=True);q=a.parse_args();S=q.study.resolve();P=q.author.resolve();O=q.out.resolve();need(not O.exists(),'Fresh output');O.mkdir(parents=True);sys.path.insert(0,str(P))
 from check_register import validate
 claims=load(P/'claim_register.json');coverage=load(P/'coverage.json');components=load(P/'components.json');result=validate(claims,coverage,components,True)
 negatives=[]
 for name in ['missing_family','false_announcement','regular_as_principal','new_count','missing_finite','nonsimple_finite','sporadic_overlap','premature_complete_gate']:
  c=copy.deepcopy(claims);v=copy.deepcopy(coverage);m=copy.deepcopy(components);byid={r['id']:r for r in c['claims']}
  if name=='missing_family':byid['P1']['route'].remove('P1O')
  elif name=='false_announcement':byid['N3']['status']='ACCEPTED_PRINCIPAL_NEGATIVE'
  elif name=='regular_as_principal':byid['G2']['kind']='principal'
  elif name=='new_count':byid['H_count_M11']['status']='NEW_EXHAUSTIVE_COUNT'
  elif name=='missing_finite':v['finite_parameter_routes'].pop()
  elif name=='nonsimple_finite':v['finite_parameter_routes'][0]['parameters']=['S',4,2]
  elif name=='sporadic_overlap':v['sporadic_fourteen'][0]=v['sporadic_twelve'][0]
  else:next(x for x in m['components']if x['id']=='orthogonal_counting')['review_state']='PENDING_DISTINCT_REVIEW'
  try:validate(c,v,m,True)
  except ValueError:negatives.append(name)
  else:raise ValueError('Bad source contract accepted '+name)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';guards=[]
 for script in [P/'check.py',P/'check_register.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(script),'--out',str(O/(script.name+mode))];e=dict(env)
   if mode=='environment':e['PYTHONOPTIMIZE']='1'
   p=subprocess.run(cmd,env=e,capture_output=True,timeout=15);(O/(script.name+mode+'.stderr')).write_bytes(p.stderr);need(p.returncode!=0 and b'optimiz'in p.stderr.lower()and not(O/(script.name+mode)).exists(),'Optimization guard');guards.append([script.name,mode])
 from pypdf import PdfReader
 def texts(p):return [x.extract_text()for x in PdfReader(p).pages]
 full=texts(P/'principal.pdf');inventory=load(P/'acquired_manuscripts.json')['manuscripts']
 for row in inventory:
  pages=texts(S/row['pdf']['path']);need(len(pages)==row['pages'],'Complete acquired pages');full.extend(pages)
 need(len(full)==58 and len(inventory)==14 and texts(P/'complete_proof.pdf')==full,'Exact 58-page complete reading volume')
 N=O/'native';N.mkdir();shutil.copy2(P/'principal.tex',N/'principal.tex')
 for n in [1,2]:
  p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','principal.tex'],cwd=N,env=env,capture_output=True,timeout=60);(N/f'pass{n}.stdout').write_bytes(p.stdout);(N/f'pass{n}.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'Native build')
 pages=texts(N/'principal.pdf');need(len(pages)==7 and '\n\f\n'.join(pages)==(P/'principal_expected.txt').read_text(),'Exact native text');log=(N/'principal.log').read_text();need(not any(t in log for t in ['Overfull','Underfull','LaTeX Warning:','undefined references']),'Native warnings')
 p=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','principal.pdf'],cwd=N,env=env,capture_output=True,timeout=60);need(p.returncode==0 and not p.stderr,'Native render')
 report=dict(status='PASS_PUBLIC_L045_APPLICATION',interfaces=result,damaged_controls=negatives,optimization_guards=guards,acquired_manuscripts=14,acquired_pages=51,synthesis_pages=7,full_reading_volume_pages=58,native_pages=7,native_text_identical=True,unchanged_author_mathematical_code=True,documentary_source_replayed=False,new_census=False,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
