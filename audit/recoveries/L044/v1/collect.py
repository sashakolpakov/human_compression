"""Inspect exact L044 proof and review closure; writes private inventory only."""
from pathlib import Path
import sys,json,hashlib,collections,argparse
if sys.flags.optimize:raise RuntimeError('No optimization')
S=Path(__file__).resolve().parents[2];R=S.parents[1]/'math_compression';W=Path(__file__).parent
cache={};files={};packets={};issues=[];edges=[];queue=collections.deque();expanded=set();aliases={}
loc=json.loads((S/'reboot_20261013/L044_binary_one_neighbour_distinct/legacy_locator_map.json').read_text())
for x in loc['bindings']:aliases[x['expected']]=x['actual']
def sha(p):
 p=p.resolve()
 if p not in cache:cache[p]=hashlib.sha256(p.read_bytes()).hexdigest()
 return cache[p]
def add(p,expected=None,ref=None,logical=None):
 p=p.resolve()
 if not p.is_file():issues.append({'kind':'missing','path':str(p),'ref':str(ref)});return
 origin='study'if p.is_relative_to(S)else'public'if p.is_relative_to(R)else'external'
 if origin=='external':issues.append({'kind':'external','path':str(p),'ref':str(ref)});return
 actual=str(p.relative_to(S if origin=='study'else R));rel=logical or actual
 if expected and (sha(p)!=expected['sha256'] or ('bytes'in expected and p.stat().st_size!=expected['bytes'])):
  issues.append({'kind':'changed','path':str(p),'expected':expected,'actual':sha(p),'ref':str(ref)});return
 key=(origin,rel)
 if ref:edges.append({'from':str(ref),'to_origin':origin,'to':rel})
 if key in files:return
 files[key]={'origin':origin,'path':rel,'source_path':actual,'bytes':p.stat().st_size,'sha256':sha(p)}
 if p.suffix=='.json':queue.append((p,origin,rel))
def pinned(obj,context):
 path=obj.get('path')
 if not isinstance(path,str)or not isinstance(obj.get('sha256'),str)or len(obj['sha256'])!=64:return
 q=Path(path);candidates=[q]if q.is_absolute()else[S/q,context.parent/q,R/q]
 if path in aliases:candidates.append(S/aliases[path])
 good=[p for p in candidates if p.is_file()and sha(p)==obj['sha256']and('bytes'not in obj or p.stat().st_size==obj['bytes'])]
 if good:
  p=good[0];logical=path if path in aliases and p==S/aliases[path]else None
  add(p,obj,str(context.relative_to(S))if context.is_relative_to(S)else str(context),logical)
 else:issues.append({'kind':'unresolved_pin','pin':obj,'context':str(context.relative_to(S))if context.is_relative_to(S)else str(context)})
def walk(obj,context):
 if isinstance(obj,dict):
  pinned(obj,context)
  # Recorded absolute path -> digest maps are exact audit inputs.
  for k,v in obj.items():
   if isinstance(k,str)and k.startswith(str(S)+'/')and isinstance(v,str)and len(v)==64:pinned({'path':k,'sha256':v},context)
   if k!='exports':walk(v,context)
 elif isinstance(obj,list):
  for v in obj:walk(v,context)
def run():
 roots=['corpus106_L044_principal_v1','corpus106_L044_principal_independent_review']
 if (S/'corpus106_L044_principal_root_adoption/manifest.json').exists():roots.append('corpus106_L044_principal_root_adoption')
 if (S/'corpus106_L044_principal_root_review/manifest.json').exists():roots.append('corpus106_L044_principal_root_review')
 for name in roots:add(S/name/'manifest.json')
 # Complete already-public L038 and L071 transports are exact acquisition
 # boundaries. Their internal historical catalogues are not recursively
 # reinterpreted as new dependencies.
 for prior in ['L038','L071']:
  tp=R/f'audit/recoveries/{prior}/v1/transport.json';tj=json.loads(tp.read_text());add(tp)
  for row in tj['files']:
   if row['origin']=='study':add(S/row['path'],row,ref=str(tp))
   elif row['origin']in ['repo','public']:add(R/row['path'],row,ref=str(tp))
   else:files[(row['origin'],row['path'])]=dict(row)
  for row in tj.get('packets',[]):packets[row['path']]=row

 add(S/'reboot_20261013/L044_binary_one_neighbour_distinct/legacy_locator_map.json')
 for logical,actual in aliases.items():add(S/actual,logical=logical)
 while queue:
  p,origin,rel=queue.popleft()
  if p in expanded:continue
  expanded.add(p)
  try:j=json.loads(p.read_text())
  except (ValueError,UnicodeError):continue
  if p.name=='manifest.json'and isinstance(j,dict)and isinstance(j.get('exports'),list):
   # A nested historical manifest records its containing edition's selection.
   # It is not independently expanded; top-level packets are whole acquisitions.
   top=(origin=='study'and len(Path(rel).parts)==2)
   if top:
    packets[rel]={'origin':origin,'path':rel,'sha256':sha(p),'exports':len(j['exports'])}
    for row in j['exports']:
     target=p.parent/row['path'];logical=None
     if not target.is_file():
      locrel=str(target.relative_to(S))if target.is_relative_to(S)else''
      if locrel in aliases:target=S/aliases[locrel];logical=locrel
     add(target,row,rel,logical)
   else:continue
  if origin=='study' and 'L044' in Path(rel).parts[0]:walk(j,p)
  if len(files)>30000:raise RuntimeError('Unexpected closure expansion')
 out={'status':'PRIVATE_CLOSURE_DISCOVERY','roots':roots,'files':list(files.values()),'packets':list(packets.values()),'issues':issues,'edges':edges,'expanded_json':len(expanded)}
 (W/'discovery03.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'files':len(files),'packets':len(packets),'issues':len(issues),'expanded_json':len(expanded),'bytes':sum(x['bytes']for x in files.values())}))
 print(json.dumps(issues[:15],indent=2))
run()
