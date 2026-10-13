"""Read-only distinct review of the concrete L046 registration candidate."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized review forbidden')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json, os, subprocess

def need(ok, message):
    if not ok:
        raise ValueError(message)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();r=a.repo.resolve();a.out.mkdir(exist_ok=False)
    candidate=json.loads(a.candidate.read_text())
    need(sha(a.candidate)=='a86b56c855855d8f9c62697b9008d5340f49fd79282259afaaa7b5a2b08ad564','exact candidate03')
    initial={}
    for row in candidate['files']:
        f=r/row['path'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'candidate binding')
        need('__pycache__'not in f.parts and f.suffix!='.pyc','generated cache excluded')
        initial[row['path']]=row['sha256']
    need(len(initial)==119,'candidate files')
    def load(path):return json.loads((r/path).read_text())
    history=load('audit/bounded-corrections/L046/v1/history_routes.json')['routes']
    for old,row in history.items():
        raw=subprocess.check_output(['git','show',candidate['baseline']+':'+old],cwd=r)
        need(raw==(r/row['path']).read_bytes(),'archived bytes differ from baseline Git')
    before=load(history['audit/corpus/latest.json']['path']);after=load('audit/corpus/latest.json')
    need(set(after)==set(before)|{'bounded_result_corrections'},'only bounded index added')
    oldkeys=set(before)-{'active_catalogue','snapshot'}
    need(all(before[k]==after[k]for k in oldkeys),'original sets/counts preserved')
    oldcat=load(before['active_catalogue']['path']);newcat=load(after['active_catalogue']['path'])
    oldrows={x['original_id']:x for x in oldcat['entries']};newrows={x['original_id']:x for x in newcat['entries']}
    need(oldrows.keys()==newrows.keys() and len(oldrows)==106,'fixed originals')
    need([k for k in oldrows if oldrows[k]!=newrows[k]]==['L046'],'only L046 changed')
    fields=[k for k in set(oldrows['L046'])|set(newrows['L046'])if oldrows['L046'].get(k)!=newrows['L046'].get(k)]
    need(set(fields)=={'edition','next_obligation','bounded_correction_evidence'},'exact evidence changes')
    need(newrows['L046']['current_principal_recovery']['status']=='PENDING_COMPLETE_RECOVERY','pending L046')
    oldtree=ast.parse((r/history['scripts/verify_snapshot.py']['path']).read_text())
    newtree=ast.parse((r/'scripts/verify_snapshot.py').read_text())
    def nodes(tree,exclude):
        return [ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,ast.FunctionDef)and n.name in exclude)]
    need(nodes(oldtree,{'main'})==nodes(newtree,{'main','check_L046_previous','check_L046_current'}),'preserved old AST')
    spec=importlib.util.spec_from_file_location('L046_distinct_registration',r/'scripts/check_L046_correction.py')
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    good=guard.verify(r,False);original=guard.load
    base='corrections/onan-map-count/v1/';index=after['bounded_result_corrections']['path'];cat=after['active_catalogue']['path']
    cases=[]
    def change(label,path,keys,value):cases.append((label,path,keys,value))
    change('pending removal','audit/corpus/latest.json',['accessible_pending_original_ids'],[x for x in after['accessible_pending_original_ids']if x!='L046'])
    for key in ['ordinary_recovery_credit','terminal_principal_disposition_credit','handled_original_credit','new_measurement_credit','new_question_credit','new_Lean_credit']:
        change('admission '+key,base+'admission.json',[key],1)
    for key in ['whole_paper_recovered','all_L046_work_finished','root_is_distinct_mathematical_reviewer']:
        change(key,base+'admission.json',[key],True)
    change('factor',base+'admission.json',['compression_factor'],2)
    change('wrong source identity',base+'admission.json',['source_ids'],['F003'])
    change('false lower total',base+'source_statement.json',['proved_lower_total'],796772)
    change('lost exact counts',base+'remaining_obligations.json',['remaining_exact_table_cells'],0)
    change('hide pending',base+'remaining_obligations.json',['keep_in_accessible_pending_original_ids'],False)
    for key in ['ordinary_recovery_credit','handled_original_credit']:
        change('index '+key,index,['entries',0,key],1)
    change('wrong manuscript route',index,['entries',0,'manuscripts',0,'pdf'],'missing.pdf')
    change('false index status',index,['status'],'COMPLETE_ORIGINAL')
    change('index source identity',index,['entries',0,'original_id'],'F003')
    change('index aggregate credit',index,['handled_originals_added'],1)
    other=next(i for i,row in enumerate(newcat['entries'])if row['original_id']!='L046')
    change('another original changed',cat,['entries',other,'next_obligation'],'Dropped')
    l046=next(i for i,row in enumerate(newcat['entries'])if row['original_id']=='L046')
    change('L046 declared recovered',cat,['entries',l046,'current_principal_recovery','status'],'RECOVERED')
    change('hidden chirality balance','audit/bounded-corrections/L046/v1/portable_report.json',['full_chirality_unpaid'],False)
    rejected=[]
    for label,path,keys,value in cases:
        def changed(root,requested,path=path,keys=keys,value=value):
            d=original(root,requested)
            if requested==path:
                d=copy.deepcopy(d);node=d
                for key in keys[:-1]:node=node[key]
                node[keys[-1]]=value
            return d
        guard.load=changed
        try:guard.verify(r,False)
        except ValueError as e:rejected.append(dict(test=label,error=str(e)))
        else:raise ValueError('accepted semantic overclaim '+label)
        finally:guard.load=original
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env.pop('PYTHONOPTIMIZE',None)
    for label,extra,child in [('python_O',['-O'],env),('environment_O',[],dict(env,PYTHONOPTIMIZE='1'))]:
        q=subprocess.run([sys.executable,*extra,str(r/'scripts/check_L046_correction.py'),'--repo',str(r),'--without-gate'],capture_output=True,env=child)
        need(q.returncode!=0 and b'Optimized Python is not accepted'in q.stderr,'optimized guard')
        rejected.append(dict(test=label,error=q.stderr.decode().splitlines()[-1]))
    need(all(sha(r/path)==h for path,h in initial.items()),'candidate changed during read-only review')
    report=dict(status='PASS_DISTINCT_L046_REGISTRATION',candidate_sha256=sha(a.candidate),candidate_files=119,
                original_entries=106,unchanged_other_originals=105,changed_L046_fields=sorted(fields),
                historical_archives_equal_baseline=5,old_nonmain_AST_nodes=len(nodes(oldtree,{'main'})),
                old_function_definitions=len([n for n in oldtree.body if isinstance(n,ast.FunctionDef)]),
                unchanged_corpus_fields=len(oldkeys),guard_result=good,rejection_controls=rejected,
                historical_full_replay_reused=True,mathematical_replay_repeated=False,
                public_bytes_unchanged=True,root_gate_still_required=True)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='rejection_controls'}));print('Rejected controls:',len(rejected))
if __name__=='__main__':main()
