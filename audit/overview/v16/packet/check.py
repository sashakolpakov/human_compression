#!/usr/bin/env python3
"""Additive overview checks: prior objects, all exact fractions, actual bars."""
import argparse,copy,json,os,subprocess,tempfile
from pathlib import Path
os.environ.setdefault('XDG_CACHE_HOME','/private/tmp/overview50-cache');os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'overview50-mpl'))
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,fraction
from reader import render_text
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def inputs(draft=False):
 b=read('bindings.json')
 for x in b['inputs']:
  raw=(HERE/x['path']).read_bytes();need((len(raw),sha(raw))==(x['bytes'],x['sha256']),'exact input '+x['path'])
 for m,f in [('previous_manifest','previous_results'),('numbers_manifest','numbers_results')]:
  e=next(x for x in read('inputs/'+m+'.json')['exports']if x['path']=='results.json');raw=(HERE/'inputs'/(f+'.json')).read_bytes();need((len(raw),sha(raw))==(e['bytes'],e['sha256']),'manifest owns results')
 need(sha((HERE/'inputs/numbers_manifest.json').read_bytes())=='0e1366b9e5d21d7e8158f3330d00db892840e1f9b2bf6d94c5bc05069b8d4cf9','frozen LCD numerical edition')
 if b['root_numerical_adoption']is None:
  need(draft,'root numerical adoption must be bound before final freeze')
 else:
  need(sha((HERE/'inputs/root_manifest.json').read_bytes())==b['adopted_numbers_root_sha256'],'root numerical adoption exact')
  a=read('inputs/root_adoption.json');need(a['status'].startswith('ROOT_ACCEPTED'),'actual root acceptance')
  e=next(x for x in read('inputs/root_manifest.json')['exports']if x['path']=='adoption.json');need(sha((HERE/'inputs/root_adoption.json').read_bytes())==e['sha256'],'adoption owned by manifest')
 if not draft:
  q=b['programme50_registration'];need(q['status']=='PENDING_ROOT_PUBLICATION_REGISTRATION'and q['intended_path']=='audit/programme50/v1/registration_report.json'and q['expected_new_originals']==['L050','F017']and q['expected_partition']==dict(topics=19,recovered=50,pending=56,active=106,archived=55),'explicit author-proposal registration boundary')
 return read('inputs/previous_results.json'),read('inputs/numbers_results.json')

