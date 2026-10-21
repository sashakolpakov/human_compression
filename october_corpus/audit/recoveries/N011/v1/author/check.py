#!/usr/bin/env python3
"""Portable binding/native replay; optional symbolic checks, no finite proof premise."""
import argparse,copy,hashlib,json,shutil,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name):return json.loads((HERE/name).read_text())
def need(ok,label):
 if not ok:raise ValueError(label)
def bind(root,row):
 p=root/row['path'];need(p.is_file(),f'missing {p}');need(p.stat().st_size==row['bytes'],f'size {p}');need(digest(p)==row['sha256'],f'hash {p}')
def scope_check(s,m,n,r):
 need(s['source_id']=='N011' and s['full_original_pages']==13,'source scope')
 need(s['authors']==['Irina A. Markovskaya','Yakov N. Nuzhin'],'author attribution')
 need(s['new_original_credit']==s['new_conjecture_credit']==s['new_lean']==s['new_measurement']==0,'unauthorized credit')
 need(s['required_new_finite_programs']==[] and s['optional_validation']==['symbolic_check.py'],'software role')
 need(m['disposition_count']==len(m['rows'])==57,'full source rows')
 need(len({x['id']for x in m['rows']})==57,'unique rows')
 need(m['named_results']=={'theorems':2,'lemmas':11,'tables':2,'table_rows':12},'named results')
 labels={x['source_label']for x in m['rows']}
 need({f'Table{t} row{i}'for t in [1,2]for i in range(1,7)}<=labels,'whole tables')
 need({f'Lemma{i}'for i in range(1,10)}|{'Lemma10a','Lemma10b','Lemma10c','Lemma11'}<=labels,'whole lemmas')
 need(m['remaining_principal_obligations']==[],'principal obligation changed')
 need(m['retained_inputs_are_not_reproved'] and not m['literal_theorem_set_equivalence'],'source qualifications')
 need(len(r['inputs'])==6 and all(x['external_complete_proof_cost']=='UNKNOWN'for x in r['inputs']),'retained cost boundary')
 need([x['pages']for x in n['documents']]==[2,7]and n['total_pages']==9,'whole native pages')
 need(all(not x['diagnostics']for x in n['documents']),'native diagnostics')
 return True

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--validate',action='store_true');p.add_argument('--pdflatex',default=shutil.which('pdflatex')or'/opt/homebrew/bin/pdflatex');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 manifest=load('manifest.json')
 for row in manifest['exports']:bind(HERE,row)
 s,m,n,r=[load(z)for z in ['scope.json','source_map.json','native.json','retained_inputs.json']];scope_check(s,m,n,r)
 for z in n['documents']:
  rr=PdfReader(HERE/z['pdf']);need(len(rr.pages)==z['pages'],'bound page count');need([hashlib.sha256(x.extract_text().encode()).hexdigest()for x in rr.pages]==z['page_text_sha256'],'bound page text')
 inv=load('program_inventory.json');need([(x['path'],x['role'])for x in inv['files']]==[('symbolic_check.py','OPTIONAL_VALIDATION'),('check.py','OPERATIONAL_REPLAY')],'whole program roles')
 ext=0
 if a.study_root:
  for row in [m['source'],m['text']]+load('prior_work.json')['items']:bind(a.study_root,row);ext+=1
  import re
  pages={int(z.group(1)):z.group(2)for z in re.finditer(r'PAGE (\d+)\n(.*?)(?=\nPAGE |\Z)',(a.study_root/m['text']['path']).read_text(),re.S)}
  for row in m['rows']:need([hashlib.sha256(pages[z].encode()).hexdigest()for z in row['printed_pages']]==row['source_page_text_sha256'],'literal source span')
 controls=[]
 mutations=[('missing source row',lambda x:x[1]['rows'].pop()),('missing table',lambda x:x[1]['rows'][6].update(source_label='removed')),('missing lemma',lambda x:x[1]['rows'][21].update(source_label='removed')),('source count',lambda x:x[0].update(full_original_pages=12)),('missing coauthor',lambda x:x[0].update(authors=['Irina A. Markovskaya'])),('new credit',lambda x:x[0].update(new_original_credit=1)),('new Lean',lambda x:x[0].update(new_lean=1)),('optional becomes premise',lambda x:x[0].update(required_new_finite_programs=['symbolic_check.py'])),('retained proof called free',lambda x:x[3]['inputs'][0].update(external_complete_proof_cost=0)),('literal equivalence',lambda x:x[1].update(literal_theorem_set_equivalence=True)),('shortened common',lambda x:x[2]['documents'][0].update(pages=1)),('shortened application',lambda x:x[2]['documents'][1].update(pages=6))]
 for label,fn in mutations:
  x=copy.deepcopy([s,m,n,r]);fn(x)
  try:scope_check(*x)
  except ValueError:controls.append(label)
  else:raise ValueError('control accepted: '+label)
 symbolic=None
 if a.validate:
  run=subprocess.run([sys.executable,'-B','-O',str(HERE/'symbolic_check.py'),'--out',str(a.out/'symbolic.json')],capture_output=True,text=True,timeout=90)
  (a.out/'symbolic.stdout').write_text(run.stdout+run.stderr);need(run.returncode==0,'symbolic replay')
  symbolic=json.loads((a.out/'symbolic.json').read_text());old=load('symbolic_report.json');need(symbolic['checks']==old['checks']and symbolic['count']==105,'exact optional checks')
 renders=[]
 if a.render:
  for z in n['documents']:
   out=a.out/Path(z['tex']).stem;out.mkdir()
   for i in range(2):
    run=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error',f'-output-directory={out.resolve()}',str(HERE/z['tex'])],cwd=HERE,capture_output=True,text=True,timeout=90)
    (out/f'pass{i+1}.stdout').write_text(run.stdout+run.stderr);need(run.returncode==0,'native build')
   log=(out/(Path(z['tex']).stem+'.log')).read_text();need(not any(v in log for v in ['Overfull','LaTeX Warning','Package hyperref Warning','Undefined control']),'native clean')
   rr=PdfReader(out/z['pdf']);need(len(rr.pages)==z['pages'],'fresh pages');need([hashlib.sha256(x.extract_text().encode()).hexdigest()for x in rr.pages]==z['page_text_sha256'],'fresh exact text');renders.append({'pdf':z['pdf'],'pages':len(rr.pages),'exact_text':True})
 report={'status':'PASS','frozen_exports':len(manifest['exports']),'source_dispositions':57,'source_named_results':13,'source_table_rows':12,'native_pages':9,'external_bindings_checked':ext,'controls':controls,'optional_symbolic_checks':symbolic['count']if symbolic else None,'renders':renders,'required_finite_premises':0,'no_formal_or_measurement_claim':True}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
