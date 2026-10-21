"""Exact L041 closure preparation; acceptance remains a separate prerequisite."""
import sys
if sys.flags.optimize: raise RuntimeError('Unoptimized Python required')
from pathlib import Path
import collections,hashlib,json,subprocess
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression'
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
roots=[('corpus106_L041_decorated_geometry_v2','6f7221a6784c479748786ca2497df0a32f1162cd995e93acb3d9f58dc1665877')]
if (W/'accepted_roots.json').exists():roots=load(W/'accepted_roots.json')
queue=collections.deque();files={};issues=[];expanded=set();packets=[]
PYTHON='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
def key(p):
 p=p.resolve()
 for ns,root in [('study',S),('public',R)]:
  if p.is_relative_to(root):return ns,str(p.relative_to(root))
 need(str(p)==PYTHON,'Explicitly recognized external runtime only: '+str(p))
 return 'runtime',str(p)
def add(p,row=None):
 p=p.resolve();k=key(p);z=pin(p)
 need(row is None or all(row.get(n,z[n])==z[n]for n in ['bytes','sha256']),'Changed input '+str(p))
 if k not in files:
  files[k]=dict(origin=k[0],path=k[1],**z,transport='RUNTIME_IDENTITY_HASH_ONLY'if k[0]=='runtime'else'NEW_FROZEN_FILE')
  if k[0]=='study'and p.suffix=='.json':queue.append(p)
def direct(row,context):
 p=Path(row['path']);ns=row.get('namespace',row.get('origin'))
 if not p.is_absolute():
  if ns in ['study','public']:p=(S if ns=='study'else R)/p
  elif row['path'].startswith('PUBLIC:'):p=R/row['path'][7:]
  else:p=context.parent/p
 add(p,row)
for name,h in roots:add(S/name/'manifest.json',dict(sha256=h))
while queue:
 p=queue.popleft()
 if p in expanded:continue
 expanded.add(p)
 try:j=load(p)
 except(ValueError,UnicodeError):continue
 if isinstance(j,dict)and isinstance(j.get('exports'),list):
  ns,rel=key(p);packets.append(dict(origin=ns,path=rel,sha256=pin(p)['sha256'],exports=len(j['exports'])))
  for row in j['exports']:
   try:direct(row,p)
   except(FileNotFoundError,ValueError)as e:issues.append(dict(context=str(p),pin=row,reason=str(e)))
  dep=p.parent/'dependencies.json'
  if dep.exists():add(dep)
 if p.name=='dependencies.json':
  need(isinstance(j,list),'Explicit dependency list')
  for row in j:
   try:direct(row,p)
   except(FileNotFoundError,ValueError)as e:issues.append(dict(context=str(p),pin=row,reason=str(e)))
# Public admission proof collection is explicitly acquired by the author; all
# already listed files remain literal public objects, not re-run mathematics.
baseline=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()
tracked=set(subprocess.check_output(['git','-C',str(R),'ls-files','-z']).decode().split('\0'))
for r in files.values():
 if r['origin']=='public':need(r['path']in tracked,'Public input must exist in clean checkout '+r['path'])
save(W/'entry_roots.json',roots)
save(W/'closure_initial.json',dict(files=sorted(files.values(),key=lambda r:(r['origin'],r['path'])),packets=sorted(packets,key=lambda r:r['path']),issues=issues,
 collection_boundary='Exact author/review manifest exports and recursively explicit dependency lists; published topic-chamber input files retained exactly. Runtime identities declared separately, never invented study paths.',
 baseline=baseline,review_pending=len(roots)<2,public_writes=False))
print(json.dumps(dict(files=len(files),packets=len(packets),exports=sum(p['exports']for p in packets),issues=len(issues),origins=dict(collections.Counter(r['origin']for r in files.values())),baseline=baseline)))
