#!/usr/bin/env python3
"""Portable input replay and semantic controls; no scientific execution or factors."""
from pathlib import Path
import argparse,json
import pypdf
import extract_inputs as h
from controls import run

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 counts,audits,controls=run(a);h.need(counts==h.load('author_counts.json'),'all 210 PDF/80 raw cells');h.need(controls==h.load('author_controls.json'),'all 36 semantic controls')
 pages=[x.extract_text() or '' for x in pypdf.PdfReader(h.H/'input_reader.pdf').pages];h.need(len(pages)==2,'two reader pages');t='\n'.join(pages)
 for r in counts['documents'].values():
  for v in ['raw_untrimmed','calibrated_selected']:h.need(f"{r['metrics'][v]['NFC']['characters_without_whitespace']:,}" in t,'reader full document cost')
 for rs in counts['raw_files'].values():
  for r in rs.values():h.need(f"{r['metrics']['NFC']['characters_without_whitespace']:,}" in t,'reader whole raw file cost')
 for token in ['two original manuscripts','no new topic','no compression factor','unknown costs, not zero costs','exhaustive J1 census remains paid in full']:
  h.need(token in ' '.join(t.split()),'reader qualification '+token)
 report=dict(status='PASS',original_manuscripts_added=2,existing_topics=['A','C'],new_topics=0,pdf_pages=48,pdf_metric_cells=210,raw_metric_cells=80,controls_rejected=36,scientific_programs_executed=False,partial_formal_declarations=9,whole_new_required_programs=2,shared_existing_program_charged_once=True,old_C_exhaustive_program_retained=True,additional_whole_C_common_note=True,operational_drivers=3,ratio=None,font_dictionaries=36,used_glyph_classes=805,calibration_classes=27,calibration_occurrences=286,actual_visible_formfeed_components=7,one_envelope_replaces_seven_decoded_characters=True,returned_extraction_modified=False)
 for n,o in [('report.json',report),('counts.json',counts),('controls.json',controls),('font_audit.json',audits)]:(a.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
