"""Exact interval tests, exhaustive small oracle, and acquired positive lists."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, ast, hashlib, json, os, shutil, subprocess
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--render',action='store_true')
    a=ap.parse_args();P=Path(__file__).resolve().parent;S=a.study.resolve();O=a.out.resolve()
    need(not O.exists(),'fresh output required')
    deps=json.loads((P/'dependencies.json').read_text())
    for row in deps:
        data=(S/row['path']).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'exact dependency '+row['path'])
    exports=[]
    if (P/'manifest.json').exists():
        exports=json.loads((P/'manifest.json').read_text())['exports']
        for row in exports:
            data=(P/row['path']).read_bytes()
            need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'frozen export '+row['path'])
    roster=json.loads((P/'positive_sources.json').read_text());positive=[]
    for row in roster:
        text=(S/row['source']).read_text()
        need(text.rstrip().endswith(row['terminal']),'accepted complete validation marker')
        tuples=[ast.literal_eval(line.split('|',1)[1]) for line in text.splitlines() if line.startswith('SOLUTION|')]
        need(len(tuples)==row['tuples'],'complete acquired tuple count')
        n=row['degree']
        need(all(type(t) is list and all(type(g) is list and len(g)==n and all(type(x) is int for x in g) and sorted(g)==list(range(1,n+1)) for g in t) for t in tuples),'literal source arrays')
        positive.append([n,tuples])
    need(positive==json.loads((P/'positive_controls.json').read_text()),'literal acquired extraction')
    O.mkdir(parents=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    (O/'positive.g').write_text('positiveRows:='+json.dumps(positive)+';;\n')
    (O/'driver.g').write_text('intervalFile:='+json.dumps(str(P/'intervals.g'))+';;\npositiveFile:='+json.dumps(str(O/'positive.g'))+';;\nRead('+json.dumps(str(P/'controls.g'))+');\n')
    def run(name,cmd,cap,cwd=None):
        cp=subprocess.run(cmd,env=env,capture_output=True,timeout=cap,cwd=cwd)
        (O/(name+'.stdout')).write_bytes(cp.stdout);(O/(name+'.stderr')).write_bytes(cp.stderr)
        need(cp.returncode==0 and not cp.stderr,'complete clean '+name)
        return cp.stdout.decode()
    text=run('controls',['/opt/homebrew/bin/gap','-q','-T',str(O/'driver.g')],180)
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    need(len(lines)==9 and lines[-2:]==['EXPLICIT_NEGATIVES|5','COMPLETE_INTERVAL_CONTROLS'],'exact terminal control roster')
    small=[];large=[]
    for r,line in enumerate(lines[:4],1):
        parts=line.split('|');need(len(parts)==4 and parts[0]=='SMALL' and parts[1]==str(r) and parts[2]==str(9**r),'every S4 tuple tested')
        good=int(parts[3]);need(0<=good<=9**r,'small success count')
        small.append(dict(rank=r,tuples=9**r,accepted=good))
    for data,line in zip(positive,lines[4:7]):
        n,tuples=data;checks=sum((len(t)-1)*(len(t)-2)//2 for t in tuples)
        need(line==f'POSITIVE|{n}|{len(tuples)}|{checks}','all acquired positives and intervals')
        large.append(dict(degree=n,tuples=len(tuples),interval_intersections=checks))
    scientific=dict(small=small,positive=large,invalid_controls=5)
    if (P/'expected.json').exists():
        need(scientific==json.loads((P/'expected.json').read_text()),'exact complete controls')
    (O/'scientific.json').write_text(json.dumps(scientific,indent=2)+'\n')
    guards=0
    for mode in ('argument','environment'):
        e=env.copy();cmd=[sys.executable]
        if mode=='argument':cmd.append('-O')
        else:e['PYTHONOPTIMIZE']='1'
        target=O/('forbidden_'+mode)
        cp=subprocess.run(cmd+[str(P/'check.py'),'--out',str(target)],env=e,capture_output=True,timeout=10)
        (O/('optimization_'+mode+'.stderr')).write_bytes(cp.stderr)
        need(cp.returncode!=0 and b'unoptimized execution required' in cp.stderr and not target.exists(),'optimization rejection')
        guards+=1
    pages=None
    if a.render:
        N=O/'native';N.mkdir();shutil.copy2(P/'intervals.tex',N/'intervals.tex')
        for i in range(2):run('native'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','intervals.tex'],45,N)
        from pypdf import PdfReader
        pdf=PdfReader(N/'intervals.pdf');pages=len(pdf.pages)
        native='\n'.join(p.extract_text() or '' for p in pdf.pages);(N/'text.txt').write_text(native)
        log=(N/'intervals.log').read_text()
        need(not any(word in log for word in ('Overfull','Underfull','LaTeX Warning')),'clean native layout')
        if (P/'native_expected.txt').exists():need(native==(P/'native_expected.txt').read_text(),'exact native text')
        run('render',['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','intervals.pdf'],45,N)
    report=dict(status='PASS_INTERVAL_VALIDATOR',exports=len(exports),dependencies=len(deps),scientific=scientific,optimization_guards=guards,native_pages=pages,new_numeric_cells=0,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
