#!/usr/bin/env python3
"""Author replay/control checker; independent numerical review remains necessary."""
import argparse,copy,csv,json,math,subprocess,sys
from pathlib import Path
from compute import HERE,UNITS,VARIANTS,NORMS,SOURCES,APPS,accepted_inputs,derive,write_result,need,sha,dump,load

def verify(r,a):
 need(len(r['coordinates'])==r['coordinates_count']==30,'30 complete coordinates')
 need(r['exact_combined_fractions']==90 and r['exact_conditional_fractions']==60,'150 exact fractions')
 seen=set();nf=0
 for c in r['coordinates']:
  v,n,u=[c[k] for k in ['variant','normalization','unit']];need((v,n,u) not in seen and v in VARIANTS and n in NORMS and u in UNITS,'coordinate domain');seen.add((v,n,u))
  d={k:row['metrics'][v][n][u] for k,row in a['documents'].items()};need(c['document_costs']==d,'whole PDF costs')
  raw={k:sum(row['metrics'][n][u] for row in rr.values()) for k,rr in a['raw_files'].items()};s=d['L084']+d['L095'];common=d['U']+d['TABLES'];apps=d['A1']+d['A2'];w=common+apps;pd=d['CODE'];rp=raw['programs'];data=raw['required_data']
  for k,val in dict(source_cost=s,whole_common_cost=common,application_cost=apps,written_cost=w,printed_program_cost=pd,raw_program_cost=rp,mandatory_data_cost=data,operational_driver_cost_separate=raw['operational_drivers']).items():need(c[k]==val,'whole cost '+k)
  need(c['conditional_acquisition']==dict(common_proof=d['U'],common_tables=d['TABLES'],whole_common=common,printed_program_option=pd,raw_program_option=rp,mandatory_raw_data=data,printed_total=common+pd+data,raw_total=common+rp+data),'full conditional acquisition')
  defs={'written_papers':(s,w),'printed_programs_plus_mandatory_data':(s,w+pd+data),'raw_programs_plus_mandatory_data':(s,w+rp+data)}
  fs=[(c['comparisons'][k],num,den) for k,(num,den) in defs.items()]+[(c['conditional_applications'][src],d[src],d[APPS[src]]) for src in SOURCES]
  for f,num,den in fs:
   g=math.gcd(num,den);need((f['numerator'],f['denominator'])==(num,den),'literal ratio integers');need((f['reduced_numerator'],f['reduced_denominator'])==(num//g,den//g),'reduced integers');need(f['exact_fraction']==(str(num//g) if den//g==1 else f'{num//g}/{den//g}'),'exact ratio string');need(f['factor']==num/den,'display float');nf+=1
 primary=next(c for c in r['coordinates'] if (c['variant'],c['normalization'],c['unit'])==('calibrated_selected','NFC','characters_without_whitespace'));need(r['primary']==primary,'accepted primary')
 need(r['whole_common_charged_once'] and r['complete_common_documents']==['U','TABLES'] and r['all_applications_charged'] and not r['cross_topic_discount'] and not r['sibling_application_free_premise'],'no free proof crossing')
 p=r['programme_boundary'];expected={'complete_required_programs':6,'raw_program_bytes':24255,'complete_printed_program_pages':6,'required_data_files':1,'required_data_bytes':39150,'required_data_in_both_routes':True,'printed_program_is_data_substitute':False,'printed_and_raw_are_alternatives':True,'operational_drivers_separate':3,'driver_raw_bytes':32220,'generated_outputs_separate':11,'generated_output_bytes':3470182,'output_not_additional_enumeration_input':True,'selected_runtime_model_pins':13,'formal_files':0,'formal_declarations':0}
 for k,val in expected.items():need(p[k]==val,'complete software role '+k)
 need(set(r['unknown_costs'])=={'retained_classical_proofs','complete_runtime_implementation','historical_software','graphics_and_layout','full_formalization'} and all(x is None for x in r['unknown_costs'].values()),'unknown costs not zero')
 need(r['originals']==2 and r['source_record_count']==52 and r['historical_rows']==145 and r['new_source_credit']==r['new_question_credit']==0,'unchanged scientific scope')
 need(not r['full_source_formalized'] and not r['public_mutations'],'no formal/public claim')
 need(r['physical_extent']==dict(source_pages={'L084':2,'L095':15},common_proof_pages=7,common_tables_pages=5,application_pages={'L084':2,'L095':3},written_replacement_pages=17,printed_program_pages=6,all_input_pages=40),'complete physical pages')
 return nf

def verify_plot(plot,r):
 c=r['primary'];d=c['document_costs'];ac=c['conditional_acquisition']
 need(plot['primary']==[c[k] for k in ['variant','normalization','unit']] and plot['zero_origin'],'plot primary/origin')
 need(plot['all_full_document_costs'] and plot['printed_raw_alternative'] and plot['mandatory_data_in_both_routes'] and not plot['acquisition_curve_claimed'],'plot accounting')
 vals=[[c['source_cost'],0,0,0,0],[0,c['whole_common_cost'],c['application_cost'],0,0],[0,c['whole_common_cost'],c['application_cost'],c['printed_program_cost'],c['mandatory_data_cost']],[0,c['whole_common_cost'],c['application_cost'],c['raw_program_cost'],c['mandatory_data_cost']]]
 components=['Sources','Whole common','Applications','Programs','Mandatory JSON'];g=plot['whole_cost_graph'];need(g['components']==components and len(g['bars'])==4,'whole four-bar graph')
 expected=[]
 for y,(bar,vs) in enumerate(zip(g['bars'],vals)):
  need(bar['components']==dict(zip(components,vs)) and bar['total']==sum(vs),'full stacked bar total');x=0
  for val in vs:
   if val:expected.append((x,y-.275,val,.55));x+=val
 need(len(expected)==len(g['rendered_rectangles']),'all actual rectangles')
 for rect,exp in zip(g['rendered_rectangles'],expected):need(all(math.isclose(rect[k],v,abs_tol=1e-9) for k,v in zip(['x','y','width','height'],exp)),'actual rectangle width/origin')
 dv=[d['L084'],d['L095'],c['whole_common_cost'],d['A1'],d['A2']];gg=plot['common_and_applications_graph'];need([b['total'] for b in gg['bars']]==dv and len(gg['rendered_rectangles'])==5,'full common/application bars')
 for i,(rect,val) in enumerate(zip(gg['rendered_rectangles'],dv)):need(math.isclose(rect['x'],0) and math.isclose(rect['width'],val) and math.isclose(rect['y'],i-.3,abs_tol=1e-9),'actual full document rectangle')
 return {'whole_cost_bars':4,'common_application_bars':5,'actual_rectangles':len(expected)+5}

def controls(r,a,plot):
 names=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError):names.append(name);return
  raise ValueError('mutation accepted: '+name)
 idx=next(i for i,c in enumerate(r['coordinates']) if c==r['primary'])
 def mutate(name,f):
  b=copy.deepcopy(r);f(b,b['coordinates'][idx]);reject(name,lambda:verify(b,a))
 mutate('omit entire common',lambda b,c:c['comparisons']['written_papers'].__setitem__('denominator',c['application_cost']))
 mutate('omit common tables',lambda b,c:c.__setitem__('whole_common_cost',c['document_costs']['U']))
 mutate('double charge common',lambda b,c:c.__setitem__('written_cost',c['written_cost']+c['whole_common_cost']))
 mutate('omit one application',lambda b,c:c.__setitem__('application_cost',c['document_costs']['A2']))
 mutate('prune mandatory historical data',lambda b,c:c.__setitem__('mandatory_data_cost',100))
 mutate('omit mandatory data from printed denominator',lambda b,c:c['comparisons']['printed_programs_plus_mandatory_data'].__setitem__('denominator',c['written_cost']+c['printed_program_cost']))
 mutate('omit mandatory data from raw denominator',lambda b,c:c['comparisons']['raw_programs_plus_mandatory_data'].__setitem__('denominator',c['written_cost']+c['raw_program_cost']))
 mutate('add both code representations',lambda b,c:c['comparisons']['printed_programs_plus_mandatory_data'].__setitem__('denominator',c['written_cost']+c['printed_program_cost']+c['raw_program_cost']+c['mandatory_data_cost']))
 mutate('prune one full program',lambda b,c:c.__setitem__('raw_program_cost',c['raw_program_cost']-1))
 mutate('add operational driver to mathematical code',lambda b,c:c.__setitem__('raw_program_cost',c['raw_program_cost']+c['operational_driver_cost_separate']))
 mutate('drop driver disclosure',lambda b,c:c.__setitem__('operational_driver_cost_separate',0))
 mutate('conditional free tables',lambda b,c:c['conditional_acquisition'].__setitem__('common_tables',0))
 mutate('conditional free data',lambda b,c:c['conditional_acquisition'].__setitem__('mandatory_raw_data',0))
 mutate('conditional numerator combines originals',lambda b,c:c['conditional_applications']['L084'].__setitem__('numerator',c['source_cost']))
 mutate('conditional denominator includes prepaid common',lambda b,c:c['conditional_applications']['L095'].__setitem__('denominator',c['document_costs']['A2']+c['whole_common_cost']))
 mutate('printed code falsely contains data',lambda b,c:b['programme_boundary'].__setitem__('printed_program_is_data_substitute',True))
 mutate('omit output inventory',lambda b,c:b['programme_boundary'].__setitem__('generated_outputs_separate',0))
 mutate('unpaid sibling proof',lambda b,c:b.__setitem__('sibling_application_free_premise',True))
 mutate('free prior umbrella',lambda b,c:b.__setitem__('cross_topic_discount',True))
 mutate('claim formal source proof',lambda b,c:b.__setitem__('full_source_formalized',True))
 mutate('invent Lean declarations',lambda b,c:b['programme_boundary'].__setitem__('formal_declarations',1))
 mutate('unknown graphics zero',lambda b,c:b['unknown_costs'].__setitem__('graphics_and_layout',0))
 mutate('change source credit',lambda b,c:b.__setitem__('new_source_credit',1))
 mutate('round exact fraction',lambda b,c:c['comparisons']['written_papers'].__setitem__('exact_fraction','0.707079'))
 mutate('silently use raw primary',lambda b,c:b.__setitem__('primary',b['coordinates'][2]))
 mutate('omit sensitivity',lambda b,c:b['coordinates'].pop())
 for name,change in [('graph drops mandatory data',lambda p:p['whole_cost_graph']['bars'][2]['components'].__setitem__('Mandatory JSON',0)),('graph crops axis origin',lambda p:p.__setitem__('zero_origin',False)),('graph omits common tables',lambda p:p['common_and_applications_graph']['bars'][2].__setitem__('total',19533)),('graph wrong actual rectangle',lambda p:p['whole_cost_graph']['rendered_rectangles'][0].__setitem__('width',1))]:
  bad=copy.deepcopy(plot);change(bad);reject(name,lambda:verify_plot(bad,r))
 return names

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');args=p.parse_args();out=args.out;need(not out.exists() and not out.is_symlink(),'fresh output');out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for e in load(HERE/'manifest.json')['exports']:need((HERE/e['path']).stat().st_size==e['bytes'] and sha(HERE/e['path'])==e['sha256'],'frozen export '+e['path'])
 a,p,old=accepted_inputs();r=derive(a,p,old);nf=verify(r,a);write_result(out/'derived',r)
 for path in (out/'derived').iterdir():
  if (HERE/path.name).exists():need(path.read_bytes()==(HERE/path.name).read_bytes(),'exact deterministic output '+path.name)
 from build_reader import render_assets
 render_assets(r,out/'reader');plot=load(out/'reader/plot_data.json');bars=verify_plot(plot,r);ctrl=controls(r,a,plot)
 for name in ['reader.tex','plot_data.json']:
  if (HERE/name).exists():need((HERE/name).read_bytes()==(out/'reader'/name).read_bytes(),'exact reader artifact '+name)
 diag=[];np=None;matching=None
 if args.render:
  for i in range(2):
   q=subprocess.run([args.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out/'reader',stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'reader'/f'render{i}.log').write_bytes(q.stdout);need(q.returncode==0,'fresh XeLaTeX')
  log=(out/'reader/reader.log').read_text(errors='replace');diag=[line for line in log.splitlines() if any(k in line for k in ['Missing character','Overfull','Underfull','LaTeX Warning','Package fontspec Warning'])];need(not diag,'clean typography')
  from pypdf import PdfReader
  texts=[p.extract_text() for p in PdfReader(out/'reader/reader.pdf').pages];np=len(texts)
  if (HERE/'reader.pdf').exists():matching=texts==[p.extract_text() for p in PdfReader(HERE/'reader.pdf').pages];need(matching,'fresh exact reader page texts')
 dump(out/'report.json',{'status':'PASS','role':'Author replay, not distinct independent review','coordinates':30,'exact_fractions':nf,'csv_rows':{'overall':90,'conditional':60,'documents':210,'software':120,'acquisition':30},'actual_plots':bars,'controls':ctrl,'reader_pages':np,'render_diagnostics':diag,'reader_page_texts_match':matching,'source_extraction_or_science_repeated':False,'inputs':__import__('compute').PINS});print(json.dumps({'status':'PASS','coordinates':30,'exact_fractions':nf,'controls':len(ctrl),'reader_pages':np,'plots':bars}))
if __name__=='__main__':main()
