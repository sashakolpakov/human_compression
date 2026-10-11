#!/usr/bin/env python3
"""Check the complete consolidation boundary; no unchanged scientific rerun."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,subprocess,sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
SOURCES=['L032','L034','F016','F013','L035','N009','L128','L012']
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def bound(row,root=ROOT):
 p=Path(row['path']);need(not p.is_absolute()and '..'not in p.parts,'relative bound path');b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'bound file '+str(p));return b
def validate_map(d):
 need(d['source_ids']==SOURCES and d['existing_principal_contracts']==8,'all eight admitted contracts')
 need(d['row_count']==len(d['rows'])==102 and len({x['id']for x in d['rows']})==102,'all102 dispositions')
 need(set(x['source_id']for x in d['rows'])==set(SOURCES),'all source owners')
 originals=[]
 for file,key in [('prior/audit/topic-a/v2/stage_U_A1_A4_map.json','rows'),('prior/audit/topic-a/v2/A5_A6_coverage.json','coverage_rows'),('prior/papers/topic-a/extensions/diagram-symmetries/v1/source_clause_map.json','rows'),('prior/papers/topic-affine/v2/scope.json','source_rows')]:originals+=read(ROOT/file)[key]
 need([x['inherited_record']for x in d['rows']]==originals,'all inherited statements and qualifications literal')
 for row in d['rows']:need(row['contract_changed']is False and row['current_span_ids']and all(x in d['proof_spans']for x in row['current_span_ids']),'current proof routes '+row['id'])
 for sid,s in d['proof_spans'].items():
  b=(ROOT/s['path']).read_bytes();a,z=s['start_byte'],s['end_byte_exclusive'];need(0<=a<z<=len(b)and sha(b[a:z])==s['span_sha256'],'actual proof/context span '+sid)
 for x in d['whole_common'].values():bound(x)
 need(d['new_source_credit']==d['new_question_credit']==0 and d['ratio']is None,'no merger credit or ratio')
def code_inclusion():
 d=read(ROOT/'program_inventory.json');rows=d['required_complete_files'];need(len(rows)==d['program_data_file_count']==11 and len({x['path']for x in rows})==11,'whole computation roster')
 out=[];texts={x:(ROOT/x).read_text()for x in ['two-group-computation.tex','affine-programs.tex','diagram-programs.tex']}
 for row in rows:
  b=bound(row);tex=texts[row['printed_in']];literal=b.decode()
  if row['path'].startswith('required-code/'):
   blocks=re.findall(r'\\begin\{CompleteProgram\}\n(.*?)\\end\{CompleteProgram\}',tex,re.S);need(sum(x==literal for x in blocks)==1,'entire inline code bytes '+row['path'])
  else:
   matches=re.findall(r'\\VerbatimInput(?:\[([^]]*)\])?\{([^}]+)\}',tex);matches=[x for x in matches if x[1]==row['path']];need(len(matches)==1 and not re.search('firstline|lastline|firstnumber',matches[0][0]),'whole external code directive '+row['path'])
  out.append(dict(path=row['path'],bytes=len(b),complete=True))
 need(len(d['auxiliary_files'])==3,'all three inherited affine auxiliaries')
 for x in d['auxiliary_files']:bound(x)
 return out

def printed_code_inclusion():
 """Check the full printed code, without using this normalization as a cost."""
 d=read(ROOT/'program_print_inclusion.json');need(d['status']=='PASS'and d['whole_files']==11 and d['not_a_cost_measurement']is True,'printed-code scope')
 cache={};checks=[]
 for row in d['checks']:
  pdf=row['pdf']
  if pdf not in cache:
   pages=[]
   for i,page in enumerate(PdfReader(ROOT/pdf).pages,1):
    text=page.extract_text()or''
    text=re.sub(r'\n'+str(i)+r'\s*$', '', text)
    pages.append(text)
   cache[pdf]=''.join(c for c in '\n'.join(pages)if not c.isspace()and c not in '\u21aa\u230b')
  raw=''.join(c for c in (ROOT/row['file']).read_text()if not c.isspace())
  need(raw in cache[pdf] and len(raw)==row['nonspace_characters'],'entire printed program '+row['file'])
  need(row['all_nonspace_program_characters_present']is True,'printed inclusion assertion')
  checks.append(dict(file=row['file'],pdf=pdf,complete_nonspace_program=True))
 need(len(checks)==11 and {x['file']for x in checks}=={x['path']for x in read(ROOT/'program_inventory.json')['required_complete_files']},'printed entire required roster')
 return checks

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');p.add_argument('--public-root',type=Path);p.add_argument('--study-root',type=Path);a=p.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if(ROOT/'manifest.json').exists():
  for x in read(ROOT/'manifest.json')['exports']:bound(x)
 d=read(ROOT/'source_contract_map.json');validate_map(d);programs=code_inclusion();printed=printed_code_inclusion();formal=read(ROOT/'formal_scope.json');need(formal['module_count']==len(formal['modules'])==14 and formal['new_declarations']==0 and formal['whole_volume_formalized']is False and formal['arbitrary_parabolic_theorem_formalized']is False,'exact inherited formal boundary')
 for row in formal['modules']:
  text=bound(row['current']).decode();need(row['unchanged']is True,'formal exact reuse');imports=[v for v in re.findall(r'^import (\S+)',text,re.M)if not v.startswith('Mathlib')];need(imports==row['local_imports']and all((ROOT/'formal'/(v+'.lean')).is_file()for v in imports),'closed local formal imports')
 reused=[]
 if a.public_root:
  for name in ['inherited_files.json','additional_inherited_files.json']:
   for x in read(ROOT/name)['files']:
    b=(a.public_root/x['source']).read_bytes();need(len(b)==x['bytes']and sha(b)==x['sha256'],'exact admitted predecessor '+x['source']);reused.append(x['source'])
 primary=[]
 if a.study_root:
  def walk(v):
   if isinstance(v,dict):
    if {'path','bytes','sha256'}<=v.keys():
     p=Path(v['path']);need(not p.is_absolute()and '..'not in p.parts,'relative primary binding');b=(a.study_root/p).read_bytes();need(len(b)==v['bytes']and sha(b)==v['sha256'],'primary binding '+str(p));primary.append(str(p))
    else:
     for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  walk(d['source_bindings'])
 from copy import deepcopy
 controls=[]
 for name,fn in [('omit entire original',lambda x:x['source_ids'].pop()),('alter inherited qualification',lambda x:x['rows'][0]['inherited_record'].update(qualification='none')),('erase actual proof route',lambda x:x['rows'][0].update(current_span_ids=[])),('silently change principal contract',lambda x:x['rows'][0].update(contract_changed=True)),('claim merger credit',lambda x:x.update(new_source_credit=1))]:
  z=deepcopy(d);fn(z)
  try:validate_map(z)
  except(ValueError,KeyError):controls.append(dict(name=name,rejected=True))
  else:raise ValueError('control accepted '+name)
 renders=[]
 if a.render:
  cmd=[sys.executable,'-B',str(ROOT/'build.py'),'--out',str(a.out/'render'),'--xelatex',a.xelatex];q=subprocess.run(cmd,capture_output=True,text=True);(a.out/'build.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'full render')
  for row in read(a.out/'render/report.json')['documents']:
   p=ROOT/(row['document']+'.pdf');need(p.is_file(),'frozen PDF '+str(p));old=[z.extract_text()or''for z in PdfReader(p).pages];fresh=[z.extract_text()or''for z in PdfReader(a.out/'render'/row['document']/(row['document']+'.pdf')).pages];need(old==fresh,'every rendered page '+row['document']);renders.append(dict(document=row['document'],pages=len(old),all_page_text_equal=True))
 report=dict(status='PASS_AUTHOR_BINDING_AND_ASSEMBLY_NOT_MATHEMATICAL_ACCEPTANCE',source_contracts=8,source_rows=102,proof_interfaces=len(d['proof_spans']),whole_programs=programs,whole_printed_programs=printed,formal_modules=14,new_formal_declarations=0,scientific_programs_or_Lean_reexecuted=False,admitted_predecessor_bindings=len(reused),primary_bindings=len(primary),controls=controls,renders=renders,new_credits=0,ratio=None)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS8 contracts/102 rows/11 whole files/14 reused formal modules; independent science review pending')
if __name__=='__main__':main()
