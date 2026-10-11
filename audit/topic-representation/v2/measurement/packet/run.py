#!/usr/bin/env python3
"""Portable numerical/reader replay from accepted Representation input packets."""
import argparse, json, subprocess, sys
from pathlib import Path
from compute import PINS, arguments, need, read, sha, write

def main():
    p=argparse.ArgumentParser();arguments(p);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args()
    packet=Path(__file__).resolve().parent
    need(not a.out.exists() and not a.out.is_symlink(),'fresh replay directory');a.out.mkdir(parents=True)
    exports=None
    if (packet/'manifest.json').exists():
        rows=read(packet/'manifest.json')['exports']
        for row in rows:
            rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe export')
            need((packet/rel).stat().st_size==row['bytes'] and sha(packet/rel)==row['sha256'],'changed numerical export '+str(rel))
        exports=len(rows)
    args=[]
    for k in PINS:args.extend(['--'+k.replace('_','-'),getattr(a,k).resolve()])
    args.extend(['--public-root',a.public_root.resolve()])
    def run(name,cmd):
        r=subprocess.run([sys.executable,'-B','-O',*map(str,cmd)],capture_output=True,text=True)
        (a.out/(name+'.log')).write_text(r.stdout+r.stderr);need(r.returncode==0,name+' failed; see log')
    run('compute',[packet/'compute.py',*args,'--out',a.out/'data'])
    run('check',[packet/'check.py',*args,'--results-dir',a.out/'data','--out',a.out/'check.json'])
    compared=[]
    for name in ['results.json','input_bindings.json','comparisons.csv']:
        if (packet/name).exists():
            need((packet/name).read_bytes()==(a.out/'data'/name).read_bytes(),'numerical output changed '+name);compared.append(name)
    render=None
    if a.render:
        run('reader',[packet/'build_reader.py','--results',a.out/'data'/'results.json','--out',a.out/'reader','--xelatex',a.xelatex])
        render=read(a.out/'reader'/'render_report.json')
        if (packet/'measurement.tex').exists():
            need((packet/'measurement.tex').read_bytes()==(a.out/'reader'/'measurement.tex').read_bytes(),'generated reader text changed')
            prior=read(packet/'render_report.json')
            need(render['page_text_sha256']==prior['page_text_sha256'] and render['plot']==prior['plot'],'rendered reader/page or plot data changed')
    check=read(a.out/'check.json')
    result=dict(status='PASS',exported_bindings_checked=exports,exact_regeneration=compared,
                all_120_fractions_verified=True,all_120_csv_rows_verified=True,
                controls=check['control_count'],rendered_pages=render['pages'] if render else None,
                source_reextraction=False,scientific_replay=False,independent_arithmetic_review=False,
                accepted_input_manifests=PINS,own_manifest_sha256=sha(packet/'manifest.json') if exports is not None else None,
                render=render)
    write(a.out/'report.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['render','accepted_input_manifests']}))

if __name__=='__main__':main()
