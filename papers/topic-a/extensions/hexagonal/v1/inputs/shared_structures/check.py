#!/usr/bin/env python3
"""Binding, full small structural replay, and optional four-page render."""
from pathlib import Path
import argparse,json,hashlib,subprocess,sys,shutil
HERE=Path(__file__).resolve().parent

def bind(p,r):
 if not p.is_file() or p.stat().st_size!=r['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('binding '+str(p))
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 if (HERE/'manifest.json').exists():
  for r in json.loads((HERE/'manifest.json').read_text())['exports']:bind(HERE/r['path'],r)
 if a.study_root:
  for r in json.loads((HERE/'bindings.json').read_text())['study_inputs']:bind(a.study_root/r['path'],r)
 subprocess.run([sys.executable,'-B','-O',str(HERE/'run.py'),'--out',str(a.out/'structural'),'--controls','--gap',a.gap],check=True)
 rep=json.loads((a.out/'structural/report.json').read_text());rep['fresh_render']=None
 if a.render:
  d=a.out/'render';d.mkdir();shutil.copy2(HERE/'shared_structures.tex',d/'shared_structures.tex')
  for i in range(2):
   r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','shared_structures.tex'],cwd=d,capture_output=True,text=True,timeout=60)
   (d/f'pass{i+1}.log').write_text(r.stdout+r.stderr)
   if r.returncode:raise ValueError('render failure')
  if any(w in r.stdout for w in ['Overfull','Warning:','undefined']):raise ValueError('final render diagnostics')
  from pypdf import PdfReader
  old=PdfReader(HERE/'shared_structures.pdf').pages;new=PdfReader(d/'shared_structures.pdf').pages
  if len(old)!=4 or len(new)!=4 or [q.extract_text() for q in old]!=[q.extract_text() for q in new]:raise ValueError('four exact page texts')
  rep['fresh_render']={'pages':4,'all_page_texts_exact':True,'diagnostics':[]}
 (a.out/'report.json').write_text(json.dumps(rep,indent=2)+'\n');print(json.dumps(rep,indent=2))
if __name__=='__main__':main()
