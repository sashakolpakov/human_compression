#!/usr/bin/env python3
"""Check the integrated written edition without changing any source packet."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
PAPERS=['common-theory','application','programs']
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_scope(migration,evidence,retained):
 old=json.loads((ROOT/'precursor_source_contract.json').read_text())
 need(len(migration['records'])==81,'all 81 source records')
 need([x['source_record'] for x in migration['records']]==old['rows'],'unchanged literal source dispositions')
 need(migration['questions']==old['questions'],'question qualifications')
 for row in migration['records']:
  need(row['current_files'],'empty source route')
  for f in row['current_files']:need((ROOT/f).is_file(),'missing source destination '+f)
 roles={r['path']:r['role'] for r in evidence['programs']}
 need(roles=={'programs/affine_example.py':'required_finite_premise_s2_s3_s4','programs/presentation_identities.py':'validation_only','programs/literal_twist.py':'validation_only'},'complete program roles')
 need(evidence['new_Lean_declarations']==0,'no new Lean coverage')
 need(evidence['required_finite_counts']=={'parameters':[2,3,4],'intersection_equalities':675,'product_equalities':10125},'small parameter proof boundary')
 ids={r['id'] for r in retained['external_inputs']['inputs']}
 need(ids=={'coxeter_parabolics','artin_embeddings','artin_products','normal_forms','trees','affine_model','triangle_model'},'all retained interfaces')
 need(retained['own_unpriced_proof_bank_premises']==[] and retained['whole_common_paper_required'],'complete own theory')
def controls(migration,evidence,retained):
 import copy
 rows=[]
 for name,kind in [('remove_source_record',0),('erase_hnn_qualification',1),('demote_affine_premise',2),('erase_classical_tree_input',3),('claim_new_Lean',4)]:
  m,e,r=copy.deepcopy(migration),copy.deepcopy(evidence),copy.deepcopy(retained)
  if kind==0:m['records'].pop()
  elif kind==1:next(x['source_record'] for x in m['records'] if x['source_record']['id']=='N005.3.35')['qualification']=None
  elif kind==2:e['programs'][0]['role']='validation_only'
  elif kind==3:r['external_inputs']['inputs']=[x for x in r['external_inputs']['inputs'] if x['id']!='trees']
  else:e['new_Lean_declarations']=1
  try:validate_scope(m,e,r)
  except RuntimeError as ex:rows.append({'name':name,'rejected':True,'reason':str(ex)})
  else:raise RuntimeError('control accepted '+name)
 return rows
def appendix_text(path):
 from pypdf import PdfReader
 parts=[]
 for i,page in enumerate(PdfReader(path).pages,1):
  lines=page.extract_text().splitlines()
  need(lines and lines[-1].strip()==str(i),'exact appendix page footer')
  parts.append('\n'.join(lines[:-1]))
 return ''.join(''.join(parts).split())
def check_appendix(text):
 rows=[]
 for f in sorted((ROOT/'programs').glob('*.py')):
  raw=''.join(f.read_text().split())
  need(raw in text,'full ordered code tokens '+f.name)
  rows.append({'path':'programs/'+f.name,'nonspace_characters':len(raw),'full_ordered_text_present':True})
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--source');ap.add_argument('--programs',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 out=Path(a.out).expanduser();need(not out.exists() and not out.is_symlink(),'fresh output required');out=out.resolve();out.mkdir(parents=True);start=time.monotonic()
 manifest=json.loads((ROOT/'manifest.json').read_text())
 for r in manifest['exports']:
  f=ROOT/r['path'];need(f.is_file() and not f.is_symlink(),'export '+r['path']);need(sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],'binding '+r['path'])
 migration=json.loads((ROOT/'source_migration.json').read_text());evidence=json.loads((ROOT/'evidence_scope.json').read_text());retained=json.loads((ROOT/'dependency_inventory.json').read_text())
 validate_scope(migration,evidence,retained);control_rows=controls(migration,evidence,retained)
 for row in evidence['programs']:need(sha(ROOT/row['path'])==row['old_binding']['sha256'],'unchanged whole program '+row['path'])
 for f in json.loads((ROOT/'current_spans.json').read_text())['files']:need(sha(ROOT/f['path'])==f['sha256'],'current proof span binding')
 for name in PAPERS[:2]:
  text=(ROOT/(name+'.tex')).read_text()
  for part in re.findall(r'\\input\{(sections/[^}]+)\}',text):text+='\n'+(ROOT/part).read_text()
  labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
  need(len(labels)==len(set(labels)),'duplicate labels '+name);need(set(refs)<=set(labels),'unresolved references '+name)
 printed=appendix_text(ROOT/'programs.pdf');printed_rows=check_appendix(printed)
 try:check_appendix(printed.replace('integer_proper_orders','lost_proper_orders'))
 except RuntimeError:appendix_control={'name':'delete_required_program_token','rejected':True}
 else:raise RuntimeError('appendix omission accepted')
 source_verified=False
 if a.source:need(sha(Path(a.source))==migration['source']['sha256'],'primary edition');source_verified=True
 finite=[]
 if a.programs:
  for key,script in [('affine','programs/affine_example.py'),('presentations','programs/presentation_identities.py'),('literal_twist','programs/literal_twist.py'),('controls','controls.py')]:
   r=subprocess.run([sys.executable,'-B','-O',str(ROOT/script)],cwd=ROOT,capture_output=True,text=True)
   (out/(key+'.stdout')).write_text(r.stdout);(out/(key+'.stderr')).write_text(r.stderr);need(r.returncode==0,'finite program '+key)
   value=json.loads(r.stdout);expected=json.loads((ROOT/'reference'/(key+'.json')).read_text());need(value==expected,'exact unchanged finite result '+key);finite.append(key)
 renders=[]
 if a.render:
  from pypdf import PdfReader
  for name in PAPERS:
   d=out/'render'/name;d.mkdir(parents=True);shutil.copyfile(ROOT/'preamble.tex',d/'preamble.tex');shutil.copyfile(ROOT/(name+'.tex'),d/(name+'.tex'))
   shutil.copytree(ROOT/'sections',d/'sections');shutil.copytree(ROOT/'programs',d/'programs',ignore=shutil.ignore_patterns('__pycache__'))
   for n in [1,2]:
    r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=d,capture_output=True,text=True);(d/f'pass{n}.stdout').write_text(r.stdout);(d/f'pass{n}.stderr').write_text(r.stderr);need(r.returncode==0,'render '+name)
   log=(d/(name+'.log')).read_text();bad=[s for s in ['Missing character','Overfull','undefined references','Undefined control sequence','LaTeX Warning: Citation','Package hyperref Warning'] if s in log];need(not bad,'render diagnostics '+name+str(bad))
   old=[p.extract_text() for p in PdfReader(ROOT/(name+'.pdf')).pages];new=[p.extract_text() for p in PdfReader(d/(name+'.pdf')).pages];need(old==new,'page text '+name)
   renders.append({'paper':name,'pages':len(old),'page_text_identical':True,'blocking_diagnostics':bad,'underfull_boxes':log.count('Underfull')})
 result={'status':'PASS','manifest_sha256':sha(ROOT/'manifest.json'),'exports':len(manifest['exports']),'source_records':81,'old_whole_scientific_inputs':len(retained['old_scientific_inputs']),'source_verified':source_verified,'scope_controls':control_rows,'programs_replayed':finite,'new_Lean_declarations':0,'complete_printed_programs':printed_rows,'appendix_control':appendix_control,'renders':renders,'elapsed_seconds':time.monotonic()-start}
 (out/'report.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
