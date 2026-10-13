from pathlib import Path
import hashlib,json,re,shutil,sys,collections
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;S=W.parent.parent;C=W/'principal_component';C.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
deps={}
def pin(p,role):
 p=p.resolve();need(p.is_file(),str(p));key=str(p)
 if key not in deps:deps[key]={'path':key,'bytes':p.stat().st_size,'sha256':sha(p),'role':role}
 return key
# Index executable workers by exact receipt hash. Witness files are not workers.
workerfolders=['cubic_workers','cubic_2048_workers','cubic_2048_fast_workers','descent_workers','cutoff_workers','subdivision_workers','nonbipartite_subdivision_workers','nonbipartite_retry01','nonbipartite_retry02','subdivision_actual_transition/workers_old']
workers=collections.defaultdict(list)
for folder in workerfolders:
 for p in (W/folder).glob('*.g'):
  if folder.startswith('nonbipartite_retry') and p.name!='worker.g':continue
  workers[sha(p)].append(p)
# The cutoff directory name is retained from the actual preparation.
for p in W.rglob('*.g'):
 if 'workers' in str(p.parent.relative_to(W)) or p.name.endswith('.worker.g'):
  if p not in workers[sha(p)]:workers[sha(p)].append(p)
q=json.loads((W/'quartic_census_scope_corrected_summary.json').read_text())
c=json.loads((W/'cubic_scopes_summary.json').read_text())
rows=[]
for family,data in [('quartic',q),('symmetric',c['symmetric_2048']),('semisymmetric',c['semisymmetric_768']),('subdivision',c['subdivisions_2048'])]:
 for row in data['rows']:
  p=W/row['certificate'];need(sha(p)==row['sha256'],'witness '+str(p));pin(p,'complete permutation witness')
  r={'family':family,'graph':row['graph'],'witness':str(p.relative_to(W)),'witness_sha256':sha(p),'markings':row['markings'],'max':row['max'],'norm':row['norm'],'reverse_parts_for_table':family=='quartic' and row['graph']=='128_055'}
  rp=p.with_suffix('.receipt.json')
  if rp.exists():
   receipt=json.loads(rp.read_text());need(receipt['status']=='PASS' and receipt['returncode']==0,'receipt '+str(rp));need(receipt['witness_sha256']==sha(p),'receipt witness')
   r['receipt']=str(rp.relative_to(W));pin(rp,'completed receipt')
   for ext in ['stdout','stderr']:
    f=(p.parent/(ext+'.log')) if p.parent.name.startswith('nonbipartite_retry') else p.with_suffix('.'+ext);need(sha(f)==receipt[ext+'_sha256'],'process output');pin(f,'completed process output');r[ext]=str(f.relative_to(W))
   need(not (W/r['stderr']).read_text().strip(),'nonempty completed stderr')
   matches=workers[receipt['script_sha256']];need(matches,'missing actual worker for '+str(p))
   chosen=sorted(matches,key=lambda x:('workers_old' not in str(x),len(str(x))))[0]
   r['worker']=str(chosen.relative_to(W));r['worker_sha256']=pin(chosen,'exact completed worker') and sha(chosen)
   if 'nauty_input_sha256' in receipt:
    oracle=W/'cubic_2048_nauty'/(row['graph']+'.json');need(sha(oracle)==receipt['nauty_input_sha256'],'nauty pin');pin(oracle,'full automorphism oracle and generators');r['oracle']=str(oracle.relative_to(W))
   if 'oracle_sha256' in receipt:
    oracle=p.parent/'oracle.json';need(sha(oracle)==receipt['oracle_sha256'],'retry oracle');pin(oracle,'full automorphism oracle and generators');r['oracle']=str(oracle.relative_to(W))
   if 'basis_sha256' in receipt:
    basis=W/json.loads((W/'subdivision_markings/basis.json').read_text())[row['graph']]
    need(sha(basis)==receipt['basis_sha256'],'subdivision basis');pin(basis,'acquired complete subgroup classification');r['basis']=str(basis.relative_to(W))
   if 'prior_capped_receipt' in row:
    old=W/row['prior_capped_receipt'];need(sha(old)==receipt['prior_capped_receipt_sha256'],'cap link');pin(old,'prior cap with no conclusion');r['prior_capped_receipt']=str(old.relative_to(W))
    for ext in ['stdout','stderr']:
     f=old.parent/(row['graph']+'.'+ext);pin(f,'prior capped process output')
  else:
   done=p.with_suffix('.done');need(done.is_file(),'missing old completion token');m=re.fullmatch(r'COMPLETE '+re.escape(row['graph'])+r' (\d+) (\d+)\n',done.read_text());need(m and int(m[1])==row['markings'],'old completion token')
   pin(done,'old per-graph terminal completion token');r['done']=str(done.relative_to(W));r['worker']='current_c4_census.g';r['worker_sha256']=sha(W/r['worker']);pin(W/r['worker'],'old complete subgroup-class producer')
  rows.append(r)
