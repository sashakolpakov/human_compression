#!/usr/bin/env python3
"""Author checks for exclusive ownership and prerequisite-union accounting.

This is not independent semantic approval of a passage or cost interface.
"""
import argparse,copy,csv,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,sha,allocations,interfaces,route,METRICS,FORMS,VARIANTS
from author import load_inputs
from boundaries import supplements

def validate(p,w,graph,coverage,texts,raw_programs,adopted):
 need(set(p['documents'])==set(texts)=={'L088','N013','F014','U_C','C1','C2','C3','C4','CODE'},'nine full PDF documents')
 need(p['missing_L108_original_pdf_cost'] is None and p['node_count_ratio'] is None,'no invented missing source cost or node ratio')
 costs,docs=allocations(p,texts)
 need(w['owner_costs']==costs and w['document_costs']==docs,'all actual metric allocations')
 for k,values in docs.items():
  for v in VARIANTS:
   for f in FORMS:need(values[v][f]=={m:adopted['documents'][k]['variants'][v][f][m] for m in METRICS},'all adopted complete PDF cells')
 links=interfaces(graph,p['owners'],costs,supplements())
 need(w['node_interfaces']==links,'reviewable complete owner interfaces')
 need(w['raw_program_alternative']==raw_programs and len(raw_programs)==2,'both whole raw program alternatives')
 mapped={o for x in links.values() for o in x['owners']}
 need(p['owners_outside_selected_logical_interfaces']==[p['owners'][n] for n in sorted(p['owners'].keys()-mapped)],'all owners outside selected routes visible')
 expected=[{'id':r['id'],'source_id':r['source'],'coverage':r['coverage'],
 'historical':route(r['historical_closure'],links,costs,p['owners'],raw_programs),
 'replacement':route(r['new_closure'],links,costs,p['owners'],raw_programs)} for r in coverage['rows']]
 need(w['source_contract_closures']==expected and len(expected)==40,'all forty scoped paired routes')
 need(w['new_application_closures']=={k:route(v,links,costs,p['owners'],raw_programs) for k,v in graph['new_output_closures'].items()},'all four complete application routes')
 need(w['additional_current_comparisons']=={k:route(v,links,costs,p['owners'],raw_programs) for k,v in graph['additional_comparison_closures'].items()},'separate additional comparison route')
 for f in ['complete_historical_pdf_cost','expanded_external_proof_cost','graphic_cost','compression_ratio']:need(w[f] is None,'unknown is not zero '+f)
 need(w['new_source_credit']==w['new_question_credit']==0,'no credit change')
 need(all(not x['charged_again'] and x['expanded_dependency_cost'] is None for x in links.values()),'no parent or alias double charge')
 need(links['h.P.T1']['known_weight'] is None and not links['h.P.T1']['owners'],'browser text not a PDF surrogate')
 codeids=[n for n,o in p['owners'].items() if o['document']=='CODE' and o['category']!='excluded_furniture']
 need(set(codeids)==set(links['program.construction']['owners'])|set(links['program.census']['owners']),'entire printed code appendix covered by two program interfaces')
 return {'documents':9,'document_metric_cells':270,'owners':len(p['owners']),'owner_metric_cells':len(p['owners'])*30,'selected_spans':sum(len(r['variants']['calibrated_selected']['spans']) for r in p['documents'].values()),'all_variant_spans':sum(len(r['variants'][v]['spans']) for r in p['documents'].values() for v in VARIANTS),'logical_interfaces':156,'paired_clauses':40,'output_closures':85,'raw_program_metric_cells':20}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output file');packet=a.packet;root=a.study_root
 inventory=json.loads((packet/'input_bindings.json').read_text())
 for b in inventory['inputs']:
  need(not Path(b['path']).is_absolute() and '..' not in Path(b['path']).parts,'safe source binding')
  data=(root/b['path']).read_bytes();need(sha(data)==b['sha256'] and len(data)==b['bytes'],'frozen input '+b['path'])
 graph,coverage,spec,extracted,texts,raw,adopted=load_inputs(root)
 p=json.loads((packet/'partition.json').read_text());w=json.loads((packet/'weights.json').read_text())
 result=validate(p,w,graph,coverage,texts,raw,adopted)
 from accounting import partition_document
 from boundaries import boundaries
 freshowners={};freshdocs={k:partition_document(k,row,extracted[k],boundaries()[k],freshowners) for k,row in spec.items()}
 need(freshdocs==p['documents'] and freshowners==p['owners'],'declared semantic-boundary reproduction and physical page locators')
 with (packet/'owner_costs.csv').open(newline='') as f:actual=list(csv.DictReader(f))
 rows=[]
 for n,o in p['owners'].items():
  for v in VARIANTS:
   for norm in FORMS:rows.append(dict(owner=n,document=o['document'],category=o['category'],variant=v,normalization=norm,**{m:str(w['owner_costs'][n][v][norm][m]) for m in METRICS}))
 need(actual==rows,'all owner CSV coordinates')
 controls=[]
 for name in ['gap','overlap','wrong_hash','wrong_owner_category','missing_source_zero','external_zero','double_parent','wrong_atomic_count','untrimmed_furniture_zero','drop_shared_statement','omit_program','omit_code_wrapper','duplicate_program_charge','drop_clause','invent_ratio']:
  pp,ww=copy.deepcopy(p),copy.deepcopy(w)
  ss=pp['documents']['U_C']['variants']['calibrated_selected']['spans']
  if name=='gap':ss[1]['start']+=1
  elif name=='overlap':ss[1]['start']-=1
  elif name=='wrong_hash':ss[0]['sha256']='0'*64
  elif name=='wrong_owner_category':ss[0]['category']='complete_proof'
  elif name=='missing_source_zero':pp['missing_L108_original_pdf_cost']=0
  elif name=='external_zero':ww['node_interfaces']['ext.Danzer']['known_weight']=0
  elif name=='double_parent':ww['node_interfaces']['C.Graph']['charged_again']=True
  elif name=='wrong_atomic_count':ww['owner_costs']['UC.front']['calibrated_selected']['NFKC']['whitespace_tokens']+=1
  elif name=='untrimmed_furniture_zero':ww['owner_costs']['L088.furniture']['raw_untrimmed']['NFC']['characters_without_whitespace']=0
  elif name=='drop_shared_statement':ww['node_interfaces']['C.Graph.geometry']['owners'].remove('C.Graph.statement')
  elif name=='omit_program':ww['raw_program_alternative'].pop('program.census')
  elif name=='omit_code_wrapper':ww['node_interfaces']['program.census']['owners'].remove('CODE.wrapper')
  elif name=='duplicate_program_charge':ww['new_application_closures']['L088']['owners'].append('program.construction.printed')
  elif name=='drop_clause':ww['source_contract_closures'].pop()
  else:ww['compression_ratio']=2
  try:validate(pp,ww,graph,coverage,texts,raw,adopted)
  except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise ValueError('mutation was accepted '+name)
 report={'status':'PASS_AUTHOR_EXCLUSIVE_OWNERSHIP_ALL30_COORDINATES',**result,'controls':controls,'CSV_rows':len(actual),'logical_semantics_reused_from_independent_acceptance':True,'ownership_semantics_independently_reviewed':False,'partition_sha256':sha((packet/'partition.json').read_bytes()),'weights_sha256':sha((packet/'weights.json').read_bytes()),'checker_sha256':sha(Path(__file__).read_bytes()),'missing_L108_pdf_cost':None,'new_source_credit':0,'new_question_credit':0}
 a.out.parent.mkdir(exist_ok=True,parents=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in result}))
if __name__=='__main__':main()
