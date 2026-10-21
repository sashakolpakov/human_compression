#!/usr/bin/env python3
"""Check exact records, data-inclusive alternatives, CSV/reader and vector bars."""
from pathlib import Path
import argparse,copy,json,hashlib,csv
from pypdf import PdfReader
import build,plotting,reader,geometry_checks as geom
H=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError('OVERVIEW40_CHECK: '+m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=H);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists()and not a.out.is_symlink(),'fresh report')
 if(H/'manifest.json').exists():
  for x in json.loads((H/'manifest.json').read_text())['exports']:
   path=Path(x['path']);need(not path.is_absolute()and '..'not in path.parts,'safe frozen export');b=(H/path).read_bytes();need(len(b)==x['bytes']and hashlib.sha256(b).hexdigest()==x['sha256'],'frozen exact file')
 p,data=build.load_inputs(a.public_root);r=build.make(data,p);now=json.loads((a.packet/'results.json').read_text());need(now==r,'exact regenerated records');build.validate(now,data['previous_results'])
 for n,t in plotting.csv_text(r).items():need((a.packet/n).read_text()==t,'exact complete CSV')
 need((a.packet/'summary.tex').read_text()==reader.tex(r),'literal reader formulas and scope');specs={k:plotting.plot_spec(r,k)for k in ['whole_topics','conditional_1','conditional_2']};need(json.loads((a.packet/'plot_data.json').read_text())==specs,'complete plot ownership')
 svg=pdf=0;geometry={}
 for k,s in specs.items():
  expected,height=geom.expected_geometry(s);geometry[k]=expected;geom.compare_geometry(geom.svg_rectangles((a.packet/(k+'.svg')).read_bytes()),expected);rows,h=geom.pdf_rectangles(a.packet/(k+'.pdf'));need(geom.near(h,height),'actual PDF dimensions');geom.compare_pdf(rows,h,expected,3 if k=='whole_topics'else 2);svg+=len(expected);pdf+=len(expected)
 need(svg==pdf==165,'all165 actual rectangles')
 pages=[z.extract_text()or''for z in PdfReader(a.packet/'summary.pdf').pages];need(len(pages)==6,'six complete reader pages');text=' '.join('\n'.join(pages).split())
 for token in ['forty original','L084','L095','L073','Locally projective','Mathieu','fifteen','unknown','raw untrimmed PDFs','28,574','48,686','83,965','39,150','0.707','0.332','both code alternatives','independent acceptance','no overlap is deducted','geo[]','48-page predecessor']:
  need(token in text,'reader scope '+token)
 controls=[]
 def reject(n,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):controls.append(n);return
  raise ValueError('accepted invalid control '+n)
 edits=[('alter old admitted object',lambda x:x['topics'][0].update(common_theory=1)),('omit L073',lambda x:x['topics'].pop()),('free earlier umbrella',lambda x:x['topics'][-1].update(old_umbrella_free_premise=True)),('omit LP common tables',lambda x:x['topics'][-2]['common_components'].pop('whole_common_tables')),('omit Mathieu class tables',lambda x:x['topics'][-1]['application_components']['MC1'].pop('all_class_tables')),('omit Mathieu source-row paper',lambda x:x['topics'][-1]['application_components']['MC1'].pop('all_source_row_dispositions')),('hide LP data in printed code',lambda x:x['topics'][-2].update(printed_program_cost=51269,mandatory_data_cost=0)),('omit data from printed denominator',lambda x:x['topics'][-1].update(including_printed_programs=build.ratio(13736,41378+31244))),('omit data from raw denominator',lambda x:x['topics'][-2].update(including_raw_programs=build.ratio(26490,37464+22104))),('drop mandatory data field',lambda x:x['topics'][-1].pop('mandatory_data_cost')),('truncate literal JSON bytes',lambda x:x['topics'][-1].update(mandatory_data_literal_bytes=100)),('add both program alternatives',lambda x:x['topics'][-1].update(raw_program_alternative=61733)),('omit printed conditional data prepayment',lambda x:x['topics'][-1]['conditional_prepaid'].update(mandatory_data=0)),('omit raw conditional data prepayment',lambda x:x['topics'][-2]['conditional_raw_alternative_prepaid'].update(mandatory_data=0)),('unknown graphic cost zero',lambda x:x['topics'][-1].update(complete_graphic_cost=0)),('pooled factor',lambda x:x.update(pooled_factor=1.2)),('cross-topic discount',lambda x:x.update(cross_topic_deduplication=True)),('whole161 complete',lambda x:x.update(all_registry_manuscripts_completed=True)),('new credit from measurement',lambda x:x.update(new_source_credit=1)),('drop distinct numerical acceptance',lambda x:x.update(pending_numerical_acceptance=['MathieuCensus'])),('self-admit overview',lambda x:x.update(pending_overview_review=False)),('change Mathieu raw primary',lambda x:x['topics'][-1].update(representation='calibrated_selected_pdf')),('zero separate driver inventory',lambda x:x['topics'][-2]['separate_raw_inventory'].update(drivers=0)),('invent full geo identities',lambda x:x['topics'][-1].update(scientific_boundary='Recovered every original historical identity')),('omit source reference page',lambda x:x['topics'][-2]['entire_source_pages'].update(L095=14)),('turn older unknown data into zero',lambda x:x['topics'][0].update(mandatory_data_cost=0))]
 for name,edit in edits:
  z=copy.deepcopy(r);edit(z);reject(name,lambda z=z:build.validate(z,data['previous_results']))
 k='whole_topics';actual=geom.svg_rectangles((a.packet/(k+'.svg')).read_bytes());first=next(iter(actual));bad=copy.deepcopy(actual);bad[first][2]*=.7;reject('distorted actual SVG bar',lambda:geom.compare_geometry(bad,geometry[k]));bad=copy.deepcopy(actual);bad.pop(first);reject('omitted actual SVG bar',lambda:geom.compare_geometry(bad,geometry[k]))
 preserved={t['topic']:hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()for t in r['topics'][:-2]}
 comparisons=sum(1+int(t['including_printed_programs']is not None)+int(t['including_raw_programs']is not None)+int(t.get('including_optional_validation')is not None)+len(t['pairs'])for t in r['topics']);need(comparisons==90,'all90 comparison records')
 csvrows=sum(len(list(csv.DictReader((a.packet/n).open(newline=''))))for n in ['topics.csv','applications.csv']);need(csvrows==57,'all57 CSV rows')
 result=dict(status='PASS',topics=17,proposed_measured_originals=40,unchanged_complete_topic_records=15,preserved_topic_canonical_hashes=preserved,exact_primary_comparisons=90,CSV_rows=57,SVG_cost_rectangles=svg,PDF_cost_rectangles=pdf,reader_pages=6,reader_page_hashes=[hashlib.sha256(x.encode()).hexdigest()for x in pages],controls=controls,public_changes=False,source_extraction_repeated=False,numerical_acceptance_pending=[],overview_acceptance_pending=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print('PASS17 topics40 originals90 comparisons57 CSV rows;',svg,'SVG/PDF rectangles;',len(controls),'controls')
if __name__=='__main__':main()
