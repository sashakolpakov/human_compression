#!/usr/bin/env python3
"""Bindings, explicit bounded-scope controls and optional exact render replay."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json,shutil,subprocess
from pypdf import PdfReader
H=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise ValueError(m)
def bind(p,r):
 b=p.read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'binding '+str(p))
def valid(r):
 need(r['status']=='ACCEPTED_BOUNDED_EQUALITY_CONNECTEDNESS'and r['statements']==6 and r['pages']==2,'full bounded written proof')
 need(r['hypotheses']==['finite faithful transitive involutory string action','exactly two selected eligible edges of each colour','at least two eligible full-graph edges of each colour','2r=n','global minimum square count among square-only selections'],'retained exact hypotheses')
 need(not r['IP_required']and not r['evenness_required'],'scope does not add hidden IP or evenness')
 need(not r['whole_original_accepted']and not r['pair_block_rigidity_accepted']and r['ratio']is None,'no wider acceptance or scalar')
 need(r['new_original_credit']==r['new_question_credit']==r['new_formal_declarations']==0,'no unsupported credits')
 need(not r['reviewer_was_author'],'distinct role')
def run(study,out,render):
 if(H/'manifest.json').exists():
  for r in read(H/'manifest.json')['exports']:bind(H/r['path'],r)
 bindings=read(H/'bindings.json')
 for r in bindings.values():bind(study/r['path'],r)
 author=study/bindings['author']['path'];am=read(author)
 for r in am['exports']:bind(author.parent/r['path'],r)
 notes=read(H/'claim_review.json');need([r['lemma']for r in notes]==list(range(1,7)),'six complete claim notes')
 r=read(H/'review.json');valid(r);controls=[]
 changes=[('omit equality hypothesis',lambda q:q['hypotheses'].remove('2r=n')),('local instead of global minimum',lambda q:q['hypotheses'].__setitem__(4,'some chosen selection')),('whole-source credit',lambda q:q.update(whole_original_accepted=True)),('pair rigidity overclaim',lambda q:q.update(pair_block_rigidity_accepted=True)),('new formal credit',lambda q:q.update(new_formal_declarations=1)),('lose distinct role',lambda q:q.update(reviewer_was_author=True))]
 for name,fn in changes:
  q=deepcopy(r);fn(q)
  try:valid(q)
  except ValueError:controls.append(name)
  else:raise ValueError('control survived '+name)
 out.mkdir(parents=True,exist_ok=False);render_result=None
 if render:
  cp=out/'author_export_copy';cp.mkdir()
  for x in am['exports']:shutil.copyfile(author.parent/x['path'],cp/x['path'])
  shutil.copyfile(author,cp/'manifest.json')
  for i in range(2):
   p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','equality_components.tex'],cwd=cp,capture_output=True,text=True)
   (cp/f'replay{i+1}.txt').write_text(p.stdout+p.stderr);need(p.returncode==0,'render')
  a=[p.extract_text()or''for p in PdfReader(author.parent/'equality_components.pdf').pages]
  b=[p.extract_text()or''for p in PdfReader(cp/'equality_components.pdf').pages]
  need(a==b and len(a)==2,'all exact page texts')
  log=(cp/'equality_components.log').read_text();need(not any(x in log for x in ['LaTeX Warning:','Overfull','undefined references']),'clean final diagnostics')
  render_result=dict(exact_page_texts=2,diagnostics=[],page_text_sha256=[hashlib.sha256(x.encode()).hexdigest()for x in b])
 report=dict(status='PASS_BOUNDED_EQUALITY_REVIEW',author_exports=len(am['exports']),statements=6,scope_controls=controls,render=render_result,mathematical_basis='complete independent written proof read, not computation or formal kernel',source_assets_exported=False)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args();print(json.dumps(run(a.study_root,a.out,a.render),indent=2))
