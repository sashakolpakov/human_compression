#!/usr/bin/env python3
"""Exact accepted-topic consolidation with public catalogue and geometry guards."""
from pathlib import Path
from copy import deepcopy
import argparse,ast,json,subprocess
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,CHANGED,NEW,fraction
from reader import render_text
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def binding(row,root,key='path'):
 p=Path(row[key]);need(not p.is_absolute()and'..'not in p.parts,'safe binding path');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p));return b

def nonmain(text):return{n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
def programme_check(programme,public):
 for row in programme['public_artifacts']:binding(row,public)
 need(programme['counts']==dict(topics=19,recovered=46,pending=60,active=106,archived=55),'programme root counts')
 need(programme['new_originals']==NEW and set(programme['source_admissions'])==set(CHANGED),'new three source admissions only')
 def doc(key):return json.loads((public/programme[key]).read_text())
 snap=doc('snapshot');old=doc('previous_corpus_pointer');active=doc('active_catalogue');prior=doc('previous_active_catalogue');papers=doc('current_paper_catalogue');pointer=doc('current_corpus_pointer')
 need(pointer==dict(snap,snapshot=next(x for x in programme['public_artifacts']if x['path']==programme['snapshot'])),'exact current corpus pointer')
 need(papers==doc('current_paper_pointer'),'current paper pointer exact')
 need([snap[k]for k in ['originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','archived_unavailable_originals']]==[106,106,46,60,55],'snapshot programme counts')
 now=set(snap['admitted_original_ids']);before=set(old['admitted_original_ids']);need(len(now)==46 and now-before==set(NEW)and before<=now,'only three added admissions')
 need(now==set(snap['measured_original_ids']),'all46 comparisons have independently accepted source inputs')
 pending=set(snap['accessible_pending_original_ids']);need(len(pending)==60 and not now&pending and now|pending==set(snap['active_original_ids'])and len(snap['active_original_ids'])==106,'complete active partition')
 need(snap['active_original_ids']==old['active_original_ids']and snap['archived_original_ids']==old['archived_original_ids']and len(snap['archived_original_ids'])==55,'no intake or retrieval change')
 rows={x['original_id']:x for x in active['entries']};prev={x['original_id']:x for x in prior['entries']};need(rows.keys()==prev.keys()and len(rows)==106,'exact106 catalogue records')
 changed=sorted(k for k in rows if rows[k]!=prev[k]);need(changed==programme['changed_original_records']==['F005','L016','L021','L043','L056','L079','L083'],'exact seven changed original records');need(sum(rows[k]==prev[k]for k in rows)==99,'99 unchanged original records')
 need(set(papers['original_ids'])==now-set(snap['historical_admitted_ids']),'paper overlay IDs plus retained original27 give46');need(set(NEW)<=set(s for r in papers['entries']for s in r['source_contracts']),'all three new application routes present')
 for topic in CHANGED:
  a=json.loads((public/programme['source_admissions'][topic]).read_text());need(a.get('new_question_credit',0)==0,'no new question credit')
 return dict(recovered=46,pending=60,active=106,archived=55,changed_records=changed,unchanged_records=99,public_artifacts=len(programme['public_artifacts']))

def inputs(public,allow_pending):
 b=read('bindings.json');p=read('protocol.json');need([p[k]for k in ['topic_count','original_count','active_count','pending_count','archived_count','current_factors','actual_bars']]==[19,46,106,60,55,65,149],'fixed scope')
 for r in b['public_inputs']:
  binding(dict(r,path=r['local']),HERE)
  if r['mode']=='immutable_public':binding(r,public,'public_path')
 for r in b['packet_inputs']:
  binding(dict(r,path=r['local']),HERE);base=HERE/Path(r['local']).parent
  for q in json.loads((base/'manifest.json').read_text())['exports']:binding(q,base)
 current=nonmain((public/'scripts/verify_snapshot.py').read_text());need(len(b['baseline_non_main_functions'])==104 and all(current.get(n)==h for n,h in b['baseline_non_main_functions'].items()),'104 unchanged prior-public non-main ASTs');need(len(b['integration_existing_non_main_functions'])==108 and all(current.get(n)==h for n,h in b['integration_existing_non_main_functions'].items()),'108 unchanged root integration non-main ASTs')
 for key,val in [('E_numbers','b5eba088d711072b33f830dc3b06ad833292d523fb08191b1ced4e408a9b44e3'),('E_review','3868cd8e79ca8fcb506b8ea3c0fdcd16b5681a515879a1d34a6d4fb4c4222bfc'),('E_adoption','dfca259d46839f6a04ebaff91983884fe4efd4cb959ac8746a7aad2c3343c410'),('Mix_numbers','c6a5365047aba5b466737aeaf20a42bb6e6aac27184dfdf9ef0c2eccbe0533fe'),('Mix_review','7d7f131ce35ee380f5d72935a9abeae2eb98f6903bdf77ab60d430145483ece2')]:need(sha((HERE/'inputs'/key/'manifest.json').read_bytes())==val,'exact accepted topic pin')
 programme=read('programme_binding.json')if(HERE/'programme_binding.json').exists()else None
 need(programme is not None or allow_pending,'root programme binding required for final candidate')
 if programme:
  binding(b['root_programme_binding'],HERE);programme_check(programme,public)
 return read('inputs/v12_results.json'),read('inputs/E_numbers/results.json'),read('inputs/Mix_numbers/results.json'),programme

def validate(r,old,e,m,prog):
 need(r==derive(old,e,m,prog),'complete deterministic consolidation')
 need(r['topic_count']==19 and len(r['topics'])==19 and sum(len(t['pairs'])for t in r['topics'])==46,'whole19/46 records')
 need(len(set(r['original_ids']))==46 and set(r['original_ids'])==set(old['original_ids'])|set(NEW),'exact46 distinct originals')
 for t,o in zip(r['topics'],old['topics']):
  if t['topic']not in CHANGED:need(t==o,'17 unchanged complete topic records')
  need(t['common_theory']+sum(a['application_cost']for a in t['pairs'])==t['written_denominator'],'whole common/all complete apps')
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'exact whole fraction')
  need(sum(a['source_cost']for a in t['pairs'])==t['source_sum'],'whole source sum')
  for a in t['pairs']:need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'exact conditional fraction')
  for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']:need(t.get(k)is None,'unknown/software scope '+k)
 E=next(t for t in r['topics']if t['topic']=='E');M=next(t for t in r['topics']if t['topic']=='Mixes')
 need(E['common_theory']==57473 and E['source_count']==5 and E['scoped_Lean_declarations']==42,'complete E common/source/formal boundary')
 need({a['source']:a['original_application_id']for a in E['pairs']}==e['applications'],'E exact source/actual-app routing')
 need(M['common_components']=={'U0':12615,'U1':11641}and M['application_components']['MX1']=={'A1':20788,'A2':10289},'both Mix common papers/full exceptional companion')
 need(E['whole_file_inventory']==e['whole_file_inventory']and M['whole_file_inventory']==m['whole_raw_file_inventory'],'entire accepted raw-file roles/bytes/metrics')
 need(len(M['required_files'])==2 and len(M['optional_files'])==4,'Mix required vs optional')
 return 65

