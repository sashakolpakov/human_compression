#!/usr/bin/env python3
"""Replay the exact additive status transformation and rendered cost geometry."""
from pathlib import Path
from copy import deepcopy
import argparse,csv,io,json,subprocess,time
from pypdf import PdfReader
from build import HERE,read,need,sha,derive,csvs,plot_data,HELD
from reader import render_text
from plotting import specs,geometry,draw
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def binding(row,root,key='path'):
 p=Path(row[key]);need(not p.is_absolute()and'..'not in p.parts,'safe bound path');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact binding '+str(p));return b

def verify_inputs(public):
 p=read('protocol.json');need([p[k]for k in ['recovered_originals','active_accessible_originals','pending_accessible_originals','archived_originals','available_whole_topics','available_conditionals']]==[43,106,63,55,16,40],'exact programme/current totals')
 need(all(p[k]is None for k in ['software_inclusive_factors','optional_validation_inclusive_factors','original_software_cost','pooled_factor']),'all inclusive/unknown coordinates null')
 need(p['whole_common_theory_paid_per_topic'] and not p['cross_topic_discount'] and not p['source_extraction'] and not p['mathematical_replay'] and not p['new_factors'],'no new extraction or factor/discount')
 for r in read('baseline_bindings.json')['public_inputs']:
  local=(HERE/r['local']).read_bytes();need(len(local)==r['bytes']and sha(local)==r['sha256'],'immutable copied historical observation');need(local==binding(r,public,'public_path'),'exact published overview input')
 s=read('screening.json');binding(s['root_listing_adoption'],HERE);
 need(s['root_listing_adoption']['sha256']=='21b87530003ef6295e7ef945e3d81bb89229b9c05bdee323549f0f4fa5997ab6','distinct listing root adoption')
 for r in read('inputs/listing_root_review/manifest.json')['exports']:binding(r,HERE/'inputs/listing_root_review')
 binding(s['audit_manifest'],HERE);m=read('inputs/listing_audit/manifest.json')
 need(s['audit_manifest']['sha256']=='eb605489814f8bc43f10445d34101159053a3da99f987925316fb0a6c7b9be5a','final audit not draft')
 for row in m['exports']:binding(row,HERE/'inputs/listing_audit')
 old=read('inputs/historical_results.json');disp=read('inputs/listing_audit/comparison_dispositions.json');rs=disp['comparisons'];need(len(rs)==62,'all exact audit dispositions')
 expected=[]
 for t in old['topics']:
  expected.append(('whole_topic',t['topic'],t['source_ids'],t['written'],t['topic']in HELD))
  for a in t['pairs']:expected.append(('conditional_application',t['topic'],[a['source']],a['conditional'],a['source']in HELD.values()))
 for a,(kind,topic,ids,value,held)in zip(rs,expected):
  need((a['kind'],a['topic'],a['source_ids'],a['historical_value'])==(kind,topic,ids,value),'exact documentary comparison route')
  status='WITHHOLD_PENDING_SYMMETRIC_REMEASUREMENT'if held else 'RETAIN_UNCHANGED_MANUSCRIPT_COORDINATE';need(a['current_status']==status,'exact audit-held set')
 review=read('inputs/listing_audit/review.json');need(review['findings']['whole_topics_to_withhold']==s['held_topics']and review['findings']['individuals_to_withhold']==s['held_sources'],'actual audit controls held rows')
 topics=read('inputs/listing_audit/topic_screen.json')['topics'];need(len(topics)==18,'bounded eighteen-topic screen')
 for t in topics:need(s['evidence_by_topic'][t['topic']]==dict(audit_record=t['topic'],basis=t['basis'],audit_status=t['status']),'precise positive or held screening basis')
 need(next(t for t in old['topics']if t['topic']=='F')['embedded_validation_listings_screened'],'earlier F explicit screen, not inferred')
 return old,s

def validate_result(c,old,screen):
 expected=derive(old,screen);need(c==expected,'complete current/historical observations and status transformation')
 need(sum(t['written']is not None for t in c['topics'])==16,'sixteen current whole topics')
 need(sum(a['conditional']is not None for t in c['topics']for a in t['pairs'])==40,'forty current conditional rows')
 need(c['original_ids']==old['original_ids']and len(c['original_ids'])==43,'all43 recoveries unchanged')
 for t,prior in zip(c['topics'],old['topics']):
  for k in ['source_sum','common_theory','applications_sum','written_denominator','source_ids','program_roles','printed_program_cost','raw_program_alternative']:
   need(t.get(k)==prior.get(k),'no cost or mandatory-role modification')
  need(t['common_theory']+t['applications_sum']==t['written_denominator'],'whole common paid once')


def graph_check(data,root):
 n=0;held=0
 for name,spec in specs(data).items():
  e,H=geometry(spec);svg=(root/(name+'.svg')).read_text();compare_geometry(svg_rectangles(svg),e)
  r,pdfH=pdf_rectangles(root/(name+'.pdf'));need(abs(H-pdfH)<1e-6,'physical graph height');compare_pdf(r,H,e,3 if spec['whole']else 2)
  nh=sum(r['held']for r in spec['rows']);need(svg.count('awaiting matched code boundary')==nh,'all actual held SVG labels');pt=''.join(x.extract_text()or''for x in PdfReader(root/(name+'.pdf')).pages);need(pt.count('awaiting matched code boundary')==nh,'all actual held PDF labels')
  need(('Whole topics: full common theory and all applications charged' if spec['whole']else 'Conditional: whole common theory and required premises already acquired') in pt,'standalone graph scope')
  n+=len(e);held+=nh
 need(n==128 and held==6,'128current bars/six held rows');return dict(svg_bars=n,pdf_bars=n,held_rows_without_bars=held)


