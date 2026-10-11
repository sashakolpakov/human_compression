#!/usr/bin/env python3
"""Bounded independent integration checks; no PDF, GAP or Lean replay."""
import ast, copy, hashlib, importlib.util, json, subprocess
from pathlib import Path
ROOT=Path('/Users/sasha/medusa/math_compression')
PRIVATE=Path('/Users/sasha/medusa/research/leemans/topic_A_dag_publication')
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,message):
 if not x:raise ValueError(message)
def load(p):return json.loads(p.read_text())
source=ROOT/'scripts/verify_snapshot.py'
old=subprocess.check_output(['git','show','0d5e3c5:scripts/verify_snapshot.py'],cwd=ROOT).decode()
current=source.read_text()
of={n.name:n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef)}
nf={n.name:n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)}
same=lambda a,b:ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
unchanged=[]
for key in of:
 if key not in ('main','check_topic_a_measurement'):
  need(same(of[key],nf[key]),'Changed prior check '+key);unchanged.append(key)
need(set(nf)-set(of)=={'check_topic_a_dag'},'Unexpected function addition/removal')
a,b=of['check_topic_a_measurement'].body,nf['check_topic_a_measurement'].body
need(len(b)==len(a)+3 and all(same(x,y) for x,y in zip(a[:-1],b[:len(a)-1])) and same(a[-1],b[-1]),'Old numerical checks not preserved')
filtered=[]
for node in nf['main'].body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='a_dag_cells' for t in node.targets):continue
 if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id=='print' and 'Topic A paired proof graphs preserve' in ast.unparse(node):continue
 filtered.append(node)
need(len(filtered)==len(of['main'].body) and all(same(x,y) for x,y in zip(filtered,of['main'].body)),'Previous main flow changed')
spec=importlib.util.spec_from_file_location('reviewed_snapshot',source); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
need(module.check_topic_a_dag()==140,'Expected all 140 graph document cells')
need(module.check_topic_a_measurement()==(420,300),'Expected retained numerical and new reader checks')
prefix='audit/topic-a/v2/dag/'
admission=load(ROOT/'audit/topic-a/v2/dag_admission.json');revision=load(ROOT/(prefix+'publication_revision.json'))
need(len(admission['artifacts'])==73,'Current artifacts')
need({r['path'] for r in admission['artifacts']}=={str(p.relative_to(ROOT)) for p in (ROOT/prefix).rglob('*') if p.is_file()},'Unbound/missing current packet file')
mapping=load(PRIVATE/'publication_map.json')['files'];differences=[]
for row in mapping:
 left=PRIVATE/row['private_path'];right=ROOT/row['public_path']
 if left.read_bytes()!=right.read_bytes():differences.append(row['public_path'].removeprefix(prefix))
need(sorted(differences)==sorted(r['path'] for r in revision['changed_artifacts']), 'Undeclared copy difference')
for r in revision['changed_artifacts']:
 oldpath=PRIVATE/(('visual/'+r['path']) if r['path'] in ('view_data.json','explorer.html') else r['path'])
 newpath=ROOT/(prefix+r['path'])
 need(sha(oldpath)==r['frozen_original_sha256'] and len(oldpath.read_bytes())==r['frozen_original_bytes'],'Old adaptation hash')
 need(sha(newpath)==r['sha256'] and len(newpath.read_bytes())==r['bytes'],'Current adaptation hash')
old_status=revision['old_review_status'];new_status=revision['current_review_status']
for name in ('render.py','visual/view_data.json','visual/explorer.html'):
 a=(PRIVATE/name).read_text();b=(ROOT/(prefix+name.removeprefix('visual/'))).read_text()
 need(a.count(old_status)==1 and a.replace(old_status,new_status)==b,'Not literal status-only replacement '+name)
old_data=load(PRIVATE/'visual/view_data.json');new_data=load(ROOT/(prefix+'view_data.json'))
need(old_data.pop('review_status')==old_status and new_data.pop('review_status')==new_status and old_data==new_data,'Payload changed beyond status')
controls=[];original_load=module.load
def reject(name,path,edit,fn=module.check_topic_a_dag):
 changed=copy.deepcopy(original_load(path));edit(changed)
 def altered(p):return copy.deepcopy(changed) if p==path else original_load(p)
 module.load=altered
 try:
  try:fn()
  except (ValueError,KeyError,IndexError):controls.append(name)
  else:raise ValueError('Negative control accepted '+name)
 finally:module.load=original_load
w=prefix+'inputs/weighted/weights.json';p=prefix+'inputs/weighted/partition.json';g=prefix+'inputs/logical/logical_graph.json'
reject('unreviewed_DAG','audit/topic-a/v2/dag_admission.json',lambda d:d.update(status='PENDING'))
reject('document_omitted',p,lambda d:d['documents'].pop('A6'))
reject('owner_weight_lost',w,lambda d:d['owner_weights']['code.appendix']['NFC'].update(characters_without_whitespace=0))
reject('partition_gap',p,lambda d:d['documents']['A1']['spans'][1].update(start=d['documents']['A1']['spans'][1]['start']+1))
reject('trailing_text_omitted',p,lambda d:d['documents']['A1'].update(selected_calibrated_codepoints=d['documents']['A1']['selected_calibrated_codepoints']+1))
reject('foreign_owner',p,lambda d:d['documents']['A1']['spans'][0].update(node='code.appendix'))
reject('new_graph_node',g,lambda d:d['nodes'].append(copy.deepcopy(d['nodes'][0])))
reject('node_count_ratio',w,lambda d:d.update(raw_node_count_ratio=12))
reject('external_cost_zero',w,lambda d:d['unknown_costs'].update(diagram_structure=0))
reject('raw_and_appendix_double_charge',w,lambda d:d['program_representation'].update(raw_file_metrics_are_alternative_not_additional=False))
reject('reader_different_measurement','audit/topic-a/v2/measurement/reader_admission.json',lambda d:d.update(numerical_admission_sha256='0'*64),module.check_topic_a_measurement)
reject('changed_frozen_UI_hash','audit/topic-a/v2/dag_admission.json',lambda d:d['artifacts'][0].update(sha256='0'*64))
report={'status':'PASS_BOUNDED_INDEPENDENT_INTEGRATION','baseline':'0d5e3c5','verifier_sha256':sha(source),'unchanged_prior_functions':unchanged,'old_numerical_checks_preserved':True,'prior_main_flow_preserved':True,'current_DAG_document_cells':140,'retained_measurement_dimensions':[420,300],'exact_current_artifact_bindings':73,'declared_status_only_files':differences,'payload_equal_except_review_status':True,'negative_controls_rejected':controls,'public_files_written':False,'PDF_census_Lean_replayed':False}
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
