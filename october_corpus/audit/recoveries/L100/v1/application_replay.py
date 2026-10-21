"""Explicit portable envelope for the byte-unchanged L100 interface assembly."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,os,shutil,subprocess,time
from pathlib import Path
def need(x,s):
 if not x:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--volume',type=Path,required=True);ap.add_argument('--policy',type=Path,required=True);a=ap.parse_args();S=a.study.resolve();P=S/'geometry/psl3_4/principal_component_v1';O=a.out.resolve();need(not O.exists(),'Fresh output');O.mkdir(parents=True)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 def run(name,cmd,cap=60,cwd=None):
  start=time.monotonic();rc=None;deadline=False
  with (O/(name+'.stdout')).open('wb') as out,(O/(name+'.stderr')).open('wb') as err:
   try:r=subprocess.run(cmd,stdout=out,stderr=err,timeout=cap,cwd=cwd,env=env);rc=r.returncode
   except subprocess.TimeoutExpired:deadline=True
  save(O/(name+'.receipt.json'),dict(command=cmd,cap_seconds=cap,exit_code=rc,deadline=deadline,seconds=time.monotonic()-start));need(rc==0 and not deadline and not (O/(name+'.stderr')).stat().st_size,'Clean '+name)
 run('assemble',[sys.executable,str(P/'assemble.py'),'--out',str(O/'join')])
 for name in ('claim_register.json','catalogue.json','execution_join.json','bibliography_routes.json','report.json'):need(read(O/'join'/name)==read(P/'expected'/name),'Accepted complete interface '+name)
 need((O/'join/catalogue.tex').read_bytes()==(P/'catalogue.tex').read_bytes(),'Literal adjacent TeX table')
 report=read(O/'join/report.json');need(len(report['damages'])==16 and report['anchors']==95 and report['inner_families']==145 and report['models']==29,'Actual unchanged assembly controls/scope')
 guards=[]
 for script in (P/'assemble.py',P/'check.py',Path(__file__).resolve()):
  for mode in ('argument','environment'):
   e=env.copy();cmd=[sys.executable]
   if mode=='argument':cmd.append('-O')
   else:e['PYTHONOPTIMIZE']='1'
   dst=O/(script.stem+'_'+mode+'_FORBIDDEN');cmd.extend([str(script),'--out',str(dst)]);r=subprocess.run(cmd,capture_output=True,timeout=10,env=e);(O/(script.stem+'_'+mode+'.stderr')).write_bytes(r.stderr);need(r.returncode!=0 and b'normal Python required' in r.stderr and not dst.exists(),'Optimization guard');guards.append([script.name,mode])
 from pypdf import PdfReader
 policy=read(a.policy);volume=PdfReader(a.volume);page=0
 for m in policy['manuscripts']:
  part=PdfReader(S/m['logical_pdf']);need(len(part.pages)==m['physical_pages'],'Exact component page count')
  for p in part.pages:need(p.extract_text()==volume.pages[page].extract_text(),'Exact complete-volume page');page+=1
 need(page==len(volume.pages)==36,'Complete 36-page volume')
 N=O/'native';N.mkdir();tex=shutil.which('pdflatex');gs=shutil.which('gs');need(tex and gs,'Installed TeX/Ghostscript')
 for i in range(2):run('native'+str(i+1),[tex,'-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'principal.tex')],cwd=P)
 need(not any(t in (N/'principal.log').read_text() for t in ('Warning','Overfull','Underfull')),'Clean native layout')
 old=PdfReader(P/'principal.pdf');new=PdfReader(N/'principal.pdf');need(len(old.pages)==len(new.pages)==7 and [p.extract_text() for p in old.pages]==[p.extract_text() for p in new.pages],'Exact seven-page native texts')
 run('render',[gs,'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(N/'page-%02d.png'),str(N/'principal.pdf')])
 result=dict(status='PASS_PUBLIC_L100_PRINCIPAL_APPLICATION',source_clauses=55,models=29,anchors=95,inner_families=145,corrections=6,retained_inputs=8,bibliography_attributions=47,damaged_controls=16,optimization_guards=len(guards),native_pages=7,complete_written_pages=36,native_text_identical=True,unchanged_author_assembly=True,private_source_fallback=False,target_censuses=0,new_Lean=0,new_question_credit=0,new_measurements=0,whole_original_credit=0)
 save(O/'report.json',result);print(json.dumps(result))
if __name__=='__main__':main()
