#!/usr/bin/env python3
"""Portable enlarged Mixes input replay. No scientific execution or factors."""
from pathlib import Path
import argparse,json,re,shutil,subprocess
import pypdf
import extract_inputs as E
import controls,make_reader
from font_tools import need,sha
H=Path(__file__).resolve().parent

def compile_twice(dest,stem,engine):
 for i in range(2):
  r=subprocess.run([str(engine),'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=dest,capture_output=True,text=True)
  (dest/f'{stem}.run{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'clean TeX exit '+stem)
 log=(dest/(stem+'.log')).read_text();need(not re.search('Overfull|Missing character|LaTeX Warning|Package .* Warning',log),'no final layout/glyph diagnostics '+stem)
 return [p.extract_text()for p in pypdf.PdfReader(dest/(stem+'.pdf')).pages]

def verify_manifest(row,args):
 f,b=E.bound(row,args);m=json.loads(b);seen=set()
 for r in m['exports']:
  rel=Path(r['path']);need(not rel.is_absolute()and'..'not in rel.parts and str(rel)not in seen,'safe unique manifest export');seen.add(str(rel));d=(f.parent/rel).read_bytes()
  need(len(d)==r['bytes']and sha(d)==r['sha256'],'frozen input packet '+row['path']+' / '+r['path'])
 return len(seen)

def run(a):
 need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True);p=E.load('policy.json')
 acceptance=p['scientific_acceptance'];need(acceptance['status']=='DISTINCT_COMPLETE_SCIENCE_REVIEW_ACCEPTED','distinct science accepted')
 root=acceptance['root_adoption'];need(root['sha256']=='6176e7c0b7a9753beee793946be26c46ef856ffbb172d10d6af70cf1076e1bc7','fixed root science adoption')
 need(root in p['scientific_bindings'],'checked actual root adoption')
 before=E.load('policy_before_final_adoption_binding.json');q=json.loads(json.dumps(p));added=q['scientific_bindings'].pop()
 need(q==before and added['path']=='topic_Mix_L016_root_adoption/review.json','only final review binding added after first replay')
 delta=E.load('acceptance_binding_delta.json');need(delta['added_binding']==added and delta['prior_policy_sha256']==sha((H/'policy_before_final_adoption_binding.json').read_bytes())and delta['current_policy_sha256']==sha((H/'policy.json').read_bytes()),'transparent acceptance binding delta')
 manifest_rows={r['path']:r for r in p['scientific_bindings']if r['path'].endswith('/manifest.json')}
 for r in p['reused_accepted_inputs'].values():
  if isinstance(r,dict)and r['path'].endswith('/manifest.json'):manifest_rows[r['path']]=r
 frozen={k:verify_manifest(r,a)for k,r in manifest_rows.items()}
 need(frozen['topic_Mix_L016_recovery/manifest.json']==41 and frozen['topic_Mix_L016_independent_review/manifest.json']==58 and frozen['topic_Mix_L016_root_adoption/manifest.json']==4,'complete scientific author/review/root packets')
 result,audits,cache=E.replay(a);expect=E.load('author_counts.json');need(result==expect,'all new150 PDF+60 raw cells and retained180/70 cells exact')
 old=json.loads(E.bound(p['reused_accepted_inputs']['counts'],a)[1]);E.validate_retained(result['retained_accepted_inputs'],old)
 code_boundary=E.load('source_code_boundary.json');E.validate_source_code_boundary(code_boundary)
 need(code_boundary['sources']['L016']['pdf_sha256']==p['source']['sha256'] and code_boundary['sources']['F005']['pdf_sha256']==old['documents']['F005']['pdf_sha256'],'actual source executable boundaries')
 negative=controls.run(a,cache);need(negative==E.load('author_controls.json')and negative['rejected']==47,'all47 semantic controls')
 need(make_reader.make()==(H/'input_reader.tex').read_text(),'exact reader counts and scope')
 visual=E.load('graphics_and_visual.json');need(set(visual['documents'])==set(result['documents']),'all new visual records')
 for k,d in result['documents'].items():
  v=visual['documents'][k];need(v['pdf_sha256']==d['pdf_sha256']and v['pages']==list(range(1,d['pages']+1))and v['all_pages_viewed'],'complete visual page record '+k)
 need(visual['reader_visual_status']=='COMPLETE_TWO_PAGE_READING'and visual['reader_pdf_sha256']==sha((H/'input_reader.pdf').read_bytes()),'final reader viewed')
 need(visual['prior_visual_reuse']['manifest_sha256']==p['reused_accepted_inputs']['distinct_input_acceptance']['sha256']and visual['prior_visual_reuse']['pages']==45 and not visual['prior_visual_reuse']['fresh_viewing_claimed'],'distinct accepted prior visual record reused')
 need(all(v is None for v in visual['excluded_costs'].values())and all(x['full_graphical_cost']is None for x in visual['source_graphical_proxies']),'unknown graphic costs')
 need(not visual['graphics_absence_implies_zero']and not visual['figures_replaced_by_synthetic_text'],'no synthetic graphic cost')
 font_counts={k:dict(dictionaries=len(v['font_dictionaries']),classes=len(v['encoded_glyph_classes']),unchanged_type0=len(v['unchanged_type0_dictionaries']))for k,v in audits.items()}
 need(font_counts['L016']==dict(dictionaries=23,classes=566,unchanged_type0=0)and sum(v['unchanged_type0']for v in font_counts.values())==15,'actual source/replacement font census')
 need(len(E.load('glyph_aliases.json')['aliases'])==12 and sum(d['glyph_repairs']for d in result['documents'].values())==331,'all observed alias occurrences')
 need(all(not x['meta']['duplicate_callbacks']for x in cache.values()),'no duplicated Form callbacks')
 rendered=[]
 if a.render:
  dest=a.out/'render';dest.mkdir();rd=dest/'reader';rd.mkdir();shutil.copyfile(H/'input_reader.tex',rd/'input_reader.tex');cases=[(rd,'input_reader',H/'input_reader.pdf',2)]
  for key,stem in [('REQ','required_program'),('VAL','optional_validation')]:
   d=dest/key;d.mkdir();shutil.copyfile(H/(stem+'.tex'),d/(stem+'.tex'));rows=[r for r in p['programs']if r['printed_document']==key]
   if key=='REQ':rows=[p['required_printed_reused_program']]+rows
   for row in rows:
    _,b=E.bound(row,a);f=d/row['printed_path'];need(f.parent==d,'literal local complete program name');f.write_bytes(b)
   cases.append((d,stem,H/(stem+'.pdf'),p['replacements'][key]['pages']))
  for d,stem,original,n in cases:
   actual=compile_twice(d,stem,a.xelatex);expect=[x.extract_text()for x in pypdf.PdfReader(original).pages]
   need(len(actual)==n and actual==expect,'all rendered page texts match '+original.name);rendered.append(dict(document=d.name,pages=n,per_page_text_equal=True))
 report=dict(status='PASS_AUTHOR_INPUT_REPLAY_PENDING_DISTINCT_INPUT_REVIEW',new_pdf_cells=150,new_raw_cells=60,retained_pdf_cells=180,retained_raw_cells=70,retained_PDFs_reextracted=False,new_physical_pages=27,source_originals=['F005','L016'],new_originals=['L016'],topic='Mixes',new_source_dispositions=19,scientific_packet_exports=frozen,semantic_controls=47,font_counts=font_counts,glyph_substitutions=331,rendered=rendered,program_inclusion=result['program_inclusion'],required_files=2,optional_validation_files=4,operational_files=5,partial_Lean_files=2,partial_Lean_declarations=6,scientific_programs_executed=False,factors_evaluated=False,ratio=None,symmetric_optional_validation_only=True,embedded_source_executable_listings=0,historical_software_cost=None)
 for n,o in [('report.json',report),('counts.json',result),('controls.json',negative),('font_audit.json',audits)]:(a.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print('PASS150 new PDF+60 raw cells;180/70 retained cells;47 controls; no factors.');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));run(ap.parse_args())
