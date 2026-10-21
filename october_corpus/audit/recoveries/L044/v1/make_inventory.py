"""Close exact L044 acquisitions with explicit documentary exceptions."""
from pathlib import Path
import json,hashlib,subprocess,collections,sys
if sys.flags.optimize:raise RuntimeError('No optimization')
S=Path(__file__).resolve().parents[2];R=S.parents[1]/'math_compression';W=Path(__file__).parent
D=W/'discovery03.json';j=json.loads(D.read_text());files={(r['origin'],r['path']):r for r in j['files']}
def need(ok,s):
 if not ok:raise ValueError(s)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def pin(p):return dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p))
byhash=collections.defaultdict(list)
for row in files.values():byhash[row['sha256']].append(row)
resolutions=[];exceptions=[]
for issue in j['issues']:
 c=issue.get('context',issue.get('ref',''));p=issue.get('pin',{});h=p.get('sha256');matches=[r for r in byhash.get(h,[])if p.get('bytes',r['bytes'])==r['bytes']]
 if matches:
  r=matches[0];resolutions.append(dict(context=c,historical_pin=p,resolved_origin=r['origin'],resolved_path=r['path'],reason='Exact bytes already acquired; historical path is relative to its declared author or working root.'));continue
 if c=='topic_B_L044_source_intake_v1/reading_receipt.json':
  need(p['path'].endswith('.png')and p.get('physical_page')in range(1,47),'source raster scope');kind='HISTORICAL_PRIMARY_SOURCE_RENDER_HASH_ONLY';reason='Private source-page raster from before reboot; original source PDF hash retained. Not a proof or finite certificate.'
 elif c=='topic_B_L044_single_crossing_v1/visual_review.json' and p.get('path')=='/private/tmp/single_crossing_support.log':
  kind='HISTORICAL_TYPESETTING_LOG_HASH_ONLY';reason='Temporary TeX log is unavailable; frozen source/PDF and recorded clean diagnostics survive. It is not an execution certificate.'
 elif c.endswith('/visual_review.json'):
  need(p.get('path','').endswith('.png'),'Only raster cache exception permitted')
  parent=c.split('/')[0];pdfs=[r['path']for r in files.values()if r['origin']=='study'and r['path'].startswith(parent+'/')and r['path'].endswith('.pdf')]
  need(pdfs,'Native PDF must survive lost raster cache: '+c);kind='HISTORICAL_NATIVE_RENDER_CACHE_HASH_ONLY';reason='Temporary raster cache is unavailable after reboot; frozen native PDF and visual-review record survive. No mathematical or program evidence is omitted.'
 elif c.endswith('/external_software.json')and issue['kind']=='external':
  kind='EXTERNAL_SOFTWARE_HASH_ONLY';reason='Installed GAP software/library file remains a declared environment premise, not a project proof payload.'
 else:raise ValueError('Unresolved substantive pin: '+json.dumps(issue))
 exceptions.append(dict(kind=kind,record=issue,reason=reason))
# Primary documentary files inherited from the two exact accepted transports.
omit=set()
for previous in ['L038','L071']:
 tr=json.loads((R/f'audit/recoveries/{previous}/v1/transport.json').read_text())
 for row in tr['files']:
  if row['transport'].endswith('HASH_ONLY'):omit.add((row['origin']if row['origin']!='repo'else'public',row['path']))
for key,row in files.items():
 if row['origin']=='study'and row['path'].startswith('sources/'):omit.add(key)
for path in ['reboot_20261013/L044_principal_distinct/source-1.png','reboot_20261013/L044_principal_distinct/source-2.png','reboot_20261013/L044_principal_distinct/source_required_pages.pdf','reboot_20261013/L044_general_imprimitive_root_work/source_7_9.txt']:omit.add(('study',path))
# Index already-published exact payloads, including losslessly compressed logs.
existing={};tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');needed={(r['bytes'],r['sha256'])for key,r in files.items()if key not in omit}
for rel in tracked:
 if not rel.endswith('/transport.json'):continue
 try:old=json.loads((R/rel).read_text())
 except (ValueError,OSError):continue
 for row in old.get('files',[]):
  if all(k in row for k in ['bytes','sha256','public_path','encoding','stored_bytes','stored_sha256']):existing.setdefault((row['bytes'],row['sha256']),{k:row[k]for k in ['public_path','encoding','stored_bytes','stored_sha256']})
sizes={v[0]for v in needed}
for rel in tracked:
 if not rel:continue
 p=R/rel
 if p.is_file()and p.stat().st_size in sizes:
  key=(p.stat().st_size,sha(p))
  if key in needed:existing.setdefault(key,dict(public_path=rel,encoding='identity',stored_bytes=key[0],stored_sha256=key[1]))
rows=[]
for key,row in sorted(files.items()):
 r=dict(row);ident=(r['bytes'],r['sha256'])
 if key in omit:r['transport']='SOFTWARE_DOCUMENTATION_HASH_ONLY'if r['origin']=='local_software_documentation'else'PRIVATE_PRIMARY_SOURCE_HASH_ONLY'
 elif ident in existing:
  e=existing[ident];p=R/e['public_path'];need(p.is_file()and p.stat().st_size==e['stored_bytes']and sha(p)==e['stored_sha256'],'Changed public copy');r.update(transport='EXISTING_PUBLIC',**e)
 else:r['transport']='NEW_FROZEN_FILE'
 need(not r['path'].endswith('.md'),'Unexpected Markdown');rows.append(r)
report=dict(status='PRIVATE_L044_TRANSPORT_INVENTORY_NOT_ADMISSION',files=rows,packets=j['packets'],logical_files=len(rows),missing_final_reviews=[],primary_sources_hash_only=[{'origin':r['origin'],'path':r['path']}for r in rows if r['transport'].endswith('HASH_ONLY')],historical_documentary_exceptions=exceptions,relative_locator_resolutions=resolutions,legacy_common_aliases=json.loads((S/'reboot_20261013/L044_binary_one_neighbour_distinct/legacy_locator_map.json').read_text()),
 closure_boundary='All recursively acquired L044 author/review packets and exact direct inputs; complete prior public L038 and L071 transports. Other acquired complete frozen editions retain all author exports and their selected embedded predecessors, not arbitrary historical measurement catalogue expansion.',
 predecessor_transports=[pin(R/f'audit/recoveries/{x}/v1/transport.json')for x in ['L038','L071']],
 discovery_sha256=sha(D),new_uncompressed_bytes=sum(r['bytes']for r in rows if r['transport']=='NEW_FROZEN_FILE'),existing_public_logical_files=sum(r['transport']=='EXISTING_PUBLIC'for r in rows),new_logical_files=sum(r['transport']=='NEW_FROZEN_FILE'for r in rows),source_assets_exported=False,private_runtime_fallback=False,whole_original_credit=0,markdown_transport='No Markdown payloads.',primary_omission_addendum='Exact source PDFs/excerpts and source render pages are documentary only. Separate enumerated historical native PNG caches and installed software are not proof/certificate payloads.')
need(any(r['path']=='corpus106_L044_principal_root_adoption/manifest.json'for r in rows),'Missing root acceptance')
p=W/'inventory01.json';need(not p.exists(),'Fresh inventory');p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k]for k in ['logical_files','new_uncompressed_bytes','existing_public_logical_files','new_logical_files']}));print(json.dumps({'packets':len(j['packets']),'exceptions':len(exceptions),'exception_kinds':dict(collections.Counter(x['kind']for x in exceptions)),'relative_locators':len(resolutions)}))
