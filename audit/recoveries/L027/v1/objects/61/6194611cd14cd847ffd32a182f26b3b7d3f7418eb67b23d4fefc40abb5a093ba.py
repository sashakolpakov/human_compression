"""Replay the bounded uniform rank-five component and its controls."""
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
def digest(p):
    data=p.read_bytes();return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
def verify(p,row):need(digest(p)=={k:row[k] for k in ('bytes','sha256')},'changed input '+str(p))
def parse_finite(stdout):
    text=stdout.decode();pat=r'FIELD\s+(\d+)\s+SIGN\s+(-?1)\s+ROOT\s+([12])\s+GROUP\s+(\d+)\s+A\s+(\d+)\s+B\s+(\d+)\s+H\s+(\d+)\s+E\s+(\d+)\s+C\s+(\d+)\s+ALL_IP\s+(\d+)\s+PASS'
    rows=[[int(x) for x in m.groups()] for m in re.finditer(pat,text)]
    remainder=re.sub(pat,'',text).strip()
    need(remainder=='PASS_ALL_SIXTEEN_RANK_FIVE_CONTROLS','complete terminal finite record')
    need(len(rows)==16 and len({tuple(r[:3]) for r in rows})==16,'sixteen distinct finite controls')
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args();out=arg.out.resolve()
    need(not out.exists(),'fresh output');need(P not in out.parents and out!=P,'external output')
    manifest=json.loads((P/'manifest.json').read_text())
    for row in manifest['exports']:verify(P/row['path'],row)
    deps=json.loads((P/'dependencies.json').read_text())
    for row in deps:verify(Path(row['path']),row)
    out.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);records=[]
    def run(label,command,cap,cwd=None,success=True):
        start=time.monotonic();r=subprocess.run(command,cwd=cwd,env=env,capture_output=True,timeout=cap)
        (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
        row=dict(label=label,command=command,returncode=r.returncode,seconds=time.monotonic()-start);records.append(row)
        if success:need(r.returncode==0,'execution '+label)
        return r
    run('literal',[sys.executable,str(P/'literal.py'),'--out',str(out/'literal.json')],30)
    literal=json.loads((out/'literal.json').read_text());need(literal==json.loads((P/'literal_expected.json').read_text()),'exact literal result')
    r=run('finite',['/opt/homebrew/bin/gap','-q','-b',str(P/'finite.g')],180)
    need(not r.stderr,'clean GAP stderr');rows=parse_finite(r.stdout)
    need(rows==json.loads((P/'finite_expected.json').read_text()),'exact finite result')
    damages=[]
    for damage in ['unipotent','conic','duality']:
        target=out/('damaged_'+damage+'.json')
        r=run('damage_'+damage,[sys.executable,str(P/'literal.py'),'--out',str(target),'--damage',damage],30,success=False)
        need(r.returncode!=0 and b'ValueError' in r.stderr and not target.exists(),'damaged identity rejected')
        damages.append(damage)
    guards=[]
    for script in ['literal.py','check.py']:
        for mode in ['argument','environment']:
            ee=dict(env);cmd=[sys.executable];target=out/(script+'_'+mode)
            if mode=='argument':cmd.append('-O')
            else:ee['PYTHONOPTIMIZE']='1'
            r=subprocess.run([*cmd,str(P/script),'--out',str(target)],env=ee,capture_output=True,timeout=10)
            need(r.returncode!=0 and b'normal Python required' in r.stderr and not target.exists(),'optimization rejected')
            guards.append([script,mode])
    native=out/'native';native.mkdir();shutil.copy2(P/'rank_five.tex',native/'rank_five.tex')
    for i in [1,2]:run('latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode','rank_five.tex'],30,native)
    log=(native/'rank_five.log').read_text();need(all(x not in log for x in ['Warning','Overfull','Underfull']),'clean native build')
    texts=lambda p:[x.extract_text() for x in PdfReader(p).pages]
    need(texts(native/'rank_five.pdf')==texts(P/'rank_five.pdf'),'native text identity')
    run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','rank_five.pdf'],30,native)
    report=dict(status='PASS_L027_RANK_FIVE_COMPONENT',exports=len(manifest['exports']),dependencies=len(deps),
                exact_identities=literal['count'],finite_models=len(rows),full_subset_intersections=sum(r[-1] for r in rows),
                damaged_controls=damages,optimization_guards=guards,native_pages=len(texts(native/'rank_five.pdf')),
                commands=records,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
