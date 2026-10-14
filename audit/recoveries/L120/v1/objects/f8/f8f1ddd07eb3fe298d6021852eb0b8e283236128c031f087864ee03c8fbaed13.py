from pathlib import Path
import gzip,hashlib,json,shutil,difflib
W=Path(__file__).resolve().parent;S=W.parents[1];F=W/'finite_rows_work';P=W/'four_rows_work'
def need(b,s):
 if not b:raise ValueError(s)
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,path=None):
 b=p.read_bytes();return dict(path=path or str(p.relative_to(S)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not P.exists(),'fresh stage');P.mkdir()
roster=[('s12','symmetric',12,7,range(1,7),'s12_complete01'),('s13','symmetric',13,7,range(1,7),'s13_complete01'),('s14','symmetric',14,8,range(1,8),'fixed_rows05'),('a15','even',15,7,[2,4,6],'fixed_rows05')];rows=[];plans=[]
for key,kind,n,limit,branches,run in roster:
 V=W/f'{key}_interval_validation';Q=P/key;Q.mkdir();B=Q/'branches';B.mkdir();records=[]
 for i in branches:
  name=f'{kind}{n}_part{i}';src=F/run/name;dst=B/name;dst.mkdir();r=json.loads((src/'report.json').read_text());need(r['status']=='COMPLETE_FIXED_BRANCH','complete branch')
  raw=(src/'stdout.log').read_bytes();need(hashlib.sha256(raw).hexdigest()==r['stdout']['sha256'],'receipt bytes')
  (dst/'stdout.log.gz').write_bytes(gzip.compress(raw,compresslevel=6,mtime=0))
  for f in ['report.json','result.json','driver.g','stderr.log']:shutil.copy2(src/f,dst/f)
  records.append(dict(name=name,spec=r['spec'],cap_seconds=r['cap_seconds'],original_stdout=r['stdout'],original_report=pin(src/'report.json'),original_driver=pin(src/'driver.g')))
  print('PACKED',name,flush=True)
 phase=Q/'author_positive';phase.mkdir()
 for f in ['receipt.json','validation_receipt.json','extraction.json','driver.g','validate.g','canonical.py','validation.stderr','canonical.stdout','canonical.stderr']:
  if(V/f).exists():shutil.copy2(V/f,phase/f)
 (phase/'validation.stdout.gz').write_bytes(gzip.compress((V/'validation.stdout').read_bytes(),compresslevel=6,mtime=0))
 shutil.copy2(V/'canonical_report.json',Q/'expected.json')
 shutil.copy2(F/f'{key}_enumeration_summary01.json',Q/'enumeration_summary.json')
 save(Q/'plan.json',dict(runs=[dict(name=x['name'],spec=x['spec'],cap_seconds=x['cap_seconds'])for x in records]))
 rows.append(dict(key=key,kind=kind,degree=n,rank_limit=limit,branches=records,author_input=pin(V/'input.g'),author_receipt=pin(V/'receipt.json'),new_cells=list(range(3,limit+1))))
save(P/'roster.json',rows)
for name in ['validate_symmetric_intervals.g','canonical_symmetric_intervals.py']:shutil.copy2(W/name,P/('predecessor_'+name))
validator=(W/'validate_symmetric_intervals.g').read_text().replace('G:=SymmetricGroup(degree);;checks:=0;;count:=0;;','if kind="symmetric" then G:=SymmetricGroup(degree);elif kind="even" then G:=AlternatingGroup(degree);else Error("fixed group kind");fi;;checks:=0;;count:=0;;').replace('COMPLETE_SYMMETRIC_INTERVAL_VALIDATION','COMPLETE_FINITE_INTERVAL_VALIDATION')
(P/'validate.g').write_text(validator)
canonical=(W/'canonical_symmetric_intervals.py').read_text().replace('COMPLETE_SYMMETRIC_INTERVAL_VALIDATION','COMPLETE_FINITE_INTERVAL_VALIDATION').replace('PASS_LITERAL_SYMMETRIC_INTERVAL_CLASSES','PASS_LITERAL_FINITE_INTERVAL_CLASSES').replace('natural symmetric target and rank interval','natural target and rank interval')
(P/'canonical.py').write_text(canonical)
for name,a,b in [('validator',W/'validate_symmetric_intervals.g',P/'validate.g'),('canonical',W/'canonical_symmetric_intervals.py',P/'canonical.py')]:
 (P/(name+'_delta.diff')).write_text(''.join(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile=str(a),tofile=str(b))))
by={x['path']:x for x in json.loads((S/'corpus106_L120_s11_v1/dependencies.json').read_text())}
acquired=['corpus106_L120_s11_v1','corpus106_L120_s11_root_review','corpus106_L120_interval_validator_v1','corpus106_L120_interval_validator_root_review','corpus106_L019_principal_v1','corpus106_L019_principal_independent_review','corpus106_L019_principal_root_adoption','corpus106_L044_principal_v1','corpus106_L044_principal_independent_review','corpus106_L044_principal_root_adoption']
for name in acquired:
 D=S/name;manifest=json.loads((D/'manifest.json').read_text())
 for e in [dict(path='manifest.json'),*manifest['exports']]:
  x=pin(D/e['path']);by[x['path']]=x
 # Direct acquired bindings remain exactly indexed; their proof dependencies are preserved in the acquired packets.
 if (D/'dependencies.json').exists():
  data=json.loads((D/'dependencies.json').read_text());deps=data if isinstance(data,list)else data.get('bindings',data.get('files',[]))
  for x in deps:
   if x.get('root','private_study')=='private_study' and x.get('namespace','study')=='study' and (S/x['path']).exists():
    y=pin(S/x['path']);need(y['bytes']==x['bytes']and y['sha256']==x['sha256'],'acquired exact bytes');by[y['path']]=y
for p in [S/'sources/survey2021.pdf',W/'survey-final.tex']:
 x=pin(p);by[x['path']]=x
save(P/'dependencies.json',sorted(by.values(),key=lambda x:x['path']))
save(P/'acquired_packets.json',[pin(S/n/'manifest.json')for n in acquired])
H=P/'history';H.mkdir()
for name in ['prepare_s13_intervals01.py','prepare_s13_intervals02.py','run_interval_rows01.py','run_a15_intervals01.py','run_s13_intervals01.py']:
 shutil.copy2(W/name,H/name)
shutil.copytree(W/'s13_interval_preparation_failed01',H/'failed_s13_extraction')
for name in ['run_accepted_plan_v4.py','run_accepted_plan_v5.py','s12_plan01.json','s13_plan01.json']:
 if(F/name).exists():shutil.copy2(F/name,H/name)
print('READY',len(by),'bindings',sum(len(x['branches'])for x in rows),'branches',flush=True)
