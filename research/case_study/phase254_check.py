#!/usr/bin/env python3
"""Replay the independent L012 review, including the frozen author interface."""
import argparse,hashlib,json,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
AUTHOR_SHA='27f605517f1fec35aef62ec181229d5ed2b8f73aeda09f5cd0ccd9a1af44c62e'
def need(ok,msg):
 if not ok:raise RuntimeError('PHASE254_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for flag in ['out','gap','lean','packages']:ap.add_argument('--'+flag,type=pathlib.Path,required=True)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
 out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 need(sha(ROOT/'phase250_manifest.json')==AUTHOR_SHA,'frozen author manifest')
 start=time.monotonic();executions=[]
 def run(label,args):
  before=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=300)
  (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
  executions.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-before,3),stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr'))))
  need(p.returncode==0,label);return p
 p=run('author',[sys.executable,'-B','-O',ROOT/'phase250_check.py','--out',out/'author','--gap',a.gap,'--lean',a.lean,'--packages',a.packages,'--verify-primary'])
 author=json.loads((out/'author/report.json').read_bytes());need(author['status']=='PASS' and author['primary_checked'],'complete frozen author replay')
 p=run('independent_affine',[sys.executable,'-B','-O',ROOT/'phase254_independent_affine.py','--out',out/'independent_affine.json'])
 affine=json.loads((out/'independent_affine.json').read_bytes());need(affine['status']=='PASS' and len(affine['models'])==18 and affine['bad_period']['intersection_failures'],'18 models and bad-period rejection')
 p=run('independent_presentations',[a.gap,'-q','-T',ROOT/'phase254_source_presentations.g'])
 need(p.stdout.count('IP64 deletions8 PASS')==6 and 'PHASE254_PRESENTATIONS_PASS' in p.stdout and 'Error' not in p.stdout+p.stderr,'six independently transcribed source presentations')
 report=dict(status='PASS',author_manifest_sha256=AUTHOR_SHA,seconds=round(time.monotonic()-start,3),executions=executions,
  source_rows=33,proof_spans=14,author_exports=author['exports_checked'],author_retained_bindings=author['retained_bindings_checked'],
  independent_affine_models=18,independent_literal_presentations=6,lean_declarations=len(author['axiom_reports']),
  scope='Independent finite evidence and full frozen replay; complete principal admission additionally requires the written/source review in phase254_review.md.',
  controls=['independent raw-Schreier counterexample','independent quotient destroying IP','all frozen author controls'],
  trust=['Burnside and Lucchini retained','SmallGroups1.5.4 complete catalogue retained','exact GAP algorithms retained','Lean covers three sign identities only'])
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
