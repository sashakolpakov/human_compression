#!/usr/bin/env python3
"""Render the complete proposed volume in fresh isolated TeX directories."""
import argparse,hashlib,json,pathlib,re,shutil,subprocess,time
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parent
DOCUMENTS=['umbrella','two-power-orders','three-generator-hypertopes','square-sections-and-free-extensions','common-two-group-quotient','high-type-two-groups','order-1024-markings','graph_symmetries','mixed-prime-polyhedra','two-group-computation','affine-programs','diagram-programs']
def run(out,xelatex):
 if out.exists():raise ValueError('fresh output required')
 out.mkdir(parents=True);start=time.monotonic();rows=[]
 for doc in DOCUMENTS:
  work=out/doc;work.mkdir()
  for p in ROOT.rglob('*'):
   if p.is_file() and p.suffix in ['.tex','.g','.py'] and 'prior' not in p.relative_to(ROOT).parts and '__pycache__' not in p.relative_to(ROOT).parts:
    q=work/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
  for n in [1,2]:
   p=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','-file-line-error',doc+'.tex'],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   (work/f'pass{n}.stdout').write_text(p.stdout)
   if p.returncode:raise RuntimeError(doc+' pass '+str(n)+' failed: '+p.stdout[-1800:])
  log=(work/(doc+'.log')).read_text(errors='replace');diagnostics=[x for x in log.splitlines()if any(y in x for y in ['Missing character:','Overfull','LaTeX Warning: Reference','LaTeX Warning: Citation','undefined references'])]
  reader=PdfReader(work/(doc+'.pdf'));texts=[page.extract_text()or''for page in reader.pages];bad=[]
  for i,t in enumerate(texts,1):
   for ch in t:
    if (ord(ch)<32 and ch not in '\n\t\r') or ch=='\ufffd' or 0xe000<=ord(ch)<=0xf8ff:bad.append([i,hex(ord(ch))])
  b=(work/(doc+'.pdf')).read_bytes();row={'document':doc,'pages':len(reader.pages),'pdf_sha256':hashlib.sha256(b).hexdigest(),'text_sha256':hashlib.sha256('\n'.join(texts).encode()).hexdigest(),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest()for t in texts],'diagnostics':diagnostics,'bad_glyphs':bad};rows.append(row)
  if diagnostics or bad:raise RuntimeError(doc+' diagnostics '+str(row))
  print(doc,len(reader.pages),'PASS',flush=True)
 report={'status':'PASS','documents':rows,'elapsed_seconds':time.monotonic()-start,'mathematical_replay':'Not performed: unchanged complete programs retain distinct prior acceptances; this command checks new TeX assembly only.'}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--xelatex',default='xelatex');v=p.parse_args();run(v.out,v.xelatex)
