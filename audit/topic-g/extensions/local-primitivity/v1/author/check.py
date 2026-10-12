#!/usr/bin/env python3
"""Whole operational binding/program/render driver, not a uniform proof premise."""
import argparse,copy,hashlib,json,re,shutil,subprocess,sys,tempfile,time
from pathlib import Path
from pypdf import PdfReader
D=Path(__file__).resolve().parent

def need(c,m):
 if not c:raise ValueError(m)
def read(n):return json.loads((D/n).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def result_ok(r):
 expected={'upper_m':10**10,'residue_cases':416666667,'proper_factor_rejections':331513606,'power_of_two_exclusions':16,'exact_modular_powers':85153045,'sieve_bound':10000,'root_classes':1222,'survivors':[],'all_cases_accounted':True}
 for k,v in expected.items():need(r.get(k)==v,'Feit semantic field '+k)
 need(r['proper_factor_rejections']+r['power_of_two_exclusions']+r['exact_modular_powers']==r['residue_cases'],'partition')
 return expected
def map_ok(m):
 required={x['id'] for x in read('plan.json')['full_contract_items']}
 rows=m['rows'];need(len(rows)==35 and {x['id'] for x in rows}==required,'source scope')
 need(all(x['disposition'] and x['current_file'] and (D/x['current_file']).is_file() for x in rows),'source routes')
 by={x['id']:x for x in rows}
 for k in ('Lemma3.5','Proposition3.7','Proposition4.3','Proposition5.8','Theorem6.1','Theorem6.2','Witt-Bose-Shrikhande','Hermitian-unitals','Classification-converses'):
  need(by[k]['disposition']==read('source_map.json')['rows'][next(i for i,x in enumerate(read('source_map.json')['rows']) if x['id']==k)]['disposition'],'correction disposition '+k)
def semantic_scope(s):
 need(s['source_id']=='L102' and s['source_pages']==22 and s['source_items']==35,'whole source')
 need(s['new_question_credit']==0 and s['new_Lean']==0 and s['measurement'] is None,'credit/formal/numeric scope')
 need(s['full_required_programs']==['small_g2_premise.g','feit_bound.cpp'],'required closure')
 need(s['retained_classification_proofs'] is True and s['whole_source_adoption'] is False,'classification/acceptance scope')
 need('unknown' in s['source_software_boundary'].lower(),'source software cannot be zero')
def controls():
 count=0
 def bad(f,x):
  nonlocal count
  try:f(x)
  except (ValueError,KeyError):count+=1;return
  raise ValueError('negative control accepted')
 r=read('feit_full_result.json')
 for k,v in [('upper_m',10**9),('residue_cases',416666666),('proper_factor_rejections',331513605),('exact_modular_powers',0),('survivors',[80]),('all_cases_accounted',False)]:
  x=copy.deepcopy(r);x[k]=v;bad(result_ok,x)
 m=read('source_map.json');x=copy.deepcopy(m);x['rows'].pop();bad(map_ok,x)
 s=read('scope.json')
 for k,v in [('source_pages',21),('new_question_credit',1),('new_Lean',1),('measurement',{'ratio':2}),('retained_classification_proofs',False),('whole_source_adoption',True),('full_required_programs',['small_g2_premise.g']),('source_software_boundary','zero')]:
  x=copy.deepcopy(s);x[k]=v;bad(semantic_scope,x)
 return count
def run(cmd,cwd,out,timeout=90):
 p=subprocess.run(list(map(str,cmd)),cwd=cwd,text=True,capture_output=True,timeout=timeout)
 out.write_text(p.stdout+p.stderr);need(p.returncode==0,'command failed '+str(cmd)+': '+p.stderr[-1000:]);return p.stdout
def texts(path):return [p.extract_text() or '' for p in PdfReader(path).pages]
def main(a):
 a.out.mkdir(parents=True,exist_ok=True);start=time.monotonic();report={'status':'RUNNING','programs':False,'render':False}
 if (D/'manifest.json').exists():
  exports=read('manifest.json')['exports']
  for x in exports:need((D/x['path']).stat().st_size==x['bytes'] and sha(D/x['path'])==x['sha256'],'export binding '+x['path'])
  report['exports']=len(exports)
 if a.study_root:
  for x in read('dependencies.json')['primary_and_prior_artifacts']:
   p=a.study_root/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'primary/prior binding '+x['path'])
  need(len(PdfReader(a.study_root/'sources/older_L102_gwdg.pdf').pages)==22,'source pages')
  report['primary_prior_bindings']=len(read('dependencies.json')['primary_and_prior_artifacts'])
 for x in read('program_inventory.json')['whole_files']:
  p=D/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'whole program/data binding '+x['path'])
 for x in read('proof_contexts.json')['contexts']:
  p=D/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'complete proof context '+x['path'])
 expected=result_ok(read('feit_full_result.json'));map_ok(read('source_map.json'));semantic_scope(read('scope.json'))
 e=read('feit_execution.json');need(e['source_sha256']==sha(D/'feit_bound.cpp'),'exact Feit executed bytes');result_ok(e['full_result'])
 need('static_assert(sizeof(unsigned long)>=8' in (D/'feit_bound.cpp').read_text(),'GMP input width guard')
 need('G2_SMALL_PREMISE|4.15.1|6048|[ 96, 96, 168, 216 ]|12096' in (D/'small_g2_premise.txt').read_text(),'G2 complete roster')
 report['controls']=controls()
 if a.programs:
  exe=a.out/'feit_bound';cmd=[a.cxx,'-O3','-std=c++17','-I'+str(a.gmp_prefix/'include'),D/'feit_bound.cpp','-L'+str(a.gmp_prefix/'lib'),'-lgmp','-o',exe]
  run(cmd,D,a.out/'compile.log')
  r=json.loads(run([exe,str(10**10)],D,a.out/'feit_full.log',120));result_ok(r)
  (a.out/'feit_full.json').write_text(json.dumps(r,indent=2)+'\n')
  g=run([a.gap,'-q','small_g2_premise.g'],D,a.out/'small_g2.log')
  need(g.replace('\r','').strip()==(D/'small_g2_premise.txt').read_text().replace('\r','').strip(),'small G2 output')
  report['programs']=True;report['Feit_exact_modular_powers']=r['exact_modular_powers']
 if a.validate:
  exe=a.out/'arithmetic_probe';run([a.cxx,'-O2','-I'+str(a.gmp_prefix/'include'),D/'check_feit_arithmetic.cpp','-L'+str(a.gmp_prefix/'lib'),'-lgmp','-o',exe],D,a.out/'probe_compile.log')
  run([sys.executable,'-B','-O',D/'validate_arithmetic.py','--probe',exe,'--out',a.out/'arithmetic_validation.json'],D,a.out/'arithmetic_validation.log')
  w=run([a.gap,'-q','check_wbs_small.g'],D,a.out/'wbs8.log');need('WBS8|1512|54|24|6|54|12|pencil_imprimitive|line_primitive' in w,'actual WBS8 roles')
  report['optional_validation']=True
 if a.render:
  build=a.out/'render';build.mkdir(exist_ok=True)
  for p in D.glob('*.tex'):shutil.copy2(p,build/p.name)
  pages={}
  for stem in ('local_actions','linear_spaces'):
   for n in (1,2):run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],build,build/(stem+f'.pass{n}.log'))
   log=(build/(stem+'.log')).read_text();need('Overfull' not in log and 'undefined' not in log and 'LaTeX Warning' not in log,'TeX diagnostics '+stem)
   old=texts(D/(stem+'.pdf'));new=texts(build/(stem+'.pdf'));need(old==new,'exact PDF page texts '+stem);pages[stem]=len(new)
  report['render']=True;report['pages']=pages
 report.update(status='PASS',source_items=35,new_Lean=0,new_question_credit=0,elapsed_seconds=time.monotonic()-start)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--programs',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');p.add_argument('--cxx',default='/usr/bin/clang++');p.add_argument('--gmp-prefix',type=Path,default=Path('/opt/homebrew'));main(p.parse_args())
