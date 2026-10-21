"""Run the unchanged integer certificate and rebuild the accepted two-page proof."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,time
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();S=a.study.resolve();O=a.out.resolve();need(not O.exists()and not O.is_relative_to(S),'Fresh external output')
 A=S/'corpus106_L036_orbit_bound_v1';V=S/'corpus106_L036_orbit_bound_independent_review';old=load(V/'fresh_report.json');independent=load(V/'independent.json')
 need(old['status']=='PASS_L036_PRINCIPAL_BOUND'and old['native_pages']==2 and all(x['returncode']==0 for x in old['commands']),'Accepted completed author replay')
 need(independent['status']=='PASS_INDEPENDENT_L036_REVIEW_CONTROLS'and independent['cycle_types']==138 and independent['permutation_elements']==790 and independent['lower_bound']==50669 and independent['exact_total']is None,'Acquired independent controls only')
 O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';commands=[];start=time.monotonic()
 def run(label,cmd,cwd=None):
  t=time.monotonic()
  try:p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=60)
  except subprocess.TimeoutExpired as e:
   (O/(label+'.stdout')).write_bytes(e.stdout or b'');(O/(label+'.stderr')).write_bytes(e.stderr or b'');raise
  (O/(label+'.stdout')).write_bytes(p.stdout);(O/(label+'.stderr')).write_bytes(p.stderr);commands.append(dict(label=label,command=cmd,returncode=p.returncode,seconds=time.monotonic()-t));need(p.returncode==0 and not p.stderr,'Clean '+label)
 run('arithmetic',[sys.executable,'-B',str(A/'arithmetic.py'),'--out',str(O/'arithmetic.json')]);got=load(O/'arithmetic.json');need(got==load(A/'expected.json'),'Exact integer arithmetic and six controls')
 guards=[]
 for program in [A/'check.py',A/'arithmetic.py',V/'independent.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   target=O/(program.stem+'_'+mode);ee=dict(env)
   if mode=='environment':ee['PYTHONOPTIMIZE']='1'
   p=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(program),'--out',str(target)],env=ee,capture_output=True,timeout=15)
   (O/(program.stem+'_'+mode+'.stderr')).write_bytes(p.stderr);need(p.returncode!=0 and b'Ordinary Python required'in p.stderr and not target.exists(),'Pre-output optimization guard');guards.append([program.name,mode])
 from pypdf import PdfReader
 texts=lambda p:[x.extract_text()for x in PdfReader(p).pages]
 N=O/'native';N.mkdir();shutil.copyfile(A/'orbit_bound.tex',N/'orbit_bound.tex');need(not re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(N/'orbit_bound.tex').read_text()),'Complete native inputs')
 for i in [1,2]:run('latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode','orbit_bound.tex'],N)
 need(texts(N/'orbit_bound.pdf')==texts(A/'orbit_bound.pdf')and len(texts(N/'orbit_bound.pdf'))==2,'Exact complete native text');need(not any(x in(N/'orbit_bound.log').read_text()for x in ['Warning','Overfull','Underfull']),'Clean native')
 run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','orbit_bound.pdf'],N)
 pages=sorted(N.glob('page-*.png'));need(len(pages)==2,'Both pages');oldnative=S/'reboot_20261013/L036_orbit_bound_distinct/fresh01/native';need(all(sha(p)==sha(oldnative/p.name)for p in pages),'Identical directly viewed distinct pages')
 report=dict(status='PASS_PUBLIC_L036_APPLICATION',lower_bound=50669,source_total=1511,exact_corrected_total=None,small_action_controls=len(got['small_action_controls']),acquired_independent_cycle_types=138,acquired_independent_elements=790,independent_controls_replayed=False,independent_script_has_historical_paths=True,optimization_guards=guards,native_pages=2,native_text_identical=True,native_rasters_equal_review=True,native_raster_sha256=[sha(p)for p in pages],commands=commands,author_scientific_code_unchanged=True,runtime_text_patching=False,private_fallback=False,general_proofs_verified_by_program=False,group_classification_verified_by_program=False,whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-start)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
