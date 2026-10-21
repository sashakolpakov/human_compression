#!/usr/bin/env python3
"""Independent Topic G arithmetic and presentation review.

Uses only accepted count records, integer arithmetic and standard libraries.
Does not import the author's builder, extract primary PDFs, or run proofs.
"""
import argparse, copy, csv, hashlib, itertools, json, math, re
from pathlib import Path
import xml.etree.ElementTree as ET

PINS={
 'inputs':'c46e1742d44138d9a63af86ae2ee9dd9d1498d0b4ca0d75cf1fd19a022af978d',
 'input_review':'4bd02d9322aa41b6f6ea09ec68c10428b07bf079288048ef416f1d7e7f737d80',
 'input_adoption':'26fefb9a3b596a7ed8ceb0792a99afe0e39f01e3cb1483225ce04d8e69d8fbbb',
 'numbers':'454d8171174d417a86897a0b86eb12a3cc2b46a6ad6809788842c11cfeb45250'}
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
FORMS=('NFC','NFKC')
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace',
       'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
ROLE_COUNTS={'required mathematical computation':4,'required witness verification':1,
             'required certificate bridge':1,'validation':7}
RAW=('complete_programs','complete_operational_drivers','complete_formal_files')
PRIMARY=('calibrated_selected','NFC','characters_without_whitespace')

def need(b,s):
    if not b: raise ValueError(s)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def key(r): return r['variant'],r['normalization'],r['unit']

def rounded(n,d,places):
    """Decimal nearest-even rounding directly from integers, without float."""
    q,r=divmod(n*10**places,d)
    if 2*r>d or (2*r==d and q%2): q+=1
    a,b=divmod(q,10**places)
    return f'{a}.{b:0{places}d}'

