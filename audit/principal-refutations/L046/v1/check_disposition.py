"""Check the new disposition scope and unchanged public scientific evidence."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
import argparse,copy,hashlib,json,os,subprocess
B='audit/principal-refutations/L046/v1';OLD='corrections/onan-map-count/v1'
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def semantic(p,s,r,source,old):
 need(p['original_id']==s['original_id']==r['original_id']=='L046','Exact source identity')
 need(p['proposed_disposition']==s['proposed_disposition']=='principal_statement_refuted','Exact disposition')
 need(p['ordinary_recovery_increment']==0 and p['proposed_handled_original_increment']==p['proposed_principal_refutation_increment']==1,'Refutation only')
 for x in [p,s]:
  for k in ['ordinary_recovery_credit','principal_refutation_credit','handled_original_credit','new_measurements','new_question_credit','new_Lean']:need(x[k]==0,'No pre-gate credit')
  need(not x['whole_paper_recovered']and not x['all_L046_work_finished']and not x['exact_total_claimed'],'No completed remainder')
 need(p['compression_factor']is None and p['software_inclusive_factor']is None,'No factor')
 need(s['source']==source and s['accepted_bound']==source['proved_lower_total']==798370 and s['printed_total']==source['source_claimed_total']==796772,'Exact source contradiction')
 need(s['principal_target']=='Theorem 1.1(2)'and s['source_counting_convention']==source['source_convention'],'No convention change')
 need(s['exact_corrected_cell']==source['corrected_cell']==dict(p=20,q=31,source=7246,proved=9118),'Exact cell')
 need(r['remaining_exact_table_cells']==old['remaining_exact_table_cells']==116 and not r['exact_full_total_known']and r['full_chirality_and_inversion_unpaid'],'Unpaid counts')
 for key in ['remaining_principal_claims','zero_types_not_excluded_by_this_component','known_zero_type','algorithm_scope']:need(r[key]==old[key],'Complete remaining ledger '+key)
 need(not r['whole_paper_recovered']and not r['all_L046_work_finished']and r['earlier_ledger_preserved_unchanged'],'Remaining work visible')
 need(p['prior_old_no_credit_statements_preserved']and not p['source_scope_recovered_beyond_existing_correction'],'Historical boundary')
 need(p['root_is_new_bound_author']and not p['root_is_distinct_mathematical_reviewer'],'Reviewer roles')
 need(p['new_manuscript_pages']==0 and [x['pages']for x in p['proof_manuscripts']]==[4,4],'Existing complete manuscripts')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--payload',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();R=a.repo.resolve();P=(a.payload.resolve()if a.payload else R)/B
 bindings=load(P/'inherited_bindings.json');seen={}
 for x in bindings['public_files']:
  q=PurePosixPath(x['path']);need(not q.is_absolute()and'..'not in q.parts,'Safe inherited route');p=(R/q).resolve();need(p.is_relative_to(R),'No escape');need(p.stat().st_size==x['bytes']and sha(p)==x['sha256'],'Exact public bytes '+x['path']);need(x['path']not in seen,'Unique binding');seen[x['path']]=x
 tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0'));need(all(x in tracked for x in seen),'Every acquired byte Git tracked')
 def bind(x):need(seen.get(x['path'])==x,'Exact explicit acquisition '+x['path'])
 p=load(P/'disposition_proposal.json');s=load(P/'scope_routes.json');r=load(P/'remaining_claims.json');source=load(R/OLD/'source_statement.json');old=load(R/OLD/'remaining_obligations.json');semantic(p,s,r,source,old)
 for k in ['scientific_author','distinct_mathematical_review','acquired_common_author','acquired_common_review','prior_public_manifest','prior_root_gate','prior_admission','prior_portable_report']:bind(p[k])
 bind(r['earlier_ledger']);bind(s['old_correction_scope'])
 need(p['baseline']==bindings['baseline']=='ade9feeb7f8feaffa8f773932d57a50e60cb64c2','Exact predecessor')
 count=0
 for x in load(R/OLD/'manifest.json')['exports']:
  bind(dict(x,path=OLD+'/'+x['path']));count+=1
 review=load(R/p['distinct_mathematical_review']['path'].rsplit('/',1)[0]/'review.json')
 need(review['status']=='ACCEPTED_L046_MAXIMAL_BOUNDS_AND_PRINCIPAL_NUMERICAL_REFUTATION'and review['source_total']==796772 and review['proved_lower_total']==798370,'Accepted same assertion')
 replay=load(R/p['prior_portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L046_BOUNDED_NUMERICAL_CORRECTION'and replay['logical_bindings']==226 and replay['independent_class_constant_counts']==574 and replay['remaining_exact_type_counts']==116,'Complete acquired replay')
 gate=load(R/p['prior_root_gate']['path']);need(gate['status']=='ROOT_ACCEPTED_L046_BOUNDED_CORRECTION_WITH_COUNTS_UNCHANGED'and gate['root_mathematical_author']and not gate['root_distinct_mathematical_reviewer'],'Historical root gate')
 damages=[]
 edits=[('ordinary_recovery',0,lambda x:x.__setitem__('ordinary_recovery_increment',1)),('exact_total',0,lambda x:x.__setitem__('exact_total_claimed',True)),('finished',0,lambda x:x.__setitem__('all_L046_work_finished',True)),('measurement',0,lambda x:x.__setitem__('new_measurements',1)),('wrong_source',1,lambda x:x.__setitem__('original_id','L029')),('wrong_convention',1,lambda x:x.__setitem__('source_counting_convention','Unordered dual quotient')),('wrong_lower',1,lambda x:x.__setitem__('accepted_bound',796772)),('lost_cells',2,lambda x:x.__setitem__('remaining_exact_table_cells',0)),('lost_chirality',2,lambda x:x.__setitem__('full_chirality_and_inversion_unpaid',False)),('lost_claim',2,lambda x:x['remaining_principal_claims'].pop()),('rewritten_history',0,lambda x:x.__setitem__('prior_old_no_credit_statements_preserved',False)),('new_math_role',0,lambda x:x.__setitem__('root_is_distinct_mathematical_reviewer',True))]
 for name,i,edit in edits:
  values=copy.deepcopy([p,s,r]);edit(values[i])
  try:semantic(*values,source,old)
  except(ValueError,KeyError):damages.append(name)
  else:raise ValueError('Damaged disposition accepted '+name)
 O=a.out.resolve();need(not O.exists(),'Fresh output');O.mkdir(parents=True);guards=[]
 for mode in ['argument','environment']:
  env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);target=O/mode
  if mode=='environment':env['PYTHONOPTIMIZE']='1'
  z=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve()),'--out',str(target)],env=env,capture_output=True,timeout=15)
  need(z.returncode!=0 and b'Ordinary Python required'in z.stderr and not target.exists(),'Pre-output guard');guards.append(mode)
 report=dict(status='PASS_L046_DISPOSITION_LAYER_WITH_UNCHANGED_SCIENCE',inherited_public_files=len(seen),prior_manifest_exports=count,all_reused_files_git_tracked=True,source_total=796772,proved_lower_total=798370,remaining_exact_cells=116,exact_total_unpaid=True,full_chirality_inversion_unpaid=True,scope_damages=damages,optimization_guards=guards,scientific_replay_repeated=False,ordinary_recovery_credit=0,principal_refutation_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,public_writes=False)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
