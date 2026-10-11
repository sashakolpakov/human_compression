#!/usr/bin/env python3
"""Exact migration and complete arrangement audit; no scientific rerun or scoring."""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess,sys
from pypdf import PdfReader
from migrate import make,require
H=Path(__file__).resolve().parent
PIN='e70770940fe3db852b77a3e400bf913263eec6f1114e89d311f6d4e07b0dad57'
ROOT_REVIEW='13aa42fa08b4a6517945c91c08c51ee3eaec87f572662dad991fe9b519cd6676'
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(root,row):
 p=Path(row['path']);require(not p.is_absolute()and'..'not in p.parts,'safe path');data=(root/p).read_bytes();require(len(data)==row['bytes']and sha(data)==row['sha256'],'whole bound file '+str(p));return data
def validate(a):
 require(a['source_id']=='L073'and a['target_originals']==1 and a['source']['pages']==9,'one complete original')
 require(a['common']['pages']==2 and [x['pages']for x in a['application']]==[5,10,9]and a['printed_programs']['pages']==11,'all complete papers, class tables and physical source rows')
 require(len(a['raw_programs'])==7 and len(a['required_raw_data'])==2 and len(a['auxiliary_scripts'])==3 and len(a['generated_outputs'])==10,'all full program/data/auxiliary/output files')
 require(all(x['whole_file']for cat in ['raw_programs','required_raw_data','auxiliary_scripts','generated_outputs']for x in a[cat]),'no partial file pricing')
 require(all(a[x]for x in ['whole_common_required','no_old_umbrella_premise','no_L095_special_theorem_premise','finite_G_scope_correction','all_scientific_body_preserved_except_three_cross_references','printed_and_raw_programs_are_alternatives','required_raw_data_has_no_complete_printed_alternative','generated_outputs_are_not_extra_independent_input_premises','generated_outputs_full_inventory_not_pruned','source_corrections_and_exclusions_preserved']),'complete declared interfaces')
 require(a['retained_notation_source']['pages']==48 and not a['predecessor_full_recovery']and not a['historical_geo_numbering_recovered'],'retained notation and unavailable historical numbering scope')
 require(a['formal_declarations']==0 and not a['primary_export']and a['factor']is None,'no invented formal, original export or factor')
 for row in a['scientific_bindings']:
  if row['path']=='corpus161_L073_recovery/manifest.json':require(row['sha256']==PIN,'immutable science pin')
  if row['path']=='corpus161_L073_root_review/manifest.json':require(row['sha256']==ROOT_REVIEW,'distinct root science pin')
def controls(a,sources):
 names=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,TypeError):names.append(name)
  else:raise ValueError('control escaped '+name)
 for name,edit in [('omit complete class table',lambda x:x['application'].pop(1)),('drop historical notation input',lambda x:x['required_raw_data'].pop()),('truncate required program',lambda x:x['raw_programs'][0].update(whole_file=False)),('free generic proof',lambda x:x.update(whole_common_required=False)),('silently import old umbrella',lambda x:x.update(no_old_umbrella_premise=False)),('drop finite hypothesis correction',lambda x:x.update(finite_G_scope_correction=False)),('claim predecessor recovery',lambda x:x.update(predecessor_full_recovery=True)),('invent factor',lambda x:x.update(factor=2))]:
  q=copy.deepcopy(a);edit(q);reject(name,lambda:validate(q))
 for name,old,new in [('remove theorem proof','An incident pair of cosets has a common representative','An incident pair'),('remove finite hypothesis','Throughout this common paper, $G$ is a finite group.',''),('corrupt imported theorem','Common Theorem~2','Common Theorem~9')]:
  key=next(k for k,v in sources.items()if old in v);corrupt=sources[key].replace(old,new,1);reject(name,lambda:require(corrupt==sources[key],'complete literal migrated text'))
 return names
def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args();require(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for row in json.loads((H/'manifest.json').read_text())['exports']:binding(H,row)
 arr=json.loads((H/'arrangement.json').read_text());validate(arr)
 sources,m=make(a.study_root/'corpus161_L073_recovery/primitive-mathieu-geometries.tex');require(m==json.loads((H/'migration.json').read_text()),'exact migration map')
 for n,s in sources.items():require((H/n).read_text()==s,'exact complete migrated TeX')
 rows=[arr['source'],arr['retained_notation_source'],arr['common'],*arr['application'],arr['printed_programs'],*arr['scientific_bindings'],*arr['raw_programs'],*arr['required_raw_data'],*arr['auxiliary_scripts'],*arr['generated_outputs']]
 rows+=[r['tex']for r in [arr['common'],*arr['application'],arr['printed_programs']]]
 for row in rows:binding(a.study_root,row)
 for row in arr['scientific_bindings']:
  if row['path'].endswith('/manifest.json'):
   packet=a.study_root/Path(row['path']).parent
   for e in json.loads(binding(a.study_root,row))['exports']:binding(packet,e)
 for row in [arr['common'],*arr['application'],arr['printed_programs']]:require(len(PdfReader(a.study_root/row['path']).pages)==row['pages'],'whole actual PDF extent')
 tests=controls(arr,sources);render=None
 if a.render:
  subprocess.run([sys.executable,'-B',str(H/'build.py'),'--study-root',str(a.study_root),'--out',str(a.out/'render'),'--xelatex',a.xelatex],check=True,timeout=120)
  render=json.loads((a.out/'render/report.json').read_text())
 report=dict(status='PASS',science_manifest_sha256=PIN,root_science_manifest_sha256=ROOT_REVIEW,whole_bound_files=len(rows),complete_common_pages=2,complete_application_pages=24,complete_program_pages=11,required_programs=7,required_raw_data=2,separate_auxiliary=3,separate_generated_outputs=10,finite_scope_correction_explicit=True,semantic_controls=tests,render=render,science_programs_or_Lean_reexecuted=False,source_or_ratio_admission=False)
 (a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='render'}))
if __name__=='__main__':main()
