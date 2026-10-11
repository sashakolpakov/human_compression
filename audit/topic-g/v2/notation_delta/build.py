#!/usr/bin/env python3
"""Add only missing multiplicative-group notation; preserve the author freeze."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
from pypdf import PdfReader
OLD=r'\(\mathbb F_{16}\)\emph{/F4}'
NEW=r'\(\mathbb F_{16}^{*}/\mathbb F_4^{*}\)'
PIN='9d1c68991e23e4b4618472c0c85b500ab208c9c579634f5b635748d8fe843992'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(b,s):
 if not b:raise ValueError(s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 need(sha(a.author/'manifest.json')==PIN,'frozen author pin')
 for row in json.loads((a.author/'manifest.json').read_text())['exports']:
  p=a.author/row['path'];need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'author file changed '+row['path'])
 stage=a.out/'stage';stage.mkdir()
 for p in a.author.rglob('*.tex'):
  q=stage/p.relative_to(a.author);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 path='sections/linear-bases.tex';old=(a.author/path).read_text();need(old.count(OLD)==1,'literal old notation not unique');new=old.replace(OLD,NEW)
 (stage/path).write_text(new)
 for i in range(2):
  r=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','steiner-geometries.tex'],cwd=stage,capture_output=True,text=True,timeout=180)
  (a.out/('render'+str(i)+'.log')).write_text(r.stdout+r.stderr);need(r.returncode==0,'render failed')
 log=(stage/'steiner-geometries.log').read_text();need(not re.search(r'Missing character:|Overfull \\hbox|LaTeX Warning:|Package .* Warning:',log),'render diagnostic')
 oldtext=[p.extract_text() or '' for p in PdfReader(a.author/'steiner-geometries.pdf').pages];newtext=[p.extract_text() or '' for p in PdfReader(stage/'steiner-geometries.pdf').pages]
 need(len(oldtext)==len(newtext)==22,'changed page count')
 need(not any(any(ord(c)<32 and c not in '\t\n\r' for c in t) for t in newtext),'control character')
 scope=json.loads((a.author/'scope.json').read_text());span=scope['proof_spans']['LinearBases'];need(span['path']==path and span['start_anchor'] is None and span['end_anchor'] is None,'whole section scope')
 prior_span=dict(span);span['bytes']=len(new.encode());span['sha256']=hashlib.sha256(new.encode()).hexdigest()
 need(len(old.splitlines())==len(new.splitlines()),'line count changed')
 (a.out/'sections').mkdir();shutil.copyfile(stage/path,a.out/path);shutil.copyfile(stage/'steiner-geometries.pdf',a.out/'steiner-geometries.pdf');(a.out/'scope.json').write_text(json.dumps(scope,indent=2,ensure_ascii=False)+'\n')
 delta={'status':'AUTHOR_NOTATION_ONLY_DELTA_AWAITING_INDEPENDENT_ACCEPTANCE','author_manifest_sha256':PIN,'old_literal':OLD,'new_literal':NEW,'requested_by':'enumeration_review full Steiner written review','reason':'The five directions are the quotient of multiplicative groups, not an additive field quotient. The cyclic order-five argument was already the proof intended by the frozen text.','replacement_files':[path,'steiner-geometries.pdf','scope.json'],'old_section_sha256':sha(a.author/path),'new_section_sha256':sha(a.out/path),'old_pdf_sha256':sha(a.author/'steiner-geometries.pdf'),'new_pdf_sha256':sha(a.out/'steiner-geometries.pdf'),'old_scope_sha256':sha(a.author/'scope.json'),'new_scope_sha256':sha(a.out/'scope.json'),'prior_span':prior_span,'current_span':span,'pages':22,'changed_extracted_pages':[i+1 for i,(x,y) in enumerate(zip(oldtext,newtext)) if x!=y],'all_other_tex_inputs_identical':True,'mathematical_statements_proofs_and_scope_otherwise_unchanged':True,'new_source_question_formal_or_ratio_credit':0,'diagnostics':[],'visual_inspection':'Separate record; not inferred from compilation.'}
 (a.out/'delta.json').write_text(json.dumps(delta,indent=2)+'\n');print(json.dumps(delta))
if __name__=='__main__':main()
