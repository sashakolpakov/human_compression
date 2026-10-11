#!/usr/bin/env python3
"""Independent complete-document/program/scientific boundary, not new science."""
import copy,json,pathlib,re,subprocess
from recount import need,read,sha
PROGRAMS={'phase177_hexagon_check.g','phase188_gadget_check.g'}
DRIVERS={'phase188_verify.py','phase193_public_check.py'}
FORMAL={'RecognizableRestriction.lean':8,'CompletedHexagonCounterexample.lean':4}

def semantics(study,p,s,r,c,g):
    need(set(s['sources'])=={'F010'} and set(r['ours'])=={'U_R','R1','CODE'},'all four complete documents')
    need({k:v['pages'] for k,v in {**s['sources'],**r['ours']}.items()}=={'F010':13,'U_R':5,'R1':5,'CODE':4},'all27physicalpages including reference page')
    need(p['factors_permitted_at_this_stage'] is False and p['ratio'] is None,'input only')
    need(p['source_question_scope']=='Question2.4 is already answered by the source TheoremA; no new answer is claimed.','source answers its question')
    expected=read(study/'topic_Representation_volume/scope.json');need(expected['intake_closed'] is True,'closed source intake')
    for k in ['inherited_source_block_order','proof_spans','precise_hypotheses','source_qualifications','exclusions','validation_boundary']:need(c[k]==expected[k],'same admitted '+k)
    need(c['source_rows']==expected['contracts'] and c['attribution']==expected['source'],'same six complete source blocks and attribution')
    need(c['row_count']==len(c['source_rows'])==6 and len(c['proof_spans'])==13 and c['principal_contracts']==1,'six blocks13contexts one prior contract')
    need(c['new_source_credit']==0 and c['new_question_credit']==0,'no new credits')
    rows=r['complete_validation_programs'];need(len(rows)==2 and {pathlib.Path(x['path']).name for x in rows}==PROGRAMS,'two complete programs')
    need(all(x['complete_original_file'] is True and x['role']=='finite_validation' and x['classification']=='validation' and x['uniform_written_proof_premise'] is False for x in rows),'validation only no pruning')
    drivers=r['complete_operational_drivers'];need(len(drivers)==2 and {pathlib.Path(x['path']).name for x in drivers}==DRIVERS and all(x['role']=='historical_operational_driver' for x in drivers),'two historical drivers separately')
    lean=r['complete_formal_files'];need(len(lean)==2 and {pathlib.Path(x['path']).name:len(x['declarations']) for x in lean}==FORMAL,'12 scoped declarations two entire files')
    need(r['formal_scope']==read(study/'topic_Representation_volume/formal/scope.json'),'same partial formal scope, historical status preserved')
    for d,keys in [(r,['retained_external_cost','graphics_cost']),(s,['graphic_cost','historical_program_cost']),(g,['graphic_cost']),(c,['retained_external_cost','graphics_cost']),(p,['retained_external_cost','source_graphics_cost','historical_program_cost'])]:need(all(d[k] is None for k in keys),'unknown is not zero')
    need(g['complete_visible_text_claim'] is False and g['primary_images_exported'] is False,'extractable-text only')
    need(set(g['documents']['F010']['vector_figure_pages'])=={'5','7','9','10','11','12'},'all six vector-figure pages')
    need(all(d['geometry_layout_cost'] is None for d in g['documents'].values()),'formula/diagram geometry remains unknown')
    cmp=p['comparison_policy'];need(cmp==r['comparison_policy'],'same policy')
    need(cmp['written']=='whole F010 / (whole U_R + whole R1), first comparison','whole written comparison first')
    need(cmp['including_program']=='whole F010 / (whole U_R + whole R1 + whole CODE), separate complete-validation-inclusive comparison','whole appendix separate')
    need('both complete raw validation programs' in cmp['raw_program_alternative'] and 'alternative representation' in cmp['raw_program_alternative'],'whole raw files alternative')
    need('after acquiring whole U_R and both complete validation programs' in cmp['conditional'] and cmp['cross_topic_deduplication'] is False,'complete common+program acquisition per topic')
    need(r['program_representation']['pruning'] is False and 'not added to CODE' in r['program_representation']['alternative'],'no pruning/double charge')
    need(r['program_representation']['drivers_count']==2 and r['program_representation']['drivers_in_appendix'] is False,'drivers not hidden in code')
    b=(study/r['appendix_tex']['path']).read_bytes();need(sha(b)==r['appendix_tex']['sha256'],'accepted full listing TeX')
    inc=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',b.decode());need(len(inc)==2 and set(inc)=={'programs/'+x for x in PROGRAMS},'whole program inclusions once')
    need(not any(x in b.decode() for x in ['firstline','lastline','firstnumber','lastnumber']),'no listing truncation')

