#!/usr/bin/env python3
"""Self-contained numerical author replay; no source/GAP/Lean execution."""
from pathlib import Path
from copy import deepcopy
import argparse,csv,json,subprocess,re
import calculate as C
import presentation as P

def controls(r):
 tests=[]
 def bad(name,fn):
  x=deepcopy(r);fn(x)
  try:C.validate_result(x)
  except (ValueError,KeyError,IndexError)as e:tests.append(dict(name=name,rejected=True,reason=str(e)));return
  raise ValueError('mutation accepted '+name)
 bad('omit coordinate',lambda x:x['coordinates'].pop())
 bad('duplicate coordinate',lambda x:x['coordinates'].__setitem__(0,deepcopy(x['coordinates'][1])))
 bad('omit class-table companion',lambda x:x['coordinates'][0]['totals'].update(applications=x['coordinates'][0]['costs']['A1']+x['coordinates'][0]['costs']['ROWS']))
 bad('omit source-row companion',lambda x:x['boundary'].update(application_documents=['A1','CLASSES']))
 bad('omit whole common',lambda x:x['coordinates'][0]['totals'].update(written=x['coordinates'][0]['totals']['applications']))
 bad('omit mandatory data in printed route',lambda x:x['coordinates'][0]['totals'].update(including_printed_programs_and_data=x['coordinates'][0]['totals']['written']+x['coordinates'][0]['costs']['CODE']))
 bad('omit mandatory data in raw route',lambda x:x['coordinates'][0]['totals'].update(including_raw_programs_and_data=x['coordinates'][0]['totals']['written']+x['coordinates'][0]['raw_costs']['programs']))
 bad('count printed and raw together',lambda x:x['coordinates'][0]['totals'].update(including_printed_programs_and_data=x['coordinates'][0]['totals']['including_printed_programs_and_data']+x['coordinates'][0]['raw_costs']['programs']))
 bad('halve mandatory data bytes',lambda x:x['boundary'].update(mandatory_data_bytes=41982))
 bad('omit one required program',lambda x:x['boundary'].update(whole_programs=6))
 bad('replace input JSON with printed code',lambda x:x['boundary'].update(printed_code_is_not_printed_data_substitute=False))
 bad('drop conditional data prepayment',lambda x:x['coordinates'][0]['conditional_acquisition'].update(mandatory_raw_data_cost=0))
 bad('drop conditional program prepayment',lambda x:x['coordinates'][0]['conditional_acquisition'].update(printed_program_cost=0))
 bad('condition only on five-page exposition',lambda x:x['coordinates'][0]['conditional_acquisition'].update(local_application_cost=x['coordinates'][0]['costs']['A1']))
 bad('wrong exact numerator',lambda x:x['coordinates'][0]['comparisons']['written'].update(numerator=1))
 bad('wrong fraction reduction',lambda x:x['coordinates'][0]['comparisons']['written'].update(reduced_denominator=1))
 bad('wrong displayed decimal',lambda x:x['coordinates'][0]['comparisons']['written'].update(decimal='1.000000000000'))
 bad('promote samples in place of required census',lambda x:x['boundary'].update(programs_are_required_mathematical_inputs=False))
 bad('make retained costs free',lambda x:x['boundary']['unknown_costs'].update(retained_external_proofs=0))
 bad('claim unavailable geo identities',lambda x:x['boundary'].update(no_unavailable_geo_identities_claimed=False))
 bad('recover predecessor as another source',lambda x:x['boundary'].update(predecessor_is_retained_not_new_original=False))
 bad('drop auxiliary driver',lambda x:x['boundary'].update(separate_drivers=2))
 bad('discard pipeline output inventory',lambda x:x['boundary'].update(separate_generated_outputs=0))
 bad('claim Lean proof',lambda x:x['boundary'].update(formal_declarations=1))
 bad('select calibrated primary instead',lambda x:x.update(primary=deepcopy(x['coordinates'][22])))
 bad('new scientific credit',lambda x:x.update(new_source_credit=1))
 bad('wrong physical page extent',lambda x:x['physical_pages'].__setitem__(3,9))
 def bad_input(name,fn):
  data=deepcopy(C.load());fn(data)
  try:C.validate_inputs(data)
  except (ValueError,KeyError,IndexError)as e:tests.append(dict(name=name,rejected=True,reason=str(e)));return
  raise ValueError('input mutation accepted '+name)
 bad_input('unaccepted independent input review',lambda d:d['review'].update(status='PENDING'))
 bad_input('remove entire mandatory data file',lambda d:d['counts']['raw_files']['required_raw_data'].pop(next(iter(d['counts']['raw_files']['required_raw_data']))))
 bad_input('raw count differs from independent recount',lambda d:next(iter(d['counts']['raw_files']['programs'].values()))['metrics']['NFC'].update(characters_without_whitespace=1))
 bad_input('shorten primary page extent',lambda d:d['counts']['documents']['L073'].update(pages=8))
 bad_input('omit one program from policy roster',lambda d:d['policy']['programs'].pop())
 bad_input('remove whole source-row application',lambda d:d['policy'].update(application_document_keys=['A1','CLASSES']))
 x=deepcopy(r);old=x['coordinates'][0];costs=old['costs'];costs['L073']+=1;x['coordinates'][0]=C.derive_row(old['variant'],old['normalization'],old['unit'],costs,old['raw_costs']);C.validate_result(x)
 try:C.need(x==C.calculate(),'coherent changed input still differs from accepted counts')
 except ValueError as e:tests.append(dict(name='coherently alter one accepted source count and all its fractions',rejected=True,reason=str(e)))
 else:raise ValueError('coherent numerical corruption accepted')
 return dict(status='PASS',rejected=len(tests),controls=tests)

