#!/usr/bin/env python3
"""Two complete detached papers, isolated rendering and literal migration audit."""
import argparse,hashlib,json,shutil,subprocess,time
from pathlib import Path
from pypdf import PdfReader
from migrate import make,require
H=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',default='xelatex');a=p.parse_args();require(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 start=time.monotonic();sources,migration=make(a.study_root/'corpus161_L073_recovery/primitive-mathieu-geometries.tex');result={}
 for name,text in sources.items():
  require((H/name).read_text()==text,'literal migrated source '+name);folder=a.out/Path(name).stem;folder.mkdir();(folder/'paper.tex').write_text(text)
  for n in (1,2):
   run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','-recorder','paper.tex'],cwd=folder,capture_output=True,timeout=90);(folder/f'pass{n}.stdout').write_bytes(run.stdout);(folder/f'pass{n}.stderr').write_bytes(run.stderr);require(run.returncode==0,'isolated XeLaTeX success')
  log=(folder/'paper.log').read_text(errors='replace');issues=[line for line in log.splitlines()if any(mark in line for mark in ('Missing character:','Overfull','undefined','LaTeX Warning:'))];require(not issues,'clean final render '+str(issues));pdf=folder/'paper.pdf';pages=[x.extract_text()or''for x in PdfReader(pdf).pages]
  require(not any('\ufffd'in x or any(0xE000<=ord(c)<=0xF8FF or(ord(c)<32 and c not in '\n\r\t')for c in x)for x in pages),'clean extracted glyphs')
  expected=H/Path(name).with_suffix('.pdf')
  if expected.exists():require(pages==[x.extract_text()or''for x in PdfReader(expected).pages],'full per-page text equality')
  result[name]=dict(source_sha256=sha(text.encode()),pages=len(pages),page_text_sha256=[sha(x.encode())for x in pages],pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf.read_bytes()),diagnostics=issues)
 report=dict(status='PASS',migration=migration,documents=result,elapsed_seconds=round(time.monotonic()-start,3),mathematical_programs_executed=False,formal_claim=False,no_factors=True)
 (a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(status='PASS',documents={k:v['pages']for k,v in result.items()},elapsed_seconds=report['elapsed_seconds'])))
if __name__=='__main__':main()
