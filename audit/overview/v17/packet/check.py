#!/usr/bin/env python3
"""Portable additive overview replay with exact prior preservation and vectors."""
import argparse,copy,json,os,subprocess,tempfile
from pathlib import Path
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'overview51-cache'))
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'overview51-mpl'))
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,fraction
from reader import render_text,shown
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
NUMERIC='0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e'
REVIEW='2d071fbfffb2288d5b0d6f434b2c0d4b63fb95f187216b8d0bf5fc093397d04d'
ADOPTION='000bced9618afa28c1e4e65424f464d29ea50682eb6f0e2e95509eab065d5599'
EDITORIAL='63fd7715402444d0ec49b102ac574dd789f6d6cebe852659a9cced0d3a738de7'
def bind(root,x):
 p=Path(x['path']);need(not p.is_absolute()and'..'not in p.parts,'safe relative file')
 raw=(root/p).read_bytes();need((len(raw),sha(raw))==(x['bytes'],x['sha256']),'exact file '+str(p))
def member(manifest,export,file):
 row=next(x for x in read(manifest)['exports']if x['path']==export);raw=(HERE/file).read_bytes();need((len(raw),sha(raw))==(row['bytes'],row['sha256']),'member '+file)
def inputs():
 b=read('bindings.json')
 for x in b['inputs']:bind(HERE,x)
 f=read('protocol_freeze.json');need(sha((HERE/'protocol.json').read_bytes())==f['protocol_sha256'],'fixed additive policy');need(sha((HERE/'bindings.json').read_bytes())==read('protocol.json')['bindings_sha256'],'fixed adopted inputs')
 for manifest,export,file in [('inputs/previous_manifest.json','results.json','inputs/previous_results.json'),('inputs/numbers_manifest.json','results.json','inputs/numbers_results.json'),('inputs/numbers_manifest.json','role_clarification.json','inputs/numbers_role_clarification.json'),('inputs/numerical_review_manifest.json','review.json','inputs/numerical_review.json'),('inputs/editorial_author_manifest.json','disposition.json','inputs/editorial_disposition.json'),('inputs/editorial_review_manifest.json','decision.json','inputs/editorial_review.json')]:member(manifest,export,file)
 for name,pin in [('numbers_manifest.json',NUMERIC),('numerical_review_manifest.json',REVIEW),('numerical_root/manifest.json',ADOPTION),('editorial_root/manifest.json',EDITORIAL)]:need(sha((HERE/'inputs'/name).read_bytes())==pin,'trusted adoption chain '+name)
 for folder in ['inputs/numerical_root','inputs/editorial_root']:
  for row in read(folder+'/manifest.json')['exports']:bind(HERE/folder,row)
 a=read('inputs/numerical_root/adoption.json');need(a['status']=='ROOT_ACCEPTED_ADDITIVE_A9_NUMERICAL_COMPARISON'and a['bindings']['author']['sha256']==NUMERIC and a['bindings']['distinct_review']['sha256']==REVIEW,'actual root numerical adoption')
 editorial=read('inputs/editorial_root/adoption.json');need(editorial['status']=='ROOT_ADOPTED_EDITORIAL_DISPOSITION_AFTER_DISTINCT_READING'and editorial['accessible_original_retained']and editorial['factor']is None and not editorial['count_as_measured_mathematical_recovery'],'exact no-mathematical-result disposition')
 q=b['programme51_registration'];need(q['status']=='PENDING_ROOT_PUBLICATION_REGISTRATION'and q['binding']is None and q['expected_partition']==dict(topics=19,measured=51,mathematical_pending=54,editorial=1,active=106,archived=55),'explicit pending registration, no invented public pin')
 return read('inputs/previous_results.json'),read('inputs/numbers_results.json'),editorial
def topic(r):return next(t for t in r['topics']if t['topic']=='A')
def programme_scope(r):
 b=read('programme_scope_binding.json');raw=(HERE/b['copied_path']).read_bytes();need(len(raw)==b['bytes']and sha(raw)==b['sha256']=='f708a64e034faab55a471cba204673b81b33cef7862481babaac0460d69567ae','immutable previous programme50 snapshot')
 p=read(b['copied_path']);measured=sorted(set(p['measured_original_ids'])|{'L121'});pending=sorted(set(p['accessible_pending_original_ids'])-{'L121','L022'});editorial=['L022']
 need(len(measured)==51 and len(pending)==54 and len(editorial)==1 and set(measured)==set(r['original_ids']),'exact local51 measured and54 pending IDs')
 need(set(measured).isdisjoint(pending)and set(measured).isdisjoint(editorial)and set(pending).isdisjoint(editorial)and set(measured+pending+editorial)==set(p['active_original_ids']),'exact106 disjoint active partition')
 need(len(p['archived_original_ids'])==55 and set(p['archived_original_ids']).isdisjoint(p['active_original_ids']),'unchanged55 archived')
 return dict(status='PRIVATE_PROGRAMME51_PROPOSAL_PENDING_ROOT_REGISTRATION',baseline_snapshot=b,measured_original_ids=measured,mathematical_pending_original_ids=pending,editorial_original_ids=editorial,active_original_ids=p['active_original_ids'],archived_original_ids=p['archived_original_ids'],counts=dict(topics=19,measured=51,mathematical_pending=54,editorial=1,active=106,archived=55),new_measured_originals=['L121'],editorial_factor=None,editorial_measured_credit=0,actual_root_registration_binding=None,no_public_mutation=True)
