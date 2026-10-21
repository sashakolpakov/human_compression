#!/usr/bin/env python3
"""Portable exact nine-source arithmetic, prior preservation and actual vector checks."""
from pathlib import Path
from copy import deepcopy
import argparse,json,math,subprocess
from pypdf import PdfReader
from calculate import R,load,need,sha,derive,outputs,key
from presentation import plots,tex
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
POLICY='38917fe6993adcb7cbf6f67311030d7c00ee8008ff774a0947638944d142d7ec'
def bind(row,root):
 p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'safe export');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p))
def inputs():
 p=load(R/'protocol.json');need(sha((R/'protocol.json').read_bytes())==POLICY,'fixed protocol before factors');need(load(R/'protocol_freeze.json')['protocol']['sha256']==POLICY,'precalculation receipt')
 for row in p['input_bindings']:
  bind(row,R);folder=R/Path(row['path']).parent
  for e in load(folder/'manifest.json')['exports']:bind(e,folder)
 for row in p['prior_bindings']:bind(row,R)
 for e in load(R/'prior/root_adoption/manifest.json')['exports']:bind(e,R/'prior/root_adoption')
 m=load(R/'prior/numerical_manifest.json');lookup={e['path']:e for e in m['exports']}
 for name in ['results.json','protocol.json']:bind(lookup[name],R/'prior')
 adoption=load(R/'prior/root_adoption/adoption.json');need(adoption['bindings']['author']['sha256']==sha((R/'prior/numerical_manifest.json').read_bytes()),'accepted exact prior numerical packet')
 if(R/'manifest.json').exists():
  for row in load(R/'manifest.json')['exports']:bind(row,R)
 root=load(R/'inputs/input_adoption/adoption.json');need(root['status']=='ROOT_ACCEPTED_COMPLETE_ADDITIVE_INPUT_BOUNDARY'and root['numerical_comparison_authorized'],'distinct root input adoption')
 return p,load(R/'inputs/input/author_counts.json'),load(R/'inputs/input/precount/raw_inventory.json')['files'],load(R/'prior/results.json')
def validate(r,p,c,roster,prior):
 need(r['software_inclusive_factors']is None and r['historical_source_software_cost']is None and r['optional_validation_inclusive_factors']is None,'unknown software comparison')
 need(r['complete_enlarged_printed_program_representation']is None,'no enlarged printed representation')
 need(all(v is None for v in r['unknown_costs'].values())and r['full_formalization_cost']is None,'unknown costs null')
 need(r['source_ids']==p['source_order']and r['applications']==p['applications'],'exact9 original/application pairs')
 need((r['source_count'],r['source_pages'],r['whole_common_pages'],sum(r['application_pages'].values()))==(9,131,23,56),'complete source/U/app pages')
 need(len(r['coordinates'])==30 and r['coordinate_count']==30 and r['exact_fraction_count']==300 and r['inherited_conditional_fractions_preserved']==240,'all30 coordinates/300 fractions')
 need(len(r['whole_file_inventory'])==45 and len({x['file']['sha256']for x in r['whole_file_inventory']})==45,'all45 distinct whole files')
 for g,n in [('required_program_or_data',20),('inherited_auxiliary',3),('operational_runners',6),('partial_formal_files',16)]:need(r['whole_file_group_costs'][g]['files']==n,'complete role group '+g)
 checked=old=0
 for v in p['variants']:
  for n in p['normalizations']:
   for u in p['units']:
    k=key(v,n,u);x=r['coordinates'][k];cost={name:d['metrics'][v][n][u]for name,d in c['documents'].items()};need(x['document_costs']==cost,'all22 input document cells')
    source=sum(cost[z]for z in p['source_order']);app=sum(cost[z]for z in p['applications'].values());whole=cost['U']+app
    need((x['source_sum'],x['whole_common'],x['application_sum'],x['whole_written'])==(source,cost['U'],app,whole),'pay wholeU and all9 apps')
    for f,aa,bb in [(x['written'],source,whole)]+[(x['conditional'][z],cost[z],cost[a])for z,a in p['applications'].items()]:
     need(f['source_cost']==aa and f['replacement_cost']==bb and f['numerator']*bb==f['denominator']*aa and math.gcd(f['numerator'],f['denominator'])==1,'exact reduced fraction');checked+=1
    for src in prior['source_ids']:need(x['conditional'][src]==prior['coordinates'][k]['conditional'][src],'exact old conditional values');old+=1
    need(x['prior_whole_written']==prior['coordinates'][k]['written'],'unchanged prior complete comparison')
    sw=x['separate_software'];need(sw['software_inclusive_factor']is None and sw['historical_source_software_cost']is None and sw['complete_enlarged_printed_cost']is None,'partial printed code not full scalar')
 need(checked==300 and old==240 and r==derive(p,c,roster,prior),'all exact values, decimal strings, roles and ten cumulative stages');return checked
