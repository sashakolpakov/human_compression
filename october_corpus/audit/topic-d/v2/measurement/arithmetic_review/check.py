#!/usr/bin/env python3
"""Independent Topic D arithmetic/CSV check; no author arithmetic import.

The accepted independent input recount is retained, not re-extracted here.
"""
import argparse, copy, csv, hashlib, json, math
from pathlib import Path
REVIEW='61f1d290429b9d30e2c106beb15ee5eaaadce984c433abd68100288aa90c85ff'
CORRECTED='8f7729bd219adb61212d3e0c6215b7b84a09e798640ee47e3d5688239edb80d0'
ORIGINAL='86cc1bbd21ce8f73e8aa89049b69248fdbcad521dd0adc1c78e787b0ac8a94d9'
AUTHOR='7c72bf563e7b2c96c5e1927a41a9170108a5787a424fc1418aa9b97ebdabbe1d'
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
VARS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC']
PAIRS=[('L066','D1'),('L074','D2'),('L104','D3')]
def need(v,m):
    if not v:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_exports(folder):
    m=read(folder/'manifest.json')
    for b in m['exports']:
        n=Path(b['path']);need(not n.is_absolute() and '..' not in n.parts,'safe manifest path')
        p=folder/n;need(p.stat().st_size==b['bytes'] and sha(p)==b['sha256'],'unchanged bound file '+str(p))
    return len(m['exports'])
def qrecord(n,d):
    g=math.gcd(n,d);nn=n//g;dd=d//g
    return {'numerator':n,'denominator':d,'reduced_numerator':nn,'reduced_denominator':dd,'exact_fraction':str(nn) if dd==1 else f'{nn}/{dd}','factor':n/d}
def derive(recount,spec):
    answer={};programs=recount['raw_records']['raw_program_alternative'];drivers=recount['raw_records']['full_drivers_separate']
    roles={Path(x['path']).name:x['classification'] for x in spec['complete_mathematical_programs']}
    for v in VARS:
        for f in FORMS:
            for u in UNITS:
                costs={k:d['variants'][v][f][u] for k,d in recount['documents'].items()}
                source=costs['L066']+costs['L074']+costs['L104']
                applications=costs['D1']+costs['D2']+costs['D3'];written=costs['U_D']+applications
                raw=sum(x['variants'][f][u] for x in programs.values());dr=sum(x['variants'][f][u] for x in drivers.values())
                answer[(v,f,u)]={'variant':v,'normalization':f,'unit':u,'document_costs':costs,'source_sum':source,'common_theory':costs['U_D'],'all_applications':applications,'written_denominator':written,'printed_program_cost':costs['CODE'],'raw_program_cost':raw,'separate_driver_cost':dr,
                    'comparisons':{'written_papers':qrecord(source,written),'including_printed_program':qrecord(source,written+costs['CODE']),'including_raw_program_alternative':qrecord(source,written+raw)},
                    'per_result':[dict(source=s,application=a,source_cost=costs[s],application_cost=costs[a],**qrecord(costs[s],costs[a])) for s,a in PAIRS],
                    'raw_program_role_costs':{r:sum(x['variants'][f][u] for n,x in programs.items() if roles[n]==r) for r in ['required','diagnostic']}}
    return answer
