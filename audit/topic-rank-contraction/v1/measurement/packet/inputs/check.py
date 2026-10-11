#!/usr/bin/env python3
"""Portable complete input replay, optionally rebuilding only the input reader."""
from pathlib import Path
import argparse,json,subprocess,sys,time
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args()
if a.out.exists():raise ValueError('fresh output required')
a.out.mkdir(parents=True);begin=time.monotonic()
def run(name,args):
 p=subprocess.run([sys.executable,'-B','-O',str(H/name)]+args,cwd=a.out,capture_output=True,text=True,timeout=120)
 (a.out/(name+'.stdout')).write_text(p.stdout);(a.out/(name+'.stderr')).write_text(p.stderr)
 if p.returncode:raise ValueError(name+' failed: '+p.stderr[-2000:])
run('extract_inputs.py',['--study-root',str(a.study_root.absolute()),'--out',str(a.out.absolute()/'inputs')])
report=json.loads((a.out/'inputs/report.json').read_text())
if a.render:
 run('build_reader.py',['--out',str(a.out.absolute()/'reader'),'--xelatex',a.xelatex,'--compare']);report['reader']=json.loads((a.out/'reader/report.json').read_text())
report['elapsed_seconds']=time.monotonic()-begin
(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
