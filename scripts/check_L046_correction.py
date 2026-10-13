"""Register a bounded correction without changing any original disposition."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not accepted')
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json
BASE='corrections/onan-map-count/v1';AUD='audit/bounded-corrections/L046/v1'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(root,path):return json.loads((root/path).read_text())
def bind(root,row):
 p=(root/row['path']).resolve();need(p.is_relative_to(root),'binding outside repository')
 raw=p.read_bytes();need(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'binding changed '+row['path'])
def verify(root,require_gate=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
 for row in history.values():bind(root,row)
 old=load(root,history['audit/corpus/latest.json']['path']);new=load(root,'audit/corpus/latest.json')
 need(set(new)==set(old)|{'bounded_result_corrections'},'unexpected corpus fields')
 for k in set(old)-{'active_catalogue','snapshot'}:need(new[k]==old[k],'original disposition changed '+k)
 need('L046'in new['accessible_pending_original_ids']and 'L046'not in new['handled_mathematical_original_ids'],'L046 must remain pending')
 for key in ['active_catalogue','snapshot','bounded_result_corrections']:bind(root,new[key])
 need(load(root,new['snapshot']['path'])=={k:v for k,v in new.items()if k!='snapshot'},'exact current snapshot')
 a=load(root,BASE+'/admission.json');proposal=load(root,BASE+'/admission_proposal.json');source=load(root,BASE+'/source_statement.json');remaining=load(root,BASE+'/remaining_obligations.json')
 spec=importlib.util.spec_from_file_location('L046_portable',root/BASE/'check.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 module.semantic(source,proposal,remaining)
 need(a['status']=='ROOT_ACCEPTED_BOUNDED_CORRECTION_PUBLICATION'and not a['publication_gate_pending']and a['original_disposition_unchanged'],'bounded admission')
 for key in ['ordinary_recovery_credit','terminal_principal_disposition_credit','handled_original_credit','new_measurement_credit','new_question_credit','new_Lean_credit']:need(a[key]==0,'unearned credit '+key)
 need(not a['whole_paper_recovered']and not a['all_L046_work_finished']and not a['root_is_distinct_mathematical_reviewer'],'false full completion or role')
 need(a['compression_factor']is a['software_inclusive_factor']is None,'invented factor')
 bind(root,a['public_manifest']);bind(root,a['remaining_obligations_binding'])
 for row in load(root,BASE+'/manifest.json')['exports']:bind(root,dict(row,path=BASE+'/'+row['path']))
 oldcat=load(root,old['active_catalogue']['path']);cat=load(root,new['active_catalogue']['path'])
 need(len(cat['entries'])==len(oldcat['entries'])==106,'fixed catalogue')
 need(cat['previous_catalogue']==old['active_catalogue']and cat['new_proof_credit']==0,'catalogue history/credit')
 for key in set(oldcat)-{'entries','previous_catalogue','new_proof_credit','review_revision'}:need(cat[key]==oldcat[key],'other catalogue field changed '+key)
 plan=load(root,BASE+'/catalogue_patch_plan.json')['proposed_original_row_change']
 for before,after in zip(oldcat['entries'],cat['entries']):
  if before['original_id']!='L046':need(before==after,'another original changed')
  else:
   need(set(after)==set(before)|{'bounded_correction_evidence'},'L046 row schema')
   for key in set(before)-{'edition','next_obligation'}:need(after[key]==before[key],'L046 historical record changed')
   for key in ['edition','next_obligation','bounded_correction_evidence']:need(after[key]==plan[key],'L046 evidence change differs')
 p=load(root,'papers/latest_catalogue.json');oldp=load(root,history['papers/latest_catalogue.json']['path'])
 need(set(p)==set(oldp)|{'bounded_correction_catalogue'},'paper routing schema')
 for key in set(oldp)-{'active_source_catalogue'}:need(p[key]==oldp[key],'old paper catalogue changed')
 need(p['active_source_catalogue']==new['active_catalogue']and p['bounded_correction_catalogue']==new['bounded_result_corrections'],'paper/corpus routing')
 papers=load(root,p['bounded_correction_catalogue']['path']);need(len(papers['entries'])==1 and papers['entries'][0]['original_id']=='L046','bounded correction index')
 entry=papers['entries'][0];bind(root,entry['admission'])
 need(papers['status']=='CURRENT_BOUNDED_CORRECTIONS_NO_ORIGINAL_CREDIT','bounded correction index status')
 need(entry['ordinary_recovery_credit']==entry['handled_original_credit']==0,'entry original credit')
 need(entry['original_id']==source['original_id']=='L046'and a['source_ids']==['L046'],'source identity')
 need(entry['admission']['path']==BASE+'/admission.json','exact admission route')
 need(entry['manuscripts']==[
  dict(tex=BASE+'/proof/maximal_bounds.tex',pdf=BASE+'/proof/maximal_bounds.pdf',pages=4,role='new bounded application'),
  dict(tex=BASE+'/common/generating_pairs.tex',pdf=BASE+'/common/generating_pairs.pdf',pages=4,role='retained common theory')],'exact manuscript routes')
 need([m['pages']for m in entry['manuscripts']]==[4,4]and entry['compression_factor']is None and not entry['whole_paper_recovered'],'complete bounded documents')
 for key in ['measured_originals_added','recovered_originals_added','handled_originals_added']:need(papers[key]==0,'index overclaim')
 replay=load(root,AUD+'/portable_report.json')
 need(replay['status']=='PASS_PUBLIC_L046_BOUNDED_NUMERICAL_CORRECTION'and replay['complete_packets']==4 and replay['logical_bindings']==226 and replay['independent_class_constant_counts']==574 and replay['lower_total']==798370 and replay['source_total']==796772,'exact public replay')
 need(replay['remaining_exact_type_counts']==116 and replay['L046_remains_pending']and replay['full_chirality_unpaid']and replay['native_pages']=={'proof':4,'common':4}and len(replay['scope_controls'])==13,'scope/native replay')
 tree_old=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());tree_new=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_L046_previous','check_L046_current'}
 def remaining(t,excluded):return[ast.dump(n,include_attributes=False)for n in t.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in excluded)]
 need(remaining(tree_old,{'main'})==remaining(tree_new,{'main'}|added),'old verifier logic changed')
 need({n.name for n in tree_new.body if isinstance(n,ast.FunctionDef)}-{n.name for n in tree_old.body if isinstance(n,ast.FunctionDef)}==added,'unexpected verifier functions')
 readme=(root/'README.rst').read_text();completion=(root/'audit/completion.rst').read_text()
 need(BASE+'/README.rst'in readme and BASE+'/README.rst'in completion,'reader links')
 need('L046 remains'in readme and 'L046 remains pending'in completion,'remaining work hidden')
 if require_gate:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_L046_BOUNDED_CORRECTION_WITH_COUNTS_UNCHANGED'and gate['whole_original_credit']==0 and gate['root_mathematical_author']and not gate['root_distinct_mathematical_reviewer'],'root role/scope')
  for row in gate['bindings']:bind(root,row)
 return dict(status='PASS_L046_BOUNDED_CORRECTION_REGISTRATION',recoveries=77,refutations=1,handled=78,pending=27,remaining_L046_exact_cells=116,new_original_credit=0)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--without-gate',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.without_gate)))
