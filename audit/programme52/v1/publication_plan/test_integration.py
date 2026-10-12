#!/usr/bin/env python3
"""Test proposed additions through a private read-only view of the full public tree."""
from pathlib import Path
import argparse,json,subprocess,sys,shutil
from stage import run as stage_run
from prepare import H,load,need

def merge(old,new,out):
 out.mkdir()
 names={p.name for p in old.iterdir()}|({p.name for p in new.iterdir()}if new.exists()else set())
 for name in names:
  a=old/name;b=new/name;c=out/name
  if b.is_dir()and a.is_dir():merge(a,b,c)
  elif b.exists():c.symlink_to(b,target_is_directory=b.is_dir())
  else:c.symlink_to(a,target_is_directory=a.is_dir())
def run(study,repo,out):
 out=out.resolve();repo=repo.resolve();need(not out.exists()and not out.is_relative_to(repo),'fresh private output');out.mkdir()
 stage=out/'stage';stage_report=stage_run(study,repo,stage,False)
 target=stage/'audit/programme52/v1/publication_plan';target.mkdir(parents=True)
 if(H/'manifest.json').exists():
  paths=[z['path']for z in load(H/'manifest.json')['exports']]+['manifest.json']
 else:paths=[str(p.relative_to(H))for p in H.rglob('*')if p.is_file()and '__pycache__'not in p.parts]
 for name in paths:
  dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(H/name,dest)
 view=out/'public_view';merge(repo,stage,view)
 proc=subprocess.run([sys.executable,'-B',str(view/'scripts/check_programme52.py'),'--repo',str(view),'--allow-pending-overview'],capture_output=True,text=True)
 (out/'current_guard.log').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'current guard; see log');current=json.loads(proc.stdout)
 base=(repo/'scripts/verify_snapshot.py').read_text();base=base[:base.rfind('if __name__')]
 ns={'__name__':'programme52_private_integration','__file__':str(repo/'scripts/verify_snapshot.py')};exec(compile(base,str(repo/'scripts/verify_snapshot.py'),'exec'),ns);ns['ROOT']=view
 exec(compile((H/'verifier_additions.py').read_text(),'proposed additions','exec'),ns)
 history=ns['check_previous_programme52']();measured=ns['check_current_measurement_pointer']();need(measured==52,'unique current measurements')
 result=dict(status='PASS_PRIVATE_CURRENT_AND_HISTORICAL_INTEGRATION',exact_stage=stage_report,current_guard=current,historical_programme_and_documentation=history,current_unique_measured_originals=measured,old_nonmain_ASTs=130,public_writes=False,root_overview_admission_pending=True)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.study_root,a.repo,a.out);print(json.dumps({k:v for k,v in r.items()if k not in ['current_guard','historical_programme_and_documentation','exact_stage']},indent=2))
