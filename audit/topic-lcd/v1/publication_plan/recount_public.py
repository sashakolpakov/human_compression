#!/usr/bin/env python3
"""Recount published LCD files and separately supplied originals in a private tree.

No scientific program runs. No primary PDF is copied into the publication tree.
The frozen original measurement checker and exact logical paths are preserved.
"""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(p,r):need(p.is_file()and p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'exact input '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True,help='Directory containing catalogue_L050.pdf and lcd_followup2018.pdf.');ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();pub=a.public_root.resolve();out=a.out.resolve()
 need(not out.exists()and out!=pub and pub not in out.parents,'fresh output outside public repository');out.mkdir(parents=True);logical=out/'logical_study';logical.mkdir()
 plan=read(HERE/'assembly_map.json');count=0
 for r in plan['new_copies']:
  # The numerical packet is not an extraction input.
  if r['packet']=='topic_LCD_measurement_results':continue
  source=pub/r['public_path'];bound(source,r);dest=logical/r['study_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest);count+=1
 inp=logical/'topic_LCD_measurement_inputs_v2'
 policy=read(inp/'policy.json');old=logical/policy['previous_stage_manifest']['path'];old.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(inp/'previous_stage/manifest.json',old);bound(old,policy['previous_stage_manifest'])
 for r in read(inp/'document_map.json')['documents']:
  if r['role']!='source':continue
  source=a.sources_root/Path(r['path']).name;bound(source,r);dest=logical/r['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
 cmd=[sys.executable,'-B','-O',str(inp/'check.py'),'--study-root',str(logical),'--out',str(out/'recount')]
 if a.render:cmd+=['--render','--xelatex',a.xelatex]
 p=subprocess.run(cmd,capture_output=True,text=True);(out/'replay.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'frozen public-input replay; see replay.log')
 r=read(out/'recount/report.json');need(r['PDF_metric_cells']==150 and r['known_file_metric_cells']==1020 and r['pages']==69,'complete public input recount')
 report=dict(status='PASS_PUBLIC_PATH_LCD_INPUT_RECOUNT',copied_public_routes=count,source_PDFs_supplied_separately=2,PDF_cells=150,raw_cells=1020,pages=69,controls=len(r['controls']),scientific_programs_executed=False,public_files_modified=False,source_assets_exported=False,author_packet_mutated=False,reader_render=r['reader_render'])
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
