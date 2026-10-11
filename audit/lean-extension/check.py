#!/usr/bin/env python3
"""Fresh bounded Lean replay and a literal false-weakening countermodel."""
import argparse,hashlib,json,os,pathlib,re,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parent.parent
SOURCE=REPO/"research/case_study/formal/MarkedInvolutionExtension.lean"
PINS=REPO/"research/case_study/formal/dependency_manifest.json"

def need(ok,msg):
 if not ok:raise RuntimeError('MARKED_EXTENSION_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def span(gens):
 out={0};todo=[0]
 for x in todo:
  for r in gens:
   y=x^r
   if y not in out:out.add(y);todo.append(y)
 return out

def countermodel(mutate=False):
 G=set(range(16));a,b,c=1,2,4;z=8 if mutate else 7
 H=span([a,b,c]);K=span([a,b,c,z])
 need(len(H)==8 and H<G,'proper original hyperplane')
 need(all(span([a,b,c,x])==G for x in G-H),'maximality checked for every outside element')
 need(len({a,b,c,z})==4 and all(x!=0 and x^x==0 for x in [a,b,c,z]),'actual distinct nonidentity involutions')
 need(all(x^y==y^x for x in G for y in G),'actual distant commutations')
 need(z in H and K==H and K!=G,'dropping outside gives failure of generation')
 need({x for x in H if x^a==a^x and x^b==b^x}==H,'internal centralizer is nontrivial')
 return dict(group_order=16,old_subgroup_order=8,new_subgroup_order=8,marks=[a,b,c,z],
             all_four_distinct=True,all_string_relations=True,old_subgroup_maximal=True,
             new_generator_inside=True,generates_whole=False,internal_centralizer_order=8)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True)
 ap.add_argument('--lean',type=pathlib.Path,default=pathlib.Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
 ap.add_argument('--packages',type=pathlib.Path,default=pathlib.Path('/Users/sasha/bogachev/formal/.lake/packages'))
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
 out=a.out.resolve();out.mkdir(parents=True)
 scope=json.loads((ROOT/'scope.json').read_text())
 for x in scope['package_inputs']:
  p=ROOT/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'bound input '+x['path'])
 pins=json.loads((PINS).read_text());deps=[]
 for row in pins['packages']:
  p=a.packages/row['name'];rev=subprocess.check_output(['git','-C',p,'rev-parse','HEAD'],text=True).strip()
  need(rev==row['rev'],'package revision '+row['name'])
  need(subprocess.run(['git','-C',p,'diff','--quiet','HEAD','--']).returncode==0,'tracked package changes '+row['name'])
  deps.append(dict(name=row['name'],rev=rev))
 version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'pinned Lean')
 env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
 source=(SOURCE).read_text()
 need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',source,re.M),'no custom axiom or proof hole')
 executions=[]
 def compile(label,text,positive):
  path=out/(label+'.lean');path.write_text(text);start=time.monotonic()
  r=subprocess.run([a.lean,'-o',path.with_suffix('.olean'),path],cwd=out,env=env,text=True,capture_output=True,timeout=180)
  for s,data in [('stdout',r.stdout),('stderr',r.stderr)]:(out/(label+'.'+s)).write_text(data)
  executions.append(dict(label=label,returncode=r.returncode,seconds=round(time.monotonic()-start,3),stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr'))))
  if positive:need(r.returncode==0 and not re.search(r'warning:|error:|sorryAx',r.stdout+r.stderr),'clean main compile')
  else:need(r.returncode!=0 and 'error:' in r.stdout+r.stderr,'false weakening rejected '+label)
  return r
 r=compile('main',source,True)
 axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",r.stdout)
 need(len(axioms)==9 and all(set(re.findall(r'[\w.]+',v))<={'propext','Classical.choice','Quot.sound'} for _,v in axioms),'nine standard-only reports')
 old='(hcent : H ⊓ Subgroup.centralizer ({a, b} : Set G) = ⊥)'
 need(source.count(old)==1,'centralizer control applies once')
 compile('without_internal_centralizer',source.replace(old,'(hcent : True)'),False)
 old='(hz : z ∉ Subgroup.closure (Set.range (triple a b c)))'
 need(source.count(old)==2,'outside control applies at both interfaces')
 compile('without_outside',source.replace(old,'(hz : True)'),False)
 model=countermodel()
 rejected=False
 try:countermodel(True)
 except RuntimeError as e:
  rejected='dropping outside gives failure of generation' in str(e)
 need(rejected,'altered countermodel rejected')
 report=dict(status='PASS',lean_version=version,dependencies=deps,source_sha256=sha(SOURCE),
  declarations=[{'name':n,'axioms':re.findall(r'[\w.]+',v)} for n,v in axioms],executions=executions,
  countermodel=model,altered_countermodel_rejected=rejected,
  scope='Generic actual four-generator extension and subgroup generation. No PSL torus/maximality or final family theorem is formalized.',
  source_credits=0,question_credits=0)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','declarations':9,'controls':3,'report':str(out/'report.json')}))
if __name__=='__main__':main()
