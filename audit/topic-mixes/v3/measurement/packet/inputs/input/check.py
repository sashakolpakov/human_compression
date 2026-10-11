#!/usr/bin/env python3
"""Portable input replay, boundary controls and optional isolated PDF builds."""
from pathlib import Path
import argparse,json,re,shutil,subprocess,time
from pypdf import PdfReader
from extract_inputs import replay,load,H,need,sha,bound
from controls import run

def render(args):
 rows=[('U2','topic_Mix_F007_recovery_v2/relations_and_flags.tex'),('A4','topic_Mix_F007_recovery_v2/faithfulness_application.tex'),('A5','topic_Mix_F007_recovery_v2/companion/rank_three.tex'),('reader',None)];records=[]
 for key,path in rows:
  stage=args.out/('render_'+key);stage.mkdir()
  tex=H/'input_reader.tex' if path is None else args.sources_root/path
  shutil.copyfile(tex,stage/'paper.tex')
  for i in [1,2]:
   q=subprocess.run([args.xelatex,'-interaction=nonstopmode','-halt-on-error','-recorder','paper.tex'],cwd=stage,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   (stage/f'pass{i}.log').write_bytes(q.stdout);need(q.returncode==0,'isolated XeLaTeX '+key)
  log=(stage/'paper.log').read_text(errors='replace');bad=[s for s in log.splitlines()if any(x in s for x in ['Missing character:','Overfull','Undefined control','undefined references','LaTeX Warning:'])];need(not bad,'clean rendering '+key)
  new=[p.extract_text()or''for p in PdfReader(stage/'paper.pdf').pages]
  oldfile=H/'input_reader.pdf' if path is None else args.sources_root/load('policy.json')['new_documents'][key]['path']
  old=[p.extract_text()or''for p in PdfReader(oldfile).pages];need(new==old,'exact complete page text '+key)
  for t in new:need(not any(0xE000<=ord(c)<=0xF8FF or(ord(c)<32 and c not in '\n\t\r')for c in t),'no control/private-use extraction glyph '+key)
  records.append(dict(document=key,pages=len(new),page_text_equal=True,text_sha256=sha('\n'.join(new).encode()),diagnostics=[]))
 return records

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');args=ap.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True);t=time.monotonic()
 counts,audit,cache=replay(args);need(counts==load('author_counts.json'),'all new and retained author cells reproduce exactly')
 ctr=run(counts,cache);records=render(args)if args.render else []
 for n,o in [('counts.json',counts),('controls.json',ctr),('font_audit.json',audit)]:(args.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 report=dict(status='PASS_COMPLETE_THREE_SOURCE_INPUT_REPLAY',new_PDF_cells=120,new_raw_cells=40,retained_PDF_cells=330,retained_raw_cells=130,all_retained_cells_unchanged=True,controls=ctr['rejected'],rendered=records,elapsed_seconds=round(time.monotonic()-t,3),science_reexecuted=False,ratios_evaluated=False)
 (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
