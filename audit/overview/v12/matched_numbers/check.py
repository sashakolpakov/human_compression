#!/usr/bin/env python3
import argparse, copy, hashlib, json, math, subprocess
from pathlib import Path
from pypdf import PdfReader
from calculate import load,need,derive,outputs
from presentation import plots,reader
from geometry_checks import svg_rectangles,compare_geometry,pdf_rectangles,compare_pdf
R=Path(__file__).resolve().parent
PIN='ee065a6a7a1533e6157ca3a495c0d6ec4a544608c89cb9c46abc5cd17707b55a'
def sha(b):return hashlib.sha256(b).hexdigest()
def bindings():
 p=load(R/'protocol.json');need(sha((R/'protocol.json').read_bytes())==PIN,'precalculation protocol')
 need(load(R/'protocol_freeze.json')['sha256']==PIN,'precalculation pin')
 for b in p['bindings']:
  raw=(R/b['path']).read_bytes();need(len(raw)==b['bytes'] and sha(raw)==b['sha256'],'adopted binding '+b['path'])
  if Path(b['path']).name!='manifest.json':
   row=next(x for x in load(R/Path(b['path']).parent/'manifest.json')['exports'] if x['path']==Path(b['path']).name)
   need((row['bytes'],row['sha256'])==(b['bytes'],b['sha256']),'actual manifest membership')
 if (R/'manifest.json').exists():
  for b in load(R/'manifest.json')['exports']:
   raw=(R/b['path']).read_bytes();need(len(raw)==b['bytes'] and sha(raw)==b['sha256'],'frozen own '+b['path'])
 return p
def validate(d,p,counts,baseline):
 need(d['software_inclusive_factors'] is None and d['historical_source_software_cost'] is None and d['full_graphics_external_proofs_and_formalization'] is None,'software/external unknown')
 need((d['programme_recovered'],d['programme_pending'],d['new_source_credit'],d['new_question_credit'])==(43,63,0,0),'programme unchanged')
 need(d['document_cells']==600 and d['whole_file_count']==46 and len(d['whole_file_roster'])==46,'all counts and whole files')
 need(set(d['topics'])==set(p['topics']),'exact three topics');total=0
 for name,t in d['topics'].items():
  boundary=p['topics'][name];need(t['scope']==boundary,'complete scientific scope');need(len(t['coordinates'])==(40 if name=='Operations' else 30),'all sensitivities')
  for key,c in t['coordinates'].items():
   v=c['document_costs'];source=sum(v[x] for x in boundary['sources']);common=sum(v[x] for x in boundary['common']);apps={s:sum(v[x] for x in bundle) for s,bundle in boundary['applications'].items()}
   need(c['common_sum']==common and c['whole_written']==common+sum(apps.values()) and c['source_sum']==source,'whole U and all bundles')
   fs=[(c['written'],source,c['whole_written'])]+[(c['conditional'][s],v[s],apps[s]) for s in boundary['sources']]
   for f,a,b in fs:
    need((f['source_cost'],f['replacement_cost'])==(a,b) and f['numerator']*b==f['denominator']*a and math.gcd(f['numerator'],f['denominator'])==1,'exact reduced fraction');total+=1
   need(c['software_inclusive_factor'] is None and c['historical_source_software_cost'] is None,'no software factor')
 need(total==d['exact_fractions']==310,'310 exact fractions')
 need(d==derive(p,counts,baseline),'all adopted metric cells, role records and outputs exact')
 return total
