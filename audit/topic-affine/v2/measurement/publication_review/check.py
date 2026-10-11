#!/usr/bin/env python3
"""Bounded read-only integration review; reuse the accepted numerical audit."""
import argparse, ast, copy, hashlib, importlib.util, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
BASE = '590d0b55de9a7248bce1e879f344e034126a015d'
ADMISSION = '133528e6fb57ce3acbffaa9913e3ab7d14e329494082faf9b1bdba7eea964864'
B = 'audit/topic-affine/v2/measurement/'
PACKETS = {
 'packet': ('topic_Affine_measurement_results', 'cc69a9eef8d78fd7e3e3f1ef2db024aae70801750d5bef0a48127575facd1725'),
 'arithmetic_review': ('topic_Affine_measurement_results_independent_review', 'f035257f560a2d1fcb40d71c2c062b10b353a1a5f9ce13e04c619d9ae876ded5'),
 'root_adoption': ('topic_Affine_measurement_root_adoption', '026ad0d0ecda386dc817fe27d04cf4d344bf9df962a0f82f9b5c0a852c6aa559')}
def need(ok, message):
 if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(n): return ast.dump(n, include_attributes=False)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--public-root',type=Path,required=True); ap.add_argument('--study-root',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output report')
 root=a.public_root.resolve(); study=a.study_root.resolve(); admission=read(root/B/'admission.json')
 need(sha((root/B/'admission.json').read_bytes())==ADMISSION,'exact admission pin')
 need(admission['packet_manifests']=={k:v[1] for k,v in PACKETS.items()},'three exact frozen packet pins')
 copies=[]
 for folder,(private,pin) in PACKETS.items():
  p,q=root/B/folder,study/private
  need((p/'manifest.json').read_bytes()==(q/'manifest.json').read_bytes() and sha((p/'manifest.json').read_bytes())==pin,'exact frozen manifest '+folder)
  m=read(p/'manifest.json')
  for row in m['exports']:
   n=Path(row['path']); need(not n.is_absolute() and '..' not in n.parts,'safe export')
   b=(p/n).read_bytes(); need(b==(q/n).read_bytes() and len(b)==row['bytes'] and sha(b)==row['sha256'],'exact frozen export '+str(n))
  copies.append(dict(folder=folder,private=private,exports=len(m['exports']),manifest_sha256=pin))
 need(sum(r['exports'] for r in copies)==51,'all 51 frozen exports')
 for row in admission['artifacts']:
  p=Path(row['path']); need(not p.is_absolute() and '..' not in p.parts,'safe artifact path')
  b=(root/p).read_bytes(); need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound admission artifact')
 need(len(admission['artifacts'])==55,'all 55 admitted artifacts')
 verifier=root/'scripts/verify_snapshot.py'; spec=importlib.util.spec_from_file_location('affine_publication_snapshot',verifier); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
 need(v.check_affine_measurement()==(120,120),'positive new standard checker')
 old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
 funcs=lambda s:{n.name:n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
 oldf,newf=funcs(old),funcs(verifier.read_text()); need(set(newf)-set(oldf)=={'check_affine_measurement'} and set(oldf)<=set(newf),'only new affine numerical checker')
 prior=[n for n in oldf if n!='main']; need(len(prior)==28 and all(dump(oldf[n])==dump(newf[n]) for n in prior),'28 older functions unchanged')
 # The previous status sentence truthfully drops 'lengths remain pending'.
 expected_old=copy.deepcopy(oldf['main'])
 old_status=' scoped Lean declarations and all six complete programs; lengths remain pending.'
 replacements=0
 for n in ast.walk(expected_old):
  if isinstance(n,ast.Constant) and n.value==old_status:
   n.value=' scoped Lean declarations and all six complete programs.'; replacements+=1
 need(replacements==1,'one explicit obsolete pending-lengths status removed')
 statements={dump(n) for n in expected_old.body}; nm=copy.deepcopy(newf['main']); extras=[n for n in nm.body if dump(n) not in statements]
 need(len(extras)==2 and any('check_affine_measurement' in dump(n) for n in extras) and any('affine_fractions' in dump(n) for n in extras),'only new invocation and status print')
 nm.body=[n for n in nm.body if dump(n) in statements]; need(dump(nm)==dump(expected_old),'prior main order unchanged apart from explicit obsolete status')
 unchanged=['papers/catalogue.json','audit/intake.json','audit/source_registry.json','audit/completion.json','audit/work_queue.json','scripts/build_papers.py','research/case_study/formal/lakefile.lean','audit/topic-affine/v2/admission.json']
 for n in unchanged: need((root/n).read_bytes()==subprocess.check_output(['git','show',BASE+':'+n],cwd=root),'unchanged scientific and credit record '+n)
 binding=read(root/B/'packet/inputs/publication_binding.json'); science=[]
 for row in list(binding['documents'].values())+sum([binding[k] for k in ['complete_mathematical_programs','complete_auxiliary_scripts','complete_formal_files']],[]):
  p=row['public_path']; b=(root/p).read_bytes(); need(sha(b)==row['sha256'],'exact public science link '+p)
  need(b==subprocess.check_output(['git','show',BASE+':'+p],cwd=root),'underlying science unchanged '+p)
  science.append(dict(path=p,sha256=sha(b)))
 need(len(science)==15,'three PDFs and twelve full program/auxiliary/formal files')
 links=[]
 for n in ['README.rst',B+'README.rst']:
  for raw in re.findall(r'<([^>]+)>`_',(root/n).read_text(),re.S):
   url=''.join(raw.split())
   if re.match(r'^[a-zA-Z]+:',url) or url.startswith('#'): continue
   need(((root/n).parent/url.split('#')[0]).exists(),'working local reader link '+n+' -> '+url); links.append(dict(document=n,target=url))
 for n in [B+'README.rst',B+'packet/README.rst']:
  for raw in re.findall(r'^\.\. image::\s*(\S+)',(root/n).read_text(),re.M):
   need(((root/n).parent/raw).exists(),'working image directive '+raw)
 controls=[]
 with tempfile.TemporaryDirectory(prefix='affine-measurement-publication-') as tmp:
  temp=Path(tmp)
  for n in {r['path'] for r in admission['artifacts']}|{B+'admission.json'}:
   p=temp/n; p.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(root/n,p)
  v.ROOT=temp
  for name,n in [('numerical_result_bytes',B+'packet/results.json'),('independent_review_bytes',B+'arithmetic_review/review.json'),('frozen_reader_bytes',B+'packet/measurement.pdf')]:
   p=temp/n; b=p.read_bytes(); p.write_bytes(b+b'\n')
   try: v.check_affine_measurement()
   except (ValueError,KeyError) as e: controls.append(dict(name=name,mode='copied file mutation',rejected=True,reason=str(e)))
   else: raise ValueError('accepted corrupt artifact '+name)
   p.write_bytes(b)
 v.ROOT=root; actual=v.load
 fields=['source_contract_rows','principal_contracts','project_total_preserved','policy_coordinates','metric_cells','normalized_text_hashes','required_program_metric_cells','auxiliary_metric_cells','formal_metric_cells','exact_combined_fractions','exact_conditional_fractions','complete_required_programs','complete_auxiliary_scripts_separate','complete_formal_files_separate','existing_Lean_declarations']
 cases=['summary:'+f for f in fields]+['wrong_source','wrong_review','deny_input_review','deny_adoption','changed_input_pin','missing_program','missing_auxiliary','missing_formal','changed_public_PDF','changed_primary','changed_conditional','invent_external_cost','claim_full_formalization','claim_paired_dependencies','new_source_credit','new_question_credit','new_formal_credit']
 for name in cases:
  overrides={}; ad=copy.deepcopy(admission)
  def edit(n):
   if n not in overrides: overrides[n]=actual(n)
   return overrides[n]
  if name.startswith('summary:'): ad[name.split(':',1)[1]]=-1
  elif name=='wrong_source': ad['source_ids']=['L014']
  elif name=='wrong_review': edit(B+'arithmetic_review/review.json')['author_manifest_sha256']='0'*64
  elif name=='deny_input_review': edit(B+'packet/independent/review.json')['status']='REJECTED'
  elif name=='deny_adoption': edit(B+'root_adoption/review.json')['status']='REJECTED'
  elif name=='changed_input_pin': ad['input_manifest_sha256']='0'*64
  elif name in ['missing_program','missing_auxiliary','missing_formal']:
   cat={'missing_program':'complete_mathematical_programs','missing_auxiliary':'complete_auxiliary_scripts','missing_formal':'complete_formal_files'}[name]
   edit(B+'packet/results.json')[cat].pop()
  elif name=='changed_public_PDF': edit(B+'packet/inputs/publication_binding.json')['documents']['U_Affine']['public_path']='papers/topic-affine/v2/mixed-prime-polyhedra.pdf'
  elif name=='changed_primary': ad['primary']['written_denominator']-=1
  elif name=='changed_conditional': edit(B+'packet/results.json')['primary']['per_result'][0]['denominator']-=1
  elif name=='invent_external_cost': ad['unknown_external_costs']['retained_external_proofs']=0
  elif name=='claim_full_formalization': ad['source_specific_formalization']=True
  elif name=='claim_paired_dependencies': ad['paired_dependency_audit_complete']=True
  else: ad[name]=1
  overrides[B+'admission.json']=ad; v.load=lambda p:copy.deepcopy(overrides[p]) if p in overrides else actual(p)
  try: v.check_affine_measurement()
  except (ValueError,KeyError,IndexError) as e: controls.append(dict(name=name,mode='in-memory semantic guard isolation',rejected=True,reason=str(e)))
  else: controls.append(dict(name=name,rejected=False))
  finally: v.load=actual
 need(all(c['rejected'] for c in controls),'accepted corruption '+repr([c for c in controls if not c['rejected']]))
 need(not subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR',BASE,'--','*.md'],cwd=root,text=True).strip(),'no Markdown exported')
 ws=subprocess.run(['git','diff','--cached','--check',BASE],cwd=root,text=True,capture_output=True)
 warnings=re.findall(r'^([^:\n]+):\d+: trailing whitespace\.$',ws.stdout,re.M)
 allowed={B+'packet/costs.svg':798,B+'packet/inputs/extract_inputs.py':1}
 need({p:warnings.count(p) for p in set(warnings)}==allowed,'only exact frozen whitespace exceptions')
 files=['scripts/verify_snapshot.py','README.rst','audit/protocol.tex','audit/protocol.pdf',B+'admission.json',B+'README.rst']
 report=dict(status='PASS_BOUNDED_AFFINE_MEASUREMENT_PUBLICATION',baseline_commit=BASE,admission_sha256=ADMISSION,copies=copies,frozen_exports=51,admission_artifacts=55,positive_checker=[120,120],old_non_main_functions_preserved=28,prior_main_order_preserved=True,unchanged_scientific_and_credit_records=unchanged,public_science_links=science,reader_links=links,controls=controls,frozen_whitespace_exceptions=[dict(path=p,occurrences=n,sha256=sha((root/p).read_bytes())) for p,n in allowed.items()],bound_public_files=[dict(path=n,bytes=(root/n).stat().st_size,sha256=sha((root/n).read_bytes())) for n in files],scope='Publication integration only; the accepted input, mathematical, and independent numerical/reader reviews are reused. No source extraction, font audit, GAP or Lean replay.',roles='Reviewer authored the original measurement inputs and independent numerical review; root authored their acceptance/numerical packet and this public integration. This is not a fresh independent re-audit of those inputs or numerical results.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,public_files_modified_by_reviewer=False)
 a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(status=report['status'],frozen_exports=51,controls=len(controls),public_science_links=len(science))))
if __name__=='__main__': main()
