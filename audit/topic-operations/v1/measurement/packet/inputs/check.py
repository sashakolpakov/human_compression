#!/usr/bin/env python3
"""Portable whole-input recount with semantic controls; no GAP/Lean or factors."""
from pathlib import Path
import json,argparse,subprocess,shutil
import pypdf
import extract_inputs as h
from controls import run
from graphics_inventory import inventory
from build_reader import render

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();h.need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 counts,audits,controls=run(a);h.need(counts==h.load('author_counts.json'),'all 330 PDF / 330 raw / 110 text-only cells and hashes');h.need(controls==h.load('author_controls.json'),'all 71 actual semantic controls')
 p=h.load('policy.json');graphics={k:inventory(h.bound(r,a)[0],k) for k,r in {**p['sources'],**p['replacements']}.items()};h.need(graphics==h.load('graphics_inventory.json'),'complete image/form/path presence metadata')
 v=h.load('visual_review.json');allpages={(k,i) for k,r in {**p['sources'],**p['replacements']}.items() for i in range(1,r['pages']+1)}
 h.need(len(v['page_views'])==161 and {(r['document'],r['page']) for r in v['page_views']}==allpages,'all physical page visual records')
 h.need(sum(r['mode']=='fresh_current_page_view' for r in v['page_views'])==116 and sum(r['mode']=='inherited_accepted_byte_identical_PDF_view' for r in v['page_views'])==45,'fresh versus reused visual scope')
 for r in v['page_views']:h.need(r['viewed'] and r['pdf_sha256']=={**p['sources'],**p['replacements']}[r['document']]['sha256'],'visual record tied to exact PDF')
 h.need(render()==(h.HERE/'input_reader.tex').read_text(),'deterministic full reader text')
 pages=[x.extract_text() or '' for x in pypdf.PdfReader(h.HERE/'input_reader.pdf').pages];h.need(len(pages)==3,'three complete reader pages');text='\n'.join(pages)
 for row in counts['documents'].values():h.need(f"{row['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']:,}" in text,'reader exact whole PDF cost')
 for cat,rows in counts['raw_files'].items():
  for val in [len(rows),sum(r['bytes'] for r in rows.values()),sum(r['metrics']['NFC']['characters_without_whitespace'] for r in rows.values())]:h.need(f'{val:,}' in text,'reader complete raw group cost '+cat)
 for key in ['N005','N006','N007']:h.need(f"{counts['text_only_sensitivity'][key]['metrics']['NFC']['characters_without_whitespace']:,}" in text,'reader text-only alternative')
 for token in ['three original manuscripts','no compression factor','not literal Unicode extraction','costs remain null','21,960,689','2,516,249','330 PDF cells','330 raw cells','110 cells','validation files and both required input drivers','conditional on acquiring the whole common theory']:
  h.need(token in ' '.join(text.split()),'reader scope '+token)
 diagnostics=None
 if a.render:
  d=a.out/'reader';d.mkdir();(d/'input_reader.tex').write_text(render())
  for n in (1,2):
   r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-file-line-error','input_reader.tex'],cwd=d,capture_output=True,text=True);(d/f'build{n}.stdout').write_text(r.stdout);(d/f'build{n}.stderr').write_text(r.stderr);h.need(r.returncode==0,'fresh reader render')
  diagnostics=[x for x in (d/'input_reader.log').read_text(errors='replace').splitlines() if any(y in x for y in ['Overfull','Underfull','Missing character','undefined','LaTeX Warning'])];h.need(not diagnostics,'clean reader render');h.need([x.extract_text() or '' for x in pypdf.PdfReader(d/'input_reader.pdf').pages]==pages,'fresh all reader page text')
 report=dict(status='PASS',scope='Author input proposal, no numerical acceptance',original_manuscripts=3,source_rows={'N005':81,'N006':27,'N007':32},pdf_documents=11,pdf_pages=161,pdf_metric_cells=330,raw_metric_cells=330,text_only_sensitivity_cells=110,controls_rejected=len(controls['controls']),scientific_programs_executed=False,required_mathematical_or_witness_files=17,validation_files=6,required_decoding_drivers=2,operational_drivers=5,unique_formal_files=3,partial_formal_declarations=17,new_N005_formal_declarations=0,ratio=None,source_glyph_classes={k:len(audits[k]['encoded_glyph_classes']) for k in p['sources']},source_substitutions={k:counts['documents'][k]['glyph_repairs'] for k in p['sources']},source_graphical_proxy_events={k:counts['documents'][k]['graphical_proxy_events'] for k in p['sources']},all_raw_extractions_unmodified=True,graphics_cost=None,reader_pages=3,reader_rendered=a.render,reader_render_diagnostics=diagnostics,citation_only_root_acceptance='7b99164d53378ee61ca73d175082616ffc365ac8501c027a2ac6177eed981284')
 for name,obj in [('report.json',report),('counts.json',counts),('controls.json',controls),('font_audit.json',audits),('graphics_inventory.json',graphics)]:(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
