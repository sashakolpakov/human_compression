"""Private exact closure collection for the accepted L120 synthesis."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
from pathlib import Path
import collections,hashlib,json
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression'
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
cache={}
def pin(p):
 p=p.resolve()
 if p not in cache:
  h=hashlib.sha256();n=0
  with p.open('rb')as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  cache[p]={'bytes':n,'sha256':h.hexdigest()}
 return cache[p]
def need(c,m):
 if not c:raise ValueError(m)
files={};packets={};predecessors=[];queue=collections.deque();expanded=set();issues=[];resolutions=[]
for name in('L042','L071'):
 p=R/f'audit/recoveries/{name}/v1/transport.json';t=load(p);predecessors.append({'path':str(p.relative_to(R)),**pin(p),'metadata':{k:t[k]for k in('relative_locator_resolutions','historical_documentary_exceptions','legacy_common_aliases')if k in t}})
 for old in t['files']:
  r=dict(old);key=(r['origin'],r['path'])
  if key in files:need(all(files[key][k]==r[k]for k in('bytes','sha256')),'Conflicting predecessors');continue
  if not r['transport'].endswith('HASH_ONLY'):r['transport']='EXISTING_PUBLIC'
  files[key]=r
 for r in t['packets']:
  key=(r['origin'],r['path']);need(key not in packets or packets[key]==r,'Packet conflict');packets[key]=r
prior_keys=set(files)
def identity(p):
 p=p.resolve()
 if p.is_relative_to(S):return 'study',str(p.relative_to(S))
 if p.is_relative_to(R):return 'public',str(p.relative_to(R))
 return 'external',str(p)
def add(p,row=None):
 p=p.resolve();key=identity(p)
 if key in files:
  r=files[key];need(not row or all(row.get(k,r[k])==r[k]for k in('bytes','sha256')),'Conflicting pin '+str(key));return
 source=p
 if not p.is_file() and row:
  for candidate in list(files.values()):
   if candidate['sha256']!=row['sha256']or candidate['bytes']!=row.get('bytes',candidate['bytes']):continue
   base=S if candidate['origin']=='study'else R if candidate['origin']=='public'else Path('/')
   q=base/candidate.get('source_path',candidate['path'])
   if q.is_file()and pin(q)['sha256']==row['sha256']:source=q;break
  if source==p:
   issues.append({'context':'manifest export','logical':str(p),'pin':row});return
 need(source.is_file(),'Missing exact dependency '+str(p));actual=pin(source);need(not row or all(row.get(k,actual[k])==actual[k]for k in('bytes','sha256')),'Changed pin '+str(p))
 origin,rel=key;so,sr=identity(source);files[key]={'origin':origin,'path':rel,'source_origin':so,'source_path':sr,**actual,'transport':'NEW_FROZEN_FILE'}
 if source!=p:
  resolutions.append({'context':'manifest export','historical_pin':{'path':str(p),**actual},'resolved_origin':so,'resolved_path':sr,'logical_alias':{'origin':origin,'path':rel}})
  if p.suffix=='.json':issues.append({'context':'JSON export alias needs explicit context','logical':str(p),'actual':str(source),'pin':row})
  return
 if p.suffix=='.json':queue.append((p,origin,rel))
# The exact twelve locator corrections already reviewed with the principal.
known=load(S/'corpus106_L120_principal_v2/historical_locators.json')
known_map={(r['historical']['binding']['path'],r['actual']['sha256']):r['actual']for r in known}
def literal(x,context):
 name=x.get('path');h=x.get('sha256')
 if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
 namep=Path(name);origin=x.get('namespace',x.get('origin'));candidates=[]
 if namep.is_absolute():candidates=[namep]
 else:
  if origin in('study','public'):candidates.append((S if origin=='study'else R)/namep)
  candidates.extend([S/namep,context.parent/namep,R/namep])
 for q in candidates:
  if q.is_file()and pin(q)['sha256']==h and x.get('bytes',pin(q)['bytes'])==pin(q)['bytes']:
   add(q,x)
   k=identity(q)
   if not namep.is_absolute()and k not in [('study',name),('public',name)]:resolutions.append({'context':str(context.relative_to(S)if context.is_relative_to(S)else context.relative_to(R)),'historical_pin':x,'resolved_origin':k[0],'resolved_path':k[1]})
   return
 for key in [('study',name),('public',name),identity(namep)if namep.is_absolute()else('none','')]:
  r=files.get(key)
  if r and r['sha256']==h and x.get('bytes',r['bytes'])==r['bytes']:return
 k=known_map.get((name,h))
 if k:
  add((S if k['namespace']=='study'else R)/k['path'],k);resolutions.append({'context':str(context.relative_to(S)if context.is_relative_to(S)else context.relative_to(R)),'historical_pin':x,'resolved_origin':k['namespace'],'resolved_path':k['path']});return
 issues.append({'context':str(context),'pin':x})
def walk(x,p):
 if isinstance(x,dict):
  literal(x,p)
  for k,v in x.items():
   if isinstance(k,str)and k.startswith('/')and isinstance(v,str)and len(v)==64:literal({'path':k,'sha256':v},p)
   if k!='exports':walk(v,p)
 elif isinstance(x,list):
  for z in x:walk(z,p)
for name,h in [('corpus106_L120_principal_v2','b5860c241cb773ae005ba412237f5b30220f7c045f5c90e21a35f2f133cc7831'),('corpus106_L120_principal_root_review','2478f1609c3ff05aec7ca856c44190042bafcaf169b118266a2f9bea40e09543')]:
 p=S/name/'manifest.json';need(pin(p)['sha256']==h,'Exact accepted edition');add(p)
for p in predecessors:add(R/p['path'],p)
while queue:
 p,origin,rel=queue.popleft()
 if p in expanded:continue
 expanded.add(p)
 try:j=load(p)
 except(ValueError,UnicodeError):continue
 if p.name=='manifest.json'and isinstance(j,dict)and isinstance(j.get('exports'),list):
  packets[(origin,rel)]={'origin':origin,'path':rel,'sha256':pin(p)['sha256'],'exports':len(j['exports'])}
  for row in j['exports']:add(p.parent/row['path'],row)
 if origin=='study' and (origin,rel)not in prior_keys:walk(j,p)
# Preserve every issue for resolution; never omit unknown proof bytes.
save(W/'closure_initial.json',{'files':list(files.values()),'packets':list(packets.values()),'predecessors':predecessors,'relative_locator_resolutions':resolutions,'issues':issues,'expanded_json':len(expanded),'prior_files':len(prior_keys)})
save(W/'unresolved_initial.json',issues)
print(json.dumps({'files':len(files),'packets':len(packets),'new':len(files)-len(prior_keys),'issues':len(issues),'expanded':len(expanded)}))
