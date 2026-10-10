#!/usr/bin/env python3
"""Public replay of the four-family certificates; primary PDFs are not required."""
import argparse, hashlib, json, pathlib, re, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent
PINS={'phase257_manifest.json':'e27a461990413f41af0799efa7f41f965ec534691251fe1fe8e12ca5b80ba67b','phase261_manifest.json':'cdf5af42ce35f767fcf6cbe6471e4bca83e8caa6379c9ddf10e0b1f631caa7af'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise RuntimeError('PHASE262_REJECT '+msg)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for x in ['out','gap','lean','packages']:ap.add_argument('--'+x,type=pathlib.Path,required=True)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
 out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 checked=0
 for name,pin in PINS.items():
  need(sha(ROOT/name)==pin,'frozen manifest '+name);manifest=json.loads((ROOT/name).read_bytes())
  for row in manifest['exports']+manifest['retained_bindings']:
   rel=pathlib.PurePosixPath(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative path')
   if row['path'].startswith('sources/'):continue
   p=ROOT/rel;need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'frozen artifact '+str(rel));checked+=1
 start=time.monotonic();runs=[]
 def run(label,command):
  t=time.monotonic();p=subprocess.run([str(x) for x in command],cwd=out,capture_output=True,text=True,timeout=240)
  stdout=out/(label+'.stdout');stderr=out/(label+'.stderr');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
  runs.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-t,3),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)));return p
 p=run('author',[sys.executable,'-B','-O',ROOT/'phase257_check.py','--out',out/'author','--gap',a.gap,'--lean',a.lean,'--packages',a.packages])
 need(p.returncode==0,'author public replay');author=json.loads((out/'author/report.json').read_bytes())
 need(author['status']=='PASS' and not author['primary_checked'] and len(author['axiom_reports'])==11,'author formal boundary')
 source=ROOT/'phase261_independent_families.g';p=run('independent',[a.gap,'-q','-T',source])
 need(p.returncode==0 and not re.search(r'Error|warning',p.stdout+p.stderr) and 'PHASE261_INDEPENDENT_FAMILIES_PASS' in p.stdout,'independent construction')
 need(p.stdout.count('P261_FAMILY ')==17 and p.stdout.count('P261_EXCLUDED_CONTROL ')==3,'independent sample and control counts')
 need(all(x in p.stdout for x in ['P261_LOCAL_S4_CASES48_PASS','P261_COXETER [3,3,3] ORDER 120 PASS','P261_COXETER [3,3,4] ORDER 384 PASS']),'full small local computations')
 s=source.read_text();bad=s.replace('[[1,-2],[2,-1]]','[[1,-1],[2,-1]]');need(s!=bad,'independent matrix mutation')
 target=out/'bad_independent_matrix.g';target.write_text(bad);p=run('control_independent',[a.gap,'-q','-T',target])
 need(p.returncode!=0 and 'PHASE261_REJECT commuting distinct distant generators' in p.stdout,'independent false matrix rejected')
 report=dict(status='PASS',seconds=round(time.monotonic()-start,3),frozen_public_bindings_checked=checked,primary_full_texts_distributed=False,
  author_samples=16,independent_samples=17,independent_S4_cases=48,Coxeter_orders=[120,384],excluded_parameters=3,semantic_mutations=4,
  lean_declarations=11,executions=runs,scope='Public finite and partial formal replay; full written proof reviewed separately; no priority claim.')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