def validate(result, expected, spec, boundary):
    coords=result['coordinates'];keys=[(c['variant'],c['normalization'],c['unit']) for c in coords]
    need(len(keys)==len(set(keys))==30 and set(keys)==set(expected),'all thirty distinct coordinates')
    for key,c in zip(keys,coords):need(c==expected[key],'independently derived complete coordinate '+str(key))
    need(result['primary']==expected[('calibrated_selected','NFC','characters_without_whitespace')],'exact declared primary')
    need(result['comparison_order']==['written_papers','per_result_conditional','including_printed_program','including_raw_program_alternative'],'written first; code separately')
    need(result['whole_common_paper_charged_once'] and result['all_three_complete_applications_charged'] and not result['cross_topic_common_discount'],'common paper once inside topic, no external discount')
    need('Whole U_D' in result['conditional_prepaid'] and 'five required programs and three complete diagnostics' in result['conditional_prepaid'],'whole declared prepayment')
    need(result['complete_mathematical_programs']==spec['complete_mathematical_programs'] and result['complete_drivers']==spec['complete_drivers'],'all eight complete programs and two separate drivers')
    p=result['program_boundary'];need(p['complete_programs']==8 and p['required']==5 and p['diagnostic']==3 and p['complete_drivers_separate']==2,'exact program classification')
    need(p['raw_metrics_summed_per_file'] and p['no_diagnostic_pruning'] and p['drivers_not_added_to_any_comparison'],'raw alternative and separate driver boundary')
    need(result['source_contract_rows']==boundary['contract_count']==37 and len(boundary['rows'])==37,'fixed mathematical scope')
    need('L104 diagrams' in result['source_corrections_and_exclusions'] and 'doubling' in result['source_corrections_and_exclusions'],'partial L104 supplementary scope explicit')
    for k in ['retained_external_proof_cost','catalogue_and_algorithm_construction_cost','historical_software_cost','graphics_and_formula_layout_cost','minimal_mathematical_complexity']:need(result[k] is None,'unknown is not zero '+k)
    need(not result['formal_source_application_claim'] and not result['full_visible_text_claim'],'no full formal or every-visible-mark claim')
    need(result['formal_validation_cost_separate'] and result['new_source_credit']==result['new_question_credit']==0,'separate formal work and no scientific credit')
    need(result['exact_combined_fractions']==result['exact_conditional_fractions']==90,'180 complete fractions')
    need(result['raw_file_bytes']=={'programs':sum(x['bytes'] for x in spec['complete_mathematical_programs']),'drivers':sum(x['bytes'] for x in spec['complete_drivers'])},'complete raw byte inventories')
    need(result['physical_pages']=={'source':26,'common':6,'applications':[5,6,2],'scientific_replacement':19,'printed_program':12,'total_input_pages':57},'complete page extents remain distinct')
    need(result['missing_original_source_pdfs']==[],'all three bound primary PDFs available')
    return True
def check_csv(packet,result,expected):
    expected_overall={};expected_conditional={}
    for key,c in expected.items():
        ids=dict(zip(['variant','normalization','unit'],key))
        for name,q in c['comparisons'].items():
            row=dict(**ids,representation=name,source_sum=c['source_sum'],whole_common=c['common_theory'],all_applications=c['all_applications'],program_cost=0 if name=='written_papers' else c['printed_program_cost'] if name=='including_printed_program' else c['raw_program_cost'],**q)
            expected_overall[key+(name,)]= {k:str(v) for k,v in row.items()}
        for q in c['per_result']:
            row=dict(**ids,**q,prepaid=result['conditional_prepaid']);expected_conditional[key+(q['source'],)]={k:str(v) for k,v in row.items()}
    for filename,expected_rows,extra in [('overall_costs.csv',expected_overall,'representation'),('conditional_costs.csv',expected_conditional,'source')]:
        with (packet/filename).open(newline='') as f:rows=list(csv.DictReader(f))
        keys=[tuple(r[k] for k in ['variant','normalization','unit',extra]) for r in rows]
        need(len(rows)==len(set(keys))==90,'ninety distinct CSV rows '+filename)
        need(dict(zip(keys,rows))==expected_rows,'all independent exact CSV cells '+filename)
