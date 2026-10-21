#!/usr/bin/env python3
"""Distinct bounded LCD numerical acceptance replay; no author arithmetic imports."""
import argparse,copy,hashlib,json,shutil,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ContentStream,FloatObject
from arithmetic import read,need,validate,exact,DOCS
from figures import check as check_figures,NS
from reader_check import check as check_reader
PIN='0e1366b9e5d21d7e8158f3330d00db892840e1f9b2bf6d94c5bc05069b8d4cf9'
INPUT='3d4f1a989020ed6cf9e632263b785b79ecdf5d30765170760b8240f9c13d27cc';REVIEW='2f9fa038f66491e5b8607970f7fa499a88f398a2868a72a80d3588948e954071';ROOT='214712d6b2976d813205ea083e59c14d88243c94b568233c7d9eef115ec5d6ac'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path('/Users/sasha/medusa/research/leemans/topic_LCD_measurement_results'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--skip-builder',action='store_true');args=ap.parse_args();p=args.packet;out=args.out;need(not out.exists(),'fresh output');out.mkdir(parents=True)
 need(sha(p/'manifest.json')==PIN,'exact numerical author manifest');m=read(p/'manifest.json');need(len(m['exports'])==47,'complete exports')
 for row in m['exports']:
  f=p/row['path'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'frozen export '+row['path'])
 for f,pin in [('input',INPUT),('review',REVIEW),('root',ROOT)]:need(sha(p/'inputs'/(f+'_manifest.json'))==pin,'accepted input chain')
 protocol=read(p/'protocol.json');need((p/'protocol.json').read_bytes()==(p/'protocol_freeze/protocol.json').read_bytes(),'fixed pre-evaluation protocol')
 for row in protocol['inputs']:
  f=p/row['path'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'exact copied accepted input')
  if row['source_export']!='manifest.json':
   entries={x['path']:x for x in read(p/row['manifest'])['exports']};owner=entries[row['source_export']];need((owner['sha256'],owner['bytes'])==(row['sha256'],row['bytes']),'actual manifest ownership')
 need(protocol['whole_common_paid_once'] and protocol['whole_required_boundary_acquired_for_each_conditional'] and not protocol['optional_validation_required'] and not protocol['sibling_premise'],'protocol acquisition boundary')
 need(protocol['software_inclusive_factor'] is None and protocol['pooled_factor'] is None,'protocol scalar boundary')
 need(read(p/'inputs/root_adoption.json')['numerical_stage_authorized'] is True,'authorized numbers')
 r=read(p/'results.json');arith=validate(p);graphics=check_figures(p,r);reader=check_reader(p);controls=[]
 # No outer hash check is applied to these deliberate semantic mutations.
 for name in ['drop_common','double_common','conditional_includes_common','software_in_denominator','unknown_as_zero','optional_as_required','omit_required_file','full_formal_claim','missing_coordinate','duplicate_contents','raw_role_zero','new_credit','false_scope']:
  bad=copy.deepcopy(r);x=bad['coordinates'][0]
  if name in ['drop_common','double_common']:
   d=x['totals']['written']+(-1 if name=='drop_common' else 1)*x['costs']['U_LCD'];x['totals']['written']=d;x['comparisons']['written']=exact(x['totals']['source'],d)
  elif name=='conditional_includes_common':x['comparisons']['conditional_L050']=exact(x['costs']['L050'],x['costs']['A_L050']+x['costs']['U_LCD'])
  elif name=='software_in_denominator':x['comparisons']['written']=exact(x['totals']['source'],x['totals']['written']+x['acquisition']['required_raw_premises'])
  elif name=='unknown_as_zero':bad['scope']['source_software_cost']=0
  elif name=='optional_as_required':bad['scope']['optional_validation_required_for_conditional']=True
  elif name=='omit_required_file':bad['acquisition']['required_whole_content_sha256'].pop()
  elif name=='full_formal_claim':bad['scope']['full_source_formalized']=True
  elif name=='missing_coordinate':bad['coordinates'].pop()
  elif name=='duplicate_contents':bad['raw_file_inventory']['files'].append(copy.deepcopy(bad['raw_file_inventory']['files'][0]))
  elif name=='raw_role_zero':x['raw_costs']['required_data']=0
  elif name=='new_credit':bad['new_question_credit']=1
  else:bad['scope']['F017_dispositions']=103
  try:validate(p,bad,False)
  except ValueError as e:controls.append({'name':name,'rejected_at':str(e)})
  else:raise ValueError('semantic mutation accepted '+name)
 # Edit actual vector geometry while leaving results/plot-data unchanged.
 for name in ['svg_bar_height','svg_missing_bar','svg_optional_solid','pdf_bar_height']:
  alt=out/name;alt.mkdir()
  for f in ['costs.svg','costs.pdf','inventory.svg','inventory.pdf','document_graph.svg','document_graph.pdf','document_graph.json']:shutil.copy2(p/f,alt/f)
  if name.startswith('svg_'):
   file='document_graph.svg' if name=='svg_optional_solid' else 'costs.svg';tree=ET.parse(alt/file);root=tree.getroot();key='edge-optional-U_LCD' if name=='svg_optional_solid' else 'cost-whole-L050';g=next(z for z in root.iter(NS+'g') if z.get('id')==key)
   if name=='svg_missing_bar':g.set('id','removed-bar')
   elif name=='svg_optional_solid':
    path=next(g.iter(NS+'path'));style=path.get('style');need('stroke-dasharray' in style,'applied dashed mutation');path.set('style',';'.join(s for s in style.split(';') if 'stroke-dash' not in s))
   else:
    path=next(g.iter(NS+'path'));d=path.get('d');d=d.replace('205.5216','200.5216');need(d!=path.get('d'),'applied SVG height mutation');path.set('d',d)
   tree.write(alt/file,encoding='utf-8',xml_declaration=True)
  else:
   w=PdfWriter(clone_from=alt/'costs.pdf');page=w.pages[0];cs=ContentStream(page.get_contents(),page.pdf);changed=0
   for operands,op in cs.operations:
    if op in [b'l'] and len(operands)==2 and abs(float(operands[1])-109.4784)<1e-4:
     operands[1]=FloatObject(float(operands[1])+5);changed+=1
   need(changed>=2,'applied PDF height mutation');page.replace_contents(cs);w.write(alt/'costs.pdf')
  try:check_figures(alt,r)
  except ValueError as e:controls.append({'name':name,'rejected_at':str(e)})
  else:raise ValueError('actual graph mutation accepted '+name)
 build=None
 if not args.skip_builder:
  export=out/'export_copy';export.mkdir()
  for row in m['exports']:
   f=export/row['path'];f.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p/row['path'],f)
  shutil.copy2(p/'manifest.json',export/'manifest.json')
  q=subprocess.run([sys.executable,'-B','-O',str(export/'build.py'),'--out',str(out/'fresh_build'),'--render','--xelatex','/opt/homebrew/bin/xelatex'],capture_output=True,text=True,timeout=120)
  (out/'builder_stdout.txt').write_text(q.stdout+q.stderr);need(q.returncode==0,'export-only whole builder')
  fresh=out/'fresh_build';need(read(fresh/'results.json')==r,'same rebuilt numerical results');check_figures(fresh,r);validate(fresh)
  need([x.extract_text() for x in PdfReader(fresh/'reader.pdf').pages]==[x.extract_text() for x in PdfReader(p/'reader.pdf').pages],'all three reader page texts')
  build={'status':'PASS','exports_only':47,'reader_pages':3,'all_page_text_exact':True,'fresh_result_exact':True,'fresh_vector_geometry_independently_checked':True}
 report={'status':'PASS_DISTINCT_LCD_NUMERICAL_REPLAY','author_manifest_sha256':PIN,'accepted_input_review_manifest':REVIEW,'accepted_root_input_adoption':ROOT,'method':'Own rational/Decimal arithmetic, complete CSV and raw-role reconstruction, direct SVG and PDF path parsing; no author arithmetic/presentation/checker imports. Separate author export-only build invoked as replay.','arithmetic':arith,'figures':graphics,'reader':reader,'semantic_controls':controls,'control_count':len(controls),'export_only_replay':build,'no_extraction_fonts_scientific_or_Lean_rerun':True}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'controls':len(controls),'fractions':90,'bars_each_format':17,'export_only':build}))
if __name__=='__main__':main()
