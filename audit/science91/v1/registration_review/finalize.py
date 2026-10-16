"""Root-run publication gates and exact tracked manifest; no scientific replay."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.util,json,shutil,subprocess
R=Path('/Users/sasha/medusa/math_compression');AUD='audit/science91/v1';A=R/AUD;B=R/'audit/recoveries/L091/v1';BASE='110e43587523df4ae47b6c037cc6b19237a3edf4'
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
def pin(p,root=R):return dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=sha(p))
def exact(p,r):need(p.is_file()and p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'Exact binding '+str(p))
def save(p,z):need(not p.exists(),'Never replace frozen gate '+str(p));p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(z,indent=2)+'\n')
def changed_paths():
 names=set(subprocess.check_output(['git','diff','HEAD','--name-only','-z'],cwd=R).decode().split('\0'))|set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=R).decode().split('\0'));names.discard('');return sorted(names)
def gates(a):
 D=a.review.resolve();m=load(D/'manifest.json');need(sha(D/'manifest.json')==a.review_sha and m['status']=='ACCEPTED_SCIENCE91_REGISTRATION','Exact root registration acceptance')
 need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()==BASE,'Uncommitted exact predecessor')
 for r in m['exports']:exact(D/r['path'],r)
 deps=load(D/'dependencies.json');need(isinstance(deps,list),'Explicit root dependency list')
 for r in deps:
  p=Path(r['path']);need(p.is_absolute(),'Explicit absolute root binding');exact(p,r)
 preflight=load(a.preflight_report);need(preflight['status']=='PASS_SCIENCE91_L091_RECOVERY','Actual successful installed preflight report')
 need(preflight['counts']==dict(active=106,corrected_recoveries=91,refuted=9,handled=100,measured=53,unmeasured=38,mathematical_pending=5,editorial=1,archived=55,comparison_topics=19,surviving_claim_obligations=9,completion_obligations=14),'Exact acquired counts')
 need(not(A/'registration_review').exists()and not(A/'integration_checks').exists(),'Fresh gate evidence')
 allowed=set(['README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py','scripts/check_science91.py','audit/protocol.tex','audit/protocol.pdf','audit/corpus/accessible106/updates/science91-L091-catalogue.json','audit/corpus/updates/accessible106-science91-L091.json'])
 candidate=[]
 for name in changed_paths():
  need(name in allowed or name.startswith((AUD+'/','audit/recoveries/L091/','papers/recoveries/L091/')),'Only reviewed L091 transition '+name)
  p=R/name;need(p.is_file()and not p.is_symlink(),'Ordinary candidate file');candidate.append(pin(p))
 for r in m['exports']+[dict(path='manifest.json',bytes=(D/'manifest.json').stat().st_size,sha256=a.review_sha)]:
  q=A/'registration_review'/r['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(D/r['path'],q)
 checks=A/'integration_checks';checks.mkdir();shutil.copyfile(a.preflight_report,checks/'installed_preflight.json')
 save(checks/'candidate_files.json',dict(status='EXACT_INSTALLED_SCIENCE91_CANDIDATE',baseline=BASE,files=candidate,new_censuses=0))
 bindings=candidate+[pin(p)for folder in [A/'registration_review',checks]for p in sorted(folder.rglob('*'))if p.is_file()]
 common=dict(source_ids=['L091'],ordinary_recovery_credit=1,principal_refutation_credit=0,new_measurements=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None,all_source_assertions_reproved=False,utc=datetime.now(timezone.utc).isoformat(),distinct_registration_manifest=pin(A/'registration_review/manifest.json'),integration_preflight=pin(checks/'installed_preflight.json'),root_role='Root distinctly reviewed the concrete registration and executes final local adoption; prior mathematical and portable operational reviews are retained separately.',scope_note='Complete corrected L091 disposition with nineteen source interfaces, 27 manuscripts occupying 77 content pages and one divider in the 78-page volume. J3 global coverage remains an attributed premise. Nine refuted originals retain surviving-claim obligations; fourteen originals still require completion. No measurement, new question or Lean credit.',remaining='Final tracked manifest, commit and network publication. Other pending sources and valid obligations of refuted sources are unchanged.',bindings=bindings)
 save(A/'root_integration.json',dict(common,status='ROOT_ACCEPTED_SCIENCE91_L091_RECOVERY'))
 save(B/'root_integration.json',dict(common,status='ROOT_ACCEPTED_SOURCE_DISPOSITION',disposition_kind='ordinary_recovery'))
 print(json.dumps(dict(status='ROOT_SCIENCE91_PUBLICATION_GATES_INSTALLED',candidate_files=len(candidate),bindings=len(bindings),public_recovery_count=91)))
def manifest(a):
 need((A/'root_integration.json').exists(),'Final root gates required')
 spec=importlib.util.spec_from_file_location('snapshot',R/'scripts/verify_snapshot.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 rows=module.publication_rows();old=load(A/'manifest_history/predecessor_publication_manifest.json');new={**old,'files':rows};path=R/'provenance/publication_manifest.json'
 if a.write_manifest:
  need(not subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R).strip(),'Stage all intended new public files before manifest')
  path.write_text(json.dumps(new,indent=2)+'\n')
 need(load(path)==new,'Exact final tracked manifest and preserved metadata')
 print(json.dumps(dict(status='PASS_SCIENCE91_TRACKED_PUBLICATION_MANIFEST',tracked_artifacts=len(rows),canonical_lean_modules_acquired=len(old['canonical_lean_modules']),new_Lean=0,new_measurement=0,whole_historical_replay=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='command',required=True);g=sub.add_parser('gates');g.add_argument('--review',type=Path,required=True);g.add_argument('--review-sha',required=True);g.add_argument('--preflight-report',type=Path,required=True);m=sub.add_parser('manifest');m.add_argument('--write-manifest',action='store_true');a=ap.parse_args();gates(a)if a.command=='gates'else manifest(a)