def run(study,packet,public):
    data=[read(packet/(n+'.json')) for n in ['policy','source_input_spec','replacement_input_spec','source_contract_boundary','graphic_inventory']];semantics(study,*data);p,s,r,c,g=data
    bindings=[]
    for k in ['author','independent_review','role_delta','root_adoption','accepted_scope']:
        row=p[k];b=(study/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'scientific '+k);bindings.append(row)
    pub=read(packet/'publication_binding.json');need(sha((public/pub['admission']['path']).read_bytes())==pub['admission']['sha256'],'public admission')
    routes=[]
    for k,row in pub['documents'].items():
        need(sha((public/row['public_path']).read_bytes())==row['sha256']==r['ours'][k]['pdf_sha256'],'public currentPDF')
        b=subprocess.run(['git','show',pub['commit']+':'+row['public_path']],cwd=public,check=True,capture_output=True).stdout;need(sha(b)==row['sha256'],'committed PDF');routes.append(row['public_path'])
    for k in ['complete_validation_programs','complete_operational_drivers','complete_formal_files']:
        need(pub[k]==r[k],'public full rawfile bindings')
        for row in pub[k]:
            route=row['path'].replace('topic_Representation_volume/','papers/topic-representation/v2/',1);b=(public/route).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'current full rawfile')
            b=subprocess.run(['git','show',pub['commit']+':'+route],cwd=public,check=True,capture_output=True).stdout;need(sha(b)==row['sha256'],'committed rawfile');routes.append(route)
    changes=[('omit_source',1,lambda x:x['sources'].pop('F010')),('omit_application',2,lambda x:x['ours'].pop('R1')),('omit_reference_only_page',2,lambda x:x['ours']['U_R'].update(pages=4)),('prune_code',2,lambda x:x['complete_validation_programs'][0].update(complete_original_file=False)),('omit_validation',2,lambda x:x['complete_validation_programs'].pop()),('promote_samples_to_premise',2,lambda x:x['complete_validation_programs'][0].update(uniform_written_proof_premise=True)),('omit_driver',2,lambda x:x['complete_operational_drivers'].pop()),('omit_formal',2,lambda x:x['complete_formal_files'][0]['declarations'].pop()),('zero_external',2,lambda x:x.update(retained_external_cost=0)),('zero_graphics',4,lambda x:x.update(graphic_cost=0)),('erase_qualification',3,lambda x:x['source_qualifications'].pop()),('omit_contract',3,lambda x:x['source_rows'].pop()),('new_credit',3,lambda x:x.update(new_question_credit=1)),('whole_visible_claim',4,lambda x:x.update(complete_visible_text_claim=True)),('drop_normality',3,lambda x:x['precise_hypotheses'].update(normal_subgroup_required=False)),('enable_ratio',0,lambda x:x.update(factors_permitted_at_this_stage=True))]
    controls=[]
    for name,i,change in changes:
        d=copy.deepcopy(data);change(d[i])
        try:semantics(study,*d)
        except (ValueError,KeyError):controls.append(dict(name=name,rejected=True))
        else:raise ValueError('Control accepted '+name)
    return dict(status='PASS_INDEPENDENT_COMPLETE_INPUT_BOUNDARY',source_blocks=6,current_contexts=13,documents=4,physical_pages=27,complete_programs=2,roles=dict(validation=2,uniform_computational_premises=0),separate_historical_drivers=2,separate_formal_files=2,scoped_declarations=12,public_current_and_committed_routes=routes,scientific_bindings=bindings,controls=controls,new_source_credit=0,new_question_credit=0,new_formal_credit=0,factors=None)
