"""Explicit same-byte locator completion; no mathematical file is omitted."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
from pathlib import Path
import collections,hashlib,json
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression'
def pin(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def need(c,m):
 if not c:raise ValueError(m)
j=json.loads((W/'closure_initial.json').read_text());files={(r['origin'],r['path']):r for r in j['files']};byhash=collections.defaultdict(list)
for r in files.values():byhash[r['sha256']].append(r)
resolved=[];remaining=[]
for x in j['issues']:
 r=x['pin'];h=r['sha256'];context=x['context']
 if context=='manifest export':
  target=Path(x['logical']);parts=target.relative_to(R).parts;need(parts[:2]==('audit','recoveries'),'Expected public recovery alias');original=parts[2];hits=[]
  for p in sorted((R/'papers/recoveries'/original).rglob(Path(r['path']).name)):
   if p.is_file()and pin(p)=={k:r[k]for k in('bytes','sha256')}:hits.append(p)
  need(hits,'Missing actual scientific public export '+str(target));p=hits[0];rel=str(p.relative_to(R));key=('public',str(target.relative_to(R)))
  files[key]={'origin':'public','path':key[1],'source_origin':'public','source_path':rel,**pin(p),'transport':'NEW_FROZEN_FILE'}
  source=('public',rel)
  if source not in files:files[source]={'origin':'public','path':rel,'source_origin':'public','source_path':rel,**pin(p),'transport':'NEW_FROZEN_FILE'}
  resolved.append({'context':context,'historical_pin':{'path':str(target),**pin(p)},'resolved_origin':'public','resolved_path':rel,'logical_alias':{'origin':'public','path':key[1]},'reason':'The accepted publication places the identical manuscript in papers rather than the historical author subdirectory.'})
 elif context=='JSON export alias needs explicit context':
  p=Path(x['actual']);need(pin(p)=={k:r[k]for k in('bytes','sha256')},'Public provenance alias');origin='study'if p.is_relative_to(S)else'public';rel=str(p.relative_to(S if origin=='study'else R))
  resolved.append({'context':context,'historical_pin':{'path':x['logical'],**pin(p)},'resolved_origin':origin,'resolved_path':rel,'reason':'Byte-identical provenance export at an accepted public boundary; its original complete manifest is acquired separately. No new private theorem depends on recursively reinterpreting this public historical metadata.'})
 else:
  candidates=[a for a in byhash[h]if r.get('bytes',a['bytes'])==a['bytes']]
  need(candidates,'No exact locator '+str(x));candidates.sort(key=lambda a:(Path(a['path']).name!=Path(r['path']).name,len(a['path']),a['path']));a=candidates[0]
  resolved.append({'context':context.removeprefix(str(S)+'/'),'historical_pin':r,'resolved_origin':a['origin'],'resolved_path':a['path'],'reason':'Exact byte identity resolves the historical relative working directory; no code, input or receipt is edited.'})
j['files']=list(files.values());j['relative_locator_resolutions']+=resolved;j['issues']=[];j['initial_issue_count']=len(resolved);j['public_boundary']='Existing declared public proof/review payloads and their admissions are acquired exactly; historical public measurement/admission metadata is not recursively re-admitted.'
(W/'closure_resolved.json').write_text(json.dumps(j,indent=2)+'\n');(W/'locator_resolution_report.json').write_text(json.dumps({'status':'PASS_ALL_EXACT_LOCATORS','issues':len(resolved),'remaining':remaining,'resolutions':resolved},indent=2)+'\n')
print(json.dumps({'files':len(files),'packets':len(j['packets']),'resolved':len(resolved),'remaining':0}))
