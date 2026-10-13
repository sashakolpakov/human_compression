import sys
if sys.flags.optimize: raise RuntimeError("No optimization")
from pathlib import Path
import json,hashlib,subprocess,shutil
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');A=S/'topic_B_L044_singleton_completion_v1';W=S/'reboot_20261013/L044_singleton_completion_distinct';N=W/'native01';N.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected='80545f28ef33d27313870c221f79d09c27a2b29bbe61013f809e3e69ad278cee';assert sha(A/'manifest.json')==expected
m=json.loads((A/'manifest.json').read_text());d=json.loads((A/'dependencies.json').read_text());acquired=0
for base,ls in [(A,m['exports']),(S,d['bindings'])]:
 for row in ls:
  p=base/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],str(p)
  if base==S and p.name=='manifest.json':
   for x in json.loads(p.read_text()).get('exports',[]):
    q=p.parent/x['path'];assert q.stat().st_size==x['bytes']and sha(q)==x['sha256'];acquired+=1
shutil.copyfile(A/'singleton_completion.tex',N/'singleton_completion.tex')
for k in range(2):
 with (N/f'pass{k+1}.log').open('wb') as f:subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','singleton_completion.tex'],cwd=N,stdout=f,stderr=subprocess.STDOUT,check=True)
log=(N/'singleton_completion.log').read_text();assert all(x not in log for x in ['Overfull','LaTeX Warning','undefined references'])
a=PdfReader(A/'singleton_completion.pdf');b=PdfReader(N/'singleton_completion.pdf');assert len(a.pages)==len(b.pages)==2
texts=[]
for x,y in zip(a.pages,b.pages):
 assert x.extract_text()==y.extract_text();texts.append(hashlib.sha256(y.extract_text().encode()).hexdigest())
subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100',f'-sOutputFile={N}/page-%d.png',str(N/'singleton_completion.pdf')],check=True)
r={'status':'PASS','author_exports':len(m['exports']),'direct_bindings':len(d['bindings']),'acquired_exports':acquired,'native_pages':2,'page_text_sha256':texts,'all_native_warnings_absent':True,'mathematical_review_replaced_by_checks':False};(W/'replay_report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
