"""Finite example and exact editions. The general automorphism bound is written."""
import sys
if sys.flags.optimize:
    raise SystemExit('optimized execution is unsupported')
sys.dont_write_bytecode=True
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

def need(ok,why):
    if not ok: raise ValueError(why)
def digest(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--render',action='store_true')
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    out=args.out.resolve()
    need(not out.exists() and not out.is_relative_to(root),'fresh external output required')
    manifest=json.loads((root/'manifest.json').read_text())
    deps=json.loads((root/'dependencies.json').read_text())
    for r in manifest['exports']:
        need(digest(root/r['path'])=={k:r[k] for k in ('bytes','sha256')},'changed export')
    for r in deps:
        need(digest(Path(r['path']))=={k:r[k] for k in ('bytes','sha256')},'changed dependency')
    out.mkdir(parents=True)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    cmd=[sys.executable,'-B',str(root/'finite.py'),'--out',str(out/'finite.json')]
    r=subprocess.run(cmd,env=env,capture_output=True,timeout=60)
    (out/'finite.stdout').write_bytes(r.stdout);(out/'finite.stderr').write_bytes(r.stderr)
    need(r.returncode==0 and not r.stderr,'finite verification completed')
    finite=json.loads((out/'finite.json').read_text())
    need(finite==json.loads((root/'expected.json').read_text()),'exact finite result')
    damaged=[]
    for mode in ('mark','edge','local_pattern'):
        r=subprocess.run(cmd+['--damage',mode],env=env,capture_output=True,timeout=60)
        (out/f'damage_{mode}.stderr').write_bytes(r.stderr)
        need(r.returncode!=0 and b'ValueError' in r.stderr,'damaged example rejected')
        damaged.append(mode)
    guards=[]
    for name in ('check.py','finite.py'):
        for mode in ('argument','environment'):
            e=dict(env)
            if mode=='environment':e['PYTHONOPTIMIZE']='1'
            r=subprocess.run([sys.executable]+(['-O'] if mode=='argument' else [])+[str(root/name)],env=e,capture_output=True,timeout=10)
            (out/f'{name}.{mode}.stderr').write_bytes(r.stderr)
            need(r.returncode!=0 and b'optimized execution is unsupported' in r.stderr,'optimization rejected')
            guards.append([name,mode])
    pages=None
    if args.render:
        native=out/'native';native.mkdir()
        shutil.copy2(root/'counterexample.tex',native/'counterexample.tex')
        for i in range(2):
            r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','counterexample.tex'],cwd=native,capture_output=True,timeout=60)
            (native/f'build{i}.stdout').write_bytes(r.stdout);(native/f'build{i}.stderr').write_bytes(r.stderr)
            need(r.returncode==0 and not r.stderr,'native build')
        log=(native/'counterexample.log').read_text()
        need(not any(x in log for x in ('Warning','Overfull','Underfull')),'clean native output')
        from pypdf import PdfReader
        old=[p.extract_text() for p in PdfReader(root/'counterexample.pdf').pages]
        new=[p.extract_text() for p in PdfReader(native/'counterexample.pdf').pages]
        need(old==new,'native text agrees')
        pages=len(new)
        r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','counterexample.pdf'],cwd=native,capture_output=True,timeout=60)
        (native/'render.stdout').write_bytes(r.stdout);(native/'render.stderr').write_bytes(r.stderr)
        need(r.returncode==0 and not r.stderr,'native rendering')
    report={'status':'PASS_L029_EXPLICIT_COUNTEREXAMPLE','exports':len(manifest['exports']),
        'dependencies':len(deps),'vertices':28,'chambers':4368,'specified_group_order':1092,
        'full_group_order':2184,'subset_intersections':256,'residue_component_sizes':[6,6],
        'damage_controls':damaged,'optimization_guards':guards,'native_pages':pages,
        'whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__': main()
