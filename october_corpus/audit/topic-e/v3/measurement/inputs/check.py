#!/usr/bin/env python3
"""Portable E input audit. Never runs mathematical programs or Lean."""
import argparse,json,subprocess,sys,time
from pathlib import Path
import pypdf
from extract_inputs import HERE,load,bound,need,sha,replay
from controls import controls
from build_reader import outputs

def pagehashes(p):return [sha((x.extract_text()or'').encode())for x in pypdf.PdfReader(p).pages]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output path');a.out.mkdir(parents=True);start=time.monotonic()
 exports=[]
 if (HERE/'manifest.json').exists():
  exports=load('manifest.json')['exports']
  for r in exports:bound(r,HERE)
 result,cache=replay(a.study_root)
 need(result==load('author_counts.json'),'all390PDF+250raw cells and full text hashes')
 expected=outputs(result,load('policy.json'))
 for name,text in expected.items():need((HERE/name).read_text()==text,'exact reader/CSV regeneration '+name)
 controls_report=controls(cache);(a.out/'controls.json').write_text(json.dumps(controls_report,indent=2)+'\n')
 info=dict(status='PASS',exports_checked=len(exports),science_executed=False,ratio=None,pdf_documents=13,physical_pages=128,pdf_metric_cells=390,raw_metric_cells=250,negative_controls=controls_report['negative_controls'],metric_fixture=True,actual_source_dictionaries=92,actual_source_glyph_classes=2086,calibration_occurrences=279,reader_and_CSV_exact=True,reader_render=None)
 if a.render:
  build=a.out/'render';build.mkdir();(build/'reader.tex').write_text(expected['reader.tex'])
  for i in [1,2]:
   c=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=build,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   (a.out/f'reader_pass{i}.log').write_text(c.stdout);need(c.returncode==0,'reader TeX pass '+str(i))
  log=(build/'reader.log').read_text(errors='replace');diagnostics=[l for l in log.splitlines()if any(s in l for s in ['Overfull','Underfull','Missing character','LaTeX Warning','Package hyperref Warning','undefined'])]
  need(not diagnostics,'reader glyph/layout/reference diagnostics '+str(diagnostics))
  hashes=pagehashes(build/'reader.pdf');need(len(hashes)==3,'complete three-page reader')
  if (HERE/'reader.pdf').exists():need(hashes==pagehashes(HERE/'reader.pdf'),'exact rebuilt reader page text')
  info['reader_render']=dict(pages=3,page_text_sha256=hashes,diagnostics=diagnostics)
 (a.out/'counts.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');info['elapsed_seconds']=round(time.monotonic()-start,3);(a.out/'report.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info))
if __name__=='__main__':main()
