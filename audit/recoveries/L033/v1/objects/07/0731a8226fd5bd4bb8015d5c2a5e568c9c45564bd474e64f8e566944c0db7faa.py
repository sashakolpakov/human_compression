"""Exact affine marking, source bindings and native proof build."""
import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,subprocess
from pathlib import Path
from affine import run,need
P=Path(__file__).resolve().parent
def pin(p):
    p=Path(p).resolve();data=p.read_bytes()
    return dict(path=str(p),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
def read(p):return json.loads(Path(p).read_text())
def frozen():
    if not(P/'manifest.json').exists():return None
    m=read(P/'manifest.json')
    for row in m['exports']:
        got=pin(P/row['path']);need(all(got[k]==row[k]for k in ['bytes','sha256']),'stable export')
    return m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    out=a.out.resolve();need(not out.exists(),'fresh output');before=frozen();deps=read(P/'dependencies.json')
    for row in deps:need(pin(row['path'])==row,'bound dependency '+row['path'])
    out.mkdir();result=run();pages=None
    def call(name,cmd):
        r=subprocess.run(cmd,capture_output=True,timeout=30)
        (out/(name+'.stdout')).write_bytes(r.stdout);(out/(name+'.stderr')).write_bytes(r.stderr)
        need(r.returncode==0 and not r.stderr,'clean '+name)
    if a.render:
        native=out/'native';native.mkdir()
        for i in [1,2]:call('tex'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(native),str(P/'cubes.tex')])
        log=(native/'cubes.log').read_text();need(not any(w in log for w in ['Warning','Overfull','Underfull']),'clean proof layout')
        from pypdf import PdfReader
        pdf=PdfReader(native/'cubes.pdf');pages=len(pdf.pages)
        if(P/'cubes.pdf').exists():need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in PdfReader(P/'cubes.pdf').pages],'same proof text')
        call('raster',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'cubes.pdf')])
    for row in deps:need(pin(row['path'])==row,'stable dependency')
    need(frozen()==before,'stable component')
    result.update(native_pages=pages,dependencies=len(deps),whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
