#!/usr/bin/env python3
"""Check complete records, exact comparisons, CSV/TeX and actual SVG/PDF bars."""
from pathlib import Path
import argparse,copy,json,hashlib
from pypdf import PdfReader
import build,plotting,reader,geometry_checks as geom
H=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError('OVERVIEW37_CHECK: '+m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=H);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
 if (H/'manifest.json').exists():
  for x in json.loads((H/'manifest.json').read_text())['exports']:
   b=(H/x['path']).read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'frozen file')
 p,data=build.load_inputs(a.public_root);r=build.make(data,p);now=json.loads((a.packet/'results.json').read_text());need(now==r,'exact regenerated records');build.validate(now,data['previous_results'])
 for n,t in plotting.csv_text(r).items():need((a.packet/n).read_text()==t,'complete CSV')
 need((a.packet/'summary.tex').read_text()==reader.tex(r),'complete reader text');specs={k:plotting.plot_spec(r,k) for k in ['whole_topics','conditional_1','conditional_2']};need(json.loads((a.packet/'plot_data.json').read_text())==specs,'all complete plot ownership')
 svg=pdf=0;geometry={}
 for k,s in specs.items():
  expected,height=geom.expected_geometry(s);geometry[k]=expected;geom.compare_geometry(geom.svg_rectangles((a.packet/(k+'.svg')).read_bytes()),expected);rows,h=geom.pdf_rectangles(a.packet/(k+'.pdf'));need(geom.near(h,height),'actual PDF dimensions');geom.compare_pdf(rows,h,expected,3 if k=='whole_topics' else 2);svg+=len(expected);pdf+=len(expected)
 pages=[pg.extract_text() or '' for pg in PdfReader(a.packet/'summary.pdf').pages];need(len(pages)==6,'complete six-page reader');text=' '.join('\n'.join(pages).split())
 for token in ['thirty-seven','L037','Rank contraction','fourteen','unknown','raw untrimmed PDFs','1.471','0.888','whole local theory','independent acceptance','no overlap is deducted']:
  need(token in text,'reader scope '+token)
 controls=[]
 def reject(n,call):
  try:call()
  except (ValueError,KeyError,TypeError):controls.append(n);return
  raise ValueError('accepted invalid control '+n)
 edits=[('alter prior topic',lambda x:x['topics'][0].update(common_theory=1)),('omit L037',lambda x:x['topics'].pop()),('free old B theory',lambda x:x['topics'][-1].update(old_Topic_B_common_free_premise=True)),('omit local common cost',lambda x:x['topics'][-1].update(common_theory=0)),('omit final application references',lambda x:x['topics'][-1].update(applications_sum=10100)),('truncate printed program',lambda x:x['topics'][-1].update(printed_program_cost=1)),('add both program alternatives',lambda x:x['topics'][-1].update(raw_program_alternative=5426)),('omit prior acquisition',lambda x:x['topics'][-1]['conditional_prepaid'].update(full_common=0)),('unknown graphics zero',lambda x:x['topics'][-1].update(complete_graphic_cost=0)),('pooled factor',lambda x:x.update(pooled_factor=1.2)),('cross-topic discount',lambda x:x.update(cross_topic_deduplication=True)),('whole161 complete',lambda x:x.update(all_registry_manuscripts_completed=True)),('credit from measurement',lambda x:x.update(new_source_credit=1)),('drop numerical acceptance',lambda x:x.update(pending_numerical_acceptance=['RankContraction'])),('self-admit overview',lambda x:x.update(pending_overview_review=False)),('change raw primary',lambda x:x['topics'][-1].update(representation='calibrated_selected_pdf')),('omit whole driver inventory',lambda x:x['topics'][-1]['separate_raw_inventory'].update(drivers=0)),('close source conjecture',lambda x:x['topics'][-1].update(scientific_boundary='all questions solved'))]
 for name,edit in edits:
  z=copy.deepcopy(r);edit(z);reject(name,lambda z=z:build.validate(z,data['previous_results']))
 k='whole_topics';actual=geom.svg_rectangles((a.packet/(k+'.svg')).read_bytes());first=next(iter(actual));bad=copy.deepcopy(actual);bad[first][2]*=.7;reject('distorted source SVG bar',lambda:geom.compare_geometry(bad,geometry[k]));bad=copy.deepcopy(actual);bad.pop(first);reject('omitted SVG bar',lambda:geom.compare_geometry(bad,geometry[k]))
 preserved={t['topic']:hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest() for t in r['topics'][:-1]}
 comparisons=sum(1+int(t['including_printed_programs'] is not None)+int(t['including_raw_programs'] is not None)+int(t.get('including_optional_validation') is not None)+len(t['pairs']) for t in r['topics']);need(comparisons==81,'all comparisons')
 result=dict(status='PASS',topics=15,proposed_measured_originals=37,unchanged_complete_topic_records=14,preserved_topic_canonical_hashes=preserved,exact_primary_comparisons=81,SVG_cost_rectangles=svg,PDF_cost_rectangles=pdf,reader_pages=6,reader_page_hashes=[hashlib.sha256(x.encode()).hexdigest() for x in pages],controls=controls,public_changes=False,source_extraction_repeated=False,numerical_acceptance_pending=[],overview_acceptance_pending=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print('PASS15 topics37 originals81 comparisons;',svg,'SVG/PDF rectangles;',len(controls),'controls')
if __name__=='__main__':main()
