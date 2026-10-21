#!/usr/bin/env python3
"""Replay frozen A10 inputs from exact public exports and separately supplied originals."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
H=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--binding-only',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args();repo=a.repo.resolve();out=a.out.resolve();need(not out.exists()and not out.is_relative_to(repo),'fresh private output');out.mkdir(parents=True);study=out/'study';study.mkdir();spec=json.loads((H/'public_input_routes.json').read_text())
 for r in spec['routes']:
  src=(repo if r['from_root']=='public'else a.source_root)/r['from_path'];b=src.read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'bound '+str(src))
  if r['root']=='study':
   dest=study/r['path'];dest.parent.mkdir(parents=True,exist_ok=True)
   if not dest.exists():dest.symlink_to(src.resolve())
 if a.binding_only:cmd=[sys.executable,'-B','-O',str(repo/spec['input_packet']/'precount/check.py'),'--study-root',str(study),'--public-root',str(repo),'--out',str(out/'precount.json')]
 else:
  cmd=[sys.executable,'-B','-O',str(repo/spec['input_packet']/'check.py'),'--study-root',str(study),'--public-root',str(repo),'--out',str(out/'recount')]
  if a.render:cmd+=['--render']
 q=subprocess.run(cmd,text=True,capture_output=True);(out/'stdout.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'frozen input replay; see stdout.log')
 report=dict(status='PASS_PUBLIC_A10_INPUT_BINDINGS'if a.binding_only else'PASS_PUBLIC_A10_INPUT_RECOUNT',routes=len(spec['routes']),separately_supplied_originals=spec['user_original_count'],source_assets_exported=False,scientific_code_executed=False,full_recount=not a.binding_only);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
