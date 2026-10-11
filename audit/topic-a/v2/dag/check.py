#!/usr/bin/env python3
"""Portable current-public-tree and private-primary replay for Topic A's DAG.

No archived Markdown/text file, Git worktree, GAP or Lean invocation is needed.
This validates the bound graph/accounting interface, not mathematical proofs.
"""
from pathlib import Path
import argparse,copy,csv,hashlib,importlib.util,json,re,sys
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def safe(root,path):
 p=Path(path);need(not p.is_absolute() and '..' not in p.parts and not any(ord(c)<32 for c in path),'Unsafe relative path')
 q=(root/p).resolve();need(q.is_relative_to(root.resolve()),'Input leaves declared root');return q

def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def routes_equal(public,private):
 pub=copy.deepcopy(public);old=pub.pop('original_private_path',None);path=pub.pop('path');original=copy.deepcopy(private)
 need(old==original.pop('path'),'Explicit original route')
 need(pub==original,'Routing change altered the measured boundary');return path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sources-root',type=Path,required=True);p.add_argument('--artifacts-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'Fresh output required')
 protocol=read(HERE/'protocol.json')
 for row in protocol['input_copies']:
  data=safe(HERE,row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Frozen copied input '+row['path'])
 I=HERE/'inputs';sys.path.insert(0,str(I/'weighted'))
 weightcheck=module('frozen_weightcheck',I/'weighted/check.py');account=module('owned_accounting',I/'weighted/accounting.py')
 graphcheck=module('frozen_graphcheck',I/'logical/check.py');extract=module('bound_extract',I/'extract_inputs.py')
 g=read(I/'logical/logical_graph.json');coverage=read(I/'logical/coverage.json')
 graph_summary=graphcheck.validate(g,coverage)
 part=read(I/'weighted/partition.json');weights=read(I/'weighted/weights.json')
 spec=read(I/'public_input_spec.json');priv=read(I/'private_replacement_spec.json');source=read(I/'source_spec.json')
 need(spec['sources']==source['sources'],'Unchanged primary boundaries')
 need(extract.pypdf.__version__==spec['pypdf_version']==source['pypdf_version']==priv['pypdf_version'],'pypdf version')
 need(set(spec['ours'])==set(priv['ours'])=={'U_A','A1','A2','A3','A4','A5','A6','code'},'Eight complete replacement documents')
 for k,v in spec['ours'].items():routes_equal(v,priv['ours'][k])
 for row in spec['published_artifacts']:
  data=safe(a.artifacts_root,row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Published artifact '+row['path'])
 docs=spec['sources']|spec['ours'];texts={};data={}
 for k,row in docs.items():
  root=a.sources_root if k in spec['sources'] else a.artifacts_root
  safe(root,row['path']);data[k]=extract.document(root,k,row);texts[k]=data[k][2]
 ow,dt=weightcheck.validate_weights(g,part,weights,texts,source['sources']|priv['ours'])
 for k,d in part['documents'].items():
  spans=copy.deepcopy(d['spans']);account.page_locations(data[k][0],docs[k],spans);need(spans==d['spans'],'Physical locator '+k)
 with (I/'weighted/owner_costs.csv').open(newline='') as file:rows=list(csv.DictReader(file))
 need(len(rows)==len(ow) and {r['owner'] for r in rows}==set(ow),'CSV ownership')
 for row in rows:need(all(int(row[f+'_'+m])==ow[row['owner']][f][m] for f in account.FORMS for m in account.METRICS),'CSV metric')
 independent=read(I/'independent_recount.json')['documents'];cells=hashes=0
 for k,record in data.items():
  for f in account.FORMS:
   for variant,text in zip(('untrimmed','raw_selected','calibrated_selected'),record[:3]):
    value=extract.metrics(text,f);expected=independent[k]['metrics'][f][variant]
    need(value==expected,'Independent metric/text mismatch '+k+f+variant);cells+=5;hashes+=1
 need(len(spec['required_programs'])==4,'Four complete required programs')
 for row,old in zip(spec['required_programs'],priv['required_programs']):
  routes_equal(row,old);raw=safe(a.artifacts_root,row['path']).read_bytes()
  need(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'Raw program binding')
  need(re.sub(r'\s+','',raw.decode()) in re.sub(r'\s+','',texts['code']),'Incomplete program appendix')
 need(set(weights['contract_closures'])=={r['id'] for r in coverage['rows']},'All declared contract rows')
 for row in coverage['rows']:need(weights['contract_closures'][row['id']]['starting_nodes']==sorted(row['new_nodes']),'Contract targets '+row['id'])
 current_spans=0;historical_archive_spans=0
 for n in g['nodes']:
  for loc in n['locators']:
   if 'start_codepoint' not in loc:continue
   if loc['path'] not in protocol['current_evidence_routes']:
    need(n['side']=='historical','Missing current proof route '+loc['path']);historical_archive_spans+=1;continue
   row=protocol['current_evidence_routes'][loc['path']];raw=safe(a.artifacts_root,row['path']).read_bytes()
   need(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'Current proof source')
   t=raw.decode();aa,bb=loc['start_codepoint'],loc['end_codepoint_exclusive']
   need(0<=aa<bb<=len(t) and sha(t[aa:bb].encode())==loc['sha256_utf8'],'Current mathematical locator '+n['id']);current_spans+=1
 measurement=read(I/'measurement.json');admission=read(I/'measurement_admission.json')
 need(admission['primary']==measurement['factors']['NFC']['calibrated_selected']['characters_without_whitespace'],'Bound headline scope')
 need(admission['status']=='PASS_ROOT_ADMITTED_TOPIC_A_MEASUREMENT','Numerical admission')
 for k in dt:
  for f in account.FORMS:need(dt[k][f]=={m:measurement['documents'][k]['metrics'][f]['calibrated_selected'][m] for m in account.METRICS},'Weighted/numerical edition difference')
 controls=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError):controls.append(name)
  else:raise ValueError('Control accepted '+name)
 bad=copy.deepcopy(spec['ours']['A6']);bad['pdf_sha256']='0'*64
 reject('routing_cannot_change_pdf',lambda:routes_equal(bad,priv['ours']['A6']))
 bad=copy.deepcopy(spec['ours']['A6']);bad['excluded_furniture']=[]
 reject('routing_cannot_drop_text',lambda:routes_equal(bad,priv['ours']['A6']))
 reject('traversal',lambda:safe(a.artifacts_root,'../hidden.pdf'))
 reject('control_character_path',lambda:safe(a.artifacts_root,'papers/\x00bad'))
 bad=copy.deepcopy(part);bad['documents']['A1']['spans'][1]['start']+=1
 reject('ownership_gap',lambda:weightcheck.validate_weights(g,bad,weights,texts,source['sources']|priv['ours']))
 bad=copy.deepcopy(weights);bad['program_representation']['raw_file_metrics_are_alternative_not_additional']=False
 reject('program_double_charge',lambda:weightcheck.validate_weights(g,part,bad,texts,source['sources']|priv['ours']))
 bad=copy.deepcopy(weights);bad['unknown_costs']['diagram_structure']=0
 reject('unknown_cost_zero',lambda:weightcheck.validate_weights(g,part,bad,texts,source['sources']|priv['ours']))
 report={'status':'PASS_PORTABLE_ADAPTER_PENDING_INDEPENDENT_REVIEW','graph':graph_summary,
  'documents':len(docs),'physical_pages':sum(r['pages'] for r in docs.values()),'ownership_spans':sum(len(x['spans']) for x in part['documents'].values()),
  'independent_metric_cells':cells,'independent_text_hashes':hashes,'current_mathematical_spans_checked':current_spans,
  'historical_archive_text_spans_not_replayed':historical_archive_spans,'historical_primary_PDFs_checked':6,
  'all_four_required_programs_in_full_charged_appendix':True,'negative_controls_rejected':controls,
  'no_primary_text_or_images_written':True,'public_proof_commit':spec['published_commit'],
  'logical_graph_sha256':sha((I/'logical/logical_graph.json').read_bytes()),'weights_sha256':sha((I/'weighted/weights.json').read_bytes()),
  'scope':protocol['replay_scope'],'mathematical_correctness_reproved':False,'self_admission':False}
 a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
if __name__=='__main__':main()
