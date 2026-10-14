"""Replay the final L027 principal interfaces and native synthesis."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
import argparse,copy,hashlib,json,os,shutil,subprocess,time
from pathlib import Path
from verify_contract import need,load,pin,verify_pin,verify
P=Path(__file__).resolve().parent

def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,default=Path('/Users/sasha/medusa/research/leemans'));ap.add_argument('--repo',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();S=a.study.resolve();R=(a.repo or S.parents[1]/'math_compression').resolve();O=a.out.resolve();need(not O.exists(),'fresh output required');roots={'study':S,'public':R}
 exports=[]
 if (P/'manifest.json').exists():
  exports=load(P/'manifest.json')['exports']
  for x in exports:need(pin(P/x['path'])=={k:x[k]for k in ('bytes','sha256')},'author export '+x['path'])
 deps=load(P/'dependencies.json')['files']
 for x in deps:verify_pin(roots,x)
 O.mkdir(parents=True);result=verify(P,roots);save(O/'interfaces.json',result)
 complete_pages=None
 if (P/'complete_proof.pdf').exists():
  from pypdf import PdfReader
  full=PdfReader(P/'complete_proof.pdf');parts=load(P/'complete_proof_routes.json')['parts'];index=0
  for part in parts:
   p=P/part['local_path'] if 'local_path'in part else verify_pin(roots,part['source'])
   pdf=PdfReader(p);need(part['first_page']==index+1 and part['pages']==len(pdf.pages),'complete proof page route')
   for page in pdf.pages:
    need(index<len(full.pages) and full.pages[index].extract_text()==page.extract_text(),'exact acquired proof page');index+=1
  need(index==len(full.pages),'complete proof has no omitted/additional page');complete_pages=index
 controls=[]
 for label in ('missing_numbered_clause','promoted_prior_census','psu17_exhaustion','question_credit','suppressed_q81'):
  sm=copy.deepcopy(load(P/'source_map.json'));rt=copy.deepcopy(load(P/'retained_inputs.json'));sc=copy.deepcopy(load(P/'scope.json'))
  if label=='missing_numbered_clause':sm['clauses']=[x for x in sm['clauses']if x['id']!='T6.1']
  elif label=='promoted_prior_census':next(x for x in rt['records']if x['id']=='R9')['evidence_status']='ACQUIRED_PROJECT_PRINCIPAL_THEOREM'
  elif label=='psu17_exhaustion':next(x for x in sm['clauses']if x['id']=='S7.psu17')['qualification']='Complete census, exactly three pairs.'
  elif label=='question_credit':sc['new_question_credit']=1
  else:next(x for x in sm['clauses']if x['id']=='S7.psl2_list')['disposition']='RETAINED_UNCHANGED'
  try:verify(P,roots,sm,rt,sc)
  except ValueError as e:controls.append(dict(case=label,rejected=True,reason=str(e)))
  else:raise ValueError('damaged interface passed '+label)
 save(O/'negative_controls.json',controls)
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);guards=[]
 for script in ('check.py','verify_contract.py'):
  for mode in ('argument','environment'):
   e=env.copy();cmd=[sys.executable]
   if mode=='argument':cmd.append('-O')
   else:e['PYTHONOPTIMIZE']='1'
   dest=O/(script+'_'+mode+'_forbidden');cmd.extend([str(P/script),'--out',str(dest)]);z=subprocess.run(cmd,capture_output=True,env=e,timeout=10);(O/(script+'_'+mode+'.stderr')).write_bytes(z.stderr);need(z.returncode!=0 and b'unoptimized execution required'in z.stderr and not dest.exists(),'optimization rejection');guards.append(dict(script=script,mode=mode,rejected=True))
 save(O/'optimization_guards.json',guards)
 pages=None
 if a.render:
  N=O/'native';N.mkdir();shutil.copy2(P/'principal.tex',N/'principal.tex')
  for i in range(2):
   cmd=['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','principal.tex'];start=time.monotonic();z=subprocess.run(cmd,cwd=N,env=env,capture_output=True,timeout=60);(N/f'build{i}.stdout').write_bytes(z.stdout);(N/f'build{i}.stderr').write_bytes(z.stderr);save(N/f'build{i}.json',dict(command=cmd,returncode=z.returncode,seconds=time.monotonic()-start));need(z.returncode==0 and not z.stderr,'native build')
  log=(N/'principal.log').read_text();need('Overfull'not in log and 'LaTeX Warning'not in log,'native layout/reference warnings')
  from pypdf import PdfReader
  pdf=PdfReader(N/'principal.pdf');pages=len(pdf.pages);text='\n'.join(p.extract_text()or''for p in pdf.pages);(N/'text.txt').write_text(text)
  if(P/'native_expected.txt').exists():need(text==(P/'native_expected.txt').read_text(),'exact final native text')
  z=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','principal.pdf'],cwd=N,capture_output=True,timeout=60);need(z.returncode==0,'native rendering')
 report=dict(status='PASS_L027_PRINCIPAL_INTERFACES',exports=len(exports),dependencies=len(deps),interfaces=result,damaged_controls=len(controls),optimization_guards=len(guards),native_pages=pages,complete_written_pages=complete_pages,mathematical_scope='Acquired proofs and distinct reviews; interface checks are not a new proof or census.',whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0);save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
