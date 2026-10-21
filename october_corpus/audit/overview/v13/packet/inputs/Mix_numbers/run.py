#!/usr/bin/env python3
"""Portable accepted-cell replay. No private PDF extraction or scientific execution."""
from pathlib import Path
import argparse,shutil,subprocess,sys
from compute import need,read,write,sha,evaluate,manifest
from build_reader import build
HERE=Path(__file__).resolve().parent
OUTPUTS=['results.json','input_bindings.json','comparisons.csv','measurement.tex','measurement.pdf','complete_costs.svg','complete_costs.pdf','plot_geometry.json','document_graphs.svg','document_graphs.pdf','document_graphs.json','render_report.json']
def run(a):
 need(not a.out.exists(),'fresh complete output')
 if(HERE/'manifest.json').exists():manifest(HERE,sha(HERE/'manifest.json'))
 a.out.mkdir(parents=True);r=evaluate(a.inputs,a.prior_inputs,a.input_review,a.out/'numbers');build(r,a.out/'render',a.xelatex)
 result=a.out/'result';result.mkdir()
 for name in OUTPUTS:shutil.copyfile((a.out/'numbers' if name in ['results.json','input_bindings.json','comparisons.csv']else a.out/'render')/name,result/name)
 z=subprocess.run([sys.executable,'-B','-O',str(HERE/'check.py'),'--inputs',str(a.inputs),'--prior-inputs',str(a.prior_inputs),'--input-review',str(a.input_review),'--results-dir',str(result),'--out',str(a.out/'author_check.json')],capture_output=True,text=True);(a.out/'check.log').write_text(z.stdout+z.stderr);need(z.returncode==0,'complete semantic/vector checker')
 exact=[]
 for name in OUTPUTS:
  if not(HERE/name).exists()or name=='measurement.pdf':continue
  need((result/name).read_bytes()==(HERE/name).read_bytes(),'exact replay '+name);exact.append(name)
 text_equal=False
 if(HERE/'measurement.pdf').exists():
  from pypdf import PdfReader
  old=[x.extract_text()for x in PdfReader(HERE/'measurement.pdf').pages];new=[x.extract_text()for x in PdfReader(result/'measurement.pdf').pages];need(old==new,'all reader page texts');text_equal=True
 report=dict(status='PASS_PORTABLE_ACCEPTED_INPUT_NUMERICAL_REPLAY',exact_outputs=exact,reader_pages=3,all_reader_page_texts_equal=text_equal,author_check=read(a.out/'author_check.json'),software_inclusive_factor=None,scientific_programs_executed=False,primary_PDFs_required=False,distinct_numerical_review=False)
 write(a.out/'report.json',report);print('PASS portable complete Mixes numerical replay')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--prior-inputs',type=Path,required=True);p.add_argument('--input-review',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));run(p.parse_args())
