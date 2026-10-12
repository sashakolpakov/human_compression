#!/usr/bin/env python3
"""Portable arithmetic/whole-boundary validation from frozen adopted input vectors."""
from pathlib import Path
from copy import deepcopy
import argparse,json,math,subprocess,csv,io
from pypdf import PdfReader
from calculate import R,inputs,derive,outputs,load,need,key,sha,IDS,APPS,GROUPS,PRIMARY
from presentation import plots,tex
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf

def validate(r,p,c,roster,prior):
 need(r['source_ids']==IDS and r['applications']==APPS and r['primary_coordinate']==list(PRIMARY),'six matched originals/fixed primary')
 need(r['common_pages']=={'U_B':16,'U_B6':10}and sum(r['application_pages'].values())==30,'both full common and applications')
 need(len(r['coordinates'])==30 and r['main_exact_fractions']==210 and r['article_sensitivity_fractions']==60 and r['all_exact_fractions']==270,'all30 settings/270 fractions')
 need(r['inherited_conditional_fractions_preserved']==150 and r['prior_article_conditionals_preserved']==30,'preservation counts')
 need(all(r[k]is None for k in ['software_inclusive_factor','optional_validation_inclusive_factor','collective_conditional_factor','pooled_factor'])and all(x is None for x in r['unknown_costs'].values()),'no invented missing-cost scalar')
 need(r['partial_Lean_declarations']==14 and not r['complete_Lean']and all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'unchanged scoped science')
 need(len(r['whole_file_inventory'])==17 and len({x['file']['sha256']for x in r['whole_file_inventory']})==17,'17 exact whole contents')
 need([r['whole_file_groups'][g]['files']for g in GROUPS]==[8,2,5,2],'correct required/optional/driver/formal roles')
 need(r['extra_stored_required_data']==[]and r['printed_program_pages']=={'CODE':7,'CODE6':7},'complete separate alternatives')
 acq=r['required_acquisition'];need(len(acq['required_or_auxiliary_whole_files'])==8 and acq['optional_validation_not_required']and acq['no_sibling_application_premise']and acq['conservative_complete_topic_union_not_minimal_graph'],'conditional acquisition scope')
 old={key(x):x for x in prior['rows']};cnt=pres=article=0
 for x in r['coordinates']:
  source=sum(x['source_costs'].values());common=sum(x['common_components'].values());app=sum(x['applications'].values());need(source==x['source_sum']and common==x['whole_common']and app==x['application_sum']and common+app==x['whole_written'],'full sum arithmetic')
  pairs=[(x['written'],source,common+app)]+[(x['conditional'][k],x['source_costs'][k],x['applications'][k])for k in IDS]
  z=x['article_only_sensitivity'];need(z['all_replacement_costs_unchanged']and z['other_five_conditionals_unchanged'],'article boundary')
  pairs.extend([(z['written'],source-x['source_costs']['L040']+z['L040_article_cost'],common+app),(z['L040_conditional'],z['L040_article_cost'],x['applications']['L040'])])
  for f,a,b in pairs:
   need(f['numerator']==a and f['denominator']==b and f['reduced_numerator']*b==f['reduced_denominator']*a and math.gcd(f['reduced_numerator'],f['reduced_denominator'])==1,'exact rational identity');cnt+=1
  for k in IDS[:-1]:need(x['conditional'][k]==old[key(x)]['conditional'][k],'exact old conditional');pres+=1
  need(z['L040_conditional']==old[key(x)]['article_only_sensitivity']['L040_conditional'],'prior article conditional');article+=1
  sw=x['separate_software'];need(sw['software_inclusive_factor']is None and sw['historical_source_software_cost']is None and sw['raw_and_printed_are_alternatives'],'symmetric separated software')
  need(x['acquisition'][0]['replacement_written']==x['common_components']['U_B'] and x['acquisition'][0]['source_written']==0 and x['acquisition'][-1]['replacement_written']==common+app and x['acquisition'][-1]['source_written']==source,'whole acquisition endpoints')
  need(len(x['acquisition'])==8 and x['acquisition'][6]['acquire']==['U_B6'] and x['acquisition'][6]['replacement_written']-x['acquisition'][5]['replacement_written']==x['common_components']['U_B6'] and x['acquisition'][6]['source_written']==x['acquisition'][5]['source_written'],'separate new common acquisition')
 need((cnt,pres,article)==(270,150,30),'full fraction/preservation counts')
 need(r==derive(p,c,roster,prior),'all accepted integer vectors, metadata, source representation, whole inventories and decimal strings')
 return cnt

