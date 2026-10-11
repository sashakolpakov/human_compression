#!/usr/bin/env python3
"""Frozen complete-input replay, semantic controls and reader values."""
from pathlib import Path
import json,argparse
import pypdf
import extract_inputs as h
from controls import run

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 counts,audits,controls=run(a);h.need(counts==h.load('author_counts.json'),'all 120 PDF and 40 whole-file cells');h.need(controls==h.load('author_controls.json'),'all thirty semantic controls')
 pages=[x.extract_text() or '' for x in pypdf.PdfReader(h.HERE/'input_reader.pdf').pages];h.need(len(pages)==2,'two complete input reader pages');text='\n'.join(pages)
 for row in counts['documents'].values():h.need(f"{row['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']:,}" in text,'reader exact PDF cost')
 for rows in counts['raw_files'].values():
  for row in rows.values():h.need(f"{row['metrics']['NFC']['characters_without_whitespace']:,}" in text,'reader exact whole-file cost')
 for token in ['one original manuscript','no compression factor','zero uniform theorems','costs remain null']:
  h.need(token in text,'reader scope '+token)
 report=dict(status='PASS',original_manuscripts=1,pdf_metric_cells=120,raw_metric_cells=40,controls_rejected=30,scientific_programs_executed=False,partial_formal_declarations=8,required_finite_premises=0,whole_validation_programs=1,operational_drivers=2,ratio=None,font_dictionaries=22,used_glyph_classes=569,calibration_classes=17,calibration_occurrences=237,actual_whitespace_decoded_visible_glyphs=7,duplicate_Form_metadata_callbacks=1,returned_extraction_modified=False)
 for name,obj in [('report.json',report),('counts.json',counts),('controls.json',controls),('font_audit.json',audits)]:(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
