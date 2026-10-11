#!/usr/bin/env python3
"""Bounded review replay; no author module is imported. Optional diagnostics are not uniform proofs."""
import argparse,copy,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PIN='e25e0ce52aab130095972d5c038245574ec40182723941880a57f5fbce8387fc'
LIFT='fec9f1455a44766df87accf0396e6766f3ce8cd4dc1628e0d434773baba93b2e'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def bound(base,r):
 q=Path(r['path']);need(not q.is_absolute()and'..'not in q.parts,'relative binding');p=base/q
 need(p.is_file()and p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'binding '+str(p));return p
def semantics(s,f):
 need(s['source_ids']==['L014','L007']and len(s['contracts'])==63,'source pair and63 rows')
 rows={r['id']:r for r in s['contracts']};need(len(rows)==63,'unique source rows')
 need(len(s['inherited_row_ids'])==25 and list(rows)[:25]==s['inherited_row_ids'],'all25 inherited rows')
 need(rows['L007.R1.3.family4']['status']=='corrected_literal_assertion','fourth family correction')
 need(rows['L007.S6.Claim4']['status']=='corrected_proof_route','invalid source quotient corrected')
 need(rows['L007.S7.prior_lift']['status']=='prior_answer_reused_no_new_credit','prior lift role')
 for k in ['L007.S3.presentation','L007.S3.maximal_class','L007.L3.1','L007.L3.2']:
  need('F2.Odd'in rows[k]['current_spans'],'full all-parity source p-group interface')
 for k in ['L007.T1.4.odd','L007.T1.4.even']:
  need('UF.Carry'in rows[k]['current_spans'],'common carry theorem used')
 for r in s['contracts']:
  need(r['current_spans']and all(x in s['proof_spans']for x in r['current_spans']),'proof owner exists')
  if 'F1.Construction'in r['current_spans']:need('UF.SplitConstruction'in r['current_spans'],'full moved common proof paid')
 need(len(s['programs'])==9 and len({r['path']for r in s['programs']})==9,'nine complete programs')
 need(all(r['role']=='finite_validation'and not r['uniform_proof_premise']for r in s['programs'])and not s['finite_programs_required_for_uniform_proofs'],'samples are validation')
 need(s['whole_common_charged_once']and s['no_free_other_application'],'complete common boundary')
 need(s['retained_CP_input']['full_text_cost']is None and all(x['full_proof_cost']is None for x in s['retained_inputs']),'unknown external proof costs')
 need([len(x['declarations'])for x in f['modules']]==[5,4,3]and f['new_declarations']==3 and not f['source_specific_claims'],'actual12/3partial formal scope')
 need(s['new_source_credit']==s['new_question_credit']==0 and s['cost_boundary']['ratio']is None,'no admission or ratio')
