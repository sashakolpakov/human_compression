#!/usr/bin/env python3
"""Replay the exact pyramid, quotient, surface and retained Lean group lemmas."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
REVISION='905b95818eb32af7874a58b427f50c1711a5e96c'
COPRIME_SHA='4eb20ee7eb85943eab4100b565146a8cd938e4f3c2055b66c6fbbdfa3f68987c'
CHAINS_SHA='64cdb792746b651ec755af4f61b9548470fb0812f1f479b5f4eaceac4b99d572'
def require(ok,label):
 if not ok:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--lean',default='/Users/sasha/.elan/bin/lean');ap.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));args=ap.parse_args()
 require(not args.out.exists() and not args.out.is_symlink(),'fresh output directory required');out=args.out.resolve();out.mkdir(parents=True);start=time.monotonic()
 require(sha(ROOT/'phase211_surface_check.py')=='728eaceef1048ad8a266b51dcabf217266f07c554474e85fede41f0a5b69e71b','frozen surface program')
 require(sha(ROOT/'formal/CoprimePullback.lean')==COPRIME_SHA,'frozen126 theorem source')
 require(sha(ROOT/'formal/CoverKernelChains.lean')==CHAINS_SHA,'frozen211 theorem source')
 for name in ['phase224_pyramid_flags.py','phase224_pyramid_groups.g','phase211_surface_check.py','formal/CoprimePullback.lean','formal/CoverKernelChains.lean']:
  target=out/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
 import phase224_pyramid_flags as flags
 import phase211_surface_check as surfaces
 allflags=flags.build_flags(3);model,flag_report=flags.analyze_flags(allflags)
 require(model['degree']==360,'source flag count');(out/'pyramid_model.json').write_text(json.dumps(model,indent=2)+'\n');(out/'pyramid_flags.g').write_text(flags.gap_input(model))
 try:flags.analyze_flags(allflags[:-1])
 except ValueError as e:flag_control=str(e)
 else:raise RuntimeError('missing flag control accepted')
 require(flag_control=='unique flag adjacency','wrong missing-flag rejection')
 proc=subprocess.run([args.gap,'-q','phase224_pyramid_groups.g'],cwd=out,text=True,capture_output=True,timeout=180)
 (out/'groups.log').write_text(proc.stdout+proc.stderr);require(proc.returncode==0 and 'Error' not in proc.stdout+proc.stderr,'exact group replay failed')
 group_report=json.loads(proc.stdout[proc.stdout.index('{'):]);require(group_report['status']=='PASS','group status')
 D={'name':'Pyramid_torus3_D3840','degree':10,'generators':[[3,4,1,2,5,6,7,8,9,10],[1,2,5,6,3,4,8,7,10,9],[1,2,3,4,7,8,5,6,10,9],[2,1,4,3,6,5,9,10,7,8]]}
 require(group_report['D_generators']==D['generators'],'exact quotient marks shared by GAP and surface witness')
 cells=surfaces.analyze(D,True)
 require(cells['cells']==[3840,7680,3200] and cells['middle_order']==6 and cells['orientable'],'quotient surface parameters')
 require(cells['Euler_characteristic']==-640 and cells['H1_dimension_odd']==cells['H1_dimension_two']==642,'uniform homology dimension')
 require([len(x['complement_components']) for x in cells['pairs']]==[1,1,1],'three actual complement components')
 require([x['complement_components'][0]['size'] for x in cells['pairs']]==[2704,3199,3199],'complement face counts')
 require(cells['all_odd_prime_criterion'] and cells['prime_two_criterion'],'surface theorem hypotheses')
 (out/'surface_certificate.json').write_text(json.dumps(cells,indent=2)+'\n');(out/'quotient_model.json').write_text(json.dumps(D,indent=2)+'\n')
 env=os.environ.copy();env['ELAN_TOOLCHAIN']='leanprover/lean4:v4.32.2';env['LEAN_PATH']=':'.join([str(out)]+[str(args.packages/p/'.lake/build/lib/lean') for p in ['mathlib','plausible','proofwidgets','batteries','aesop','importGraph','LeanSearchClient','Qq']])
 revision=subprocess.run(['git','-C',str(args.packages/'mathlib'),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip();require(revision==REVISION,'pinned mathlib revision')
 lean_reports={}
 for name,count in [('CoprimePullback',3),('CoverKernelChains',6)]:
  src=out/'formal'/f'{name}.lean';require(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',src.read_text(),re.M),'untrusted Lean source')
  proc=subprocess.run([args.lean,'-o',str(out/f'{name}.olean'),str(src)],cwd=out,env=env,text=True,capture_output=True,timeout=180);log=proc.stdout+proc.stderr;(out/f'{name}.log').write_text(log)
  require(proc.returncode==0 and 'sorryAx' not in log and log.count('depends on axioms:')==count,'retained Lean replay')
  for a in re.findall(r'depends on axioms:\s*\[([^]]*)\]',log,re.S):require(set(x.strip() for x in a.split(','))<={'propext','Classical.choice','Quot.sound'},'unexpected Lean axiom')
  lean_reports[name]={'theorems':count,'source_sha256':sha(src),'axioms':['propext','Classical.choice','Quot.sound']}
 report={'status':'PASS','seconds':round(time.monotonic()-start,3),'flags':flag_report,'groups':group_report,'surface':{k:cells[k] for k in ['order','cells','middle_order','orientable','Euler_characteristic','H1_dimension_odd']},'Lean':lean_reports,'controls':{'missing_flag':flag_control,'larger_quotient_kernel':'rejected because its top intersection has order4 and its middle intersection order2'},'scope':'Exact single-polytope construction and finite group/surface witnesses. Written211 surface theorem gives all primes; written coprime argument gives the original pyramid covers for every prime>=5. Lean checks reused general fiber-product and admissible-kernel lemmas, not the particular geometry or GAP computation. No general finite minimal-cover theorem is asserted.','artifacts':{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.suffix!='.olean'}}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
