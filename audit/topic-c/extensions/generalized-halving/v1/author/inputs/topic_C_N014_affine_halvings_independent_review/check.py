"""Portable bounded independent audit; no author module imports."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys
from pypdf import PdfReader
from sympy import Matrix
P=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def audit(r):
 need(r['parameter_triples']==75 and r['literal_extra_relations']==150 and r['Coxeter_pair_checks']==240,'diagnostic extent')
 need(r['author_imports'] is False and r['uniform_proof_claim_from_samples'] is False,'diagnostic independence/scope')
 keys={(z['n'],z['s'],z['k']) for z in r['rows']}
 need(len(r['rows'])==75 and keys=={(n,s,k) for n in range(3,8) for s in range(2,7) for k in (1,2,n)},'complete parameter grid')
 for z in r['rows']:
  n,s,k=z['n'],z['s'],z['k'];need([c['operation'] for c in z['cases']]==[1,2],'both endpoint operations')
  di=(s**n//2 if s%2==0 else s**n) if k==1 else s**n if k==2 else 2**(n-2+(n*s%2))*s**n
  for c in z['cases']:
   factor=2**(n-1) if (k==1 and s%2==1 or k==n and n*s%2==1) else 2 if k==n and n%2==0 and c['operation']==2 else 1
   need(c['D_period_index']==di and c['presented_over_intended_factor']==factor,'exact lattice indices')
   L=Matrix(n,n,c['period_HNF']);R=Matrix(n,n,c['normal_lattice_HNF'])
   need(abs(L.det())==2*di and abs(R.det())==2*di*factor,'actual HNF determinants')
   need(all(x.q==1 for x in L.inv()*R),'actual integral lattice inclusion')
   v=[(1+s%2)*s]+[0]*(n-1) if k==1 else [s,s]+[0]*(n-2) if k==2 else [(1+n*s%2)*s]*n
   need(c['literal_relator_vector']==v,'literal translation vector')
 need(len(r['controls'])==4,'four arithmetic weakenings')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,default=P.parent);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 bound=read(P/'bindings.json')
 for e in bound['inputs']:
  f=a.study_root/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'external binding '+e['path'])
 if (P/'manifest.json').exists():
  for e in read(P/'manifest.json')['exports']:
   f=P/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'review export '+e['path'])
 scope=read(P/'source_scope.json');need(scope['new_original_credit']==scope['new_conjecture_credit']==scope['new_Lean']==0 and scope['measurement'] is None,'bounded acceptance')
 need(read(P/'review.json')['corrections_requested']==[],'review corrections')
 run=subprocess.run([sys.executable,'-B','-O',str(P/'check_algebra.py'),'--out',str(a.out/'algebra.json')],text=True,capture_output=True,timeout=60)
 (a.out/'algebra.stdout').write_text(run.stdout);(a.out/'algebra.stderr').write_text(run.stderr);need(run.returncode==0,'independent arithmetic replay')
 fresh=read(a.out/'algebra.json');audit(fresh);need(fresh==read(P/'algebra_result.json'),'exact independent result reproduction')
 controls=[]
 def reject(name,mutate):
  bad=copy.deepcopy(fresh);mutate(bad)
  try:audit(bad)
  except ValueError:controls.append(name);return
  raise ValueError('accepted mutation '+name)
 reject('missing parameter row',lambda r:r['rows'].pop())
 reject('missing double operation',lambda r:r['rows'][0]['cases'].pop())
 reject('wrong reported factor',lambda r:r['rows'][0]['cases'][0].__setitem__('presented_over_intended_factor',2))
 reject('wrong actual relator vector',lambda r:r['rows'][0]['cases'][0]['literal_relator_vector'].__setitem__(0,3))
 reject('wrong actual HNF determinant',lambda r:r['rows'][0]['cases'][0]['normal_lattice_HNF'].__setitem__(0,4))
 pages=0
 if a.render:
  d=a.out/'render';d.mkdir(exist_ok=True);src=a.study_root/'topic_C_N014_affine_halvings';shutil.copy2(src/'affine_halvings.tex',d/'affine_halvings.tex')
  for i in range(2):
   r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','affine_halvings.tex'],cwd=d,text=True,capture_output=True,timeout=60);(d/f'build-{i}.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'TeX render')
  log=(d/'affine_halvings.log').read_text();need(not any(x in log for x in ['LaTeX Warning','Overfull','Underfull']),'clean layout')
  old=PdfReader(str(src/'affine_halvings.pdf'));new=PdfReader(str(d/'affine_halvings.pdf'));need(len(old.pages)==len(new.pages)==4,'four pages');need([p.extract_text() for p in old.pages]==[p.extract_text() for p in new.pages],'exact four page texts');pages=4
 result={'status':'PASS_BOUNDED_INDEPENDENT_REVIEW_REPLAY','author_manifest':bound['author_manifest_sha256'],'bound_inputs':len(bound['inputs']),'parameter_triples':75,'literal_relators':150,'Coxeter_pairs':240,'arithmetic_controls':fresh['controls'],'independent_semantic_controls':controls,'rendered_pages':pages,'no_GAP_Lean_or_census':True,'uniform_acceptance_basis':'Complete written proof and exact source reading recorded separately; finite grid is supplementary.'}
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
