"""Install one exact reviewed L091 registration; root owns public mutation."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,ctypes,hashlib,importlib.util,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent;PUBLIC=Path('/Users/sasha/medusa/math_compression')
spec=importlib.util.spec_from_file_location('science91_guard',HERE/'check_science91.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
AUD=guard.AUD;IDS=guard.IDS;HISTORY=guard.HISTORY

def need(v,m):guard.need(v,m)
def load(p):return json.loads(p.read_text())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p,root):return dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def clone_or_copy(p,q):
 need(shutil.disk_usage(q.parent).free>4*2**30+p.stat().st_size,'4 GiB disk reserve')
 if sys.platform=='darwin':
  lib=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True);fn=lib.clonefile;fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int];fn.restype=ctypes.c_int
  if fn(os.fsencode(p),os.fsencode(q),0):raise OSError(ctypes.get_errno(),str(q))
  need(p.stat().st_ino!=q.stat().st_ino,'Independent clone inode')
 else:shutil.copyfile(p,q)
 need(pin(p,p.parent)['sha256']==pin(q,q.parent)['sha256'],'Exact installed bytes')
def main(a):
 root=a.repo.resolve();params=load(HERE/'registration_parameters.json');install=load(HERE/'install_files.json')['files'];payload=load(HERE/'payload_manifest.json')
 need(root==PUBLIC.resolve(),'Single explicit public destination; no repository copies')
 need(a.verify_inputs or a.allow_public_write,'Root must explicitly authorize installation')
 need(params['baseline']==guard.BASELINE and params['source_ids']==IDS,'Exact accepted transition')
 need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==guard.BASELINE,'Exact predecessor commit')
 need(not subprocess.check_output(['git','status','--porcelain'],cwd=root).strip(),'Clean predecessor')
 need(not(root/AUD).exists(),'Fresh registration; preserve prior attempts')
 need([{k:v for k,v in r.items()if k!='source_path'}for r in install]==payload['files'],'Exact installation list')
 for r in install:
  p=Path(r['source_path']);need(p.is_file()and p.stat().st_size==r['bytes']and guard.sha(p)==r['sha256'],'Exact payload source '+str(p));q=guard.safe(root,r['path'])
  need(not q.exists(),'Every new payload path is fresh '+r['path'])
 old=load(root/'audit/corpus/latest.json');need([old[k]for k in ['admitted_principal_originals','refuted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery']]==[90,9,99,6],'Exact predecessor counts');need('L091'in old['accessible_pending_original_ids'],'Pending source')
 new_verifier=guard.verifier_delta((root/'scripts/verify_snapshot.py').read_text());tree=load(HERE/'predecessor_tree.json');need(tree['commit']==guard.BASELINE,'Exact tree')
 for r in tree['files']:
  p=root/r['path']
  if r['mode']=='120000':need(p.is_symlink()and str(p.readlink())==r['link'],'Exact old symlink')
  else:guard.bind(root,r);need(bool(p.stat().st_mode&0o111)==(r['mode']=='100755'),'Exact old executable mode')
 package=params['package'];route={r['path']:Path(r['source_path'])for r in install};proposal=load(route[package['proposal']['path']]);source=params['source_spec'];admission=guard.expected_admission(source,proposal)
 need(guard.sha(route[package['proposal']['path']])==guard.PROPOSAL_SHA,'Exact accepted proposal')
 op=load(route[package['operational_review']['path']]);need(op['original_manifest_sha256']==guard.OP_SHA and op['original_status']==params['operational_status'],'Exact operational gate')
 narratives={}
 for name in ['README.rst','audit/completion.rst','audit/protocol.tex']:
  text=(root/name).read_text()
  for r in params['narrative_delta']:
   if r['path']!=name:continue
   need(text.count(r['before'])==r['occurrences'],'Exact narrative anchor '+name);text=text.replace(r['before'],r['after'])
  narratives[name]=text
 projected=copy.deepcopy(old);projected.update(copy.deepcopy(params['machine_set_fields']))
 guard.semantics(projected,old,admission,source,proposal);controls=guard.damaged_controls(projected,old,admission,source,proposal)
 if a.verify_inputs:
  print(json.dumps(dict(status='PASS_SCIENCE91_EXACT_INSTALLATION_INPUTS',payload_files=len(install),predecessor_paths=len(tree['files']),controls=controls,whole_repository_copied=False,public_writes=False)));return
 # First mutation follows all exact input, baseline, narrative and semantic checks.
 history={}
 for name in HISTORY:
  p=root/AUD/'previous'/name;p.parent.mkdir(parents=True,exist_ok=True);clone_or_copy(root/name,p);history[name]=pin(p,root)
 archive=root/AUD/'manifest_history/predecessor_publication_manifest.json';archive.parent.mkdir(parents=True,exist_ok=True);clone_or_copy(root/'provenance/publication_manifest.json',archive)
 dump(root/AUD/'history_routes.json',dict(baseline_commit=guard.BASELINE,routes=history))
 for r in install:
  q=root/r['path'];q.parent.mkdir(parents=True,exist_ok=True);clone_or_copy(Path(r['source_path']),q)
 for name in ['payload_manifest.json','predecessor_tree.json']:
  q=root/AUD/name;clone_or_copy(HERE/name,q)
 dump(root/guard.admission_path(),admission);ap=pin(root/guard.admission_path(),root)
 reg=dict(status='REVIEWED_DISPOSITIONS_REQUIRING_ROOT_GATES',source_ids=IDS,admissions=[ap],ordinary_recoveries_added=1,principal_refutations_added=0,handled_originals_added=1,new_measurements=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None,previous_science_registration=old['current_science_registration'],previous_disposition_registration=old['current_principal_disposition_registration'],previous_corpus=history['audit/corpus/latest.json'],publication_gate=AUD+'/root_integration.json',individual_publication_gates=[guard.final_gate()])
 dump(root/AUD/'new_original_registration.json',reg);rp=pin(root/AUD/'new_original_registration.json',root)
 cat=load(root/old['active_catalogue']['path']);entry=next(e for e in cat['entries']if e['original_id']=='L091');historic=copy.deepcopy(entry['current_principal_recovery'])
 disposition=dict(status='CORRECTED_PRINCIPAL_RECOVERY_ACCEPTED_MEASUREMENT_PENDING',disposition_kind='ordinary_recovery',principal_contract_admitted=True,complete_principal_contract_recovered=True,original_fully_handled=True,all_original_assertions_claimed=False,whole_source_formalized=False,measured=False,compression_factor=None,latest_admission_references=[ap],historical_admission_evidence=historic,source_contract=source['source_contract'],source_qualifications=source['scope_note'],accepted_proposal=source['proposal'])
 entry.update(authors=source['authors'],edition=source['edition'],current_principal_recovery=disposition,next_obligation=source['scope_note'])
 cat.update(status='CURRENT_ACCESSIBLE106_91_RECOVERED_9_PRINCIPAL_REFUTATIONS_5_PENDING',admitted_principal_originals=91,accessible_pending_complete_recovery=5,handled_mathematical_originals=100,handled_mathematical_original_ids=sorted(old['handled_mathematical_original_ids']+IDS),measurement_pending_original_ids=sorted(old['measurement_pending_original_ids']+IDS),new_principal_refutation_credit=0,review_revision='L091 receives a complete corrected disposition of nineteen source interfaces, all 86 HS diagrams and the acquired supplement. The six-page source and supplement editions are explicit; J3 global coverage remains borrowed from L097. All nine principal refutations retain surviving-claim obligations. No new measurement, question, Lean, principal-refutation or compression credit.',previous_catalogue=old['active_catalogue'],current_recovery_counts=dict(active=106,admitted=91,refuted=9,handled=100,measured=53,measurement_pending=38,pending=5,editorial=1,surviving_claim_obligations=9,completion_obligations=14))
 cp=root/'audit/corpus/accessible106/updates/science91-L091-catalogue.json';dump(cp,cat)
 current=projected;current.pop('snapshot');current.update(previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=pin(cp,root),current_science_registration=rp);current['added_admissions'].append(ap)
 sp=root/'audit/corpus/updates/accessible106-science91-L091.json';dump(sp,current);current['snapshot']=pin(sp,root);dump(root/'audit/corpus/latest.json',current)
 native=load(root/'papers/catalogue_corrected_unmeasured.json');native['original_ids']+=IDS;new=[]
 for m in source['manuscripts']:
  new.append(dict(id=m['id'],title=m['title'],tex=m['tex']['path'],pdf=m['pdf']['path'],tex_inputs=[x['path']for x in m['tex_inputs']],compiler='pdflatex',physical_pages=m['physical_pages'],source_ids=IDS,role='Complete corrected L091 source disposition; acquired proof and validation evidence retained',measured=False,compression_factor=None,admission=ap,topic=proposal['title'],comparison_topic_created=False,existing_public_dependency=False))
 native['entries']+=new
 if 'root_publication_gate'in native:native['root_publication_gate']=AUD+'/root_integration.json'
 dump(root/'papers/catalogue_corrected_unmeasured.json',native)
 paper=load(root/'papers/latest_catalogue.json');paper.update(status='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_THIRTY_EIGHT_CORRECTED_UNMEASURED',active_source_catalogue=current['active_catalogue'],corrected_unmeasured_scientific_catalogue=pin(root/'papers/catalogue_corrected_unmeasured.json',root));dump(root/'papers/latest_catalogue.json',paper)
 finalparams=copy.deepcopy(params);finalparams.update(catalogue_disposition=disposition,native_additions=new);dump(root/AUD/'registration_parameters.json',finalparams)
 for name,text in narratives.items():(root/name).write_text(text)
 (root/'scripts/verify_snapshot.py').write_text(new_verifier);shutil.copyfile(HERE/'check_science91.py',root/'scripts/check_science91.py')
 if a.build_protocol:
  old_native={n:(root/'audit'/n).read_bytes()for n in ['protocol.log','protocol.aux','protocol.out']if(root/'audit'/n).exists()}
  for i in [1,2]:
   r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','protocol.tex'],cwd=root/'audit',capture_output=True,timeout=60);(root/AUD/f'protocol{i}.stdout').write_bytes(r.stdout);(root/AUD/f'protocol{i}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'Native protocol build')
  for n,b in old_native.items():shutil.copyfile(root/'audit'/n,root/AUD/('rebuilt_'+n));(root/'audit'/n).write_bytes(b)
 print(json.dumps(dict(status='SCIENCE91_INSTALLED_CANDIDATE_REQUIRES_ROOT_GATES',source_ids=IDS,ordinary=1,principal_refutations=0,final_root_gate_created=False,whole_repository_copied=False,preflight=f'python scripts/check_science91.py --repo {root} --preflight')))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--verify-inputs',action='store_true');p.add_argument('--allow-public-write',action='store_true');p.add_argument('--build-protocol',action='store_true');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
