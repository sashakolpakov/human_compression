import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import itertools,json,time
N=9;V=tuple(range(N));start=time.monotonic()
def permutation(swaps):
 p=list(V)
 for x,y in swaps:p[x],p[y]=p[y],p[x]
 return tuple(p)
def commute(p,q):return all(p[q[x]]==q[p[x]]for x in V)
def components(marks):
 parent=list(V)
 def root(x):
  while parent[x]!=x:x=parent[x]
  return x
 for p in marks:
  for x in V:parent[root(x)]=root(p[x])
 return tuple(root(x)for x in V)
def eligible(t,i):
 lab=components(t[:i]+t[i+1:]);return [(x,t[i][x])for x in V if x<t[i][x]and lab[x]!=lab[t[i][x]]]
def rooted_map(t,z):
 f={0:0};todo=[0]
 while todo:
  x=todo.pop()
  for a,b in zip(t,z):
   y=a[x];v=b[f[x]]
   if y in f:
    if f[y]!=v:return None
   else:f[y]=v;todo.append(y)
 if len(f)!=9 or len(set(f.values()))!=9:return None
 return tuple(f[x]for x in V)
models=[]
for ra in range(3):
 for rd in range(3):
  for both in range(3):
   for regular in range(2):
    fixed=5-2*(ra+rd+both)-4*regular
    if fixed<0:continue
    aa=[(0,1)];dd=[(7,8)];p=2
    for kind,count in [('a',ra),('d',rd),('both',both)]:
     for j in range(count):
      if kind in['a','both']:aa.append((p,p+1))
      if kind in['d','both']:dd.append((p,p+1))
      p+=2
    for j in range(regular):aa.extend([(p,p+1),(p+2,p+3)]);dd.extend([(p,p+2),(p+1,p+3)]);p+=4
    assert p+fixed==7
    models.append({'type':[ra,rd,both,regular,fixed],'a':permutation(aa),'d':permutation(dd)})
assert len(models)==11
middle=[]
for q in itertools.permutations(range(1,8)):
 p=(0,)+q+(8,)
 if p!=V and all(p[p[x]]==x for x in V):middle.append(p)
assert len(middle)==231
sequence=[0,1,0,1,2,3,2,3];target=tuple(permutation([(j,j+1)for j,c in enumerate(sequence)if c==i])for i in range(4));survivors=[];rows=[]
for index,row in enumerate(models):
 a,d=row['a'],row['d'];bs=[p for p in middle if commute(p,d)];cs=[p for p in middle if commute(p,a)];trans=paired=0
 for b in bs:
  for c in cs:
   t=(a,b,c,d)
   if len(set(t))!=4 or len(set(components(t)))!=1:continue
   trans+=1;es=[eligible(t,i)for i in range(4)]
   if min(map(len,es))<2:continue
   paired+=1;f=rooted_map(t,target);survivors.append({'case':index,'marks':t,'eligible':es,'path_map':f})
 rows.append({'case':index,'type':row['type'],'middle_left':len(bs),'middle_right':len(cs),'pairs':len(bs)*len(cs),'transitive':trans,'paired':paired})
report={'status':'COMPLETE_ELEVEN_ENDPOINT_MODELS','models':models,'rows':rows,'target':target,'survivors':survivors,'survivor_count':len(survivors),'all_survivors_path':all(s['path_map']is not None for s in survivors),'seconds':time.monotonic()-start,'scope':'Full normalized endpoint pair coverage follows from written Klein-orbit argument; no IP or full-group assumption in this search.'}
p=Path(__file__).with_name('enumeration01.json');assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in['models','survivors','target']}))
