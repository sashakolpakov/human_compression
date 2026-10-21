#!/usr/bin/env python3
"""Validate exact A10 pre-count boundaries; never extract, score or divide text."""
import argparse, collections, copy, hashlib, json
from pathlib import Path
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
def need(b,m):
    if not b: raise ValueError('A10_PRECOUNT: '+m)
def read(n): return json.loads((HERE/n).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(p,b):need(p.stat().st_size==b['bytes'] and sha(p)==b['sha256'],'exact bytes '+str(p))

def coarse(o,rp):
    role=o['role'];name=Path(o['path']).name
    if role=='required_program_or_data': return 'required_data' if name=='phase78_n009_integration_data.g' else 'required_program'
    if role=='required mathematical program or complete source roster':return 'required_data' if name.endswith('.json') else 'required_program'
    if role=='inherited_auxiliary':return 'optional_validation' if name=='controls.py' else 'operational'
    d={**rp['explicit_role_map'],**rp['additional_role_map']}
    need(role in d,'no unmatched-role fallback')
    return d[role]

def group_classes(classes,rp):
    need(bool(classes) and all(c in rp['content_precedence'] for c in classes),'known content roles')
    return min(classes,key=rp['content_precedence'].index)

def semantic(p,d,r,rp,a,i,plan):
    old=read('baseline/policy.json');old_docs=read('baseline/documents.json')['documents'];byold={x['id']:x for x in old_docs}
    need(p['source_ids']==old['source_ids']+['L003'] and p['source_to_application']==dict(old['source_to_application'],L003='A10'),'one exact additional original')
    for k in ['primary','variants','normalizations','metrics','pypdf_version']:need(p[k]==old[k],'fixed inherited policy '+k)
    need(p['primary']['variant']=='calibrated_selected' and p['primary']['normalization']=='NFC' and p['primary']['metric']=='characters_without_whitespace','fixed primary')
    need(p['common_documents']==['U','U_HEX','U_STRUCT'] and p['common_pages']==41 and p['source_pages']==152 and p['application_pages']==63,'complete common/source/apps')
    need(p['pdf_documents']==29 and p['physical_pages']==286 and p['program_appendix_pages']==30,'complete physical boundary')
    need(p['inherited_PDF_metric_cells']==630 and p['expected_new_PDF_metric_cells']==240 and p['expected_total_PDF_metric_cells']==870,'native PDF cell extent')
    need(p['inherited_raw_metric_cells']==450 and p['expected_new_raw_metric_cells']==1580 and p['expected_total_raw_metric_cells']==2030,'whole-file cell extent')
    need(not p['new_metrics_evaluated'] and not p['new_raw_metrics_evaluated'] and not p['input_accepted'] and p['science_accepted'],'no premature input result')
    need(p['ratios'] is None and p['software_inclusive_factor'] is None and all(v is None for v in p['unknown_costs'].values()),'unknown costs/factors remain null')
    need(all(p[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']) and not p['new_scientific_execution'] and not p['new_Lean_compile'],'scope and credit')
    need(not p['complete_printed_program_representation'] and not p['old_L121_application_cells_reused'] and not p['old_nine_application_invariance_claim'],'no stale appendix/application claim')
    rows=d['documents'];by={x['id']:x for x in rows};need(len(rows)==len(by)==29,'unique native PDFs')
    need(all(x['whole_document'] for x in rows),'whole PDF scope')
    expect={'source':152,'common':41,'application':63,'complete_program_appendix':30}
    need({k:sum(x['pages'] for x in rows if x['kind']==k) for k in expect}==expect,'actual page-kind sums')
    need(sum(x['pages'] for x in rows)==286,'total native pages')
    inherited=[x for x in rows if not x['new_extraction']];new=[x for x in rows if x['new_extraction']]
    need(len(inherited)==21 and sum(x['pages'] for x in inherited)==229 and len(new)==8 and sum(x['pages'] for x in new)==57,'exact reuse/new boundary')
    for x in inherited:
        oldx=byold[x['id']];need(x['file']==oldx['file'] and x['pages']==oldx['pages'] and x['kind']==oldx['kind'],'reuse only identical whole PDF')
    need(set(x['id'] for x in new)=={'L003','U_HEX','U_STRUCT','A9','A10_MAIN','A10_STRUCT','A10_CORR','A10_768'},'fresh eight documents')
    need([by[k]['pages'] for k in p['common_documents']]==[23,14,4],'all theory paid')
    need([by[k]['pages'] for k in ['A9','A10_MAIN','A10_STRUCT','A10_CORR','A10_768']]==[1,7,4,4,2],'whole new application components')
    need(by['A9']['file']['sha256']!=byold['A9']['file']['sha256'],'old A9 cannot substitute new adapter')
    excluded={x['file']['sha256'] for x in d['excluded_current_PDFs']};need(len(excluded)==3 and not excluded.intersection(x['file']['sha256'] for x in rows),'exclude prior A9 and convenience bundles')
    need(d['application_documents']==p['application_documents']==a['applications'],'complete bundle routing')
    need(rp['content_precedence']==['required_program','required_data','optional_validation','operational','partial_formal','output_receipt'],'explicit role precedence')
    need(rp['required_role_dominates_output'] and rp['retain_every_occurrence_role'] and rp['classes_are_disjoint_only_after_content_grouping'],'no overlapping cost sum')
    occ=r['occurrences'];groups=r['contents'];need(len(occ)==253 and len(groups)==203 and r['accepted_assembly_occurrences']==252 and r['accepted_assembly_unique_contents']==202 and r['additional_operational_wrappers']==1,'full accepted union plus wrapper')
    byhash={};byid={}
    for o in occ:
        need(o['whole_file'],'whole raw file');c=coarse(o,rp);need(o['coarse_class']==c and o['mathematical_premise']==(c in ['required_program','required_data']),'actual occurrence role')
        byhash.setdefault(o['sha256'],[]).append(o);need(o['occurrence_id'] not in byid,'unique occurrence id');byid[o['occurrence_id']]=o
    need(len(byhash)==203 and len({g['id'] for g in groups})==203,'whole-content grouping')
    oldraw=read('baseline/raw_inventory.json')['files'];oldhash={x['file']['sha256']:x['id'] for x in oldraw}
    need(set(oldhash)<=set(byhash),'all45 old whole files still present')
    for g in groups:
        os=byhash[g['sha256']];roles=sorted({o['role'] for o in os});cs=sorted({o['coarse_class'] for o in os})
        need(g['occurrence_ids']==[o['occurrence_id'] for o in os] and g['roles']==roles and g['coarse_roles']==cs,'complete nonexclusive role evidence')
        need(all(o['bytes']==g['bytes'] for o in os) and g['accounting_class']==group_classes(cs,rp),'one disjoint content class')
        need(g['mathematical_premise']==any(c in ['required_program','required_data'] for c in cs),'required input not demoted')
        need(g['inherited_A9_raw_id']==oldhash.get(g['sha256']),'reuse exact complete contents only')
    expected={'required_program':28,'required_data':71,'operational':17,'optional_validation':5,'partial_formal':16,'output_receipt':66}
    need(dict(collections.Counter(g['accounting_class'] for g in groups))==expected==r['disjoint_content_class_counts'],'disjoint coarse totals')
    need(a['required_whole_content_ids']==[g['id'] for g in groups if g['mathematical_premise']] and len(a['required_whole_content_ids'])==99,'whole99 required contents')
    need(a['common_documents']==p['common_documents'] and a['whole_common_pages']==41 and a['common_charged_once'] and not a['sibling_application_premise'],'full conditional acquisition')
    need(i['reuse_document_ids']==[x['id'] for x in inherited] and i['reuse_PDF_cells']==630 and i['reuse_raw_cells']==450 and i['unchanged_application_ids']==[f'A{j}' for j in range(1,9)] and i['changed_application_ids']==['A9'],'precise conservation boundary')
    need(set(x['id'] for x in plan['fresh_documents'])==set(x['id'] for x in new) and not plan['all_new_PDF_audits_complete'] and plan['new_glyph_maps'] is None and plan['new_furniture_masks'] is None and plan['independent_input_acceptance_required_before_factors'],'audit remains explicit work before counts')
    return True

def controls(args):
    changes=[
      ('drop whole common',lambda x:x[0].update(common_pages=23)),
      ('switch primary',lambda x:x[0]['primary'].update(variant='raw_untrimmed')),
      ('omit source page',lambda x:next(z for z in x[1]['documents'] if z['id']=='L003').update(pages=20)),
      ('reuse changed adapter',lambda x:next(z for z in x[1]['documents'] if z['id']=='A9').update(new_extraction=False)),
      ('omit companion',lambda x:x[1]['documents'].pop()),
      ('append convenience bundle',lambda x:x[1]['documents'].append(copy.deepcopy(x[1]['documents'][-1]))),
      ('invent complete printed code',lambda x:x[0].update(complete_printed_program_representation=True)),
      ('drop old required file',lambda x:x[2]['occurrences'].pop(0)),
      ('demote consumed marked image',lambda x:next(z for z in x[2]['occurrences'] if z['role']=='required complete accepted marked-image data').update(coarse_class='output_receipt',mathematical_premise=False)),
      ('hide free-text role as formal',lambda x:next(z for z in x[2]['occurrences'] if z['role']=='required mathematical model constructor').update(coarse_class='partial_formal',mathematical_premise=False)),
      ('unknown role fallback',lambda x:x[2]['occurrences'][0].update(role='unrecognized future role')),
      ('output outranks required data',lambda x:x[3]['content_precedence'].reverse()),
      ('double-count occurrence roles',lambda x:x[2]['disjoint_content_class_counts'].update(required_data=106)),
      ('omit complete receipt copy',lambda x:next(z for z in x[2]['contents'] if len(z['occurrence_ids'])>1)['occurrence_ids'].pop()),
      ('free common for conditional',lambda x:x[4].update(common_charged_once=False)),
      ('omit required acquisition',lambda x:x[4]['required_whole_content_ids'].pop()),
      ('claim all nine old apps unchanged',lambda x:x[0].update(old_nine_application_invariance_claim=True)),
      ('unknown source software zero',lambda x:x[0]['unknown_costs'].update(historical_L003_software=0)),
      ('premature input acceptance',lambda x:x[0].update(input_accepted=True)),
      ('premature factor',lambda x:x[0].update(ratios=1)),
      ('claim unaudited glyph maps done',lambda x:x[6].update(all_new_PDF_audits_complete=True)),
      ('new measured-original credit',lambda x:x[0].update(new_source_credit=1))]
    out=[]
    for name,f in changes:
        x=copy.deepcopy(args);f(x)
        try:semantic(*x)
        except (ValueError,KeyError,StopIteration):out.append(name)
        else:raise ValueError('SURVIVED '+name)
    need(group_classes(['output_receipt','required_data'],args[3])=='required_data','mixed-role required data positive control')
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh report path');roots={'study':a.study_root,'public':a.public_root}
    if (HERE/'manifest.json').exists():
        for e in read('manifest.json')['exports']:bound(HERE/e['path'],e)
    b=read('bindings.json')
    for e in b['references']:bound(roots[e['root']]/e['path'],e)
    for e in b['baseline_copies']:bound(HERE/e['path'],e)
    need(b['science_adoption']['sha256']=='f6eec52be2d15b1bab922e38e7018ad8fb18dffc3d3dda7b72e24858de872bf9' and b['input_acceptance'] is None,'science accepted/input pending')
    args=[read(n) for n in ['policy.json','documents.json','raw_inventory.json','role_policy.json','acquisition_routes.json','inheritance.json','audit_plan.json']]
    semantic(*args);p,d,r,rp,ac,i,plan=args
    for x in d['documents']:
        e=x['file'];f=roots[e['root']]/e['path'];bound(f,e);need(len(PdfReader(f).pages)==x['pages'],'actual PDF pages '+x['id'])
    for x in d['excluded_current_PDFs']:
        e=x['file'];bound(roots[e['root']]/e['path'],e)
    for x in r['occurrences']:
        bound(roots[x['root']]/x['path'],x)
        if 'current_exact_copy' in x:
            e=x['current_exact_copy'];bound(roots[e['root']]/e['path'],e);need(e['sha256']==x['sha256'] and e['bytes']==x['bytes'],'exact assembly content route')
    old_union=json.loads((a.study_root/'topic_A_L003_complete_assembly/whole_file_inventory.json').read_text())
    for new,old in zip(r['occurrences'][:252],old_union['occurrences']):need(all(new[k]==v for k,v in old.items()),'accepted whole occurrence preserved')
    report=dict(status='PASS_PRECOUNT_BOUNDARY_NO_NEW_METRIC_EVALUATION',complete_native_PDFs=29,physical_pages=286,source_common_application_program_pages=[152,41,63,30],identical_PDFs_reused=21,new_PDFs_to_audit=8,inherited_PDF_cells_preserved=630,inherited_raw_cells_preserved=450,accepted_raw_occurrences=252,additional_operational_wrapper=1,whole_raw_occurrences=253,unique_whole_contents=203,required_whole_contents=99,disjoint_classes=r['disjoint_content_class_counts'],controls=controls(args),actual_PDF_page_counts_checked=True,new_text_extraction=False,new_metric_evaluation=False,new_science_execution=False,new_formal_execution=False,factors=None,input_accepted=False)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
