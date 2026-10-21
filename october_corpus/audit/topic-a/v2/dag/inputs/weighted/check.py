#!/usr/bin/env python3
"""Re-extract bound private PDFs and verify exclusive ownership and all weights.

This tests accounting, not theorem validity or historical argument correctness.
"""
from pathlib import Path
import argparse,collections,copy,csv,importlib.util,json,re,sys
from accounting import *

HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def check_binding(root,row):
    p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'unsafe binding path')
    b=(root/p).read_bytes()
    need(sha(b)==row['sha256'] and len(b)==row['bytes'],'input hash: '+str(p))
def validate_weights(graph,partition,result,texts,spec):
    owners=partition['owners'];docs=partition['documents'];spans={k:d['spans'] for k,d in docs.items()}
    need(set(docs)==set(texts)==set(spec),'all fourteen documents')
    for k,text in texts.items():
        d=docs[k]
        need(d['pdf']==spec[k]['path'] and d['pdf_sha256']==spec[k]['pdf_sha256'],'PDF edition binding '+k)
        need(d['pages']==spec[k]['pages'],'page count '+k)
        need(d['selected_calibrated_codepoints']==len(text) and d['selected_calibrated_sha256']==sha(text.encode()),'selected text binding '+k)
        need(d['span_count']==len(spans[k]),'span count '+k)
    ow,dt=build_weights(texts,spec,spans,owners)
    need(ow==result['owner_weights'],'owner weights')
    need(dt==result['document_totals'],'document weights')
    need(set(owners)=={s['node'] for a in spans.values() for s in a},'orphan owner')
    categories={}
    for k in docs:
        cc={o['category'] for o in owners.values() if o['document']==k}
        categories[k]={c:add_weights([ow[i] for i,o in owners.items() if o['document']==k and o['category']==c]) for c in sorted(cc)}
    need(categories==result['category_totals'],'category conservation')
    links=result['logical_node_cost_interfaces'];validate_links(graph,owners,links)
    for node,required in {'A2.main':['A2.seed.inputs','A2.presentation','A2.statement'],'A2.recognition':['A2.presentation'],'L034.T3.2':['L034.proof.setup'],'N009.Table6':['N009.universal.algorithm']}.items():
        need(set(required)<=set(links[node]['owners']),'missing substantive statement/argument ownership '+node)
    for n,row in links.items():
        expected=add_weights([ow[i] for i in row['owners']]) if row['owners'] else None
        need(row['weight']==expected,'logical owner rollup '+n)
        need(row['full_dependency_cost'] is None,'unmeasured full dependency cost')
    index={n['id']:n for n in graph['nodes']};incoming=collections.defaultdict(set)
    kinds={'proof_use','retained_input_use','retained_algorithm_use','computational_use','branch_membership',
           'output_assembly','historical_documented_use','historical_asserted_use','definition_use',
           'declared_retained_translation'}
    for e in graph['edges']:
        if e['kind'] in kinds:incoming[e['target']].add(e['source'])
    def closure(starts):
        found=set(starts);todo=list(starts)
        while todo:
            for n in incoming[todo.pop()]-found:found.add(n);todo.append(n)
        return found
    for family in ('logical_closures','contract_closures'):
        for id,row in result[family].items():
            ns=closure(row['starting_nodes']);leaves=sorted(set().union(*(set(links[n]['owners']) for n in ns)))
            need(row['logical_nodes']==sorted(ns),'documentary closure '+id)
            need(row['unique_owner_ids']==leaves,'duplicate or missing closure owner '+id)
            need(row['known_owned_text_subtotal']==add_weights([ow[i] for i in leaves]),'closure sum '+id)
            need(row['unknown_external_nodes']==sorted(n for n in ns if index[n]['category']=='external'),'external closure '+id)
            need(row['complete_dependency_cost'] is None,'closure has unsupported complete cost')
            qualifications=[{'node':n,'qualification':index[n]['documentary_validity']} for n in sorted(ns) if index[n].get('documentary_validity')]
            need(row['documentary_qualifications']==qualifications,'documentary qualifications lost')
            used={owners[i]['document'] for i in leaves}
            need(row['other_document_text_not_in_this_graph_closure']==sorted(i for i,o in owners.items() if o['document'] in used and i not in leaves),'unpriced local text not disclosed')
    unknown=result['unknown_costs']
    need(all(unknown[k] is None for k in ('retained_external_proofs','unextracted_scientific_raster_labels','diagram_structure')),'unknown cost converted to zero')
    need(result['raw_node_count_ratio'] is None and result['proof_count_ratio'] is None,'invalid node ratio')
    need(result['program_representation']['charged']=='code.appendix','raw code double charge')
    need(result['program_representation']['raw_file_metrics_are_alternative_not_additional'] is True,'program double representation')
    return ow,dt

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--study-root',type=Path,default=HERE.parent)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=a.study_root.resolve()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output required')
    b=read(HERE/'input_bindings.json')
    for row in b['inputs']+b['pdf_inputs']:check_binding(root,row)
    ss=read(root/'topic_A_measurement/source_input_spec.json')
    rs=read(root/'topic_A_numerical_audit/final_replacement_input_spec_private.json')
    spec=ss['sources']|rs['ours']
    im=importlib.util.spec_from_file_location('measurement',root/'topic_A_measurement/extract_inputs.py')
    m=importlib.util.module_from_spec(im);im.loader.exec_module(m)
    need(m.pypdf.__version__==ss['pypdf_version']==rs['pypdf_version'],'pypdf version')
    data={k:m.document(root,k,row) for k,row in spec.items()};texts={k:x[2] for k,x in data.items()}
    graph=read(root/'topic_A_logical_dag_v3/logical_graph.json')
    part=read(HERE/'partition.json');result=read(HERE/'weights.json')
    ow,dt=validate_weights(graph,part,result,texts,spec)
    with (HERE/'owner_costs.csv').open(newline='') as file:csvrows=list(csv.DictReader(file))
    need(len(csvrows)==len(ow) and {x['owner'] for x in csvrows}==set(ow),'CSV owner coverage')
    for row in csvrows:
        id=row['owner'];owner=part['owners'][id]
        need(all(row[k]==owner[k] for k in ('document','category','label')),'CSV owner metadata')
        pp=sorted(set().union(*(set(s['physical_pages']) for s in part['documents'][owner['document']]['spans'] if s['node']==id)))
        need(row['physical_pages']==','.join(map(str,pp)),'CSV physical pages')
        need(all(int(row[f+'_'+m])==ow[id][f][m] for f in FORMS for m in METRICS),'CSV metrics')
    for k,d in part['documents'].items():
        calculated=copy.deepcopy(d['spans']);positions=page_locations(data[k][0],spec[k],calculated)
        need(len(positions)==len(texts[k]),'selected position length')
        need(calculated==d['spans'],'physical-page locators '+k)
    old=read(root/'topic_A_measurement_root_review/recount.json')['documents']
    final=read(root/'topic_A_A6_final_recount_root/recount.json')['document']
    root_cells=0
    for k in dt:
        for f in FORMS:
            expected=(final if k=='A6' else old[k])['metrics'][f]['calibrated_selected']
            need(dt[k][f]=={v:expected[v] for v in METRICS},'independent root metrics '+k+f);root_cells+=5
    need(result['program_representation']['required_raw_files']==rs['required_programs'],'four program closure')
    need(len(rs['required_programs'])==4,'all four required programs')
    for row in rs['required_programs']:
        check_binding(root,row);code=(root/row['path']).read_text()
        need(re.sub(r'\s+','',code) in re.sub(r'\s+','',texts['code']),'whole program absent from appendix')
    coverage=read(root/'topic_A_logical_dag/coverage.json')
    need(set(result['contract_closures'])=={x['id'] for x in coverage['rows']},'all 55 contract rows')
    for row in coverage['rows']:
        need(result['contract_closures'][row['id']]['starting_nodes']==sorted(row['new_nodes']),'contract mapping '+row['id'])
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):controls.append(name)
        else:raise ValueError('control accepted '+name)
    for name,change in [('ownership_gap',lambda x:x['documents']['A1']['spans'][1].update(start=x['documents']['A1']['spans'][1]['start']+1)),
                        ('ownership_overlap',lambda x:x['documents']['A1']['spans'][1].update(start=x['documents']['A1']['spans'][1]['start']-1)),
                        ('wrong_span_hash',lambda x:x['documents']['A1']['spans'][1].update(sha256='0'*64))]:
        pp=copy.deepcopy(part);change(pp);reject(name,lambda pp=pp:validate_weights(graph,pp,result,texts,spec))
    external=next(n['id'] for n in graph['nodes'] if n['category']=='external')
    for name,change in [('drop_required_source_argument',lambda x:x['logical_node_cost_interfaces']['N009.Table6']['owners'].remove('N009.universal.algorithm')),
                        ('external_zero',lambda x:x['logical_node_cost_interfaces'][external].update(weight=0)),
                        ('parent_double_charge',lambda x:x['logical_node_cost_interfaces']['UA.SK'].update(charged_as_an_additional_item=True)),
                        ('code_double_representation',lambda x:x['program_representation'].update(raw_file_metrics_are_alternative_not_additional=False)),
                        ('owner_weight_corruption',lambda x:x['owner_weights']['A1.front']['NFC'].update(whitespace_tokens=999999)),
                        ('unknown_image_zero',lambda x:x['unknown_costs'].update(diagram_structure=0))]:
        rr=copy.deepcopy(result);change(rr);reject(name,lambda rr=rr:validate_weights(graph,part,rr,texts,spec))
    wrong=copy.deepcopy(b['pdf_inputs'][0]);wrong['sha256']='0'*64
    reject('wrong_primary_edition',lambda:check_binding(root,wrong))
    report={'status':'PASS_ACCOUNTING_PENDING_INDEPENDENT_OWNERSHIP_REVIEW',
      'documents':len(texts),'pages':sum(x['pages'] for x in spec.values()),'contract_rows':len(coverage['rows']),
      'ownership_spans':sum(len(d['spans']) for d in part['documents'].values()),'unique_owners':len(ow),
      'root_metric_cells_equal':root_cells,'all_selected_characters_owned_exactly_once':True,
      'all_four_required_programs_in_charged_appendix':True,'unknown_external_and_image_costs':None,
      'negative_controls_rejected':controls,'logical_graph_sha256':sha((root/'topic_A_logical_dag_v3/logical_graph.json').read_bytes()),
      'pypdf_version':m.pypdf.__version__,'python_version':sys.version,
      'checked_artifacts':[{ 'path':n,'sha256':sha((HERE/n).read_bytes())} for n in ('partition.json','weights.json','input_bindings.json','owner_costs.csv','accounting.py','check.py')],
      'scope':'Hashes, extraction, partition, atomic allocation, rollups and recorded closures. Does not prove semantic correctness of edges or of source/replacement mathematics.',
      'self_admission':False,'ratio':None,'new_source_credit':0,'new_question_credit':0}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:report[k] for k in ('status','documents','ownership_spans','root_metric_cells_equal','negative_controls_rejected')}))
if __name__=='__main__':main()
