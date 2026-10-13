from itertools import permutations
from collections import deque
import argparse,hashlib,json,os,re,subprocess
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));parser.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean');args=parser.parse_args()
A=args.packet;O=args.out;O.mkdir()
if hashlib.sha256((A/'manifest.json').read_bytes()).hexdigest()!='79e1e922dc4da4290d498d516b79f45fa5e5944059d1fd6c728fef806f653b1b':raise ValueError('wrong author edition')
for row in json.loads((A/'manifest.json').read_text())['exports']:
 p=A/row['path']
 if p.stat().st_size!=row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('changed author export')
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def generated(gens,n):
 one=tuple(range(n));known={one};queue=deque([one])
 while queue:
  p=queue.popleft()
  for g in gens:
   q=compose(p,g)
   if q not in known:known.add(q);queue.append(q)
 return frozenset(known)
def transposition(a,b,n):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
sym=list(permutations(range(4)));trivial=generated([],4);subs=[trivial];seen={trivial}
for p in subs:
 for g in sym:
  if g not in p:
   q=generated(list(p)+[g],4)
   if q not in seen:seen.add(q);subs.append(q)
if len(subs)!=30:raise ValueError('complete S4 subgroup inventory')
checks=0;positive=0;negative=0
for p in subs:
 for q in subs:
  if not p<=q:continue
  for a in range(4):
   orbit={x[a] for x in p};complement=set(range(4))-orbit
   kernel={x for x in q if all(x[j]==j for j in complement)}
   rhs=kernel<=p
   saturated=generated([x+(4,) for x in p]+[transposition(a,4,5)],5)
   lhs={x for x in q if x+(4,) in saturated}==p
   if lhs!=rhs:raise ValueError('kernel/intersection equivalence')
   checks+=1;positive+=rhs;negative+=not rhs
if checks!=600:raise ValueError('complete subgroup/root tests')
pins=json.loads((A/'dependency_manifest.json').read_text());packages=args.packages
for pin in pins['packages']:
 d=packages/pin['name']
 rev=subprocess.run(['git','-C',d,'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
 if rev!=pin['rev']:raise ValueError('wrong dependency revision')
 if subprocess.run(['git','-C',d,'diff','--quiet','HEAD','--']).returncode:raise ValueError('changed dependency source')
libs=[str(packages/x['name']/'.lake/build/lib/lean') for x in pins['packages'] if (packages/x['name']/'.lake/build/lib/lean').is_dir()]
text=(A/'RestrictionKernelCriterion.lean').read_text();src=O/'RestrictionKernelCriterion.lean';src.write_text(text)
if re.search(r'\b(sorry|admit|axiom|native_decide)\b',text):raise ValueError('unpermitted proof placeholder')
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
lean=args.lean
version=subprocess.run([lean,'--version'],capture_output=True,text=True,check=True).stdout
if 'version 4.32.2,' not in version:raise ValueError('wrong Lean version')
p=subprocess.run([lean,'-o','RestrictionKernelCriterion.olean',src.name],cwd=O,env=env,capture_output=True,text=True,timeout=120)
(O/'lean.stdout').write_text(p.stdout);(O/'lean.stderr').write_text(p.stderr)
if p.returncode or 'warning:' in p.stdout+p.stderr:raise ValueError('fresh direct Lean compile')
axs=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",p.stdout,re.S)
if len(axs)!=3 or any(set(re.findall(r'[A-Za-z][\w.]*',a))-{'propext','Classical.choice','Quot.sound'} for _,a in axs):raise ValueError('scoped proof inventory')
r={'status':'PASS_DISTINCT_ROOT','independent_python_subgroups':30,'independent_kernel_cases':checks,'positive_cases':positive,'negative_cases':negative,'author_program_imported':False,'GAP_used_for_distinct_finite_check':False,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'formal_declarations':[name for name,a in axs],'standard_axioms_only':True,'cached_dependencies_trusted':True,'complete_string_criteria_formalized':False}
(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