def controls(s,f):
 rows=[]
 def reject(name,change):
  x,y=copy.deepcopy(s),copy.deepcopy(f);change(x,y)
  try:semantics(x,y)
  except(ValueError,KeyError):rows.append(name)
  else:raise ValueError('unrejected '+name)
 def row(x,k):return next(r for r in x['contracts']if r['id']==k)
 reject('missing source family',lambda x,y:x['contracts'].pop())
 reject('fourth regular family restored for every prime',lambda x,y:row(x,'L007.R1.3.family4').__setitem__('status','recovered'))
 reject('invalid even quotient restored',lambda x,y:row(x,'L007.S6.Claim4').__setitem__('status','recovered'))
 reject('old lift credited anew',lambda x,y:row(x,'L007.S7.prior_lift').__setitem__('status','new_answer'))
 reject('all-parameter p-group interface omitted',lambda x,y:row(x,'L007.L3.2')['current_spans'].remove('F2.Odd'))
 reject('common carry premise omitted',lambda x,y:row(x,'L007.T1.4.even')['current_spans'].remove('UF.Carry'))
 reject('moved split proof unpaid',lambda x,y:row(x,'L014.T1.3')['current_spans'].remove('UF.SplitConstruction'))
 reject('finite scan substituted for proof',lambda x,y:x.__setitem__('finite_programs_required_for_uniform_proofs',True))
 reject('complete validation file pruned',lambda x,y:x['programs'].pop())
 reject('source-specific formal claim',lambda x,y:y.__setitem__('source_specific_claims',True))
 reject('reused declarations counted as new',lambda x,y:y.__setitem__('new_declarations',12))
 reject('unavailable CP proof priced zero',lambda x,y:x['retained_CP_input'].__setitem__('full_text_cost',0))
 return rows
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--author-root',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--models',action='store_true');a=ap.parse_args()
 need(not os.path.lexists(a.out),'fresh output');a.out.mkdir(parents=True)
 if(ROOT/'manifest.json').exists():
  for r in load(ROOT/'manifest.json')['exports']:bound(ROOT,r)
 b=load(ROOT/'bindings.json');need(sha(a.author_root/'manifest.json')==PIN,'exact frozen author')
 m=load(a.author_root/'manifest.json')
 for r in m['exports']:bound(a.author_root,r)
 for r in b['author_records']:bound(a.author_root,r)
 s=load(a.author_root/'scope.json');f=load(a.author_root/'formal/scope.json');semantics(s,f)
 need(s['contracts']==load(ROOT/'source_rows.json')['exact_author_rows'],'exact reviewed clause records')
 for k,r in s['proof_spans'].items():
  t=(a.author_root/r['path']).read_text();x=t[r['start_codepoint']:r['end_codepoint_exclusive']]
  need(hashlib.sha256(x.encode()).hexdigest()==r['sha256_utf8'],'proof span '+k)
 if a.study_root:
  for r in b['study_records']:bound(a.study_root,r)
  root=a.study_root/'topic_F_L007_lift_root_review';need(sha(root/'manifest.json')==LIFT,'distinct lift adjudication')
  for r in load(root/'manifest.json')['exports']:bound(root,r)
  for r in load(a.author_root/'migration.json')['records']:
   old=bound(a.study_root,r['old']);new=bound(a.author_root,r['new'])
   if r['kind']=='byte_identical':need(old.read_bytes()==new.read_bytes(),'byte-identical migration')
  old=(a.study_root/'topic_F_volume/sections/06-construction.tex').read_text();new=(a.author_root/'sections/10-split-construction.tex').read_text()
  def proof(t):return t[t.index('\\begin{proof}'):t.index('\\end{proof}')+len('\\end{proof}')]
  old,new=proof(old),proof(new)
  for x,y in load(a.author_root/'migration.json')['construction_proof_exact_after_three_reference_changes']['literal_replacements']:old=old.replace(x,y)
  need(old==new,'complete old construction moved')
  prior=load(a.study_root/'phase236_source_ledger.json')['rows'];need(prior==[r['inherited_record']for r in s['contracts'][:25]],'literal old25rows')
 replay=load(ROOT/'fresh_replay/report.json');need(replay['status']=='PASS'and replay['manifest_sha256']==PIN and replay['formal']['distinct_declarations']==12 and len(replay['render'])==4,'fresh exact author replay')
 models=load(ROOT/'models.json');need(models['status']=='PASS'and len(models['carry_models'])==9 and len(models['p_only_models'])==15 and len(models['regular_models'])==5 and len(models['class_three'])==3 and len(models['hypothesis_controls'])==4,'independent actual model record')
 if a.models:
  p=subprocess.run([sys.executable,'-B','-O',str(ROOT/'local_models.py'),'--out',str(a.out/'models.json')],capture_output=True,text=True,timeout=300)
  need(p.returncode==0,'independent models replay');need(load(a.out/'models.json')==models,'deterministic model agreement')
 answer=dict(status='PASS',author_manifest=PIN,exports=len(m['exports']),source_rows=63,source_L007_rows=38,inherited_L014_rows=25,proof_spans=len(s['proof_spans']),whole_validation_programs=9,scoped_Lean_declarations=12,new_Lean_declarations=3,semantic_controls=controls(s,f),hypothesis_countermodels=4,independent_models_rerun=a.models,study_bindings_checked=bool(a.study_root),root_lift_review=LIFT,uniform_proof_is_written=True,new_source_credit=0,new_question_credit=0,ratio=None)
 (a.out/'report.json').write_text(json.dumps(answer,indent=2)+'\n');print(json.dumps(answer))
if __name__=='__main__':main()
