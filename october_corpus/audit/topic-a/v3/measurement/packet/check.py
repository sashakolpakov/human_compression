#!/usr/bin/env python3
"""Portable 30-coordinate whole-topic/application arithmetic and actual graph replay."""
from pathlib import Path
from copy import deepcopy
import argparse,json,math,subprocess
from pypdf import PdfReader
from calculate import R,load,need,sha,derive,outputs,key
from presentation import plots,tex
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
POLICY='cca473960898846a57267068864ee8e081a5c133829048e0923f15aedd80dc84'
def bind(row,root):
 p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'safe export');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p))
def inputs():
 p=load(R/'protocol.json');need(sha((R/'protocol.json').read_bytes())==POLICY,'protocol fixed before factors');need(load(R/'protocol_freeze.json')['protocol']['sha256']==POLICY,'precalculation receipt')
 for row in p['input_bindings']:
  bind(row,R);folder=R/Path(row['path']).parent
  for e in load(folder/'manifest.json')['exports']:bind(e,folder)
 if(R/'manifest.json').exists():
  for row in load(R/'manifest.json')['exports']:bind(row,R)
 need(load(R/'inputs/input_adoption/adoption.json')['status']=='ROOT_ACCEPTED_UNIFIED_A_MEASUREMENT_INPUTS','root input acceptance')
 return p,load(R/'inputs/input/author_counts.json'),load(R/'inputs/input/raw_inventory.json')
def validate(r,p,c,roster):
 need(r['software_inclusive_factors']is None and r['historical_source_software_cost']is None and r['optional_validation_inclusive_factors']is None,'unknown software comparisons')
 need(all(v is None for v in r['unknown_costs'].values()) and r['full_formalization_cost'] is None,'external/formal costs unknown')
 need(r['source_ids']==p['source_order']and r['applications']==p['applications'],'exact8 original/application pairs')
 need((r['source_count'],r['source_pages'],r['whole_common_pages'],sum(r['application_pages'].values()))==(8,119,23,45),'whole paper extent')
 need(len(r['coordinates'])==30 and r['coordinate_count']==30 and r['exact_fraction_count']==270,'all30 coordinates/270 fractions')
 need(len(r['whole_file_inventory'])==30,'complete raw files')
 for g,n in [('required_program_or_data',11),('inherited_auxiliary',3),('current_operational_driver',2),('partial_formal_evidence',14)]:need(r['whole_file_group_costs'][g]['files']==n,'actual role boundary '+g)
 checked=0
 for v in p['variants']:
  for n in p['normalizations']:
   for u in p['units']:
    x=r['coordinates'][key(v,n,u)];cost={k:z['metrics'][v][n][u]for k,z in c['documents'].items()};need(x['document_costs']==cost,'all20 input PDF costs unchanged');s=sum(cost[k]for k in p['source_order']);a=sum(cost[k]for k in p['applications'].values());whole=cost['U']+a
    need((x['source_sum'],x['application_sum'],x['whole_common'],x['whole_written'])==(s,a,cost['U'],whole),'full U and all8 apps')
    for f,aa,bb in [(x['written'],s,whole)]+[(x['conditional'][k],cost[k],cost[vv])for k,vv in p['applications'].items()]:
     need(f['source_cost']==aa and f['replacement_cost']==bb and f['numerator']*bb==f['denominator']*aa and math.gcd(f['numerator'],f['denominator'])==1,'exact reduced fraction');checked+=1
    need(x['separate_software']['software_inclusive_factor']is None and x['separate_software']['historical_source_software_cost']is None,'separate code not comparison')
 need(checked==270 and r==derive(p,c,roster),'complete exact result/roster/decimals/acquisition');return checked

