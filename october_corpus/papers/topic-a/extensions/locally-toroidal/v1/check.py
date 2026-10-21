#!/usr/bin/env python3
"""Replay the assembled application's whole copied proof programs."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def need(test,message):
    if not test:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(base,row):
    p=base/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'bound file '+row['path'])
def run(argv,cwd,out,name):
    q=subprocess.run([str(x) for x in argv],cwd=cwd,text=True,capture_output=True,timeout=180)
    (out/(name+'.stdout')).write_text(q.stdout);(out/(name+'.stderr')).write_text(q.stderr)
    need(q.returncode==0 and not q.stderr.strip(),'successful '+name)
    return q

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path)
    ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--render',action='store_true');ap.add_argument('--formal',action='store_true')
    ap.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    ap.add_argument('--package-root',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    args=ap.parse_args();need(not args.out.exists(),'fresh output');out=args.out.resolve();out.mkdir(parents=True)
    if (HERE/'manifest.json').exists():
        for row in json.loads((HERE/'manifest.json').read_text())['exports']:bound(HERE,row)
    scope=json.loads((HERE/'scope.json').read_text())
    for row in scope['required_whole_files']:bound(HERE,row)
    if args.study_root:
        bound(args.study_root,scope['source'])
        for row in scope['retained_bindings']:bound(args.study_root,row)
    reports={}
    for sub in ['cubic','square','finite']:
        cmd=[sys.executable,'-B',HERE/sub/'check.py','--out',out/sub,'--gap',args.gap]
        if sub=='finite' and args.formal:cmd += ['--formal','--lean',args.lean,'--package-root',args.package_root]
        run(cmd,HERE/sub,out,sub);reports[sub]=json.loads((out/sub/'report.json').read_text())
    q=run([sys.executable,'-B',HERE/'cubic_relation/check.py'],HERE/'cubic_relation',out,'cubic_relation');reports['cubic_relation']=json.loads(q.stdout)
    if args.render:
        from pypdf import PdfReader
        work=out/'render';work.mkdir();shutil.copy2(HERE/'application.tex',work/'application.tex');shutil.copytree(HERE/'sections',work/'sections')
        for i in [1,2]:run(['/opt/homebrew/bin/pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','application.tex'],work,out,'tex'+str(i))
        diagnostics=[s for s in (work/'application.log').read_text().splitlines() if any(x in s for x in ['Warning:','Overfull','Missing character:','Missing glyph'])];need(not diagnostics,'clean rendered proof '+str(diagnostics))
        pages=[p.extract_text() for p in PdfReader(work/'application.pdf').pages]
        if (HERE/'application.pdf').exists():need(pages==[p.extract_text() for p in PdfReader(HERE/'application.pdf').pages],'all compiled page texts agree')
        reports['render']={'pages':len(pages),'diagnostics':diagnostics,'page_text_sha256':[hashlib.sha256(x.encode()).hexdigest() for x in pages]}
    reports.update(status='PASS_ASSEMBLED_L121_APPLICATION',whole_original_credit=0,new_open_question_credit=0,full_Lean=False,formal_rebuilt=args.formal)
    (out/'report.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps({'status':reports['status'],'pages':reports.get('render',{}).get('pages'),'formal_rebuilt':args.formal}))
if __name__=='__main__':main()