def validate(r,old,n):
 need(r==derive(old,n),'exact deterministic additive result');need(r['topics'][:18]==old['topics'],'all18 previous whole topic objects unchanged')
 need(len(r['topics'])==19 and len(r['original_ids'])==len(set(r['original_ids']))==50,'19topics50originals');need(set(r['original_ids'])-set(old['original_ids'])=={'L050','F017'},'only exact two originals')
 for t in r['topics']:
  need(t['source_sum']==sum(a['source_cost']for a in t['pairs']),'complete source sum')
  need(t['common_theory']+sum(a['application_cost']for a in t['pairs'])==t['written_denominator'],'whole common and all applications')
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'exact whole fraction')
  for a in t['pairs']:need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'exact conditional fraction')
  need(all(t.get(k)is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']),'software symmetry and unknowns')
 t=r['topics'][-1];need(t['topic']=='LCD'and(t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'])==(58756,32300,66886,99186),'exact LCD primary complete costs')
 need(t['required_whole_file_count']==83 and t['required_original_bytes']==422956 and t['whole_file_original_bytes']==548250 and len(t['whole_file_inventory'])==102,'full raw acquisition/inventory')
 need(t['scoped_Lean_declarations']==9 and not t['full_source_formalized']and t['no_sibling_application_dependency'],'scope')
 need('Expansion'in t['whole_topic_interpretation']and r['pooled_factor']is None and r['accessible_pending_originals']==56,'expansion/no pooling/partition')
 need(r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no self admission')
 return 69

def graphs(folder,r):
 count=0
 for name,s in specs(plot_data(r)).items():
  e,H=geometry(s);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),e);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'PDF height');compare_pdf(rect,H,e,3 if s['whole']else 2);count+=len(e)
 need(count==157,'57 whole+100 conditional bars');return count

def controls(r,old,n):
 out=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):out.append(name);return
  raise ValueError('accepted mutation '+name)
 def lcd(q):return q['topics'][-1]
 edits=[('drop F017',lambda q:q['original_ids'].remove('F017')),('repeat L050',lambda q:q['original_ids'].append('L050')),('include unadmitted L121',lambda q:q['original_ids'].append('L121')),('free whole common',lambda q:lcd(q).__setitem__('common_theory',0)),('drop complete L050 application',lambda q:lcd(q)['pairs'][0].__setitem__('application_cost',0)),('drop required data',lambda q:lcd(q).__setitem__('mandatory_data_cost',0)),('invent asymmetric software factor',lambda q:lcd(q).__setitem__('including_raw_programs',1)),('sibling premise introduced',lambda q:lcd(q).__setitem__('no_sibling_application_dependency',False)),('claim full Lean',lambda q:lcd(q).__setitem__('full_source_formalized',True)),('claim whole compression',lambda q:lcd(q).__setitem__('whole_topic_interpretation','Compression')),('change prior A object',lambda q:q['topics'][0].__setitem__('common_theory',0)),('wrong pending partition',lambda q:q.__setitem__('accessible_pending_originals',58)),('switch accepted LCD primary',lambda q:lcd(q).__setitem__('primary_coordinate','raw_untrimmed/NFC/characters_without_whitespace')),('pooled factor',lambda q:q.__setitem__('pooled_factor',2)),('new question credit',lambda q:q.__setitem__('new_question_credit',1))]
 for name,edit in edits:
  q=copy.deepcopy(r);edit(q);reject(name,lambda q=q:validate(q,old,n))
 e,_=geometry(specs(plot_data(r))['whole_topics']);q=copy.deepcopy(e);q[next(iter(q))][2]*=1.1;reject('distorted actual bar',lambda:compare_geometry(q,e));q=copy.deepcopy(e);q.pop(next(iter(q)));reject('missing actual bar',lambda:compare_geometry(q,e));return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--draft',action='store_true',help='Explicitly allow missing root numerical/registration pins during private preparation only.');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 if(HERE/'manifest.json').exists():
  need(not a.draft,'frozen final overview cannot run as provisional')
  for x in read('manifest.json')['exports']:
   raw=(HERE/x['path']).read_bytes();need((len(raw),sha(raw))==(x['bytes'],x['sha256']),'immutable overview export')
 old,n=inputs(a.draft);r=derive(old,n)
 for k,v in [('results.json',r),('plot_data.json',plot_data(r))]:(a.out/k).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 for k,v in csvs(r).items():(a.out/k).write_text(v)
 for s in specs(plot_data(r)).values():draw(s,a.out)
 (a.out/'reader.tex').write_text(render_text(r));report={'status':'PASS_AUTHOR_PRIVATE_OVERVIEW50','draft':a.draft,'exact_fractions':validate(r,old,n),'unchanged_whole_topic_objects':18,'unchanged_individual_records':48,'unchanged_prior_fractions':66,'SVG_bars':graphs(a.out,r),'PDF_bars':157,'controls':controls(r,old,n)}
 if(HERE/'results.json').exists():need(read('results.json')==r,'frozen regeneration')
 if a.render:
  for i in[1,2]:
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'TeX build')
  bad=[s for s in(a.out/'reader.log').read_text().splitlines()if any(k in s for k in['Warning','Overfull','Underfull','Missing character'])];need(not bad,'clean diagnostics '+str(bad));texts=[p.extract_text()for p in PdfReader(a.out/'reader.pdf').pages];need(len(texts)==6,'six complete reader pages');report['render']={'pages':6,'diagnostics':bad,'page_text_hashes':[sha(t.encode())for t in texts]}
  if(HERE/'reader.pdf').exists():need(texts==[p.extract_text()for p in PdfReader(HERE/'reader.pdf').pages],'exact frozen page text')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','draft':a.draft,'fractions':69,'bars':157,'controls':len(report['controls'])}))
if __name__=='__main__':main()