def graph_check(d,folder):
 n=0
 for name,spec in specs(d).items():
  expected,H=geometry(spec);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),expected);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'PDF page extent');compare_pdf(rect,H,expected,3 if spec['whole']else 2);n+=len(expected)
  txt=''.join(p.extract_text()or''for p in PdfReader(folder/(name+'.pdf')).pages);need('awaiting matched code boundary'not in txt,'no held bar');need(('Whole topics: full common theory and all applications charged'if spec['whole']else'Conditional: whole common theory and required premises already acquired')in txt,'graph acquisition caption')
 need(n==149,'57whole+92conditional actualbars');return dict(SVG_bars=n,PDF_bars=n,whole_rows=19,conditional_rows=46)

def controls(old,e,m,prog):
 base=derive(old,e,m,prog);rejected=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):rejected.append(name);return
  raise ValueError('control not rejected '+name)
 edits=[('drop new original',lambda q:q['original_ids'].remove('L016')),('include unified A',lambda q:next(t for t in q['topics']if t['topic']=='A').__setitem__('source_count',8)),('invent F007',lambda q:next(t for t in q['topics']if t['topic']=='F')['source_ids'].append('F007')),('omit new E common',lambda q:next(t for t in q['topics']if t['topic']=='E').__setitem__('common_theory',19790)),('swap E applications',lambda q:next(a for t in q['topics']if t['topic']=='E'for a in t['pairs']if a['source']=='L079').__setitem__('original_application_id','A1')),('use old E coordinate',lambda q:next(t for t in q['topics']if t['topic']=='E').__setitem__('representation','calibrated_selected_pdf')),('forget second Mix common',lambda q:next(t for t in q['topics']if t['topic']=='Mixes').__setitem__('common_theory',12615)),('omit exceptional F005 paper',lambda q:next(a for t in q['topics']if t['topic']=='Mixes'for a in t['pairs']if a['source']=='F005').__setitem__('application_cost',20788)),('undo symmetric listing correction',lambda q:next(t for t in q['topics']if t['topic']=='Chamber').__setitem__('source_sum',35802)),('reclassify required program',lambda q:next(t for t in q['topics']if t['topic']=='E').__setitem__('program_roles','all optional')),('drop mandatory JSON',lambda q:next(t for t in q['topics']if t['topic']=='E')['whole_file_inventory'].pop()),('invent software factor',lambda q:q['topics'][0].__setitem__('including_raw_programs',2)),('zero unknown external proof',lambda q:q['topics'][0].__setitem__('external_proof_cost',0)),('change unrelated application',lambda q:q['topics'][0]['pairs'][0].__setitem__('application_cost',1)),('change pending count',lambda q:q.__setitem__('accessible_pending_originals',63)),('infer pooled factor',lambda q:q.__setitem__('pooled_factor',2)),('erase old topic history',lambda q:next(t for t in q['topics']if t['topic']=='E').pop('previous_topic_record')),('assign source GAP incorrectly',lambda q:next(t for t in q['topics']if t['topic']=='E').__setitem__('historical_source_software_attribution','Source GAP'))]
 for name,edit in edits:q=deepcopy(base);edit(q);reject(name,lambda q=q:validate(q,old,e,m,prog))
 expected,_=geometry(specs(plot_data(base))['whole_topics']);q=deepcopy(expected);q[next(iter(q))][2]*=1.1;reject('distorted actual bar',lambda:compare_geometry(q,expected))
 q=deepcopy(expected);q.pop(next(iter(q)));reject('missing actual bar',lambda:compare_geometry(q,expected));return rejected

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--allow-pending-programme',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if(HERE/'manifest.json').exists():
  for row in read('manifest.json')['exports']:binding(row,HERE)
 old,e,m,prog=inputs(a.public_root,a.allow_pending_programme);r=read('results.json');n=validate(r,old,e,m,prog)
 for f,s in csvs(r).items():need((HERE/f).read_text()==s,'exact whole19/46 CSV '+f)
 d=plot_data(r);need(d==read('plot_data.json'),'graph costs');need(render_text(r)==(HERE/'reader.tex').read_text(),'reader generation');g=graph_check(d,HERE);render=None
 if a.render:
  out=a.out/'render';out.mkdir()
  for s in specs(d).values():draw(s,out)
  need(graph_check(d,out)==g,'fresh graph geometry');(out/'reader.tex').write_text(render_text(r))
  for i in[1,2]:
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'TeX render')
  bad=[x for x in(out/'reader.log').read_text().splitlines()if any(s in x for s in ['Overfull','Underfull','Missing character','LaTeX Warning','undefined'])];need(not bad,'render diagnostics '+str(bad));txt=[p.extract_text()or''for p in PdfReader(out/'reader.pdf').pages];need(len(txt)==6,'six-page reader')
  if(HERE/'reader.pdf').exists():need(txt==[p.extract_text()or''for p in PdfReader(HERE/'reader.pdf').pages],'exact reader page text')
  render=dict(pages=6,diagnostics=bad,page_text_sha256=[sha(t.encode())for t in txt])
 report=dict(status='PASS_CANDIDATE_PENDING_PROGRAMME_BINDING'if prog is None else'PASS_AUTHOR_CONSOLIDATION_PENDING_DISTINCT_OVERVIEW_REVIEW',topics=19,originals=46,factors=n,unchanged_topics=17,unchanged_other_individuals=39,pending=60,active=106,archived=55,software_inclusive_factors=None,graphs=g,controls=controls(old,e,m,prog),reader=render,root_programme_bound=prog is not None,programme=programme_check(prog,a.public_root)if prog else None,old_nonmain_functions_unchanged=104,root_integration_nonmain_functions_unchanged=108,no_source_extraction_or_scientific_replay=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
