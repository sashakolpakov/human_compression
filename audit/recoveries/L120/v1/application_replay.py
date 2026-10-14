"""Source-free L120 interface replay; immutable author code is imported unchanged.

This explicit adapter omits only the private documentary-source argument and
its filesystem checks. The enclosing portable checker pays every retained
mathematical dependency and every complete manifest export before this runs.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
import argparse,copy,json,os,subprocess,shutil
from pathlib import Path

def need(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();S=a.study.resolve();P=a.author.resolve();O=a.out.resolve();need(not O.exists(),'Fresh output required');O.mkdir(parents=True);sys.path.insert(0,str(P))
 from verify_contract import verify,check_marking
 result=verify(P,S);expected=load(P/'expected.json');need({k:v for k,v in result.items()if k!='source_replay'}=={k:v for k,v in expected.items()if k!='source_replay'},'Exact complete source-free interface result');need(result['source_replay']is None,'No original-source fallback');save(O/'interfaces.json',result)
 scope=load(P/'survey_table_scope09.json');clauses=load(P/'named_clause_register03.json');figure=load(P/'survey_figure_records01.json');bad=[]
 x=copy.deepcopy(scope);x['rows'].pop();bad.append(('missing_source_cell',lambda:verify(P,S,scope=x)))
 y=copy.deepcopy(scope);y['rows'][0]['comparison_value']+=1;bad.append(('changed_acquired_count',lambda:verify(P,S,scope=y)))
 z=copy.deepcopy(scope);next(r for r in z['rows']if r['disposition']=='retained_independent_published_classification')['disposition']='acquired_project_result';bad.append(('promoted_retained_classification',lambda:verify(P,S,scope=z)))
 c=copy.deepcopy(clauses);c['clauses'].pop();bad.append(('missing_source_question',lambda:verify(P,S,clauses=c)))
 f=copy.deepcopy(figure);f['records'][0]['to_model']['point_map'][0],f['records'][0]['to_model']['point_map'][1]=f['records'][0]['to_model']['point_map'][1],f['records'][0]['to_model']['point_map'][0];bad.append(('wrong_diagram_transport',lambda:verify(P,S,figure=f)))
 m=copy.deepcopy(load(P/'table_interfaces01.json')['table4_literal_controls'][0]);m['marks'][0][0]=999;bad.append(('invalid_construction_literal',lambda:check_marking(m['marks'],m['degree'],m['type'])))
 negative=[]
 for name,action in bad:
  try:action()
  except ValueError as e:negative.append(dict(case=name,rejected=True,message=str(e)))
  else:raise ValueError('Damaged interface passed '+name)
 save(O/'negative_controls.json',negative);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';guards=[]
 for script in(P/'check.py',P/'verify_contract.py',Path(__file__).resolve()):
  for mode in('argument','environment'):
   e=env.copy();cmd=[sys.executable]
   if mode=='argument':cmd.append('-O')
   else:e['PYTHONOPTIMIZE']='1'
   dest=O/(script.name+'_'+mode+'_forbidden');cmd.extend([str(script),'--out',str(dest)]);r=subprocess.run(cmd,capture_output=True,timeout=10,env=e);(O/(script.name+'_'+mode+'.stderr')).write_bytes(r.stderr);need(r.returncode!=0 and b'unoptimized'in r.stderr.lower()and not dest.exists(),'Optimization rejection before output');guards.append(dict(script=script.name,mode=mode))
 save(O/'optimization_guards.json',guards)
 N=O/'native';N.mkdir();shutil.copy2(P/'survey.tex',N/'survey.tex')
 for i in range(2):
  cmd=['pdflatex','-halt-on-error','-interaction=nonstopmode','survey.tex'];r=subprocess.run(cmd,cwd=N,env=env,capture_output=True,timeout=60);(N/f'build{i}.stdout').write_bytes(r.stdout);(N/f'build{i}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'Native build')
 log=(N/'survey.log').read_text();need('Overfull'not in log and 'LaTeX Warning'not in log,'Native layout/reference warning')
 from pypdf import PdfReader
 pdf=PdfReader(N/'survey.pdf');text='\n'.join(p.extract_text()or''for p in pdf.pages);(N/'text.txt').write_text(text);need(text==(P/'native_expected.txt').read_text(),'Exact final native text')
 r=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile=page-%02d.png','survey.pdf'],cwd=N,capture_output=True,timeout=60);need(r.returncode==0 and not r.stderr,'Native rendering')
 report=dict(status='PASS_PUBLIC_L120_APPLICATION',interfaces=result,damaged_controls=len(negative),optimization_guards=len(guards),native_pages=len(pdf.pages),native_text_identical=True,unchanged_author_mathematical_code=True,primary_source_replayed=False,new_census=False,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0);save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
