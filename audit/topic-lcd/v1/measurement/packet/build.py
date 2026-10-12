#!/usr/bin/env python3
"""Portable fresh numerical replay. No sources, scientific tools or study tree needed."""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
from pypdf import PdfReader
from calculate import ROOT,calculate,need,read,sha
from presentation import write,dump
from check import check
from figure_checks import check as figures

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();out=a.out.resolve()
 need(not out.exists(),'fresh nonexistent output directory required');need(out!=ROOT and ROOT not in out.parents,'isolated output outside packet');out.mkdir(parents=True)
 if(ROOT/'manifest.json').exists():
  for x in read(ROOT/'manifest.json')['exports']:
   p=ROOT/x['path'];need(p.stat().st_size==x['bytes']and sha(p)==x['sha256'],'immutable export '+x['path'])
 r=calculate(ROOT);shutil.copytree(ROOT/'inputs',out/'inputs');shutil.copytree(ROOT/'protocol_freeze',out/'protocol_freeze')
 for name in ['protocol.json','reader_template.tex']:shutil.copy2(ROOT/name,out/name)
 write(out,r);report={'status':'PASS_AUTHOR_LCD_NUMERICAL_REPLAY','input_manifests':r['input_manifests'],'arithmetic':check(out,r),'vectors':figures(out,r),'reextracted_inputs':False,'scientific_programs_executed':False,'independent_numerical_review':False}
 if a.render:
  for k in [1,2]:
   run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,capture_output=True,text=True);(out/f'xelatex{k}.stdout').write_text(run.stdout+run.stderr);need(run.returncode==0,'reader TeX build; see '+str(out/f'xelatex{k}.stdout'))
  log=(out/'reader.log').read_text();diagnostics=[x for x in log.splitlines()if any(k in x for k in ['Warning','Overfull','Underfull','Missing character'])];need(not diagnostics,'clean TeX diagnostics '+repr(diagnostics))
  texts=[p.extract_text()for p in PdfReader(out/'reader.pdf').pages];need(len(texts)==3,'exact3 reader pages')
  report['render']={'pages':len(texts),'diagnostics':diagnostics,'page_text_sha256':[hashlib.sha256(x.encode()).hexdigest()for x in texts]}
  if(ROOT/'reader.pdf').exists():need(texts==[p.extract_text()for p in PdfReader(ROOT/'reader.pdf').pages],'frozen reader page-text equality')
 if(ROOT/'results.json').exists():need(read(ROOT/'results.json')==r,'frozen results regenerated exactly')
 for name in ['costs.csv','fractions.csv','raw_files.csv','raw_occurrences.csv','acquisition.csv','reader.tex','plot_data.json','document_graph.json','acquisition.json']:
  if(ROOT/name).exists():need((ROOT/name).read_bytes()==(out/name).read_bytes(),'exact generated '+name)
 dump(out/'report.json',report);print(json.dumps({'status':'PASS','fractions':90,'controls':len(report['arithmetic']['semantic_controls'])+len(report['vectors']['figure_controls']),'bars_per_format':report['vectors']['actual_PDF_bars'],'render':a.render}))
if __name__=='__main__':main()
