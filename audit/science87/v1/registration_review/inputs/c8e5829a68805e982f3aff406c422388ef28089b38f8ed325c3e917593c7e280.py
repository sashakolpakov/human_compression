"""Install a reviewed private six-source candidate; public execution is root-only.

Every accepted payload and proposal is immutable. No final gate, mathematical
review, measurement or new question disposition is manufactured here.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('science87_guard',HERE/'check_science87.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
AUD=guard.AUD;HISTORY=guard.HISTORY;IDS=guard.IDS;RECOVERED=guard.RECOVERED;REFUTED=guard.REFUTED
PUBLIC=Path('/Users/sasha/medusa/math_compression')
def need(x,m):guard.need(x,m)
def load(p):return json.loads(p.read_text())
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,root):return dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=sha(p))
def main(a):
 root=a.repo.resolve();bundle=a.bundle.resolve();params=load(HERE/'registration_parameters.json')
 need(root!=PUBLIC.resolve()or a.allow_public_write,'Root alone installs public repository')
 need(params['baseline']==guard.BASELINE and params['source_ids']==IDS,'Exact accepted transition')
 need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==guard.BASELINE,'Exact predecessor commit')
 need(not subprocess.check_output(['git','diff','HEAD','--name-only'],cwd=root).strip(),'Clean tracked predecessor')
 need(not(root/AUD).exists(),'Fresh candidate; preserve prior trials')
 stage=bundle/'stage';manifest=load(bundle/'stage_manifest.json');need(pin(bundle/'stage_manifest.json',bundle)==params['bundle_manifest'],'Exact accepted payload bundle')
 need(pin(bundle/'accepted_bundle.json',bundle)==params['bundle_record'],'Exact operational bundle record')
 for r in manifest['files']:
  p=guard.bind(stage,r);q=root/r['path'];need(not q.exists()or q.read_bytes()==p.read_bytes(),'No replacement of earlier payload '+r['path'])
 for p in params['packages']:
  guard.bind(stage,p['proposal']);op=load(stage/p['operational_review']['path'])
  need(op['original_manifest_sha256']==p['operational_manifest_sha256']and op['original_status']==p['operational_status'],'Exact accepted operation')
 old=load(root/'audit/corpus/latest.json');need([old[k]for k in ['admitted_principal_originals','refuted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery']]==[85,5,90,15],'Actual predecessor counts')
 need(all(s in old['accessible_pending_original_ids']for s in IDS),'Six genuinely pending originals')
 new_verifier=guard.verifier_delta((root/'scripts/verify_snapshot.py').read_text())
 # Verify the full Git predecessor before any repository mutation.
 tree=load(HERE/'predecessor_tree.json');need(tree['commit']==guard.BASELINE,'Exact predecessor tree')
 for r in tree['files']:
  p=root/r['path']
  if r['mode']=='120000':need(p.is_symlink()and str(p.readlink())==r['link'],'Exact old symlink')
  else:guard.bind(root,r);need(bool(p.stat().st_mode&0o111)==(r['mode']=='100755'),'Exact executable mode')
 # Prepare admissions entirely in memory, acquiring rather than editing proposals.
 proposals={p['id']:load(stage/p['proposal']['path'])for p in params['packages']};admissions={}
 for sid,s in params['source_specs'].items():
  ordinary=sid in RECOVERED
  admissions[sid]=dict(status='ACCEPTED_MATHEMATICS_REGISTRATION_REQUIRES_ROOT_GATES',source_ids=[sid],disposition_kind='ordinary_recovery'if ordinary else'principal_statement_refuted',accepted_proposal=s['proposal'],accepted_proposal_contents=proposals[s['package_id']],source_contract=s['source_contract'],operational_review=s['operational_review'],registration_baseline=guard.BASELINE,publication_gate=guard.final_gate(sid),shared_registration_gate=AUD+'/root_integration.json',ordinary_recovery_credit=int(ordinary),principal_refutation_credit=int(not ordinary),handled_original_credit=1,new_measurements=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,all_source_assertions_reproved=False,compression_factor=None,software_inclusive_factor=None,all_other_valid_source_claims_recovered=False if not ordinary else None,complete_manuscripts=s['manuscripts'],scope_note=s['scope_note'])
 narratives={}
 for name in ['README.rst','audit/completion.rst','audit/protocol.tex']:
  text=(root/name).read_text()
  for r in params['narrative_delta']:
   if r['path']!=name:continue
   need(text.count(r['before'])==r['occurrences'],'Exact narrative predecessor '+name);text=text.replace(r['before'],r['after'])
  narratives[name]=text
 # This is the first mutation. All package/gate/baseline inputs were validated.
 history={}
 for name in HISTORY:
  p=root/AUD/'previous'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/name,p);history[name]=pin(p,root)
 dump(root/AUD/'history_routes.json',dict(baseline_commit=guard.BASELINE,routes=history))
 for r in manifest['files']:
  q=root/r['path'];q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists():shutil.copyfile(stage/r['path'],q)
 shutil.copyfile(bundle/'accepted_bundle.json',root/AUD/'accepted_bundle.json');shutil.copyfile(bundle/'stage_manifest.json',root/AUD/'payload_manifest.json');shutil.copyfile(HERE/'predecessor_tree.json',root/AUD/'predecessor_tree.json')
 for sid,a1 in admissions.items():dump(root/guard.admission_path(sid),a1)
 ap={sid:pin(root/guard.admission_path(sid),root)for sid in IDS}
 registrations=[]
 for ids,ordinary,name in [(RECOVERED,True,'new_original_registration.json'),(REFUTED,False,'principal_refutation_registration.json')]:
  reg=dict(status='REVIEWED_DISPOSITIONS_REQUIRING_ROOT_GATES',source_ids=ids,admissions=[ap[s]for s in ids],ordinary_recoveries_added=2 if ordinary else 0,principal_refutations_added=0 if ordinary else 4,handled_originals_added=len(ids),new_measurements=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None,previous_science_registration=old['current_science_registration'],previous_disposition_registration=old['current_principal_disposition_registration'],previous_corpus=history['audit/corpus/latest.json'],publication_gate=AUD+'/root_integration.json',individual_publication_gates=[guard.final_gate(s)for s in ids])
  dump(root/AUD/name,reg);registrations.append(pin(root/AUD/name,root))
 cat=load(root/old['active_catalogue']['path']);dispositions={}
 for e in cat['entries']:
  sid=e['original_id']
  if sid not in IDS:continue
  s=params['source_specs'][sid];ordinary=sid in RECOVERED;historic=copy.deepcopy(e['current_principal_recovery'])
  d=dict(status='CORRECTED_PRINCIPAL_RECOVERY_ACCEPTED_MEASUREMENT_PENDING'if ordinary else'CLOSED_BY_REVIEWED_PRINCIPAL_REFUTATION',disposition_kind=admissions[sid]['disposition_kind'],principal_contract_admitted=ordinary,complete_principal_contract_recovered=ordinary,original_fully_handled=ordinary,all_original_assertions_claimed=False,whole_source_formalized=False,measured=False,compression_factor=None,latest_admission_references=[ap[sid]],historical_admission_evidence=historic,source_contract=s['source_contract'],source_qualifications=s['scope_note'],accepted_proposal=s['proposal'])
  e['edition']=s['edition'];e['current_principal_recovery']=d;e['next_obligation']=s['scope_note'];dispositions[sid]=d
 cat.update(status='CURRENT_ACCESSIBLE106_87_RECOVERED_9_REFUTED_9_PENDING',admitted_principal_originals=87,accessible_pending_complete_recovery=9,refuted_principal_originals=9,refuted_principal_original_ids=old['refuted_principal_original_ids']+REFUTED,handled_mathematical_originals=96,handled_mathematical_original_ids=sorted(old['handled_mathematical_original_ids']+IDS),measurement_pending_original_ids=sorted(old['measurement_pending_original_ids']+RECOVERED),new_principal_refutation_credit=4,review_revision='L027 and L076 receive separately scoped corrected principal recoveries. L036, L046, L063 and L064 receive separately scoped principal-refutation dispositions; L063/L064 share one omission. All unpaid source assertions, retained inputs and historical decisions remain explicit. No new measurement, question, Lean or compression credit.',previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=87,refuted=9,handled=96,measured=53,measurement_pending=34,pending=9,editorial=1))
 cp=root/'audit/corpus/accessible106/updates/science87-six-dispositions-catalogue.json';dump(cp,cat)
 current=copy.deepcopy(old);current.pop('snapshot');current.update(status='CURRENT_PROGRAMME_87_RECOVERED_9_REFUTED_9_PENDING_1_EDITORIAL',admitted_principal_originals=87,accessible_pending_complete_recovery=9,accessible_pending_original_ids=[s for s in old['accessible_pending_original_ids']if s not in IDS],refuted_principal_originals=9,refuted_principal_original_ids=old['refuted_principal_original_ids']+REFUTED,handled_mathematical_originals=96,previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pin(cp,root),current_science_registration=registrations[0],current_principal_disposition_registration=registrations[1])
 for k in ['admitted_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids']:current[k]=sorted(old[k]+RECOVERED)
 current['handled_mathematical_original_ids']=sorted(old['handled_mathematical_original_ids']+IDS);current['added_admissions']+=[ap[s]for s in RECOVERED];current['principal_refutation_admissions'].append(registrations[1])
 sp=root/'audit/corpus/updates/accessible106-science87-six-dispositions.json';dump(sp,current);current['snapshot']=pin(sp,root);dump(root/'audit/corpus/latest.json',current)
 native_additions={}
 for name,ids in [('papers/catalogue_corrected_unmeasured.json',RECOVERED),('papers/catalogue_principal_refutations.json',REFUTED)]:
  native=load(root/name);native['original_ids']+=ids;new=[];seen=set()
  for sid in ids:
   for m in params['source_specs'][sid]['manuscripts']:
    if m['id']in seen:continue
    seen.add(m['id']);sources=m['source_ids'];ordinary=sid in RECOVERED
    entry=dict(id=m['id'],title=m['title'],tex=m['tex']['path'],pdf=m['pdf']['path'],tex_inputs=[x['path']for x in m['tex_inputs']],compiler='pdflatex',physical_pages=m['physical_pages'],source_ids=sources,role='Immediate principal recovery manuscript; complete acquired proof and validation closure retained'if ordinary else'principal_statement_refutation',measured=False,compression_factor=None,admission=ap[sources[0]])
    if ordinary:entry.update(topic=m['topic'],comparison_topic_created=False,existing_public_dependency=False)
    if len(sources)>1:entry['additional_admissions']=[ap[s]for s in sources[1:]]
    new.append(entry)
  native['entries']+=new
  if 'root_publication_gate'in native:native['root_publication_gate']=AUD+'/root_integration.json'
  dump(root/name,native);native_additions[name]=new
 paper=load(root/'papers/latest_catalogue.json');paper.update(active_source_catalogue=current['active_catalogue'],corrected_unmeasured_scientific_catalogue=pin(root/'papers/catalogue_corrected_unmeasured.json',root),principal_refutation_catalogue=pin(root/'papers/catalogue_principal_refutations.json',root));dump(root/'papers/latest_catalogue.json',paper)
 finalparams=copy.deepcopy(params);finalparams.update(catalogue_dispositions=dispositions,native_additions=native_additions);dump(root/AUD/'registration_parameters.json',finalparams)
 for name,text in narratives.items():(root/name).write_text(text)
 (root/'scripts/verify_snapshot.py').write_text(new_verifier)
 for name in ['check_science87.py','check_science87_history.py']:shutil.copyfile(HERE/name,root/'scripts'/name)
 if a.build_protocol:
  for i in [1,2]:
   r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','protocol.tex'],cwd=root/'audit',capture_output=True,timeout=60)
   (root/AUD/f'protocol{i}.stdout').write_bytes(r.stdout);(root/AUD/f'protocol{i}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'Native protocol pass')
 print(json.dumps(dict(status='SCIENCE87_PRIVATE_CANDIDATE_NOT_ADMITTED',source_ids=IDS,ordinary=2,principal_refutations=4,final_root_gate_created=False,preflight=f'python scripts/check_science87.py --repo {root} --preflight')))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--allow-public-write',action='store_true');p.add_argument('--build-protocol',action='store_true');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
