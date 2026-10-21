#!/usr/bin/env python3
"""Replay exact integral words, exports and scope; not a formal proof checker."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
from arithmetic import run,need
HERE=Path(__file__).resolve().parent

def load(p):return json.loads((HERE/p).read_text())
def binding(root,r):
 b=(root/r['path']).read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'binding '+r['path'])
def scope(s):
 need(s['original']=='N012' and s['source_part']=='Chapter 2, Theorem 2.2.1, pp.20--29','source scope')
 need(s['domain']=='integer dimensions n>=2','domain')
 need(s['GL_admissible']=='n>=5' and s['PGL_admissible']=='n=2 or n>=5','classification')
 need(s['uniform_certificate']=='eight distinct abstract labels for all n>=8; n7 handled separately','uniform scope')
 need(s['retained_exclusions']==['PSL3(2)','PSL4(2)'],'retained facts')
 for k in ['whole_N012_accepted','finite_H_classification_proved','marked_polytope_types_proved','new_original_credit','new_conjecture_credit','new_Lean','new_measurement','formalized']:
  need(type(s[k])is bool and s[k]is False,'scope '+k)
def main():
 need(sys.flags.optimize==0,'optimized Python unsupported')
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 m=load('manifest.json')
 for r in m['exports']:binding(HERE,r)
 bound=0
 if a.study_root:
  for r in load('dependencies.json')['bindings']:binding(a.study_root,r);bound+=1
 sc=load('scope.json');scope(sc);controls=[]
 for k in ['whole_N012_accepted','finite_H_classification_proved','marked_polytope_types_proved','new_original_credit','new_conjecture_credit','new_Lean','new_measurement','formalized']:
  bad=copy.deepcopy(sc);bad[k]=True
  try:scope(bad)
  except ValueError:controls.append(k)
  else:raise ValueError('damaged scope accepted '+k)
 actual=run();expected=load('expected.json');need(actual==expected,'displayed integral identities differ')
 damaged=[]
 for label,path,value in [('n6 root',['n6','R',0,2],2),('n7 cancellation',['n7','unit',0,2],2),('uniform wrap sign',['uniform','-1','X',1,2],1),('root orbit',['n6_root_orbit'],29)]:
  b=copy.deepcopy(expected);v=b
  for k in path[:-1]:v=v[k]
  v[path[-1]]=value
  try:need(actual==b,'damaged certificate')
  except ValueError:damaged.append(label)
  else:raise ValueError('damaged arithmetic passed')
 (a.out/'arithmetic.json').write_text(json.dumps(actual,indent=2)+'\n')
 pages=None
 if a.render:
  from pypdf import PdfReader
  d=a.out/'native';d.mkdir();shutil.copyfile(HERE/'integral_groups.tex',d/'integral_groups.tex');env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
  for k in (1,2):
   r=subprocess.run(['pdflatex','-halt-on-error','-interaction=nonstopmode','integral_groups.tex'],cwd=d,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/f'pass{k}.log').write_text(r.stdout);need(r.returncode==0,'native build')
  log=(d/'integral_groups.log').read_text()
  for t in ['Overfull','LaTeX Warning:','undefined references']:need(t not in log,'native warning '+t)
  ts=[x.extract_text()or''for x in PdfReader(d/'integral_groups.pdf').pages];n=load('native.json');need(len(ts)==n['pages'] and [hashlib.sha256(t.encode()).hexdigest()for t in ts]==n['page_text_sha256'],'native edition');pages=len(ts)
 count=sum(len(actual[k])for k in ['n2','n5','n6','n6_permutations','n7'])+sum(len(v)for v in actual['uniform'].values())+1
 out={'status':'PASS','exports':len(m['exports']),'bindings':bound,'displayed_matrix_and_orbit_records':count,'n6_root_positions':30,'universal_sign_cases':2,'universal_support':'eight abstract labels, not a selected concrete dimension','scope_controls':controls,'damaged_certificate_controls':damaged,'native_pages':pages,'whole_N012_accepted':False,'uniform_proof_formalized':False}
 (a.out/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
