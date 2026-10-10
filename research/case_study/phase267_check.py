#!/usr/bin/env python3
"""Replay the complete primitive-square review in isolated writable copies."""
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
AUTHOR_SHA='7c92dee573d004c7d91783fd135f94819eab66e49d8834987089acb06039bbb5'
def need(b,s):
 if not b:raise RuntimeError('PHASE267_REJECT '+s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(row):
 rel=pathlib.PurePosixPath(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative binding')
 p=ROOT/rel;need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'bound input '+str(rel))
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for k in ['out','gap','lean','packages']:ap.add_argument('--'+k,type=pathlib.Path,required=True)
 ap.add_argument('--verify-primary',action='store_true');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output');out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 need(sha(ROOT/'phase266_manifest.json')==AUTHOR_SHA,'frozen formal author manifest');m=json.loads((ROOT/'phase266_manifest.json').read_bytes())
 for row in m['exports']+m['retained_bindings']:bound(row)
 inputs=json.loads((ROOT/'phase267_inputs.json').read_bytes())['files']
 for row in inputs:
  if a.verify_primary or not row['path'].startswith('sources/'):bound(row)
 before={r['path']:sha(ROOT/r['path']) for r in inputs if not r['path'].startswith('sources/')}
 work=out/'old/research/leemans';work.mkdir(parents=True)
 for name in before:
  if pathlib.Path(name).suffix in ['.py','.g','.json']:shutil.copyfile(ROOT/name,work/name)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 runs=[];start=time.monotonic()
 def run(label,args,cwd=out):
  t=time.monotonic();p=subprocess.run([str(x) for x in args],cwd=cwd,env=env,text=True,capture_output=True,timeout=300)
  for ext,v in [('stdout',p.stdout),('stderr',p.stderr)]:(out/(label+'.'+ext)).write_text(v)
  runs.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-t,3),stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr'))));return p
 p=run('assertion_mode',[sys.executable,'-B','-c','import sys; print(sys.flags.optimize)']);need(p.returncode==0 and p.stdout.strip()=='0','assertions enabled in old child processes')
 p=run('old_integer',[sys.executable,'-B',work/'psl2_square_bound_check.py']);need(p.returncode==0 and 'ALL_EXACT_INTEGER_CHECKS_PASSED' in p.stdout and 'NONNESTED_TESTED 66' in p.stdout and 'NESTED_FIELDS_TESTED 23' in p.stdout,'old complete integer reduction')
 p=run('old_witnesses',[sys.executable,'-B',work/'verify_square_witnesses.py']);need(p.returncode==0,'old witness verifier');w=json.loads((work/'psl2_square_witnesses_independent.json').read_bytes());need(w['all_passed'] and len(w['results'])==11,'all eleven exact witnesses')
 for label,name,cases in [('old_gap_nonnested','psl2_square_witnesses.g',6),('old_gap_nested','psl2_nested_witnesses.g',5)]:
  p=run(label,[a.gap,'-q','-T',work/name],out/'old');need(p.returncode==0 and p.stdout.count('CASE p=')==cases and p.stdout.count('PASS\n')==cases and not re.search(r'Error|warning',p.stdout+p.stderr),'exact GAP witness reconstruction '+label)
 p=run('independent_integer',[sys.executable,'-B','-O',ROOT/'phase267_independent_arithmetic.py','--out',out/'independent_arithmetic.json']);need(p.returncode==0 and 'PHASE267_ARITHMETIC_PASS 66 23 3354' in p.stdout,'independent arithmetic scope')
 p=run('independent_fields',[a.gap,'-q','-T',ROOT/'phase267_field_checks.g']);need(p.returncode==0 and 'PHASE267_FIELD_PASS' in p.stdout and p.stdout.count('DIRECT_EQUAL_FIELD ')==5 and p.stdout.count('DIRECT_NORM ')==4 and not re.search(r'Error|warning',p.stdout+p.stderr),'direct pair and norm checks')
 data=json.loads((ROOT/'psl2_square_witnesses.json').read_text())
 for control in ['norm_coefficient','nonprimitive','missing_case']:
  target=out/('bad_'+control);target.mkdir();shutil.copyfile(ROOT/'verify_square_witnesses.py',target/'verify_square_witnesses.py');bad=json.loads(json.dumps(data))
  if control=='norm_coefficient':bad[0]['normpoly'][0]=(bad[0]['normpoly'][0]+1)%bad[0]['p']
  elif control=='nonprimitive':next(r for r in bad if r['kind']=='nested')['j2_exponent']=2
  else:bad.pop(0)
  (target/'psl2_square_witnesses.json').write_text(json.dumps(bad));p=run('control_'+control,[sys.executable,'-B',target/'verify_square_witnesses.py'])
  need(p.returncode!=0 and 'AssertionError' in p.stderr and not (target/'psl2_square_witnesses_independent.json').exists(),'corrupted old witness rejected '+control)
 bad=(ROOT/'psl2_square_bound_check.py').read_text().replace('w = 2 ** len(fs)','w = 1');need(bad!=(ROOT/'psl2_square_bound_check.py').read_text(),'W mutation applied')
 target=out/'bad_bound.py';target.write_text(bad);p=run('control_bound',[sys.executable,'-B',target]);need(p.returncode!=0 and 'AssertionError' in p.stderr and 'ALL_EXACT_INTEGER_CHECKS_PASSED' not in p.stdout,'underestimated divisor weight rejected')
 p=run('formal',[sys.executable,'-B','-O',ROOT/'phase266_check.py','--out',out/'formal','--lean',a.lean,'--packages',a.packages]);need(p.returncode==0,'six formal declarations')
 formal=json.loads((out/'formal/report.json').read_bytes());need(formal['status']=='PASS' and len(formal['axiom_reports'])==6,'exact formal scope')
 need(all(sha(ROOT/n)==h for n,h in before.items()),'frozen old mathematical inputs unchanged')
 report=dict(status='PASS',seconds=round(time.monotonic()-start,3),author_manifest_sha256=AUTHOR_SHA,primary_checked=a.verify_primary,
             nonnested_reduction_cases=66,nested_reduction_fields=23,witnesses=11,independent_equal_field_pairs=214132,direct_norm_cases=4,
             independent_algebra_pairs=3354,corrupted_certificate_controls=4,formal_declarations=6,formal_hypothesis_controls=4,
             assert_enabled_old_replay=True,frozen_inputs_unchanged=True,executions=runs,
             scope='Complete independent written arithmetic review plus exact finite and six limited algebraic Lean checks; no new question, source or historical-priority credit; full conjecture not entirely formalized.')
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
