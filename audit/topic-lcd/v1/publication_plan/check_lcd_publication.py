#!/usr/bin/env python3
"""Additive LCD public guard: exact files, accepted chains and scoped inventory."""
import argparse,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
def need(x,m):
 if not x:raise ValueError('LCD_PUBLIC: '+m)
def verify(root):
 def read(rel):return json.loads((root/rel).read_text())
 def bind(e):
  p=Path(e['path']);need(not p.is_absolute()and '..'not in p.parts,'safe bound route');b=(root/p).read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'exact '+str(p))
 a=read('audit/topic-lcd/v1/admission.json');m=read('audit/topic-lcd/v1/measurement/admission.json');need(a['status'].startswith(('ROOT_ADMITTED','ROOT_ACCEPTED'))and m['status'].startswith(('ROOT_ADMITTED','ROOT_ACCEPTED')),'root public admissions')
 need(a['source_ids']==m['source_ids']==['L050','F017']and a['principal_originals_added']==2 and a['new_intake_originals']==a['new_question_credit']==a['new_formal_credit']==0,'exact two source scope')
 for e in a['artifacts']:bind(e)
 for e in a['science_manifests']+m['manifests']:
  bind(e);manifest=read(e['path']);folder=Path(e['path']).parent
  for x in manifest['exports']:bind(dict(x,path=str(folder/x['path'])))
 need(a['source_dispositions']==dict(L050=54,F017=104)and a['whole_common_pages']==14 and a['whole_application_pages']==dict(L050=15,F017=12)and not a['full_source_formalized']and a['unique_partial_Lean_declarations']==9 and a['unresolved_questions_retained'],'complete scientific scope')
 need(m['primary_costs']==dict(sources=58756,common=32300,L050_application=37432,F017_application=29454,denominator=99186)and m['whole']['interpretation']=='expansion'and m['software_inclusive_factor']is None and m['pooled_factor']is None and m['unknown_original_software_cost']is None,'adopted manuscript boundary')
 need(m['whole_file_contents']==102 and m['whole_file_occurrences']==127 and m['original_bytes']==548250 and m['required_original_bytes']==422956,'complete raw collection')
 inv=read('audit/topic-lcd/v1/measurement/inputs/whole_file_counts.json');need(len(inv['files'])==102 and sum(x['bytes']for x in inv['files'])==548250 and sum(len(x['occurrences'])for x in inv['files'])==127,'whole-file inventory')
 rows=a['scientific_catalogue_rows'];need(len(rows)==3 and[r['physical_pages']for r in rows]==[14,15,12]and[r['compiler']for r in rows]==['pdflatex','pdflatex','xelatex'],'authoritative compilers')
 for r in rows:
  need(re.search(r'\\title\{([^{}]+)\}',(root/r['tex']).read_text()).group(1)==r['title'],'literal title');need(len(PdfReader(root/r['pdf']).pages)==r['physical_pages'],'complete PDF')
  for f in r['tex_inputs']+r['raw_program_inputs']+r['required_data_inputs']+r['optional_validation_inputs']+r['operational_driver_inputs']+r['partial_formal_inputs']:need((root/f).is_file(),'full route '+f)
  need(len(r['raw_program_inputs'])==22 and len(r['required_data_inputs'])==61 and len(r['optional_validation_inputs'])==3,'explicit topic-wide required/optional routes')
 return dict(status='PASS_LCD_PUBLICATION',source_ids=['L050','F017'],artifacts=len(a['artifacts']),scientific_pages=41,source_pages=28,whole_files=102,raw_occurrences=127,unique_partial_Lean_declarations=9,software_inclusive_factor=None)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);print(json.dumps(verify(p.parse_args().repo),indent=2))
