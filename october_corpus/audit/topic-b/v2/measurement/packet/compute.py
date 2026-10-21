#!/usr/bin/env python3
"""Derive whole-topic and conditional costs from independently matched counts."""
import argparse,hashlib,json
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace',
       'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
PAIRS=(('N001','B1'),('N003','B2'),('N008','B3'),('L030','B4'))
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def derive(author,independent):
    docs=author['documents']
    need(set(docs)=={'N003','N008','L030','U_B','B1','B2','B3','B4'},'exact document roster')
    need(set(independent['documents'])==set(docs),'independent roster')
    for name,row in docs.items():
        need(row['variants']==independent['documents'][name],'independent metric disagreement')
    need(author['source_pdf_metrics_unknown']=={'N001':None} and
         author['four_source_pdf_total'] is None,'missing source is unknown')
    coordinates=[]
    for variant in VARIANTS:
        for form in ('NFC','NFKC'):
            for unit in UNITS:
                costs={k:v['variants'][variant][form][unit] for k,v in docs.items()}
                common=costs['U_B'];local=sum(costs[b] for _,b in PAIRS)
                known=sum(costs[s] for s,_ in PAIRS if s in costs)
                pairs=[]
                for source,application in PAIRS:
                    n=costs.get(source);d=costs[application]
                    ratio=None if n is None else Fraction(n,d)
                    pairs.append(dict(source=source,application=application,source_cost=n,
                        application_cost=d,fraction=None if ratio is None else str(ratio),
                        factor=None if ratio is None else float(ratio)))
                coordinates.append(dict(variant=variant,normalization=form,unit=unit,
                    common_theory=common,all_applications=local,complete_denominator=common+local,
                    known_source_sum=known,unknown_source='N001',complete_source_sum=None,
                    overall_factor=None,overall_formula=dict(unknown_numerator_coefficient=1,
                        known_numerator=known,denominator=common+local),per_result=pairs))
    need(len(coordinates)==30,'all thirty measurement coordinates')
    primary=next(r for r in coordinates if (r['variant'],r['normalization'],r['unit'])==
                 ('calibrated_selected','NFC','characters_without_whitespace'))
    return dict(status='DERIVED_FROM_INDEPENDENTLY_MATCHED_COUNTS_PENDING_ARITHMETIC_REVIEW',
        primary=primary,coordinates=coordinates,known_conditional_fractions=90,
        unknown_conditional_coordinates=30,unknown_overall_coordinates=30,
        complete_common_theory_prepaid_for_conditional_factors=True,
        common_theory_discount_for_other_topics=False,all_four_applications_charged=True,
        required_mathematical_programs=[],required_program_cost=0,
        required_program_note='There are no required mathematical programs in this proof edition. Validation and formal-check infrastructure are separately inventoried.',
        outside_proof_cost=None,unextracted_graphic_cost=None,minimum_mathematical_complexity=None,
        source_pages_available=31,replacement_scientific_pages=22,N001_pdf_pages=None,
        new_source_credit=0,new_question_credit=0)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh result path')
    author_path=HERE/'inputs/author_counts.json';independent_path=HERE/'independent/recount.json'
    result=derive(json.loads(author_path.read_text()),json.loads(independent_path.read_text()))
    result['bindings']={str(p.relative_to(HERE)):sha(p) for p in
        (author_path,independent_path,HERE/'inputs/protocol.json',HERE/'inputs/manifest.json',
         HERE/'independent/manifest.json',Path(__file__))}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(known_conditional_fractions=90,overall_factor=None,primary=result['primary'])))
if __name__=='__main__':main()
