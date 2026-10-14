"""Explicit public-input adapter; unchanged source-join validation function."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
import argparse,copy,json,os,shutil,subprocess
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);x=ap.parse_args();S=x.study.resolve();P=x.author.resolve();O=x.out.resolve();need(not O.exists()and not O.is_relative_to(P),'Fresh external output');O.mkdir(parents=True)
 sys.path.insert(0,str(P));from check_register import validate
 a=load(P/'claim_register.json');c=load(P/'coverage.json');m=load(P/'acquired_packets.json');scope=load(P/'scope.json');g=load(S/'corpus106_L052_residue_theory_v1/scope.json');f=load(S/'corpus106_L052_finite_v1/finite_source_map.json');literal=load(S/'corpus106_L052_finite_v1/final_literal_report.json');source=load(S/'corpus106_L052_finite_v1/source_contract01.json')
 counts=validate(a,c,m,scope,g,f,literal,source)
 controls=[]
 for case in ['omit_named_clause','lose_table_row','wrong_chiral_chambers','restore_false_group_name','false_A6_Cplus','drop_retained_input','claim_chiral_completeness','new_old_question_credit','remove_two_orbits','automatic_Cplus_geometry','wrong_A6_intersection','pending_component','invent_acquisition']:
  aa,cc,mm,ss=copy.deepcopy((a,c,m,scope));by={r['id']:r for r in aa['claims']}
  if case=='omit_named_clause':aa['claims'].remove(by['N8.2'])
  elif case=='lose_table_row':cc['finite_rows'].pop()
  elif case=='wrong_chiral_chambers':by['T2.4']['chambers']=168
  elif case=='restore_false_group_name':by['T2.7']['corrected_group']='A5 x S4'
  elif case=='false_A6_Cplus':by['C_A6_rotation']['status']='ACCEPTED_CPLUS_EXAMPLE'
  elif case=='drop_retained_input':aa['retained_inputs'].pop()
  elif case=='claim_chiral_completeness':by['Qtable1-completeness']['status']='NEW_COMPLETE_CLASSIFICATION'
  elif case=='new_old_question_credit':aa['questions'][2]['new_question_credit']=1
  elif case=='remove_two_orbits':aa['principal_hypotheses']['Cplus_converse_requires_exactly_two_chamber_orbits']=False
  elif case=='automatic_Cplus_geometry':aa['principal_hypotheses']['Cplus_converse_requires_hypertope']=False
  elif case=='wrong_A6_intersection':by['C_A6_rotation']['evidence']['intersection_order']=5
  elif case=='pending_component':mm['components'][1]['review_state']='PENDING'
  else:aa['retained_inputs'][1]['full_primary_reacquisition_claimed']=True
  try:validate(aa,cc,mm,ss,g,f,literal,source)
  except (ValueError,KeyError):controls.append(case)
  else:raise ValueError('Damaged source join accepted '+case)

 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';guards=[]
 for script in [P/'check.py',P/'check_register.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(script),'--out',str(O/(script.name+mode))];e=dict(env)
   if mode=='environment':e['PYTHONOPTIMIZE']='1'
   r=subprocess.run(cmd,env=e,capture_output=True,timeout=15);(O/(script.name+mode+'.stderr')).write_bytes(r.stderr);need(r.returncode!=0 and b'optimiz'in r.stderr.lower()and not(O/(script.name+mode)).exists(),'Pre-output optimization guard');guards.append([script.name,mode])
 from pypdf import PdfReader
 def texts(p):return [page.extract_text()for page in PdfReader(p).pages]
 full=texts(P/'principal.pdf');need(len(full)==5,'Five synthesis pages');inventory=load(P/'acquired_manuscripts.json')['manuscripts'];need([r['pages']for r in inventory]==[8,5],'Two complete acquired manuscripts')
 for row in inventory:
  pages=texts(S/row['pdf']['path']);need(len(pages)==row['pages'],'Complete acquired page range');full.extend(pages)
 need(len(full)==18 and texts(P/'complete_proof.pdf')==full,'Exact18page reading volume')
 N=O/'native';N.mkdir();shutil.copyfile(P/'principal.tex',N/'principal.tex')
 for i in [1,2]:
  r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','principal.tex'],cwd=N,env=env,capture_output=True,timeout=60);(N/f'pass{i}.stdout').write_bytes(r.stdout);(N/f'pass{i}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'Native build')
 pages=texts(N/'principal.pdf');need(len(pages)==5 and '\n\f\n'.join(pages)==(P/'principal_expected.txt').read_text(),'Exact fresh native text');log=(N/'principal.log').read_text();need(not any(t in log for t in ['Overfull','Underfull','LaTeX Warning:','undefined references']),'Clean final native log')
 r=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','principal.pdf'],cwd=N,env=env,capture_output=True,timeout=60);need(r.returncode==0 and not r.stderr,'All native rasters');need(len(list(N.glob('page-*.png')))==5,'Five native rasters')
 report=dict(status='PASS_PUBLIC_L052_APPLICATION',counts=counts,damaged_controls=controls,optimization_guards=guards,acquired_manuscripts=2,acquired_pages=13,synthesis_pages=5,full_reading_volume_pages=18,native_pages=5,native_text_identical=True,unchanged_author_mathematical_code=True,original_source_assets_accessed=False,acquired_census_repeated=False,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
