from pathlib import Path
import datetime,gzip,hashlib,json,shutil,ast
W=Path(__file__).resolve().parent;S=W.parents[1];P=W/'four_rows_work';O=W/'four_rows_author02';D=S/'corpus106_L120_four_rows_v1'
def need(b,s):
 if not b:raise ValueError(s)
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,base):
 b=p.read_bytes();return dict(path=str(p.relative_to(base)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
report=json.loads((O/'report.json').read_text());need(report['status']=='PASS_FOUR_COMPLETE_FINITE_ROWS','full common wrapper completed')
need(report['tuples']==94354 and report['interval_checks']==150173,'exact totals')
need(not D.exists(),'immutable destination absent')
# Explicit final driver and family controls; no enumeration or subgroup replay.
controlled=[]
for row in json.loads((P/'roster.json').read_text()):
 n,kind,limit=[row[k]for k in ['degree','kind','rank_limit']]
 for b in row['branches']:
  Q=P/row['key']/'branches'/b['name'];r=json.loads((Q/'report.json').read_text())
  expected=f'degree:={n};;rankLimit:={limit};;\nrootTranspositions:={b["spec"]["branch"]};;\nRead('+json.dumps(r['engine']['path'])+');\n'
  need((Q/'driver.g').read_text()==expected,'literal driver scope')
  controlled.append(dict(branch=b['name'],exact_driver=True,source_engine_sha256=r['engine']['sha256']))
# Only marker/description changed in the rooted canonical functions.
def funcs(p):
 return {x.name:ast.dump(x,include_attributes=False)for x in ast.parse(p.read_text()).body if isinstance(x,ast.FunctionDef)}
a=funcs(W/'canonical_symmetric_intervals.py');b=funcs(P/'canonical.py')
need(all(a[x]==b[x]for x in ['rooted','key','need']),'literal canonical mathematical functions unchanged')
save(P/'final_integration_controls.json',dict(status='PASS_FINAL_BINDINGS_AND_DRIVER_SCOPE',branches=controlled,rooted_key_ast_unchanged=True,source_images_added_after_replay_start=2,scientific_rerun=False))
# Recheck all final dependencies, including the two freshly viewed documentary images.
for x in json.loads((P/'dependencies.json').read_text()):
 p=S/x['path'];q=pin(p,S);need(all(q[k]==x[k]for k in ['bytes','sha256']),'final binding '+x['path'])
I=P/'author_integration';I.mkdir()
for f in sorted(O.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(O)
 if f.name=='input.g':continue
 target=I/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if f.name=='validation.stdout':target.with_suffix('.stdout.gz').write_bytes(gzip.compress(f.read_bytes(),compresslevel=6,mtime=0))
 else:shutil.copy2(f,target)
save(I/'derived_inputs.json',dict(policy='Each input.g is deterministically reconstructed from the complete frozen transcripts by check.py, so its large plaintext is not duplicated. Exact fresh hashes follow.',files=[pin(p,O)for p in sorted(O.glob('*/input.g'))]))
for f in ['rows.pdf','rows.log']:shutil.copy2(O/'native'/f,P/f)
shutil.copy2(O/'native/text.txt',P/'native_expected.txt')
visual=json.loads((P/'visual_record.json').read_text());need((O/'native/viewed.json').exists(),'all native pages explicitly viewed');visual['native']=json.loads((O/'native/viewed.json').read_text());visual['native_direct_view_pending']=False;save(P/'visual_record.json',visual)
dev=json.loads((P/'development.json').read_text());dev['status']='ALL_COMPLETE_CENSUSES_AND_FINAL_COMMON_REPLAY_PASSED';dev['native_pages']=report['native_pages'];dev['new_common_wrapper_session']=12912;dev['final_integration_controls']='final_integration_controls.json';save(P/'development.json',dev)
shutil.copy2(Path(__file__),P/'history/freeze_four_rows.py')
shutil.copytree(P,D,ignore=shutil.ignore_patterns('__pycache__','*.aux','*.out'))
exports=[pin(p,D)for p in sorted(D.rglob('*'))if p.is_file()]
save(D/'manifest.json',dict(schema='frozen-proof-packet-v1',status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports))
print(json.dumps(dict(manifest=pin(D/'manifest.json',S),exports=len(exports),bytes=sum(x['bytes']for x in exports))))
cp=json.loads((W/'checkpoint22.json').read_text());cp['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();cp['live']=[];cp['terminal'].append(dict(session=12912,status='Final four-row wrapper PASS; all94354 tuples,150173intervals,8damages,4optimization guards, allnativepages viewed'));cp['four_rows_author']=pin(D/'manifest.json',S);cp['next']=['Root distinct review of final21-cell component; no ledger change until acceptance','Distinct review of L045 symplectic upper v1','L120 principal final assembly after numeric component acceptance'];save(W/'checkpoint23.json',cp);print(json.dumps(pin(W/'checkpoint23.json',S)))
