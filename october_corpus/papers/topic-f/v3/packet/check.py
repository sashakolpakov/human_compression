#!/usr/bin/env python3
"""Portable author binding/validation/render/partial-Lean replay for expanded Topic F.
All finite programs are diagnostics; the quantified mathematical arguments are written.
No input primary texts, package objects, or source-render images are distributed here.
"""
import argparse,copy,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','odd-kernel-polyhedra','chiral-odd-kernels','program-appendix']
PROGRAMS=['phase236_models.py','phase236_finite_check.g','phase248_presentation_check.g','cyclotomic_carries.g','regular_byproducts.g','small_order_probe.g','modularity_probe.g','central_lift.g','verify_lift_normalforms.py']
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(r,base=ROOT):
 p=Path(r['path']);need(not p.is_absolute() and '..' not in p.parts,'Safe relative path')
 p=base/p;need(p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Changed binding '+str(p))
def validate(s):
 need(s['source_ids']==['L014','L007'],'Exact source pair')
 need(len(s['contracts'])==63 and s['l007_rows']==38,'All25+38 source rows')
 ids=[r['id'] for r in s['contracts']];need(len(set(ids))==63,'Unique rows')
 need(ids[:25]==s['inherited_row_ids'],'Unchanged inherited row identities')
 for n,r in s['proof_spans'].items():
  t=(ROOT/r['path']).read_text();a,b=r['start_codepoint'],r['end_codepoint_exclusive']
  need(0<=a<b<=len(t) and hashlib.sha256(t[a:b].encode()).hexdigest()==r['sha256_utf8'],'Changed proof span '+n)
 for r in s['contracts']:need(r['current_spans'] and all(n in s['proof_spans'] for n in r['current_spans']),'Complete source-to-proof map')
 byid={r['id']:r for r in s['contracts']}
 for n in ['L007.R1.3.family4','L007.S6.Claim4']:need(byid[n]['status'].startswith('corrected'),'Literal correction lost')
 need(byid['L007.S7.prior_lift']['status']=='prior_answer_reused_no_new_credit','Prior lift attribution')
 need(byid['L014.T1.2.defect']['status']=='literal_preprint_marking_corrected','Old marking correction')
 for n in ['excluded.census','excluded.classification']:need(byid[n]['status']=='excluded_not_recovered','Old scope exclusion')
 for r in s['contracts'][:25]:
  if 'F1.Construction' in r['current_spans']:need('UF.SplitConstruction' in r['current_spans'],'Unpaid moved construction')
 need(set(r['path'] for r in s['programs'])=={'programs/'+n for n in PROGRAMS},'Whole9programs')
 for r in s['programs']:binding(r);need(r['role']=='finite_validation' and not r['uniform_proof_premise'],'Program role')
 need(len(s['drivers'])==2,'Two historical drivers')
 for r in s['drivers']:binding(r)
 for r in s['migration']:binding(r['new'])
 binding(s['formal_scope']);f=json.loads((ROOT/'formal/scope.json').read_text())
 need(len(f['modules'])==3 and [len(x['declarations']) for x in f['modules']]==[5,4,3] and f['new_declarations']==3,'Exact distinct12formal boundary')
 need(not f['source_specific_claims'],'No full application formalization')
 for r in f['modules']:binding(dict(r,path='formal/'+r['file']))
 need(not s['finite_programs_required_for_uniform_proofs'] and s['whole_common_charged_once'] and s['no_free_other_application'],'Written common boundary')
 need(s['retained_CP_input']['local_pdf'] is None and s['retained_CP_input']['full_text_cost'] is None,'CP limitation')
 need(all(r['full_proof_cost'] is None for r in s['retained_inputs']),'External costs unknown')
 need(s['new_source_credit']==s['new_question_credit']==0 and s['cost_boundary']['ratio'] is None,'No new admission or ratio')
 need(s['section7_current_literature_priority_not_asserted'],'Prior/status distinction')
 return {'source_rows':63,'retained_L014_rows':25,'new_L007_rows':38,'proof_spans':len(s['proof_spans']),'whole_validation_programs':9,'distinct_Lean_declarations':12,'new_Lean_declarations':3}
def controls(s):
 ans=[]
 def reject(n,fn):
  x=copy.deepcopy(s);fn(x)
  try:validate(x)
  except RuntimeError as e:ans.append({'name':n,'rejected':True,'reason':str(e)})
  else:raise RuntimeError('Accepted bad control '+n)
 reject('omit source row',lambda x:x['contracts'].pop())
 reject('duplicate source row',lambda x:x['contracts'].__setitem__(-1,x['contracts'][-2]))
 reject('alter proof',lambda x:x['proof_spans']['UF.Carry'].__setitem__('sha256_utf8','0'*64))
 reject('erase regular correction',lambda x:next(r for r in x['contracts'] if r['id']=='L007.R1.3.family4').__setitem__('status','recovered'))
 reject('erase presentation repair',lambda x:next(r for r in x['contracts'] if r['id']=='L007.S6.Claim4').__setitem__('status','recovered'))
 reject('claim new lift answer',lambda x:next(r for r in x['contracts'] if r['id']=='L007.S7.prior_lift').__setitem__('status','new_answer'))
 reject('drop common construction',lambda x:next(r for r in x['contracts'] if 'F1.Construction' in r['current_spans'])['current_spans'].remove('UF.SplitConstruction'))
 reject('drop full validation file',lambda x:x['programs'].pop())
 reject('samples prove theorem',lambda x:x.__setitem__('finite_programs_required_for_uniform_proofs',True))
 reject('old common free',lambda x:x.__setitem__('whole_common_charged_once',False))
 reject('invent CP cost',lambda x:x['retained_CP_input'].__setitem__('full_text_cost',0))
 reject('invent external cost',lambda x:x['retained_inputs'][0].__setitem__('full_proof_cost',0))
 reject('invent new question credit',lambda x:x.__setitem__('new_question_credit',1))
 reject('claim priority audit',lambda x:x.__setitem__('section7_current_literature_priority_not_asserted',False))
 return ans

def hypothesis_controls():
 # The identity endomorphism fixes the two transpositions generating S3,
 # but does not invert their 3-cycle product: commutativity cannot be dropped.
 one=(0,1,2);a=(1,0,2);b=(0,2,1)
 mul=lambda u,v:tuple(v[u[i]] for i in range(3))
 c=mul(a,b);need(mul(a,a)==one and mul(b,b)==one and mul(c,c)!=one,'Nonabelian closure countermodel')
 # Additive C3: inversion fixes no nonzero beta, whereas identity fails to invert z.
 need((-1)%3!=1 and (2*1)%3!=0,'Nonzero odd carry')
 # Additive C2: the nonzero carry equals its inverse under identity.
 need((-1)%2==1 and (2*1)%2==0,'Order-two carry countermodel')
 return [{'omitted':'abelian generated subgroup','model':'S3; identity fixes two involutions but not inverse of their product'},
 {'omitted':'fixed beta','model':'C3; inversion sends beta=z=1 to -1 and beta^1=z'},
 {'omitted':'inverted generators','model':'C3; identity fixes beta=z=1 with nontrivial square'},
 {'omitted':'carry square nonidentity','model':'C2; identity both fixes and inverts the nonzero carry'}]

def appendix():
 t=(ROOT/'program-appendix.tex').read_text();names=re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',t)
 need(names==PROGRAMS,'Nine complete printed files in order')
 chunks=[]
 for p in PdfReader(ROOT/'program-appendix.pdf').pages:
  def visitor(t,cm,tm,font,size):
   if font and 'Menlo' in str(font.get('/BaseFont','')):chunks.append(t)
  p.extract_text(visitor_text=visitor)
 norm=lambda t:''.join(x for x in t if not x.isspace())
 expected=norm(''.join((ROOT/'programs'/n).read_text() for n in PROGRAMS))
 need(norm(''.join(chunks))==expected,'Full printed-code inclusion')
 return {'whole_files':9,'nonspace_code_characters':len(expected),'layout_whitespace_ignored_for_inclusion_only':True}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path)
 ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--render',action='store_true')
 ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--xelatex',default=shutil.which('xelatex'))
 ap.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean');ap.add_argument('--packages',default='/Users/sasha/bogachev/formal/.lake/packages')
 a=ap.parse_args();need(not os.path.lexists(a.out),'Fresh output path required');out=a.out.resolve();out.mkdir(parents=True)
 started=time.monotonic();s=json.loads((ROOT/'scope.json').read_text());res=validate(s);res['integrity_controls']=controls(s);res['hypothesis_controls']=hypothesis_controls();res['appendix']=appendix()
 if (ROOT/'manifest.json').exists():
  for r in json.loads((ROOT/'manifest.json').read_text())['exports']:binding(r)
  res['manifest_sha256']=sha(ROOT/'manifest.json')
 if a.study_root:
  for r in s['predecessors']:binding(r,a.study_root)
  for r in s['sources']:binding(r['primary'],a.study_root)
  prior=json.loads((a.study_root/'phase236_source_ledger.json').read_text())['rows']
  need(prior==[r['inherited_record'] for r in s['contracts'][:25]],'Exact inherited25row records')
  res['external_bindings_checked']=len(s['predecessors'])+2
  for r in s['migration']:binding(r['old'],a.study_root)
  migration=json.loads((ROOT/'migration.json').read_text())
  delta=migration['construction_proof_exact_after_three_reference_changes']
  old=(a.study_root/'topic_F_volume/sections/06-construction.tex').read_text()
  new=(ROOT/'sections/10-split-construction.tex').read_text()
  def proof(t):return t[t.index('\\begin{proof}'):t.index('\\end{proof}')+len('\\end{proof}')]
  old,new=proof(old),proof(new)
  for x,y in delta['literal_replacements']:old=old.replace(x,y)
  need(old==new,'Complete old construction migration after three reference edits')
  res['old_construction_proof_exact_after_reference_edits']=True
 def run(n,cmd,cwd=out):
  p=subprocess.run(list(map(str,cmd)),cwd=cwd,text=True,capture_output=True,timeout=1800)
  (out/(n+'.stdout')).write_text(p.stdout);(out/(n+'.stderr')).write_text(p.stderr)
  need(p.returncode==0 and not re.search(r'Error,|Error\(|Syntax error|Error at',p.stdout+p.stderr),'Replay failure '+n)
  return p
 if a.programs:
  need(a.gap,'GAP executable required');stats={}
  p=run('legacy_models',[sys.executable,'-B',ROOT/'programs/phase236_models.py','--out',out/'models.g'])
  stats['old_cyclotomic_models']=len(json.loads(p.stdout))
  g=out/'old_models_run.g';g.write_text('Read('+json.dumps(str(out/'models.g'))+');\nRead('+json.dumps(str(ROOT/'programs/phase236_finite_check.g'))+');\n')
  p=run('legacy_finite',[a.gap,'-q','-T',g]);need('PHASE236_FINITE_PASS' in p.stdout,'Old finite marker');stats['old_abelian_models']=p.stdout.count('ABELIAN p=')
  for n in PROGRAMS[2:]:
   p=run(Path(n).stem,([sys.executable,'-B'] if n.endswith('.py') else [a.gap,'-q','-T'])+[ROOT/'programs'/n])
   stats[n]={'stdout_sha256':sha(out/(Path(n).stem+'.stdout')),'stderr_sha256':sha(out/(Path(n).stem+'.stderr'))}
   if n=='phase248_presentation_check.g':need('PHASE248_PRESENTATION_PASS' in p.stdout,'Literal old presentations')
   if n=='cyclotomic_carries.g':need(p.stdout.count('CARRY rec(')==9,'Nine exact carry models')
   if n=='regular_byproducts.g':need(p.stdout.count('REGULAR_CYC rec(')==6 and p.stdout.count('REGULAR_MIXED rec(')==3,'Fifteen exact regular markings')
   if n=='small_order_probe.g':need('chiral 0' in p.stdout and p.stdout.count('RESULT ')==3 and 'CHIRAL ' not in p.stdout,'Small-order reversal diagnostic')
   if n=='modularity_probe.g':need('NONPERMUTABLE' not in p.stdout and p.stdout.count('checked ')==3,'Bounded modularity diagnostic')
   if n=='central_lift.g':need(p.stdout.count('reversal_homomorphism_exists := false')==3,'Three old lift cases')
   if n=='verify_lift_normalforms.py':need(json.loads(p.stdout)['group_order']==31250,'Explicit old lift normal forms')
  res['validation']=stats
 if a.formal:
  run('formal',[sys.executable,'-B','-O',ROOT/'formal/check.py','--out',out/'formal','--lean',a.lean,'--packages',a.packages])
  f=json.loads((out/'formal/report.json').read_text());need(sum(len(r['axioms']) for r in f['modules'])==12,'Twelve distinct scoped declarations')
  res['formal']={'distinct_declarations':12,'new':3,'source_specific_instances':False,'report':'formal/report.json'}
 if a.render:
  need(a.xelatex,'XeLaTeX required');stage=out/'render';stage.mkdir()
  for p in ROOT.rglob('*.tex'):
   q=stage/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
  shutil.copytree(ROOT/'programs',stage/'programs');reports=[]
  for n in DOCS:
   for i in range(2):run(n+'_'+str(i),[a.xelatex,'-interaction=nonstopmode','-halt-on-error',n+'.tex'],stage)
   t=(stage/(n+'.log')).read_text();need(not any(w in t for w in ['Overfull','Missing character','LaTeX Warning','Package hyperref Warning']),'Final TeX diagnostic '+n)
   x=PdfReader(ROOT/(n+'.pdf'));y=PdfReader(stage/(n+'.pdf'))
   need(len(x.pages)==len(y.pages) and all(p.extract_text()==q.extract_text() for p,q in zip(x.pages,y.pages)),'Exact page text '+n)
   reports.append({'document':n,'pages':len(x.pages),'page_text_identical':True,'critical_diagnostics':[],'underfull_boxes':t.count('Underfull')})
  res['render']=reports
 res.update(status='PASS',seconds=round(time.monotonic()-started,3),independent_review=False,ratio=None,new_source_credit=0,new_question_credit=0)
 (out/'report.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':'PASS','source_rows':63,'controls':18,'seconds':res['seconds'],'out':str(out)}))
if __name__=='__main__':main()
