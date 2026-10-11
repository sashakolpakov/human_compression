#!/usr/bin/env python3
"""Portable full input replay and reader; no mathematical execution or ratios."""
import argparse,json,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
from extract_inputs import HERE,load,bound
from font_tools import need,sha

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for e in load('manifest.json')['exports']:bound(e,HERE)
 for e in load('protocol.json')['local_bindings']:bound(e,HERE)
 jobs=[['extract_inputs.py','--study-root',str(a.study_root),'--out',str(a.out/'recount')],['controls.py','--study-root',str(a.study_root),'--out',str(a.out/'controls')]]
 if a.render:jobs.append(['build_reader.py','--out',str(a.out/'reader'),'--xelatex',a.xelatex])
 for i,cmd in enumerate(jobs):
  q=subprocess.run([sys.executable,'-B','-O',str(HERE/cmd[0]),*cmd[1:]],capture_output=True);(a.out/f'job{i}.stdout').write_bytes(q.stdout);(a.out/f'job{i}.stderr').write_bytes(q.stderr);need(q.returncode==0,'bounded input step '+cmd[0])
 r=json.loads((a.out/'recount/counts.json').read_text());controls=json.loads((a.out/'controls/report.json').read_text());need(r==load('author_counts.json'),'all document/raw metrics exact');pages=None;match=None
 if a.render:
  t=[p.extract_text() for p in PdfReader(a.out/'reader/reader.pdf').pages];pages=len(t);match=t==[p.extract_text() for p in PdfReader(HERE/'reader.pdf').pages];need(pages==2 and match and (a.out/'reader/reader.tex').read_bytes()==(HERE/'reader.tex').read_bytes(),'two reader pages and exact TeX')
 result=dict(status='PASS_COMPLETE_L020_INPUT_PROPOSAL',pdf_metric_cells=150,raw_metric_cells=80,physical_pages=33,calibrated_occurrences=112,actual_source_glyph_classes=528,controls=controls['count'],reader_pages=pages,reader_page_texts_match=match,scientific_programs_executed=False,factors_computed=False)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
