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
 bad('omit required counterproof',lambda x:x['coordinates'][0]['totals'].update(applications=x['coordinates'][0]['costs']['A1']))
 bad('counterproof free local premise',lambda x:x['boundary'].update(application_documents=['A1']))
 bad('omit whole common',lambda x:x['coordinates'][0]['totals'].update(written=x['coordinates'][0]['totals']['applications']))
 bad('add both code representations',lambda x:x['coordinates'][0]['totals'].update(with_printed_programs=x['coordinates'][0]['totals']['with_printed_programs']+x['coordinates'][0]['raw_costs']['programs']))
 bad('conditional skips code',lambda x:x['coordinates'][0]['conditional_acquisition'].update(printed_upfront=x['coordinates'][0]['costs']['U']))
 bad('conditional skips counterproof',lambda x:x['coordinates'][0]['conditional_acquisition'].update(local_application_cost=x['coordinates'][0]['costs']['A1']))
 bad('incorrect fraction numerator',lambda x:x['coordinates'][0]['comparisons']['written'].update(numerator=1))
 bad('incorrect reduced fraction',lambda x:x['coordinates'][0]['comparisons']['written'].update(reduced_denominator=1))
 bad('incorrect decimal',lambda x:x['coordinates'][0]['comparisons']['written'].update(decimal='2.000000000000'))
 bad('omit one program',lambda x:x['boundary'].update(whole_programs=2))
 bad('promote validation to uniform premise',lambda x:x['boundary']['program_roles'].__setitem__(1,'required_uniform_proof'))
 bad('unknown retained proof made zero',lambda x:x['boundary']['unknown_costs'].update(full_retained_classical_proofs=0))
 bad('add old appendix',lambda x:x['boundary'].update(old_program_appendix_replaced=False))
 bad('old B common free',lambda x:x['boundary'].update(no_free_old_B=False))
 bad('omit driver',lambda x:x['boundary'].update(separate_drivers=2))
 bad('claim complete Lean proof',lambda x:x['boundary'].update(whole_source_formalized=True))
 bad('inflate partial declarations',lambda x:x['boundary'].update(partial_Lean_declarations=16))
 bad('wrong physical pages',lambda x:x['physical_pages'].__setitem__(3,2))
 bad('count correction as second original',lambda x:x.update(source_ids=['L020','COUNTER']))
 bad('new scientific credit',lambda x:x.update(new_source_credit=1))
 bad('calibrated primary substituted',lambda x:x.update(primary=deepcopy(x['coordinates'][22])))
 def bad_input(name,fn):
  x=deepcopy(C.load());fn(x)
  try:C.validate_inputs(x)
  except (ValueError,KeyError,IndexError)as e:tests.append(dict(name=name,rejected=True,reason=str(e)));return
  raise ValueError('input mutation accepted '+name)
 bad_input('unaccepted input review',lambda x:x['review'].update(status='PENDING'))
 bad_input('short source extent',lambda x:x['counts']['documents']['L020'].update(pages=18))
 bad_input('omit raw validation file',lambda x:x['policy']['programs'].pop())
 bad_input('raw value differs from independent recount',lambda x:next(iter(x['counts']['raw_files']['programs'].values()))['metrics']['NFC'].update(characters_without_whitespace=1))
 bad_input('local boundary omits counterproof',lambda x:x['policy'].update(applications={'L020':['A1']}))
 x=deepcopy(r);z=x['coordinates'][0];z['costs']['L020']+=1;x['coordinates'][0]=C.derive_row(z['variant'],z['normalization'],z['unit'],z['costs'],z['raw_costs']);C.validate_result(x)
 try:C.need(x==C.calculate(),'coherent altered arithmetic differs from accepted source counts')
 except ValueError as e:tests.append(dict(name='coherently alter accepted count and all dependent fractions',rejected=True,reason=str(e)))
 else:raise ValueError('coherent corruption accepted')
 return dict(status='PASS',rejected=len(tests),controls=tests)

def acquisition(r):
 c=r['primary']['costs'];raw=r['primary']['raw_costs'];routes=[]
 for kind,code in [('printed',c['CODE']),('raw',raw['programs'])]:
  total=0;steps=[]
  for key,n in [('U',c['U']),('complete_program_representation',code)]+[(k,c[k])for k in C.APP]:
   total+=n;steps.append(dict(acquired=key,increment=n,total=total))
  routes.append(dict(program_representation=kind,steps=steps,total=total,upfront=steps[1]['total'],local_application=sum(c[k]for k in C.APP)))
 written=[];total=0
 for key in ['U']+C.APP:
  total+=c[key];written.append(dict(acquired=key,increment=c[key],total=total))
 return dict(scope='Whole-document/file acquisition. Counterproof, wrappers and references remain charged. No graph-node savings.',written_route=written,routes=routes,source_cost=c['L020'],retained_proof_cost=None,graphics_cost=None)

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
 report=dict(status='PASS_AUTHOR_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',input_manifests=C.PINS,coordinates=30,exact_fractions=120,combined_fractions=90,conditional_fractions=30,cost_csv_rows=240,raw_file_csv_rows=80,controls_rejected=test['rejected'],cost_bars=15,graph_nodes=6,graph_edges=8,reader_pages=None,diagnostics=[],source_extraction=False,scientific_programs_or_Lean_executed=False,new_credits=0)
 if a.render:
  from pypdf import PdfReader
  for n in (1,2):
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'pass{n}.log').write_text(p.stdout+p.stderr);C.need(p.returncode==0,'XeLaTeX exit')
  log=(a.out/'reader.log').read_text();diag=re.findall(r'(?:Overfull|Missing character|LaTeX Warning|Package .* Warning)[^\n]*',log);C.need(not diag,'clean diagnostics '+str(diag))
  pages=[p.extract_text()or''for p in PdfReader(a.out/'reader.pdf').pages];C.need(len(pages)==2,'two complete reader pages')
  report.update(reader_pages=len(pages),reader_page_text_sha256=[__import__('hashlib').sha256(x.encode()).hexdigest()for x in pages])
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(f"PASS30 coordinates/120 fractions/{test['rejected']} controls; distinct numerical acceptance pending")
if __name__=='__main__':main()