def publication_proposal():
 if not(HERE/'proposed_latest.json').exists():return 'NOT_YET_PREPARED'
 p=read('proposed_latest.json');need(p['status']=='PROPOSED_OVERVIEW51_PENDING_ROOT_ADMISSION'and p['publication_requires_actual_root_bindings'],'unadmitted pointer proposal only')
 need((p['topics'],p['recovered_originals'],p['current_whole_factors'],p['current_conditional_factors'],p['pending_accessible_originals'],p['editorial_originals'],p['active_catalogue_originals'],p['archived_unavailable_originals'])==(19,51,19,51,54,1,106,55),'exact proposed pointer partition')
 for name in ['admission','counts_source']:need(p[name]['sha256']is None and p[name]['bytes']is None,'no invented future public binding')
 b=(HERE/'reader.pdf').read_bytes();need(p['reader']==dict(path='audit/overview/v17/packet/reader.pdf',bytes=len(b),sha256=sha(b)),'exact proposed reader route')
 plan=read('publication_plan.json');need(plan['current_registration_binding']is None and plan['current_overview_admission_binding']is None and plan['destination']=='audit/overview/v17/packet'and not plan['public_writes_performed'],'separate root publication step')
 return 'CHECKED_PENDING_ROOT_REGISTRATION'
