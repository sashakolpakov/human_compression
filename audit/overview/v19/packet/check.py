#!/usr/bin/env python3
"""Portable A10 overview replay; accepted costs only, no extraction or science."""
from pathlib import Path
from copy import deepcopy
import argparse,json,subprocess,os,tempfile
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'overview53_cache'))
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'overview53_mpl'))
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,fraction
from reader import render_text,shown
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
NUM='524b5f73c007e5ba783920859874fe3cb8b5ce7a73d28929b82bf94678e9e31f';REVIEW='2ff490f6744b5edce0307861dbb9d16dec2029efbb4251d80120c405729dfad5'
def bind(row,root=HERE):
 p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'relative binding');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p))
def inputs():
 for z in read('bindings.json')['inputs']:bind(z)
 need(sha((HERE/'protocol.json').read_bytes())==read('protocol_freeze.json')['protocol_sha256'],'fixed protocol');need(sha((HERE/'bindings.json').read_bytes())==read('protocol.json')['bindings_sha256'],'fixed inputs')
 for manifest,name,pin in [('inputs/numbers_manifest.json','inputs/numbers_results.json',NUM),('inputs/previous_manifest.json','inputs/previous_results.json',None)]:
  if pin:need(sha((HERE/manifest).read_bytes())==pin,'accepted manifest pin')
  z=next(z for z in read(manifest)['exports']if z['path']=='results.json');bind(dict(z,path=name))
 need(sha((HERE/'inputs/distinct_review/manifest.json').read_bytes())==REVIEW,'root review pin')
 for z in read('inputs/distinct_review/manifest.json')['exports']:bind(z,HERE/'inputs/distinct_review')
 q=read('inputs/distinct_review/review.json');need(q['status']=='ACCEPTED_DISTINCT_NUMERICAL_REVIEW'and q['author_manifest']['sha256']==NUM,'actual adoption')
 for z in read('acceptance_binding.json')['bindings']:bind(z)
 need(sha((HERE/'inputs/root_adoption/manifest.json').read_bytes())=='22c8ee3758140daabe9f01ae3d4701b36340c5b7d293695a76e065549bff3b3c','actual root adoption')
 for z in read('inputs/root_adoption/manifest.json')['exports']:bind(z,HERE/'inputs/root_adoption')
 need(read('inputs/root_adoption/adoption.json')['bindings']['author']['sha256']==NUM,'accepted exact numerical packet')
 return read('inputs/previous_results.json'),read('inputs/numbers_results.json')
def topic(r):return next(t for t in r['topics']if t['topic']=='A')
def scope(r):
 p=read('inputs/previous_corpus.json');measured=sorted(p['measured_original_ids']+['L003']);pending=sorted(set(p['accessible_pending_original_ids'])-{'L003'});editorial=p['editorial_original_ids']
 need((len(measured),len(pending),len(editorial),len(p['archived_original_ids']))==(53,52,1,55),'partition53/52/1/55');need(set(measured)==set(r['original_ids'])and len(set(measured+pending+editorial))==106 and set(measured+pending+editorial)==set(p['active_original_ids']),'unique106 partition')
 return dict(status='PRIVATE_PROGRAMME53_PENDING_ROOT_PUBLICATION',measured_original_ids=measured,mathematical_pending_original_ids=pending,editorial_original_ids=editorial,active_original_ids=p['active_original_ids'],archived_original_ids=p['archived_original_ids'],counts=dict(active=106,measured=53,mathematical_pending=52,editorial=1,archived=55,topics=19),actual_root_registration_binding=None,new_measured_originals=['L003'],editorial_factor=None)
