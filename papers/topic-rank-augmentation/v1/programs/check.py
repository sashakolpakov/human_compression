#!/usr/bin/env python3
"""Rebuild the complete code appendix; no mathematical computation repeated."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
def need(b,m):
    if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    b=json.loads((HERE/'bindings.json').read_text())
    for r in b['files']:
        f=HERE/r['path'];need(sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],'whole bound file')
        if a.study_root:need(f.read_bytes()==(a.study_root/r['source_path']).read_bytes(),'source program unchanged')
        shutil.copyfile(f,a.out/r['path'])
    if (HERE/'manifest.json').exists():
        for r in json.loads((HERE/'manifest.json').read_text())['exports']:
            f=HERE/r['path'];need(sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],'frozen export')
    shutil.copyfile(HERE/'programs.tex',a.out/'programs.tex')
    for i in range(2):
        r=subprocess.run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','programs.tex'],cwd=a.out,capture_output=True);(a.out/f'render{i}.log').write_bytes(r.stdout+r.stderr);need(r.returncode==0,'appendix rebuild')
    log=(a.out/'programs.log').read_text();diagnostics=[s for s in log.splitlines() if any(x in s for x in ['Overfull','Underfull','Missing character','LaTeX Warning','Font Warning'])];need(not diagnostics,'render diagnostics')
    pages=[p.extract_text() for p in PdfReader(a.out/'programs.pdf').pages];old=[p.extract_text() for p in PdfReader(HERE/'programs.pdf').pages];need(pages==old and len(pages)==3,'same complete page text')
    texts=[]
    for i,t in enumerate(pages):
        lines=t.splitlines();need(lines[-1].strip()==str(i+1),'numeric footer');texts.append('\n'.join(lines[:-1]))
    whole=''.join(''.join(texts).split())
    for r in b['files']:need(''.join((HERE/r['path']).read_text().split()) in whole,'entire printed file '+r['path'])
    result=dict(status='PASS_COMPLETE_PROGRAM_APPENDIX',pages=3,whole_files=3,per_page_text_equal=True,source_programs_compared=bool(a.study_root),diagnostics=diagnostics,mathematics_replayed=False,new_source_credit=0,new_question_credit=0)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
