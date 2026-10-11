#!/usr/bin/env python3
"""Portable whole-input recount; no GAP/Lean replay and no factors."""
from pathlib import Path
import json,argparse
import pypdf
import extract_inputs as h
from controls import run

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 counts,audits,controls=run(a);h.need(counts==h.load('author_counts.json'),'all 240 PDF/280 raw/80 text-only cells');h.need(controls==h.load('author_controls.json'),'all 49 semantic controls')
 pages=[x.extract_text() or '' for x in pypdf.PdfReader(h.HERE/'input_reader.pdf').pages];h.need(len(pages)==3,'three complete input reader pages');text='\n'.join(pages)
 for row in counts['documents'].values():h.need(f"{row['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']:,}" in text,'reader exact PDF cost')
 for category,rows in counts['raw_files'].items():
  for val in [len(rows),sum(r['bytes'] for r in rows.values()),sum(r['metrics']['NFC']['characters_without_whitespace'] for r in rows.values())]:h.need(f'{val:,}' in text,'reader complete raw group cost '+category)
 for key in ['N007','N006']:
  h.need(f"{counts['text_only_sensitivity'][key]['metrics']['NFC']['characters_without_whitespace']:,}" in text,'reader text-only sensitivity')
 for token in ['two original manuscripts','no compression factor','not literal Unicode extraction','costs remain null','21,960,689','2,516,249','240 PDF cells','280 cells']:
  h.need(token in text,'reader scope '+token)
 report=dict(status='PASS',original_manuscripts=2,pdf_metric_cells=240,raw_metric_cells=280,text_only_sensitivity_cells=80,controls_rejected=len(controls['controls']),scientific_programs_executed=False,pdf_pages=66,source_rows=dict(N007=32,N006=27),required_GAP_or_witness_files=16,validation_GAP_files=3,required_decoding_drivers=2,operational_drivers=4,partial_formal_declarations=17,unique_formal_files=3,ratio=None,font_dictionaries=dict(N007=22,N006=23),used_glyph_classes=dict(N007=569,N006=698),calibration_classes=dict(N007=17,N006=21),calibration_occurrences=dict(N007=237,N006=356),graphical_proxy_events=dict(N007=152,N006=288),graphical_proxy_policy='proposed; distinct input review required before numerical adoption',actual_whitespace_decoded_visible_glyphs=dict(N007=7,N006=0),duplicate_Form_metadata_callbacks=dict(N007=1,N006=0),returned_extraction_modified=False,unchanged_N007_prior_documents=3)
 for name,obj in [('report.json',report),('counts.json',counts),('controls.json',controls),('font_audit.json',audits)]:(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
