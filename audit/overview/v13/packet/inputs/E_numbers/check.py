#!/usr/bin/env python3
"""Portable arithmetic, boundary, CSV, graph and reader replay."""
from pathlib import Path
import argparse, copy, hashlib, json, math, subprocess, sys
from pypdf import PdfReader
from calculate import load,need,derive,outputs,key
from presentation import plots,tex
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
R=Path(__file__).resolve().parent
POLICY='bfcacc505a3b39a4031ed47c6e751e8bbc236e71fd5a9a4644f88c4c02e54369'
def sha(b):return hashlib.sha256(b).hexdigest()
def binding_checks():
 p=load(R/'protocol.json');need(sha((R/'protocol.json').read_bytes())==POLICY,'fixed precalculation protocol')
 need(load(R/'protocol_freeze.json')['sha256']==POLICY,'precalculation freeze')
 for b in p['bindings']:
  data=(R/b['path']).read_bytes();need(len(data)==b['bytes'] and sha(data)==b['sha256'],'adopted input binding '+b['path'])
  folder=Path(b['path']).parent;manifest=load(R/folder/'manifest.json')
  if Path(b['path']).name!='manifest.json':
   row=next(x for x in manifest['exports'] if x['path']==Path(b['path']).name)
   need((row['bytes'],row['sha256'])==(b['bytes'],b['sha256']),'input export membership')
 if (R/'manifest.json').exists():
  for b in load(R/'manifest.json')['exports']:
   data=(R/b['path']).read_bytes();need(len(data)==b['bytes'] and sha(data)==b['sha256'],'own frozen export '+b['path'])
 return p
def validate(d,p,counts):
 need(d['software_inclusive_factors'] is None and d['historical_source_software_cost'] is None,'unknown software factors')
 need(all(v is None for v in d['unknown_costs'].values()),'unknown external costs')
 need(d['source_ids']==p['source_order'] and d['applications']==p['applications'],'exact original/application pairing')
 need(len(d['coordinates'])==30 and d['coordinate_count']==30 and d['exact_fraction_count']==180,'all coordinates')
 need(d['source_registration_or_question_credit']==0,'no credit')
 need(d['whole_common_pages']==20 and d['source_pages']==67,'full paper pages')
 need(len(d['whole_file_inventory'])==25,'complete required/optional/driver/formal roster')
 for g,count in [('required_programs',6),('required_data',1),('optional_validation',6),('operational_drivers',5),('partial_formal',7)]:need(d['whole_file_group_costs'][g]['files']==count,'role '+g)
 checked=0
 for v in p['variants']:
  for n in p['normalizations']:
   for u in p['units']:
    c=d['coordinates'][key(v,n,u)];costs={k:x['metrics'][v][n][u] for k,x in counts['documents'].items()}
    need(c['document_costs']==costs,'whole component vector')
    source=sum(costs[k] for k in p['source_order']);apps=sum(costs[k] for k in p['applications'].values());whole=costs['U']+apps
    need((c['source_sum'],c['application_sum'],c['whole_common'],c['whole_written'])==(source,apps,costs['U'],whole),'whole U and all applications charged')
    pairs=[(c['written'],source,whole)]+[(c['conditional'][k],costs[k],costs[a]) for k,a in p['applications'].items()]
    for f,a,b in pairs:
     need(f['source_cost']==a and f['replacement_cost']==b and f['numerator']*b==f['denominator']*a,'exact fraction')
     need(math.gcd(f['numerator'],f['denominator'])==1,'reduced fraction');checked+=1
    need(c['separate_software']['software_inclusive_factor'] is None and c['separate_software']['historical_source_software_cost'] is None,'separate software not comparison')
 need(checked==180,'180 exact fractions')
 need(d==derive(p,counts),'all raw costs, acquisition and decimal representations')
 return checked
