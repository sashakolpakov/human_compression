#!/usr/bin/env python3
"""Public replay of the reviewed PSL maniplex application; no primary PDFs needed."""
import argparse,hashlib,json,pathlib,re,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
AUTHOR_SHA='ccd07fd98645aa1ae31213b9c7d3f76501ca5225ae05992b64e7ac9dc80915cc'
REVIEW_SHA='552ee266a09152e1cc51d5239c6c0cbe19c43c305ff0a776417f7b7f6167d0f5'
def need(b,s):
 if not b:raise RuntimeError('PHASE264_REJECT '+s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for k in ['out','gap','lean','packages']:ap.add_argument('--'+k,type=pathlib.Path,required=True)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
 out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 checked=0
 for name,pin in [('phase258_manifest.json',AUTHOR_SHA),('phase263_manifest.json',REVIEW_SHA)]:
  need(sha(ROOT/name)==pin,'exact frozen manifest '+name);m=json.loads((ROOT/name).read_bytes())
  for row in m['exports']+m['retained_bindings']:
   rel=pathlib.PurePosixPath(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative binding')
   if row['path'].startswith('sources/'):continue
   path=ROOT/rel;need(path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'frozen bytes '+str(rel));checked+=1
 need((ROOT/'formal/StringCentralizerBridge.lean').read_bytes()==(ROOT/'phase258_formal/StringCentralizerBridge.lean').read_bytes(),'canonical source equals compiled source')
 start=time.monotonic();runs=[]
 def run(label,args):
  t=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=ROOT,text=True,capture_output=True,timeout=300)
  for suffix,data in [('stdout',p.stdout),('stderr',p.stderr)]:(out/(label+'.'+suffix)).write_text(data)
  runs.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-t,3),stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr'))));return p
 p=run('author',[sys.executable,'-B','-O',ROOT/'phase258_check.py','--out',out/'author','--gap',a.gap,'--lean',a.lean,'--packages',a.packages])
 need(p.returncode==0,'full author replay')
 author=json.loads((out/'author/report.json').read_bytes())
 need(author['status']=='PASS' and not author['primary_checked'] and author['source_rows']==32 and author['proof_spans']==9 and author['new_lean_declarations']==3,'author exact scope')
 p=run('independent_permutations',[sys.executable,'-B','-O',ROOT/'phase263_independent.py','--out',out/'independent.json'])
 need(p.returncode==0 and 'PHASE263_INDEPENDENT_PASS' in p.stdout,'independent 432 triples and literal witnesses')
 p=run('independent_fields',[a.gap,'-q','-T',ROOT/'phase263_field_checks.g'])
 need(p.returncode==0 and not re.search(r'Error|warning',p.stdout+p.stderr) and p.stdout.count('INDEPENDENT_PSL_FAMILY ')==4 and p.stdout.count('INDEPENDENT_NONPRIME_EXTENSION ')==2 and 'PHASE263_FIELD_PASS' in p.stdout,'six independent field models')
 p=run('independent_witness_control',[sys.executable,'-B','-O',ROOT/'phase263_independent.py','--out',out/'rejected.json','--mutate-witness'])
 need(p.returncode!=0 and 'PHASE263_REJECT actual distant commutations' in p.stderr and not (out/'rejected.json').exists(),'corrupted source witness rejected')
 report=dict(status='PASS',seconds=round(time.monotonic()-start,3),author_manifest_sha256=AUTHOR_SHA,review_manifest_sha256=REVIEW_SHA,frozen_public_bindings_checked=checked,primary_full_texts_distributed=False,executions=runs,
  independent_local_markings=432,independent_all_subset_intersections=27648,independent_literal_witnesses=2,
  independent_prime_families={'A5':[59,61],'S4':[71,97]},independent_nonprime_fields=[25,49],independent_mutation_rejected=True,
  new_lean=3,reused_lean=2,retained_universal_rows=10,source_rows=32,proof_spans=9,
  scope='Public finite and partial formal replay of the reviewed PSL principal contract; full written proof reviewed separately; no whole-paper, question, priority, full-Lean or compression-ratio claim.')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
