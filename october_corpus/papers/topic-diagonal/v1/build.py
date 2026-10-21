#!/usr/bin/env python3
"""Build the declared TeX closure in a fresh directory; no Markdown input."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
import pypdf
ROOT=Path(__file__).resolve().parent
PAPERS={'umbrella':['preamble.tex'],'diagonal-twistings':['preamble.tex'],'programs':['preamble.tex','programs/diagonal_models.g']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise RuntimeError('DIAGONAL_BUILD_REJECT '+msg)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True);out=a.out.resolve();report={}
 for name,inputs in PAPERS.items():
  d=out/name;d.mkdir();bindings=[]
  for f in [name+'.tex']+inputs:
   src=ROOT/f;target=d/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target);bindings.append({'path':f,'sha256':sha(src),'bytes':src.stat().st_size})
  for i in range(3):
   r=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder',name+'.tex'],cwd=d,text=True,capture_output=True,timeout=120)
   (d/f'pass{i+1}.stdout').write_text(r.stdout);(d/f'pass{i+1}.stderr').write_text(r.stderr);need(r.returncode==0,'render '+name)
  log=(d/(name+'.log')).read_text();bad=[line for line in log.splitlines() if re.search(r'Overfull|Missing character|Missing glyph|LaTeX Warning|Package .* Warning',line)]
  need(not bad,'render diagnostics '+repr(bad))
  doc=pypdf.PdfReader(d/(name+'.pdf'));pages=[q.extract_text() or '' for q in doc.pages];text='\n'.join(pages)
  need(not any((ord(c)<32 and c not in '\n\t\r') or c=='\ufffd' or 0xe000<=ord(c)<=0xf8ff for c in text),'PDF glyph scan')
  same=None
  if (ROOT/(name+'.pdf')).exists():same=pages==[q.extract_text() or '' for q in pypdf.PdfReader(ROOT/(name+'.pdf')).pages];need(same,'complete PDF page text reproduced')
  (d/'extracted.txt').write_text(text)
  for b in bindings:need(sha(ROOT/b['path'])==b['sha256'],'unchanged source')
  report[name]={'pages':len(pages),'pdf_sha256':sha(d/(name+'.pdf')),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'input_bindings':bindings,'diagnostics':bad,'old_page_text_equal':same}
 (out/'report.json').write_text(json.dumps({'status':'PASS','papers':report,'program_full_byte_inclusion':{'path':'programs/diagonal_models.g','sha256':sha(ROOT/'programs/diagonal_models.g'),'method':'literal complete VerbatimInput; entire raw file copied into isolated TeX closure'}},indent=2)+'\n');print(json.dumps({k:v['pages'] for k,v in report.items()}))
if __name__=='__main__':main()
