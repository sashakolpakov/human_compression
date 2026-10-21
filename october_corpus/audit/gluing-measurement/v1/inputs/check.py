#!/usr/bin/env python3
"""Full Gluing input replay, with optional isolated TeX rebuild; no ratios."""
from pathlib import Path
import argparse,json,re,shutil,subprocess
import pypdf
import extract_inputs as E
import controls,make_reader
from font_tools import need,sha
H=Path(__file__).resolve().parent

def run(a):
 need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
 result,audits,cache=E.replay(a)
 need(result==E.load('author_counts.json'),'all150 PDF and80 raw cells and text hashes match')
 negative=controls.run(a,cache);need(negative==E.load('author_controls.json'),'all36 semantic controls reproduce')
 need(make_reader.make()==(H/'input_reader.tex').read_text(),'exact complete reader, counts and qualifications')
 visual=E.load('graphics_and_visual.json');need(visual['source']['pdf_sha256']==result['documents']['L010']['pdf_sha256'] and len(visual['source']['pages'])==15,'source visual record binding')
 need(visual['source']['full_graphical_cost'] is None and all(v is None for v in visual['excluded_costs'].values()),'graphic and outside costs are unknown')
 font_counts={k:dict(dictionaries=len(v['font_dictionaries']),classes=len(v['encoded_glyph_classes']))for k,v in audits.items()}
 need(font_counts['L010']==dict(dictionaries=27,classes=559) and font_counts['CODE']==dict(dictionaries=2,classes=3),'actual font dictionary/class counts')
 need(sum(v['glyph_repairs']for v in result['documents'].values())==175,'all observed substitutions')
 rendered=[]
 if a.render:
  dest=a.out/'render';dest.mkdir();(dest/'programs').mkdir()
  for f in ['input_reader.tex','programs.tex']:
   shutil.copyfile(H/f,dest/f)
  for row in E.load('policy.json')['programs']:shutil.copyfile(H/row['printed_path'],dest/row['printed_path'])
  for stem,pages in [('programs',4),('input_reader',2)]:
   for i in range(2):
    r=subprocess.run([str(a.xelatex),'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=dest,capture_output=True,text=True)
    (dest/f'{stem}.run{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'clean TeX exit '+stem)
   log=(dest/(stem+'.log')).read_text();need(not re.search('Overfull|Missing character|LaTeX Warning|Package .* Warning',log),'no layout or glyph diagnostics '+stem)
   original=[p.extract_text()for p in pypdf.PdfReader(H/(stem+'.pdf')).pages];actual=[p.extract_text()for p in pypdf.PdfReader(dest/(stem+'.pdf')).pages]
   need(len(actual)==pages and actual==original,'complete page-text render match '+stem)
   rendered.append(dict(document=stem,pages=pages,per_page_text_equal=True))
 report=dict(status='PASS_AUTHOR_INPUT_REPLAY_PENDING_DISTINCT_REVIEW',pdf_cells=150,raw_cells=80,whole_PDFs=5,pages=35,semantic_controls=negative['rejected'],font_counts=font_counts,glyph_substitutions=175,rendered=rendered,program_inclusion=result['program_inclusion'],scientific_programs_executed=False,factors_evaluated=False,ratio=None,source_count=1,source_map_records=23,partial_formal_declarations=10)
 for name,obj in [('report.json',report),('counts.json',result),('controls.json',negative),('font_audit.json',audits)]:
  (a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS150 PDF+80 raw cells,36 controls; no factors.');return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--sources-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));run(p.parse_args())
