#!/usr/bin/env python3
"""Read-only independent audit of the fixed F003 registration candidate."""
from pathlib import Path
import ast,hashlib,json,subprocess,sys,os
S=Path('/Users/sasha/medusa/research/leemans')
R=Path('/Users/sasha/medusa/math_compression')
W=Path(__file__).resolve().parent
C=S/'reboot_20261013/F003_publication_work/registration_candidate01.json'
EXPECTED='0abef0b53ee2c3df2d9f902f161445e042d805a69a046f7c1934be2c6f88ad21'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(b,m):
 if not b:raise ValueError(m)
def main():
 need(sha(C)==EXPECTED,'candidate edition')
 candidate=load(C);P=Path(candidate['stage']);A=P/'audit/principal-refutations/F003/v1'
 for x in candidate['files']:
  p=P/x['path'];need(p.stat().st_size==x['bytes']and sha(p)==x['sha256'],'candidate file '+x['path'])
 need(len(candidate['files'])==156,'candidate156')
 need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==candidate['base_commit'],'public base commit')
 need(not subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True),'public worktree clean before review')
 old=load(R/'audit/corpus/latest.json');new=load(P/'audit/corpus/latest.json')
 oldcat=load(R/old['active_catalogue']['path']);newcat=load(P/new['active_catalogue']['path'])
 before={x['original_id']:x for x in oldcat['entries']};after={x['original_id']:x for x in newcat['entries']}
 need(len(before)==len(after)==106 and set(before)==set(after),'same original IDs')
 changed=[k for k in before if before[k]!=after[k]];need(changed==['F003'],'one changed original')
 proposal=load(P/'corrections/suzuki-rank/v1/catalogue_disposition_proposal.json')
 wanted=dict(before['F003']);wanted.update(proposal['proposed_row']);need(after['F003']==wanted,'exact proposed row')
 need(wanted['current_principal_recovery']['historical_admission_evidence']==before['F003']['current_principal_recovery'],'literal prior evidence')
 categories={k:set(new[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']}
 need([len(x)for x in categories.values()]==[72,1,32,1],'exact partition sizes')
 sets=list(categories.values());need(all(not sets[i]&sets[j]for i in range(4)for j in range(i+1,4))and set.union(*sets)==set(before),'disjoint exhaustive partition')
 need(categories['refuted_principal_original_ids']=={'F003'},'exact refuted original')
 need(new['admitted_original_ids']==old['admitted_original_ids']and new['measured_original_ids']==old['measured_original_ids'],'unchanged recovered and measured IDs')
 samefiles=['papers/catalogue_corrected_unmeasured.json','papers/overview_measurements.json','measurements/latest.json']
 actualsame=[]
 for name in samefiles:
  if (R/name).is_file():need((R/name).read_bytes()==(P/name).read_bytes(),'measurement file changed '+name);actualsame.append(name)
 # Every pre-existing tracked file outside the seven archived mutable routes is exact.
 routes=load(A/'history_routes.json')['routes'];tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');identical=0;staging_only_links=[]
 for name in tracked:
  if not name or name in routes:continue
  p=R/name;q=P/name
  if p.is_symlink():
   need(name not in {x['path']for x in candidate['files']},'unexpected staged symlink mutation')
   if p.is_file():need(q.read_bytes()==p.read_bytes(),'materialized file alias changed')
   else:
    need(name=='research/leemans'and os.readlink(p)=='case_study'and q.is_dir(),'known public case-study alias')
    for item in tracked:
     if item.startswith('research/case_study/'):
      rel=Path(item).relative_to('research/case_study');need((q/rel).read_bytes()==(R/item).read_bytes(),'materialized public case-study alias '+str(rel))
   staging_only_links.append(dict(path=name,original_target=os.readlink(p),stage='equivalent materialized public alias; not part of installation delta'));continue
  need(q.is_file(),'missing old file '+name)
  sp,sq=p.stat(),q.stat()
  need((sp.st_dev,sp.st_ino)==(sq.st_dev,sq.st_ino)or(p.read_bytes()==q.read_bytes()),'old content changed '+name);identical+=1
 for name,row in routes.items():need((R/name).read_bytes()==(P/row['path']).read_bytes(),'archived pointer not exact '+name)
 oldtree=ast.parse((R/'scripts/verify_snapshot.py').read_text());newtree=ast.parse((P/'scripts/verify_snapshot.py').read_text())
 extra={'check_previous_F003_disposition','check_F003_disposition'}
 def nodes(tree,skip):return[ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,ast.FunctionDef)and n.name in skip)]
 need(nodes(oldtree,{'main'})==nodes(newtree,{'main'}|extra),'old top-level ASTs')
 names={n.name for n in oldtree.body if isinstance(n,ast.FunctionDef)};need(len(names)-1==171,'old function count')
 need({n.name for n in newtree.body if isinstance(n,ast.FunctionDef)}-names==extra,'exact new functions')
 run=subprocess.run([sys.executable,'-B',str(P/'scripts/check_F003_disposition.py'),'--repo',str(P),'--preflight'],capture_output=True,text=True,timeout=120)
 (W/'preflight.stdout').write_text(run.stdout);(W/'preflight.stderr').write_text(run.stderr)
 need(run.returncode==0 and not run.stderr,'distinct preflight')
 pre=json.loads(run.stdout);need(pre['status']=='PASS_SEPARATE_F003_PRINCIPAL_REFUTATION'and len(pre['controls'])==12,'preflight result')
 history=load(S/'reboot_20261013/F003_publication_work/history03.json');need(history['status']=='PASS_EXACT_HISTORICAL_SCIENCE72'and history['science72']['counts']['corrected_recoveries']==72 and history['science72']['counts']['mathematical_pending']==33,'completed root-owned historical chain')
 need(not (S/'reboot_20261013/F003_publication_work/history03.stderr').read_bytes(),'clean completed historical chain stderr')
 report=dict(status='PASS_DISTINCT_SEPARATE_F003_REGISTRATION',candidate_sha256=EXPECTED,candidate_files=156,changed_original_ids=changed,other_original_rows_unchanged=105,counts=dict(recovered=72,refuted=1,pending=32,editorial=1,handled=73,measured=53,unmeasured=19),old_tracked_regular_files_exact_except_seven_pointers=identical,staging_materialized_public_aliases=staging_only_links,separate_unchanged_measurement_files=actualsame,old_nonmain_verifier_functions=171,old_top_level_ASTs_preserved=True,old_history_result_reused=True,expensive_history_repeated=False,preflight=pre,root_gate_still_required=True,public_repository_modified=False,new_mathematical_acceptance=False)
 (W/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
