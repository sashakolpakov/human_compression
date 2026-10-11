#!/usr/bin/env python3
"""Replay counts, controls and full reader values from exact public inputs."""
from pathlib import Path
import argparse,json
import pypdf
import extract_inputs as h
from controls import run

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 counts,control,audit=run(a)
 h.need(counts==h.load_json('author_counts.json'),'all 240 PDF/90 raw counts and complete scope')
 h.need(control==h.load_json('author_controls.json'),'all 21 controls')
 pages=[x.extract_text() or '' for x in pypdf.PdfReader(h.HERE/'input_reader.pdf').pages];h.need(len(pages)==2,'complete two-page reader');text='\n'.join(pages)
 for key in ['F015','L028','U_M','M1','M_CODE','U_CE','CE1','CE_CODE']:
  n=counts['documents'][key]['metrics']['calibrated_selected']['NFC']['characters_without_whitespace'];h.need(f'{n:,}' in text,'reader whole-document count '+key)
 for row in counts['raw_files']['complete_programs'].values():h.need(f"{row['metrics']['NFC']['characters_without_whitespace']:,}" in text,'reader raw whole program count')
 h.need('no compression factor' in text and 'two originals' in text,'reader no numerical-factor or source-count inflation')
 report=dict(status='PASS',pdf_metric_cells=240,raw_metric_cells=90,original_manuscripts=2,controls_rejected=len(control['controls']),complete_reader_pages=2,fresh_font_dictionaries=sum(len(v['font_dictionaries']) for v in audit.values()),fresh_glyph_classes=sum(len(v['encoded_glyph_classes']) for v in audit.values()),actual_repairs=sum(v['glyph_repairs'] for v in counts['documents'].values()),scientific_programs_executed=False,ratio=None)
 for name,data in [('report.json',report),('counts.json',counts),('controls.json',control),('font_audit.json',audit)]: (a.out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
