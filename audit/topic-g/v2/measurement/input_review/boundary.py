#!/usr/bin/env python3
"""Independent full source/program/policy boundary and semantic controls."""
import copy, json, pathlib, re
from recount import need,read,sha
ROLES={'phase265_exceptional.g':'required mathematical computation','phase265_residues.g':'required mathematical computation','phase186_witt_derived_check.g':'required mathematical computation','phase182_mathieu_fibers.g':'required mathematical computation','phase186_witt_validate.py':'required witness verification','phase186_witt_lean_generate.py':'required certificate bridge','phase265_frame_control.g':'validation','phase265_plane_models.g':'validation','phase186_hermitian_labels.g':'validation','phase182_deleted_line_check.py':'validation','phase182_inversive_geometry_check.py':'validation','hermitian_unital_check.g':'validation','phase199_path_length.py':'validation'}
FORMAL={'ResidueConnectivity.lean':1,'DeterminantFibers.lean':4,'HermitianPlaneTransport.lean':13,'DeletedLineFourResidue.lean':7,'WittDerivedPlanes.lean':9,'CyclicBiplaneDelta.lean':6}

def semantics(study,p,s,r,c,g):
    need(set(s['sources'])=={'L009','L092'} and set(r['ours'])=={'U_G','G1','G2','CODE'},'all six complete documents')
    need({k:v['pages'] for k,v in {**s['sources'],**r['ours']}.items()}=={'L009':25,'L092':14,'U_G':12,'G1':8,'G2':22,'CODE':20},'101 physical pages')
    need(p['source_intake_closed'] is True and p['factors_permitted'] is False and p['ratio'] is None,'input-only closed intake')
    need(all(p[k]==0 for k in ['new_source_credit','new_question_credit']),'no credits')
    expected=read(study/'topic_G_current_edition/scope.json')
    need(expected['counts']=={'L009':44,'L092':35,'proof_spans':34},'accepted counts')
    for name,old in [('source_rows','rows'),('proof_spans','proof_spans'),('complete_application_closure','complete_application_closure'),('qualification','qualification'),('source_bindings','source_bindings')]:need(c[name]==expected[old],'exact admitted '+name)
    need(c['row_count']==79 and c['principal_contracts']==2,'exact source scope')
    rows=r['complete_programs'];need(len(rows)==13 and {pathlib.Path(x['path']).name:x['role'] for x in rows}==ROLES,'four/two/seven entire programs')
    need(all(x['complete_original_file'] is True for x in rows),'no pruned programs')
    drivers=r['complete_operational_drivers'];need(len(drivers)==3 and {pathlib.Path(x['path']).name for x in drivers}=={'check.py','render.py','binding_controls.py'},'three complete operational files separately')
    lean=r['complete_formal_files'];need(len(lean)==6 and {pathlib.Path(x['path']).name:len(x['declarations']) for x in lean}==FORMAL,'six complete files and40 component declarations')
    need(r['formal_scope']==read(study/'topic_G_current_edition/formal/scope.json'),'same partial formal scope')
    for d,keys in [(r,['retained_external_cost','graphics_cost']),(s,['graphic_cost','historical_program_cost']),(g,['graphic_cost','raster_lettering_cost']),(c,['retained_BDL_full_proof_cost','retained_Kantor_full_proof_cost','graphics_cost'])]:
        need(all(d[k] is None for k in keys),'unpriced inputs remain unknown')
    need(g['full_visible_text_claim'] is False and g['primary_images_exported'] is False,'extractable-text boundary')
    cmp=p['comparison_policy'];need(cmp==r['comparison_policy'],'same comparison policy')
    need(cmp['written']=='sum of both whole source PDFs / (whole U_G + whole G1 + whole G2), first comparison','written-first common theory once')
    need('never added to CODE' in cmp['raw_program_alternative'] and 'whole CODE' in cmp['including_program'],'alternate program representation')
    need('after acquiring whole U_G and the complete programme' in cmp['conditional'] and cmp['cross_topic_deduplication'] is False,'whole common/program acquisition')
    need(r['program_representation']['pruning'] is False,'no hidden program pruning')
    b=(study/r['appendix_tex']['path']).read_bytes();need(sha(b)==r['appendix_tex']['sha256'],'complete listing TeX')
    inc=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',b.decode());need(len(inc)==13 and set(inc)=={'programs/'+x for x in ROLES},'whole thirteen program inclusions once')
    need(not any(x in b.decode() for x in ['firstline','lastline','firstnumber','lastnumber']),'no listing cuts')

def run(study,packet,public):
    names=['policy','source_input_spec','replacement_input_spec','source_contract_boundary','graphic_inventory'];data=[read(packet/(n+'.json')) for n in names];semantics(study,*data)
    p,s,r,c,g=data;bindings=[]
    for k in ['author','current_edition','root_adoption','accepted_scope','program_inventory']:
        row=p[k];b=(study/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'scientific '+k);bindings.append(row)
    pub=read(packet/'publication_binding.json');need(sha((public/pub['admission']['path']).read_bytes())==pub['admission']['sha256'],'public science admission')
    for key,row in pub['documents'].items():need(sha((public/row['public_path']).read_bytes())==row['sha256']==r['ours'][key]['pdf_sha256'],'exact public PDF '+key)
    controls=[]
    changes=[('omit_source',1,lambda x:x['sources'].pop('L092')),('omit_application',2,lambda x:x['ours'].pop('G2')),('prune_code',2,lambda x:x['complete_programs'][0].update(complete_original_file=False)),('omit_validation',2,lambda x:x['complete_programs'].pop()),('demote_premise',2,lambda x:x['complete_programs'][0].update(role='validation')),('omit_bridge',2,lambda x:x['complete_programs'].pop(4)),('omit_driver',2,lambda x:x['complete_operational_drivers'].pop()),('omit_formal',2,lambda x:x['complete_formal_files'][0]['declarations'].pop()),('zero_external',2,lambda x:x.update(retained_external_cost=0)),('zero_graphics',4,lambda x:x.update(graphic_cost=0)),('erase_qualification',3,lambda x:x.update(qualification=[])),('omit_contract',3,lambda x:x['source_rows'].pop()),('new_credit',0,lambda x:x.update(new_question_credit=1)),('whole_visible_claim',4,lambda x:x.update(full_visible_text_claim=True)),('omit_cover_page',1,lambda x:x['sources']['L009'].update(pages=24))]
    for name,i,change in changes:
        d=copy.deepcopy(data);change(d[i])
        try:semantics(study,*d)
        except (ValueError,KeyError):controls.append(dict(name=name,rejected=True))
        else:raise ValueError('Control accepted: '+name)
    return dict(status='PASS_INDEPENDENT_SCIENTIFIC_INPUT_BOUNDARY',source_rows=79,current_spans=34,documents=6,physical_pages=101,whole_programs=13,roles=dict(required_finite=4,witness_certificate_bridges=2,validation=7),separate_drivers=3,separate_formal_files=6,prior_scoped_declarations=40,public_pdf_routes=4,scientific_bindings=bindings,controls=controls,new_source_credit=0,new_question_credit=0,new_formal_credit=0,factors=None)
if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--study-root',type=pathlib.Path,required=True);a.add_argument('--packet',type=pathlib.Path,required=True);a.add_argument('--public-root',type=pathlib.Path,required=True);a.add_argument('--out',type=pathlib.Path,required=True);o=a.parse_args();need(not o.out.exists() and not o.out.is_symlink(),'fresh out');v=run(o.study_root,o.packet,o.public_root);o.out.write_text(json.dumps(v,indent=2)+'\n');print(v['status'])
