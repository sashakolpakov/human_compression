#!/usr/bin/env python3
"""Exact overview arithmetic, preservation and actual SVG/PDF geometry."""
import argparse,copy,json,os,shutil,subprocess,tempfile
from pathlib import Path
os.environ.setdefault('XDG_CACHE_HOME','/private/tmp/overview48-cache')
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'overview48-mpl'))
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,fraction
from reader import render_text
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def inputs():
 for x in read('bindings.json')['inputs']:
  b=(HERE/x['path']).read_bytes();need(len(b)==x['bytes']and sha(b)==x['sha256'],'exact adopted evidence')
 for m,f in [('previous_manifest','previous_results'),('numbers_manifest','numbers_results')]:
  e=next(x for x in read('inputs/'+m+'.json')['exports']if x['path']=='results.json');b=(HERE/'inputs'/ (f+'.json')).read_bytes();need((len(b),sha(b))==(e['bytes'],e['sha256']),'manifest owns result')
 need(sha((HERE/'inputs/root_manifest.json').read_bytes())=='e52ed6fff70311e54c866402da59d69912d4e07b560956f365f4175049364f4e','root numerical acceptance')
 a=read('inputs/root_adoption.json');need(a['status']=='ROOT_ACCEPTED_REPRESENTATION_SUCCESSOR_NUMERICAL_COMPARISON'and a['corrections_requested']==[],'accepted exact numbers')
 e=next(x for x in read('inputs/root_manifest.json')['exports']if x['path']=='adoption.json');need(sha((HERE/'inputs/root_adoption.json').read_bytes())==e['sha256'],'adoption bytes')
 return read('inputs/previous_results.json'),read('inputs/numbers_results.json')
def validate(r,old,n):
 need(r==derive(old,n),'whole deterministic result');need(len(r['topics'])==18 and len(r['original_ids'])==len(set(r['original_ids']))==48,'18/48 boundary')
 prior={x['topic']:x for x in old['topics']};unchanged=0
 for t in r['topics']:
  if t['topic']!='Representation':need(t==prior[t['topic']],'unchanged topic '+t['topic']);unchanged+=1
  need(t['source_sum']==sum(a['source_cost']for a in t['pairs']),'complete source sum');need(t['common_theory']+sum(a['application_cost']for a in t['pairs'])==t['written_denominator'],'whole common and apps')
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'whole factor')
  for a in t['pairs']:need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'individual factor')
  need(all(t.get(k)is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']),'unknown and symmetric software')
 need(unchanged==17,'17 unchanged');t=next(t for t in r['topics']if t['topic']=='Representation');need(t['common_theory']==36715 and t['source_sum']==60472 and t['written_denominator']==82152,'whole adopted coordinate')
 need(t['mandatory_data_cost']==19315 and t['raw_program_alternative']==34823 and t['printed_program_cost']==35723,'code/data separate full inventory')
 need(t['no_sibling_application_dependency']and t['scoped_Lean_declarations']==22 and not t['full_source_formalized'],'actual proof/formal scope')
 need('Expansion'in t['whole_topic_interpretation']and r['pooled_factor']is None,'candid whole expansion/no pooling')
 return 66

def graphs(folder,r):
 count=0
 for name,s in specs(plot_data(r)).items():
  e,H=geometry(s);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),e);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'PDF height');compare_pdf(rect,H,e,3 if s['whole']else 2);count+=len(e)
 need(count==150,'54 whole and96 local bars');return count

def controls(r,old,n):
 out=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):out.append(name);return
  raise ValueError('accepted mutation '+name)
 def rep(q):return next(x for x in q['topics']if x['topic']=='Representation')
 edits=[('drop L126',lambda q:q['original_ids'].remove('L126')),('repeat F010',lambda q:q['original_ids'].append('F010')),('free common',lambda q:rep(q).__setitem__('common_theory',0)),('reuse old R1',lambda q:rep(q)['pairs'][0].__setitem__('application_cost',13688)),('drop requiredJSON',lambda q:rep(q).__setitem__('mandatory_data_cost',0)),('invent software factor',lambda q:rep(q).__setitem__('including_raw_programs',1)),('free sibling',lambda q:rep(q).__setitem__('no_sibling_application_dependency',False)),('claim fullLean',lambda q:rep(q).__setitem__('full_source_formalized',True)),('claim wholecompression',lambda q:rep(q).__setitem__('whole_topic_interpretation','Compression')),('alter priorA',lambda q:q['topics'][0].__setitem__('common_theory',0)),('wrongpending',lambda q:q.__setitem__('accessible_pending_originals',59)),('switch primary',lambda q:rep(q).__setitem__('primary_coordinate','raw_untrimmed/NFC/characters_without_whitespace')),('pooledfactor',lambda q:q.__setitem__('pooled_factor',2)),('questioncredit',lambda q:q.__setitem__('new_question_credit',1))]
 for name,edit in edits:
  q=copy.deepcopy(r);edit(q);reject(name,lambda q=q:validate(q,old,n))
 e,_=geometry(specs(plot_data(r))['whole_topics']);q=copy.deepcopy(e);q[next(iter(q))][2]*=1.1;reject('distorted actualbar',lambda:compare_geometry(q,e));q=copy.deepcopy(e);q.pop(next(iter(q)));reject('missingactualbar',lambda:compare_geometry(q,e));return out

def verify():
 old,n=inputs();r=read('results.json');validate(r,old,n)
 for name,text in csvs(r).items():need((HERE/name).read_text()==text,'literal CSV '+name)
 need(read('plot_data.json')==plot_data(r),'plot data');need((HERE/'reader.tex').read_text()==render_text(r),'reader source')
 return {'status':'PASS_AUTHOR_OVERVIEW48','topics':18,'originals':48,'pending':58,'active':106,'unchanged_topic_objects':17,'unchanged_other_individuals':46,'exact_fractions':66,'CSV_rows':66,'actual_SVG_bars':graphs(HERE,r),'actual_PDF_bars':150,'semantic_and_vector_controls':controls(r,old,n)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);old,n=inputs();r=derive(old,n)
 for k,v in [('results.json',r),('plot_data.json',plot_data(r))]:(a.out/k).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 for k,v in csvs(r).items():(a.out/k).write_text(v)
 for spec in specs(plot_data(r)).values():draw(spec,a.out)
 (a.out/'reader.tex').write_text(render_text(r));report={'status':'PASS_AUTHOR_OVERVIEW48','exact_fractions':validate(r,old,n),'SVG_bars':graphs(a.out,r),'PDF_bars':150,'controls':controls(r,old,n)}
 if(HERE/'results.json').exists():need(read('results.json')==r,'frozen exact regeneration')
 if a.render:
  for i in[1,2]:
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'TeX build')
  bad=[s for s in(a.out/'reader.log').read_text().splitlines()if any(k in s for k in['Warning','Overfull','Underfull','Missing character'])];need(not bad,'clean diagnostics '+str(bad));text=[p.extract_text()for p in PdfReader(a.out/'reader.pdf').pages];need(len(text)==6,'sixpages')
  report['render']={'pages':6,'diagnostics':bad,'page_text_hashes':[sha(t.encode())for t in text]}
  if(HERE/'reader.pdf').exists():need(text==[p.extract_text()for p in PdfReader(HERE/'reader.pdf').pages],'exact frozen page text')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','fractions':66,'bars':150,'controls':len(report['controls'])}))
if __name__=='__main__':main()