need(len(rows)==1950 and sum(r['markings'] for r in rows)==4254,'aggregate scope')
# Whole-source structural and primary interfaces, not every exploratory artifact.
names=['CAT_lcf.txt','CSS_lcf.txt','foster_primary.html','sage_smallgraphs_source.py','cubic_2048_bipartite.json','cubic_2048_nonbipartite.json','cubic_markings/inputs.json','current_c4_150_bipartite.json','current_c4_census_scope.json','quartic_census_scope_corrected_summary.json','cubic_scopes_summary.json','verify_cubic_sources.py','cubic_source_verification.json','cubic_source_verification.stdout','cubic_source_verification.stderr','summarize_cubic_scopes.py','summarize_quartic.py','maximal_descent.g','maximal_descent_arcs.g','subdivision_markings.g','subdivision_actual_actions.g','current_c4_census.stdout','current_c4_census.stderr','named_examples_check.g','named_examples_check.stdout','named_examples_check.stderr','named_examples_development.json','exception_witnesses.g','exception_census.g','exception_census.stdout','exception_census.stderr','mathieu_witness_9.g','mathieu_Q8_complement.g','mathieu_432_complements.g','final_and_foster_web_receipt.json','final_edition_scope_web_receipt.json','c4_table_20080505.html.json','c4_table_20141228.html.json','c4_table.html.json','subdivision_markings/basis.json','nonbipartite_subdivisions/queue.json','subdivision_markings/queue.json','source_tables_01.png','source_tables_02.png']
for name in names:pin(W/name,'primary or proof/certificate interface')
for pat in ['prepare_*.py','run_*.py']:
 for p in W.glob(pat):pin(p,'retained producer orchestration')
for folder in ['cubic_engine_transition','subdivision_actual_transition','fast_validation','nonbipartite_retry01','nonbipartite_retry02','subdivision_second_owner']:
 for p in (W/folder).rglob('*'):
  if p.is_file():pin(p,'engine transition or separate validation receipt')
for name in ['phase177_L059_contract.json','phase177_rank_two_graphs.g','phase177_rank_two_validate.g','phase177_evidence/phase177_graph_witnesses.g','phase177_evidence/phase177_rank_two_validate.log','formal/RankTwoMarkedCounterexample.lean','phase177_evidence/RankTwoMarkedCounterexample.log','sources/catalogue_L059.pdf']:
 pin(S/name,'acquired original or prior proof')
accepted=['corpus106_L059_historical_quartic_v1','corpus106_L059_historical_quartic_root_review','corpus106_L059_subdivision_actual_actions_v1','corpus106_L059_subdivision_actual_actions_root_review']
for folder in accepted:
 base=S/folder;pin(base/'manifest.json','accepted bounded component manifest')
 manifest=json.loads((base/'manifest.json').read_text())
 for x in manifest['exports']:
  p=base/x['path'];need(sha(p)==x['sha256'],'acquired export');pin(p,'accepted bounded component export')
 # Retain exact leaf paths declared by the accepted review, without rewriting them.
 for name in ['dependencies.json','bindings.json']:
  if (base/name).exists():
   d=json.loads((base/name).read_text())
   if isinstance(d,list):
    for x in d:
     if isinstance(x,dict) and 'path' in x and Path(x['path']).is_absolute():
      p=Path(x['path']);need(sha(p)==x['sha256'],'accepted binding');pin(p,'acquired bounded component dependency')
for name in ['faithful_markings.tex','faithful_markings.pdf','source_tables.tex','principal_contract.json','verify_cubic_sources.py']:
 shutil.copy2(W/name,C/name)
(C/'census_register.json').write_text(json.dumps(rows,indent=2)+'\n')
(C/'dependencies.json').write_text(json.dumps(sorted(deps.values(),key=lambda x:x['path']),indent=2)+'\n')
(C/'accepted_components.json').write_text(json.dumps([{'path':str(S/f/'manifest.json'),'sha256':sha(S/f/'manifest.json')} for f in accepted],indent=2)+'\n')
print('PREPARED_PRINCIPAL',len(rows),'graphs',len(deps),'dependencies',sum(x['bytes'] for x in deps.values()),'bytes')