def fraction(n,d):
    need(type(n) is int and type(d) is int and n>0 and d>0,'positive integral fraction')
    h=math.gcd(n,d)
    return {'numerator':n,'denominator':d,'reduced_numerator':n//h,'reduced_denominator':d//h,'decimal':rounded(n,d,12)}

def calculate(independent,cover):
    documents=independent['documents']; raw=independent['raw_files']
    need(set(documents)=={'L009','L092','U_G','G1','G2','CODE'},'six complete PDFs')
    need([len(raw[k]) for k in RAW]==[13,3,6],'whole program/driver/formal boundary')
    actual={r:sum(x['role']==r for x in raw['complete_programs'].values()) for r in ROLE_COUNTS}
    need(actual==ROLE_COUNTS and sum(actual.values())==13,'exact four/two/seven program roles')
    rows={}; sensitivity={}; fractions=[]
    for v,f,u in itertools.product(VARIANTS,FORMS,UNITS):
        c={name:d['variants'][v][f][u] for name,d in documents.items()}
        raw_totals={kind:sum(file['metrics'][f][u] for file in raw[kind].values()) for kind in RAW}
        roles={role:sum(file['metrics'][f][u] for file in raw['complete_programs'].values() if file['role']==role) for role in ROLE_COUNTS}
        need(sum(roles.values())==raw_totals['complete_programs'],'every whole program counted')
        numerator=sum(c[x] for x in ('L009','L092'))
        denominator=sum(c[x] for x in ('U_G','G1','G2'))
        comparisons={name:fraction(numerator,cost) for name,cost in [
            ('written',denominator),('including_printed_programs',denominator+c['CODE']),
            ('including_raw_programs',denominator+raw_totals['complete_programs'])]}
        conditional={s:{'application':a,'comparison':fraction(c[s],c[a])} for s,a in [('L009','G1'),('L092','G2')]}
        r={'variant':v,'normalization':f,'unit':u,'document_costs':c,'raw_costs':raw_totals,
           'program_costs_by_role':roles,'source_sum':numerator,'written_denominator':denominator,
           'combined':comparisons,'conditional':conditional,'acquired_common':c['U_G'],
           'acquired_printed_programs':c['CODE'],'acquired_raw_programs_alternative':raw_totals['complete_programs']}
        rows[v,f,u]=r
        article=cover['article_only'][v][f][u]
        s={'variant':v,'normalization':f,'unit':u,'L009_article_only':article,'source_sum':article+c['L092'],
           'written':fraction(article+c['L092'],denominator),
           'including_printed_programs':fraction(article+c['L092'],denominator+c['CODE']),
           'including_raw_programs':fraction(article+c['L092'],denominator+raw_totals['complete_programs']),
           'L009_conditional':fraction(article,c['G1']),'L092_conditional_unchanged':True}
        sensitivity[v,f,u]=s
        for name,value in comparisons.items():fractions.append(dict(variant=v,normalization=f,unit=u,comparison='main.'+name,**value))
        for name,value in conditional.items():fractions.append(dict(variant=v,normalization=f,unit=u,comparison='conditional.'+name,**value['comparison']))
        for name in ['written','including_printed_programs','including_raw_programs','L009_conditional']:
            fractions.append(dict(variant=v,normalization=f,unit=u,comparison='article_only.'+name,**s[name]))
    return rows,sensitivity,fractions

def verify(result,expected,sensitivity):
    need(result['input_manifests']=={k:v for k,v in PINS.items() if k!='numbers'},'accepted input pins')
    need(result['source_ids']==['L009','L092'] and result['source_records']==79 and result['principal_contracts']==2,'two fixed source contracts')
    rows={key(r):r for r in result['coordinates']}
    need(len(result['coordinates'])==len(rows)==30 and rows==expected,'all thirty exact main coordinate records')
    need(result['primary']==expected[PRIMARY],'primary is the fixed cover-inclusive full-document coordinate')
    need((result['coordinate_count'],result['exact_fraction_count'],result['combined_fractions'],result['conditional_fractions'])==(30,150,90,60),'main fraction inventory')
    s=result['cover_sensitivity']
    need(s['primary_includes_cover'] is True and s['full_visible_cover_logo_cost'] is None,'cover retained and visual cost unknown')
    need('Directly counted' in s['method'] and 'not subtraction' in s['method'],'direct article count rule')
    sr={key(r):r for r in s['article_only_coordinates']}
    need(len(s['article_only_coordinates'])==len(sr)==30 and sr==sensitivity and s['additional_exact_fractions']==120,'all direct article-only sensitivity fractions')
    b=result['boundary']
    need(b['whole_common_once_within_topic'] and b['whole_source_and_applications'] and not b['cross_topic_discount'],'full topic charge')
    need([b[k] for k in ['required_finite_programs','witness_certificate_bridges','validation_programs','complete_programs']]==[4,2,7,13],'four/two/seven program boundary')
    need([b[k] for k in ['operational_drivers_separate','Lean_files_separate','prior_partial_Lean_declarations']]==[3,6,40],'separate auxiliary/formal scope')
    need('all thirteen complete programs' in b['conditional'] and 'including validation' in b['conditional'],'complete conditional prepayment')
    need('alternatives never both' in b['program_representations'],'no simultaneous code charges')
    need(all(b[k] is None for k in ['retained_BDL_full_proof_cost','retained_Kantor_full_proof_cost','other_external_proof_cost','historical_program_cost','graphics_and_formula_layout_cost']),'unknown costs remain null')
    need('all recorded exclusions' in b['source_qualifications'],'source correction/exclusion boundary')
    need(not b['mathematical_complexity_claim'] and not b['sawtooth_claim'],'no invented complexity result')
    need(all(result[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']) and not result['primary_text_fonts_images_exported'],'no new credit or primary material')

def chart(svg,primary):
    root=ET.fromstring(svg);ns={'s':'http://www.w3.org/2000/svg'};costs=primary['document_costs']
    expected=[([primary['source_sum'],costs['U_G'],costs['G1']+costs['G2']],['#686868','#426b9a','#70a59a']),
              ([costs[x] for x in ['U_G','L009','G1','L092','G2','CODE']],['#426b9a','#686868','#70a59a','#686868','#70a59a','#bd874e'])]
    bars_count=0
    for index,(values,colors) in enumerate(expected,1):
        axis=root.find(f'.//s:g[@id="axes_{index}"]',ns);need(axis is not None,'plot panel')
        bars=[]
        for group in axis.findall('s:g',ns):
            if not group.get('id','').startswith('patch_'):continue
            for path in group.findall('s:path',ns):
                if 'clip-path' not in path.attrib:continue
                nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',path.get('d',''))]
                need(len(nums)==8,'rectangular bar')
                xs,ys=nums[::2],nums[1::2]
                bars.append((min(ys),max(ys),min(xs),max(xs),path.get('style')))
        need(len(bars)==len(values),'complete chart bar count')
        scale=(bars[0][1]-bars[0][0])/values[0]
        for bar,value,color in zip(bars,values,colors):
            need(abs(bar[1]-bar[0]-scale*value)<0.00002 and color in bar[4],'actual bar height and role color')
        if index==1:
            need(bars[0][1]==bars[1][1] and abs(bars[2][1]-bars[1][0])<0.000001 and bars[1][2:4]==bars[2][2:4],'whole common/application stack')
        else:
            need(all(abs(bar[1]-bars[0][1])<0.000001 for bar in bars),'component bars share zero')
        bars_count+=len(bars)
    for value in [primary['source_sum'],primary['written_denominator'],*costs.values()]:
        need(f'<!-- {value:,} -->' in svg,'explicit chart value label')
    return bars_count

def reader(tex,result):
    p=result['primary'];c=p['document_costs']
    for value in [*c.values(),p['source_sum'],p['written_denominator'],*p['raw_costs'].values()]:need(str(value) in tex,'reader numerical value')
    for row in result['coordinates']:
        if row['variant']=='calibrated_selected' and row['normalization']=='NFC':
            for f in [row['combined']['written'],*(x['comparison'] for x in row['conditional'].values())]:need(rounded(f['numerator'],f['denominator'],3) in tex,'rounded sensitivity display')
    for phrase in ['After acquiring the whole common paper and all thirteen complete programs',
                   'The complete written replacement is longer','G2 is longer than L092',
                   'never simultaneous charges','full\nproof costs unknown',
                   'named-geometry\nidentifications','They do not formalize the entire source contracts.',
                   'The primary comparison continues to include that cover.',
                   'not establish a recurring sawtooth pattern']:
        need(phrase in tex,'reader qualification '+phrase)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--input-review',type=Path,required=True);ap.add_argument('--input-adoption',type=Path,required=True);ap.add_argument('--numbers',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output directory');roots={k:getattr(a,k) for k in PINS};bound=[]
    for k,root in roots.items():
        need(sha(root/'manifest.json')==PINS[k],'frozen manifest '+k)
        for r in read(root/'manifest.json')['exports']:
            p=root/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'frozen exported file '+str(p))
        bound.append({'role':k,'path':str(root/'manifest.json'),'sha256':PINS[k]})
    independent=read(a.input_review/'recount.json');counts=read(a.inputs/'author_counts.json')
    policy=read(a.inputs/'policy.json');scope=read(a.inputs/'source_contract_boundary.json');input_review=read(a.input_review/'review.json');adoption=read(a.input_adoption/'review.json')
    need(independent['documents']==counts['documents'] and all(independent['raw_files'][k]==counts[k] for k in RAW),'independently accepted primitive counts agree')
    need(input_review['status']=='ACCEPTED_INDEPENDENT_TOPIC_G_MEASUREMENT_INPUTS_V2' and adoption['status']=='ROOT_ACCEPTED_TOPIC_G_INPUTS_V2_WITH_EXPLICIT_EXTRACTION_BOUNDARY','independent input admission')
    need(tuple(policy['variants'])==VARIANTS and tuple(policy['normalizations'])==FORMS and tuple(policy['units'])==UNITS,'prespecified metric axes')
    need(not policy['comparison_policy']['cross_topic_deduplication'] and scope['row_count']==79 and scope['principal_contracts']==2,'fixed contracts and no cross-topic discount')
    expected,sensitivity,fractions=calculate(independent,counts['identification_cover_sensitivity'])
    result=read(a.numbers/'measurement.json');verify(result,expected,sensitivity)
    controls=[]
    tests=[
      ('changed_late_coordinate',lambda d:d['coordinates'][-1]['combined']['written'].update(numerator=1)),
      ('lost_common_cost',lambda d:d['coordinates'][0].update(written_denominator=1)),
      ('code_double_charge',lambda d:d['coordinates'][1]['combined']['including_raw_programs'].update(denominator=d['coordinates'][1]['written_denominator']+d['coordinates'][1]['document_costs']['CODE']+d['coordinates'][1]['raw_costs']['complete_programs'])),
      ('wrong_conditional_source',lambda d:d['coordinates'][2]['conditional']['L009']['comparison'].update(numerator=d['coordinates'][2]['document_costs']['L092'])),
      ('wrong_decimal_only',lambda d:d['coordinates'][3]['combined']['written'].update(decimal='1.000000000000')),
      ('missing_coordinate',lambda d:d['coordinates'].pop()),
      ('cover_replaces_primary',lambda d:d['primary'].update(source_sum=72710)),
      ('incorrect_article_sensitivity',lambda d:d['cover_sensitivity']['article_only_coordinates'][0].update(L009_article_only=1)),
      ('cover_excluded_silently',lambda d:d['cover_sensitivity'].update(primary_includes_cover=False)),
      ('conditional_not_prepaid',lambda d:d['boundary'].update(conditional='Application alone')),
      ('omit_validation',lambda d:d['boundary'].update(complete_programs=6,validation_programs=0)),
      ('borrow_other_topic_free',lambda d:d['boundary'].update(cross_topic_discount=True)),
      ('zero_BDL_proof',lambda d:d['boundary'].update(retained_BDL_full_proof_cost=0)),
      ('zero_Kantor_proof',lambda d:d['boundary'].update(retained_Kantor_full_proof_cost=0)),
      ('erase_qualification',lambda d:d['boundary'].update(source_qualifications='All source assertions proved.')),
      ('claim_sawtooth',lambda d:d['boundary'].update(sawtooth_claim=True)),
      ('new_question_credit',lambda d:d.update(new_question_credit=1))]
    for name,mut in tests:
        d=copy.deepcopy(result);mut(d)
        try:verify(d,expected,sensitivity)
        except ValueError as exc:controls.append({'name':name,'rejected':True,'reason':str(exc)})
        else:raise ValueError('accepted control '+name)
    svg=(a.numbers/'complete_costs.svg').read_text();tex=(a.numbers/'measurement.tex').read_text()
    bar_count=chart(svg,result['primary']);reader(tex,result)
    svgroot=ET.fromstring(svg);ns={'s':'http://www.w3.org/2000/svg'};path=svgroot.find('.//s:g[@id="patch_3"]/s:path',ns)
    path.set('d',path.get('d').replace('110.316926','111.316926'))
    presentation_controls=[]
    for name,check in [('distorted_bar_height',lambda:chart(ET.tostring(svgroot,encoding='unicode'),result['primary'])),('missing_prepaid_programs',lambda:reader(tex.replace('all thirteen complete programs','some programs'),result))]:
        try:check()
        except ValueError as exc:presentation_controls.append({'name':name,'rejected':True,'reason':str(exc)})
        else:raise ValueError('accepted presentation control '+name)
    a.out.mkdir(parents=True)
    with (a.out/'fractions.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(fractions[0]));wr.writeheader();wr.writerows(fractions)
    report={'status':'PASS_INDEPENDENT_TOPIC_G_NUMERICAL_AND_READER_CHECK','input_bindings':bound,'method':'No author builder imports. Accepted independent primitive counts; gcd reduction and integer nearest-even decimal rounding; direct accepted article-only counts.','pdf_input_cells':180,'raw_input_cells':220,'metric_coordinates':30,'combined_fractions':90,'conditional_fractions':60,'article_only_fractions':120,'all_exact_fractions':270,'primary':expected[PRIMARY],'arithmetic_controls':controls,'presentation_controls':presentation_controls,'bar_rectangles_checked':bar_count,'full_primary_reextraction':False,'scientific_program_or_Lean_replay':False,'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'coordinates':30,'fractions':270,'controls':len(controls)+len(presentation_controls),'bars':bar_count}))

if __name__=='__main__':main()
