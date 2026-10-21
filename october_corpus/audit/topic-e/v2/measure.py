#!/usr/bin/env python3
"""Measure the readable edition of complete three-application Topic E proofs.

Private: --root STUDY --sources-root STUDY
Public: --repo REPO --sources-root EXTERNAL_PRIMARY_ROOT
Both modes verify identical bound PDFs and code. Optional --locations maps
private relative artifact names to repository-relative paths. No primary text
is emitted. Requires pypdf6.13.0. All outputs must be fresh.
"""
import argparse,copy,hashlib,importlib.util,json,re,sys,unicodedata
from pathlib import Path
sys.dont_write_bytecode=True
PROTOCOL_SHA256='46e5b99c7e0aefd85f4687e4031470332cf8134d07c3dc9496fc7f142f6afbbb'
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError('TOPIC_E_COMPARISON_REJECT '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def plus(items):return sum(items)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path);ap.add_argument('--repo',type=Path)
    ap.add_argument('--sources-root',type=Path,required=True)
    ap.add_argument('--locations',type=Path)
    ap.add_argument('--protocol',type=Path,default=ROOT/'readable_protocol.json')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();need(args.root is not None or args.repo is not None,'root or repo required')
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output required')
    pb=args.protocol.read_bytes();need(sha(pb)==PROTOCOL_SHA256,'frozen comparison protocol')
    p=json.loads(pb);locations=p['public_locations'].copy()
    if args.locations:locations.update(json.loads(args.locations.read_text()))
    def locate(name,primary=False):
        candidates=[]
        if primary:candidates=[args.sources_root/name,args.sources_root/Path(name).name]
        else:
            if args.root:candidates.append(args.root/name)
            if args.repo:
                if name in locations:
                    mapped=args.repo/locations[name];candidates += [mapped,mapped.with_name(Path(name).name)]
                candidates.append(args.repo/name)
        for candidate in candidates:
            if candidate.is_file():return candidate
        raise ValueError('TOPIC_E_COMPARISON_REJECT missing '+name)
    resolved={}
    def bound(row):
        path=locate(row['path']);b=path.read_bytes()
        need(sha(b)==row['sha256'],'bound file '+row['path'])
        if 'bytes' in row:need(len(b)==row['bytes'],'bytes '+row['path'])
        resolved[row['path']]=str(path);return b
    old=json.loads(bound(p['old_boundary']));helper=bound(p['helper'])
    spec=importlib.util.spec_from_file_location('topic_E_bound_ruler',locate(p['helper']['path']))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    need(m.pypdf.__version__==p['pypdf_version'],'pypdf version')
    review=json.loads(bound(p['independent_mathematical_review']))
    need(review['status']=='ACCEPTED_COMPLETE_WRITTEN_PROOFS_AND_REQUIRED_FINITE_CLOSURE','accepted complete mathematical review')
    need(not review['unresolved_mathematical_objections'],'no outstanding mathematical objection')
    edition=json.loads(bound(p['readable_edition_review']))
    need(edition['status']=='ACCEPTED_LANGUAGE_EDITION_OF_PREVIOUSLY_REVIEWED_PROOFS','language edition review')
    need(edition['root_acceptance_reported_in_thread'] and not edition['unresolved_mathematical_objections'],'independent language delta accepted')
    need(not edition['new_mathematical_credit'] and not edition['proof_library_or_program_cost_deleted'],'unchanged mathematical scope and costs')
    for row in edition['bound_artifacts']:bound(row)
    ledger=json.loads(bound(p['literal_edit_ledger']))
    def check_literal_edits(rows):
        for row in rows:
            current=bound(row['new']).decode()
            for edit in reversed(row['edits']):
                need(current.count(edit['new'])==1,'literal reverse edit uniqueness')
                current=current.replace(edit['new'],edit['old'],1)
            need(sha(current.encode())==row['old']['sha256'],'complete old TeX recovered by reverse edits')
    check_literal_edits(ledger['files'])
    bound(p['prior_comparison_protocol'])
    prior_result=json.loads(bound(p['prior_comparison_result']))
    for row in p['new_scientific_files']:bound(row)
    need(p['sources']==old['sources'] and p['old']==old['ours'],'unchanged old boundary')
    need(p['old_required_programs']==old['required_programs'],'complete old program boundary')
    need(set(p['new'])=={'New_U','New_A1','New_A2','New_A3','New_Code','New_Validation'},'all six new artifacts')
    need(p['metrics']==old['metrics'] and p['normalizations']==old['normalizations'],'same ten metrics')
    raw={};texts={};raw_glyph={};costs={};input_paths={}
    for group in ('sources','old','new'):
        costs[group]={}
        for key,row in p[group].items():
            path=locate(row['path'],group=='sources');input_paths[key]=str(path)
            rr=dict(row,path=str(path.resolve()))
            a,b,c=m.document(Path('/'),key,rr)
            raw[key]=a;texts[key]=c;raw_glyph[key]=b
            costs[group][key]={form:m.metrics(c,form) for form in p['normalizations']}
            for form in p['normalizations']:
                before=m.metrics(b,form)
                need(all(before[k]==costs[group][key][form][k] for k in p['metrics']),'glyph invariance '+key)
    code={};programs=[]
    for side,rows in [('old',p['old_required_programs']),('new',p['new_programs'])]:
        for row in rows:
            b=bound(row);code[row['path']]=b
            need(re.sub(r'\s+','',b.decode()) in re.sub(r'\s+','',texts[row['appendix']]),'complete program appendix '+row['path'])
            programs.append(dict(side=side,path=row['path'],sha256=row['sha256'],bytes=len(b),appendix=row['appendix'],complete=True))
    # The two new TeX blocks contain exact bytes, including comments/controls.
    for row in p['new_programs']:
        tex_path=p['new'][row['appendix']]['path'].removesuffix('.pdf')+'.tex'
        tex=locate(tex_path).read_bytes()
        need(tex.count(code[row['path']])==1,'exact single program occurrence in TeX '+row['path'])
    comparisons={};chronology={}
    for form in p['normalizations']:
        comparisons[form]={};chronology[form]={}
        for metric in p['metrics']:
            c={k:v[form][metric] for group in costs.values() for k,v in group.items()}
            src=plus(c[k] for k in ['L083','L079','L021'])
            ow=plus(c[k] for k in ['U_E','A1','A2','A3']);oc=c['Code_shared']+c['Code_A3']
            nw=plus(c[k] for k in ['New_U','New_A1','New_A2','New_A3']);nc=c['New_Code'];nv=c['New_Validation']
            comparisons[form][metric]=dict(source_full_manuscripts=src,old_written=ow,old_all_required_programs=oc,old_written_and_programs=ow+oc,new_written=nw,new_required_program=nc,new_validation_program=nv,new_written_and_required=nw+nc,new_written_required_and_validation=nw+nc+nv,
                source_over_old_written=src/ow,source_over_old_written_and_programs=src/(ow+oc),source_over_new_written=src/nw,source_over_new_written_and_required=src/(nw+nc),source_over_new_written_required_and_validation=src/(nw+nc+nv),
                old_over_new_written=ow/nw,old_over_new_with_required= (ow+oc)/(nw+nc),old_over_new_including_validation=(ow+oc)/(nw+nc+nv),written_characters_removed=ow-nw,program_change_required_only=oc-nc,program_change_including_validation=oc-nc-nv,
                exact_all_artifact_factor=None,unconditional_library_factor=None,
                conditional_application_factors={l:dict(source_full_manuscript=c[l],complete_local_application=c[a],factor=c[l]/c[a]) for l,a in [('L083','New_A1'),('L079','New_A2'),('L021','New_A3')]},
                conditional_application_basis='Complete common manuscript and required common program are already available; their full costs are included once in the combined topic total, not zero.',
                previous_common_proof_draft_written=prior_result['comparisons'][form][metric]['new_written'],
                readable_prose_change=nw-prior_result['comparisons'][form][metric]['new_written'])
            chronology[form][metric]=dict(stage_order=['acquisition','L083','L079','L021'],
                source_marginal=[0,c['L083'],c['L079'],c['L021']],source_cumulative=[0,c['L083'],c['L083']+c['L079'],src],
                old_written_marginal=[c['U_E'],c['A1'],c['A2'],c['A3']],old_written_cumulative=[c['U_E'],c['U_E']+c['A1'],c['U_E']+c['A1']+c['A2'],ow],
                old_with_code_marginal=[c['U_E']+c['Code_shared'],c['A1'],c['A2'],c['A3']+c['Code_A3']],old_with_code_cumulative=[c['U_E']+c['Code_shared'],c['U_E']+c['Code_shared']+c['A1'],c['U_E']+c['Code_shared']+c['A1']+c['A2'],ow+oc],
                new_written_marginal=[c['New_U'],c['New_A1'],c['New_A2'],c['New_A3']],new_written_cumulative=[c['New_U'],c['New_U']+c['New_A1'],c['New_U']+c['New_A1']+c['New_A2'],nw],
                new_with_required_marginal=[c['New_U']+nc,c['New_A1'],c['New_A2'],c['New_A3']],new_with_required_cumulative=[c['New_U']+nc,c['New_U']+nc+c['New_A1'],c['New_U']+nc+c['New_A1']+c['New_A2'],nw+nc],
                new_including_validation_marginal=[c['New_U']+nc+nv,c['New_A1'],c['New_A2'],c['New_A3']],new_including_validation_cumulative=[c['New_U']+nc+nv,c['New_U']+nc+nv+c['New_A1'],c['New_U']+nc+nv+c['New_A1']+c['New_A2'],nw+nc+nv])
    rejected=[]
    def reject(label,action):
        try:action()
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('negative control accepted '+label)
    changed=copy.deepcopy(p['new']['New_U']);changed['included_spans'][0]['end']-=1
    reject('changed_complete_new_manuscript_boundary',lambda:m.spans(raw['New_U'],changed))
    changed=copy.deepcopy(p['new']['New_A3']);changed['excluded_furniture'][0]['start']+=1
    reject('shifted_new_footer',lambda:m.spans(raw['New_A3'],changed))
    changed=copy.deepcopy(p['sources']['L021']);changed['glyph_substitutions'][0]['output']=''
    reject('deleted_visible_source_parenthesis',lambda:m.calibrate(raw['L021'],changed,'L021'))
    row=p['new_programs'][0]
    reject('changed_required_program',lambda:need(sha(code[row['path']]+b' ')==row['sha256'],'changed required program'))
    row2=p['new_programs'][1]
    reject('validation_sensitivity_without_program',lambda:need(re.sub(r'\s+','',code[row2['path']].decode()) in 'empty','full validation absent'))
    changed=copy.deepcopy(p);changed['new_programs'].pop()
    reject('silently_drop_validation_coordinate',lambda:need(sha((json.dumps(changed,indent=2,ensure_ascii=False)+'\n').encode())==PROTOCOL_SHA256,'changed scope'))
    changed=copy.deepcopy(p);changed['historical_program_cost']=0
    reject('unknown_historical_code_forged_zero',lambda:need(sha((json.dumps(changed,indent=2,ensure_ascii=False)+'\n').encode())==PROTOCOL_SHA256,'changed unknown'))
    first=Path(input_paths['New_U'])
    reject('changed_new_pdf_bytes',lambda:need(sha(first.read_bytes()+b' ') == p['new']['New_U']['pdf_sha256'],'PDF changed'))
    altered=copy.deepcopy(ledger['files']);altered[0]['edits'][0]['old']+=' '
    reject('unrecorded_or_changed_language_edit',lambda:check_literal_edits(altered))
    reject('old_review_silently_rebound_to_new_edition',lambda:need(edition['prior_complete_review']['sha256']==sha(b'changed old proof review'),'prior complete review changed'))
    # Exact arithmetic and closure checks independent of rounded display values.
    for form in chronology:
        for metric,ch in chronology[form].items():
            for prefix in ['source','old_written','old_with_code','new_written','new_with_required','new_including_validation']:
                need(ch[prefix+'_cumulative']==[sum(ch[prefix+'_marginal'][:i+1]) for i in range(4)],'cumulative account '+prefix)
    result=dict(status='PASS_READABLE_COMPARISON_AUTHOR_REPLAY',protocol_sha256=PROTOCOL_SHA256,checker_sha256=sha(Path(__file__).read_bytes()),pypdf_version=m.pypdf.__version__,scope=p['scope'],costs=costs,comparisons=comparisons,chronology=chronology,
        complete_programs=programs,program_byte_lengths={x['path']:x['bytes'] for x in programs},glyph_metric_invariance_all_documents=True,primary=p['primary'],new_pages={k:v['pages'] for k,v in p['new'].items()},old_pages={k:v['pages'] for k,v in p['old'].items()},source_pages={k:v['pages'] for k,v in p['sources'].items()},
        negative_controls=rejected,readable_edition=True,previous_public_edition_commit=p['prior_public_edition_commit'],literal_edit_reversal_verified=True,conditioned_application_ratio_definition=p['conditioned_application_ratios'],diagnostic_relocation_sensitivity=True,retained_library_cost=None,historical_program_cost=None,full_Lean_cost=None,exact_all_artifact_factor=None,conditions=p['conditions'],cost_allocation=p['cost_allocation'],no_new_source_question_or_priority_credit=True,
        interpretation='The source/new written factor compares full manuscript lengths for accepted main results. Known program coordinates include complete current required artifacts, with a separate complete-validation sensitivity. They are not exact all-artifact or unconditional proof costs. Cumulative stages use declared whole-file charging, not inferred historical discovery or repeated sawtooth evidence.')
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result['comparisons']['NFC']['characters_without_whitespace'],indent=2))
if __name__=='__main__':main()
