#!/usr/bin/env python3
"""Validate exclusive ownership, additive metric allocation and accepted DAG routing.

This is an author consistency checker, not independent semantic span review.
"""
import argparse,collections,copy,csv,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,sha,build_weights,page_locations,add_weights,FORMS,METRICS

def union_route(names,links,costs,owners):
    paid=sorted({x for n in names for x in links[n]['owners']})
    return dict(logical_nodes=sorted(names),owners=paid,known_extracted_text_subtotal=add_weights([costs[x] for x in paid]),
        by_document={k:add_weights([costs[x] for x in paid if owners[x]['document']==k]) for k in sorted({owners[x]['document'] for x in paid})},
        unknown_inputs=sorted(n for n in names if links[n]['weight'] is None),expanded_dependency_cost=None,
        scope='Selected documentary prerequisite union, not a minimal proof or a complete-paper denominator. Omitted context and all full-paper text remain charged in the accepted overall comparison.')

def validate(p,w,g,c,texts,extracted,spec,measured):
    need(set(p['documents'])==set(texts)==set(spec),'all eight available complete PDFs')
    need(p['N001_original_pdf_cost'] is None,'missing N001 PDF cost remains null')
    owners=p['owners'];parts={k:r['spans'] for k,r in p['documents'].items()}
    for k,row in p['documents'].items():
        need(row['text_sha256']==sha(texts[k].encode()) and row['length']==len(texts[k]) and row['pdf_sha256']==spec[k]['pdf_sha256'],'document hash/length binding')
        actual=copy.deepcopy(parts[k]);positions=page_locations(extracted[k][0],spec[k],actual)
        need(len(positions)==len(texts[k]),'selected text / raw page-position alignment')
        need(actual==parts[k],'exact physical page correspondence')
    costs,doc=build_weights(texts,spec,parts,owners)
    need(costs==w['owner_costs'] and doc==w['document_costs'],'actual additive owner and document metrics')
    for k,values in doc.items():
        for f in FORMS:
            need(values[f]=={m:measured['documents'][k]['calibrated_selected'][f][m] for m in METRICS},'independently accepted whole document count')
    nodes={n['id']:n for n in g['nodes']};links=w['node_interfaces']
    need(set(links)==set(nodes),'one explicit cost interface per logical node')
    for name,row in links.items():
        n=nodes[name];paid=row['owners']
        need(paid==sorted(set(paid)) and set(paid)<=set(owners),'valid unique interface owner union')
        need(row['charged_as_an_additional_item'] is False and row['full_dependency_cost'] is None,'aliases are not additional cost or complete dependency cost')
        need(all(owners[x]['document']==n['document'] for x in paid),'same-document statement/proof ownership')
        unknown=n['side'] in ['external','verification'] or n['document']=='N001'
        if unknown:need(row['weight'] is None and paid==[],'unknown retained/missing/validation cost not zero')
        else:
            need(paid and row['weight']==add_weights([costs[x] for x in paid]),'exact named/branch owner union')
            for direct in [name,name+'.statement']:
                if direct in owners:need(direct in paid,'direct named statement/proof owner preserved')
            if n.get('parent') and n['parent']+'.statement' in owners:
                need(n['parent']+'.statement' in paid,'branch pays shared theorem statement')
        if n.get('parent'):need(set(paid)<=set(links[n['parent']]['owners']),'parent includes every child passage, without additive double charge')
    essential={
      'UB.Relative':['UB.relative.setup'],'UB.F':['UB.F.unit'],'UB.TwoBlockData':['UB.Overgroups.statement'],
      'B1.Reconstruction':['B1.B97'],'B4.Distance':['B4.distance.setup'],
      'h.N003.T2.1':['h.N003.tree.defs'],'h.N003.T3.2':['h.N003.T3.2.converse_setup'],
      'h.N008.Definitions':['h.N008.frattini.defs'],'h.N008.T3.1':['h.N008.containment.setup'],
      'h.N008.T3.4':['h.N008.frattini_free.setup','h.N008.frattini_free.proof'],
      'h.N008.P3.7':['h.N008.pgroup.input'],'h.N008.T3.8':['h.N008.pgroup.input'],
      'h.L030.T1.2':['h.L030.T1.2.assembly']}
    for name,required in essential.items():need(set(required)<=set(links[name]['owners']),'explicit mathematical setup/assembly owner')
    mapped={x for r in links.values() for x in r['owners']}
    unmapped=[owners[n] for n in sorted(set(owners)-mapped)]
    need(p['unmapped_owners']==unmapped,'all omitted closure owners are listed')
    need(all(x['category'] in ['front_matter','context','references'] for x in unmapped if x['document'] in ['U_B','B1','B2','B3','B4']),
         'no new substantive proof passage omitted from all logical interfaces')
    rows=w['source_contract_closures'];need(len(rows)==len(c['rows'])==30,'all fixed clauses')
    for row,source in zip(rows,c['rows']):
        need(row['adapter']==source['adapter'] and row['source_id']==source['source_id'],'source clause order/identity')
        need(row['historical']==union_route(source['historical_closure'],links,costs,owners),'actual historical prerequisite owner union')
        need(row['replacement']==union_route(source['new_closure'],links,costs,owners),'actual new prerequisite owner union')
    need(w['new_application_closures']=={k:union_route(v,links,costs,owners) for k,v in g['new_output_closures'].items()},'complete application routes')
    for key in ['whole_historical_pdf_cost','expanded_external_proof_cost','graphic_cost','compression_ratio']:
        need(w[key] is None,'unknown or deliberately undefined total: '+key)
    need(w['new_source_credit']==w['new_question_credit']==0,'no credit changes')
    return dict(documents=len(texts),spans=sum(len(v) for v in parts.values()),owners=len(owners),document_metric_cells=len(texts)*10,
        owner_metric_cells=len(owners)*10,logical_interfaces=len(links),source_contracts=30,application_closures=4,
        unmapped_context_or_excluded_source_owners=len(unmapped))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.study_root.resolve();need(not a.out.exists(),'fresh report');packet=a.packet.resolve()
    load=lambda name:json.loads((root/name).read_text())
    inp=json.loads((packet/'input_bindings.json').read_text())
    for row in inp['inputs']:
        need(not Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts,'safe relative binding')
        raw=(root/row['path']).read_bytes();need(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'fixed input hash')
    need(inp['logical_packet_independently_accepted'] and inp['primary_text_exported'] is False and inp['node_count_ratio'] is None,'logical/adopted-boundary scope')
    g=load('topic_B_logical_dag_v2/logical_graph.json');c=load('topic_B_logical_dag_v2/coverage.json')
    specs=load('topic_B_measurement/source_input_spec.json')['sources']|load('topic_B_measurement/replacement_input_spec.json')['ours']
    modspec=importlib.util.spec_from_file_location('bound_bmeasure',root/'topic_B_measurement/extract_inputs.py');m=importlib.util.module_from_spec(modspec);modspec.loader.exec_module(m)
    need(m.pypdf.__version__=='6.13.0','pinned parser')
    extracted={k:m.document(root,k,v) for k,v in specs.items()};texts={k:v[2] for k,v in extracted.items()}
    measured=load('topic_B_measurement_results/independent/recount.json')
    p=json.loads((packet/'partition.json').read_text());w=json.loads((packet/'weights.json').read_text())
    result=validate(p,w,g,c,texts,extracted,specs,measured)
    with (packet/'owner_costs.csv').open(newline='') as f:csvrows=list(csv.DictReader(f))
    expected=[]
    for name in sorted(p['owners']):
        for form in FORMS:expected.append(dict(owner=name,document=p['owners'][name]['document'],category=p['owners'][name]['category'],normalization=form,
            **{m:str(w['owner_costs'][name][form][m]) for m in METRICS}))
    need(csvrows==expected,'complete owner CSV')
    controls=[]
    for name in ['gap','overlap','wrong_span_hash','wrong_page','missing_N001_zero','external_zero','parent_double_charge','wrong_atomic_weight','omit_branch_statement','omit_retained_classification_statement','lose_clause','invent_graph_factor']:
        pp,ww=copy.deepcopy(p),copy.deepcopy(w)
        if name=='gap':pp['documents']['U_B']['spans'][1]['start']+=1
        elif name=='overlap':pp['documents']['U_B']['spans'][1]['start']-=1
        elif name=='wrong_span_hash':pp['documents']['U_B']['spans'][0]['sha256']='0'*64
        elif name=='wrong_page':pp['documents']['U_B']['spans'][0]['physical_pages']=[99]
        elif name=='missing_N001_zero':pp['N001_original_pdf_cost']=0
        elif name=='external_zero':ww['node_interfaces']['ext.B97']['weight']=0
        elif name=='parent_double_charge':ww['node_interfaces']['UB.F']['charged_as_an_additional_item']=True
        elif name=='wrong_atomic_weight':ww['owner_costs']['UB.front']['NFC']['whitespace_tokens']+=1
        elif name=='omit_branch_statement':ww['node_interfaces']['UB.Relative.choices']['owners'].remove('UB.Relative.statement')
        elif name=='omit_retained_classification_statement':ww['node_interfaces']['B1.Reconstruction']['owners'].remove('B1.B97')
        elif name=='lose_clause':ww['source_contract_closures'].pop()
        else:ww['compression_ratio']=2
        try:validate(pp,ww,g,c,texts,extracted,specs,measured)
        except ValueError as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('negative control accepted: '+name)
    report=dict(status='PASS_AUTHOR_EXCLUSIVE_OWNERSHIP_ACCOUNTING_CHECK',**result,controls=controls,
       logical_graph_sha256=sha((root/'topic_B_logical_dag_v2/logical_graph.json').read_bytes()),
       graph_semantics_reused_from_independent_acceptance=True,ownership_semantics_independently_accepted=False,
       graphic_and_retained_proof_costs_unknown=True,N001_pdf_cost=None,
       partition_sha256=sha((packet/'partition.json').read_bytes()),weights_sha256=sha((packet/'weights.json').read_bytes()),
       checker_sha256=sha(Path(__file__).read_bytes()))
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in result}))
if __name__=='__main__':main()
