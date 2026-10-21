import sys
if sys.flags.optimize: raise RuntimeError('ordinary Python required')
from pathlib import Path
import os,subprocess,json
W=Path(__file__).parent; D=W.parent/'publication_work/registration_drafts';R=W.parent/'publication_work/trial01'
O=W/'optimization01';O.mkdir()
records=[]
for name,args in [('check_science89.py',['--repo',str(R),'--preflight']),('integrate_science89.py',['--repo',str(O/'must_not_exist'),'--bundle',str(W.parent/'publication_work/bundle01')]),('check_science89_history.py',[])]:
 for mode in ['argument','environment']:
  cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(D/name)]+args
  env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
  if mode=='environment':env['PYTHONOPTIMIZE']='1'
  r=subprocess.run(cmd,env=env,capture_output=True,timeout=10)
  if r.returncode==0 or b'Ordinary Python required'not in r.stderr or r.stdout or(O/'must_not_exist').exists():raise ValueError((name,mode))
  stem=name[:-3]+'_'+mode;(O/(stem+'.stdout')).write_bytes(r.stdout);(O/(stem+'.stderr')).write_bytes(r.stderr)
  records.append(dict(script=name,mode=mode,command=cmd,returncode=r.returncode,rejected_before_filesystem_work=True))
(O/'report.json').write_text(json.dumps(dict(status='PASS',controls=records),indent=2)+'\n');print('PASS six optimization guards')
