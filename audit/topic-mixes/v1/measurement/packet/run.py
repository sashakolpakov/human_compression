#!/usr/bin/env python3
"""Portable complete numerical rebuild; accepted input artifacts are explicit roots."""
from pathlib import Path
import argparse,shutil
import compute,build_reader,check
from compute import need,write
from pypdf import PdfReader
H=Path(__file__).resolve().parent

def run(a):
 need(not a.out.exists(),'fresh complete replay output');data=compute.inputs(a);r=compute.derive(*data);a.out.mkdir(parents=True)
 write(a.out/'results.json',r);write(a.out/'input_bindings.json',data[3]);compute.save_csv(a.out/'comparisons.csv',compute.csv_rows(r))
 build_reader.build(r,a.out/'render',a.xelatex)
 for n in ['complete_costs.svg','complete_costs.pdf','plot_geometry.json','measurement.tex','measurement.pdf','render_report.json']:shutil.copyfile(a.out/'render'/n,a.out/n)
 args=argparse.Namespace(inputs=a.inputs,input_review=a.input_review,results_dir=a.out,out=a.out/'author_check.json');check.run(args)
 exact=['results.json','input_bindings.json','comparisons.csv','complete_costs.svg','complete_costs.pdf','plot_geometry.json','measurement.tex']
 for n in exact:need((a.out/n).read_bytes()==(H/n).read_bytes(),'exact frozen numerical/reader/vector output '+n)
 old=[p.extract_text()for p in PdfReader(H/'measurement.pdf').pages];new=[p.extract_text()for p in PdfReader(a.out/'measurement.pdf').pages]
 need(len(new)==2 and new==old,'exact two-page reader text')
 if (H/'manifest.json').exists():compute.bind(H,compute.sha(H/'manifest.json'))
 write(a.out/'replay.json',dict(status='PASS_PORTABLE_AUTHOR_NUMERICAL_REPLAY',exact_outputs=exact,reader_pages=2,reader_page_text_equal=True,exact_fractions=120,actual_vector_rectangles=dict(svg=14,pdf=14),negative_controls=24,input_extraction_repeated=False,scientific_programs_repeated=False,independent_numerical_review=False))
 print('PASS complete numerical replay: seven exact outputs, two page texts,120fractions and24controls.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--input-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));run(ap.parse_args())
