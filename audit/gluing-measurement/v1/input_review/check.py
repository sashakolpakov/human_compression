#!/usr/bin/env python3
"""Portable independent recount and bound copied-author replay (optional)."""
from pathlib import Path
import argparse, json, shutil, subprocess, sys
import recount as R
import controls, font_bindings

H=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--sources-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--author-replay',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args()
    R.need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
    for name,obj in [('recount.json',R.audit(a.packet,a.public_root,a.sources_root)),('controls.json',controls.run(a.packet,a.sources_root)),('font_bindings.json',font_bindings.run(a.packet,a.sources_root))]:
        R.need(obj==R.read(H/name),'exact independently reproduced '+name)
        (a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    copied=False
    if a.author_replay:
        dest=a.out/'author_exports';dest.mkdir()
        m=R.read(a.packet/'manifest.json')
        for r in m['exports']:
            rel=Path(r['path']);R.need(not rel.is_absolute() and '..' not in rel.parts,'relative manifest path')
            target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.packet/rel,target)
        shutil.copyfile(a.packet/'manifest.json',dest/'manifest.json')
        cmd=[sys.executable,'-B','-O',str((dest/'check.py').resolve()),'--sources-root',str(a.sources_root.resolve()),'--public-root',str(a.public_root.resolve()),'--out',str((a.out/'author_replay').resolve())]
        if a.render:cmd+=['--render','--xelatex',a.xelatex]
        run=subprocess.run(cmd,capture_output=True,text=True);(a.out/'author.log').write_text(run.stdout+run.stderr)
        R.need(run.returncode==0,'copied export-only author replay')
        report=R.read(a.out/'author_replay/report.json')
        expected=R.read(H/'copied_author_replay.json')
        if not a.render:expected['rendered']=[]
        R.need(report==expected,'fresh author report exactly matches inspected replay')
        copied=True
    report=dict(status='PASS',author_manifest_sha256=R.PIN,pdf_cells=150,raw_cells=80,text_hashes=46,independent_controls=16,actual_calibrated_events=175,copied_author_replay=copied,scientific_programs_executed=False,factors_evaluated=False)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS 230 cells / 46 text hashes / 16 independent controls')
if __name__=='__main__':main()
