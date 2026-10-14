import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
from finite import need,run
P=Path(__file__).resolve().parent

def verify(p,row):
    b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--public',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False);public=a.public or a.study.parents[1]/'math_compression'
    m=json.loads((P/'manifest.json').read_text())
    for x in m['exports']:verify(P/x['path'],x)
    deps=json.loads((P/'dependencies.json').read_text())
    for x in deps:verify((public if x['namespace']=='public' else a.study)/x['path'],x)
    got=run();want=json.loads((P/'finite_report.json').read_text());need(got==want,'complete finite report')
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    guards=[]
    for script in ['finite.py','check.py']:
        p=subprocess.run([sys.executable,'-O',str(P/script)],env=env,capture_output=True,text=True,timeout=10)
        need(p.returncode!=0 and 'unoptimized execution required' in p.stderr,'optimization guard');guards.append(script)
    native=None
    if a.render:
        from pypdf import PdfReader
        b=a.out/'native';b.mkdir();shutil.copy2(P/'elementary.tex',b/'elementary.tex')
        for i in range(2):
            z=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','elementary.tex'],cwd=b,capture_output=True,text=True,env=env,timeout=60)
            (b/f'pass{i}.stdout').write_text(z.stdout);(b/f'pass{i}.stderr').write_text(z.stderr);need(z.returncode==0,'native build')
        need('undefined' not in z.stdout.lower() and 'Overfull' not in z.stdout,'native warnings')
        ref=PdfReader(P/'elementary.pdf');out=PdfReader(b/'elementary.pdf');need(len(ref.pages)==len(out.pages)==3,'native page count')
        need([x.extract_text() for x in ref.pages]==[x.extract_text() for x in out.pages],'native text')
        z=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','elementary.pdf'],cwd=b,capture_output=True,text=True,timeout=60);need(z.returncode==0,'native raster');native={'pages':3,'text_identical':True}
    report={'status':'PASS','exports':len(m['exports']),'bindings':len(deps),'S4_actions':2,'multiplication_checks':1152,'IP_checks':128,'path_controls':len(got['paths']),'optimization_guards':guards,'native':native,'whole_original_credit':0,'new_question_credit':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