def controls(d,p,counts):
 rejected=[]
 def reject(name,change):
  q=copy.deepcopy(d);change(q)
  try:validate(q,p,counts)
  except (ValueError,KeyError):rejected.append(name);return
  raise ValueError('negative control accepted '+name)
 pk=d['primary_coordinate']
 reject('drop common cost',lambda q:q['coordinates'][pk].update(whole_common=0))
 reject('exclude an application',lambda q:q['coordinates'][pk].update(application_sum=q['coordinates'][pk]['application_sum']-1))
 reject('change source numerator',lambda q:q['coordinates'][pk]['written'].update(source_cost=1))
 reject('alter reduced numerator',lambda q:q['coordinates'][pk]['written'].update(numerator=1))
 reject('inflate conditional ratio',lambda q:q['coordinates'][pk]['conditional']['L043'].update(denominator=1))
 reject('swap A1/A2 pairings',lambda q:q['applications'].update(L079='A1'))
 reject('invent software-inclusive factor',lambda q:q.update(software_inclusive_factors=1.2))
 reject('unknown source software zero',lambda q:q.update(historical_source_software_cost=0))
 reject('unknown graphics zero',lambda q:q['unknown_costs'].update(full_graphics_formula_layout=0))
 reject('drop required JSON',lambda q:q['whole_file_group_costs']['required_data'].update(files=0))
 reject('required program relabeled optional',lambda q:q['whole_file_group_costs']['required_programs'].update(files=5))
 reject('drop optional whole file',lambda q:q['whole_file_inventory'].pop(next(i for i,r in enumerate(q['whole_file_inventory']) if r['group']=='optional_validation')))
 reject('omit coordinate',lambda q:q['coordinates'].pop(next(iter(q['coordinates']))))
 reject('change a source count',lambda q:q['coordinates'][pk]['document_costs'].update(L043=1))
 reject('acquisition begins with free U',lambda q:q['primary_acquisition'][0].update(replacement_written=0))
 reject('claim new source credit',lambda q:q.update(source_registration_or_question_credit=2))
 reject('alter raw required bytes',lambda q:q['whole_file_group_costs']['required_data'].update(literal_bytes=0))
 reject('replace primary by favorable sensitivity',lambda q:q.update(primary_coordinate='raw_selected/NFKC/whitespace_tokens'))
 return rejected
def graphcheck(out,expected):
 actual=svg_rectangles((out/'costs.svg').read_text());compare_geometry(actual,expected)
 rects,height=pdf_rectangles(out/'costs.pdf');compare_pdf(rects,height,expected,0)
 rejected=[]
 for name,change in [('distorted bar',lambda x:x[next(iter(x))].__setitem__(2,1)),('missing bar',lambda x:x.pop(next(iter(x))))]:
  q=copy.deepcopy(actual);change(q)
  try:compare_geometry(q,expected)
  except ValueError:rejected.append(name)
  else:raise ValueError('graph control accepted')
 return {'SVG_bars':len(actual),'PDF_bars':len(rects),'controls':rejected}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 p=binding_checks();counts=load(R/'inputs/input/author_counts.json');d=load(R/'results.json');n=validate(d,p,counts)
 for name,text in outputs(derive(p,counts)).items():need((R/name).read_text()==text,'exact output '+name);(a.out/name).write_text(text)
 reader=tex(d);need(reader==(R/'reader.tex').read_text(),'reader complete derivation');(a.out/'reader.tex').write_text(reader)
 plot=plots(d,a.out);need(plot==load(R/'plot_data.json'),'all full-document bars');g=graphcheck(a.out,plot['expected_rectangles'])
 g0=graphcheck(R,plot['expected_rectangles']);need(g0==g,'frozen graphs equal current geometry')
 rendering=None
 if a.render:
  for passno in [1,2]:
   q=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(a.out.resolve()),'reader.tex'],cwd=a.out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   (a.out/f'reader-pass{passno}.log').write_text(q.stdout);need(q.returncode==0,'reader TeX compile')
  log=(a.out/'reader.log').read_text();bad=[x for x in log.splitlines() if any(s in x for s in ['Missing character','Overfull','Underfull','LaTeX Warning'])];need(not bad,'reader diagnostics '+str(bad))
  texts=[x.extract_text() or '' for x in PdfReader(a.out/'reader.pdf').pages]
  need(len(texts)==3,'three complete reader pages')
  if (R/'reader.pdf').exists():need(texts==[x.extract_text() or '' for x in PdfReader(R/'reader.pdf').pages],'fresh reader page equality')
  rendering={'pages':len(texts),'diagnostics':bad,'page_text_sha256':[sha(t.encode()) for t in texts]}
 report={'status':'PASS_AUTHOR_ARITHMETIC_PENDING_DISTINCT_REVIEW','protocol_sha256':POLICY,'coordinates':30,'exact_fractions':n,'whole_file_inventory':25,'controls':controls(d,p,counts),'graphs':g,'reader':rendering,'software_inclusive_factors':None,'no_source_extraction_or_science_replay':True}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
