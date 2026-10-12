#!/usr/bin/env python3
"""Portable B6 overview replay; accepted costs only, no extraction or science."""
from pathlib import Path
from copy import deepcopy
import argparse,json,subprocess,os,tempfile
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'overview52_cache'))
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'overview52_mpl'))
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,fraction
from reader import render_text,shown
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
NUM='eaa3f62b0cea99890ed73f2816212423cde2a48dec43a8aaca756b4d6e7a9118';REVIEW='e296ffe24f1313cd7d2a1f70e16c3b8a25b3e825a9d4f87a4e52e9276f552f1f'
def bind(row,root=HERE):
 p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'relative binding');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p))
def inputs():
 for z in read('bindings.json')['inputs']:bind(z)
 need(sha((HERE/'protocol.json').read_bytes())==read('protocol_freeze.json')['protocol_sha256'],'fixed protocol');need(sha((HERE/'bindings.json').read_bytes())==read('protocol.json')['bindings_sha256'],'fixed inputs')
 for manifest,name,pin in [('inputs/numbers_manifest.json','inputs/numbers_results.json',NUM),('inputs/previous_manifest.json','inputs/previous_results.json',None)]:
  if pin:need(sha((HERE/manifest).read_bytes())==pin,'accepted manifest pin')
  z=next(z for z in read(manifest)['exports']if z['path']=='results.json');bind(dict(z,path=name))
 need(sha((HERE/'inputs/root_review/manifest.json').read_bytes())==REVIEW,'root review pin')
 for z in read('inputs/root_review/manifest.json')['exports']:bind(z,HERE/'inputs/root_review')
 q=read('inputs/root_review/review.json');need(q['status']=='ACCEPTED_DISTINCT_NUMERICAL_REVIEW_AND_ROOT_ADOPTION'and q['author_manifest']['sha256']==NUM,'actual adoption')
 return read('inputs/previous_results.json'),read('inputs/numbers_results.json')
def topic(r):return next(t for t in r['topics']if t['topic']=='B')
def scope(r):
 p=read('inputs/previous_corpus.json');measured=sorted(p['measured_original_ids']+['L047']);pending=sorted(set(p['accessible_pending_original_ids'])-{'L047'});editorial=p['editorial_original_ids']
 need((len(measured),len(pending),len(editorial),len(p['archived_original_ids']))==(52,53,1,55),'partition52/53/1/55');need(set(measured)==set(r['original_ids'])and len(set(measured+pending+editorial))==106 and set(measured+pending+editorial)==set(p['active_original_ids']),'unique106 partition')
 return dict(status='PRIVATE_PROGRAMME52_PENDING_ROOT_PUBLICATION',measured_original_ids=measured,mathematical_pending_original_ids=pending,editorial_original_ids=editorial,active_original_ids=p['active_original_ids'],archived_original_ids=p['archived_original_ids'],counts=dict(active=106,measured=52,mathematical_pending=53,editorial=1,archived=55,topics=19),actual_root_registration_binding=None,new_measured_originals=['L047'],editorial_factor=None)
