#!/usr/bin/env python3
"""Distinct successor arithmetic comparison, based on the independent oracle."""
import copy,json,pathlib
from derive import need,read,sha,derive,VARIANTS,FORMS,UNITS,PRIMARY
DOCS=['F010','L126','U_R','R1','R2','CODE']
ROLES=['required_finite_certificate','required_graph_data','optional_validation','current_orchestration_driver','partial_formal_evidence']
def as_fraction(x):return {k:v for k,v in x.items()if k!='decimal_12'}|{'decimal':x['decimal_12']}
def expected_rows(oracle):
    raw={(x['normalization'],x['unit']):x['whole_role_counts']for x in oracle['raw_inventory']};out=[]
    for x in oracle['coordinates']:
        d=x['documents'];r=raw[x['normalization'],x['unit']]
        out.append(dict(variant=x['variant'],normalization=x['normalization'],unit=x['unit'],costs=d,raw_costs=r,totals={'source':d['F010']+d['L126'],'common':d['U_R'],'applications':d['R1']+d['R2'],'written':d['U_R']+d['R1']+d['R2']},comparisons={'written':as_fraction(x['whole_written']),'conditional_F010':as_fraction(x['conditional']['F010']),'conditional_L126':as_fraction(x['conditional']['L126'])},software_inclusive_factor=None,inventory={'printed_all10_programs':d['CODE'],'raw_all10_programs':r['required_finite_certificate']+r['optional_validation'],'mandatory_graph_data':r['required_graph_data'],'printed_and_raw_code_are_alternatives':True,'data_is_not_in_printed_code':True,'source_software_cost':None}))
    return out

def check_result(r,oracle,study,protocol):
    rows=expected_rows(oracle);need(r['coordinates']==rows,'all90 fractions,180 document cells and all programme inventories')
    primary=next(x for x in rows if(x['variant'],x['normalization'],x['unit'])==PRIMARY)
    need(r['primary']==primary and r['primary_coordinate']==list(PRIMARY),'exact primary and all rounded values')
    inp=study/'topic_Representation_L126_measurement_inputs_v2'
    for key,filename in [('whole_document_map','document_map.json'),('raw_file_inventory','raw_file_map.json'),('source_boundary','source_boundary.json')]:need(r[key]==read(inp/filename),'whole accepted '+key)
    need(r['unknown_costs']==read(inp/'policy.json')['unknowns']and all(x is None for x in r['unknown_costs'].values()),'unknown costs null')
    need(r['physical_pages']==dict(zip(DOCS,[13,13,13,4,12,16]))and r['source_ids']==['F010','L126'],'full document/source scope')
    need((r['coordinate_count'],r['exact_fraction_count'],r['whole_written_fractions'],r['conditional_fractions'])==(30,90,30,60),'exact fraction counts')
    need(r['source_titles']==read(inp/'source_boundary.json')['source_titles'],'literal source titles')
    s=r['scope'];need(s=={'F010_blocks':6,'L126_dispositions':31,'whole_common_once':True,'both_complete_applications':True,'no_sibling_application_dependency':True,'programs_excluded_symmetrically':True,'optional_validation_required_for_conditional':False,'required_certificate_and_graph_data_for_L126':True,'retained_classical_premises_acquired':True,'whole_required_files_never_discounted':True,'full_source_formalized':False,'partial_Lean_declarations':22,'software_inclusive_factor':None,'source_software_cost':None},'complete fixed scope')
    need(r['acquisition']=={'initial_common':['U_R'],'F010_local':['R1'],'L126_local':['R2'],'retained_classical_cost':None,'F010_required_software':[],'L126_required_software':['certificate/check.py','certificate/graph.json'],'optional_validation_is_not_prepaid':True,'complete_written_stages':[36715,47700,82152]},'actual acquisition, no sibling or optional prerequisite')
    need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit'])and r['primary_material_exported']is False,'no new credit')
    need(primary['comparisons']['written']['numerator']<primary['comparisons']['written']['denominator']and 'expansion' in r['interpretation']['whole_topic']and 'not achieved whole-topic compression'in r['interpretation']['whole_topic'],'explicit primary expansion')
    need(protocol['primary']==list(PRIMARY)and protocol['source_ids']==['F010','L126']and protocol['written_documents']==['U_R','R1','R2'],'complete precount policy')
    need(protocol['conditional_applications']=={'F010':'R1','L126':'R2'}and protocol['allowed_comparisons']==['written','conditional_F010','conditional_L126'],'only three comparisons')
    need(protocol['software_inclusive_factor']is None and not protocol['optional_validation_required']and protocol['required_graph_certificate_and_data_acquired_for_L126']and protocol['no_sibling_application_dependency'],'fixed symmetric programme policy')
    return rows

def controls(result,oracle,study,protocol):
    changes=[('free_common',lambda x:x['coordinates'][0]['totals'].update(written=x['coordinates'][0]['totals']['applications'])),('change_reduced_fraction',lambda x:x['coordinates'][0]['comparisons']['written'].update(reduced_numerator=1)),('change_decimal',lambda x:x['coordinates'][0]['comparisons']['conditional_F010'].update(decimal='1.000000000000')),('omit_coordinate',lambda x:x['coordinates'].pop()),('substitute_primary',lambda x:x.update(primary_coordinate=['raw_untrimmed','NFC',UNITS[2]])),('omit_application',lambda x:x['whole_document_map']['manuscript_application_keys'].pop()),('demote_required_graph',lambda x:x['scope'].update(required_certificate_and_graph_data_for_L126=False)),('lose_whole_JSON',lambda x:x['acquisition']['L126_required_software'].pop()),('promote_optional_to_premise',lambda x:x['scope'].update(optional_validation_required_for_conditional=True)),('charge_sibling',lambda x:x['acquisition']['L126_local'].append('R1')),('invent_software_factor',lambda x:x['scope'].update(software_inclusive_factor=2)),('unknown_zero',lambda x:x['unknown_costs'].update(retained_external_proofs=0)),('claim_full_formal',lambda x:x['scope'].update(full_source_formalized=True)),('remove_expansion_disclosure',lambda x:x['interpretation'].update(whole_topic='compression achieved')),('wrong_title',lambda x:x['source_titles'].update(L126='Other source'))]
    out=[]
    for name,change in changes:
        x=copy.deepcopy(result);change(x)
        try:check_result(x,oracle,study,protocol)
        except (ValueError,KeyError):out.append(dict(name=name,rejected=True))
        else:raise ValueError('accepted negative control '+name)
    return out
