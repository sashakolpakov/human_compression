"""Binding/render/scope replay for a human mathematical review, not a proof kernel."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess
import pypdf
from coordinate_checks import run,valid,cube,square
H=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((H/n).read_text())
def need(v,m):
 if not v:raise ValueError(m)
def bound(p,row):
 b=p.read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'bound file '+str(p))
def scope(r,c):
 need(r['status']=='ACCEPTED_BOUNDED_WRITTEN_MATHEMATICS'and r['reviewer']=='enumeration_volume'and not r['reviewer_was_author'],'distinct bounded role')
 need(r['authors']==['enumeration_review','root'],'both author roles')
 need(r['author_manifest_sha256']=='af4aa8b648ee8f93a4250cc601d94268fd24f2a3de764287fb1e180a12432b86','exact author freeze')
 need(r['statements']==10 and r['pages']==5 and c['all_statements_and_proofs_read'],'whole bounded manuscript')
 need(not r['whole_original_accepted']and not c['whole_original_accepted']and r['new_original_credit']==r['new_question_credit']==r['new_formal_declarations']==0 and not r['historical_priority_claim']and r['ratio']is None,'no widened claim')
 need(not c['uniform_proof_computational_premise'],'finite diagnostics not uniform premise')
 need(len(r['remaining_scope'])==4 and len(r['scope_clarifications'])==2 and all(x['author_confirmed']for x in r['scope_clarifications']),'all explicit limits and clarifications')
 need([x['number']for x in c['claims']]==[str(i)for i in range(1,11)]and all(x['status']=='ACCEPTED_AS_STATED'for x in c['claims']),'all ten proof assessments')
def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--pdflatex',default='pdflatex');v=a.parse_args();need(not v.out.exists(),'fresh output');v.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for x in load('manifest.json')['exports']:bound(H/x['path'],x)
 b=load('bindings.json');bound(v.study_root/b['author_manifest']['path'],b['author_manifest']);bound(v.study_root/b['source']['path'],b['source']);A=(v.study_root/b['author_manifest']['path']).parent
 m=json.loads((A/'manifest.json').read_text());need(m['exports']==b['author_exports'],'all author exports')
 for x in m['exports']:bound(A/x['path'],x)
 need(len(pypdf.PdfReader(v.study_root/b['source']['path']).pages)==46,'exact source extent')
 r=load('review.json');c=load('claim_review.json');scope(r,c);need(run()==load('coordinate_report.json'),'independent coordinate diagnostics')
 controls=[]
 def reject(name,f):
  try:f()
  except(ValueError,KeyError,AssertionError):controls.append(name)
  else:raise ValueError('control survived: '+name)
 def mutation(name,f):
  x=copy.deepcopy(r);y=copy.deepcopy(c);f(x,y);reject(name,lambda:scope(x,y))
 mutation('whole-original admission',lambda x,y:x.update(whole_original_accepted=True))
 mutation('new question claim',lambda x,y:x.update(new_question_credit=1))
 mutation('new formal declaration',lambda x,y:x.update(new_formal_declarations=1))
 mutation('historical priority',lambda x,y:x.update(historical_priority_claim=True))
 mutation('undisclosed root contribution',lambda x,y:x.update(authors=['enumeration_review']))
 mutation('reviewer becomes author',lambda x,y:x.update(reviewer_was_author=True))
 mutation('missing source qualification',lambda x,y:x['scope_clarifications'].pop())
 mutation('discard remaining obligations',lambda x,y:x.update(remaining_scope=[]))
 mutation('finite example becomes uniform premise',lambda x,y:y.update(uniform_proof_computational_premise=True))
 mutation('missing proof assessment',lambda x,y:y['claims'].pop())
 Q=square(0,0,1);Q.pop();reject('missing selected cut edge',lambda:valid(cube(2),Q))
 render=None
 if v.render:
  out=v.out/'render';out.mkdir();shutil.copyfile(A/'paired_cuts.tex',out/'paired_cuts.tex')
  for i in range(2):
   z=subprocess.run([v.pdflatex,'-interaction=nonstopmode','-halt-on-error','paired_cuts.tex'],cwd=out,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);need(z.returncode==0,'fresh TeX render')
  log=(out/'paired_cuts.log').read_text();diag=[l for l in log.splitlines()if any(w in l for w in ['Overfull','LaTeX Warning','Undefined control','Missing character'])];need(not diag,'clean render')
  old=pypdf.PdfReader(A/'paired_cuts.pdf');new=pypdf.PdfReader(out/'paired_cuts.pdf');need(len(old.pages)==len(new.pages)==5,'five whole pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'five exact page texts');render=dict(pages=5,diagnostics=diag,exact_page_texts=True)
 report=dict(status='PASS_DISTINCT_BOUNDED_REVIEW_REPLAY',author_exports=len(m['exports']),written_statements_reviewed=10,scope_controls=controls,independent_small_examples=5,small_examples_are_proof_premises=False,source_contexts_viewed=[12,13,14,15,22,23,29,30],author_pages_viewed=5,render=render,whole_L044_admitted=False,new_question_credit=0,new_formal_credit=0)
 (v.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
