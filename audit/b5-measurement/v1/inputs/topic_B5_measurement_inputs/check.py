#!/usr/bin/env python3
"""Portable full-document/whole-file B5 input replay, without numerical factors."""
from pathlib import Path
import argparse,json
import pypdf
import extract_inputs as h
from controls import run

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 c,f,r=run(a);h.need(c==h.load('author_counts.json'),'120 full PDF/30 direct article/70 raw cells');h.need(r==h.load('author_controls.json'),'34 semantic controls')
 pages=[p.extract_text() or '' for p in pypdf.PdfReader(h.H/'input_reader.pdf').pages];h.need(len(pages)==2,'two input reader pages');t=' '.join('\n'.join(pages).split())
 for doc in list(c['documents'].values())+[c['source_article_only']]:
  for v in ['raw_untrimmed','calibrated_selected']:h.need(f"{doc['metrics'][v]['NFC']['characters_without_whitespace']:,}" in t,'reader exact full PDF/source-body cost')
 for rows in c['raw_files'].values():
  for row in rows.values():h.need(f"{row['metrics']['NFC']['characters_without_whitespace']:,}" in t,'reader whole raw file cost')
 for s in ['one original manuscript','existing five-page common paper','entire earlier program bundle','No factor is calculated','null costs','not the final journal PDF']:
  h.need(s in t,'reader boundary '+s)
 report=dict(status='PASS',original_manuscripts_added=1,topic='B',new_topics=0,existing_originals_retained=4,pdf_pages=49,pdf_metric_cells=120,article_only_cells=30,raw_metric_cells=70,semantic_controls=34,whole_new_mathematical_programs=4,principal_required_programs=1,uniform_validation_programs=2,auxiliary_example_programs=1,operational_drivers=2,partial_formal_declarations=8,source_cover_retained_in_primary=True,article_only_direct_extraction=True,full_old_and_new_common_charged=True,source_font_dictionaries=26,combined_Type1_dictionaries=27,combined_used_classes=667,actual_exceptional_classes_viewed=58,calibrated_classes=15,calibration_occurrences=173,curved_diagram_classes_literal=24,ratio=None,scientific_programs_executed=False)
 for n,o in [('report.json',report),('counts.json',c),('font_audit.json',f),('controls.json',r)]:(a.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
