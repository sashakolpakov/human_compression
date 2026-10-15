import sys
if sys.flags.optimize: raise SystemExit('optimized execution unsupported')
sys.dont_write_bytecode=True
import argparse,hashlib,json,os,pathlib,re,shutil,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def pincheck(row,base):
 p=base/row['path'];b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'damaged '+str(p))
def run(cmd,out,seconds=60):
 out.mkdir(parents=True,exist_ok=False);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';start=time.monotonic()
 with (out/'stdout').open('wb') as so,(out/'stderr').open('wb') as se:
  try:r=subprocess.run(cmd,stdout=so,stderr=se,env=env,timeout=seconds)
  except subprocess.TimeoutExpired:
   (out/'receipt.json').write_text(json.dumps({'status':'TIMEOUT_NO_CERTIFICATE','seconds':time.monotonic()-start}));raise
 text=(out/'stdout').read_text();err=(out/'stderr').read_text();need(r.returncode==0 and not err.strip() and not any(w in text for w in ['Error,','Error:','Syntax warning']),'unclean child '+str(out))
 (out/'receipt.json').write_text(json.dumps({'status':'PASS','returncode':r.returncode,'seconds':time.monotonic()-start,'command':cmd},indent=2)+'\n');return text

def interfaces(study):
 path=pathlib.Path('/opt/homebrew/Cellar/gap/4.15.1/lib/gap/pkg/lins/gap/findPQuotients.gi');s=path.read_text();i=s.index('InstallGlobalFunction(LINS_FindPModules, function');j=s.index('\nend);',i)+len('\nend);');s=s[i:j]
 s=s.replace('InstallGlobalFunction(LINS_FindPModules, function','MakeReadWriteGlobal("LINS_FindPModules");;\nLINS_FindPModules := function',1);s=s[:-len('\nend);')]+'\nend;;\nMakeReadOnlyGlobal("LINS_FindPModules");;\n'
 s=s.replace('    Iso,    #','    Nu,     # composed H -> elementary abelian quotient\n    Iso,    #',1).replace('    gens := [];','    Nu := Iso * Mu;\n    gens := [];',1).replace('word := Image(Mu, Image(Iso, x * y * x ^ (-1) ));','word := Image(Nu, x * y * x ^ (-1));')
 need(s==(ROOT/'composed_pmodules.g').read_text(),'unexpected executable module delta')
 control='ComposedImageChecks:=0;;\n'+s;control=control.replace('word := Image(Nu, x * y * x ^ (-1));','word := Image(Nu, x * y * x ^ (-1));\n            if word<>Image(Mu,Image(Iso,x*y*x^(-1))) then Error("composition differs");fi;\n            ComposedImageChecks:=ComposedImageChecks+1;')
 need(control==(ROOT/'composed_control.g').read_text(),'wrong comparison helper')
 old=(study/'corpus106_L033_hyperbolic_core_v1/enumerate_broad.g').read_text()
 need((ROOT/'enumerate_changed.g').read_text()==old.replace('gr:=LowIndexNormalSubgroupsSearchForAll(G,bound);','gr:=LowIndexNormalSubgroupsSearch(G,bound,CoxeterSeedOptions(M));'),'unexpected caller delta')
 return 3

def main():
 p=argparse.ArgumentParser();p.add_argument('--study',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
 m=json.loads((ROOT/'manifest.json').read_text());deps=json.loads((ROOT/'dependencies.json').read_text())
 for row in m['exports']:pincheck(row,ROOT)
 for row in deps:pincheck(row,a.study if row['namespace']=='study' else pathlib.Path('/'))
 deltas=interfaces(a.study);a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
 driver=a.out/'driver.g';driver.write_text('LoadPackage("LINS");;\n'+''.join('Read('+json.dumps(str(ROOT/f))+');;\n' for f in ['coxeter_seeds.g','compare_markings.g'])+'ComposedImageChecks:=0;;\nRead('+json.dumps(str(ROOT/'controls.g'))+');;\nMethodControls('+json.dumps(str(ROOT))+');;\nQUIT;\n')
 text=run(['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(driver)],a.out/'controls',60)
 need(re.search(r'COMPLETE_METHOD_CONTROLS\s+18\s+SEED_CASES\s+7\s+INNER_ORBITS\s+3\s+KERNEL_CONTROLS\s+676\s+IMAGE_CHECKS',text),'missing complete controls')
 need(len(re.findall('NORMAL_KERNEL_CONTROL',text))==3,'missing kernel control')
 bads=[('F:=FreeGroup(2);;CoxeterTargetEpis(F,Group(()),[[1,3],[3,1]]);;','source relators differ'),('CoxeterTargetEpis(FreeGroup(2),Group(()),[[1,3],[4,1]]);;','invalid Coxeter matrix'),('CoxeterTargetEpis(Group(()),Group(()),[[1]]);;','whole fp source required')]
 for n,(body,marker) in enumerate(bads):
  q=a.out/('bad'+str(n)+'.g');q.write_text('LoadPackage("LINS");;\nRead('+json.dumps(str(ROOT/'coxeter_seeds.g'))+');;\n'+body+'\nQUIT;\n');r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(q)],capture_output=True,text=True,timeout=15);(a.out/('bad'+str(n)+'.stdout')).write_text(r.stdout);(a.out/('bad'+str(n)+'.stderr')).write_text(r.stderr);need(r.returncode!=0 and marker in r.stdout+r.stderr,'damaged source accepted')
 for envopt in [False,True]:
  env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);target=a.out/('opt'+str(envopt));cmd=[sys.executable]
  if envopt:env['PYTHONOPTIMIZE']='1'
  else:cmd+=['-O']
  cmd += [str(ROOT/'check.py'),'--out',str(target)];r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=10);need(r.returncode!=0 and 'optimized execution unsupported' in r.stderr and not target.exists(),'optimization guard')
 pages=None
 if a.render:
  native=a.out/'native';native.mkdir();shutil.copyfile(ROOT/'method.tex',native/'method.tex')
  for n in [1,2]:run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),str(native/'method.tex')],a.out/('latex'+str(n)))
  log=(native/'method.log').read_text();need('Overfull' not in log and 'undefined' not in log,'native warning')
  run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'method.pdf')],a.out/'render');pages=len(list(native.glob('page-*.png')))
 result={'status':'PASS','exports':len(m['exports']),'bindings':len(deps),'literal_seed_cases':18,'surjective_inner_orbits':7,'complete_kernel_controls':3,'composed_image_equalities':676,'exact_deltas':deltas,'damaged_sources':3,'optimization_guards':2,'native_pages':pages,'target_census_credit':0,'whole_original_credit':0};(a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
