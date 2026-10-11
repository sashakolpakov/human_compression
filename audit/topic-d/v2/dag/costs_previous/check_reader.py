#!/usr/bin/env python3
"""Check derived Topic D views without trusting their generator's route traversal.

This is an author test, not independent mathematical/ownership acceptance.
"""
import argparse, copy, json
from pathlib import Path
from accounting import need, sha, VARIANTS, FORMS, METRICS

def read(p): return json.loads(p.read_text())

def summed(ids, weights):
    return {v:{f:{m:sum(weights[n][v][f][m] for n in set(ids))
                    for m in METRICS} for f in FORMS} for v in VARIANTS}

def ancestors(targets, graph):
    incoming={n['id']:[] for n in graph['nodes']}
    for e in graph['edges']:
        if e['kind'] in graph['logical_edge_kinds']: incoming[e['target']].append(e['source'])
    visited=set();todo=list(targets)
    while todo:
        n=todo.pop()
        if n not in visited: visited.add(n);todo.extend(incoming[n])
    return visited

def validate(d, acquisition, partition, w, graph, coverage, measurement, published):
    need(d['measurement']==measurement,'unchanged admitted whole-document figures')
    need(d['edges']==graph['edges'] and d['logical_edge_kinds']==graph['logical_edge_kinds'],'actual typed arrow direction')
    need(d['owner_weights']==w['owner_costs'],'all owner coordinates unchanged')
    need(d['logical_node_count']==137 and d['edge_count']==283 and d['owner_count']==220,'declared exact granularity')
    need(d['parents']=={n['id']:n['parent'] for n in graph['nodes'] if n.get('parent')},'actual grouping parents')
    need(d['source_qualifications']==graph['limits'],'all source qualifications retained')
    by={n['id']:n for n in d['nodes']};need(len(by)==len(d['nodes']),'unique displayed ids')
    all_owners=partition['owners'];costs=w['owner_costs'];interfaces=w['node_interfaces']
    for n in graph['nodes']:
        actual=by[n['id']];route=ancestors([n['id']],graph)
        owned={o for k in route for o in interfaces[k]['owners']}
        need(actual['owners']==interfaces[n['id']]['owners'],'node owner interface')
        need(actual['weight']==interfaces[n['id']]['known_weight'],'node weight or unknown')
        need(actual['closure']['unique_owner_ids']==sorted(owned),'independent prerequisite owner union')
        need(actual['closure']['known_owned_text_subtotal']==summed(owned,costs),'independent 30-coordinate closure sum')
        need(actual['closure']['unknown_external_nodes']==[k for k in sorted(route) if interfaces[k]['known_weight'] is None],'unknown route inputs retained')
        need(actual['locators']==n['locators'] and actual['documentary_flags']==n['documentary_flags'],'exact proof/source qualifiers')
    pairs={r['id']:r for r in d['pairs']};need(len(pairs)==42,'three full contracts, thirty-seven clauses, two additional current outputs')
    for source,app in graph['applications'].items():
        rows=[r for r in coverage['rows'] if r['source']==source]
        need(pairs[app]['new_targets']==graph['new_application_outputs'][source],'complete application targets')
        need(pairs[app]['historical_targets']==sorted({n for r in rows for n in r['historical_outputs']}),'full historical contract targets')
    for r in coverage['rows']:
        pair=pairs['clause:'+r['id']]
        need(pair['historical_targets']==r['historical_outputs'] and pair['new_targets']==r['new_outputs'],'each of thirty-seven paired output interfaces')
        need(pair.get('context_targets')==r['retained_input_nodes']+r['qualification_context_nodes'],'all retained and qualification context routes')
        need(r['accepted_record']['reference'] in pair['statement'],'exact source-target description')
    for name in graph['additional_current_outputs']:need(pairs['additional:'+name]['new_targets']==[name] and pairs['additional:'+name]['historical_targets']==[],'separate additional current output')
    for key,b in published.items():need(d['documents'][key]['path']==b['public_path'],'current public PDF link')
    need(all(d['documents'][k]['weight']==w['document_costs'][k] for k in w['document_costs']),'all eight full-document costs unchanged')
    need(d['acquisition']==acquisition,'single derived acquisition dataset')
    need(acquisition['expanded_external_proof_cost'] is None and acquisition['graphic_cost'] is None,'unknowns remain null')
    stages=acquisition['stages'];need([r['stage'] for r in stages]==['U_D','CODE','D1','D2','D3'],'declared full-document order')
    paid=set();known=[];missing=False;source_by_app={a:s for s,a in graph['applications'].items()}
    for r in stages:
        key=r['stage'];full={o for o,x in all_owners.items() if x['document']==key}
        targets=[n['id'] for n in graph['nodes'] if n['document']==key and not n['id'].startswith('program.')]
        route=ancestors(targets,graph);used={o for n in route for o in interfaces[n]['owners']}
        need(r['previous_owner_ids']==sorted(paid) and r['complete_local_owner_ids']==sorted(full),'all complete local context owners')
        need(r['new_owner_ids']==sorted(full-paid) and r['cumulative_owner_ids']==sorted(paid|full),'exclusive sequential acquisition')
        need(r['logical_route_owner_ids']==sorted(used) and not used-paid-full,'prerequisites paid before use')
        need(r['new_cost']==summed(full-paid,costs) and r['cumulative_cost']==summed(paid|full,costs),'all sequential 30-coordinate totals')
        need(r['written_cumulative_cost']==summed({o for o in paid|full if all_owners[o]['document']!='CODE'},costs),'written first, program comparison separate')
        need(r['reused_owner_ids']==sorted(used&paid) and r['reused_route_cost']==summed(used&paid,costs),'reuse is existing owner union, not a discount')
        need(r['local_text_outside_route']==sorted(full-used),'context omitted by small route remains charged')
        if key in source_by_app:
            source=source_by_app[key]
            if source in w['document_costs']:known.append(source)
            else:missing=True
            hist=r['historical_cumulative'];subtotal=summed(known,w['document_costs'])
            need(hist['known_documents']==known and hist['known_subtotal']==subtotal,'whole historical document acquisition')
            need(hist['unknown_source']==None and hist['unknown_coefficient']==int(missing),'historical symbolic source sum')
            need(hist['complete_cost']==(None if missing else subtotal),'no invented full historical numerical curve')
        paid|=full
    need(paid=={o for o,x in all_owners.items() if x['document'] in ['U_D','CODE','D1','D2','D3']},'every current document owner paid once')
    need(acquisition['historical_complete_numeric_curve']==[r['historical_cumulative']['complete_cost'] for r in stages if r['historical_cumulative']],'complete historical acquisition curve')
    for name,raw in w['raw_operational_drivers'].items():need(by[name]['raw_driver']==raw,'complete driver inventory')
    for name in w['raw_program_alternative']:
        need(by[name]['weight'] is not None and by[name]['owners'],'required and diagnostic program PDF costs known')
    return {'paired_views':84,'node_closure_coordinate_checks':137*30,'sequential_stages':5,'mathematical_nodes':137,'view_nodes':len(by),'complete_document_factor_changes':0}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh reader report')
    p=a.packet;root=a.study_root
    for b in read(p/'reader_input_bindings.json')['inputs']:
        name=Path(b['path']);need(not name.is_absolute() and '..' not in name.parts,'safe reader input binding')
        raw=(root/name).read_bytes();need(len(raw)==b['bytes'] and sha(raw)==b['sha256'],'fixed reader input '+str(name))
    d=read(p/'view_data.json');acq=read(p/'acquisition.json');partition=read(p/'partition.json');w=read(p/'weights.json')
    g=read(root/'topic_D_logical_dag_v2/logical_graph.json');c=read(root/'topic_D_logical_dag_v2/coverage.json');m=read(root/'topic_D_measurement_results/results.json');pub=read(root/'topic_D_measurement_v2/publication_binding.json')['scientific_documents']
    counts=validate(d,acq,partition,w,g,c,m,pub)
    policy=read(p/'protocol.json');primary=m['primary']
    need(policy['units']==list(METRICS) and policy['policy_variants']==list(VARIANTS) and policy['normalizations']==list(FORMS),'exact thirty-coordinate policy')
    need(policy['node_count_factor'] is None and policy['minimum_proof_complexity'] is None,'no node or route factor')
    expected=(p/'explorer_template.html').read_text().replace('__CSS__',(p/'explorer.css').read_text()).replace('__JS__',(p/'explorer.js').read_text()).replace('__DATA__',json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    need((p/'explorer.html').read_text()==expected,'HTML exactly generated from current code and data')
    controls=[]
    for name in ['reverse_proof_arrow','drop_qualifier','wrong_historical_total','omit_local_context','reuse_as_discount','duplicate_owner','drop_program_stage','replace_full_ratio','drop_clause_target','external_cost_zero','diagnostic_zero','wrong_public_link','invent_parent']:
        dd=copy.deepcopy(d);aa=copy.deepcopy(acq)
        if name=='reverse_proof_arrow':dd['edges'][0]['source'],dd['edges'][0]['target']=dd['edges'][0]['target'],dd['edges'][0]['source']
        elif name=='drop_qualifier':dd['source_qualifications']=[]
        elif name=='wrong_historical_total':aa['stages'][4]['historical_cumulative']['complete_cost']=None
        elif name=='omit_local_context':aa['stages'][2]['complete_local_owner_ids'].pop()
        elif name=='reuse_as_discount':aa['stages'][3]['new_cost']=aa['stages'][3]['reused_route_cost']
        elif name=='duplicate_owner':aa['stages'][4]['cumulative_owner_ids'].append(aa['stages'][4]['cumulative_owner_ids'][0])
        elif name=='drop_program_stage':aa['stages'].pop(1)
        elif name=='replace_full_ratio':dd['measurement']['primary']['comparisons']['written_papers']['factor']=2
        elif name=='drop_clause_target':next(x for x in dd['pairs'] if x['id']=='clause:L066.4')['new_targets']=[]
        elif name=='external_cost_zero':next(x for x in dd['nodes'] if x['id']=='ext.Mobius')['weight']=0
        elif name=='diagnostic_zero':next(x for x in dd['nodes'] if x['id']=='diagnostic.fields')['weight']=0
        elif name=='wrong_public_link':dd['documents']['D3']['path']='missing.pdf'
        else:dd['parents']['D1.Symmetric']='D1.Ordered'
        dd['acquisition']=aa
        try:validate(dd,aa,partition,w,g,c,m,pub)
        except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('accepted corruption '+name)
    report={'status':'PASS_AUTHOR_READER_AND_ACQUISITION_CHECKS',**counts,'controls':controls,'real_browser_test':False,'independent_ownership_acceptance':False,'input_hashes':{n:sha((p/n).read_bytes()) for n in ['partition.json','weights.json','view_data.json','acquisition.json','explorer.html','reader_data.py','explorer.js','check_reader.py']}}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(counts))
if __name__=='__main__':main()
