#!/usr/bin/env python3
"""Replay frozen B6 input checker using public payloads and supplied originals."""
from pathlib import Path
import argparse,json,hashlib,subprocess,sys
H=Path(__file__).resolve().parent

def need(v,m):
 if not v:raise ValueError(m)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--originals-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();root=a.repo.resolve();out=a.out.resolve();need(not out.exists()and not out.is_relative_to(root),'fresh output outside repository');out.mkdir(parents=True)
 routes=json.loads((H/'public_input_routes.json').read_text());study=out/'study';study.mkdir();checked=[]
 for row in routes['files']:
  path=Path(row['path']);need(not path.is_absolute()and'..'not in path.parts,'safe alias');src=root/row['public_path']if row['source_kind']=='public_payload'else a.originals_root/path
  b=src.read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'exact input '+str(path));dst=study/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.symlink_to(src.resolve());checked.append(dict(path=str(path),source_kind=row['source_kind'],sha256=row['sha256']))
 packet=root/routes['frozen_input_public_path'];need(hashlib.sha256((packet/'manifest.json').read_bytes()).hexdigest()==routes['frozen_input_manifest_sha256'],'frozen input packet')
 cmd=[sys.executable,'-B','-O',str(packet/'check.py'),'--study-root',str(study),'--public-root',str(root),'--out',str(out/'replay')]
 if a.render:cmd+=['--render','--xelatex',a.xelatex]
 q=subprocess.run(cmd,capture_output=True,text=True);(out/'stdout.log').write_text(q.stdout);(out/'stderr.log').write_text(q.stderr);need(q.returncode==0,'frozen input replay failed; see logs');result=json.loads((out/'replay/report.json').read_text());report=dict(status='PASS_PUBLIC_ROUTED_B6_INPUT_REPLAY',routes=checked,originals_supplied_not_exported=6,scope=routes['replay_scope'],frozen_checker_result=result,programs_or_Lean_run=False,public_mutations=False);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'routes':len(checked),'main_cells':result['whole_document_cells'],'raw_cells':result['whole_raw_cells']}))
if __name__=='__main__':main()
