#!/usr/bin/env python3
"""Verify principal assembly bindings and the two retained A12 witnesses."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(b,s):
 if not b:raise ValueError(s)
def load(s):return json.loads((HERE/s).read_text())
def bind(root,row):
 b=(root/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def scope(s):
 need(s['original']=='L038' and s['edition']=='arXiv:1810.12450v2, 4 January 2019','edition')
 need(s['principal']=='For every integer n>=12 and 3<=r<=floor((n-1)/2), An has a string C-group representation of rank r.','principal')
 need(s['principal_author_proof_complete'] is True and s['all_auxiliary_results_recovered'] is False,'principal versus auxiliary scope')
 need(s['retained_upper_rank_bound']=='not reproved or newly credited' and s['earlier_maximal_seeds']=='retained attributed theorem inputs','prior theorem boundaries')
 need(s['new_original_credit']==s['new_conjecture_credit']==s['new_Lean']==s['new_measurement']==0,'new credit')
 need(s['whole_original_accepted'] is False and s['no_principal_mathematical_case_unresolved'] is True,'admission boundary')
 need(s['branches']==['n=12','n=1 mod4, n>=13','n=2 mod4, n>=14','n=0 mod4, n>=16','n=3 mod4, n>=15'],'branches')
 need(s['finite_witness_scope']=='two existing A12 tuples, not a new census','finite scope')
def run(path,exe,code):
 path.mkdir();shutil.copyfile(HERE/'a12_witnesses.g',path/'a12_witnesses.g');(path/'certificate.g').write_text(code)
 p=subprocess.run([exe,'-q','certificate.g'],cwd=path,text=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60);(path/'stdout.log').write_text(p.stdout);(path/'stderr.log').write_text(p.stderr);return p
def main():
 need(sys.flags.optimize==0,'optimized Python is unsupported')
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--gap',default='gap');ap.add_argument('--render',action='store_true');a=ap.parse_args();a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 m=load('manifest.json')
 for row in m['exports']:bind(HERE,row)
 ext=0
 if a.study_root:
  for row in load('dependencies.json')['bindings']:bind(a.study_root,row);ext+=1
 s=load('scope.json');scope(s);sc=[]
 for k,v in [('principal_author_proof_complete',False),('all_auxiliary_results_recovered',True),('retained_upper_rank_bound','newly proved'),('earlier_maximal_seeds','newly proved'),('new_original_credit',1),('new_conjecture_credit',1),('new_Lean',1),('new_measurement',1),('whole_original_accepted',True),('no_principal_mathematical_case_unresolved',False),('branches',[]),('finite_witness_scope','new complete census')]:
  b=copy.deepcopy(s);b[k]=v
  try:scope(b)
  except ValueError:sc.append(k)
  else:raise ValueError('scope control accepted '+k)
 code=(HERE/'a12_certificate.g').read_text();p=run(a.out/'exact',a.gap,code);need(p.returncode==0 and not p.stderr.strip(),'A12 replay');need(p.stdout.split()==load('expected.json')['stdout_tokens'],'A12 expected output')
 neg=[]
 for name,old,new in [('wrong_order','Size(Group(t))<>Factorial(12)/2','Size(Group(t))<>Factorial(12)'),('wrong_intersection','Intersection(sets[i],sets[j])','Union(sets[i],sets[j])')]:
  need(code.count(old)==1,'mutation target '+name);q=run(a.out/('negative_'+name),a.gap,code.replace(old,new));need('TWO_RETAINED_A12_WITNESSES_PASS'not in q.stdout and 'Error,'in q.stderr,'damaged witness check accepted '+name);neg.append(name)
 origin=False
 if a.study_root:
  path=(a.study_root/'reboot_20261013/L071_A12_full_IP01/records.g').resolve()
  origin_code='Read("a12_witnesses.g");\nRead('+json.dumps(str(path))+');\nfor j in [1,2] do\n r:=j+2;\n if recordedMarks[r][a12RecordPositions[j]]<>a12RecordIndices[j] or recordedInvolutions{a12RecordIndices[j]}<>a12Tuples[j] then Error("retained record differs");fi;\nod;\nPrint("EXACT_RETAINED_RECORDS_PASS\\n");QUIT;\n'
  q=run(a.out/'record_origin',a.gap,origin_code);need(q.returncode==0 and not q.stderr.strip() and 'EXACT_RETAINED_RECORDS_PASS'in q.stdout,'record origin');origin=True
 pages=None
 if a.render:
  from pypdf import PdfReader
  d=a.out/'native';d.mkdir();shutil.copyfile(HERE/'principal.tex',d/'principal.tex');env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
  for i in [1,2]:
   q=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','principal.tex'],cwd=d,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/f'pass{i}.log').write_text(q.stdout);need(q.returncode==0,'TeX build')
  log=(d/'principal.log').read_text()
  for bad in ['Overfull','LaTeX Warning:','undefined references']:need(bad not in log,'native '+bad)
  texts=[p.extract_text()or''for p in PdfReader(d/'principal.pdf').pages];ref=load('native.json');need(len(texts)==ref['pages'],'page count');need([hashlib.sha256(t.encode()).hexdigest()for t in texts]==ref['page_text_sha256'],'native text');pages=len(texts)
 report={'status':'PASS','exports':len(m['exports']),'bindings':ext,'A12_subset_pairs':320,'exact_retained_record_selection':origin,'scope_controls':sc,'damaged_certificate_controls':neg,'native_pages':pages,'uniform_proof':'written assembly of pinned reviewed components; not formalized by this script','whole_original_accepted':False,'distinct_review':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
