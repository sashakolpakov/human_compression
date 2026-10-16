"""Bounded L091 admission controls; no mathematical search or bulk restore."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,copy,subprocess
import portable_check as p
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 p.need(a.out.is_absolute() and not a.out.exists(),'fresh absolute control output');a.out.mkdir()
 D=a.stage/p.PREFIX;t=p.load(D/'transport.json');policy=p.load(D/'premises.json')
 positive=p.metadata(p.Archive(a.stage,a.repo,t),policy);passed=[]
 def trial(name,z,pol=policy):
  try:p.metadata(p.Archive(a.stage,a.repo,z),pol)
  except (ValueError,KeyError):passed.append(name)
  else:raise ValueError('damaged admission accepted: '+name)
 z=dict(t,root_acceptance=dict(t['root_acceptance'],sha256='0'*64));trial('wrong whole-source acceptance',z)
 z=dict(t,author_manifest=dict(t['author_manifest'],sha256='0'*64));trial('wrong author',z)
 z=dict(t,logical_files=t['logical_files'][:-1]);trial('missing logical binding',z)
 z=dict(t,logical_files=t['logical_files']+[t['logical_files'][0]]);trial('duplicate logical binding',z)
 z=dict(t,logical_files=[dict(t['logical_files'][0],path='../escaped')]+t['logical_files'][1:]);trial('unsafe logical route',z)
 z=dict(t,objects=dict(t['objects']));z['objects'].pop(t['logical_files'][0]['sha256']);trial('missing object',z)
 z=dict(t,objects=dict(t['objects']));h=t['logical_files'][0]['sha256'];z['objects'][h]=dict(z['objects'][h],bytes=z['objects'][h]['bytes']+1);trial('wrong decoded length',z)
 ar=p.Archive(a.stage,a.repo,t);h=ar.originals[p.A+'/verify.py']['sha256'];z=dict(t,objects=dict(t['objects']))
 z['objects'][h]=dict(kind='DOCUMENTARY_SOURCE_PREMISE',sha256=h,bytes=z['objects'][h]['bytes'],exact_locator=p.A+'/verify.py',reason='not allowed')
 trial('scientific reader cannot become premise',z)
 pol=copy.deepcopy(policy);pol['premises']=pol['premises'][1:];trial('missing approved premise',t,pol)
 pol=dict(policy,premises=policy['premises']+[policy['premises'][0]]);trial('duplicate approved premise',t,pol)
 z=dict(t,premises=t['premises']+[t['premises'][0]]);trial('duplicate used premise',z)
 z=dict(t,environment_aliases=t['environment_aliases'][:-1]);trial('missing literal environment alias',z)
 z=dict(t,environment_aliases=copy.deepcopy(t['environment_aliases']));z['environment_aliases'][0]['canonical']['sha256']='0'*64;trial('wrong canonical environment alias',z)
 for name,fn in [('no private fallback',lambda:ar.content('/etc/hosts')),('premise cannot execute',lambda:ar.content(t['premises'][0]['exact_locator']))]:
  try:fn()
  except (ValueError,KeyError):passed.append(name)
  else:raise ValueError('rejected boundary admitted '+name)
 cli=[]
 for name,stage_sha,transport_sha in [('wrong_stage','0'*64,p.pin(D/'transport.json')['sha256']),('wrong_transport',p.pin(D/'manifest.json')['sha256'],'0'*64)]:
  out=a.out/name;cmd=[sys.executable,str(D/'portable_check.py'),'--stage',str(a.stage),'--repo',str(a.repo),'--out',str(out),'--expected-stage',stage_sha,'--expected-transport',transport_sha]
  q=subprocess.run(cmd,capture_output=True,timeout=20);p.need(q.returncode!=0 and not(out/'report.json').exists(),'real CLI exact gate rejection')
  (a.out/(name+'.stderr')).write_bytes(q.stderr);cli.append(name)
 guards=[]
 for script in ['portable_check.py','portable_controls.py','codec_controls.py']:
  for option in ['-O','-OO']:
   q=subprocess.run([sys.executable,option,str(D/script)],capture_output=True,timeout=10)
   p.need(q.returncode!=0 and b'ordinary Python required' in q.stderr,'actual ordinary-Python guard');guards.append(script+option)
 result=dict(status='PASS_L091_PORTABLE_ADMISSION_CONTROLS',positive=positive,metadata_and_boundary_rejections=passed,real_cli_rejections=cli,optimization_guards=guards,new_scientific_targets=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
