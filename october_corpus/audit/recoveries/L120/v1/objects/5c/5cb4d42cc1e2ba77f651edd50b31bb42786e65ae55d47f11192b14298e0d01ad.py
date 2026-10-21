from pathlib import Path
import hashlib,importlib.util,json,math,re,shutil
W=Path(__file__).resolve().parent;S=W.parents[1];F=W/'finite_rows_work';V=W/'s13_interval_validation'
def need(b,s):
 if not b:raise ValueError(s)
def pin(p):return dict(path=str(p.relative_to(S)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
V.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('accepted',S/'corpus106_L120_finite_method_v1/run_pool.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
counts={str(r):dict(ordered=0,self_dual=0)for r in range(3,8)};ids=[];literal=None;sources=[];reports=[]
for i in range(1,7):
 p=F/'s13_complete01'/f'symmetric13_part{i}';rep=json.loads((p/'report.json').read_text());need(rep['status']=='COMPLETE_FIXED_BRANCH','complete branch')
 raw=(p/'stdout.log').read_bytes();need(hashlib.sha256(raw).hexdigest()==rep['stdout']['sha256'],'raw receipt')
 data=mod.parse(p/'stdout.log',13,'symmetric',7);need(data==json.loads((p/'result.json').read_text()),'exact accepted parse')
 m=re.search(r'INVOLUTIONS_LITERAL\s+(\[.*?\])',raw.decode(),re.S);need(m is not None,'literal array');lit=re.sub(r'\s+','',m[1])
 if literal is None:literal=lit
 else:need(literal==lit,'same literal universe')
 chosen=[x['ids']for x in data['marks']if x['order']==math.factorial(13)];ids.extend(chosen)
 for r in counts:
  for k in counts[r]:counts[r][k]+=data['counts'][r][k]
 sources.append(dict(path=str(p.relative_to(S)),stdout_sha256=rep['stdout']['sha256'],target_marks=len(chosen)))
 reports.append(dict(**pin(p/'report.json'),seconds=rep['elapsed_seconds']))
for r in counts:counts[r]['with_duality']=(counts[r]['ordered']+counts[r]['self_dual'])//2
save(F/'s13_enumeration_summary01.json',dict(status='COMPLETE_ENUMERATION_AWAITING_DISTINCT_REVIEW_AND_ACTUAL_VALIDATION',degree=13,counts=counts,reports=reports,total_seconds=sum(x['seconds']for x in reports)))
(V/'input.g').write_text('degree:=13;;rankLimit:=7;;\nivs:='+literal+';;\nids:='+json.dumps(ids)+';;\n')
shutil.copy2(W/'validate_symmetric_intervals.g',V/'validate.g');shutil.copy2(W/'canonical_symmetric_intervals.py',V/'canonical.py')
(V/'driver.g').write_text('intervalFile:='+json.dumps(str(S/'corpus106_L120_interval_validator_v1/intervals.g'))+';;\ninputFile:='+json.dumps(str(V/'input.g'))+';;\nRead('+json.dumps(str(V/'validate.g'))+');\n')
save(V/'extraction.json',dict(status='PREPARED_WITH_ACCEPTED_INTERVAL_METHOD',degree=13,rank_limit=7,tuples=len(ids),sources=sources,input=pin(V/'input.g')))
runner=(W/'run_interval_rows01.py').read_text().replace('[(12,7),(14,8)]','[(13,7)]').replace('Positive validation; interval-method distinct acceptance pending at launch.','Positive validation; interval method root accepted ab10c8c1.')
(W/'run_s13_intervals01.py').write_text(runner)
print(json.dumps(dict(tuples=len(ids),counts=counts)))
