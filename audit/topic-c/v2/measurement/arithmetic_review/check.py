#!/usr/bin/env python3
"""Independent Topic C arithmetic and CSV audit; no source or proof replay."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

UNITS = ('whitespace_tokens','alphanumeric_units','characters_without_whitespace',
         'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
FORMS = ('NFC','NFKC')
VARIANTS = ('raw_untrimmed','raw_selected','calibrated_selected')
PAIRS = (('L088','C1'),('N013','C2'),('L108','C3'),('F014','C4'))
REPRESENTATIONS = ('written_papers_only','complete_printed_programs','complete_raw_programs')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def csv_rows(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))


def audit(result, author, recount, specification, overall, conditional):
    docs=author['documents']; raw=author['raw_program_alternative']
    need(docs==recount['documents'] and raw==recount['raw_program_alternative'], 'accepted independent count agreement')
    need(set(docs)=={'L088','N013','F014','U_C','C1','C2','C3','C4','CODE'}, 'complete PDF inventory')
    programs=specification['required_mathematical_programs']
    need(programs==result['required_mathematical_programs'] and len(programs)==2 and
         {Path(p['path']).name for p in programs}==set(raw), 'both complete required programs')
    for p in programs:
        r=raw[Path(p['path']).name]
        need(r['bytes']==p['bytes'] and r['sha256']==p['sha256'], 'complete program edition')
    need(result['raw_program_total_bytes']==sum(p['bytes'] for p in programs)==9241, 'full raw program bytes')
    need(author['source_pdf_metrics_unknown']=={'L108':None} and author['four_source_pdf_total'] is None,
         'unavailable source remains unknown')
    need(result['complete_common_and_programs_prepaid_for_conditional_factors'] and
         result['all_four_applications_charged'] and result['raw_program_metrics_summed_per_file'] and
         result['common_theory_discount_for_other_topics'] is False, 'acquisition assumptions')
    need(result['primary_program_representation']=='Complete printed CODE appendix once' and
         result['headline_comparison']=='written_papers_only' and
         result['required_program_comparison']=='complete_printed_programs', 'written comparison first; code explicit separately')
    coordinates=result['coordinates']
    expected_keys=[(v,f,u) for v in VARIANTS for f in FORMS for u in UNITS]
    need([(r['variant'],r['normalization'],r['unit']) for r in coordinates]==expected_keys,
         'all thirty distinct coordinates in declared order')
    expected_overall=[]; expected_conditional=[]; fractions=0
    for row,(variant,form,unit) in zip(coordinates,expected_keys):
        costs={k:d['variants'][variant][form][unit] for k,d in docs.items()}
        need(all(type(v) is int and v>0 for v in costs.values()), 'positive measured costs')
        common=costs['U_C']; applications=sum(costs[a] for _,a in PAIRS)
        written=common+applications; printed=costs['CODE']
        raw_cost=sum(p['variants'][form][unit] for p in raw.values())
        known=sum(costs[s] for s,_ in PAIRS if s!='L108')
        expected=dict(common_theory=common,all_applications=applications,written_denominator=written,
                      complete_printed_program_cost=printed,complete_raw_program_cost=raw_cost,
                      complete_denominator=written+printed,raw_program_denominator=written+raw_cost,
                      known_source_sum=known,unknown_source='L108',complete_source_sum=None,overall_factor=None)
        need(all(row.get(k)==v for k,v in expected.items()), 'complete costs and unknown numerator')
        need(tuple(row['overall_formulas'])==REPRESENTATIONS, 'written comparison precedes code representations')
        for representation,extra in zip(REPRESENTATIONS,(0,printed,raw_cost)):
            formula=dict(unknown_source='L108',unknown_numerator_coefficient=1,
                         known_numerator=known,denominator=written+extra,overall_factor=None)
            need(row['overall_formulas'][representation]==formula, 'exact symbolic formula')
            expected_overall.append(dict(variant=variant,normalization=form,unit=unit,representation=representation,
                common_theory=str(common),all_applications=str(applications),program_cost=str(extra),
                known_source_sum=str(known),unknown_source='L108',complete_denominator=str(written+extra),
                overall_factor='unknown',formula=f'(x+{known})/{written+extra}'))
        need(len(row['per_result'])==4, 'four matched source/application comparisons')
        for saved,(source,application) in zip(row['per_result'],PAIRS):
            n=costs.get(source); d=costs[application]
            fraction=None if n is None else str(Fraction(n,d))
            decimal=None if n is None else float(Fraction(n,d))
            need(saved==dict(source=source,application=application,source_cost=n,application_cost=d,
                             fraction=fraction,factor=decimal), 'complete conditional fraction')
            fractions+=int(n is not None)
            expected_conditional.append(dict(variant=variant,normalization=form,unit=unit,source=source,
                application=application,source_cost='unknown' if n is None else str(n),application_cost=str(d),
                fraction='unknown' if fraction is None else fraction,factor='unknown' if decimal is None else str(decimal),
                prepaid='whole U_C and both complete programs'))
    need(overall==expected_overall and len(overall)==90, 'all overall CSV cells including display order')
    need(conditional==expected_conditional and len(conditional)==120, 'all conditional CSV cells')
    primary=next(r for r in coordinates if (r['variant'],r['normalization'],r['unit'])==
                 ('calibrated_selected','NFC','characters_without_whitespace'))
    need(result['primary']==primary and result['headline_formula']==primary['overall_formulas']['written_papers_only'] and
         result['required_program_inclusive_formula']==primary['overall_formulas']['complete_printed_programs'],
         'headline formulas use accepted primary coordinate and separate written/code denominators')
    need(result['known_conditional_fractions']==fractions==90 and result['unknown_conditional_coordinates']==30 and
         result['unknown_overall_coordinates_per_representation']==30, 'known and unknown counts')
    need(all(result[k] is None for k in ('outside_proof_cost','unextracted_graphic_cost','minimum_mathematical_complexity','L108_pdf_pages')),
         'unmeasured costs remain unknown')
    need(result['source_scope_rows']==40 and result['new_source_credit']==result['new_question_credit']==0,
         'measurement does not expand mathematical scope')
    need((result['source_pages_available'],result['replacement_scientific_pages'],result['required_program_appendix_pages'])==(33,27,4),
         'complete physical PDF boundary')
    return primary


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--original',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();p=args.packet;old=args.original
    need(not args.out.exists(),'fresh output report')
    for folder in (p,old,p/'inputs',p/'independent'):
        for row in read(folder/'manifest.json')['exports']:
            path=folder/row['path']
            need(path.stat().st_size==row['bytes'] and sha(path)==row['sha256'], 'frozen export: '+str(path))
    need(sha(p/'inputs/manifest.json')=='2d7362de8060e5e20be435193b7c95c40b67799508cb84d086d37425db5acb00' and
         sha(p/'independent/manifest.json')=='da559bab5cf59c5441ebbe7e7e06943ce653d1adf2947d2cf2b8dd7243dc628a',
         'accepted input proposal and independent recount')
    result=read(p/'results.json');author=read(p/'inputs/author_counts.json');recount=read(p/'independent/recount.json')
    specification=read(p/'inputs/replacement_input_spec.json')
    for path,value in result['bindings'].items():
        need(not Path(path).is_absolute() and '..' not in Path(path).parts and sha(p/path)==value, 'arithmetic input binding')
    overall=csv_rows(p/'overall_costs.csv');conditional=csv_rows(p/'conditional_costs.csv')
    primary=audit(result,author,recount,specification,overall,conditional)
    original=read(old/'results.json')
    need(original['coordinates']==result['coordinates'] and original['primary']==primary, 'revision preserves every measurement coordinate')
    need((old/'conditional_costs.csv').read_bytes()==(p/'conditional_costs.csv').read_bytes(), 'conditional CSV unchanged')
    canonical=lambda rows:sorted(json.dumps(r,sort_keys=True) for r in rows)
    need(canonical(csv_rows(old/'overall_costs.csv'))==canonical(overall), 'overall CSV changes only row order')
    controls=[]
    for case in ('omit_C3','halve_common','omit_CODE','double_programs','invent_L108','wrong_fraction',
                 'drop_coordinate','lose_prepaid_program','program_only_headline','external_zero','new_credit','wrong_CSV'):
        changed=copy.deepcopy(result);table=copy.deepcopy(overall)
        if case=='omit_C3':changed['coordinates'][0]['all_applications']-=1
        elif case=='halve_common':changed['coordinates'][0]['common_theory']//=2
        elif case=='omit_CODE':changed['coordinates'][0]['complete_denominator']=changed['coordinates'][0]['written_denominator']
        elif case=='double_programs':changed['coordinates'][0]['complete_denominator']+=changed['coordinates'][0]['complete_raw_program_cost']
        elif case=='invent_L108':changed['coordinates'][0]['per_result'][2]['source_cost']=0
        elif case=='wrong_fraction':changed['coordinates'][0]['per_result'][0]['fraction']='2'
        elif case=='drop_coordinate':changed['coordinates'].pop()
        elif case=='lose_prepaid_program':changed['complete_common_and_programs_prepaid_for_conditional_factors']=False
        elif case=='program_only_headline':changed['headline_comparison']='complete_printed_programs'
        elif case=='external_zero':changed['outside_proof_cost']=0
        elif case=='new_credit':changed['new_question_credit']=1
        else:table[0]['complete_denominator']='0'
        try:audit(changed,author,recount,specification,table,conditional)
        except ValueError as error:controls.append(dict(name=case,rejected=True,reason=str(error)))
        else:raise ValueError('undetected corruption: '+case)
    output=dict(status='PASS_INDEPENDENT_ARITHMETIC_AND_CSV_REVIEW',author_manifest_sha256=sha(p/'manifest.json'),
                original_manifest_sha256=sha(old/'manifest.json'),checker_sha256=sha(Path(__file__)),
                coordinates=30,exact_known_conditional_fractions=90,symbolic_overall_formulas=90,
                unknown_conditional_coordinates=30,overall_CSV_rows=90,conditional_CSV_rows=120,
                primary=primary,controls=controls,all_numeric_coordinates_unchanged_by_revision=True,
                source_reextraction_or_proof_replay=False,new_source_credit=0,new_question_credit=0)
    args.out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('primary','controls')}))


if __name__=='__main__':
    main()
