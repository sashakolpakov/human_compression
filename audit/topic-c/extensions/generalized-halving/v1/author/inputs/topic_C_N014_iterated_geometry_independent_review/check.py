#!/usr/bin/env python3
"""Independent frozen review bindings, scope controls and local diagnostics."""
import argparse,copy,hashlib,json,subprocess,sys
from pathlib import Path
from check_local import run

def need(b,m):
 if not b:raise ValueError(m)
def sig(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def check_scope(s,rows):
 need(s['required_new_finite_programs']==[] and s['new_Lean']==[],'written-only new theorem')
 need(s['new_original_credit']==s['new_conjecture_credit']==0,'bounded credits')
 need(s['measurement'] is None and not s['whole_source_acceptance'],'bounded acceptance')
 need(s['optional_validation']==['check_coordinates.py'] and s['operational']==['check.py'],'roles')
 need(len(rows)==14 and len({r['id'] for r in rows})==14,'source clauses')
def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--author-replay',action='store_true');a=p.parse_args();h=Path(__file__).resolve().parent;a.out.mkdir(parents=True,exist_ok=False)
 for r in json.loads((h/'bindings.json').read_text())['files']:
  need(sig(a.study_root/r['path'])=={k:r[k] for k in ('bytes','sha256')},'binding '+r['path'])
 own=0
 if (h/'manifest.json').exists():
  for r in json.loads((h/'manifest.json').read_text())['exports']:
   need(sig(h/r['path'])=={k:r[k] for k in ('bytes','sha256')},'review export '+r['path']);own+=1
 author=a.study_root/'topic_C_N014_iterated_geometry';s=json.loads((author/'scope.json').read_text());rows=json.loads((author/'source_map.json').read_text())['rows'];check_scope(s,rows)
 mutations=[('whole-source overclaim','whole_source_acceptance',True),('required finite premise','required_new_finite_programs',['check_coordinates.py']),('formal overclaim','new_Lean',['all_geometry']),('measurement added','measurement',1),('source credit','new_original_credit',1)]
 controls=[]
 for label,key,value in mutations:
  t=copy.deepcopy(s);t[key]=value
  try:check_scope(t,rows)
  except ValueError:controls.append(label)
  else:raise ValueError('undetected '+label)
 try:check_scope(s,rows[:-1])
 except ValueError:controls.append('missing source figure')
 else:raise ValueError('missing source control failed')
 result=run();need(result==json.loads((h/'local_result.json').read_text()),'independent local result');(a.out/'local_result.json').write_text(json.dumps(result,indent=2)+'\n')
 if a.author_replay:
  cp=a.out/'author_copy';cp.mkdir()
  manifest=json.loads((author/'manifest.json').read_text())
  for name in ['manifest.json']+[x['path'] for x in manifest['exports']]:
   (cp/name).write_bytes((author/name).read_bytes())
  proc=subprocess.run([sys.executable,'-B','-O',str(cp/'check.py'),'--out',str(a.out/'author_replay'),'--study-root',str(a.study_root),'--render'],capture_output=True,text=True)
  (a.out/'author_stdout.txt').write_text(proc.stdout);(a.out/'author_stderr.txt').write_text(proc.stderr);need(proc.returncode==0,'author replay')
 report=dict(status='PASS',bound_files=len(json.loads((h/'bindings.json').read_text())['files']),own_exports=own,local_flags=sum(x['dual_cube_and_clique_checks'] for x in result['lower_flag_checks']),diagrams=len(result['diagrams']),shadow_graphs=len(result['shadow_graphs']),mathematical_controls=result['controls'],scope_controls=controls,author_replay=a.author_replay,whole_source_acceptance=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
