#!/usr/bin/env python3
"""Replay bounded premises; the uniform proof is written, not machine formalized."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(b,s):
 if not b:raise ValueError(s)
def load(s):return json.loads((HERE/s).read_text())
def bind(root,row):
 b=(root/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def scope(s):
 need(s['original']=='F001' and s['source_edition']=='arXiv:1912.05512v1, 11 December 2019','source scope')
 for k in ['whole_original_accepted','odd_upper_bound_proved','new_original_credit','new_conjecture_credit','new_Lean','new_measurement','uniform_theorem_formally_verified']:
  need(s[k] is False or type(s[k]) is int and s[k]==0,'scope '+k)
 need(s['odd_positive_ranks']==[3,4,5] and s['odd_positive_fields']=='all odd prime powers q>=5','positive scope')
 need(s['exceptional_q3']=='all ranks excluded by complete finite extension certificate','exceptional scope')
 need(s['small_fields']==[5,7,9,11] and s['finite_subset_pairs']==4096,'finite scope')
 need(s['parameter_fields']==[13,17,19,23,25,27,29,31] and s['uniform_threshold']==33,'uniform scope')
 need(s['remaining_principal_obligation']=='rank upper bound for Omega(5,q), odd q>=5; complete source assembly and distinct review','remaining obligation')
def gaprun(path,exe,model,code):
 path.mkdir();(path/'finite_model.g').write_text(model);(path/'finite_certificate.g').write_text(code)
 p=subprocess.run([exe,'-q','-b','--quitonbreak','finite_certificate.g'],cwd=path,text=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 (path/'stdout.log').write_text(p.stdout);(path/'stderr.log').write_text(p.stderr);return p
def main():
 need(sys.flags.optimize==0,'optimized Python is unsupported')
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--study-root',type=Path);ap.add_argument('--gap',default='gap');ap.add_argument('--render',action='store_true');a=ap.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 man=load('manifest.json')
 for row in man['exports']:bind(HERE,row)
 ext=0
 if a.study_root:
  for row in load('dependencies.json')['bindings']:bind(a.study_root,row);ext+=1
 s=load('scope.json');scope(s);sc=[]
 mutations=[('whole_original_accepted',True),('odd_upper_bound_proved',True),('new_original_credit',1),('new_conjecture_credit',1),('new_Lean',1),('new_measurement',1),('uniform_theorem_formally_verified',True),('odd_positive_fields','all finite fields'),('exceptional_q3','rank three only'),('remaining_principal_obligation','none')]
 for k,v in mutations:
  bad=copy.deepcopy(s);bad[k]=v
  try:scope(bad)
  except ValueError:sc.append(k)
  else:raise ValueError('scope control accepted '+k)
 model=(HERE/'finite_model.g').read_text();code=(HERE/'finite_certificate.g').read_text();p=gaprun(a.out/'exact',a.gap,model,code)
 need(p.returncode==0 and not p.stderr.strip(),'finite GAP replay');need(p.stdout.split()==load('expected.json')['stdout_tokens'],'finite output changed');need('ALL_F001_ODD_CERTIFICATES_PASS' in p.stdout,'completion missing')
 neg=[]
 for name,target,old,new,driver in [
  ('wrong_full_order','code','q^4*(q^2-1)*(q^4-1)/2','q^4*(q^2-1)*(q^4-1)',code),
  ('wrong_subset_intersection','model','Position(sets,Intersection(sets[i],sets[j]))','Position(sets,Union(sets[i],sets[j]))',code),
  ('wrong_exhaustion_count','model','nodes=[2,13,121,20,2,0,0,0,0,0,0,0,0,0]','nodes=[2,13,120,20,2,0,0,0,0,0,0,0,0,0]','Read("finite_model.g");; F001Q3Exhaust();; Print("ALL_F001_ODD_CERTIFICATES_PASS\\n");; QUIT_GAP(0);\n')]:
  original=code if target=='code' else model;need(original.count(old)==1,'mutation target '+name)
  bm=model.replace(old,new) if target=='model' else model
  bc=driver.replace(old,new) if target=='code' else driver
  q=gaprun(a.out/('negative_'+name),a.gap,bm,bc)
  need('ALL_F001_ODD_CERTIFICATES_PASS' not in q.stdout and 'Error,' in q.stderr,'damaged certificate accepted '+name);neg.append(name)
 pages=None
 if a.render:
  from pypdf import PdfReader
  d=a.out/'native';d.mkdir();shutil.copyfile(HERE/'odd_endpoints.tex',d/'odd_endpoints.tex')
  env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
  for i in [1,2]:
   q=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','odd_endpoints.tex'],cwd=d,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/f'pass{i}.log').write_text(q.stdout);need(q.returncode==0,'TeX build')
  log=(d/'odd_endpoints.log').read_text()
  for bad in ['Overfull','LaTeX Warning:','undefined references']:need(bad not in log,'native warning '+bad)
  texts=[p.extract_text()or'' for p in PdfReader(d/'odd_endpoints.pdf').pages];ref=load('native.json');need(len(texts)==ref['pages'],'page count');need([hashlib.sha256(t.encode()).hexdigest()for t in texts]==ref['page_text_sha256'],'native text');pages=len(texts)
 report={'status':'PASS','exports':len(man['exports']),'bindings':ext,'finite_subset_pairs':4096,'small_fields':[5,7,9,11],'parameter_fields':[13,17,19,23,25,27,29,31],'q3_prefix_counts':[2,13,121,20,2],'q3_generating_markings':0,'scope_controls':sc,'damaged_certificate_controls':neg,'native_pages':pages,'uniform_proof':'written, not formally verified by this script','odd_upper_bound_proved':False,'whole_original_accepted':False,'distinct_review':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
