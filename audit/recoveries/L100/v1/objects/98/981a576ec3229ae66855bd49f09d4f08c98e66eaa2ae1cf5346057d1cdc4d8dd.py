"""Focused level-resume controls; no unfinished L100 search is executed."""
import argparse,copy,importlib.util,json,subprocess,sys,os
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('resume_wrapper',HERE/'run_level_resume.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute();out.mkdir(parents=True,exist_ok=False)
 base,pins=m.preflight();d=json.loads((m.PRIOR/'receipt.json').read_text());stdout=(m.PRIOR/'target/stdout').read_text();damages=[]
 mutations=[lambda d:d.update(status='COMPLETE_REQUEST'),lambda d:d.update(completed_anchors=[1]),lambda d:d.update(requested_anchors=[2]),lambda d:d['execution'].update(status='RETURNED'),lambda d:d['audit'].update(returncode=1),lambda d:d.update(reported_completed_rows=[[1,[],[]]])]
 for i,f in enumerate(mutations):
  z=copy.deepcopy(d);f(z)
  try:m.prior_shape(z,stdout)
  except ValueError:damages.append(['receipt',i])
  else:raise AssertionError('prior damage accepted')
 for i,s in enumerate([stdout.replace('classes=334','classes=333'),stdout+'BOREL_COMPLETE id=1\n',stdout.replace('BOREL_LEVEL id=1 rank=3','BOREL_LEVEL id=1 rank=5')]):
  try:m.prior_shape(d,s)
  except ValueError:damages.append(['stdout',i])
  else:raise AssertionError('prior marker damage accepted')
 command=[sys.executable,str(HERE/'run_level_resume.py'),'--out',str(out/'prepared'),'--prepare-only'];r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
 (out/'prepare.stdout').write_bytes(r.stdout);(out/'prepare.stderr').write_bytes(r.stderr);assert r.returncode==0 and not r.stderr
 for mi in range(1,4):
  (out/f'm{mi}full').mkdir()
  for cut in range(2,5):(out/f'm{mi}resume{cut}').mkdir()
 q=lambda x:json.dumps(str(x))
 driver=out/'tiny.g';driver.write_text('SizeScreen([100000,24]);;\nG:=Group(());;reps:=[];;maxinclusions:=[];;maxorders:=rec();;REQUIRE_2T:=false;;local2T:=[];;OUTPUT_DIR:="";;\n'+''.join('Read('+q(p)+');;\n' for p in [base.P/'legacy_functions.g',HERE/'resume_borel.g',HERE/'validate_resume.g',HERE/'resume_controls.g'])+'TestLevelResume([Group((1,2),(3,4)),Group((1,2),(3,4),(5,6)),Group((1,2,3),(4,5),(6,7))],'+q(out)+');;QUIT_GAP(0);\n')
 tiny=base.phase([str(base.GAP),'-q','-b',str(driver)],out/'tiny',25,False);text=(out/'tiny/stdout').read_text()
 if not base.clean_phase(tiny,out/'tiny') or 'PASS_COMPLETE_LEVEL_RESUME' not in text:raise RuntimeError('tiny resume controls failed')
 # Validate the exact existing L100 partial records only; do not invoke RunBorel.
 lines=['SizeScreen([100000,24]);;','OUTPUT_DIR:="";;', 'INPUT_CATALOGUE:='+q(base.P/'input_catalogue01.g')+';;','Read('+q(base.P/'catalogue_loader_v2.g')+');;','Read('+q(base.P/'legacy_functions.g')+');;','Read('+q(HERE/'validate_resume.g')+');;','borelCheckpoint:=rec();;cs:=[];;']
 for rank in range(2,5):lines+=['Read('+q(m.PRIOR/f'prepared/checkpoints/b1_r{rank}.g')+');;Add(cs,borelCheckpoint);;']
 lines+=['rr:=ValidateLevelResume(1,cs,[4,30,196,334]);;if rr=fail then Error("actual checkpoint validation");fi;','Print("PASS_ACTUAL_COMPLETED_LEVEL_INPUT_ONLY\\n");QUIT_GAP(0);']
 (out/'actual_input.g').write_text('\n'.join(lines)+'\n');actual=base.phase([str(base.GAP),'-q','-b',str(out/'actual_input.g')],out/'actual_input',20,False)
 if not base.clean_phase(actual,out/'actual_input') or 'PASS_ACTUAL_COMPLETED_LEVEL_INPUT_ONLY' not in (out/'actual_input/stdout').read_text():raise RuntimeError('actual input validation failed')
 guards=[]
 for n in ['run_level_resume.py','controls.py']:
  for kind in ['arg','env']:
   dest=out/(n+'_'+kind);cmd=[sys.executable]+(['-O'] if kind=='arg' else [])+[str(HERE/n),'--out',str(dest)];env=dict(os.environ)
   if kind=='env':env['PYTHONOPTIMIZE']='1'
   z=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5);assert z.returncode and not dest.exists() and b'optimized execution forbidden' in z.stderr;guards.append([n,kind,z.returncode])
 report=dict(status='PASS_COMPLETE_LEVEL_RESUME_CONTROLS_NO_TARGET',pins=len(pins),prior_damages=damages,guards=guards,tiny=tiny,tiny_stdout=text,actual_input=actual,target_runs=0)
 base.save(out/'report.json',report);print(json.dumps(dict(status=report['status'],damages=len(damages),guards=len(guards),tiny=text.splitlines()[-1])))
if __name__=='__main__':main()