def controls(d,p,counts,baseline):
 result=[]
 def reject(name,fn):
  q=copy.deepcopy(d);fn(q)
  try:validate(q,p,counts,baseline)
  except (ValueError,KeyError):result.append(name);return
  raise ValueError('accepted mutation '+name)
 def row(q,name='Operations'):return q['topics'][name]['coordinates'][q['topics'][name]['primary_coordinate']]
 reject('drop whole common',lambda q:row(q).update(common_sum=0))
 reject('omit N006 companion',lambda q:q['topics']['Operations']['scope']['applications']['N006'].pop())
 reject('restore unmatched source cost',lambda q:row(q)['document_costs'].update(N006=row(q)['pre_listing_document_costs']['N006']))
 reject('inflate whole numerator',lambda q:row(q)['written'].update(numerator=1))
 reject('inflate conditional denominator',lambda q:row(q)['conditional']['N006'].update(denominator=1))
 reject('free Chamber common',lambda q:row(q,'Chamber').update(whole_written=sum(row(q,'Chamber')['application_bundle_costs'].values())))
 reject('lose text-only sensitivity',lambda q:q['topics']['Operations']['coordinates'].pop(next(x for x in q['topics']['Operations']['coordinates'] if x.startswith('text_only'))))
 reject('text-only source cost altered',lambda q:next(c for k,c in q['topics']['Operations']['coordinates'].items() if k.startswith('text_only'))['document_costs'].update(N006=0))
 reject('software-inclusive factor invented',lambda q:q.update(software_inclusive_factors=1))
 reject('historical software treated as zero',lambda q:q.update(historical_source_software_cost=0))
 reject('graphics cost treated as zero',lambda q:q.update(full_graphics_external_proofs_and_formalization=0))
 reject('omit required decoder',lambda q:q['whole_file_roster'].pop(next(i for i,r in enumerate(q['whole_file_roster']) if r['category']=='required_drivers')))
 reject('rewrite program role',lambda q:q['whole_file_roster'][0].update(category='optional'))
 reject('change inherited whole bytes',lambda q:q['whole_file_roster'][0]['file'].update(bytes=0))
 reject('alter an unchanged app',lambda q:row(q)['document_costs'].update(A0=1))
 reject('change primary policy',lambda q:q['topics']['Chamber'].update(primary_coordinate='raw_without_listings/NFKC/whitespace_tokens'))
 reject('invent source credit',lambda q:q.update(new_source_credit=3))
 reject('alter recovery count',lambda q:q.update(programme_recovered=46))
 reject('lose other conditional',lambda q:row(q)['conditional'].pop('N005'))
 reject('discard historical observation',lambda q:row(q)['pre_listing_document_costs'].update(N006=0))
 return result
def check_graph(folder,expected):
 actual=svg_rectangles((folder/'costs.svg').read_text());compare_geometry(actual,expected)
 rects,H=pdf_rectangles(folder/'costs.pdf');compare_pdf(rects,H,expected,0)
 rejected=[]
 for name,fn in [('distorted cost bar',lambda x:x[next(iter(x))].__setitem__(2,1)),('missing common bar',lambda x:x.pop('bar-common-Operations'))]:
  q=copy.deepcopy(actual);fn(q)
  try:compare_geometry(q,expected)
  except ValueError:rejected.append(name)
  else:raise ValueError('accepted chart mutation')
 return {'SVG_bars':len(actual),'PDF_bars':len(rects),'controls':rejected}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 p=bindings();counts=load(R/'inputs/input/author_counts.json');baseline=load(R/'inputs/input/baseline_documents.json');d=load(R/'results.json');n=validate(d,p,counts,baseline)
 for name,text in outputs(derive(p,counts,baseline)).items():need((R/name).read_text()==text,'regenerated '+name);(a.out/name).write_text(text)
 text=reader(d);need(text==(R/'reader.tex').read_text(),'reader derivation');(a.out/'reader.tex').write_text(text)
 g=plots(d,a.out);need(g==load(R/'plot_data.json'),'cost rectangles');chart=check_graph(a.out,g['rectangles']);need(check_graph(R,g['rectangles'])==chart,'saved vector geometry')
 render=None
 if a.render:
  for i in [1,2]:
   x=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(a.out.resolve()),'reader.tex'],cwd=a.out,capture_output=True,text=True);(a.out/f'pass{i}.log').write_text(x.stdout+x.stderr);need(x.returncode==0,'reader compile')
  log=(a.out/'reader.log').read_text();bad=[s for s in log.splitlines() if any(k in s for k in ['Missing character','Overfull','Underfull','LaTeX Warning'])];need(not bad,'diagnostics '+str(bad))
  txt=[x.extract_text() or '' for x in PdfReader(a.out/'reader.pdf').pages];need(len(txt)==3,'three reader pages')
  if (R/'reader.pdf').exists():need(txt==[x.extract_text() or '' for x in PdfReader(R/'reader.pdf').pages],'reader page equality')
  render={'pages':3,'diagnostics':bad,'page_text_sha256':[sha(t.encode()) for t in txt]}
 report={'status':'AUTHOR_ARITHMETIC_PASS_PENDING_DISTINCT_REVIEW','protocol_sha256':PIN,'topics':3,'originals':6,'standard_coordinates_per_topic':30,'Operations_extra_coordinates':10,'exact_fractions':n,'input_cells_unchanged':600,'whole_file_roster_unchanged':46,'controls':controls(d,p,counts,baseline),'charts':chart,'reader':render,'software_inclusive_factors':None,'programme':[43,63],'no_primary_extraction_or_scientific_replay':True};(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
