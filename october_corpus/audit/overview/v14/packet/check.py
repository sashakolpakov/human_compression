#!/usr/bin/env python3
"""Exact current consolidation, independent integer invariants and literal bars."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import argparse,ast,json,subprocess
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,CHANGED,NEW,fraction
from reader import render_text
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def binding(row,root):
 p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'safe binding');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p));return b

def nonmain(text):return{n.name:sha(ast.dump(n,include_attributes=False).encode())for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
def programme_check(prog,public):
 for row in prog['public_artifacts']:binding(row,public)
 need(prog['counts']==dict(topics=18,recovered=47,pending=59,active=106,archived=55),'programme counts');need(prog['new_originals']==NEW,'only F007')
 def doc(key):return json.loads((public/prog[key]).read_text())
 snap=doc('snapshot');old=doc('previous_corpus_pointer');active=doc('active_catalogue');prior=doc('previous_active_catalogue');papers=doc('current_paper_pointer');pointer=doc('current_corpus_pointer')
 need(pointer==dict(snap,snapshot=next(x for x in prog['public_artifacts']if x['path']==prog['snapshot'])),'exact current corpus pointer')
 need([snap[k]for k in ['originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','archived_unavailable_originals']]==[106,106,47,59,55],'snapshot programme counts')
 now=set(snap['admitted_original_ids']);before=set(old['admitted_original_ids']);need(len(now)==47 and now-before=={'F007'}and before<=now,'only F007 admitted')
 need(now==set(snap['measured_original_ids']),'47 measured originals');pending=set(snap['accessible_pending_original_ids']);need(len(pending)==59 and not now&pending and now|pending==set(snap['active_original_ids']),'47/59 partition')
 need(snap['active_original_ids']==old['active_original_ids']and snap['archived_original_ids']==old['archived_original_ids']and len(snap['active_original_ids'])==106 and len(snap['archived_original_ids'])==55,'no intake/retrieval change')
 rows={x['original_id']:x for x in active['entries']};prev={x['original_id']:x for x in prior['entries']};need(rows.keys()==prev.keys()and len(rows)==106,'exact106 records')
 changed=sorted(k for k in rows if rows[k]!=prev[k]);need(changed==prog['changed_original_records']==['F005','F007','F013','F016','L012','L016','L032','L034','L035','L128','N009'],'eleven changed records');need(sum(rows[k]==prev[k]for k in rows)==95,'95 unchanged original records')
 need(set(papers['original_ids'])==now-set(snap['historical_admitted_ids']),'overlay plus historical principal originals');need('F007'in {s for r in papers['entries']for s in r['source_contracts']},'new application catalogue route')
 for k,path in prog['source_admissions'].items():
  a=json.loads((public/path).read_text());need(a.get('new_question_credit',0)==0,'no question credit')
 return dict(recovered=47,pending=59,active=106,archived=55,changed_records=changed,unchanged_records=95,public_artifacts=len(prog['public_artifacts']))

def inputs(public):
 b=read('bindings.json');p=read('protocol.json');need([p[k]for k in ['expected_topics','expected_recovered_originals','fixed_active_originals','expected_accessible_pending_originals','fixed_archived_originals','expected_total_factors']]==[18,47,106,59,55,65],'fixed precount protocol')
 for r in b['public_inputs']:
  raw=binding(r,public)
  if 'local'in r:need((HERE/r['local']).read_bytes()==raw,'exact local/public accepted input')
 packet_exports=0
 for r in b['public_packets']:
  m=json.loads(binding(r,public));base=(public/r['path']).parent
  for q in m['exports']:binding(q,base);packet_exports+=1
 current=nonmain((public/'scripts/verify_snapshot.py').read_text());need(len(b['baseline_non_main_functions'])==110 and all(current.get(n)==h for n,h in b['baseline_non_main_functions'].items()),'110 prior non-main ASTs unchanged')
 prog=read('programme_binding.json');programme_check(prog,public)
 return read('inputs/v13_results.json'),read('inputs/A_results.json'),read('inputs/Mix_results.json'),prog,packet_exports

def validate(r,old,a,m,prog):
 need(r==derive(old,a,m,prog),'complete deterministic consolidation');need(r['topic_count']==18 and len(r['topics'])==18 and sum(len(t['pairs'])for t in r['topics'])==47,'18whole47individual')
 need(set(r['original_ids'])==set(old['original_ids'])|{'F007'}and len(r['original_ids'])==len(set(r['original_ids']))==47,'47 distinct originals')
 oldby={t['topic']:t for t in old['topics']};unchanged=0;individuals=0
 for t in r['topics']:
  if t['topic']not in CHANGED:need(t==oldby[t['topic']],'complete untouched topic record');unchanged+=1;individuals+=len(t['pairs'])
  need(t['common_theory']+sum(x['application_cost']for x in t['pairs'])==t['written_denominator'],'whole common and every application');need(t['written']==fraction(t['source_sum'],t['written_denominator']),'whole exact fraction');need(sum(x['source_cost']for x in t['pairs'])==t['source_sum'],'source sum')
  for x in t['pairs']:need(x['conditional']==fraction(x['source_cost'],x['application_cost']),'conditional exact fraction')
  for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']:need(t.get(k)is None,'unknown/software scope '+k)
 need((unchanged,individuals)==(16,36),'16/36 unchanged records');need('Affine'not in{t['topic']for t in r['topics']},'no duplicate Affine')
 A=next(t for t in r['topics']if t['topic']=='A');M=next(t for t in r['topics']if t['topic']=='Mixes')
 need(A['common_theory']==66140 and A['applications_sum']==110576 and A['source_sum']==246570,'accepted whole A closure');need(M['common_components']=={'U':12615,'U1':11641,'U2':10501},'all three Mix common papers');need(M['application_components']=={'F005':{'A1':20788,'A2':10289},'L016':{'A3':15125},'F007':{'A4':13841,'A5':8650}},'every full Mix companion')
 need(A['whole_file_inventory']==a['whole_file_inventory']and M['whole_file_inventory']==m['whole_file_inventory'],'complete whole-file inventories')
 need(Counter(x['role']for x in A['whole_file_inventory'])=={'required_program_or_data':11,'inherited_auxiliary':3,'current_operational_driver':2,'partial_formal_evidence':14},'A exact roles')
 need(len(M['required_files'])==2 and len(M['optional_files'])==6 and M['required_printed_coverage']['REQ']==M['required_files'],'both required files printed; six optional')
 for t,n in[(A,a),(M,m)]:
  need(t['written']['decimal']==n['primary']['written']['decimal'],'accepted whole fraction reproduced')
  for x in t['pairs']:need(x['conditional']['decimal']==n['primary']['conditional'][x['source']]['decimal'],'accepted conditional reproduced')
 return 65

def graph_check(d,folder):
 count=0
 for name,spec in specs(d).items():
  expected,H=geometry(spec);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),expected);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'PDF extent');compare_pdf(rect,H,expected,3 if spec['whole']else 2);count+=len(expected)
  txt=''.join(p.extract_text()or''for p in PdfReader(folder/(name+'.pdf')).pages);need('awaiting matched code boundary'not in txt,'no held bars');need(('Whole topics: full common theory and all applications charged'if spec['whole']else'Conditional: whole common theory and required premises already acquired')in txt,'caption')
 need(count==148,'54whole94conditional actual bars');return dict(SVG_bars=count,PDF_bars=count,whole_rows=18,conditional_rows=47)

def controls(old,a,m,prog):
 base=derive(old,a,m,prog);bad=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):bad.append(name);return
  raise ValueError('control not rejected '+name)
 def topic(q,key):return next(x for x in q['topics']if x['topic']==key)
 edits=[('omit F007',lambda q:q['original_ids'].remove('F007')),('retain duplicate Affine',lambda q:q['topics'].append(deepcopy(next(x for x in old['topics']if x['topic']=='Affine')))),('free old A common',lambda q:topic(q,'A').__setitem__('common_theory',0)),('change A coordinate',lambda q:topic(q,'A').__setitem__('primary_coordinate','raw_untrimmed/NFC/characters_without_whitespace')),('omit third Mix common',lambda q:topic(q,'Mixes')['common_components'].pop('U2')),('omit exceptional F005',lambda q:topic(q,'Mixes')['application_components']['F005'].pop('A2')),('omit F007 companion',lambda q:topic(q,'Mixes')['application_components']['F007'].pop('A5')),('demote required certificate',lambda q:topic(q,'Mixes').__setitem__('program_roles','all optional')),('false REQ one-file claim',lambda q:topic(q,'Mixes')['required_printed_coverage']['REQ'].pop()),('drop A data file',lambda q:topic(q,'A')['whole_file_inventory'].pop(1)),('change another topic',lambda q:topic(q,'E').__setitem__('common_theory',1)),('reverse listing restoration',lambda q:topic(q,'Chamber').__setitem__('source_sum',35802)),('invent software scalar',lambda q:topic(q,'A').__setitem__('including_raw_programs',1)),('zero unknown cost',lambda q:topic(q,'A').__setitem__('external_proof_cost',0)),('pooled factor',lambda q:q.__setitem__('pooled_factor',2)),('wrong pending',lambda q:q.__setitem__('accessible_pending_originals',60)),('new question credit',lambda q:q.__setitem__('new_question_credit',1)),('erase Affine history',lambda q:topic(q,'A').pop('previous_affine_record'))]
 for name,edit in edits:
  q=deepcopy(base);edit(q);reject(name,lambda q=q:validate(q,old,a,m,prog))
 expected,_=geometry(specs(plot_data(base))['whole_topics']);q=deepcopy(expected);q[next(iter(q))][2]*=1.1;reject('distorted bar',lambda:compare_geometry(q,expected));q=deepcopy(expected);q.pop(next(iter(q)));reject('missing bar',lambda:compare_geometry(q,expected));return bad

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh out');a.out.mkdir(parents=True)
 if(HERE/'manifest.json').exists():
  for row in read('manifest.json')['exports']:binding(row,HERE)
 old,u,m,prog,exports=inputs(a.public_root);r=read('results.json');n=validate(r,old,u,m,prog)
 for f,s in csvs(r).items():need((HERE/f).read_text()==s,'exact CSV '+f)
 d=plot_data(r);need(d==read('plot_data.json'),'graph integer data');need(render_text(r)==(HERE/'reader.tex').read_text(),'reader source');g=graph_check(d,HERE);render=None
 if a.render:
  out=a.out/'render';out.mkdir()
  for s in specs(d).values():draw(s,out)
  need(graph_check(d,out)==g,'fresh graphs');(out/'reader.tex').write_text(render_text(r))
  for i in[1,2]:
   proc=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'TeX render')
  bad=[s for s in(out/'reader.log').read_text().splitlines()if any(x in s for x in ['Overfull','Underfull','Missing character','LaTeX Warning','undefined'])];need(not bad,'diagnostics '+str(bad));txt=[p.extract_text()or''for p in PdfReader(out/'reader.pdf').pages];need(len(txt)==6,'six-page reader')
  if(HERE/'reader.pdf').exists():need(txt==[p.extract_text()or''for p in PdfReader(HERE/'reader.pdf').pages],'exact per-page text')
  render=dict(pages=6,diagnostics=bad,page_text_sha256=[sha(t.encode())for t in txt])
 report=dict(status='PASS_AUTHOR_V14_PENDING_DISTINCT_REVIEW',topics=18,originals=47,factors=n,unchanged_topics=16,unchanged_other_individuals=36,pending=59,active=106,archived=55,software_inclusive_factors=None,graphs=g,controls=controls(old,u,m,prog),reader=render,programme=programme_check(prog,a.public_root),old_nonmain_functions_unchanged=110,accepted_numerical_packet_exports_verified=exports,no_source_extraction_or_scientific_replay=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
