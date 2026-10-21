#!/usr/bin/env python3
"""Independent frozen F014 application bindings and fresh scoped replays."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR='75a07ebe73b2cfd31db5d2904130f41c47f344eb74cbd92d86cca9f18776621e'
def need(ok,msg):
 if not ok:raise RuntimeError('P232_REJECT '+msg)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def binding(row):
 rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe binding')
 p=ROOT/rel;need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'binding '+str(rel))
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--lean',type=Path)
 ap.add_argument('--packages',type=Path)
 ap.add_argument('--gap',default=shutil.which('gap'))
 ap.add_argument('--bindings-only',action='store_true')
 ap.add_argument('--verify-primary',action='store_true')
 a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output required')
 need(sha(ROOT/'phase229_manifest.json')==AUTHOR,'wrong author freeze')
 author=json.loads((ROOT/'phase229_manifest.json').read_text())
 for row in author['exports']:binding(row)
 for row in author['retained_bindings']:
  if not row['path'].startswith('sources/') or a.verify_primary:binding(row)
 review=json.loads((ROOT/'phase232_manifest.json').read_text())
 for row in review['exports']:binding(row)
 a.out.mkdir(parents=True);out=a.out.resolve()
 status={'status':'PASS_BINDINGS_ONLY','author_manifest_sha256':AUTHOR,'review_manifest_sha256':sha(ROOT/'phase232_manifest.json'),'author_exports_checked':len(author['exports']),'review_exports_checked':len(review['exports']),'private_primary_bindings_checked':a.verify_primary,'full_Lean_application_claimed':False,'new_question_credit':0,'ratio':None}
 if not a.bindings_only:
  need(a.lean is not None and a.packages is not None,'--lean and --packages required for fresh formal replay')
  need(a.gap is not None,'GAP unavailable')
  commands=[('lean',[sys.executable,'-B','-O',str(ROOT/'phase229_lean_check.py'),'--lean',str(a.lean),'--packages',str(a.packages),'--out',str(out/'lean')]),('author_model',[sys.executable,'-B','-O',str(ROOT/'phase229_model_check.py')]),('independent_gap',[a.gap,'-q','-b',str(ROOT/'phase232_polygon_permutations.g')])]
  results={}
  for label,cmd in commands:
   r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=180)
   (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
   need(r.returncode==0 and not r.stderr,label+' failure')
   results[label]=r.stdout
  formal=json.loads((out/'lean/report.json').read_text())
  need(formal['status']=='P229_FORMAL_REPLAY_PASS' and len(formal['declarations'])==5,'formal scope')
  need(json.loads(results['author_model'])==json.loads((ROOT/'phase229_model_report.json').read_text()),'author finite model differs')
  lines=results['independent_gap'].splitlines()
  for n in [3,4,5,6,7,8,11,13]:
   need(f'n={n} order={n*2**n} intersections=64 full_relators={n-1} duality=PASS' in lines,'independent model missing')
  for s in ['altered_translation_rejected=PASS','exceptional_n2_order8_IP64_duality=PASS','period_only_commutativity_weakening_refuted=PASS','PASS_INDEPENDENT_FINITE_DIAGNOSTICS_ONLY']:
   need(s in lines,'missing control '+s)
  need('Error' not in results['independent_gap'],'GAP error')
  status.update(status='PASS_FRESH_SCOPED_FORMAL_AND_INDEPENDENT_FINITE_REPLAY',fresh_Lean_seconds=formal['seconds'],selected_standard_axiom_reports=5,independent_GAP_models=8,exceptional_n2_checked=True,controls_passed=2,scope='The unbounded geometric/presentation proof is reviewed written mathematics. Lean formalizes only its five declared algebraic statements. Finite tests are diagnostics.')
 (out/'report.json').write_text(json.dumps(status,indent=2)+'\n');print(json.dumps(status,indent=2))
if __name__=='__main__':main()
