"""Bounded admission damage controls on actual transport metadata, no census."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,copy,subprocess
import portable_check as p

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();p.need(not a.out.exists(),'fresh control output');a.out.mkdir()
 D=a.stage/p.PREFIX;t=p.jsonfile(D/'transport.json');policy=p.jsonfile(D/'premises.json');positive=p.validate_metadata(p.Archive(a.stage,a.repo,t),policy);passed=[]
 def trial(name,z,pol=policy):
  try:p.validate_metadata(p.Archive(a.stage,a.repo,z),pol)
  except (ValueError,KeyError):passed.append(name)
  else:raise ValueError('damaged admission accepted: '+name)
 z=dict(t,root_acceptance=dict(t['root_acceptance'],sha256='0'*64));trial('wrong whole-source acceptance',z)
 z=dict(t,author_manifest=dict(t['author_manifest'],sha256='0'*64));trial('wrong author',z)
 z=dict(t,logical_files=t['logical_files'][:-1]);trial('missing logical binding',z)
 z=dict(t,logical_files=t['logical_files']+[t['logical_files'][0]]);trial('duplicate logical binding',z)
 z=dict(t,logical_files=[dict(t['logical_files'][0],path='../escaped')]+t['logical_files'][1:]);trial('unsafe logical route',z)
 z=dict(t,objects=dict(t['objects']));z['objects'].pop(t['logical_files'][0]['sha256']);trial('missing object',z)
 z=dict(t,objects=dict(t['objects']));h=t['logical_files'][0]['sha256'];z['objects'][h]=dict(z['objects'][h],bytes=z['objects'][h]['bytes']+1);trial('wrong decoded length',z)
 ar=p.Archive(a.stage,a.repo,t);h=ar.originals[p.C+'/principal_v1/verify.py']['sha256'];z=dict(t,objects=dict(t['objects']));z['objects'][h]=dict(kind='DOCUMENTARY_SOURCE_PREMISE',sha256=h,bytes=z['objects'][h]['bytes'],exact_locator=p.C+'/principal_v1/verify.py',reason='not allowed');trial('scientific reader cannot become premise',z)
 pol=copy.deepcopy(policy);pol['premises']=[r for r in pol['premises']if r['sha256']!=t['premises'][0]['sha256']];trial('missing approved premise',t,pol)
 for name,fn in [('no private fallback',lambda:ar.content('/etc/hosts')),('premise cannot execute',lambda:ar.content(t['premises'][0]['exact_locator']))]:
  try:fn()
  except (ValueError,KeyError):passed.append(name)
  else:raise ValueError('rejected boundary admitted '+name)
 # Real CLI gates reject before any object replay. Partial output directories
 # are permitted for failure evidence, but no successful report is allowed.
 cli=[]
 for name,stage_sha,transport_sha in [('wrong_stage','0'*64,p.pin(D/'transport.json')['sha256']),('wrong_transport',p.pin(D/'manifest.json')['sha256'],'0'*64)]:
  out=a.out/name;cmd=[sys.executable,str(D/'portable_check.py'),'--stage',str(a.stage),'--repo',str(a.repo),'--out',str(out),'--expected-stage',stage_sha,'--expected-transport',transport_sha];q=subprocess.run(cmd,capture_output=True,timeout=20);p.need(q.returncode!=0 and not(out/'report.json').exists(),'real CLI exact gate rejection');(a.out/(name+'.stderr')).write_bytes(q.stderr);cli.append(name)
 guards=[]
 for script in ['portable_check.py','portable_controls.py','codec_controls.py']:
  for option in ['-O','-OO']:
   q=subprocess.run([sys.executable,option,str(D/script)],capture_output=True,timeout=10);p.need(q.returncode!=0 and b'ordinary Python required'in q.stderr,'actual optimization guard');guards.append(script+option)
 z=dict(status='PASS_L070_PORTABLE_ADMISSION_CONTROLS',positive=positive,metadata_and_boundary_rejections=passed,real_cli_rejections=cli,optimization_guards=guards,new_group_calls=0,new_censuses=0)
 (a.out/'report.json').write_text(json.dumps(z,indent=2)+'\n');print(json.dumps(z))
if __name__=='__main__':main()