def acquisition(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs'];routes=[]
 for kind,code in [('printed',c['CODE']),('raw',raw['programs'])]:
  total=0;steps=[]
  for key,n in [('U',c['U']),('complete_program_representation',code),('both_mandatory_JSON',raw['required_raw_data'])]+[(k,c[k])for k in C.APP]:
   total+=n;steps.append(dict(acquired=key,increment=n,total=total))
  routes.append(dict(program_representation=kind,steps=steps,total=total,upfront=steps[2]['total'],local_application=sum(c[k]for k in C.APP)))
 written=[];total=0
 for key in ['U']+C.APP:
  total+=c[key];written.append(dict(acquired=key,increment=c[key],total=total))
 return dict(scope='Whole-document and whole-file acquisition; all wrappers, references, companion tables, programs and mandatory data charged. No theorem-node saving.',written_route=written,routes=routes,source_cost=c['L073'],retained_proof_cost=None,graphics_cost=None)

def csvs(r,out):
 with (out/'costs.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['variant','normalization','unit','kind','component','cost'])
  for x in r['coordinates']:
   for kind,key in [('PDF','costs'),('raw_group','raw_costs')]:
    for k,v in x[key].items():w.writerow([x['variant'],x['normalization'],x['unit'],kind,k,v])
 with (out/'fractions.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'])
  for x in r['coordinates']:
   for k,v in x['comparisons'].items():w.writerow([x['variant'],x['normalization'],x['unit'],k]+list(v.values()))
 a=C.load()['counts']
 with (out/'raw_files.csv').open('w',newline='')as f:
  w=csv.writer(f);w.writerow(['group','path','literal_bytes','sha256','normalization','unit','cost'])
  for group,files in a['raw_files'].items():
   for path,x in files.items():
    for form in C.FORMS:
     for unit in C.UNITS:w.writerow([group,path,x['bytes'],x['sha256'],form,unit,x['metrics'][form][unit]])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 C.need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
 r=C.calculate();test=controls(r)
 for n,obj in [('results.json',r),('controls.json',test),('acquisition.json',acquisition(r))]:(a.out/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 csvs(r,a.out);P.figures(r,a.out);(a.out/'reader.tex').write_text(P.reader(r))
 report=dict(status='PASS_AUTHOR_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',input_manifests=C.PINS,coordinates=30,exact_fractions=120,combined_fractions=90,conditional_fractions=30,cost_csv_rows=300,raw_file_csv_rows=220,controls_rejected=test['rejected'],cost_bars=21,graph_nodes=6,graph_edges=6,reader_pages=None,diagnostics=[],source_extraction=False,scientific_programs_or_Lean_executed=False,new_credits=0)
 if a.render:
  from pypdf import PdfReader
  for n in (1,2):
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'pass{n}.log').write_text(p.stdout+p.stderr);C.need(p.returncode==0,'XeLaTeX exit')
  log=(a.out/'reader.log').read_text();diag=re.findall(r'(?:Overfull|Missing character|LaTeX Warning|Package .* Warning)[^\n]*',log);C.need(not diag,'clean diagnostics '+str(diag))
  pages=[p.extract_text()or''for p in PdfReader(a.out/'reader.pdf').pages];C.need(len(pages)==2,'two complete reader pages')
  report.update(reader_pages=len(pages),reader_page_text_sha256=[__import__('hashlib').sha256(x.encode()).hexdigest()for x in pages])
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(f"PASS30 coordinates/120 fractions/{test['rejected']} controls; distinct numerical acceptance pending")
if __name__=='__main__':main()
