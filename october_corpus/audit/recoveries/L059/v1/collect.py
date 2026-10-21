"""Exact private L059 transport discovery; no public writes."""
from pathlib import Path
import collections,hashlib,json,sys
if sys.flags.optimize:raise RuntimeError('No optimization')
S=Path(__file__).resolve().parents[2];R=S.parents[1]/'math_compression';W=Path(__file__).parent
files={};packets={};issues=[];queue=collections.deque();expanded=set();cache={}
def sha(p):
 p=p.resolve()
 if p not in cache:cache[p]=hashlib.sha256(p.read_bytes()).hexdigest()
 return cache[p]
def add(p,row=None,context='root'):
 p=p.resolve()
 if not p.is_file():issues.append(dict(kind='missing',path=str(p),context=context));return
 origin='study' if p.is_relative_to(S) else 'public' if p.is_relative_to(R) else 'external'
 if origin=='external':issues.append(dict(kind='external',path=str(p),pin=row,context=context));return
 if row and (sha(p)!=row['sha256'] or row.get('bytes',p.stat().st_size)!=p.stat().st_size):issues.append(dict(kind='changed',path=str(p),pin=row,context=context));return
 rel=str(p.relative_to(S if origin=='study' else R));key=(origin,rel)
 if key in files:return
 files[key]=dict(origin=origin,path=rel,source_path=rel,bytes=p.stat().st_size,sha256=sha(p))
 if p.suffix=='.json':queue.append((p,origin,rel))
def pinned(obj,p):
 name=obj.get('path');h=obj.get('sha256')
 if not isinstance(name,str) or not isinstance(h,str) or len(h)!=64:return
 q=Path(name);candidates=[q] if q.is_absolute() else [S/q,p.parent/q,R/q]
 good=[x for x in candidates if x.is_file() and sha(x)==h and obj.get('bytes',x.stat().st_size)==x.stat().st_size]
 if good:add(good[0],obj,str(p))
 else:issues.append(dict(kind='unresolved_pin',pin=obj,context=str(p)))
def walk(j,p):
 if isinstance(j,dict):
  pinned(j,p)
  for k,v in j.items():
   if isinstance(k,str) and k.startswith(str(S)+'/') and isinstance(v,str) and len(v)==64:pinned(dict(path=k,sha256=v),p)
   if k!='exports':walk(v,p)
 elif isinstance(j,list):
  for x in j:walk(x,p)
roots=['corpus106_L059_principal_v2','corpus106_L059_principal_independent_review','corpus106_L059_principal_root_adoption','reboot_20261013/L059_publication_inputs']
for root in roots:add(S/root/'manifest.json')
while queue:
 p,origin,rel=queue.popleft()
 if p in expanded:continue
 expanded.add(p)
 try:j=json.loads(p.read_text())
 except (ValueError,UnicodeError):continue
 if p.name=='manifest.json' and isinstance(j,dict) and isinstance(j.get('exports'),list):
  packets[(origin,rel)]=dict(origin=origin,path=rel,sha256=sha(p),exports=len(j['exports']))
  for x in j['exports']:add(p.parent/x['path'],x,str(p))
 # Exact bindings of every acquired L059 edition/review are followed. JSON
 # execution records are already acquired through these explicit dependency
 # lists; their incidental historical paths do not add unrelated studies.
 if origin=='study' and ('L059' in Path(rel).parts[0] or p.name in ['edition_delta.json','source_ledger.json']):walk(j,p)
 if len(files)>25000:raise RuntimeError('unexpected closure expansion')
out=dict(status='PRIVATE_EXACT_L059_DISCOVERY',roots=roots,files=list(files.values()),packets=list(packets.values()),issues=issues)
(W/'discovery01.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(files=len(files),packets=len(packets),issues=len(issues),bytes=sum(x['bytes'] for x in files.values()))))
print(json.dumps(issues[:12],indent=2))
