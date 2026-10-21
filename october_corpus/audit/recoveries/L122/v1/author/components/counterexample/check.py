"""Operational packet binding, exact finite replay, controls and native rendering."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,shutil
HERE=Path(__file__).resolve().parent

def need(t,s):
    if not t:raise ValueError(s)

def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true')
    p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');args=p.parse_args()
    need(not args.out.exists(),'fresh output directory');args.out.mkdir(parents=True)
    man=json.loads((HERE/'manifest.json').read_text())
    for r in man['exports']:
        f=HERE/r['path'];need(f.stat().st_size==r['bytes'] and pin(f)==r['sha256'],'export '+r['path'])
    bound=0
    if args.study_root:
        for r in json.loads((HERE/'dependencies.json').read_text())['bindings']:
            f=args.study_root/r['path'];need(f.stat().st_size==r['bytes'] and pin(f)==r['sha256'],'input '+r['path']);bound+=1
    run=subprocess.run([sys.executable,'-B','-O',str(HERE/'certificate.py'),'--out',str(args.out/'certificate')],check=True,capture_output=True,text=True)
    actual=json.loads(run.stdout);need(actual==json.loads((HERE/'certificate_report.json').read_text()),'exact finite report')
    run=subprocess.run([sys.executable,'-B','-O',str(HERE/'controls.py')],check=True,capture_output=True,text=True)
    controls=json.loads(run.stdout);need(controls==json.loads((HERE/'controls_report.json').read_text()),'exact control report')
    pages=0
    if args.render:
        from pypdf import PdfReader
        b=args.out/'render';b.mkdir();shutil.copy2(HERE/'no_triality.tex',b/'no_triality.tex')
        for i in range(2):
            run=subprocess.run([args.pdflatex,'-halt-on-error','-interaction=nonstopmode','no_triality.tex'],cwd=b,capture_output=True,text=True)
            (b/f'run{i}.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'native render')
        log=(b/'no_triality.log').read_text()
        for s in ['Overfull','Undefined control sequence','LaTeX Warning:']:need(s not in log,'TeX diagnostic '+s)
        a=PdfReader(b/'no_triality.pdf');r=PdfReader(HERE/'no_triality.pdf')
        need(len(a.pages)==len(r.pages)==3,'three native pages')
        for i,(x,y) in enumerate(zip(a.pages,r.pages)):need(x.extract_text()==y.extract_text(),'exact page text '+str(i+1))
        pages=len(a.pages)
    report=dict(status='PASS_AUTHOR_PACKET_REPLAY',exports=len(man['exports']),external_bindings=bound,
                finite_objects=actual['objects'],full_correlation_order=actual['full_correlation_order'],
                sylow_elements=actual['sylow_order'],order3_type_cycles=0,controls=controls['count'],
                rendered_pages=pages,graph_automorphism_backend_used=False,distinct_review=False)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