def controls(r,p,c,roster,prior):
 rejected=[];pk=r['primary_coordinate']
 def reject(name,fn):
  q=deepcopy(r);fn(q)
  try:validate(q,p,c,roster,prior)
  except(ValueError,KeyError):rejected.append(name);return
  raise ValueError('control accepted '+name)
 tests=[('drop common',lambda q:q['coordinates'][pk].update(whole_common=0)),('drop A9 application',lambda q:q['coordinates'][pk].update(application_sum=110576)),('change numerator',lambda q:q['coordinates'][pk]['written'].update(source_cost=1)),('wrong reduced fraction',lambda q:q['coordinates'][pk]['written'].update(numerator=1)),('change old conditional',lambda q:q['coordinates'][pk]['conditional']['L012'].update(denominator=1)),('change L121 conditional',lambda q:q['coordinates'][pk]['conditional']['L121'].update(denominator=1)),('wrong app pairing',lambda q:q['applications'].update(L121='A1')),('invent software-inclusive factor',lambda q:q.update(software_inclusive_factors=1)),('historical code zero',lambda q:q.update(historical_source_software_cost=0)),('graphics zero',lambda q:q['unknown_costs'].update(full_graphical_structure=0)),('missing required data',lambda q:q['whole_file_group_costs']['required_program_or_data'].update(files=19)),('drop complete raw file',lambda q:q['whole_file_inventory'].pop()),('drop sensitivity',lambda q:q['coordinates'].pop(next(iter(q['coordinates'])))),('change accepted source cost',lambda q:q['coordinates'][pk]['document_costs'].update(L035=1)),('free common acquisition',lambda q:q['primary_acquisition'][0].update(replacement_written=0)),('new source credit',lambda q:q.update(new_source_credit=1)),('drop required bytes',lambda q:q['whole_file_group_costs']['required_program_or_data'].update(literal_bytes=0)),('change primary after evaluation',lambda q:q.update(primary_coordinate='raw_selected/NFKC/whitespace_tokens')),('add code only to our written denominator',lambda q:q['coordinates'][pk].update(whole_written=q['coordinates'][pk]['whole_written']+1)),('claim full formalization',lambda q:q.update(full_formalization_cost=0)),('old appendix becomes complete enlarged code',lambda q:q.update(complete_enlarged_printed_program_representation=30)),('invent lower prior factor',lambda q:q['coordinates'][pk]['prior_whole_written'].update(numerator=1)),('erase additional common-cost explanation',lambda q:q['coordinates'][pk]['addition'].update(extra_common_cost=1)),('omit last cumulative source',lambda q:q['primary_acquisition'][-1].update(source_written=246570))]
 for name,fn in tests:reject(name,fn)
 return rejected
def graphcheck(folder,expected):
 results={}
 for stem,count in [('costs',30),('cumulative',19)]:
  want=expected[stem]['expected_rectangles'];actual=svg_rectangles((folder/(stem+'.svg')).read_text());compare_geometry(actual,want);rect,H=pdf_rectangles(folder/(stem+'.pdf'));compare_pdf(rect,H,want,0);need(len(actual)==len(rect)==count,'complete actual vector bars');rejected=[]
  for name,fn in [('distorted width',lambda x:x[next(iter(x))].__setitem__(2,1)),('missing rectangle',lambda x:x.pop(next(iter(x)))),('shifted zero baseline',lambda x:x[next(iter(x))].__setitem__(0,0))]:
   q=deepcopy(actual);fn(q)
   try:compare_geometry(q,want)
   except ValueError:rejected.append(name)
   else:raise ValueError('SVG control accepted')
  q=deepcopy(rect);q[0][3]+=1
  try:compare_pdf(q,H,want,0)
  except ValueError:rejected.append('distorted actual PDF height')
  else:raise ValueError('PDF control accepted')
  results[stem]=dict(SVG_bars=len(actual),PDF_bars=len(rect),controls=rejected)
 return results
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 p,c,roster,prior=inputs();r=load(R/'results.json');num=validate(r,p,c,roster,prior)
 for name,text in outputs(derive(p,c,roster,prior)).items():need((R/name).read_text()==text,'exact complete JSON/CSV '+name);(a.out/name).write_text(text)
 reader=tex(r);need(reader==(R/'reader.tex').read_text(),'reader generated from same exact result');(a.out/'reader.tex').write_text(reader)
 plot=plots(r,a.out);need(plot==load(R/'plot_data.json'),'actual graph expectations');g=graphcheck(a.out,plot);need(graphcheck(R,plot)==g,'saved graphs agree');render=None
 if a.render:
  for j in[1,2]:
   z=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{j}.log').write_text(z.stdout+z.stderr);need(z.returncode==0,'reader render')
  bad=[s for s in(a.out/'reader.log').read_text().splitlines()if any(x in s for x in ['Overfull','Underfull','Missing character','LaTeX Warning'])];need(not bad,'render diagnostics '+str(bad));text=[pg.extract_text()or''for pg in PdfReader(a.out/'reader.pdf').pages];need(len(text)==4,'complete four-page reader')
  if(R/'reader.pdf').exists():need(text==[pg.extract_text()or''for pg in PdfReader(R/'reader.pdf').pages],'all page text exact')
  render=dict(pages=4,diagnostics=bad,page_text_sha256=[sha(t.encode())for t in text])
 report=dict(status='PASS_AUTHOR_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',protocol_sha256=POLICY,coordinates=30,exact_fractions=num,unchanged_conditional_fractions=240,adopted_PDF_cells=660,adopted_raw_cells=450,whole_raw_files=45,controls=controls(r,p,c,roster,prior),graphs=g,reader=render,software_inclusive_factors=None,no_extraction_or_scientific_replay=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
