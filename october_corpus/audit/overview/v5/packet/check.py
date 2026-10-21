#!/usr/bin/env python3
"""Check unchanged records, complete costs and actual SVG/PDF bar geometry."""
from pathlib import Path
import argparse,copy,json,hashlib
from pypdf import PdfReader
import build,plotting,reader,geometry_checks as geom
H=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError('OVERVIEW36_CHECK: '+m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=H);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
 if (H/'manifest.json').exists():
  for x in json.loads((H/'manifest.json').read_text())['exports']:need(hashlib.sha256((H/x['path']).read_bytes()).hexdigest()==x['sha256'],'frozen file')
 p,data=build.load_inputs(a.public_root);r=build.make(data,p);now=json.loads((a.packet/'results.json').read_text());need(now==r,'exact regenerated records');build.validate(now,data['previous_results'])
 for n,t in plotting.csv_text(r).items():need((a.packet/n).read_text()==t,'complete CSV')
 need((a.packet/'summary.tex').read_text()==reader.tex(r),'complete reader text');specs={k:plotting.plot_spec(r,k) for k in ['whole_topics','conditional_1','conditional_2']};need(json.loads((a.packet/'plot_data.json').read_text())==specs,'all plot ownership')
 svg=pdf=0;geometry={}
 for k,s in specs.items():
  expected,height=geom.expected_geometry(s);geometry[k]=expected;geom.compare_geometry(geom.svg_rectangles((a.packet/(k+'.svg')).read_bytes()),expected);rows,h=geom.pdf_rectangles(a.packet/(k+'.pdf'));need(geom.near(h,height),'actual PDF dimensions');geom.compare_pdf(rows,h,expected,3 if k=='whole_topics' else 2);svg+=len(expected);pdf+=len(expected)
 pages=[p.extract_text() or '' for p in PdfReader(a.packet/'summary.pdf').pages];need(len(pages)==6,'complete six-page reader');text=' '.join('\n'.join(pages).split())
 for token in ['thirty-six','N005','N006','N007','21-page','twenty-three','seventeen finite','six validations','thirteen','unknown','Operations','independent acceptance','required decoding drivers']:
  need(token in text,'reader scope '+token)
 controls=[]
 def reject(n,call):
  try:call()
  except (ValueError,KeyError,TypeError):controls.append(n);return
  raise ValueError('accepted invalid control '+n)
 for name,edit in [('alter unaffected topic',lambda x:x['topics'][0].update(common_theory=1)),('omit N005',lambda x:next(t for t in x['topics'] if t['topic']=='Operations')['pairs'].pop(0)),('old common still used',lambda x:next(t for t in x['topics'] if t['topic']=='Operations').update(common_theory=19859)),('omit HN segment',lambda x:next(t for t in x['topics'] if t['topic']=='Operations')['application_components']['DG2'].pop('A2HN')),('omit decoder',lambda x:next(t for t in x['topics'] if t['topic']=='Operations')['raw_program_components'].update(both_required_decoders=0)),('invent complete printed appendix',lambda x:next(t for t in x['topics'] if t['topic']=='Operations').update(printed_program_cost=11725)),('no theory acquisition',lambda x:next(t for t in x['topics'] if t['topic']=='Operations')['conditional_prepaid'].update(full_common=0)),('unknown graphics zero',lambda x:next(t for t in x['topics'] if t['topic']=='Operations').update(complete_graphic_cost=0)),('pooled factor',lambda x:x.update(pooled_factor=1.2)),('cross-topic discount',lambda x:x.update(cross_topic_deduplication=True)),('whole161 completed',lambda x:x.update(all_registry_manuscripts_completed=True)),('source credit from measurement',lambda x:x.update(new_source_credit=1)),('drop numerical acceptance status',lambda x:x.update(pending_numerical_acceptance=['Operations'])),('self-admit overview',lambda x:x.update(pending_overview_review=False))]:
  z=copy.deepcopy(r);edit(z);reject(name,lambda z=z:build.validate(z,data['previous_results']))
 k='whole_topics';raw=(a.packet/(k+'.svg')).read_bytes();ar=geom.svg_rectangles(raw);first=next(iter(ar));bad=copy.deepcopy(ar);bad[first][2]*=.7;reject('distorted source SVG bar',lambda:geom.compare_geometry(bad,geometry[k]));bad2=copy.deepcopy(ar);bad2.pop(first);reject('omitted SVG bar',lambda:geom.compare_geometry(bad2,geometry[k]))
 result=dict(status='PASS',topics=14,proposed_measured_originals=36,unchanged_complete_topic_records=13,SVG_cost_rectangles=svg,PDF_cost_rectangles=pdf,reader_pages=6,reader_page_hashes=[hashlib.sha256(x.encode()).hexdigest() for x in pages],controls=controls,public_changes=False,source_extraction_repeated=False,numerical_acceptance_pending=[],overview_acceptance_pending=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
