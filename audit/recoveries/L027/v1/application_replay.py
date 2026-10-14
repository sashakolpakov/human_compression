"""Explicit source-free adapter for unchanged L027 principal interface code.

The portable envelope verifies complete exports and 460 direct bindings, with
only its declared documentary assets hash-only. This adapter imports the exact
author verifier; it does not edit a program or repeat any group enumeration.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
import argparse,copy,json,os,shutil,subprocess
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();P=a.author.resolve();O=a.out.resolve();need(not O.exists(),'Fresh output');O.mkdir(parents=True);roots={'study':a.study.resolve(),'public':a.repo.resolve()};sys.path.insert(0,str(P))
 from verify_contract import verify,verify_pin
 result=verify(P,roots);need(result==load(P/'author_receipt/interfaces.json'),'Exact author interface result');save(O/'interfaces.json',result)
 from pypdf import PdfReader
 full=PdfReader(P/'complete_proof.pdf');parts=load(P/'complete_proof_routes.json')['parts'];index=0
 for part in parts:
  p=P/part['local_path']if 'local_path'in part else verify_pin(roots,part['source']);pdf=PdfReader(p);need(part['first_page']==index+1 and part['pages']==len(pdf.pages),'Full proof route')
  for page in pdf.pages:need(index<len(full.pages)and full.pages[index].extract_text()==page.extract_text(),'Exact acquired proof page');index+=1
 need(index==len(full.pages)==34,'Complete 34-page manuscript')
 controls=[]
 for label in('missing_numbered_clause','promoted_prior_census','psu17_exhaustion','question_credit','suppressed_q81'):
  sm=copy.deepcopy(load(P/'source_map.json'));rt=copy.deepcopy(load(P/'retained_inputs.json'));sc=copy.deepcopy(load(P/'scope.json'))
  if label=='missing_numbered_clause':sm['clauses']=[x for x in sm['clauses']if x['id']!='T6.1']
  elif label=='promoted_prior_census':next(x for x in rt['records']if x['id']=='R9')['evidence_status']='ACQUIRED_PROJECT_PRINCIPAL_THEOREM'
  elif label=='psu17_exhaustion':next(x for x in sm['clauses']if x['id']=='S7.psu17')['qualification']='Complete census, exactly three pairs.'
  elif label=='question_credit':sc['new_question_credit']=1
  else:next(x for x in sm['clauses']if x['id']=='S7.psl2_list')['disposition']='RETAINED_UNCHANGED'
  try:verify(P,roots,sm,rt,sc)
  except ValueError as e:controls.append(dict(case=label,rejected=True,reason=str(e)))
  else:raise ValueError('Damaged interface accepted '+label)
 save(O/'negative_controls.json',controls);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';guards=[]
 for script in(P/'check.py',P/'verify_contract.py',Path(__file__).resolve()):
  for mode in('argument','environment'):
   e=env.copy();cmd=[sys.executable]
   if mode=='argument':cmd.append('-O')
   else:e['PYTHONOPTIMIZE']='1'
   dest=O/(script.name+'_'+mode+'_forbidden');cmd.extend([str(script),'--out',str(dest)]);z=subprocess.run(cmd,capture_output=True,env=e,timeout=10);(O/(script.name+'_'+mode+'.stderr')).write_bytes(z.stderr);need(z.returncode!=0 and b'unoptimized'in z.stderr.lower()and not dest.exists(),'Optimization rejection before output');guards.append(dict(script=script.name,mode=mode,rejected=True))
 save(O/'optimization_guards.json',guards);N=O/'native';N.mkdir();shutil.copy2(P/'principal.tex',N/'principal.tex')
 for i in range(2):
  z=subprocess.run(['pdflatex','-halt-on-error','-interaction=nonstopmode','principal.tex'],cwd=N,env=env,capture_output=True,timeout=60);(N/f'build{i}.stdout').write_bytes(z.stdout);(N/f'build{i}.stderr').write_bytes(z.stderr);need(z.returncode==0 and not z.stderr,'Native build')
 log=(N/'principal.log').read_text();need('Overfull'not in log and 'LaTeX Warning'not in log,'Native layout/reference warnings');pdf=PdfReader(N/'principal.pdf');text='\n'.join(p.extract_text()or''for p in pdf.pages);(N/'text.txt').write_text(text);need(text==(P/'native_expected.txt').read_text()and len(pdf.pages)==3,'Exact synthesis native text')
 z=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','principal.pdf'],cwd=N,capture_output=True,timeout=60);need(z.returncode==0 and not z.stderr,'Native rendering')
 report=dict(status='PASS_PUBLIC_L027_APPLICATION',interfaces=result,damaged_controls=len(controls),optimization_guards=len(guards),native_pages=3,complete_written_pages=index,native_text_identical=True,unchanged_author_mathematical_code=True,primary_source_replayed=False,new_census=False,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0);save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
