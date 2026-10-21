#!/usr/bin/env python3
"""Check frozen inputs, complete current/history records and actual plot geometry."""
from pathlib import Path
from copy import deepcopy
import argparse,ast,json,subprocess,time
from pypdf import PdfReader
from build import HERE,read,need,sha,restore,csvs,plot_data,CHANGED,fraction
from reader import render_text
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def binding(row,root,key='path'):
 p=Path(row[key]);need(not p.is_absolute()and'..'not in p.parts,'safe path');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'binding '+str(p));return b

def nonmain(text):return {n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
def inputs(public):
 b=read('bindings.json');p=read('protocol.json')
 need([p[k]for k in ['topic_count','source_count','active_count','pending_count','archived_count','current_whole_factors','current_conditional_factors']]==[19,43,106,63,55,19,43],'fixed current scope')
 need(all(p[k]is None for k in ['software_inclusive_factor','optional_validation_inclusive_factor','original_software_cost','pooled_factor']),'unknown costs null')
 for r in b['public_inputs']:
  if r.get('local'):binding(dict(r,path=r['local']),HERE)
  if r['mode']=='immutable_public':binding(r,public,'public_path')
 for r in b['packet_inputs']:
  binding(dict(r,path=r['local']),HERE);base=HERE/Path(r['local']).parent
  for q in json.loads((base/'manifest.json').read_text())['exports']:binding(q,base)
 need(read('inputs/matched_numbers/manifest.json')['status'].startswith('AUTHOR_FROZEN'),'frozen numerical author evidence')
 need(sha((HERE/'inputs/matched_numbers/manifest.json').read_bytes())==p['required_numeric_author_manifest'],'exact numerical edition')
 current=nonmain((public/'scripts/verify_snapshot.py').read_text());need(all(current.get(n)==h for n,h in b['baseline_non_main_functions'].items()),'all old non-main ASTs unchanged')
 need(p['distinct_numeric_review']!='pending','final candidate requires distinct numerical review')
 review=read('inputs/number_review/manifest.json');need(sha((HERE/'inputs/number_review/manifest.json').read_bytes())==p['distinct_numeric_review'],'exact numerical review manifest')
 return read('inputs/v11_results.json'),read('inputs/matched_numbers/results.json'),len(current),len(review['exports'])

def validate(r,old,nums):
 need(r==restore(old,nums),'complete exact restoration')
 need(len(r['topics'])==19 and sum(len(t['pairs'])for t in r['topics'])==43,'all rows')
 need(r['original_ids']==old['original_ids']and len(set(r['original_ids']))==43,'same originals counted once')
 for t,o in zip(r['topics'],old['topics']):
  if t['topic']not in CHANGED:need(t==o,'sixteen complete topic records unchanged')
  for k in ['common_theory','applications_sum','written_denominator','program_roles','printed_program_cost','raw_program_alternative','conditional_assumption','source_ids','historical_written']:
   need(t.get(k)==o.get(k),'unchanged whole proof/code/acquisition cost '+k)
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'whole factor exact')
  need(t['written_denominator']==t['common_theory']+sum(a['application_cost']for a in t['pairs']),'whole U plus every complete bundle')
  for a,z in zip(t['pairs'],o['pairs']):
   need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'conditional exact')
   if a['source']not in CHANGED.values():need(a==z,'forty complete conditional records unchanged')
  for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost']:
   need(t.get(k)is None,'software/unknown remains null')
 return 62

def graph_check(d,root):
 count=0
 for name,s in specs(d).items():
  e,h=geometry(s);svg=(root/(name+'.svg')).read_text();compare_geometry(svg_rectangles(svg),e)
  actual,H=pdf_rectangles(root/(name+'.pdf'));need(abs(h-H)<1e-6,'PDF page geometry');compare_pdf(actual,H,e,3 if s['whole']else 2)
  text=''.join(p.extract_text()or''for p in PdfReader(root/(name+'.pdf')).pages)
  need('awaiting matched code boundary'not in svg+text,'no stale held labels')
  need(('Whole topics: full common theory and all applications charged'if s['whole']else'Conditional: whole common theory and required premises already acquired')in text,'standalone chart scope')
  count+=len(e)
 need(count==143,'all 57 whole and 86 conditional bars');return dict(actual_svg_bars=count,actual_pdf_bars=count,whole_rows=19,conditional_rows=43)