def controls(r,p,c,roster):
 rejected=[];pk=r['primary_coordinate']
 def reject(name,fn):
  q=deepcopy(r);fn(q)
  try:validate(q,p,c,roster)
  except(ValueError,KeyError):rejected.append(name);return
  raise ValueError('control accepted '+name)
 for name,fn in [('drop common cost',lambda q:q['coordinates'][pk].update(whole_common=0)),('exclude local paper',lambda q:q['coordinates'][pk].update(application_sum=1)),('change source numerator',lambda q:q['coordinates'][pk]['written'].update(source_cost=1)),('alter reduced factor',lambda q:q['coordinates'][pk]['written'].update(numerator=1)),('inflate conditional',lambda q:q['coordinates'][pk]['conditional']['L012'].update(denominator=1)),('swap source/app pairs',lambda q:q['applications'].update(L012='A1')),('invent software-inclusive factor',lambda q:q.update(software_inclusive_factors=1)),('original software zero',lambda q:q.update(historical_source_software_cost=0)),('graphics zero',lambda q:q['unknown_costs'].update(full_graphical_structure=0)),('required data relabeled auxiliary',lambda q:q['whole_file_group_costs']['required_program_or_data'].update(files=10)),('drop whole raw file',lambda q:q['whole_file_inventory'].pop()),('omit coordinate',lambda q:q['coordinates'].pop(next(iter(q['coordinates'])))),('source calibration changed',lambda q:q['coordinates'][pk]['document_costs'].update(L035=1)),('acquire free U',lambda q:q['primary_acquisition'][0].update(replacement_written=0)),('invent source credit',lambda q:q.update(new_source_credit=1)),('drop data bytes',lambda q:q['whole_file_group_costs']['required_program_or_data'].update(literal_bytes=0)),('change fixed primary',lambda q:q.update(primary_coordinate='raw_selected/NFKC/whitespace_tokens')),('add code to written denominator',lambda q:q['coordinates'][pk].update(whole_written=q['coordinates'][pk]['whole_written']+1)),('claim full formalization',lambda q:q['unknown_costs'].update(full_formalization=0))]:reject(name,fn)
 return rejected

def graphcheck(out,expected):
 actual=svg_rectangles((out/'costs.svg').read_text());compare_geometry(actual,expected);rect,H=pdf_rectangles(out/'costs.pdf');compare_pdf(rect,H,expected,0);need(len(actual)==len(rect)==27,'all27 actual bars');rejected=[]
 for name,fn in [('distorted bar',lambda x:x[next(iter(x))].__setitem__(2,1)),('missing bar',lambda x:x.pop(next(iter(x))))]:
  q=deepcopy(actual);fn(q)
  try:compare_geometry(q,expected)
  except ValueError:rejected.append(name)
  else:raise ValueError('graph control accepted')
 return dict(SVG_bars=len(actual),PDF_bars=len(rect),controls=rejected)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 p,c,roster=inputs();r=load(R/'results.json');n=validate(r,p,c,roster)
 for name,text in outputs(derive(p,c,roster)).items():need((R/name).read_text()==text,'exact JSON/CSV '+name);(a.out/name).write_text(text)
 reader=tex(r);need(reader==(R/'reader.tex').read_text(),'reader derivation');(a.out/'reader.tex').write_text(reader);plot=plots(r,a.out);need(plot==load(R/'plot_data.json'),'whole graph expectations');g=graphcheck(a.out,plot['expected_rectangles']);need(graphcheck(R,plot['expected_rectangles'])==g,'saved graph agrees');render=None
 if a.render:
  for i in[1,2]:
   run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{i}.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'reader render')
  bad=[s for s in(a.out/'reader.log').read_text().splitlines()if any(z in s for z in ['Overfull','Underfull','Missing character','LaTeX Warning'])];need(not bad,'render diagnostics '+str(bad));texts=[z.extract_text()or''for z in PdfReader(a.out/'reader.pdf').pages];need(len(texts)==3,'complete3page reader')
  if(R/'reader.pdf').exists():need(texts==[z.extract_text()or''for z in PdfReader(R/'reader.pdf').pages],'page text matches')
  render=dict(pages=3,diagnostics=bad,page_text_sha256=[sha(t.encode())for t in texts])
 report=dict(status='PASS_AUTHOR_ARITHMETIC_PENDING_DISTINCT_REVIEW',protocol_sha256=POLICY,coordinates=30,exact_fractions=n,unchanged_PDF_cells=600,unchanged_raw_cells=300,whole_file_inventory=30,controls=controls(r,p,c,roster),graphs=g,reader=render,software_inclusive_factors=None,no_extraction_or_scientific_replay=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