def validate(r,old,n):
 need(r==derive(old,n),'deterministic complete overview');need([t for t in r['topics']if t['topic']!='A']==[t for t in old['topics']if t['topic']!='A'],'18 whole records exact')
 before={a['source']:a for t in old['topics']for a in t['pairs']};after={a['source']:a for t in r['topics']for a in t['pairs']};need(all(after[k]==v for k,v in before.items()if k!='L121')and set(after)-set(before)=={'L003'},'all51 old individual objects except changed L121 exact')
 for t in r['topics']:
  need(t['source_ids']==[a['source']for a in t['pairs']]and t['source_count']==len(t['pairs']),'exact pairing')
  need(t['source_sum']==sum(a['source_cost']for a in t['pairs']),'all sources')
  need(t['written_denominator']==t['common_theory']+sum(a['application_cost']for a in t['pairs']),'whole common/all apps')
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'whole fraction')
  for a in t['pairs']:need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'conditional')
  need(all(t.get(k)is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']),'no unknown-inclusive factor')
 t=topic(r);need(t['current_written_status']=='AVAILABLE_FROM_ACCEPTED_ENLARGED_MATCHED_MANUSCRIPT_BOUNDARY'and len(t['whole_file_inventory'])==203,'current A metadata')
 need((t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'])==(319016,108271,155199,263470),'accepted complete A10 components');need(t['whole_file_inventory']==n['whole_file_inventory']and t['whole_file_group_costs']==n['whole_file_group_costs'],'full whole-file inventory');need(t['entire_common_pages']==[23,14,4]and t['required_whole_file_count']==99,'three whole common papers/all required premises')
 need(r['pooled_factor']is None and r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no pooled/new credits');need(r['editorial_original_ids']==['L022']and 'L022'not in r['original_ids']and r['editorial_dispositions']==old['editorial_dispositions'],'editorial unchanged')
 scope(r);return 72
def graphs(folder,r):
 count=0
 for name,s in specs(plot_data(r)).items():
  e,H=geometry(s);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),e);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'PDF dimensions');compare_pdf(rect,H,e,3 if s['whole']else 2);count+=len(e)
 need(count==163,'57+106 actual rectangles');return count

def controls(r,old,n):
 out=[]
 tests=[('omit L003',lambda q:q['original_ids'].remove('L003')),('duplicate L003',lambda q:q['original_ids'].append('L003')),('free common supplement',lambda q:topic(q).__setitem__('common_theory',66140)),('free structural common',lambda q:topic(q).__setitem__('common_theory',100126)),('alter prior individual',lambda q:topic(q)['pairs'][0].__setitem__('application_cost',1)),('drop complete A10 companion',lambda q:topic(q)['pairs'][-1].__setitem__('application_cost',20122)),('restore obsolete L121 application',lambda q:topic(q)['pairs'][-2].__setitem__('application_cost',25549)),('change unrelated topic',lambda q:next(t for t in q['topics']if t['topic']=='B').__setitem__('common_theory',0)),('software-inclusive ratio',lambda q:topic(q).__setitem__('including_raw_programs',1)),('missing required content',lambda q:topic(q)['whole_file_inventory'].pop()),('full Lean',lambda q:topic(q).__setitem__('full_source_formalized',True)),('remove corrected source qualifications',lambda q:topic(q).__setitem__('scientific_boundary','All literal source statements reproduced.')),('editorial factor zero',lambda q:q['editorial_dispositions'][0].__setitem__('factor',0)),('wrong pending',lambda q:q.__setitem__('accessible_pending_originals',53)),('new conjecture credit',lambda q:q.__setitem__('new_question_credit',1)),('invent root registration pin',lambda q:q['whole_programme_binding'].__setitem__('registration_sha256','invented')),('pooled ratio',lambda q:q.__setitem__('pooled_factor',1)),('stale A status',lambda q:topic(q).__setitem__('current_written_reason','Exact v18 whole cost unchanged.')),('old inventory as current',lambda q:topic(q).__setitem__('whole_file_inventory',topic(old)['whole_file_inventory']))]
 for label,fn in tests:
  q=deepcopy(r);fn(q)
  try:validate(q,old,n)
  except(ValueError,KeyError,TypeError):out.append(label)
  else:raise ValueError('mutation accepted '+label)
 for name,s in specs(plot_data(r)).items():
  want,_=geometry(s)
  for change in ['width','missing']:
   q=deepcopy(want)
   if change=='width':q[next(iter(q))][2]*=1.1
   else:q.pop(next(iter(q)))
   try:compare_geometry(q,want)
   except ValueError:out.append(name+' '+change)
   else:raise ValueError('graph mutation accepted')
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 if(HERE/'manifest.json').exists():
  for z in read('manifest.json')['exports']:bind(z)
 old,n=inputs();r=derive(old,n);objs={'results.json':r,'plot_data.json':plot_data(r),'programme_scope.json':scope(r)}
 for name,q in objs.items():
  (a.out/name).write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n')
  if(HERE/name).exists():need(read(name)==q,'exact regenerated '+name)
 for name,text in csvs(r).items():
  (a.out/name).write_text(text)
  if(HERE/name).exists():need((HERE/name).read_text()==text,'exact CSV '+name)
 for spec in specs(plot_data(r)).values():draw(spec,a.out)
 (a.out/'reader.tex').write_text(render_text(r));report=dict(status='PASS_AUTHOR_PRIVATE_OVERVIEW53',exact_fractions=validate(r,old,n),unchanged_other_topics=18,unchanged_individuals=51,actual_bars_per_format=graphs(a.out,r),controls=controls(r,old,n),public_registration_pending=True,no_scientific_or_input_replay=True)
 if(HERE/'reader.tex').exists():need((HERE/'reader.tex').read_text()==render_text(r),'exact reader');graphs(HERE,r)
 if a.render:
  for i in [1,2]:
   q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'render')
  bad=[z for z in(a.out/'reader.log').read_text().splitlines()if any(k in z for k in ['Warning','Overfull','Underfull','Missing character'])];need(not bad,'clean render '+str(bad));texts=[z.extract_text()or''for z in PdfReader(a.out/'reader.pdf').pages];need(len(texts)==6,'six pages')
  for t in r['topics']:need(shown(t['written'])in texts[0],'printed whole factor')
  for i,z in enumerate([z for t in r['topics']for z in t['pairs']]):need(shown(z['conditional'])in texts[1 if i<27 else 2],'printed conditional')
  report['reader']=dict(pages=6,diagnostics=[],table_rows=[19,27,26],page_text_sha256=[sha(z.encode())for z in texts])
  if(HERE/'reader.pdf').exists():need(texts==[z.extract_text()or''for z in PdfReader(HERE/'reader.pdf').pages],'exact saved page texts')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
