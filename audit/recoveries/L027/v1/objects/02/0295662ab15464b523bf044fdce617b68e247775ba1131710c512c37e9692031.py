"""Bounded controls for the uniform written even-characteristic proof."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from pypdf import PdfReader

P=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(p,row):need(pin(p)=={k:row[k] for k in ('bytes','sha256')},'changed input '+str(p))
def parse(stdout):
    text=stdout.decode().replace('\r','');rows=[]
    for line in text.splitlines():
        if line.startswith('MODEL '):
            need(re.fullmatch(r'MODEL \d+ (?:product|heisenberg|onezero) (?:\d+ ){4}PASS',line) is not None,'finite model receipt')
            rows.append(line.split())
        else:need(line=='PASS_ALL_ODD_FOUR_CONTROLS','unexpected receipt '+line)
    need(text.rstrip().endswith('PASS_ALL_ODD_FOUR_CONTROLS'),'complete terminal receipt')
    need(len(rows)==14 and len({tuple(r[:3]) for r in rows})==14,'fourteen distinct models')
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args();out=arg.out.resolve()
    need(not out.exists() and out!=P and P not in out.parents,'fresh external output')
    manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
    for row in manifest['exports']:verify(P/row['path'],row)
    for row in deps:verify(Path(row['path']),row)
    out.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);records=[]
    def run(label,cmd,cap,cwd=None):
        start=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=cap)
        (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
        records.append(dict(label=label,command=cmd,returncode=r.returncode,seconds=time.monotonic()-start))
        need(r.returncode==0,'execution '+label);return r
    run('literal',[sys.executable,str(P/'literal.py'),'--out',str(out/'literal.json')],30)
    literal=json.loads((out/'literal.json').read_text());need(literal==json.loads((P/'literal_expected.json').read_text()),'exact symbolic identities')
    r=run('finite',['/opt/homebrew/bin/gap','-q','-b',str(P/'finite.g')],180)
    need(not r.stderr,'clean finite stderr');rows=parse(r.stdout)
    need(rows==json.loads((P/'finite_expected.json').read_text()),'exact finite controls')
    guards=[]
    for mode in ['argument','environment']:
        ee=dict(env);cmd=[sys.executable];target=out/('optimized_'+mode)
        if mode=='argument':cmd.append('-O')
        else:ee['PYTHONOPTIMIZE']='1'
        r=subprocess.run([*cmd,str(P/'check.py'),'--out',str(target)],env=ee,capture_output=True,timeout=10)
        need(r.returncode!=0 and b'normal Python required' in r.stderr and not target.exists(),'optimization rejected')
        guards.append(mode)
    native=out/'native';native.mkdir();shutil.copy2(P/'odd_four.tex',native/'odd_four.tex')
    for i in [1,2]:run('latex'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','odd_four.tex'],30,native)
    log=(native/'odd_four.log').read_text();need(all(s not in log for s in ['Warning','Overfull','Underfull']),'clean final native')
    texts=lambda p:[x.extract_text() for x in PdfReader(p).pages]
    need(texts(native/'odd_four.pdf')==texts(P/'odd_four.pdf'),'native text identity')
    run('render',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','odd_four.pdf'],30,native)
    report=dict(status='PASS_L027_ODD_FOUR_CONTROLS',exports=len(manifest['exports']),dependencies=len(deps),
                finite_models=len(rows),exact_identities=literal['count'],
                subset_intersections=sum(int(x[-2]) for x in rows),positive_models=10,excluded_models=4,
                guards=guards,native_pages=len(texts(native/'odd_four.pdf')),commands=records,
                proof_status='The uniform written proof is the theorem; bounded finite controls are not a universal census.',
                whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
