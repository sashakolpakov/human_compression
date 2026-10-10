#!/usr/bin/env python3
"""Independent four-family review replay; written review remains indispensable."""
import argparse,hashlib,json,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
AUTHOR_SHA='e27a461990413f41af0799efa7f41f965ec534691251fe1fe8e12ca5b80ba67b'
def need(ok,msg):
 if not ok:raise RuntimeError('PHASE261_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for x in ['out','gap','lean','packages']:ap.add_argument('--'+x,type=pathlib.Path,required=True)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
 out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 need(sha(ROOT/'phase257_manifest.json')==AUTHOR_SHA,'exact frozen author manifest')
 runs=[];start=time.monotonic()
 def run(label,args):
  t=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=300)
  (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
  runs.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-t,3),stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr'))));return p
 p=run('author',[sys.executable,'-B','-O',ROOT/'phase257_check.py','--out',out/'author','--gap',a.gap,'--lean',a.lean,'--packages',a.packages,'--verify-primary'])
 need(p.returncode==0,'full frozen author replay')
 author=json.loads((out/'author/report.json').read_bytes());need(author['status']=='PASS' and author['primary_checked'] and len(author['axiom_reports'])==11,'author scope')
 source=ROOT/'phase261_independent_families.g';p=run('independent_native',[a.gap,'-q','-T',source])
 need(p.returncode==0 and p.stdout.count('P261_FAMILY ')==17 and p.stdout.count('P261_EXCLUDED_CONTROL ')==3 and 'PHASE261_INDEPENDENT_FAMILIES_PASS' in p.stdout,'17 native models and excluded parameters')
 need('P261_LOCAL_S4_CASES48_PASS' in p.stdout and 'P261_COXETER [3,3,3] ORDER 120 PASS' in p.stdout and 'P261_COXETER [3,3,4] ORDER 384 PASS' in p.stdout,'complete small local and literal Coxeter checks')
 text=source.read_text();bad=text.replace('[[1,-2],[2,-1]]','[[1,-1],[2,-1]]');need(bad!=text,'independent matrix mutation')
 target=out/'bad_matrix.g';target.write_text(bad);p=run('independent_matrix_control',[a.gap,'-q','-T',target])
 need(p.returncode!=0 and 'PHASE261_REJECT commuting distinct distant generators' in p.stdout,'incorrect actual distant commutation rejected')
 report=dict(status='PASS',seconds=round(time.monotonic()-start,3),author_manifest_sha256=AUTHOR_SHA,
  author_samples=16,independent_samples=17,independent_S4_cases=48,literal_Coxeter_orders=[120,384],
  excluded_parameter_controls=3,independent_matrix_control=True,lean_declarations=11,executions=runs,
  scope='One complete answer to the bound four-family conjecture, conditional on the accompanying full written/source review; no full Lean or historical-priority claim.')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
