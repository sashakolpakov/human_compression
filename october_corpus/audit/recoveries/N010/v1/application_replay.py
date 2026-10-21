"""Explicit source-free public adapter; unchanged author validation function."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
import argparse,copy,importlib.util,json,os,shutil,subprocess
from pathlib import Path
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 S=a.study.resolve();P=a.author.resolve();O=a.out.resolve();need(not O.exists()and not O.is_relative_to(P),'Fresh external output')
 spec=importlib.util.spec_from_file_location('accepted_n010_author',P/'check.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);validate=module.validate
 source=load(S/'reboot_20261013/N010_work/source_contract02.json');retained=load(S/'reboot_20261013/N010_retained_inputs/register01/retained_register.json')
 register=load(P/'claim_register.json');scope=load(P/'scope.json');acquired=load(P/'acquired_packets.json');manuscripts=load(P/'acquired_manuscripts.json')
 counts=validate(register,scope,source,retained,acquired,manuscripts)
 cases=['omit_context','omit_clause','lose_question','lose_secondary','lose_bibliography','promote_global_census','invent_corrected_total','declare_currently_open','solve_general_twogroup','solve_all_chiral_ranks','credit_old_sporadic','promote_retained_classification','abridge_component','invent_formalization','promote_source_claim','promote_rank_distinction','lose_rank_distinction_route']
 controls=[]
 for case in cases:
  rr,ss,aa,mm=copy.deepcopy((register,scope,acquired,manuscripts))
  if case=='omit_context':rr['contexts'].pop()
  elif case=='omit_clause':rr['established_clauses'].pop()
  elif case=='lose_question':rr['questions'].pop()
  elif case=='lose_secondary':rr['secondary_records'].pop()
  elif case=='lose_bibliography':rr['source_bibliography'].pop(next(iter(rr['source_bibliography'])))
  elif case=='promote_global_census':ss['global_aggregates_reproduced']=True
  elif case=='invent_corrected_total':rr['corrected_global_total']=400
  elif case=='declare_currently_open':rr['source_questions_asserted_currently_open']=True
  elif case=='solve_general_twogroup':rr['questions'][29]['synthesis_status']='Solved completely'
  elif case=='solve_all_chiral_ranks':rr['questions'][31]['synthesis_status']='Solved completely'
  elif case=='credit_old_sporadic':rr['questions'][30]['new_question_credit']=1
  elif case=='promote_retained_classification':rr['established_clauses'][16]['disposition']='REPROVED'
  elif case=='abridge_component':mm['immediate_components'][0]['complete']=False
  elif case=='invent_formalization':rr['new_Lean_declarations']=1
  elif case=='promote_source_claim':rr['established_clauses'][21]['claim']='The corrected global total is441'
  elif case=='promote_rank_distinction':rr['established_clauses'][-1]['disposition']='REPROVED'
  else:rr['contexts'][6]['rows']='R20--R23'
  try:validate(rr,ss,source,retained,aa,mm)
  except(ValueError,KeyError):controls.append(case)
  else:raise ValueError('Damaged source join accepted '+case)
 from pypdf import PdfReader
 def text(p):return [page.extract_text()for page in PdfReader(p).pages]
 expected=text(P/'principal.pdf');need(len(expected)==11 and '\n\f\n'.join(expected)==(P/'principal_expected.txt').read_text(),'Exact eleven synthesis pages')
 full=expected[:]
 for row in manuscripts['immediate_components']:
  part=text(S/row['pdf']['path']);need(len(part)==row['pages'],'Full component page range');full.extend(part)
 need(len(full)==22 and text(P/'principal_and_components.pdf')==full,'Complete22page immediate reading volume')
 O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';env['XDG_CACHE_HOME']=str(O/'font-cache');guards=[]
 for script in [P/'check.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   target=O/(script.name+'_'+mode);cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(script),'--out',str(target)];e=dict(env)
   if mode=='environment':e['PYTHONOPTIMIZE']='1'
   p=subprocess.run(cmd,env=e,capture_output=True,timeout=15);(O/(script.name+'_'+mode+'.stderr')).write_bytes(p.stderr)
   need(p.returncode!=0 and b'Python'in p.stderr and not target.exists(),'Pre-output optimization guard');guards.append([script.name,mode])
 N=O/'native';N.mkdir()
 for name in ['principal.tex','context_table.tex','question_table.tex','secondary_table.tex']:shutil.copyfile(P/name,N/name)
 for i in [1,2]:
  p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','principal.tex'],cwd=N,env=env,capture_output=True,timeout=60);(N/f'pass{i}.stdout').write_bytes(p.stdout);(N/f'pass{i}.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'Native build')
 need(text(N/'principal.pdf')==expected,'Exact native text/page identity');log=(N/'principal.log').read_text();need(not any(x in log for x in ['Overfull','Underfull','LaTeX Warning:','undefined references']),'Clean native log')
 p=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r90','-sOutputFile=page-%02d.png','principal.pdf'],cwd=N,env=env,capture_output=True,timeout=60)
 need(p.returncode==0 and not p.stderr and len(list(N.glob('page-*.png')))==11,'All eleven native rasters')
 report=dict(status='PASS_PUBLIC_N010_APPLICATION',counts=counts,damaged_controls=controls,optimization_guards=guards,
 synthesis_pages=11,acquired_components=4,acquired_pages=11,full_reading_volume_pages=22,native_pages=11,
 native_text_identical=True,unchanged_author_validate=True,runtime_text_patching=False,original_source_assets_accessed=False,
 original_source_inventory='Acquired exact distinct source inventory; not rerun without omitted original documentary TeX.',
 acquired_censuses_repeated=False,mathematical_proof_checked_by_this_program=False,whole_original_credit=0,
 new_question_credit=0,new_Lean=0,new_measurements=0)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
