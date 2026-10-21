#!/usr/bin/env python3
"""Check exact records, data-inclusive alternatives, CSV/reader and vector bars."""
from pathlib import Path
import argparse,copy,json,hashlib,csv
from pypdf import PdfReader
import build,plotting,reader,geometry_checks as geom
H=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError('OVERVIEW42_CHECK: '+m)
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
 need(svg==pdf==179,'all179 actual rectangles')
 pages=[z.extract_text()or''for z in PdfReader(a.packet/'summary.pdf').pages];need(len(pages)==6,'six complete reader pages');text=' '.join('\n'.join(pages).split())
 for token in ['forty-two original','F005','Mixes','eighteen','unknown','raw untrimmed PDFs','28,574','48,686','both code alternatives','independent acceptance','no overlap is deducted','geo[]','48-page predecessor','1.322','0.967','0.991','1.858','counterproof','64 pending','55 unavailable','two generic','three final problems remain unanswered','106 accessible','Singleton topics remain included']:
  need(token in text,'reader scope '+token)

 controls=[]
 def reject(n,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):controls.append(n);return
  raise ValueError('accepted invalid control '+n)
 edits=[
 ('alter old admitted object',lambda x:x['topics'][0].update(common_theory=1)),
 ('omit F005',lambda x:x['topics'].pop()),
 ('free earlier theory',lambda x:x['topics'][-1].update(prior_theory_free=True)),
 ('omit common paper',lambda x:x['topics'][-1]['common_components'].pop('whole_common')),
 ('omit exceptional application',lambda x:x['topics'][-1]['application_components']['MX1'].pop('exceptional_application')),
 ('free prior correction claim',lambda x:x['topics'][-1].update(prior_correction_free=True)),
 ('wrong printed denominator',lambda x:x['topics'][-1].update(including_printed_programs=build.ratio(57753,50800))),
 ('wrong raw denominator',lambda x:x['topics'][-1].update(including_raw_programs=build.ratio(57753,51000))),
 ('add both program alternatives',lambda x:x['topics'][-1].update(raw_program_alternative=30633)),
 ('drop conditional programme acquisition',lambda x:x['topics'][-1]['conditional_prepaid'].update(full_declared_printed_programs=0)),
 ('drop raw programme acquisition',lambda x:x['topics'][-1]['conditional_raw_alternative_prepaid'].update(full_declared_raw_programs=0)),
 ('unknown graphic cost zero',lambda x:x['topics'][-1].update(complete_graphic_cost=0)),
 ('pooled factor',lambda x:x.update(pooled_factor=1.2)),
 ('cross-topic discount',lambda x:x.update(cross_topic_deduplication=True)),
 ('whole active corpus complete',lambda x:x.update(all_registry_manuscripts_completed=True)),
 ('restore161 active scope',lambda x:x.update(registry_manuscripts=161)),
 ('restore55 retrieval targets',lambda x:x.update(active_retrieval=55)),
 ('drop historical archive',lambda x:x.update(archived_unavailable=0)),
 ('new overview credit',lambda x:x.update(new_source_credit=1)),
 ('drop distinct numerical acceptance',lambda x:x.update(pending_numerical_acceptance=['Mixes'])),
 ('self-admit overview',lambda x:x.update(pending_overview_review=False)),
 ('change raw primary',lambda x:x['topics'][-1].update(representation='calibrated_selected_pdf')),
 ('zero separate driver inventory',lambda x:x['topics'][-1]['separate_raw_inventory'].update(drivers=0)),
 ('invent literal source recovery',lambda x:x['topics'][-1].update(scientific_boundary='All literal statements are true')),
 ('claim final problems answered',lambda x:x['topics'][-1].update(unanswered_final_problems=0)),
 ('omit source reference page',lambda x:x['topics'][-1].update(entire_source_pages=20)),
 ('turn older unknown data into zero',lambda x:x['topics'][0].update(mandatory_data_cost=0)),
 ('remove inherited mandatory JSON',lambda x:next(t for t in x['topics']if t['topic']=='MathieuCensus').update(mandatory_data_cost=0)),
 ('claim full formalization',lambda x:x['topics'][-1].update(full_source_formalized=True)),
 ('stale programme status',lambda x:x['programme_snapshot'].update(status='CURRENT_PROGRAMME_41_ADMITTED_ORIGINALS_106_ACCESSIBLE')),
 ('infer counts from measurement',lambda x:x.update(programme_counts_not_inferred_from_measurement=False)),
 ('drop accessible pending original',lambda x:x['programme_snapshot'].update(accessible_pending_complete_recovery=63))]

 for name,edit in edits:
  z=copy.deepcopy(r);edit(z);reject(name,lambda z=z:build.validate(z,data['previous_results']))
 for name,edit in [
  ('snapshot drops a pending ID',lambda z:z['current_corpus_snapshot']['accessible_pending_original_ids'].pop()),
  ('snapshot restores retrieval',lambda z:z['current_corpus_snapshot'].update(pending_source_retrieval=55)),
  ('archive drops an ID',lambda z:z['current_corpus_snapshot']['archived_original_ids'].pop()),
  ('scope excludes singleton topics',lambda z:z['scope_admission'].update(singletons_excluded=10)),
  ('admission makes exception free',lambda z:z['new_admission']['primary'].update(application_cost=20788)),
  ('catalogue removes companion',lambda z:z['current_catalogue'].update(entries=[q for q in z['current_catalogue']['entries']if q.get('application_id')!='MX1_exceptional']))]:
  z=copy.deepcopy(data);edit(z);reject(name,lambda z=z:build.verify_publication(p,z))

 k='whole_topics';actual=geom.svg_rectangles((a.packet/(k+'.svg')).read_bytes());first=next(iter(actual));bad=copy.deepcopy(actual);bad[first][2]*=.7;reject('distorted actual SVG bar',lambda:geom.compare_geometry(bad,geometry[k]));bad=copy.deepcopy(actual);bad.pop(first);reject('omitted actual SVG bar',lambda:geom.compare_geometry(bad,geometry[k]))
 preserved={t['topic']:hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()for t in r['topics'][:-1]}
 comparisons=sum(1+int(t['including_printed_programs']is not None)+int(t['including_raw_programs']is not None)+int(t.get('including_optional_validation')is not None)+len(t['pairs'])for t in r['topics']);need(comparisons==98,'all98 comparison records')
 csvrows=sum(len(list(csv.DictReader((a.packet/n).open(newline=''))))for n in ['topics.csv','applications.csv']);need(csvrows==61,'all61 CSV rows')
 result=dict(status='PASS',topics=19,proposed_measured_originals=42,unchanged_complete_topic_records=18,preserved_topic_canonical_hashes=preserved,exact_primary_comparisons=98,CSV_rows=61,SVG_cost_rectangles=svg,PDF_cost_rectangles=pdf,reader_pages=6,reader_page_hashes=[hashlib.sha256(x.encode()).hexdigest()for x in pages],controls=controls,public_changes=False,source_extraction_repeated=False,numerical_acceptance_pending=[],overview_acceptance_pending=True)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print('PASS19 topics42 originals98 comparisons61 CSV rows;',svg,'SVG/PDF rectangles;',len(controls),'controls')
if __name__=='__main__':main()
