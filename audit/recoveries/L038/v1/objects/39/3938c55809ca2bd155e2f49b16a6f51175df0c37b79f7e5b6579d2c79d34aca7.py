#!/usr/bin/env python3
"""Replay the two finite premises; the uniform argument remains written."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(b,s):
 if not b:raise ValueError(s)
def load(s):return json.loads((HERE/s).read_text())
def bind(root,row):
 b=(root/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def scope(s):
 need(s['original']=='L038' and s['source_edition']=='arXiv:1810.12450v2, 4 January 2019','source scope')
 for k in ['whole_original_accepted','new_original_credit','new_conjecture_credit','new_Lean','new_measurement','diagnostics_are_premises','uniform_theorem_formally_verified']:need(s[k] is False or type(s[k]) is int and s[k]==0,'scope '+k)
 need(s['maximal_odd_seed']=='retained prior theorem, not proved here','maximal seed scope')
 need(s['finite_premises']==[[2,5],[4,7]] and s['finite_subset_pairs']==1280,'finite scope')
 need(s['remaining_principal_integration']==['contraction interfaces','A12 witnesses','whole-source distinct review'],'principal omissions')
def gaprun(path,exe,code):
 path.mkdir();shutil.copyfile(HERE/'signed_model.g',path/'signed_model.g');(path/'signed_certificate.g').write_text(code)
 p=subprocess.run([exe,'-q','signed_certificate.g'],cwd=path,text=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
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
 for k,v in [('whole_original_accepted',True),('new_original_credit',1),('new_conjecture_credit',1),('new_Lean',1),('new_measurement',1),('diagnostics_are_premises',True),('uniform_theorem_formally_verified',True),('maximal_odd_seed','proved here'),('remaining_principal_integration',[])]:
  bad=copy.deepcopy(s);bad[k]=v
  try:scope(bad)
  except ValueError:sc.append(k)
  else:raise ValueError('scope control accepted '+k)
 code=(HERE/'signed_certificate.g').read_text();p=gaprun(a.out/'exact',a.gap,code)
 need(p.returncode==0 and not p.stderr.strip(),'finite GAP replay');need(p.stdout.split()==load('expected.json')['stdout_tokens'],'finite output changed');need('ALL_SIGNED_CAP_CERTIFICATES_PASS' in p.stdout,'completion missing')
 mutations=[('wrong_group_order','Size(full)=2^(t-1)*Factorial(t)','Size(full)=2^t*Factorial(t)'),('wrong_cube','(s[p-1]*s[p])^3=f','(s[p-1]*s[p])^3=()'),('wrong_subset','Position(sets,Intersection(sets[I],sets[J]))','Position(sets,Union(sets[I],sets[J]))'),('wrong_prefix','Group(s{[1..p+1]})=M','Group(s{[1..p]})=M')]
 neg=[]
 for name,old,new in mutations:
  need(code.count(old)==1,'mutation target '+name);q=gaprun(a.out/('negative_'+name),a.gap,code.replace(old,new));need('ALL_SIGNED_CAP_CERTIFICATES_PASS' not in q.stdout and 'Error,' in q.stderr,'damaged certificate accepted '+name);neg.append(name)
 pages=None
 if a.render:
  from pypdf import PdfReader
  d=a.out/'native';d.mkdir();shutil.copyfile(HERE/'signed_ends.tex',d/'signed_ends.tex')
  env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
  for i in [1,2]:
   q=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','signed_ends.tex'],cwd=d,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/f'pass{i}.log').write_text(q.stdout);need(q.returncode==0,'TeX build')
  log=(d/'signed_ends.log').read_text()
  for bad in ['Overfull','LaTeX Warning:','undefined references']:need(bad not in log,'native warning '+bad)
  texts=[p.extract_text()or'' for p in PdfReader(d/'signed_ends.pdf').pages];ref=load('native.json');need(len(texts)==ref['pages'],'page count');need([hashlib.sha256(t.encode()).hexdigest()for t in texts]==ref['page_text_sha256'],'native text');pages=len(texts)
 report={'status':'PASS','exports':len(man['exports']),'bindings':ext,'finite_subset_pairs':1280,'finite_premises':[[2,5],[4,7]],'scope_controls':sc,'damaged_certificate_controls':neg,'native_pages':pages,'uniform_proof':'written, not formally verified by this script','whole_original_accepted':False,'distinct_review':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
