#!/usr/bin/env python3
"""Portable input and isolated reader/whole-appendix replay. No GAP/Lean execution."""
import argparse,json,subprocess,sys,shutil,time
from pathlib import Path
from pypdf import PdfReader
from extract_inputs import HERE,load,bound
from font_tools import need,sha

def appendix(root,out,xelatex):
 out.mkdir();p=load('policy.json');b=load('printing_bindings.json')
 for r in b['inputs']:
  path,data=bound(r,root);dest=out/r['staged_path'];dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(data)
 need(sorted(str(f.relative_to(out)) for f in out.rglob('*') if f.is_file())==sorted(r['staged_path'] for r in b['inputs']),'only declared TeX/program inputs staged')
 for i in range(2):
  q=subprocess.run([xelatex,'-halt-on-error','-interaction=nonstopmode','program-appendix.tex'],cwd=out,capture_output=True);(out/f'pass{i}.stdout').write_bytes(q.stdout);(out/f'pass{i}.stderr').write_bytes(q.stderr);need(q.returncode==0,'complete appendix rendered')
 diag=[s for s in (out/'program-appendix.log').read_text().splitlines() if any(k in s for k in ['Missing character','Overfull','Underfull','LaTeX Warning','Font Warning'])];need(not diag,'appendix diagnostics')
 original,_=bound(p['documents']['CODE'],root);a=[pg.extract_text() for pg in PdfReader(original).pages];c=[pg.extract_text() for pg in PdfReader(out/'program-appendix.pdf').pages];need(a==c and len(c)==9,'all nine printed pages exact')
 return dict(pages=9,page_texts_match=True,declared_inputs=len(b['inputs']),diagnostics=diag)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True);start=time.monotonic()
 if (HERE/'manifest.json').exists():
  for e in load('manifest.json')['exports']:bound(e,HERE)
 for e in load('protocol.json')['local_bindings']:bound(e,HERE)
 jobs=[['extract_inputs.py','--study-root',str(a.study_root),'--out',str(a.out/'recount')],['controls.py','--study-root',str(a.study_root),'--out',str(a.out/'controls')]]
 if a.render:jobs.append(['build_reader.py','--out',str(a.out/'reader'),'--xelatex',a.xelatex])
 for i,cmd in enumerate(jobs):
  q=subprocess.run([sys.executable,'-B','-O',str(HERE/cmd[0]),*cmd[1:]],capture_output=True);(a.out/f'job{i}.stdout').write_bytes(q.stdout);(a.out/f'job{i}.stderr').write_bytes(q.stderr);need(q.returncode==0,'bounded input step '+cmd[0])
 r=json.loads((a.out/'recount/counts.json').read_text());c=json.loads((a.out/'controls/report.json').read_text());need(r==load('author_counts.json'),'all document/raw metrics exact')
 old=load('prior_source_comparison.json');_,data=bound(old['prior'],a.study_root);old_counts=json.loads(data)['documents']['L014']['variants']
 for v,ns in old_counts.items():
  for n,ms in ns.items():
   for k,x in ms.items():need(r['documents']['L014']['metrics'][v][n][k]==x,'unchanged old source coordinate')
 for b in load('visual_review.json')['reused_complete_receipts']:bound(b,a.study_root)
 for b in load('helper_provenance.json')['unchanged_helpers']:need(bound(b,a.study_root)[1]==(HERE/Path(b['path']).name).read_bytes(),'unchanged accepted helper')
 pages=None;match=None;ar=None
 if a.render:
  t=[p.extract_text() for p in PdfReader(a.out/'reader/reader.pdf').pages];pages=len(t);match=t==[p.extract_text() for p in PdfReader(HERE/'reader.pdf').pages];need(pages==2 and match and (a.out/'reader/reader.tex').read_bytes()==(HERE/'reader.tex').read_bytes(),'two reader pages and exact TeX')
  ar=appendix(a.study_root,a.out/'appendix',a.xelatex)
 result=dict(status='PASS_COMPLETE_EXPANDED_TOPIC_F_INPUT_PROPOSAL',pdf_metric_cells=180,raw_metric_cells=160,physical_pages=61,source_classes=1140,source_dictionaries=50,calibrated_classes=37,calibrated_occurrences=780,controls=c['count'],reader_pages=pages,reader_page_texts_match=match,appendix=ar,old_L014_coordinates_unchanged=30,scientific_programs_executed=False,factors_computed=False,elapsed_seconds=round(time.monotonic()-start,3))
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
