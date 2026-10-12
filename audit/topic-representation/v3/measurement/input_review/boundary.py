#!/usr/bin/env python3
"""Independent boundary review. No current author helper is imported."""
import argparse,collections,copy,hashlib,json,pathlib,re
from pypdf import PdfReader

def need(b,s):
    if not b: raise ValueError(s)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def bound(root,row):
    p=pathlib.Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path')
    data=(root/p).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact binding '+str(p));return root/p

def semantics(policy,docs,raw,reuse):
    need(policy['primary']['variant']=='calibrated_selected' and policy['primary']['normalization']=='NFC' and policy['primary']['unit']=='characters_without_whitespace','inherited primary')
    need(policy['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and policy['normalizations']==['NFC','NFKC'] and len(policy['units'])==5,'all30 coordinates')
    expected={'F010':13,'L126':13,'U_R':13,'R1':4,'R2':12,'CODE':16}
    need({r['key']:r['pages'] for r in docs['documents']}==expected and len(docs['documents'])==6,'complete six-PDF boundary')
    need(docs['physical_pages']==sum(expected.values())==71 and docs['written_pages']==55,'whole physical and written extent')
    need(docs['reusable_exact_rows']==['F010'] and set(docs['new_pdf_extraction_rows'])==set(expected)-{'F010'},'only SOURCE reused')
    need(docs['manuscript_source_keys']==['F010','L126'] and docs['manuscript_common_keys']==['U_R'] and docs['manuscript_application_keys']==['R1','R2'],'whole common and both applications')
    need(docs['pair_map']==[{'source':'F010','application':'R1','prepaid_documents':['U_R']},{'source':'L126','application':'R2','prepaid_documents':['U_R'],'required_files':['certificate/check.py','certificate/graph.json']}],'no sibling premise, complete required input')
    need(docs['no_sibling_application_dependency'] is True and docs['historical_old_U_or_CODE_free'] is False,'migration and full shared charge')
    need(reuse['F010']['all30_coordinates_preserved'] is True and reuse['F010']['pdf_identical'] is True,'all old source coordinates fixed')
    roles=collections.Counter(r['role'] for r in raw['files'])
    need(roles=={'optional_validation':9,'required_finite_certificate':1,'required_graph_data':1,'current_orchestration_driver':2,'partial_formal_evidence':4},'complete role inventory')
    need(len(raw['files'])==raw['raw_file_count']==17 and all(r['whole_file'] is True for r in raw['files']),'whole unique files')
    need(len({r['key'] for r in raw['files']})==17,'no aliases counted as files')
    req={r['key']:r for r in raw['files'] if r['role'].startswith('required_')}
    need(set(req)=={'certificate/check.py','certificate/graph.json'} and req['certificate/graph.json']['bytes']==19326,'required certificate and full data')
    need(sum(r.get('declarations',0) for r in raw['files'])==raw['partial_declarations']==22,'partial formal scope')
    need(raw['source_counterpart_inventory'] is None,'source software remains unknown')
    need(policy['symmetric_program_rule']['software_inclusive_factor'] is None and policy['factors_permitted'] is False and policy['ratio'] is None,'no input-stage factors')
    need(all(x is None for x in policy['unknowns'].values()),'unknown retained costs not zero')
    need(policy['new_source_credit']==policy['new_question_credit']==policy['new_formal_credit']==0,'no new credit')
    need('BOTH' in policy['symmetric_program_rule']['written_manuscripts'] and 'not conditional proof premises' in policy['symmetric_program_rule']['optional_validation'],'symmetric optional-code policy')

def run(study,packet,public):
    proto=packet/'protocol_freeze';m=read(proto/'manifest.json');need(sha((proto/'manifest.json').read_bytes())=='dc9b06df777ea9b27c8fcec7bef539689061b5b41254bcc4158d42f3ea4b11ae','fixed pre-extraction manifest')
    for row in m['exports']:bound(proto,row)
    p,d,r,u=[read(proto/(x+'.json')) for x in ['policy','document_map','raw_file_map','reuse_map']];semantics(p,d,r,u)
    bindings=[]
    def walk(x):
        if isinstance(x,dict):
            if {'path','bytes','sha256'}<=set(x):
                root=public if x['path'].startswith('audit/') else study
                bound(root,x);bindings.append(x)
            else:
                for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    for data in [p,d,r,u,m['predecessor']]:walk(data)
    physical={row['key']:len(PdfReader(study/row['path']).pages) for row in d['documents']}
    need(physical=={row['key']:row['pages'] for row in d['documents']},'actual PDF page counts')
    old=read(study/'topic_Representation_measurement_inputs/source_input_spec.json')['sources']['F010'];need(old['pdf_sha256']==d['documents'][0]['sha256'],'same F010 source edition')
    tex=study/'topic_Representation_L126_recovery_v2/volume/program-appendix.tex';s=tex.read_text();includes=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',s)
    needed={str((tex.parent/x).resolve()) for x in includes};roster={str((study/x['path']).resolve()) for x in r['files'] if x['role'] in ['optional_validation','required_finite_certificate']}
    need(len(includes)==10 and needed==roster,'ten exact complete code inclusions')
    need(not re.search(r'firstline|lastline|firstnumber|lastnumber',s),'no program pruning')
    migration=read(study/'topic_Representation_L126_migration_independent_review/review.json');need(migration['acquisition_scope']['F010_sibling_required_for_L126'] is False and migration['acquisition_scope']['required_graph_certificate_and_retained_inputs_still_required'],'accepted proof migration boundary')
    changes=[('drop_source',1,lambda x:x['documents'].pop(0)),('old_application',1,lambda x:x['documents'][3].update(pages=5)),('drop_required_data',2,lambda x:x['files'].__setitem__(10,{**x['files'][10],'role':'optional_validation'})),('demote_certificate',2,lambda x:x['files'][8].update(role='optional_validation')),('prune_program',2,lambda x:x['files'][0].update(whole_file=False)),('reuse_old_own',1,lambda x:x['reusable_exact_rows'].append('R1')),('restore_sibling',1,lambda x:x['pair_map'][1]['prepaid_documents'].append('R1')),('omit_common',1,lambda x:x.update(manuscript_common_keys=[])),('enable_ratio',0,lambda x:x.update(factors_permitted=True)),('zero_unknown',0,lambda x:x['unknowns'].update(source_programs=0)),('invent_software_factor',0,lambda x:x['symmetric_program_rule'].update(software_inclusive_factor=1)),('full_formal_claim',2,lambda x:x.update(partial_declarations=23))]
    controls=[]
    for name,i,f in changes:
        data=copy.deepcopy([p,d,r,u]);f(data[i])
        try:semantics(*data)
        except (ValueError,KeyError):controls.append({'name':name,'rejected':True})
        else:raise ValueError('mutation accepted '+name)
    return {'status':'PASS_PREEXTRACTION_BOUNDARY_ONLY','manifest_sha256':sha((proto/'manifest.json').read_bytes()),'actual_physical_pages':physical,'bound_records':len(bindings),'whole_program_inclusions':10,'raw_files':17,'controls':controls,'previous_mathematical_reviews_reused':['b855471dbb35482443c1047e3910e17f07cdbb08ed40bba4c51d716526ddf58a','245c635d713ad0b2ad3c9667405af0e61ced5360a5b3573646b19da8617dbdd1'],'final_extraction_acceptance':False,'factors':None}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--public-root',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');result=run(a.study_root,a.packet,a.public_root);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
