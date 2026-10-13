"""Explicit source exclusions, byte reuse and exact L059 publication inventory."""
from pathlib import Path
import collections,hashlib,json,subprocess,sys
if sys.flags.optimize:raise RuntimeError('No optimization')
S=Path(__file__).resolve().parents[2];R=S.parents[1]/'math_compression';W=Path(__file__).parent
def need(v,msg):
 if not v:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((W/'discovery01.json').read_text());files={(x['origin'],x['path']):x for x in d['files']}
byhash=collections.defaultdict(list)
for x in files.values():byhash[x['sha256']].append(x)
resolutions=[]
for issue in d['issues']:
 pin=issue['pin'];matches=[x for x in byhash[pin['sha256']] if x['bytes']==pin.get('bytes',x['bytes'])]
 need(matches,'unresolved dependency '+str(issue));r=matches[0]
 resolutions.append(dict(context=issue['context'],historical_pin=pin,resolved_origin=r['origin'],resolved_path=r['path'],reason='Exact acquired bytes; original relative source root was declared by the earlier component.'))
omit={('study',x['path'].removeprefix(str(S)+'/')) for x in json.loads((S/'corpus106_L059_principal_v2/source_ledger.json').read_text())}
# The explicit ledger includes raw upstream numeric lists, restored by exact
# bounded public input records instead; no proof or witness is omitted.
for name in ['c4_index.html','c4_index_20110130.html','final_and_foster_web_receipt.json','source_tables_01.png','source_tables_02.png','Wilson_Potocnik_coverage_page2.png']:
 omit.add(('study','reboot_20261013/L059_recovery_work/'+name))
for name in ['source-1.png','source-2.png']:omit.add(('study','reboot_20261013/L059_principal_distinct/'+name))
need(omit<=files.keys(),'unregistered documentary omission')
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');needed={(x['bytes'],x['sha256']) for key,x in files.items() if key not in omit};existing={}
for rel in tracked:
 if not rel.endswith('/transport.json'):continue
 try:t=json.loads((R/rel).read_text())
 except (ValueError,OSError):continue
 for x in t.get('files',[]):
  if all(k in x for k in ['bytes','sha256','public_path','encoding','stored_bytes','stored_sha256']):existing.setdefault((x['bytes'],x['sha256']),{k:x[k] for k in ['public_path','encoding','stored_bytes','stored_sha256']})
sizes={x[0] for x in needed}
for rel in tracked:
 p=R/rel
 if rel and p.is_file() and p.stat().st_size in sizes:
  key=(p.stat().st_size,sha(p))
  if key in needed:existing.setdefault(key,dict(public_path=rel,encoding='identity',stored_bytes=key[0],stored_sha256=key[1]))
rows=[]
for key,x in sorted(files.items(),key=lambda item:(not item[1]['path'].startswith('corpus106_L059_principal_v2/'),item[0])):
 r=dict(x);ident=(r['bytes'],r['sha256'])
 if key in omit:r['transport']='PRIVATE_PRIMARY_SOURCE_HASH_ONLY'
 elif ident in existing:
  e=existing[ident];p=R/e['public_path'];need(p.is_file() and p.stat().st_size==e['stored_bytes'] and sha(p)==e['stored_sha256'],'public payload changed');r.update(transport='EXISTING_PUBLIC',**e)
 else:r['transport']='NEW_FROZEN_FILE'
 if r['path'].endswith('.md'):r['public_suffix_override']='.txt'
 rows.append(r)
out=dict(status='PRIVATE_L059_TRANSPORT_INVENTORY_NOT_ADMISSION',files=rows,packets=d['packets'],logical_files=len(rows),missing_final_reviews=[],primary_sources_hash_only=[dict(origin=o,path=p) for o,p in sorted(omit)],historical_documentary_exceptions=[],relative_locator_resolutions=resolutions,legacy_common_aliases={'bindings':[]},predecessor_transports=[],closure_boundary='Complete L059 principal v1/v2, distinct/root reviews, two complete bounded components with their root reviews, and every exact declared proof/program/execution dependency. Primary documentary/full upstream sources are explicit hash-only records; bounded numeric inputs have public exact replacements.',markdown_transport='Any acquired working Markdown is stored byte-exact as a public .txt object, restored only into the local replay tree.',primary_omission_addendum='Full original articles, upstream source documents/data catalogues and their source-page rasters are hash-only. Exact bounded numerical rosters and all retained execution evidence are public. No source-free proof, program, witness or receipt is omitted.',source_assets_exported=False,private_runtime_fallback=False,whole_original_credit=0)
(W/'inventory01.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(files=len(rows),omitted=len(omit),packets=len(d['packets']),locators=len(resolutions),existing=sum(x['transport']=='EXISTING_PUBLIC' for x in rows),new=sum(x['transport']=='NEW_FROZEN_FILE' for x in rows),new_raw_bytes=sum(x['bytes'] for x in rows if x['transport']=='NEW_FROZEN_FILE'))))
