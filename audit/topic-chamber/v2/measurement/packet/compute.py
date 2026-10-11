#!/usr/bin/env python3
"""Whole-document arithmetic from accepted Chamber inputs; no extraction changes."""
import argparse,csv,hashlib,json
from fractions import Fraction
from pathlib import Path
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
FORMS=['NFC','NFKC']
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected']
PAIRS=[('L008','H1'),('N016','H2')]
RAW=['complete_mathematical_programs','complete_operational_drivers','complete_formal_files']
def need(x,m):
    if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def bind(folder,pin):
    need(sha(folder/'manifest.json')==pin,'Exact accepted manifest: '+str(folder))
    for r in read(folder/'manifest.json')['exports']:
        p=folder/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Exact accepted export '+r['path'])
def quotient(n,d):
    need(type(n) is int and type(d) is int and n>0 and d>0,'Positive complete integer costs')
    x=Fraction(n,d)
    return dict(numerator=n,denominator=d,reduced_numerator=x.numerator,reduced_denominator=x.denominator,decimal=format(float(x),'.12f'))
def calculate(roots,protocol):
    for k in ['inputs','input_review','input_adoption']:bind(roots[k],protocol['accepted_manifests'][k])
    counts=read(roots['inputs']/'input_counts.json');ind=read(roots['input_review']/'recount.json')
    policy=read(roots['inputs']/'policy.json');scope=read(roots['inputs']/'source_contract_boundary.json')
    spec=read(roots['inputs']/'replacement_input_spec.json')
    need(ind['status']=='PASS_INDEPENDENT_INPUT_RECOUNT_AND_FONT_AUDIT','Independent input audit')
    need(policy['units']==UNITS and policy['normalizations']==FORMS and policy['variants']==VARIANTS,'All fixed coordinates')
    need(protocol['conditional_prepayment']==['U_H','both_complete_programs'] and not policy['comparison_policy']['cross_topic_deduplication'],'Full independent topic and conditional acquisition')
    need(counts['ratios'] is None and counts['source_contract_rows']==27 and counts['proof_contexts']==22 and counts['principal_contracts']==2,'Accepted input-only scope')
    need(set(counts['documents'])=={'L008','N016','U_H','H1','H2','CODE'},'All complete source/replacement documents')
    for k,r in counts['documents'].items():need(r['variants']==ind['documents'][k]['variants'],'Independent PDF counts '+k)
    for k in RAW:
        need(set(counts[k])==set(ind['raw_files'][k]),'Whole raw roster')
        for name,r in counts[k].items():need(r==ind['raw_files'][k][name],'Independent raw counts '+name)
    need([len(counts[k]) for k in RAW]==[2,3,3],'All eight whole executable/formal files')
    roles={Path(r['path']).name:r for r in spec['complete_mathematical_programs']}
    need({n:(r['classification'],r['required_mathematical_premise']) for n,r in roles.items()}=={'chiral_cover.g':('required',True),'reflection_models.py':('diagnostic',False)},'Required and diagnostic remain distinct')
    need(scope['new_source_credit']==scope['new_question_credit']==0 and not scope['whole_manuscript_all_assertions_claim'],'No scientific credit or broadened principal scope')
    need(all(scope[k] is None for k in ['retained_external_cost','graphics_cost','historical_software_cost']),'Unknown costs remain null')
    rows=[]
    for variant in VARIANTS:
        for form in FORMS:
            for unit in UNITS:
                c={k:r['variants'][variant][form][unit] for k,r in counts['documents'].items()}
                raw={k:sum(r['metrics'][form][unit] for r in counts[k].values()) for k in RAW}
                role_costs={role:sum(counts['complete_mathematical_programs'][n]['metrics'][form][unit] for n,r in roles.items() if r['classification']==role) for role in ['required','diagnostic']}
                need(sum(role_costs.values())==raw['complete_mathematical_programs'],'All mathematical-program bytes allocated once')
                source=c['L008']+c['N016'];written=c['U_H']+c['H1']+c['H2']
                rows.append(dict(variant=variant,normalization=form,unit=unit,documents=c,raw_costs=raw,program_costs_by_role=role_costs,source_sum=source,written_denominator=written,combined={'written':quotient(source,written),'including_printed_programs':quotient(source,written+c['CODE']),'including_raw_programs':quotient(source,written+raw['complete_mathematical_programs'])},conditional={s:dict(application=a,comparison=quotient(c[s],c[a])) for s,a in PAIRS},acquisition={'whole_common':c['U_H'],'whole_printed_programs':c['CODE'],'whole_raw_programs_alternative':raw['complete_mathematical_programs']}))
    primary=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==tuple(protocol['primary_coordinate']))
    return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_INDEPENDENT_REVIEW',accepted_manifests=protocol['accepted_manifests'],source_ids=['L008','N016'],principal_source_manuscripts=2,detailed_source_rows=27,proof_contexts=22,coordinate_count=30,exact_fractions=150,combined_fractions=90,conditional_fractions=60,coordinates=rows,primary=primary,boundary=protocol['boundary'],no_new_source_credit=True,no_new_question_credit=True,no_new_formal_credit=True,primary_text_exported=False)
def write_csv(path,result):
    with path.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'])
        for r in result['coordinates']:
            values=list(r['combined'].items())+[(s+'_conditional',x['comparison']) for s,x in r['conditional'].items()]
            for name,v in values:w.writerow([r['variant'],r['normalization'],r['unit'],name,*[v[k] for k in ['numerator','denominator','reduced_numerator','reduced_denominator','decimal']]])
def main():
    p=argparse.ArgumentParser();p.add_argument('--protocol',type=Path,default=Path(__file__).with_name('protocol.json'))
    for k in ['inputs','input_review','input_adoption']:p.add_argument('--'+k.replace('_','-'),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'Fresh output');protocol=read(a.protocol);need(protocol['status']=='FIXED_BEFORE_NUMERICAL_COMPUTATION','Fixed accepted protocol required');result=calculate({k:getattr(a,k) for k in ['inputs','input_review','input_adoption']},protocol);a.out.mkdir(parents=True);write(a.out/'results.json',result);write_csv(a.out/'comparisons.csv',result);print(json.dumps(result['primary']))
if __name__=='__main__':main()
