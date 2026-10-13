"""Separate literal orbit/conjugacy/leaf/receipt checks; no census completeness inference."""
import ast,hashlib,itertools,json,sys
from pathlib import Path
if sys.flags.optimize: raise RuntimeError('normal Python required')
S=Path('/Users/sasha/medusa/research/leemans');P=S/'topic_B_L019_balanced_pairs_v1';O=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def tup(line):return tuple(tuple(x-1 for x in g) for g in ast.literal_eval(line.split('|',1)[1]))
def orbits(t,n):
 left=set(range(n));out=[]
 while left:
  a=min(left);seen={a};q=[a]
  for x in q:
   for g in t:
    if g[x] not in seen:seen.add(g[x]);q.append(g[x])
  left-=seen;out.append(seen)
 return out
def group(t,n):
 e=tuple(range(n));seen={e};queue=[e]
 for g in queue:
  for a in t:
   h=tuple(g[a[x]] for x in range(n))
   if h not in seen:seen.add(h);queue.append(h)
 return seen
def ip(t,n):
 r=len(t);groups=[group([g for i,g in enumerate(t) if m>>i&1],n)for m in range(1<<r)]
 for i,a in enumerate(groups):
  for j,b in enumerate(groups):need(a&b==groups[i&j],'leaf extension actual full IP')
 return len(groups)**2
def conjugate(t,p):
 inv=[0]*len(p)
 for i,j in enumerate(p):inv[j]=i
 return tuple(tuple(p[g[inv[x]]] for x in range(len(p)))for g in t)
def intertwiner(a,b,root=0,image=0):
 n=len(a[0]);m={root:image};used={image};todo=[root]
 for x in todo:
  for g,h in zip(a,b):
   y,z=g[x],h[m[x]]
   if y in m:
    if m[y]!=z:return None
   else:
    if z in used:return None
    m[y]=z;used.add(z);todo.append(y)
 need(len(m)==n,'connected tuples')
 p=tuple(m[i]for i in range(n));need(conjugate(a,p)==b,'literal conjugacy witness');return p
wings={};receipts=[]
for n in range(2,13,2):
 d=P/(f'n{n}_run03'if n==12 else f'n{n}_run01');r=json.loads((d/'receipt.json').read_text());raw=(d/'stdout.log').read_bytes();need(r['status']=='COMPLETE_DIAGNOSTIC'and r['returncode']==0 and not(d/'stderr.log').read_bytes(),'terminal receipt')
 for name,h in r['files'].items():need(hashlib.sha256((d/name).read_bytes()).hexdigest()==h,'actual executed input')
 need(hashlib.sha256(raw).hexdigest()==r['stdout_sha256'],'raw execution output')
 lines=raw.decode().splitlines();marks=[x for x in lines if x.startswith('COMPLETE_ANCHORED_CRITICAL_WINGS|')];need(len(marks)==1,'one exhaustion marker')
 ts=[tup(x)for x in lines if x.startswith('SOLUTION|')];wings[n]=ts
 marker=marks[0].split('|');need(int(marker[1])==n and int(marker[2])==n//2 and int(marker[6])==len(ts),'exact terminal dimensions/count')
 for i,t in enumerate(ts):
  for u in ts[:i]:need(intertwiner(t,u) is None,'rooted classes distinct')
 receipts.append({'degree':n,'count':len(ts),'completion':marks[0]})
# Independently expand all degree-six rooted point conjugacies and compare the labelled census.
expanded=set()
for t in wings[6]:
 orbit={conjugate(t,(0,)+p)for p in itertools.permutations(range(1,6))};need(len(orbit)==120,'rooted transitive action is free');need(not expanded&orbit,'disjoint rooted classes');expanded|=orbit
raw=(P/'small_independent_v2.stdout').read_text();labelled=[tup(l)for l in raw.splitlines()if l.startswith('LABELLED|')];need(len(labelled)==len(set(labelled))==720 and set(labelled)==expanded,'literal labelled completeness')
# Actual pure-leaf extension full subset IP, rather than only kernel inclusions, in all small wings.
leaf_pairs=0
for n in [2,4,6]:
 for t in wings[n]:
  z=list(range(n+1));z[0],z[n]=n,0;ext=(tuple(z),)+tuple(g+(n,)for g in t)
  leaf_pairs+=ip(ext,n+1);need(len(group(ext,n+1))==__import__('math').factorial(n+1),'leaf supported full symmetric group')
# Find actual pure perfect cuts and extract the unique balanced pair in every literal glued tuple.
arrays=json.loads((P/'arrays_report.json').read_text())['boundary_literal_classes'];full=[];balanced=[]
for k,rows in arrays.items():
 for row in rows:
  t=tuple(tuple(g)for g in row['marks']);n=len(t[0]);r=len(t);cuts={}
  for i,g in enumerate(t):
   moved={x for x in range(n)if g[x]!=x}
   if len(moved)!=2:continue
   parts=orbits(t[:i]+t[i+1:],n)
   if len(parts)!=2:continue
   prefix={x for h in t[:i]for x in range(n)if h[x]!=x};suffix={x for h in t[i+1:]for x in range(n)if h[x]!=x}
   if not prefix:prefix={next(x for x in moved if x not in suffix)}
   if not suffix:suffix={next(x for x in moved if x not in prefix)}
   if prefix&suffix or prefix|suffix!=set(range(n)) or prefix not in parts or suffix not in parts:continue
   cuts[i]=(2*i-len(prefix),prefix,suffix)
  inds=sorted(cuts);need(inds==list(range(inds[0],inds[-1]+1)),'actual pure cut interval')
  pairs=[i for i in inds if i+1 in cuts and cuts[i][0]==0 and cuts[i+1][0]==1];need(len(pairs)==1,'unique actual balanced pair')
  i=pairs[0];p=row['left'][0];q=row['right'][0];need(i==p and r-i-2==q and n==2*(p+q)+1,'exact wing extraction ranks')
  for old in full:
   if len(old)!=r:continue
   for orient in [t,tuple(reversed(t))]:
    need(all(intertwiner(old,orient,0,x) is None for x in range(n)),'full class distinctness by explicit intertwining')
  full.append(t);balanced.append({'kappa':int(k),'pair_index':i,'pure_indices':inds,'left_rank':p,'right_rank':q})
need(len(full)==101,'all constructed classes')
# Whole export/execution closure retains every literal GAP Read target.
reads=[]
import re
for p in P.rglob('*.g'):
 for target in re.findall(r'Read\("([^\"]+)"\)',p.read_text()):
  q=p.parent/target
  if p.name.startswith('enumerate') and p.parent==P:q=P/'n2_run01'/target
  need(q.exists(),'missing actual Read input '+str(q));reads.append({'file':str(p.relative_to(P)),'read':target,'resolved':str(q.relative_to(P))})
r={'status':'PASS','executed_receipts':receipts,'degree6_literal_rooted_orbit_size':720,'direct_leaf_extension_subset_pairs':leaf_pairs,'independent_full_class_checks':len(full),'actual_balanced_pairs':balanced,'literal_read_closure':reads,'whole_original_credit':0}
(O/'independent_audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in ['actual_balanced_pairs','literal_read_closure','executed_receipts']}))
