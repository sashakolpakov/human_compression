#!/usr/bin/env python3
"""Replay four fixed end certificates; the uniform proof remains a written proof."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def require(ok,message):
 if not ok: raise ValueError(message)
def load(name):return json.loads((HERE/name).read_text())
def bind(root,row):
 b=(root/row['path']).read_bytes();require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def scope_check(s):
 require(s['original_id']=='L038' and s['source_edition']=='arXiv:1810.12450v2, 4 January 2019','source scope')
 require(s['whole_original_accepted'] is False,'whole-source overclaim')
 for k in ['new_original_credit','new_conjecture_credit','new_Lean','new_measurement']:require(s[k]==0,'credit '+k)
 require(s['finite_models']==[10,12,15,16],'finite models')
 require(s['diagnostic_degree_samples_are_premises'] is False and s['formalization_claim'] is False,'proof scope')
 require('higher ranks' in s['not_covered'] and 'degree12 rank4' in s['not_covered'],'omitted principal cases')
def gap_run(root,out,exe,code=None):
 root.mkdir();shutil.copyfile(HERE/'model.g',root/'model.g');(root/'certificate.g').write_text(code if code is not None else (HERE/'certificate.g').read_text())
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 r=subprocess.run([exe,'-q','certificate.g'],cwd=root,env=env,text=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
 (out.with_suffix('.stdout')).write_text(r.stdout);(out.with_suffix('.stderr')).write_text(r.stderr)
 return r

def main():
 require(sys.flags.optimize==0,'optimized Python is unsupported')
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--gap',default='gap');ap.add_argument('--render',action='store_true');a=ap.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 man=load('manifest.json')
 for row in man['exports']:bind(HERE,row)
 s=load('scope.json');scope_check(s);controls=[]
 for k,v in [('whole_original_accepted',True),('new_original_credit',1),('new_conjecture_credit',1),('new_Lean',1),('new_measurement',1),('diagnostic_degree_samples_are_premises',True),('formalization_claim',True),('not_covered',[])]:
  bad=copy.deepcopy(s);bad[k]=v
  try:scope_check(bad)
  except ValueError:controls.append(k)
  else:raise ValueError('scope control accepted '+k)
 ext=0
 if a.study_root:
  for row in load('dependencies.json')['bindings']:bind(a.study_root,row);ext+=1
 r=gap_run(a.out/'exact',a.out/'exact',a.gap)
 require(r.returncode==0 and not r.stderr.strip(),'GAP exact replay failed')
 require(r.stdout.split()==load('expected.json')['stdout_tokens'],'finite certificate output changed')
 require('ALL_FOUR_FINITE_CERTIFICATES_PASS' in r.stdout,'missing completion')
 code=(HERE/'certificate.g').read_text()
 mutations=[('diagonal','if j=4 then B:=Centralizer(B,(8,9)*(10,11)*(13,14));fi;',''),('parity','B:=PreImage(hom,Intersection(Image(hom),AlternatingGroup(5)));',''),('three_pairs','B:=Centralizer(Centralizer(B,(1,3)*(2,4)),(1,5)*(2,6));',''),('four_point_matching','B:=Centralizer(B,(1,4)*(2,3));',''),('pure_word','if w<>(4,9,12,14,11)','if w<>(4,9,14,12,11)')]
 negatives=[]
 for name,old,new in mutations:
  require(code.count(old)==1,'mutation target '+name)
  damaged=gap_run(a.out/('negative_'+name),a.out/('negative_'+name),a.gap,code.replace(old,new))
  require('ALL_FOUR_FINITE_CERTIFICATES_PASS' not in damaged.stdout and 'Error,' in damaged.stderr,'damaged certificate accepted '+name);negatives.append(name)
 pages=None
 if a.render:
  from pypdf import PdfReader
  native=a.out/'native';native.mkdir();shutil.copyfile(HERE/'finite_ends.tex',native/'finite_ends.tex')
  for i in [1,2]:
   run=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','finite_ends.tex'],cwd=native,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(native/f'pass{i}.log').write_text(run.stdout);require(run.returncode==0,'TeX compilation')
  log=(native/'finite_ends.log').read_text()
  for bad in ['Overfull','LaTeX Warning:','undefined references']:require(bad not in log,'native warning '+bad)
  ts=[p.extract_text()or''for p in PdfReader(native/'finite_ends.pdf').pages];nd=load('native.json');require(len(ts)==nd['pages']==7,'native page count');require([hashlib.sha256(t.encode()).hexdigest()for t in ts]==nd['page_text_sha256'],'native page text');pages=len(ts)
 report={'status':'PASS','exports':len(man['exports']),'bindings':ext,'finite_models':[10,12,15,16],'finite_subset_pairs':1600,'uniform_proof':'written; not certified by this script','scope_controls':controls,'damaged_certificate_controls':negatives,'native_pages':pages,'whole_original_accepted':False,'distinct_review':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