def controls(r,p,c,roster,prior):
 rejected=[]
 def reject(name,fn):
  q=deepcopy(r);fn(q)
  try:validate(q,p,c,roster,prior)
  except(ValueError,KeyError,TypeError):rejected.append(name);return
  raise ValueError('accepted mutation '+name)
 tests=[('omit old whole common',lambda q:q['coordinates'][0]['common_components'].update(U_B=0)),('omit new supplement',lambda q:q['coordinates'][0]['common_components'].update(U_B6=0)),('omit sixth application',lambda q:q['applications'].pop('L047')),('double-charge source alias',lambda q:q['coordinates'][0].update(source_sum=1)),('change whole numerator',lambda q:q['coordinates'][0]['written'].update(numerator=1)),('wrong reduced numerator',lambda q:q['coordinates'][0]['written'].update(reduced_numerator=1)),('old conditional changed',lambda q:q['coordinates'][0]['conditional']['N001'].update(denominator=1)),('new conditional altered',lambda q:q['coordinates'][0]['conditional']['L047'].update(denominator=1)),('article sensitivity changes denominator',lambda q:q['coordinates'][0]['article_only_sensitivity']['written'].update(denominator=1)),('drop primary cover',lambda q:q['primary']['source_costs'].update(L040=51113)),('N001 PDF invented zero',lambda q:q['unknown_costs'].update(N001_original_PDF=0)),('software-inclusive scalar',lambda q:q.update(software_inclusive_factor=1)),('source software zero',lambda q:q['unknown_costs'].update(historical_source_software=0)),('graphics zero',lambda q:q['unknown_costs'].update(graphics_and_layout=0)),('optional now required',lambda q:q['required_acquisition'].update(optional_validation_not_required=False)),('roster file demoted',lambda q:q['whole_file_inventory'][13].update(mathematical_premise=False)),('prune whole program',lambda q:q['whole_file_inventory'].pop()),('erase raw bytes',lambda q:q['whole_file_groups'][GROUPS[0]].update(literal_bytes=0)),('printed and raw additive',lambda q:q['coordinates'][0]['separate_software'].update(raw_and_printed_are_alternatives=False)),('drop sensitivity',lambda q:q['coordinates'].pop()),('change primary',lambda q:q.update(primary_coordinate=['calibrated_selected','NFC','whitespace_tokens'])),('free added common acquisition',lambda q:q['coordinates'][0]['acquisition'][6].update(replacement_written=q['coordinates'][0]['acquisition'][5]['replacement_written'])),('free initial acquisition',lambda q:q['primary_acquisition'][0].update(replacement_written=0)),('omit final source',lambda q:q['primary_acquisition'][-1].update(source_written=124906)),('invent full formalization',lambda q:q.update(complete_Lean=True)),('new source credit',lambda q:q.update(new_source_credit=1)),('claim all Table3 regenerated',lambda q:q['source_scope'].update(L047='All Table3 assertions regenerated.')),('historical one-sided factor current',lambda q:q.update(prior_software_inclusive_values='Current comparisons')),('old common page omission',lambda q:q['common_pages'].update(U_B=15))]
 for name,fn in tests:reject(name,fn)
 return rejected

def graphcheck(folder,expect):
 result={}
 for stem,count in [('costs',23),('cumulative',15)]:
  want=expect[stem]['expected_rectangles'];actual=svg_rectangles((folder/(stem+'.svg')).read_text());compare_geometry(actual,want);rect,H=pdf_rectangles(folder/(stem+'.pdf'));compare_pdf(rect,H,want,0);need(len(actual)==len(rect)==count,'complete actual bars '+stem);rejected=[]
  for label,fn in [('distorted width',lambda a:a[next(iter(a))].__setitem__(2,1)),('missing bar',lambda a:a.pop(next(iter(a)))),('shifted baseline',lambda a:a[next(iter(a))].__setitem__(0,0))]:
   q=deepcopy(actual);fn(q)
   try:compare_geometry(q,want)
   except ValueError:rejected.append(label)
   else:raise ValueError('accepted SVG mutation')
  q=deepcopy(rect);q[0][3]+=1
  try:compare_pdf(q,H,want,0)
  except ValueError:rejected.append('distorted PDF height')
  else:raise ValueError('accepted PDF mutation')
  result[stem]=dict(SVG_bars=len(actual),PDF_bars=len(rect),controls=rejected)
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 p,c,roster,prior=inputs();r=load(R/'results.json');cnt=validate(r,p,c,roster,prior)
 for name,text in outputs(derive(p,c,roster,prior)).items():need((R/name).read_text()==text,'complete table '+name);(a.out/name).write_text(text)
 t=tex(r);need(t==(R/'reader.tex').read_text(),'all exact reader values');need('whole-topic expansion' in t and 'not achieved whole-topic compression' in t,'candid primary expansion');(a.out/'reader.tex').write_text(t)
 expect=plots(r,a.out);need(expect==load(R/'plot_data.json'),'same graph expectations');g=graphcheck(a.out,expect);need(graphcheck(R,expect)==g,'saved graph geometry')
 render=None
 if a.render:
  for j in [1,2]:
   proc=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'render{j}.log').write_text(proc.stdout+proc.stderr);need(proc.returncode==0,'clean reader build')
  bad=[l for l in(a.out/'reader.log').read_text().splitlines()if any(s in l for s in ['Overfull','Underfull','Missing character','LaTeX Warning'])];need(not bad,'reader diagnostics '+str(bad));texts=[p.extract_text()or''for p in PdfReader(a.out/'reader.pdf').pages];need(len(texts)==4,'four complete reader pages');need(texts==[p.extract_text()or''for p in PdfReader(R/'reader.pdf').pages],'all final page texts exact');render=dict(pages=4,diagnostics=[],page_text_sha256=[sha(s.encode())for s in texts])
 report=dict(status='PASS_AUTHOR_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',coordinates=30,exact_fractions=cnt,main_fractions=210,article_sensitivity_fractions=60,prior_conditionals=150,prior_article_conditionals=30,adopted_cells={'main_documents':480,'article_sensitivity':30,'raw':170},whole_raw_files=17,CSV_rows={n:len(list(csv.DictReader(io.StringIO((a.out/n).read_text()))))for n in ['document_costs.csv','fractions.csv','acquisition.csv','raw_files.csv']},controls=controls(r,p,c,roster,prior),graphs=g,reader=render,no_source_extraction_or_scientific_replay=True,software_inclusive_factor=None)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
