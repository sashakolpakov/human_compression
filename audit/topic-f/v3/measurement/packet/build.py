#!/usr/bin/env python3
"""Portable arithmetic/reader generation from accepted counts; no science rerun."""
from pathlib import Path
from copy import deepcopy
import argparse,csv,json,re,subprocess
import calculate as C,presentation as P

def controls(r):
 tests=[]
 def bad(name,fn,validator=C.validate_result,base=r):
  x=deepcopy(base);fn(x)
  try:validator(x)
  except(ValueError,KeyError,IndexError)as e:tests.append(dict(name=name,rejected=True,reason=str(e)));return
  raise ValueError('mutation accepted '+name)
 bad('omit coordinate',lambda x:x['coordinates'].pop())
 bad('omit whole common',lambda x:x['coordinates'][0]['totals'].update(written=x['coordinates'][0]['totals']['applications']))
 bad('omit chiral application',lambda x:x['boundary'].update(written_documents=['U','A1']))
 bad('add asymmetric software fraction',lambda x:x['coordinates'][0]['comparisons'].update(including_printed_programs=C.fraction(x['coordinates'][0]['totals']['source'],x['coordinates'][0]['totals']['written']+x['coordinates'][0]['costs']['CODE'])))
 bad('require optional validation for conditional',lambda x:x['coordinates'][0]['conditional_acquisition'].update(optional_validation_required=True))
 bad('replace unknown source software by zero',lambda x:x['boundary'].update(source_validation_software_cost=0))
 bad('omit one validation program from inventory',lambda x:x['boundary'].update(whole_programs=8))
 bad('promote validation to proof premise',lambda x:x['boundary'].update(uniform_finite_premise_programs=1))
 bad('alter exact numerator',lambda x:x['coordinates'][0]['comparisons']['written'].update(numerator=1))
 bad('make retained proof free',lambda x:x['boundary']['unknown_costs'].update(full_retained_CP_proof=0))
 bad('claim full source formalization',lambda x:x['boundary'].update(full_source_formalized=True))
 bad('claim new question credit',lambda x:x.update(new_question_credit=1))
 old=C.read(C.ROOT/'correction_evidence/previous_results.json')
 x=deepcopy(r);row=x['coordinates'][0];row['costs']['L014']+=1;x['coordinates'][0]=C.derive_row(row['variant'],row['normalization'],row['unit'],row['costs'],row['raw_costs']);C.validate_result(x)
 try:C.check_preservation(x,old)
 except ValueError as e:tests.append(dict(name='coherently change accepted costs and derived fractions',rejected=True,reason=str(e)))
 else:raise ValueError('coherent cost corruption accepted')
 protocol=C.read(C.ROOT/'protocol.json')
 bad('restore obsolete all-program prepayment',lambda x:x.update(conditional_prepaid=['whole U','all nine programs']),lambda x:C.validate_correction(C.ROOT,x,C.load()),protocol)
 return dict(status='PASS',rejected=len(tests),controls=tests)

def acquisition(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs'];total=0;written=[]
 for key in ['U']+C.APP:total+=c[key];written.append(dict(acquired=key,increment=c[key],total=total))
 return dict(scope='Whole documents including context and references; optional validation is separate, not required prepayment or a source-software comparison.',written_route=written,optional_validation_alternatives=dict(printed=c['CODE'],raw=raw['programs'],whole_files=9,source_cost=None,symmetric_factor=None),conditional_prepaid_common=c['U'],source_costs={s:c[s]for s in C.SOURCES},retained_proof_cost=None,graphics_cost=None)

def csvs(r,out):
 with(out/'costs.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['variant','normalization','unit','kind','component','cost'])
  for x in r['coordinates']:
   for kind,key in [('PDF','costs'),('raw_group','raw_costs')]:
    for k,v in x[key].items():w.writerow([x['variant'],x['normalization'],x['unit'],kind,k,v])
 with(out/'fractions.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'])
  for x in r['coordinates']:
   for k,v in x['comparisons'].items():w.writerow([x['variant'],x['normalization'],x['unit'],k]+list(v.values()))
 with(out/'raw_files.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['group','path','literal_bytes','sha256','normalization','unit','cost'])
  for group,files in C.load()['counts']['raw_files'].items():
   for path,x in files.items():
    for form in C.FORMS:
     for unit in C.UNITS:w.writerow([group,path,x['bytes'],x['sha256'],form,unit,x['metrics'][form][unit]])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();C.need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
 r=C.calculate();test=controls(r)
 for n,obj in [('results.json',r),('controls.json',test),('acquisition.json',acquisition(r)),('preservation.json',C.check_preservation(r,C.read(C.ROOT/'correction_evidence/previous_results.json')))]:(a.out/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 csvs(r,a.out);P.figures(r,a.out);(a.out/'reader.tex').write_text(P.reader(r))
 report=dict(status='PASS_AUTHOR_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',input_manifests=C.PINS,coordinates=30,exact_fractions=90,combined_fractions=30,conditional_fractions=60,cost_csv_rows=270,raw_file_csv_rows=160,controls_rejected=test['rejected'],cost_bars=11,graph_nodes=7,graph_edges=9,reader_pages=None,diagnostics=[],source_extraction=False,scientific_programs_or_Lean_executed=False,new_credits=0)
 if a.render:
  from pypdf import PdfReader
  for n in(1,2):
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'pass{n}.log').write_text(p.stdout+p.stderr);C.need(p.returncode==0,'XeLaTeX exit')
  log=(a.out/'reader.log').read_text();diag=re.findall(r'(?:Overfull|Missing character|LaTeX Warning|Package .* Warning)[^\n]*',log);C.need(not diag,'clean diagnostics '+str(diag))
  pages=[p.extract_text()or''for p in PdfReader(a.out/'reader.pdf').pages];C.need(len(pages)==3,'three complete reader pages')
  C.need(all(not any(ord(c)<32 and c not in '\n\t\r' or c=='\ufffd' or 0xE000<=ord(c)<=0xF8FF for c in t)for t in pages),'reader glyphs')
  report.update(reader_pages=len(pages),reader_page_text_sha256=[__import__('hashlib').sha256(x.encode()).hexdigest()for x in pages])
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(f"PASS30 coordinates/90 fractions/{test['rejected']} controls; distinct numerical acceptance pending")
if __name__=='__main__':main()
