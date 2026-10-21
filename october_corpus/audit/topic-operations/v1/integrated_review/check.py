#!/usr/bin/env python3
"""Reproduce the independently reviewed migration, not a theorem prover."""
from pathlib import Path
import argparse,hashlib,json,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
PAT=re.compile(r'\\begin\{(lemma|theorem|proposition|corollary|proof)\}(.*?)\\end\{\1\}',re.S)
def need(p,m):
 if not p:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def norm(s):
 s=re.sub(r'\\(?:label|ref|eqref)\{(?:[A-Z]+-)?([^}]+)\}',r'LABEL{\1}',s)
 s=re.sub(r'\bH([1-6])\b',r'\1',s)
 return re.sub(r'\s+',' ',s).strip()
def main():
 a=argparse.ArgumentParser();a.add_argument('--packet',required=True);a.add_argument('--out',required=True);args=a.parse_args()
 packet=Path(args.packet).resolve();out=Path(args.out).resolve();need(not out.exists(),'fresh output')
 review=read(ROOT/'review.json');manifest=read(packet/'manifest.json')
 need(sha(packet/'manifest.json')==review['author_manifest_sha256'],'reviewed final edition')
 for row in manifest['exports']:
  p=packet/row['path'];need(p.is_file() and not p.is_symlink() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'whole final export '+row['path'])
 old=read(ROOT/'precursor_bindings.json');env=read(ROOT/'environment_migration.json')
 need(len(old)==17 and len(env['rows'])==84,'complete earlier scientific text set')
 seen=set();exact=0
 for row in old:
  p=ROOT/row['path'];need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'whole precursor '+row['path'])
  units=list(PAT.finditer(p.read_text()))
  needed={(row['path'],i+1) for i in range(len(units))}
  selected=[r for r in env['rows'] if r['source']==row['path']]
  need({(r['source'],r['source_unit']) for r in selected}==needed,'every old theorem/proof has a destination')
  for r in selected:
   key=(r['source'],r['source_unit']);need(key not in seen,'unique old environment');seen.add(key)
   prior=units[r['source_unit']-1];current=list(PAT.finditer((packet/r['new_path']).read_text()))[r['new_unit']-1]
   need(prior[1]==current[1]==r['kind'],'same theorem/proof kind')
   isexact=norm(prior[2])==norm(current[2]);need(isexact==r['exact_mod_notation'],'reviewed textual migration classification')
   exact+=isexact
 need(len(seen)==84 and exact==70,'84 complete routes, 70 unchanged environments')
 migration=read(packet/'source_migration.json');prior=read(packet/'precursor_source_contract.json')
 need(len(migration['records'])==81 and [r['source_record'] for r in migration['records']]==prior['rows'],'all unchanged source dispositions')
 need(migration['questions']==prior['questions'],'question qualifications unchanged')
 for r in migration['records']:
  need(r['current_files'] and all((packet/p).is_file() for p in r['current_files']),'complete source destinations')
 for name in ['common-theory','application']:
  text=(packet/(name+'.tex')).read_text()
  for f in re.findall(r'\\input\{(sections/[^}]+)\}',text):text+='\n'+(packet/f).read_text()
  labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text)
  need(len(labels)==len(set(labels)) and set(refs)<=set(labels),'all actual internal references')
 pages={name:len(PdfReader(packet/name).pages) for name in review['whole_documents']}
 need(pages==review['whole_documents'],'whole final PDFs')
 evidence=read(packet/'evidence_scope.json');need(evidence['new_Lean_declarations']==0,'no added formal credit')
 roles={r['path']:r['role'] for r in evidence['programs']}
 need(roles=={'programs/affine_example.py':'required_finite_premise_s2_s3_s4','programs/presentation_identities.py':'validation_only','programs/literal_twist.py':'validation_only'},'distinct whole program roles')
 for row in evidence['programs']:need(sha(packet/row['path'])==row['old_binding']['sha256'],'whole unchanged program')
 text=''.join(''.join(p.extract_text().splitlines()[:-1]) for p in PdfReader(packet/'programs.pdf').pages)
 text=''.join(text.split())
 for row in evidence['programs']:need(''.join((packet/row['path']).read_text().split()) in text,'complete ordered printed program')
 ext=read(packet/'dependency_inventory.json')['external_inputs']['inputs']
 need(len(ext)==7 and all(r['full_external_proof_cost'] is None for r in ext),'seven unpriced retained classical interfaces')
 result={'status':'PASS','reviewed_manifest':review['author_manifest_sha256'],'source_records':81,'precursor_texts':17,'complete_environment_routes':84,'unchanged_mod_notation':70,'manually_reviewed_changes':14,'whole_pages':pages,'unchanged_whole_programs':3,'new_Lean_declarations':0,'new_question_credit':0,'public_admission_change':0,'compression_factor':None,'limitation':'Binding and migration checks reproduce the recorded human-readable review; they are not a formal proof of all mathematics.'}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
