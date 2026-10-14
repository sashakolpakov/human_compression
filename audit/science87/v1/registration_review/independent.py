from pathlib import Path
import argparse,ast,collections,difflib,hashlib,json,re,subprocess
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--git-repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=a.repo.resolve();g=a.git_repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
base='ade9feeb7f8feaffa8f773932d57a50e60cb64c2';aud=r/'audit/science87/v1';ids={'L027','L036','L046','L063','L064','L076'};ordinary={'L027','L076'}
def need(x,m):
 if not x:raise ValueError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def before(path):return subprocess.check_output(['git','show',base+':'+path],cwd=g)
def oldjson(path):return json.loads(before(path))
def j(path):return json.loads((r/path).read_text())
old=oldjson('audit/corpus/latest.json');new=j('audit/corpus/latest.json');hist=json.loads((aud/'history_routes.json').read_text());pins=[]
need(hist['baseline_commit']==base,'history baseline')
for name,x in hist['routes'].items():
 b=before(name);saved=(r/x['path']).read_bytes();need(b==saved,'exact archived Git bytes '+name);pins.append(dict(path=name,sha256=sha(b),bytes=len(b)))
oldsrc=before('scripts/verify_snapshot.py').decode();newsrc=(r/'scripts/verify_snapshot.py').read_text();oldtree=ast.parse(oldsrc);newtree=ast.parse(newsrc)
def funs(t,s):return {x.name:(ast.dump(x,include_attributes=False),ast.get_source_segment(s,x))for x in t.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))and x.name!='main'}
of=funs(oldtree,oldsrc);nf=funs(newtree,newsrc)
need(set(nf)-set(of)=={'check_previous_science87','check_science87'},'only two new functions')
need(all(nf[k]==v for k,v in of.items()),'all old functions text and AST identical')
need(len(of)==203,'actual old function count')
for key,added in [('admitted_original_ids',ordinary),('refuted_principal_original_ids',ids-ordinary),('handled_mathematical_original_ids',ids)]:
 need(len(new[key])==len(set(new[key])) and set(new[key])==set(old[key])|added and not(set(old[key])&added),'exact additive roster '+key)
need(set(old['accessible_pending_original_ids'])-set(new['accessible_pending_original_ids'])==ids and set(new['accessible_pending_original_ids'])<=set(old['accessible_pending_original_ids']),'pending difference')
need(new['measured_original_ids']==old['measured_original_ids']and len(new['measured_original_ids'])==53,'measurements unchanged')
parts=[set(new[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']]
need([len(x)for x in parts]==[87,9,9,1]and len(set.union(*parts))==106 and sum(map(len,parts))==106,'independent partition')
need(set(new['measurement_pending_original_ids'])==set(old['measurement_pending_original_ids'])|ordinary and len(new['measurement_pending_original_ids'])==34,'unmeasured roster')
oldcat=oldjson(old['active_catalogue']['path']);newcat=j(new['active_catalogue']['path']);oa={x['original_id']:x for x in oldcat['entries']};na={x['original_id']:x for x in newcat['entries']}
need(set(oa)==set(na)and len(oa)==106,'same source IDs')
need({k for k in oa if oa[k]!=na[k]}==ids,'only six catalogue rows changed')
scopes=[]
for sid in sorted(ids):
 z=na[sid]['current_principal_recovery'];need(z['historical_admission_evidence']==oa[sid]['current_principal_recovery'],'old row preserved '+sid)
 need(z['original_fully_handled']is(sid in ordinary),'ordinary-only fully handled '+sid)
 need(z['principal_contract_admitted']is(sid in ordinary)and z['complete_principal_contract_recovered']is(sid in ordinary),'principal admission kind '+sid)
 need(z['measured']is False and z['compression_factor']is None and z['all_original_assertions_claimed']is False and z['whole_source_formalized']is False,'no extra claims '+sid)
 path='audit/'+('recoveries/'if sid in ordinary else'principal-refutations/')+sid+'/v1/admission.json';ad=j(path)
 need(ad['source_ids']==[sid]and ad['ordinary_recovery_credit']==int(sid in ordinary)and ad['principal_refutation_credit']==int(sid not in ordinary),'one correct credit per source')
 need(ad['new_measurements']==ad['new_question_credit']==ad['new_Lean_declarations']==0,'zero unrelated credit')
 if sid not in ordinary:need(ad['all_other_valid_source_claims_recovered']is False,'remaining source claims not recovered')
 scopes.append(dict(source_id=sid,admission=path,kind=ad['disposition_kind'],scope_note=ad['scope_note']))
# Independent exact native catalogue suffix inventory, including a single shared plane manuscript.
volumes=[];native_counts={}
for name,added in [('papers/catalogue_corrected_unmeasured.json',ordinary),('papers/catalogue_principal_refutations.json',ids-ordinary)]:
 o=oldjson(name);n=j(name);need(n['entries'][:len(o['entries'])]==o['entries'],'old native list intact')
 extra=n['entries'][len(o['entries']):];need(set(n['original_ids'])-set(o['original_ids'])==added,'native IDs')
 for row in extra:
  need(set(row['source_ids'])<=added,'native source scope');need(row['measured']is False and row['compression_factor']is None,'native no measurement')
  for f in ['tex','pdf']:need((r/row[f]).is_file(),'native artifact '+row[f])
  need(not re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(r/row['tex']).read_text())and not row['tex_inputs'],'this roster has no omitted adjacent TeX inputs')
  volumes.append(dict(id=row['id'],sources=row['source_ids'],pages=row['physical_pages'],tex=row['tex'],pdf=row['pdf']))
 native_counts[name]=len(extra)
need(len(volumes)==14 and sum(x['pages']for x in volumes)==53,'14 unique manuscripts/53 retained pages')
need(sum(x['pages']for x in volumes if x['sources']==['L027'])==34,'all L027 pages')
need(sum(x['sources']==['L063','L064']for x in volumes)==1,'one shared plane proof')
# Only newly added literal local RST link targets, independent of narrative parameters.
links=[];diffs={}
for name in ['README.rst','audit/completion.rst','audit/protocol.tex','scripts/verify_snapshot.py']:
 b=before(name).decode();n=(r/name).read_text();diffs[name]=''.join(difflib.unified_diff(b.splitlines(True),n.splitlines(True),fromfile='baseline/'+name,tofile='candidate/'+name))
 if name.endswith('.rst'):
  oldlinks=set(re.findall(r'<([^<>]+)>`_',b,re.S));newlinks=set(re.findall(r'<([^<>]+)>`_',n,re.S))
  for target in sorted(newlinks-oldlinks):
   target=''.join(target.split())
   if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:',target)or target.startswith('#'):continue
   p=(r/name).parent/target.split('#',1)[0];need(p.exists(),'new RST link exists '+name+' '+target);links.append(dict(from_path=name,target=target))
for name,text in diffs.items():(out/(name.replace('/','__')+'.diff')).write_text(text)
report=dict(status='PASS_INDEPENDENT_SCIENCE87_REGISTRATION',baseline=base,archived_git_files=pins,unchanged_old_function_AST_and_text=len(of),source_changes=sorted(ids),counts=dict(recoveries=87,principal_refutations=9,pending=9,editorial=1,measured=53,unmeasured_recoveries=34),scopes=scopes,manuscripts=volumes,native_additions=native_counts,new_local_links=links,no_math_replay=True,no_public_writes=True)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'old_functions':len(of),'manuscripts':len(volumes),'pages':sum(x['pages']for x in volumes),'new_links':len(links)}))
