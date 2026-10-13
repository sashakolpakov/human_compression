#!/usr/bin/env python3
"""Check finite identities and byte bindings, not the uniform written proof."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(name):return json.loads((HERE/name).read_text())
def binding(root,row):
 b=(root/row['path']).read_bytes()
 need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def det(a):
 a=[list(map(F,r)) for r in a];v=F(1)
 for i in range(len(a)):
  j=next((j for j in range(i,len(a)) if a[j][i]),None)
  if j is None:return F(0)
  if i!=j:a[i],a[j]=a[j],a[i];v=-v
  x=a[i][i];v*=x
  for j in range(i+1,len(a)):
   y=a[j][i]/x
   for k in range(i,len(a)):a[j][k]-=y*a[i][k]
 return v
def mul(a,b):return tuple((1 if x>0 else -1)*b[abs(x)-1] for x in a)
def order(a):
 e=tuple(range(1,len(a)+1));b=e
 for n in range(1,100):
  b=mul(b,a)
  if b==e:return n
 raise ValueError('unexpected order')
def finite(expected):
 patterns=[]
 for a,b in [(3,3),(4,3),(3,4),(4,4)]:
  bonds=[a,3,3,3,b];ds=[F(1),F(1)]
  for p in bonds:ds.append(ds[-1]-F(1,4 if p==3 else 2)*ds[-2])
  patterns.append({'bonds':bonds,'determinants':[str(x) for x in ds]})
 roots=[[1,0,0,0,0],[1,-1,0,0,0],[0,1,-1,0,0],[0,0,1,-1,0],[0,0,0,1,-1],[0,0,0,0,1]]
 gram=[[sum(x*y for x,y in zip(u,v)) for v in roots]for u in roots]
 gens=[]
 for u in roots:
  n=sum(x*x for x in u);m=[[F(i==j)-F(2*u[i]*u[j],n)for j in range(5)]for i in range(5)]
  rows=[]
  for row in m:
   js=[j for j,x in enumerate(row)if x]
   need(len(js)==1 and abs(row[js[0]])==1,'model is monomial')
   rows.append(int(row[js[0]])*(js[0]+1))
  gens.append(tuple(rows))
 identity=(1,2,3,4,5);seen={identity};todo=[identity]
 for g in todo:
  for h in gens:
   z=mul(g,h)
   if z not in seen:seen.add(z);todo.append(z)
 need(len(seen)<=3840,'model too large')
 for i in range(6):
  for j in range(i+2,6):need(mul(gens[i],gens[j])==mul(gens[j],gens[i]),'distant commutation')
 actual={'patterns':patterns,'model_order':len(seen),'model_adjacent_orders':[order(mul(gens[i],gens[i+1]))for i in range(5)],'model_gram_det':str(det(gram)),'model_first_five_normalized_det':str(det([r[:5]for r in gram[:5]])/16),'omega5_order':5**4*(5**2-1)*(5**4-1)//2}
 need(actual==expected,'finite identities differ')
 return actual
def scope(s):
 need(s['original']=='F001' and s['source_edition']=='arXiv:1912.05512v1, 11 December 2019','source scope')
 need(s['fields']=='all odd prime powers q>=5' and s['involution_scope']=='all generators are negatives of reflections','theorem scope')
 need(s['rank_bound']==5,'rank bound')
 for k in ['mixed_involutions_covered','whole_odd_upper_bound_proved','whole_original_accepted','uniform_proof_formalized','new_original_credit','new_conjecture_credit','new_Lean','new_measurement']:
  need(type(s[k]) is bool and s[k] is False,'scope '+k)
 need(s['remaining']=='mixed involution types; complete F001 principal assembly','remaining scope')
def main():
 need(sys.flags.optimize==0,'optimized Python unsupported')
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');a=p.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 man=load('manifest.json')
 for row in man['exports']:binding(HERE,row)
 count=0
 if a.study_root:
  for row in load('dependencies.json')['bindings']:binding(a.study_root,row);count+=1
 s=load('scope.json');scope(s);controls=[]
 for key in ['mixed_involutions_covered','whole_odd_upper_bound_proved','whole_original_accepted','uniform_proof_formalized','new_original_credit','new_conjecture_credit','new_Lean','new_measurement']:
  bad=copy.deepcopy(s);bad[key]=True
  try:scope(bad)
  except ValueError:controls.append(key)
  else:raise ValueError('damaged scope passed '+key)
 ex=load('expected.json');actual=finite(ex);negative=[]
 for key,value in [('model_order',1920),('model_first_five_normalized_det','0')]:
  bad=copy.deepcopy(ex);bad[key]=value
  try:finite(bad)
  except ValueError:negative.append(key)
  else:raise ValueError('damaged arithmetic passed '+key)
 pages=None
 if a.render:
  from pypdf import PdfReader
  d=a.out/'native';d.mkdir();shutil.copyfile(HERE/'reflection_bound.tex',d/'reflection_bound.tex');env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
  for k in [1,2]:
   r=subprocess.run(['pdflatex','-halt-on-error','-interaction=nonstopmode','reflection_bound.tex'],cwd=d,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/f'pass{k}.log').write_text(r.stdout);need(r.returncode==0,'native build')
  log=(d/'reflection_bound.log').read_text()
  for t in ['Overfull','LaTeX Warning:','undefined references']:need(t not in log,'native warning '+t)
  ts=[p.extract_text()or'' for p in PdfReader(d/'reflection_bound.pdf').pages];ref=load('native.json');need(len(ts)==ref['pages'] and [hashlib.sha256(t.encode()).hexdigest() for t in ts]==ref['page_text_sha256'],'native changed');pages=len(ts)
 report={'status':'PASS','exports':len(man['exports']),'bindings':count,'arithmetic':actual,'scope_controls':controls,'damaged_arithmetic_controls':negative,'native_pages':pages,'uniform_proof':'written, not formally verified by this program','whole_original_accepted':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