def validate(r,old,n):
 need(r==derive(old,n),'deterministic complete overview');need([t for t in r['topics']if t['topic']!='B']==[t for t in old['topics']if t['topic']!='B'],'18 whole records exact')
 before={a['source']:a for t in old['topics']for a in t['pairs']};after={a['source']:a for t in r['topics']for a in t['pairs']};need(all(after[k]==v for k,v in before.items())and set(after)-set(before)=={'L047'},'all51 old individual objects exact')
 for t in r['topics']:
  need(t['source_ids']==[a['source']for a in t['pairs']]and t['source_count']==len(t['pairs']),'exact pairing')
  need(t['source_sum']==sum(a['source_cost']for a in t['pairs']),'all sources')
  need(t['written_denominator']==t['common_theory']+sum(a['application_cost']for a in t['pairs']),'whole common/all apps')
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'whole fraction')
  for a in t['pairs']:need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'conditional')
  need(all(t.get(k)is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']),'no unknown-inclusive factor')
 t=topic(r);need(t['current_written_status']=='AVAILABLE_FROM_ACCEPTED_ENLARGED_MATCHED_MANUSCRIPT_BOUNDARY'and len(t['separate_raw_inventory']['files'])==17 and t['historical_separate_raw_inventory']['inventory']==topic(old)['separate_raw_inventory'],'current B metadata and historical inventory');need((t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'])==(144877,74303,74768,149071),'accepted B6 components');need(t['whole_file_inventory']==n['whole_file_inventory']and t['whole_file_group_costs']==n['whole_file_groups'],'full whole-file inventory');need(t['entire_common_pages']==[16,10]and t['whole_written_interpretation']=='expansion','both common/expansion')
 need(r['pooled_factor']is None and r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no pooled/new credits');need(r['editorial_original_ids']==['L022']and 'L022'not in r['original_ids']and r['editorial_dispositions']==old['editorial_dispositions'],'editorial unchanged')
 scope(r);return 71
def graphs(folder,r):
 count=0
 for name,s in specs(plot_data(r)).items():
  e,H=geometry(s);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),e);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'PDF dimensions');compare_pdf(rect,H,e,3 if s['whole']else 2);count+=len(e)
 need(count==161,'57+104 actual rectangles');return count

def controls(r,old,n):
 out=[]
 tests=[('omit L047',lambda q:q['original_ids'].remove('L047')),('duplicate L047',lambda q:q['original_ids'].append('L047')),('free supplement',lambda q:topic(q).__setitem__('common_theory',44905)),('free old common',lambda q:topic(q).__setitem__('common_theory',29398)),('alter prior individual',lambda q:topic(q)['pairs'][0].__setitem__('application_cost',1)),('drop complete B6',lambda q:topic(q)['pairs'][-1].__setitem__('application_cost',0)),('change unrelated topic',lambda q:q['topics'][0].__setitem__('common_theory',0)),('software-inclusive ratio',lambda q:topic(q).__setitem__('including_raw_programs',1)),('missing required roster',lambda q:topic(q)['whole_file_inventory'].pop()),('mislabel expansion',lambda q:topic(q).__setitem__('whole_written_interpretation','compression')),('full Lean',lambda q:topic(q).__setitem__('full_source_formalized',True)),('regenerate all ancillary claims',lambda q:topic(q).__setitem__('scientific_boundary','All source statements reproduced.')),('editorial factor zero',lambda q:q['editorial_dispositions'][0].__setitem__('factor',0)),('wrong pending',lambda q:q.__setitem__('accessible_pending_originals',54)),('new conjecture credit',lambda q:q.__setitem__('new_question_credit',1)),('invent current root pin',lambda q:q['whole_programme_binding'].__setitem__('registration_sha256','invented')),('pooled ratio',lambda q:q.__setitem__('pooled_factor',1)),('stale B status',lambda q:topic(q).__setitem__('current_written_status','AVAILABLE_FROM_UNCHANGED_MATCHED_MANUSCRIPT_BOUNDARY')),('historical inventory as current',lambda q:topic(q).__setitem__('separate_raw_inventory',topic(old)['separate_raw_inventory'])),('stale whole-cost reason',lambda q:topic(q).__setitem__('current_written_reason','Exact v10 costs and fraction retained.'))]
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

def metadata_delta(r):
 m=read('historical/manifest.json');need(sha((HERE/'historical/manifest.json').read_bytes())=='299ac13b8abf48861009f517a318d29aba829b5e0dea679d7d1a702d51f52131','immutable original overview18')
 binding=next(z for z in m['exports']if z['path']=='results.json');bind(binding,HERE/'historical')
 before=read('historical/results.json');after=deepcopy(r);allowed={'current_written_status','current_written_reason','written_comparison_scope','separate_raw_inventory','historical_separate_raw_inventory','historical_acquisition_inventory_source'}
 tb=topic(before);ta=topic(after);changed={k for k in set(tb)|set(ta)if tb.get(k)!=ta.get(k)};need(changed==allowed,'exact six-field metadata-only correction')
 for k in allowed:
  if k in tb:ta[k]=tb[k]
  else:ta.pop(k,None)
 need(after==before,'all other overview values exact')
 for name in ['topics.csv','applications.csv','editorial.csv','reader.tex','reader.pdf','whole_topics.svg','whole_topics.pdf','conditional_1.svg','conditional_1.pdf','conditional_2.svg','conditional_2.pdf']:
  bind(next(z for z in m['exports']if z['path']==name))
 return sorted(changed)

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 if(HERE/'manifest.json').exists():
  for z in read('manifest.json')['exports']:bind(z)
 old,n=inputs();r=derive(old,n);metadata_delta(r);objs={'results.json':r,'plot_data.json':plot_data(r),'programme_scope.json':scope(r)}
 for name,q in objs.items():
  (a.out/name).write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n')
  if(HERE/name).exists():need(read(name)==q,'exact regenerated '+name)
 for name,text in csvs(r).items():
  (a.out/name).write_text(text)
  if(HERE/name).exists():need((HERE/name).read_text()==text,'exact CSV '+name)
 for spec in specs(plot_data(r)).values():draw(spec,a.out)
 (a.out/'reader.tex').write_text(render_text(r));report=dict(status='PASS_AUTHOR_PRIVATE_OVERVIEW52',exact_fractions=validate(r,old,n),unchanged_other_topics=18,unchanged_individuals=51,actual_bars_per_format=graphs(a.out,r),controls=controls(r,old,n),public_registration_pending=True,no_scientific_or_input_replay=True)
 if(HERE/'reader.tex').exists():need((HERE/'reader.tex').read_text()==render_text(r),'exact reader');graphs(HERE,r)
 if a.render:
  for i in [1,2]:
   q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'render')
  bad=[z for z in(a.out/'reader.log').read_text().splitlines()if any(k in z for k in ['Warning','Overfull','Underfull','Missing character'])];need(not bad,'clean render '+str(bad));texts=[z.extract_text()or''for z in PdfReader(a.out/'reader.pdf').pages];need(len(texts)==6,'six pages')
  for t in r['topics']:need(shown(t['written'])in texts[0],'printed whole factor')
  for i,z in enumerate([z for t in r['topics']for z in t['pairs']]):need(shown(z['conditional'])in texts[1 if i<26 else 2],'printed conditional')
  report['reader']=dict(pages=6,diagnostics=[],table_rows=[19,26,26],page_text_sha256=[sha(z.encode())for z in texts])
  if(HERE/'reader.pdf').exists():need(texts==[z.extract_text()or''for z in PdfReader(HERE/'reader.pdf').pages],'exact saved page texts')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
