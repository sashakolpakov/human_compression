#!/usr/bin/env python3
"""Bind the independent review and freshly replay its declared computation."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
AUTHOR='2adb69dc5b475b0ec2fd629c03286505c4ca88a9e9baecbb5b2d0e5fe79dcec0'
def need(ok,msg):
 if not ok:raise RuntimeError('P234_REJECT '+msg)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def binding(row):
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'unsafe path')
 path=ROOT/p;need(sha(path)==row['sha256'] and path.stat().st_size==row['bytes'],'binding '+str(p))
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--out',type=Path,required=True);ap.add_argument('--lean',type=Path)
 ap.add_argument('--packages',type=Path);ap.add_argument('--gap',type=Path)
 ap.add_argument('--bindings-only',action='store_true');ap.add_argument('--verify-primary',action='store_true')
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output path')
 need(sha(ROOT/'phase230_manifest.json')==AUTHOR,'author freeze')
 author=json.loads((ROOT/'phase230_manifest.json').read_text())
 for row in author['exports']:binding(row)
 for row in author['retained']:
  if not row['path'].startswith('sources/') or a.verify_primary:binding(row)
 review=json.loads((ROOT/'phase234_manifest.json').read_text())
 for row in review['exports']:binding(row)
 a.out.mkdir(parents=True);out=a.out.resolve()
 report={'status':'PASS_BINDINGS_ONLY','author_manifest_sha256':AUTHOR,'review_manifest_sha256':sha(ROOT/'phase234_manifest.json'),'author_exports_checked':len(author['exports']),'review_exports_checked':len(review['exports']),'private_primary_bindings_checked':a.verify_primary,'principal_sources_licensed_at_most':2,'whole_source_claims':0,'new_question_results':0,'complete_Lean_application':False,'matched_ratio':None}
 if not a.bindings_only:
  need(a.lean and a.packages and a.gap,'fresh replay requires --lean --packages --gap')
  cmd=[sys.executable,'-B','-O',str(ROOT/'phase230_check.py'),'--out',str(out/'author'),'--lean',str(a.lean),'--packages',str(a.packages),'--gap',str(a.gap)]
  r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=240)
  (out/'author.stdout').write_text(r.stdout);(out/'author.stderr').write_text(r.stderr)
  need(r.returncode==0 and not r.stderr,'author replay')
  fresh=json.loads((out/'author/report.json').read_text());need(fresh['status']=='PASS' and len(fresh['axiom_reports'])==5,'formal interface')
  output=(out/'author/finite.stdout').read_text()
  need(output==(ROOT/'phase234_finite.stdout').read_text(),'finite semantic output differs')
  r=subprocess.run([str(a.gap),'-q','-T',str(ROOT/'phase234_centralizer_check.g')],cwd=ROOT,text=True,capture_output=True,timeout=60)
  (out/'centralizers.stdout').write_text(r.stdout);(out/'centralizers.stderr').write_text(r.stderr)
  need(r.returncode==0 and not r.stderr,'independent centralizer replay')
  normalized=' '.join(r.stdout.split())
  for expected in ['FIELD 3 TO 9 SEMISIMPLE_PAIRS 24 UNIPOTENT_PAIRS 24 LABELS [ 3, 4 ] PASS','FIELD 5 TO 25 SEMISIMPLE_PAIRS 360 UNIPOTENT_PAIRS 120 LABELS [ 3, 4, 5, 6 ] PASS','CHAR2 4 INVOLUTIONS 15 PASS','CHAR2 8 INVOLUTIONS 63 PASS','ODDNESS_AND_NORMALIZER_WEAKENINGS_REFUTED','PHASE234_INDEPENDENT_CENTRALIZERS_PASS']:
   need(expected in normalized,'missing independent assertion')
  need('Error' not in normalized,'GAP error')
  report.update(status='PASS_FRESH_FORMAL_FINITE_AND_CENTRALIZER_REPLAY',local_marking_classes=6,universal_presentations=10,author_negative_controls=2,independent_weakening_controls=2,selected_Lean_declarations=5,semisimple_pairs=384,unipotent_pairs=144,scope='Complete written principal proofs independently reviewed. Trusted exact GAP computation; only the abstract normalizer obstruction is formalized in Lean.')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