def reader_tables(tex,expected):
    primary=expected[('calibrated_selected','NFC','characters_without_whitespace')]
    for q in primary['per_result']:
        row=f"{q['source']} / {q['application']} & {q['source_cost']:,} & {q['application_cost']:,} & {q['factor']:.3f}"+r'\\'
        need(row in tex,'each printed complete application row')
    labels={'whitespace_tokens':'Whitespace tokens','alphanumeric_units':'Alphanumeric runs','characters_without_whitespace':'Nonspace characters','characters_with_collapsed_whitespace':'Collapsed characters','utf8_bytes_with_collapsed_whitespace':'Collapsed UTF-8 bytes'}
    for u,label in labels.items():
        nfc=expected[('calibrated_selected','NFC',u)]['comparisons'];nfkc=expected[('calibrated_selected','NFKC',u)]['comparisons']
        values=[expected[(v,f,u)]['comparisons']['written_papers']['factor'] for v in VARS for f in FORMS]
        row=f"{label} & {nfc['written_papers']['factor']:.3f} & {nfkc['written_papers']['factor']:.3f} & {min(values):.3f}--{max(values):.3f} & {nfc['including_printed_program']['factor']:.3f}"+r'\\'
        need(row in tex,'each printed ruler sensitivity row')
    for name,label in [('written_papers','Written papers'),('including_printed_program','Written papers plus whole printed appendix'),('including_raw_program_alternative','Written papers plus all eight whole raw programs')]:
        q=primary['comparisons'][name];need(f"{label} & {q['denominator']:,} & {q['factor']:.3f}" in tex,'separate printed representation row')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh report')
    p=a.packet;need(sha(p/'manifest.json')==AUTHOR,'exact frozen numerical author packet')
    need(sha(p/'independent/manifest.json')==REVIEW and sha(p/'inputs/manifest.json')==CORRECTED and sha(p/'previous/manifest.json')==ORIGINAL,'accepted corrected input/review chain')
    n=verify_exports(p);counts={folder:verify_exports(p/folder) for folder in ['independent','inputs','previous']}
    rootreview=read(p/'independent/review.json');need(rootreview['measurement_inputs_accepted'] and rootreview['unresolved_corrections']==[],'root input acceptance retained')
    recount=read(p/'independent/recount_corrected.json');spec=read(p/'inputs/replacement_input_spec.json');boundary=read(p/'inputs/source_contract_boundary.json');r=read(p/'results.json')
    need(r['public_proof_admission_sha256']==rootreview['mathematical_admission_sha256'],'unchanged admitted proof scope')
    expected=derive(recount,spec);validate(r,expected,spec,boundary);check_csv(p,r,expected)
    reader_tables((p/'measurement.tex').read_text(),expected)
    controls=[]
    for name in ['omit_common','omit_application','drop_one_program','double_program_representations','include_drivers','wrong_fraction','wrong_pair','wrong_normalization','duplicate_coordinate','classical_zero','new_question','hide_L104_gap','formal_overclaim','conditional_hidden']:
        x=copy.deepcopy(r);c=x['coordinates'][0]
        if name=='omit_common':c['comparisons']['written_papers']['denominator']-=c['common_theory']
        elif name=='omit_application':c['all_applications']-=c['document_costs']['D3']
        elif name=='drop_one_program':x['complete_mathematical_programs'].pop()
        elif name=='double_program_representations':c['comparisons']['including_raw_program_alternative']['denominator']+=c['printed_program_cost']
        elif name=='include_drivers':c['comparisons']['including_printed_program']['denominator']+=c['separate_driver_cost']
        elif name=='wrong_fraction':c['comparisons']['written_papers']['exact_fraction']='1'
        elif name=='wrong_pair':c['per_result'][0]['application']='D2'
        elif name=='wrong_normalization':c['normalization']='NFKC'
        elif name=='duplicate_coordinate':x['coordinates'][1]=copy.deepcopy(c)
        elif name=='classical_zero':x['retained_external_proof_cost']=0
        elif name=='new_question':x['new_question_credit']=1
        elif name=='hide_L104_gap':x['source_corrections_and_exclusions']='All printed claims recovered.'
        elif name=='formal_overclaim':x['formal_source_application_claim']=True
        else:x['conditional_prepaid']='Given U.'
        try:validate(x,expected,spec,boundary)
        except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('accepted corruption '+name)
    report={'status':'PASS_INDEPENDENT_D_ARITHMETIC_CSV_AND_SCOPE','author_manifest_sha256':sha(p/'manifest.json'),'author_exports_checked':n,'retained_input_exports_checked':counts,'independent_input_review_sha256':REVIEW,'implementation':'No author computation or checking functions imported. Integer sums and math.gcd derive each fraction directly from the accepted independent recount. CSV rows are reconstructed separately.','coordinates':30,'pdf_metric_cells_reused_and_matched':240,'raw_program_and_driver_cells_reused':100,'exact_combined_fractions':90,'exact_conditional_fractions':90,'CSV_rows':180,'reader_numeric_table_rows':11,'primary':expected[('calibrated_selected','NFC','characters_without_whitespace')],'controls':controls,'source_input_reaudit':False,'formal_or_group_computations_rerun':False,'reader_visual_review':'separate review record','checker_sha256':sha(Path(__file__))}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'coordinates':30,'exact_fractions':180,'CSV_rows':180,'controls':len(controls)}))
if __name__=='__main__':main()