def controls(old,screen):
 c=derive(old,screen);done=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):done.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL_NOT_REJECTED: '+name)
 for name,edit in [
  ('restore held whole factor',lambda r:next(t for t in r['topics']if t['topic']=='Chamber').__setitem__('written',deepcopy(next(t for t in old['topics']if t['topic']=='Chamber')['written']))),
  ('restore held conditional factor',lambda r:next(a for t in r['topics']for a in t['pairs']if a['source']=='N006').__setitem__('conditional',dict(numerator=1,denominator=1,exact_fraction='1',decimal='1'))),
  ('withdraw unaffected N016',lambda r:next(a for t in r['topics']for a in t['pairs']if a['source']=='N016').__setitem__('conditional',None)),
  ('alter source observation',lambda r:r['topics'][0].__setitem__('source_sum',0)),
  ('free whole common theory',lambda r:r['topics'][0].__setitem__('common_theory',0)),
  ('relabel required code optional',lambda r:next(t for t in r['topics']if t['topic']=='Chamber').__setitem__('program_roles','All optional')),
  ('invent software-inclusive ratio',lambda r:r['topics'][0].__setitem__('including_raw_programs',dict(decimal='2'))),
  ('invent historical software zero',lambda r:r['topics'][0].__setitem__('historical_software_cost',0)),
  ('lose historical held factor',lambda r:next(t for t in r['topics']if t['topic']=='Operations').__setitem__('historical_written',None)),
  ('change recovery count',lambda r:r.__setitem__('original_manuscript_count',40)),
  ('change pending programme',lambda r:r.__setitem__('accessible_pending_originals',66)),
  ('missing application',lambda r:r['topics'][0]['pairs'].pop()),
  ('invent pooled ratio',lambda r:r.__setitem__('pooled_factor',1)),
 ]:
  q=deepcopy(c);edit(q);reject(name,lambda q=q:validate_result(q,old,screen))
 q=deepcopy(screen);q['unaffected_topics_screened'].remove('E');reject('silence treated as positive screen',lambda:derive(old,q))
 q=deepcopy(screen);q['held_listing_roles']['N006']='optional_validation';reject('source proof implementation relabeled optional',lambda:derive(old,q))
 d=plot_data(c);q=deepcopy(d);next(r for r in q['whole_topics']if r['held'])['values']={'source':0,'common':0,'applications':0};reject('held row replaced by zero bars',lambda:need(q==plot_data(c),'graph values exact'))
 spec=specs(d)['whole_topics'];e,_=geometry(spec);q=deepcopy(e);first=next(iter(q));q[first][2]*=1.01;reject('distorted visible bar',lambda:compare_geometry(q,e))
 return dict(status='PASS',negative_controls=len(done),results=done)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);start=time.monotonic();export_count=0
 if(HERE/'manifest.json').exists():
  for r in read('manifest.json')['exports']:binding(r,HERE);export_count+=1
 old,screen=verify_inputs(a.public_root);c=read('results.json');validate_result(c,old,screen)
 for name,text in csvs(c).items():need((HERE/name).read_text()==text,'all19/43 CSV values/statuses')
 data=read('plot_data.json');need(data==plot_data(c),'no hidden current held bars');need((HERE/'reader.tex').read_text()==render_text(c),'exact reader generated from carried values')
 con=controls(old,screen);(a.out/'controls.json').write_text(json.dumps(con,indent=2)+'\n');graph_result=None;render_result=None
 if a.render:
  out=a.out/'render';out.mkdir()
  for spec in specs(data).values():draw(spec,out)
  graph_result=graph_check(data,out);(out/'reader.tex').write_text(render_text(c))
  for i in[1,2]:
   p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=out,capture_output=True,text=True);(a.out/f'reader_pass{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'reader render')
  log=(out/'reader.log').read_text();diag=[l for l in log.splitlines()if any(x in l for x in ['Overfull','Underfull','Missing character','LaTeX Warning','undefined'])];need(not diag,'reader diagnostics '+str(diag))
  txt=[p.extract_text()or''for p in PdfReader(out/'reader.pdf').pages];need(len(txt)==2,'compact two-page reader')
  if(HERE/'reader.pdf').exists():need(txt==[p.extract_text()or''for p in PdfReader(HERE/'reader.pdf').pages],'reader page text equal')
  render_result=dict(pages=len(txt),diagnostics=diag,page_text_sha256=[sha(t.encode())for t in txt])
 if(HERE/'whole_topics.svg').exists():graph_result=graph_check(data,HERE)
 report=dict(status='PASS',export_bindings=export_count,topics=19,originals=43,current_available_factors=56,held_whole_topics=3,held_conditionals=3,all_old_costs_and_roles_unchanged=True,recovered_pending=[43,63],software_inclusive_factors=None,negative_controls=con['negative_controls'],graphs=graph_result,reader=render_result,no_extraction_or_math_runs=True,elapsed_seconds=round(time.monotonic()-start,3));(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