def validate(r,old,n,e):
 need(r==derive(old,n,e),'complete deterministic additive records')
 need([t for t in r['topics']if t['topic']!='A']==[t for t in old['topics']if t['topic']!='A'],'all18 other whole-topic objects exact')
 before={a['source']:a for t in old['topics']for a in t['pairs']};after={a['source']:a for t in r['topics']for a in t['pairs']};need(all(after[k]==v for k,v in before.items())and set(after)-set(before)=={'L121'},'all50 prior individual records exact')
 need(len(r['topics'])==19 and len(r['original_ids'])==len(set(r['original_ids']))==51,'19topics51 originals')
 need(r['active_originals']==106 and r['archived_unavailable_originals']==55 and r['accessible_pending_originals']==54 and r['editorial_original_count']==1 and 51+54+1==106,'full active partition')
 for t in r['topics']:
  need(t['source_count']==len(t['pairs'])==len(t['source_ids'])and t['source_ids']==[a['source']for a in t['pairs']],'all source/application pairs')
  need(t['source_sum']==sum(a['source_cost']for a in t['pairs']),'complete source sum')
  need(t['common_theory']+sum(a['application_cost']for a in t['pairs'])==t['written_denominator'],'whole common plus all complete apps')
  need(t['written']==fraction(t['source_sum'],t['written_denominator']),'exact whole fraction')
  for a in t['pairs']:need(a['conditional']==fraction(a['source_cost'],a['application_cost']),'exact conditional fraction')
  need(all(t.get(k)is None for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','external_proof_cost','complete_graphic_cost','full_formalization_cost']),'symmetric software and unknown-cost limits')
 t=topic(r);need((t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'])==(273937,66140,136125,202265),'exact adopted A9 costs')
 need(t['whole_file_inventory']==n['whole_file_inventory']and t['whole_file_group_costs']==n['whole_file_group_costs']and t['required_whole_file_count']==20 and t['required_original_bytes']==105850,'complete45 raw files and20 required contents')
 need(t['complete_enlarged_printed_program_representation']is None and t['printed_program_cost']is None and t['entire_program_pages']is None,'old printed subset is not enlarged complete code')
 need(t['no_sibling_application_dependency']and not t['full_source_formalized']and t['added_Lean_declarations']==6,'scope and acquisition')
 need('L022'not in r['original_ids']and r['editorial_original_ids']==['L022']and r['editorial_dispositions'][0]['factor']is None and not r['editorial_dispositions'][0]['count_as_measured_mathematical_recovery'],'editorial retained with no factor/credit')
 need(r['pooled_factor']is None and r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0,'no pooled rate or self-admission')
 return 70
def graphs(folder,r):
 count=0
 for name,s in specs(plot_data(r)).items():
  e,H=geometry(s);compare_geometry(svg_rectangles((folder/(name+'.svg')).read_text()),e);rect,h=pdf_rectangles(folder/(name+'.pdf'));need(abs(H-h)<1e-6,'actual PDF canvas');compare_pdf(rect,H,e,3 if s['whole']else 2);count+=len(e)
 need(count==159,'57whole and102conditional actual rectangles');return count
def controls(r,old,n,e):
 out=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):out.append(name);return
  raise ValueError('accepted mutation '+name)
 edits=[('drop new original',lambda q:q['original_ids'].remove('L121')),('repeat L121',lambda q:q['original_ids'].append('L121')),('free whole A theory',lambda q:topic(q).__setitem__('common_theory',0)),('drop new complete application',lambda q:topic(q)['pairs'][-1].__setitem__('application_cost',0)),('change old individual',lambda q:topic(q)['pairs'][0]['conditional'].__setitem__('denominator',1)),('change unrelated topic',lambda q:q['topics'][1].__setitem__('common_theory',0)),('invent software-inclusive factor',lambda q:topic(q).__setitem__('including_raw_programs',1)),('drop required data inventory',lambda q:topic(q)['whole_file_inventory'].pop()),('claim old printed code complete',lambda q:topic(q).__setitem__('printed_program_cost',71460)),('claim full Lean',lambda q:topic(q).__setitem__('full_source_formalized',True)),('free sibling premise',lambda q:topic(q).__setitem__('no_sibling_application_dependency',False)),('include L022 as measured',lambda q:q['original_ids'].append('L022')),('editorial zero factor',lambda q:q['editorial_dispositions'][0].__setitem__('factor',0)),('editorial infinite factor',lambda q:q['editorial_dispositions'][0].__setitem__('factor','infinity')),('editorial still mathematical pending',lambda q:q.__setitem__('mathematical_pending_originals',55)),('drop editorial accessible count',lambda q:q.__setitem__('active_originals',105)),('wrong total pending',lambda q:q.__setitem__('accessible_pending_originals',55)),('invent root registration pin',lambda q:q['whole_programme_binding'].__setitem__('registration_sha256','invented')),('pooled factor',lambda q:q.__setitem__('pooled_factor',2)),('new question credit',lambda q:q.__setitem__('new_question_credit',1)),('switch primary',lambda q:topic(q).__setitem__('primary_coordinate','raw_untrimmed/NFC/characters_without_whitespace'))]
 for name,edit in edits:
  q=copy.deepcopy(r);edit(q);reject(name,lambda q=q:validate(q,old,n,e))
 for name,s in specs(plot_data(r)).items():
  want,_=geometry(s);q=copy.deepcopy(want);q[next(iter(q))][2]*=1.1;reject(name+' distorted actual bar',lambda q=q,want=want:compare_geometry(q,want));q=copy.deepcopy(want);q.pop(next(iter(q)));reject(name+' missing actual bar',lambda q=q,want=want:compare_geometry(q,want))
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 if(HERE/'manifest.json').exists():
  for x in read('manifest.json')['exports']:bind(HERE,x)
 old,n,e=inputs();r=derive(old,n,e)
 scope=programme_scope(r)
 for name,obj in [('results.json',r),('plot_data.json',plot_data(r)),('programme_scope.json',scope)]:(a.out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 for name,text in csvs(r).items():(a.out/name).write_text(text)
 for s in specs(plot_data(r)).values():draw(s,a.out)
 (a.out/'reader.tex').write_text(render_text(r));report={'status':'PASS_AUTHOR_PRIVATE_OVERVIEW51','exact_fractions':validate(r,old,n,e),'unchanged_whole_topic_objects':18,'unchanged_individual_records':50,'unchanged_prior_fractions':68,'SVG_bars':graphs(a.out,r),'PDF_bars':159,'controls':controls(r,old,n,e),'registration_status':'PENDING_ROOT_PUBLICATION_REGISTRATION','publication_proposal':publication_proposal()}
 if(HERE/'results.json').exists():
  need(read('results.json')==r and read('plot_data.json')==plot_data(r)and read('programme_scope.json')==scope,'frozen data regeneration')
  for name,text in csvs(r).items():need((HERE/name).read_text()==text,'exact full CSV '+name)
  need((HERE/'reader.tex').read_text()==render_text(r),'exact reader TeX');need(graphs(HERE,r)==159,'actual frozen geometry')
 if a.render:
  for i in[1,2]:
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'TeX build')
  bad=[s for s in(a.out/'reader.log').read_text().splitlines()if any(k in s for k in['Warning','Overfull','Underfull','Missing character'])];need(not bad,'clean diagnostics '+str(bad));texts=[p.extract_text()or''for p in PdfReader(a.out/'reader.pdf').pages];need(len(texts)==6,'six complete reader pages')
  for t in r['topics']:need(shown(t['written'])in texts[0],'actual rounded whole table')
  pairs=[a for t in r['topics']for a in t['pairs']]
  for i,row in enumerate(pairs):need(shown(row['conditional'])in texts[1 if i<26 else 2],'actual rounded conditional table')
  report['render']={'pages':6,'diagnostics':bad,'page_text_hashes':[sha(t.encode())for t in texts],'whole_table_rows':19,'conditional_table_rows':51}
  if(HERE/'reader.pdf').exists():need(texts==[p.extract_text()or''for p in PdfReader(HERE/'reader.pdf').pages],'exact frozen page text')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','fractions':70,'bars':159,'controls':len(report['controls'])}))
if __name__=='__main__':main()
