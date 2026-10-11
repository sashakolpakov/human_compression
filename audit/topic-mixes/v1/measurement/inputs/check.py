#!/usr/bin/env python3
"""Replay complete F005 measurement inputs, controls and optional TeX; no ratios."""
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

def run(a):
 need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
 p=E.load('policy.json');acceptance=p['scientific_acceptance']
 need(isinstance(acceptance,dict) and acceptance['status']=='DISTINCT_ROOT_SCIENTIFIC_ACCEPTANCE_BOUND','distinct scientific acceptance before input freeze')
 need(acceptance['root_manifest_path'] in [r['path']for r in p['scientific_bindings']],'acceptance manifest is an actual checked scientific binding')
 old_policy=E.load('policy_before_scientific_acceptance.json');comparison=dict(p)
 comparison['scientific_acceptance']=old_policy['scientific_acceptance'];comparison['scientific_bindings']=comparison['scientific_bindings'][:-2]
 need(comparison==old_policy,'only declared acceptance metadata changed after counting')
 root_row=next(r for r in p['scientific_bindings']if r['path']==acceptance['root_manifest_path']);root_path,data=E.bound(root_row,a)
 need(sha(data)==acceptance['root_manifest_sha256'],'exact accepted science manifest')
 for row in json.loads(data)['exports']:
  rel=Path(row['path']);need(not rel.is_absolute() and '..'not in rel.parts,'safe root evidence path');b=(root_path.parent/rel).read_bytes()
  need(len(b)==row['bytes'] and sha(b)==row['sha256'],'unchanged root scientific evidence '+row['path'])
 result,audits,cache=E.replay(a)
 need(result==E.load('author_counts.json'),'all180 PDF+70 raw cells, complete hashes and unknowns match')
 negative=controls.run(a,cache);need(negative==E.load('author_controls.json'),'all40 semantic controls reproduce')
 need(make_reader.make()==(H/'input_reader.tex').read_text(),'exact complete reader with all counts and qualifications')
 visual=E.load('graphics_and_visual.json')
 need(set(visual['documents'])==set(result['documents']),'all six visual bindings')
 for k,d in result['documents'].items():
  v=visual['documents'][k];need(v['pdf_sha256']==d['pdf_sha256'] and v['pages']==list(range(1,d['pages']+1)) and v['all_pages_viewed'],'complete visual page record '+k)
 need(visual['reader_visual_status']=='COMPLETE_TWO_PAGE_READING' and visual['reader_pdf_sha256']==sha((H/'input_reader.pdf').read_bytes()),'final reader visual record')
 need(all(v is None for v in visual['excluded_costs'].values()) and all(x['full_graphical_cost']is None for x in visual['source_graphical_proxies']),'unknown graphical and retained costs')
 need(not visual['graphics_absence_implies_zero'] and not visual['figures_replaced_by_synthetic_text'],'no fabricated graphical price')
 font_counts={k:dict(dictionaries=len(v['font_dictionaries']),classes=len(v['encoded_glyph_classes']),unchanged_type0=len(v['unchanged_type0_dictionaries']))for k,v in audits.items()}
 need(font_counts['F005']==dict(dictionaries=23,classes=469,unchanged_type0=0) and font_counts['CODE2']==dict(dictionaries=1,classes=5,unchanged_type0=2),'actual source/code font counts')
 need(sum(v['unchanged_type0']for v in font_counts.values())==18,'all unchanged Type0 dictionaries')
 need(sum(d['glyph_repairs']for d in result['documents'].values())==1210 and len(E.load('glyph_aliases.json')['aliases'])==9,'all and only nine observed classes/1210 substitutions')
 rendered=[]
 if a.render:
  dest=a.out/'render';dest.mkdir();rd=dest/'reader';rd.mkdir();shutil.copyfile(H/'input_reader.tex',rd/'input_reader.tex')
  cases=[(rd,'input_reader',H/'input_reader.pdf',2)]
  for key in ['CODE1','CODE2']:
   d=dest/key;d.mkdir();row=p['replacements'][key];texpath=str(Path(row['path']).with_suffix('.tex'))
   texrow=next(r for r in p['scientific_bindings']if r['path']==texpath);_,b=E.bound(texrow,a);(d/'programs.tex').write_bytes(b)
   for r in p['programs']:
    if r['printed_document']==key:
     _,b=E.bound(r,a);target=d/r['printed_path'];need(target.parent==d,'literal local complete program name');target.write_bytes(b)
   pdf,_=E.bound(row,a);cases.append((d,'programs',pdf,row['pages']))
  for d,stem,original,n in cases:
   actual=compile_twice(d,stem,a.xelatex);expect=[x.extract_text()for x in pypdf.PdfReader(original).pages]
   need(len(actual)==n and actual==expect,'complete per-page text render equality '+str(original))
   rendered.append(dict(document=d.name,pages=n,per_page_text_equal=True))
 report=dict(status='PASS_AUTHOR_INPUT_REPLAY_PENDING_DISTINCT_INPUT_REVIEW',pdf_cells=180,raw_cells=70,whole_PDFs=6,pages=45,semantic_controls=negative['rejected'],font_counts=font_counts,glyph_substitutions=1210,rendered=rendered,program_inclusion=result['program_inclusion'],scientific_programs_executed=False,factors_evaluated=False,ratio=None,source_count=1,source_map_records=35,unanswered_source_problems=3,partial_formal_declarations=2,scientific_acceptance=acceptance)
 for name,obj in [('report.json',report),('counts.json',result),('controls.json',negative),('font_audit.json',audits)]:
  (a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS180 PDF+70 raw cells,40 controls; no factors.');return report

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));run(ap.parse_args())
