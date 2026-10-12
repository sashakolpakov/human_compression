#!/usr/bin/env python3
"""Replay the bounded square-family certificate and optional manuscript build."""
import argparse,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
from certificate import run,require

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--gap',default='/opt/homebrew/bin/gap');a.add_argument('--study-root',type=Path);args=a.parse_args()
    require(not args.out.exists(),'fresh output directory');args.out.mkdir(parents=True)
    here=Path(__file__).resolve().parent;started=time.monotonic()
    def bound(base,row):
        raw=(base/row['path']).read_bytes()
        require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'bound input '+row['path'])
    if (here/'manifest.json').exists():
        for row in json.loads((here/'manifest.json').read_text())['exports']:bound(here,row)
    if args.study_root:
        for row in json.loads((here/'scope.json').read_text())['retained_bindings']:bound(args.study_root,row)
    result,perms=run()
    (args.out/'affine_result.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'root_actions.g').write_text('rho:='+str(perms['rho'])+';;\ntau:='+str(perms['tau'])+';;\n')
    shutil.copy2(here/'kernel_certificate.g',args.out/'kernel_certificate.g')
    p=subprocess.run([args.gap,'-q','-b','kernel_certificate.g'],cwd=args.out,text=True,capture_output=True,timeout=180)
    (args.out/'kernel_transcript.txt').write_text(p.stdout+p.stderr)
    require(p.returncode==0 and not p.stderr and 'PASS_ALL_THREE_ACTUAL_KERNELS_AND_TWO_FINITE_TORI' in p.stdout,'exact kernel and torus calculations')
    render=None
    if args.render:
        from pypdf import PdfReader
        shutil.copy2(here/'proof.tex',args.out/'proof.tex')
        for _ in range(2):
            p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','proof.tex'],cwd=args.out,text=True,capture_output=True,timeout=60)
            require(p.returncode==0,'TeX build')
        log=(args.out/'proof.log').read_text();diagnostics=[s for s in log.splitlines() if any(x in s for x in ['Overfull','undefined','Warning'])]
        require(not diagnostics,'clean TeX diagnostics')
        fresh=[p.extract_text() for p in PdfReader(args.out/'proof.pdf').pages]
        pages=len(fresh);require(pages==4,'whole four-page proof')
        if (here/'proof.pdf').exists():require(fresh==[p.extract_text() for p in PdfReader(here/'proof.pdf').pages],'exact complete page text')
        render=dict(pages=pages,diagnostics=diagnostics)
    report=dict(status='PASS_BOUNDED_L121_SQUARE_CERTIFICATE',runtime_seconds=time.monotonic()-started,IP_equalities=256,linear_order=1152,kernel_ranks=[4,4,2],finite_torus_orders=[36,48],render=render,full_Lean=False,whole_L121_recovery=False,new_question_credit=0)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
