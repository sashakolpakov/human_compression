#!/usr/bin/env python3
"""Portable exact replay. GAP kernel certificate is mandatory; rendering optional."""
from pathlib import Path
import argparse,copy,hashlib,json,subprocess,sys,time
sys.dont_write_bytecode=True
from certificate import audit,kernel_check,ensure,R
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def page_text(p):
 from pypdf import PdfReader
 return [x.extract_text() for x in PdfReader(p).pages]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');ap.add_argument('--study-root',type=Path);ns=ap.parse_args();ns.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 if (HERE/'manifest.json').exists():
  for row in json.loads((HERE/'manifest.json').read_text())['exports']:
   p=HERE/row['path'];ensure(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen export '+row['path'])
 if ns.study_root:
  for row in json.loads((HERE/'scope.json').read_text())['retained_bindings']:
   p=ns.study_root/row['path'];ensure(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'retained input '+row['path'])
 proc=subprocess.run([ns.gap,'-q',str(HERE/'kernel_certificate.g')],text=True,capture_output=True,timeout=60)
 (ns.out/'kernel.stdout').write_text(proc.stdout);(ns.out/'kernel.stderr').write_text(proc.stderr)
 ensure(proc.returncode==0 and not proc.stderr.strip(),'GAP kernel replay')
 k=json.loads(proc.stdout);report=audit(k);controls=[]
 def reject(name,x):
  try:kernel_check(x)
  except (ValueError,KeyError,IndexError):controls.append(name);return
  raise ValueError('accepted bad control '+name)
 x=copy.deepcopy(k);x['kernel_relators'].pop();reject('missing_commutator_does_not_identify_Z3',x)
 x=copy.deepcopy(k);x['kernel_relators'][0]=[1,2,-1,-2];reject('duplicate_pair_omits_required_commutation',x)
 x=copy.deepcopy(k);x['basis_words'][0]=[];reject('rank_deficient_translation_image',x)
 x=copy.deepcopy(k);x['basis_words'][0]=[1];reject('nontranslation_kernel_word',x)
 old=R[2]
 try:
  R[2]=(old[0],(0,0,0))
  try:audit(k)
  except ValueError:controls.append('lost_affine_shift_rejected')
  else:raise ValueError('accepted collapsed finite model')
 finally:R[2]=old
 report.update({'controls_rejected':controls,'kernel_report':k,'verified_retained_inputs':bool(ns.study_root),'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0})
 if ns.render:
  work=ns.out/'render';work.mkdir()
  for i in [1,2]:
   p=subprocess.run([ns.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(work),str(HERE/'cubic_family.tex')],cwd=HERE,capture_output=True,text=True,timeout=60)
   (work/f'pass{i}.log').write_text(p.stdout+p.stderr);ensure(p.returncode==0,'render')
  log=(work/'cubic_family.log').read_text();bad=[x for x in log.splitlines() if 'Overfull' in x or 'LaTeX Warning:' in x];ensure(not bad,'render diagnostics '+str(bad))
  fresh=page_text(work/'cubic_family.pdf');ensure(fresh==page_text(HERE/'cubic_family.pdf'),'exact page text')
  report['render']={'pages':len(fresh),'exact_page_text':True,'diagnostics':bad}
 report['elapsed_seconds']=round(time.monotonic()-start,3);(ns.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','controls':len(controls),'seconds':report['elapsed_seconds']}))
if __name__=='__main__':main()
