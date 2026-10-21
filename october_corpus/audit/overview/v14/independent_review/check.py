#!/usr/bin/env python3
"""Root comparison of v14 with the accepted A, Mixes and v13 records."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse, csv, hashlib, importlib.util, json
from pypdf import PdfReader

def need(value, message):
    if not value: raise ValueError(message)
def read(path): return json.loads(path.read_text())
def fraction(a,b):
    q=Fraction(a,b)
    with localcontext() as ctx:
        ctx.prec=50; decimal=format(Decimal(a)/Decimal(b),'.12f')
    return dict(numerator=a,denominator=b,exact_fraction=f'{q.numerator}/{q.denominator}',decimal=decimal)

def check(packet, public):
    manifest=read(packet/'manifest.json')
    for row in manifest['exports']:
        data=(packet/row['path']).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path'])
    previous=read(public/'audit/overview/v13/packet/results.json')
    current=read(packet/'results.json')
    ar=read(public/'audit/topic-a/v3/measurement/packet/results.json')
    mr=read(public/'audit/topic-mixes/v3/measurement/packet/results.json')
    ap=ar['coordinates'][ar['primary_coordinate']]
    mp=mr['primary']
    corpus=read(public/'audit/corpus/latest.json')
    need(set(current['original_ids'])==set(previous['original_ids'])|{'F007'}
         and len(current['original_ids'])==len(set(current['original_ids']))==47
         and set(current['original_ids'])==set(corpus['measured_original_ids']),'Original inventory')
    need(current['active_originals']==106 and current['accessible_pending_originals']==59
         and current['archived_unavailable_originals']==55,'Programme counts')
    need(current['pooled_factor'] is None and not current['software_inclusive_comparisons_available']
         and not current['cross_topic_deduplication']
         and current['new_source_credit']==current['new_question_credit']==current['new_formal_credit']==0,
         'Unsupported costs or proof credits')
    need(len(current['topics'])==18 and len(previous['topics'])==19,'Topic inventory')
    old_topics={t['topic']:t for t in previous['topics']};pairs=[]
    need({t['topic'] for t in current['topics']}==set(old_topics)-{'Affine'},'Affine counted twice')
    maps={'A':dict(zip(['L032','L034','F016','F013','L035','N009','L128','L012'],
                       ['A1','A2','A3','A4','A5','A6','A7','A8'])),
          'Mixes':{'F005':'A1+A2','L016':'A3','F007':'A4+A5'}}
    unchanged=0;unchanged_pairs=0
    for t in current['topics']:
        key=t['topic'];old=old_topics[key]
        if key not in {'A','Mixes'}:
            need(t==old,'Unchanged topic '+key)
            unchanged+=1;unchanged_pairs+=len(t['pairs'])
        else:
            need(t['previous_topic_record']==old,'Previous topic retained')
            p=ap if key=='A' else mp
            representation='calibrated_selected_pdf' if key=='A' else 'raw_untrimmed_pdf'
            need(t['representation']==representation and t['normalization']=='NFC'
                 and t['unit']=='characters_without_whitespace','Adopted coordinate')
            expected=tuple(p[k] for k in ['source_sum','whole_common','application_sum','whole_written'])
            need(tuple(t[k] for k in ['source_sum','common_theory','applications_sum','written_denominator'])==expected,
                 'Accepted whole document costs '+key)
            need(t['separate_software_inventory']==p['separate_software' if key=='A' else 'separate_inventory'],
                 'Software inventory changed')
            need(t['source_count']==(8 if key=='A' else 3),'Expanded original count')
            if key=='A':
                need(t['previous_affine_record']==old_topics['Affine'],'Affine history omitted')
                need(t['common_components']=={'U':66140},'Whole A common theory')
            else:
                need(t['common_components']=={'U':12615,'U1':11641,'U2':10501},'Whole Mixes common theory')
                need(t['required_printed_coverage']['REQ']==['topic_Mix_F005_recovery/check_coprime.g',
                     'topic_Mix_L016_recovery/base_certificate.g'],'Required printed inventory')
            need(t['whole_file_inventory']==(ar if key=='A' else mr)['whole_file_inventory'],
                 'Complete software/formal inventory')
            for a in t['pairs']:
                s=a['source'];doc=maps[key][s]
                need(a['original_application_id']==doc,'Source/application pairing')
                cost=sum(p['document_costs'][x] for x in doc.split('+'))
                need(a['source_cost']==p['document_costs'][s] and a['application_cost']==cost,'Complete local costs')
        need(t['source_count']==len(t['pairs']) and t['source_ids']==[p['source'] for p in t['pairs']], 'Whole original count')
        need(t['written_denominator']==t['common_theory']+t['applications_sum']
             and t['written']==fraction(t['source_sum'],t['written_denominator']),'Whole arithmetic')
        need(sum(p['source_cost'] for p in t['pairs'])==t['source_sum']
             and sum(p['application_cost'] for p in t['pairs'])==t['applications_sum'],'Complete source/application sum')
        for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost']:
            need(t.get(k) is None,'Unknown software converted to a number')
        need(t['embedded_validation_listings_screened'] and not t['held_sources'],'Symmetric listing boundary')
        for p in t['pairs']:
            need(p['conditional']==fraction(p['source_cost'],p['application_cost']),'Conditional arithmetic')
            pairs.append((t,p))
    need(len(pairs)==47 and unchanged==16 and unchanged_pairs==36,'Complete individual count')
    topics=list(csv.DictReader((packet/'topics.csv').open()))
    individual=list(csv.DictReader((packet/'applications.csv').open()))
    need(len(topics)==18 and len(individual)==47,'CSV rows')
    for r,t in zip(topics,current['topics']):
        need(r['topic']==t['topic'] and int(r['originals'])==t['source_count'],'CSV topic')
        for a,b in [('current_source_cost','source_sum'),('whole_common_cost','common_theory'),
                    ('all_applications_cost','applications_sum'),('written_denominator','written_denominator')]:
            need(int(r[a])==t[b],'CSV complete cost')
        need(r['current_written_exact']==t['written']['exact_fraction'] and
             r['current_written_factor']==t['written']['decimal'],'CSV whole ratio')
    for r,(t,p) in zip(individual,pairs):
        need((r['topic'],r['source'],r['application'])==(t['topic'],p['source'],p['application']),'CSV individual')
        need(int(r['current_source_cost'])==p['source_cost'] and int(r['application_cost'])==p['application_cost']
             and int(r['whole_common_prepaid'])==t['common_theory'],'CSV local costs')
        need(r['conditional_exact']==p['conditional']['exact_fraction'] and r['conditional_factor']==p['conditional']['decimal'],
             'CSV local ratio')

    # The old parser only extracts rectangles; every expected dimension comes
    # from accepted counts above, without importing v14 author code or plot data.
    spec=importlib.util.spec_from_file_location('old_vector_parser', public/'audit/overview/v10/packet/geometry_checks.py')
    parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
    whole=[(t['topic'],[('source',t['source_sum']),('common',t['common_theory']),('applications',t['applications_sum'])]) for t in current['topics']]
    individual=[(p['source'],[('source',p['source_cost']),('application',p['application_cost'])]) for _,p in pairs]
    plots=[('whole_topics',whole,604.8,3),('conditional_1',individual[:24],655.2,2),('conditional_2',individual[24:],655.2,2)]
    bars=0
    for name,rows,height,legend in plots:
        maximum=max(max(v[0][1],sum(n for _,n in v[1:])) for _,v in rows)
        sx=777.6*.77/(maximum*1.08);sy=height*.84/len(rows);expected={}
        for i,(identity,values) in enumerate(rows):
            start=0
            for k,(kind,value) in enumerate(values):
                expected[f'bar-{identity}-{kind}']=[777.6*.19+(start*sx if k else 0),
                    height*.08+(i+(.535 if k else .235))*sy,value*sx,.23*sy]
                if k:start+=value
        svg=(packet/(name+'.svg')).read_text();parser.compare_geometry(parser.svg_rectangles(svg),expected)
        actual,h=parser.pdf_rectangles(packet/(name+'.pdf'));need(abs(h-height)<1e-6,'PDF height')
        parser.compare_pdf(actual,height,expected,legend);bars+=len(expected)
    need(bars==148,'Complete graph count')
    pages=[' '.join((p.extract_text() or '').split()) for p in PdfReader(packet/'reader.pdf').pages]
    need(len(pages)==6,'Whole reader')
    for t in current['topics']:
        cells=[t['topic'],str(t['source_count']),format(t['source_sum'],','),format(t['common_theory'],','),
               format(t['applications_sum'],','),f"{float(t['written']['decimal']):.3f}"]
        need(' '.join(cells) in pages[0],'Reader topic row')
    for i,(t,p) in enumerate(pairs):
        cells=[p['source'],t['topic'],format(p['source_cost'],','),format(p['application_cost'],','),
               f"{float(p['conditional']['decimal']):.3f}"]
        need(' '.join(cells) in pages[1 if i<24 else 2],'Reader individual row')
    need('calibrated selected extraction' in pages[1] and 'Magma' in pages[2]
         and 'Historical software' in pages[2] and 'F007' in pages[2]
         and 'Problems 1 and 2 remain unanswered' in pages[2], 'Reader scope')
    return dict(status='PASS_ROOT_INDEPENDENT_OVERVIEW47',exact_fractions=65,unchanged_topics=16,
                unchanged_individual_records=36,SVG_bars=148,PDF_bars=148,reader_pages=6,
                recovered=47,pending=59,software_inclusive_factor=None,new_question_credit=0,
                source_measurement_or_science_rerun=False,current_author_code_imported=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--public',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'Fresh output')
    result=check(a.packet,a.public);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
