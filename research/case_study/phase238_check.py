#!/usr/bin/env python3
"""Bind three complete papers and replay their one shared exact dependency."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OLD='2adb69dc5b475b0ec2fd629c03286505c4ca88a9e9baecbb5b2d0e5fe79dcec0'
def need(ok,msg):
 if not ok:raise RuntimeError('P238_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(r):
 p=Path(r['path']);need(not p.is_absolute() and '..' not in p.parts,'unsafe path')
 q=ROOT/p;need(q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],'binding '+str(p))
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True)
 for s in ['gap','lean','packages']:ap.add_argument('--'+s,type=Path)
 ap.add_argument('--bindings-only',action='store_true');ap.add_argument('--verify-primary',action='store_true');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output path')
 freeze=json.loads((ROOT/'phase238_manifest.json').read_text())
 for r in freeze['exports']+freeze['retained']:
  if not r['path'].startswith('sources/') or a.verify_primary:binding(r)
 need(sha(ROOT/'phase230_manifest.json')==OLD,'old freeze')
 old=json.loads((ROOT/'phase230_manifest.json').read_text())
 for r in old['exports']:binding(r)
 for r in old['retained']:
  if not r['path'].startswith('sources/') or a.verify_primary:binding(r)
 r=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase238_build_umbrella.py'),'--check'],text=True,capture_output=True)
 need(r.returncode==0 and 'PHASE238_COMMON_BUILD_PASS' in r.stdout,'common proof provenance')
 ledger=json.loads((ROOT/'phase238_contract.json').read_text());need(len(ledger['rows'])==22,'all source clauses')
 need(ledger['additional_principal_source_credit']==0 and ledger['new_question_solutions']==0,'no duplicated credits')
 graph=json.loads((ROOT/'phase238_dependency.json').read_text())
 for node in graph['nodes']:
  if 'sha256' in node:binding(node)
 if a.verify_primary:
  for span in json.loads((ROOT/'phase238_source_boundaries.json').read_text())['spans']:
   p=ROOT/span['text_path'];need(sha(p)==span['text_sha256'],'source extraction')
   text=p.read_text()[span['character_start']:span['character_end']]
   need(hashlib.sha256(text.encode()).hexdigest()==span['span_sha256'],'source span')
 a.out.mkdir(parents=True);out=a.out.resolve()
 report={'status':'PASS_BINDINGS_ONLY','new_exports':len(freeze['exports']),'source_clauses':22,'complete_papers':3,'additional_sources':0,'new_questions':0,'ratio':None,'primary_checked':a.verify_primary}
 if not a.bindings_only:
  need(a.gap and a.lean and a.packages,'executables/packages required')
  cmd=[sys.executable,'-B','-O',str(ROOT/'phase230_check.py'),'--out',str(out/'shared'),'--gap',str(a.gap),'--lean',str(a.lean),'--packages',str(a.packages)]
  r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=240)
  (out/'shared.stdout').write_text(r.stdout);(out/'shared.stderr').write_text(r.stderr)
  need(r.returncode==0 and not r.stderr,'shared exact replay')
  result=json.loads((out/'shared/report.json').read_text());need(result['status']=='PASS' and len(result['axiom_reports'])==5,'formal boundary')
  report.update(status='PASS_FRESH_SHARED_PROOF_REPLAY',local_classes=6,universal_presentations=10,inherited_Lean_declarations=5,rejected_controls=2)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
