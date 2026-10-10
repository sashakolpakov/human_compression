#!/usr/bin/env python3
"""Independent review replay of the exact frozen PSL maniplex application."""
import argparse,hashlib,json,pathlib,re,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
AUTHOR_SHA='ccd07fd98645aa1ae31213b9c7d3f76501ca5225ae05992b64e7ac9dc80915cc'
def need(b,s):
 if not b:raise RuntimeError('PHASE263_REJECT '+s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for k in ['out','gap','lean','packages']:ap.add_argument('--'+k,type=pathlib.Path,required=True)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
 out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 need(sha(ROOT/'phase258_manifest.json')==AUTHOR_SHA,'exact frozen author manifest')
 start=time.monotonic();runs=[]
 def run(label,args):
  t=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=300)
  for suffix,data in [('stdout',p.stdout),('stderr',p.stderr)]:(out/(label+'.'+suffix)).write_text(data)
  runs.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-t,3),stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr'))));return p
 p=run('author',[sys.executable,'-B','-O',ROOT/'phase258_check.py','--out',out/'author','--gap',a.gap,'--lean',a.lean,'--packages',a.packages,'--verify-primary'])
 need(p.returncode==0,'full author replay')
 author=json.loads((out/'author/report.json').read_bytes())
 need(author['status']=='PASS' and author['primary_checked'] and author['source_rows']==32 and author['proof_spans']==9 and author['new_lean_declarations']==3,'author exact scope')
 p=run('independent_permutations',[sys.executable,'-B','-O',ROOT/'phase263_independent.py','--out',out/'independent.json'])
 need(p.returncode==0 and 'PHASE263_INDEPENDENT_PASS' in p.stdout,'independent 432 triples and literal witnesses')
 p=run('independent_fields',[a.gap,'-q','-T',ROOT/'phase263_field_checks.g'])
 need(p.returncode==0 and not re.search(r'Error|warning',p.stdout+p.stderr) and p.stdout.count('INDEPENDENT_PSL_FAMILY ')==4 and p.stdout.count('INDEPENDENT_NONPRIME_EXTENSION ')==2 and 'PHASE263_FIELD_PASS' in p.stdout,'six independent field models')
 p=run('independent_witness_control',[sys.executable,'-B','-O',ROOT/'phase263_independent.py','--out',out/'rejected.json','--mutate-witness'])
 need(p.returncode!=0 and 'PHASE263_REJECT actual distant commutations' in p.stderr and not (out/'rejected.json').exists(),'corrupted source witness rejected')
 report=dict(status='PASS',seconds=round(time.monotonic()-start,3),author_manifest_sha256=AUTHOR_SHA,executions=runs,
  independent_local_markings=432,independent_all_subset_intersections=27648,independent_literal_witnesses=2,
  independent_prime_families={'A5':[59,61],'S4':[71,97]},independent_nonprime_fields=[25,49],independent_mutation_rejected=True,
  new_lean=3,reused_lean=2,retained_universal_rows=10,source_rows=32,proof_spans=9,
  scope='One corrected principal PSL contract accepted only together with the complete written/source review; no whole-paper, question, priority, full-Lean or compression-ratio credit.')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