def controls(old,nums):
 base=restore(old,nums);done=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):done.append(name);return
  raise ValueError('unrejected control '+name)
 edits=[('drop recovered original',lambda r:r['original_ids'].pop()),('restore old source-only code cost',lambda r:next(t for t in r['topics']if t['topic']=='Chamber').__setitem__('source_sum',35802)),('keep whole factor held',lambda r:next(t for t in r['topics']if t['topic']=='Operations').__setitem__('written',None)),('omit whole common',lambda r:r['topics'][0].__setitem__('common_theory',0)),('modify unrelated E',lambda r:next(t for t in r['topics']if t['topic']=='E').__setitem__('source_count',5)),('expand Mixes',lambda r:next(t for t in r['topics']if t['topic']=='Mixes').__setitem__('source_count',2)),('change required roles',lambda r:next(t for t in r['topics']if t['topic']=='Operations').__setitem__('program_roles','all optional')),('invent software factor',lambda r:r['topics'][0].__setitem__('including_raw_programs',1)),('zero unknown source software',lambda r:r['topics'][0].__setitem__('historical_software_cost',0)),('erase history',lambda r:next(t for t in r['topics']if t['topic']=='Chamber').__setitem__('historical_written',None)),('wrong conditional restoration',lambda r:next(a for t in r['topics']for a in t['pairs']if a['source']=='L028')['conditional'].__setitem__('decimal','9')),('change unchanged N016',lambda r:next(a for t in r['topics']for a in t['pairs']if a['source']=='N016').__setitem__('source_cost',0)),('free N006 companion',lambda r:next(a for t in r['topics']for a in t['pairs']if a['source']=='N006').__setitem__('application_cost',21509)),('change programme count',lambda r:r.__setitem__('accessible_pending_originals',60)),('invent pooled ratio',lambda r:r.__setitem__('pooled_factor',2))]
 for name,fn in edits:q=deepcopy(base);fn(q);reject(name,lambda q=q:validate(q,old,nums))
 e,_=geometry(specs(plot_data(base))['whole_topics']);q=deepcopy(e);q[next(iter(q))][2]*=1.1;reject('distorted rendered bar',lambda:compare_geometry(q,e))
 q=deepcopy(plot_data(base));q['whole_topics'][0]['held']=True;reject('missing current numeric bar',lambda:need(q==plot_data(base),'plot complete'))
 return dict(status='PASS',negative_controls=len(done),rejected=done)

def publication_plan_check():
 plan=read('publication_map.json');rows=plan['candidate_packet'];paths=[r['source']for r in rows]
 need(len(paths)==len(set(paths)),'no duplicate candidate destination')
 need(all(r['public_path']=='audit/overview/v12/packet/'+r['source']for r in rows),'exact packet publication route')
 if(HERE/'manifest.json').exists():need(set(paths)=={'manifest.json'}|{r['path']for r in read('manifest.json')['exports']},'every frozen export mapped exactly once')
 for r in plan['evidence_packets']+plan['additional_exact_files']:binding(dict(r,path=r['source']),HERE)
 pointer=read('proposed/latest.template.json');need(pointer['current_whole_factors']==19 and pointer['current_conditional_factors']==43 and pointer['held_topics']==pointer['held_sources']==[],'proposed current pointer')
 need(pointer['admission']['sha256']is None and pointer['admission']['bytes']is None,'no fabricated root admission')
 binding(dict(pointer['reader'],path='reader.pdf'),HERE)
 need(len(read('bindings.json')['baseline_non_main_functions'])==101,'old verifier boundary')
 return dict(candidate_routes=len(rows),evidence_routes=len(plan['evidence_packets']),proposed_additions=len(plan['additional_exact_files']),unresolved_root_admission=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);start=time.monotonic()
 if(HERE/'manifest.json').exists():
  for r in read('manifest.json')['exports']:binding(r,HERE)
 old,nums,nast,nreview=inputs(a.public_root);plan_result=publication_plan_check();r=read('results.json');validate(r,old,nums)
 for n,s in csvs(r).items():need((HERE/n).read_text()==s,'exact full CSV '+n)
 d=plot_data(r);need(d==read('plot_data.json'),'exact graph data');need(render_text(r)==(HERE/'reader.tex').read_text(),'exact complete reader');con=controls(old,nums);g=graph_check(d,HERE);render=None
 if a.render:
  out=a.out/'render';out.mkdir()
  for s in specs(d).values():draw(s,out)
  need(graph_check(d,out)==g,'fresh graph reproduction');(out/'reader.tex').write_text(render_text(r))
  for i in[1,2]:
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,capture_output=True,text=True);(a.out/f'render_pass{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'TeX compilation')
  log=(out/'reader.log').read_text();diag=[l for l in log.splitlines()if any(k in l for k in ['Overfull','Underfull','Missing character','LaTeX Warning','undefined'])];need(not diag,'render diagnostics '+str(diag))
  text=[p.extract_text()or''for p in PdfReader(out/'reader.pdf').pages];need(len(text)==6,'six-page reader');need(text==[p.extract_text()or''for p in PdfReader(HERE/'reader.pdf').pages],'authoritative page-text reproduction');render=dict(pages=6,diagnostics=[],page_text_sha256=[sha(t.encode())for t in text])
 report=dict(status='PASS',whole_factors=19,conditional_factors=43,exact_fractions=62,unchanged_topics=16,unchanged_conditionals=40,recovered=43,pending=63,all_old_nonmain_ASTs_preserved=len(read('bindings.json')['baseline_non_main_functions']),current_nonmain_functions=nast,numeric_review_exports=nreview,software_inclusive_factors=None,graphs=g,controls=con,publication_plan=plan_result,render=render,no_source_extraction_or_scientific_replay=True,elapsed_seconds=round(time.monotonic()-start,3));(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
