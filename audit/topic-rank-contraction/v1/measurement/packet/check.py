#!/usr/bin/env python3
"""Author reproducibility and corruption controls; distinct review remains required."""
import argparse,copy,csv,hashlib,json,math,shutil,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
from compute import HERE,UNITS,VARIANTS,NORMALIZATIONS,accepted_inputs,derive,need,dump,write_result,sha

def verify(r,a):
 need(len(r['coordinates'])==30 and r['coordinates_count']==30,'all coordinates')
 need(r['exact_combined_fractions']==90 and r['exact_conditional_fractions']==30,'all fractions')
 seen=set();nf=0
 for c in r['coordinates']:
  v,n,u=[c[k] for k in ['variant','normalization','unit']];need((v,n,u) not in seen and v in VARIANTS and n in NORMALIZATIONS and u in UNITS,'coordinate domain');seen.add((v,n,u))
  costs={k:row['metrics'][v][n][u] for k,row in a['documents'].items()};need(c['document_costs']==costs,'whole PDF costs')
  raw={cat:sum(row['metrics'][n][u] for row in rs.values()) for cat,rs in a['raw_files'].items()}
  source,common,app,printed=[costs[k] for k in ['L037','U','A1','CODE']]
  need(c['written_cost']==common+app and c['printed_program_cost']==printed and c['raw_program_cost']==raw['programs'],'whole paper/program boundary')
  need(c['driver_cost_separate']==raw['drivers'] and c['formal_file_cost_separate']==raw['formal'],'separate raw files')
  need(c['conditional_acquisition']==dict(whole_common=common,complete_printed_program_option=printed,complete_raw_program_option=raw['programs'],printed_total=common+printed,raw_total=common+raw['programs']),'whole acquisition')
  dens={'written_papers':common+app,'including_printed_program':common+app+printed,'including_raw_program_alternative':common+app+raw['programs']}
  fs=[(c['comparisons'][k],d) for k,d in dens.items()]+[(c['conditional_application'],app)]
  for f,d in fs:
   g=math.gcd(source,d);need(f['numerator']==source and f['denominator']==d,'literal integer ratio');need(f['reduced_numerator']==source//g and f['reduced_denominator']==d//g,'reduced fraction');need(f['exact_fraction']==f'{source//g}/{d//g}' if d//g!=1 else f['exact_fraction']==str(source//g),'exact string');need(f['factor']==source/d,'numeric display');nf+=1
 primary=next(c for c in r['coordinates'] if (c['variant'],c['normalization'],c['unit'])==('raw_untrimmed','NFC','characters_without_whitespace'))
 need(r['primary']==primary,'complete raw primary')
 need(r['whole_common_charged_once'] and r['all_application_pages_charged'] and not r['old_Topic_B_common_free_premise'] and not r['cross_topic_discount'],'no free earlier theory')
 p=r['programme_boundary'];need(p['complete_programs']==p['local_finite_certificate_programs']==1 and p['uniform_required_programs']==0 and p['printed_and_raw_are_alternatives'],'program roles')
 need(p['driver_files_separate']==p['Lean_files_separate']==1 and p['scoped_declarations']==4 and not p['full_source_formalized'],'formal/driver roles')
 for k in ['retained_external_proof_cost','full_graphic_layout_cost','historical_software_cost','full_formalization_cost','minimal_mathematical_complexity']:need(r[k] is None,'unknown cost '+k)
 need(r['source_rows']==22 and r['proof_contexts']==20 and r['originals']==1 and r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'scope/credits')
 need(r['physical_extent']==dict(source_pages=6,common_pages=3,application_pages=5,written_replacement_pages=8,printed_program_pages=1,all_input_pages=15),'full physical extent')
 return nf

def controls(r,a):
 out=[]
 def reject(name,mutate):
  bad=copy.deepcopy(r);mutate(bad)
  try:verify(bad,a)
  except (ValueError,KeyError):out.append(name);return
  raise ValueError('mutation accepted '+name)
 pidx=next(i for i,c in enumerate(r['coordinates']) if c==r['primary'])
 def setc(r,key,value):r['coordinates'][pidx][key]=value
 reject('omit common in written denominator',lambda r:r['coordinates'][pidx]['comparisons']['written_papers'].__setitem__('denominator',10555))
 reject('double count common',lambda r:setc(r,'written_cost',24429))
 reject('omit application reference page',lambda r:r['coordinates'][pidx]['document_costs'].__setitem__('A1',10000))
 reject('combine raw and printed code',lambda r:r['coordinates'][pidx]['comparisons']['including_printed_program'].__setitem__('denominator',22918))
 reject('prune raw finite program',lambda r:setc(r,'raw_program_cost',2000))
 reject('add driver to mathematical program',lambda r:setc(r,'raw_program_cost',8615))
 reject('drop separate driver cost',lambda r:setc(r,'driver_cost_separate',0))
 reject('drop separate formal file',lambda r:setc(r,'formal_file_cost_separate',0))
 reject('conditional denominator adds prepaid theory',lambda r:r['coordinates'][pidx]['conditional_application'].__setitem__('denominator',17492))
 reject('conditional acquisition omits program',lambda r:r['coordinates'][pidx]['conditional_acquisition'].__setitem__('printed_total',6937))
 reject('claim free old Topic B overlap',lambda r:r.__setitem__('cross_topic_discount',True))
 reject('promote finite certificates to uniform premises',lambda r:r['programme_boundary'].__setitem__('uniform_required_programs',1))
 reject('claim full formalization',lambda r:r['programme_boundary'].__setitem__('full_source_formalized',True))
 reject('unknown external cost zero',lambda r:r.__setitem__('retained_external_proof_cost',0))
 reject('unknown graphics cost zero',lambda r:r.__setitem__('full_graphic_layout_cost',0))
 reject('source-credit change',lambda r:r.__setitem__('new_source_credit',1))
 reject('select calibrated instead of raw primary',lambda r:r.__setitem__('primary',r['coordinates'][22]))
 reject('rounded number as exact fraction',lambda r:r['coordinates'][pidx]['comparisons']['written_papers'].__setitem__('exact_fraction','0.887834'))
 reject('missing sensitivity coordinate',lambda r:r['coordinates'].pop())
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');args=p.parse_args();out=args.out
 need(not out.exists() and not out.is_symlink(),'fresh output required');out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for e in json.loads((HERE/'manifest.json').read_text())['exports']:
   f=HERE/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'frozen numerical export')
 a,policy=accepted_inputs();r=derive(a,policy);n=verify(r,a);negative=controls(r,a);write_result(out/'calculation',r)
 coordinate_map={(c['variant'],c['normalization'],c['unit']):c for c in r['coordinates']}
 observed={}
 for basename,expected_count in [('overall_costs',90),('conditional_costs',30),('document_costs',120),('software_costs',120)]:
  with (out/'calculation'/(basename+'.csv')).open(newline='') as f: records=list(csv.DictReader(f))
  observed[basename]=len(records);need(len(records)==expected_count,'all CSV rows')
  for row in records:
   c=coordinate_map[tuple(row[k] for k in ['variant','normalization','unit'])]
   if basename in ['overall_costs','conditional_costs']:
    ratio=c['comparisons'][row['comparison']] if basename=='overall_costs' else c['conditional_application']
    for k,v in ratio.items():need(row[k]==str(v),'CSV exact fraction')
    if basename=='conditional_costs':need(row['prepaid']==r['conditional_prepayment'],'conditional CSV disclosure')
   elif basename=='document_costs':need(int(row['cost'])==c['document_costs'][row['document']],'CSV whole document cost')
   else:need(int(row['cost'])==c[row['role']],'CSV separate program/driver/formal cost')
 for name in ['results.json','overall_costs.csv','conditional_costs.csv','document_costs.csv','software_costs.csv']:
  if (HERE/name).exists():need((HERE/name).read_bytes()==(out/'calculation'/name).read_bytes(),'exact regenerated '+name)
 reader=None
 if args.render:
  q=subprocess.run([sys.executable,'-B','-O',str(HERE/'build_reader.py'),'--out',str(out/'reader'),'--render','--xelatex',args.xelatex],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'reader_build.log').write_bytes(q.stdout);need(q.returncode==0,'reader build')
  log=(out/'reader/reader.log').read_text();diagnostics=[s for s in log.splitlines() if any(x in s for x in ['Overfull','Underfull','Missing character','LaTeX Warning','Package hyperref Warning'])];need(not diagnostics,'reader diagnostics')
  pg=PdfReader(out/'reader/reader.pdf').pages;need(len(pg)==3,'complete three-page reader')
  if (HERE/'reader.pdf').exists():need([p.extract_text() for p in pg]==[p.extract_text() for p in PdfReader(HERE/'reader.pdf').pages],'reader page text')
  for name in ['reader.tex','plot_data.json']:
   if (HERE/name).exists():need((out/'reader'/name).read_bytes()==(HERE/name).read_bytes(),'reader/plot exact data')
  plot=json.loads((out/'reader/plot_data.json').read_text());need(plot['zero_origin'] and len(plot['rendered_rectangles'])==9,'actual zero-based rectangles')
  totals=[b['total'] for b in plot['bars']];need(totals==[15530,17492,20417,19993],'complete bars')
  row_widths=[sum(q['width'] for q in plot['rendered_rectangles'] if abs(q['y']-(i-.31))<1e-6) for i in range(4)];need(row_widths==totals,'actual plotted rectangle widths')
  reader={'pages':3,'diagnostics':diagnostics,'actual_bars':4,'actual_stacked_rectangles':9,'page_text_sha256':[hashlib.sha256(p.extract_text().encode()).hexdigest() for p in pg]}
 report={'status':'PASS','policy_coordinates':30,'exact_fractions':n,'csv_rows':observed,'negative_controls':negative,'reader':reader,'input_extraction_repeated':False,'mathematics_GAP_Lean_replayed':False,'author_not_independent_numerical_acceptance':True}
 dump(out/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
