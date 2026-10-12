#!/usr/bin/env python3
"""Replay document migration only; retain prior finite and Lean execution evidence."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for z in load(HERE/'manifest.json')['exports']:
   p=HERE/z['path'];need(p.stat().st_size==z['bytes'] and sha(p)==z['sha256'],'export '+z['path'])
 lean=load(HERE/'retained_Lean_compile.json');finite=load(HERE/'retained_tree_check.json')
 need(lean['sha256']==sha(HERE/'BooleanShadow.lean') and lean['exit_code']==0 and lean['stderr']=='','exact inherited Lean evidence')
 need(lean['dependency_manifest_sha256']==sha(HERE/'dependency_manifest.json'),'inherited dependencies')
 need(finite['script_sha256']==sha(HERE/'retained_tree_check.py') and finite['status']=='PASS','exact inherited finite evidence')
 scope=load(HERE/'scope.json');need(scope['source_id']=='L096' and scope['new_original_credit']==scope['new_question_credit']==scope['new_Lean_credit']==0,'bounded claim')
 need(scope['L089_archived'] and not scope['L089_full_text_read'] and not scope['whole_L096_recovered'],'no whole-original credit')
 need(scope['measurement_factor'] is None and not scope['fresh_finite_execution'] and not scope['fresh_Lean_execution'],'no new measurement or execution')
 texts=[p.extract_text() or '' for p in PdfReader(HERE/'tree_shadows.pdf').pages];need(len(texts)==4,'complete four-page document')
 rendered=False
 if a.render:
  shutil.copyfile(HERE/'tree_shadows.tex',a.out/'tree_shadows.tex')
  for i in [1,2]:
   p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','tree_shadows.tex'],cwd=a.out,capture_output=True,text=True,timeout=30)
   (a.out/f'render{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'TeX build')
  log=(a.out/'tree_shadows.log').read_text();need(not any(z in log for z in ['Overfull','Underfull','LaTeX Warning','Missing character']),'clean TeX diagnostics')
  need(texts==[p.extract_text() or '' for p in PdfReader(a.out/'tree_shadows.pdf').pages],'exact rebuilt page texts');rendered=True
 result=dict(status='PASS_DOCUMENT_MIGRATION_AND_PRIOR_RECEIPT_BINDINGS',pages=4,rendered=rendered,inherited_Lean_named_claims=scope['inherited_Lean_scope'],inherited_finite_counts=finite['counts'],finite_rerun=False,Lean_rerun=False,new_mathematical_review=False,new_original_credit=0,new_question_credit=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
