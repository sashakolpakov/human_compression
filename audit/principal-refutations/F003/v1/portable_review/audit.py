#!/usr/bin/env python3
"""Distinct operational audit; explicit public-only reconstruction and disposition checks."""
import copy, hashlib, json, shutil, subprocess, sys
from pathlib import Path
S=Path('/Users/sasha/medusa/research/leemans')
R=Path('/Users/sasha/medusa/math_compression')
W=Path(__file__).resolve().parent
P=S/'reboot_20261013/F003_publication_work/stage01/corrections/suzuki-rank/v1'
EXPECTED='abdef1dcb1de90f4047cf52b812590d29a3ec1056511af201c5f6ab3f3fcdad2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(b,m):
 if not b:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def check_disposition(d):
 require(d['original_id']=='F003' and d['classification']=='REVIEWED_PRINCIPAL_STATEMENT_REFUTATION','disposition class')
 require(d['status']=='PRIVATE_PROPOSED_PRINCIPAL_REFUTATION_DISPOSITION_NOT_APPLIED' and d['public_mutations']==0,'proposal only')
 for key in ('ordinary_recovery_credit','measurement_credit','new_question_credit','new_Lean_credit'):require(d[key]==0,key)
 require(d['compression_factor'] is None,'factor')
 r=d['proposed_row']['current_principal_recovery']
 require(r['status']=='CLOSED_BY_REVIEWED_PRINCIPAL_REFUTATION' and r['disposition_kind']=='principal_statement_refuted','row disposition')
 require(r['original_fully_handled'] is True and r['principal_contract_admitted'] is False,'false theorem not recovered')
 for key in ('all_original_assertions_claimed','whole_source_formalized','measured'):require(r[key] is False,key)
 require(r['compression_factor'] is None and r['source_target']=='Theorem 1.1, fixed arXiv:2010.04080v1','row source boundary')
 ledger=d['ledger_rule']
 require(ledger['add_to']=='refuted_principal_original_ids' and ledger['remove_from']=='accessible_pending_original_ids','ledger sets')
 require(set(ledger['do_not_add_to'])=={'admitted_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','measured_original_ids'},'no ordinary credit')
 require(len(d['count_scenarios'])==2,'scenarios')
 for c,recovered in zip(d['count_scenarios'],(71,72)):
  require(c['recovered']==recovered and c['refuted']==1 and c['editorial']==1,'scenario fixed sets')
  require(c['mathematical_handled']==recovered+1 and c['mathematical_pending']==104-recovered,'handled arithmetic')
  require(c['measured']==53 and c['unmeasured_recoveries']==recovered-53,'measurement partition')
  require(c['mathematical_handled']+c['mathematical_pending']==105,'stop boundary')
def main():
 require(sha(P/'manifest.json')==EXPECTED,'frozen wrapper edition')
 m=load(P/'manifest.json');exports=m['exports']
 for e in exports:
  f=P/e['path'];require(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'export '+e['path'])
 t=load(P/'transport.json');routes=t['files']
 require(len(routes)==116 and len({x['logical_path'] for x in routes})==116,'complete distinct routes')
 mini=W/'mini_repo';target=mini/'corrections/suzuki-rank/v1'
 require(not mini.exists(),'fresh mini repo required')
 target.parent.mkdir(parents=True);shutil.copytree(P,target)
 originals=0;omitted=[];existing=[]
 for x in routes:
  if x['transport']=='PRIMARY_SOURCE_HASH_ONLY':omitted.append(x['logical_path']);continue
  original=S/x['logical_path']
  if x['transport']=='EXISTING_PUBLIC':
   original=R/x['public_path'];dest=mini/x['public_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,dest);existing.append(x['public_path'])
  else:dest=mini/x['public_path']
  require(original.is_file() and original.stat().st_size==x['bytes'] and sha(original)==x['sha256'],'original binding '+x['logical_path'])
  require(dest.read_bytes()==original.read_bytes(),'route is exact copy '+x['logical_path']);originals+=1
 require(originals==105 and len(omitted)==11 and len(existing)==1,'transport partition')
 d=load(P/'catalogue_disposition_proposal.json');check_disposition(d)
 changes=[('ordinary_credit',lambda x:x.update(ordinary_recovery_credit=1)),('measurement',lambda x:x.update(measurement_credit=1)),('question',lambda x:x.update(new_question_credit=1)),('formal',lambda x:x.update(new_Lean_credit=1)),('factor',lambda x:x.update(compression_factor=2)),('admitted',lambda x:x['proposed_row']['current_principal_recovery'].update(principal_contract_admitted=True)),('later_edition',lambda x:x['proposed_row']['current_principal_recovery'].update(source_target='all editions')),('ordinary_set',lambda x:x['ledger_rule'].update(add_to='admitted_original_ids')),('pending_count',lambda x:x['count_scenarios'][1].update(mathematical_pending=33)),('applied',lambda x:x.update(public_mutations=1))]
 controls=[]
 for name,change in changes:
  bad=copy.deepcopy(d);change(bad)
  try:check_disposition(bad)
  except ValueError:controls.append(name)
  else:raise ValueError('accepted invalid disposition '+name)
 out=W/'public_replay01'
 run=subprocess.run([sys.executable,'-B',str(target/'check.py'),'--repo',str(mini),'--out',str(out),'--render','--gap','/opt/homebrew/bin/gap'],capture_output=True,text=True,timeout=180)
 (W/'wrapper.stdout').write_text(run.stdout);(W/'wrapper.stderr').write_text(run.stderr)
 require(run.returncode==0 and not run.stderr,'public-only wrapper replay')
 rep=load(out/'report.json');require(rep['status']=='PASS_PUBLIC_CORRECTION_REPLAY','wrapper completion')
 for e in exports:require(sha(P/e['path'])==e['sha256'],'frozen original changed')
 report=dict(status='PASS_DISTINCT_PORTABILITY_AND_DISPOSITION_REVIEW',wrapper_manifest=EXPECTED,exports=len(exports),exact_transported_originals=originals,documentary_primary_hash_only=omitted,existing_public=existing,complete_packets=7,packet_exports=sum(p['exports']for p in t['complete_packets']),disposition_negative_controls=controls,public_replay=rep,public_repository_mutated=False,new_mathematical_acceptance=False,ordinary_recovery_credit=0,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None)
 (W/'audit_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
