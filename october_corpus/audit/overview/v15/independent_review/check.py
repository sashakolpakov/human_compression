#!/usr/bin/env python3
"""Root comparison of v15 with accepted Representation numbers and v14.

Prior root vector/reader checking is reused. No current author code is imported.
"""
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
    def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
    need(sha(packet/'manifest.json')=='c44d8d9aa6cddc9127d1d11493dad747b623efe207a42f6e24a94e2394e69b8a', 'Author identity')
    for row in read(packet/'manifest.json')['exports']:
        p=packet/row['path']
        need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'], row['path'])
    for name in ['manifest.json','results.json']:
        need((packet/'inputs'/('previous_'+name)).read_bytes()==
             (public/'audit/overview/v14/packet'/name).read_bytes(), 'Public v14 input')
    for prefix,pin in [('numbers','2b9f3078221231d7db32b17d20517531ca3956ba5caa8fbab6f18b3b2bf645d3'),
                       ('root','e52ed6fff70311e54c866402da59d69912d4e07b560956f365f4175049364f4e')]:
        m=packet/'inputs'/(prefix+'_manifest.json')
        need(sha(m)==pin, 'Accepted input manifest '+prefix)
        name='results.json' if prefix=='numbers' else 'adoption.json'
        row=next(r for r in read(m)['exports'] if r['path']==name)
        p=packet/'inputs'/(prefix+'_'+name)
        need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Accepted literal input '+prefix)
    previous=read(public/'audit/overview/v14/packet/results.json')
    current=read(packet/'results.json')
    numbers=read(packet/'inputs/numbers_results.json');primary=numbers['primary'];costs=primary['costs']
    old_topics={t['topic']:t for t in previous['topics']};pairs=[]
    need(len(current['topics'])==18 and {t['topic'] for t in current['topics']}==set(old_topics),'Topic inventory')
    need(len(current['original_ids'])==len(set(current['original_ids']))==48 and
         set(current['original_ids'])==set(previous['original_ids'])|{'L126'},'Only L126 added')
    need(current['active_originals']==106 and current['accessible_pending_originals']==58 and
         current['archived_unavailable_originals']==55,'Programme counts')
    need(current['pooled_factor'] is None and not current['software_inclusive_comparisons_available'] and
         not current['cross_topic_deduplication'] and
         current['new_source_credit']==current['new_question_credit']==current['new_formal_credit']==0,'Scope and costs')
    unchanged=0;unchanged_pairs=0
    for t in current['topics']:
        key=t['topic'];old=old_topics[key]
        if key!='Representation':
            need(t==old,'Changed unrelated topic '+key);unchanged+=1;unchanged_pairs+=len(t['pairs'])
        else:
            need(t['previous_topic_record']==old,'Retained prior topic')
            need(t['source_ids']==['F010','L126'] and t['source_count']==2,'Representation originals')
            need((t['representation'],t['normalization'],t['unit'])==
                 ('calibrated_selected_pdf','NFC','characters_without_whitespace'),'Fixed coordinate')
            expected=(costs['F010']+costs['L126'],costs['U_R'],costs['R1']+costs['R2'])
            need(tuple(t[k] for k in ['source_sum','common_theory','applications_sum'])==expected,'All complete costs')
            need(expected==(60472,36715,45437),'Exact accepted coordinate')
            need(t['common_components']=={'U_R':36715} and t['application_components']==
                 {'R1':{'R1':10985},'R2':{'R2':34452}},'No free sibling or common theory')
            need(t['no_sibling_application_dependency'] and t['entire_common_pages']==[13] and
                 t['entire_source_pages']=={'F010':13,'L126':13} and
                 t['entire_application_pages']=={'F010':4,'L126':12},'Complete document acquisition')
            need(t['whole_file_inventory']==numbers['raw_file_inventory']['files'] and
                 t['whole_file_group_costs']==primary['raw_costs'],'Whole program/data inventory')
            need(t['required_certificate_raw_cost']==6070 and t['mandatory_data_cost']==19315 and
                 t['optional_validation_raw_cost']==28753 and t['raw_program_alternative']==34823 and
                 t['printed_program_cost']==35723,'Separate required, optional and alternative costs')
            need(t['unknown_costs']==numbers['unknown_costs'] and not t['full_source_formalized'] and
                 t['scoped_Lean_declarations']==22,'No invented cost or full formalization')
            need('Expansion' in t['whole_topic_interpretation'] and 'Section6.2/Section8' in
                 t['scientific_boundary'],'Expansion and unresolved scope visible')
            for p in t['pairs']:
                doc={'F010':'R1','L126':'R2'}[p['source']]
                need(p['application']==p['original_application_id']==doc and
                     p['source_cost']==costs[p['source']] and p['application_cost']==costs[doc], 'Local document costs')
        need(t['source_ids']==[p['source'] for p in t['pairs']] and t['source_count']==len(t['pairs']),'Distinct original count')
        need(t['written_denominator']==t['common_theory']+t['applications_sum'] and
             t['written']==fraction(t['source_sum'],t['written_denominator']),'Whole arithmetic')
        need(sum(p['source_cost'] for p in t['pairs'])==t['source_sum'] and
             sum(p['application_cost'] for p in t['pairs'])==t['applications_sum'],'Complete sums')
        need(t['embedded_validation_listings_screened'] and not t['held_sources'],'Symmetric listing boundary')
        for k in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost']:
            need(t.get(k) is None,'Unsupported software-inclusive factor')
        for p in t['pairs']:
            need(p['conditional']==fraction(p['source_cost'],p['application_cost']),'Conditional arithmetic')
            pairs.append((t,p))
    need(len(pairs)==48 and unchanged==17 and unchanged_pairs==46,'Comparison count')
    topics=list(csv.DictReader((packet/'topics.csv').open()));individual=list(csv.DictReader((packet/'applications.csv').open()))
    need(len(topics)==18 and len(individual)==48,'Complete CSV rows')
    for r,t in zip(topics,current['topics']):
        need(r['topic']==t['topic'] and int(r['originals'])==t['source_count'],'CSV topic')
        for a,b in [('source_cost','source_sum'),('whole_common','common_theory'),
                    ('all_applications','applications_sum'),('written_denominator','written_denominator')]:
            need(int(r[a])==t[b],'CSV complete costs')
        need(r['written_exact']==t['written']['exact_fraction'] and r['written_factor']==t['written']['decimal'],'CSV whole ratio')
    for r,(t,p) in zip(individual,pairs):
        need((r['topic'],r['source'],r['application'])==(t['topic'],p['source'],p['application']),'CSV source pairing')
        need(int(r['source_cost'])==p['source_cost'] and int(r['application_cost'])==p['application_cost'] and
             int(r['whole_common_prepaid'])==t['common_theory'],'CSV local costs')
        need(r['conditional_exact']==p['conditional']['exact_fraction'] and
             r['conditional_factor']==p['conditional']['decimal'],'CSV conditional ratio')
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
    need(bars==150,'Complete graph count')
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
    need('written expansion' in pages[0] and '13-page' in pages[1] and '19,326-byte' in pages[1] and '19326' not in pages[1] and 'remain unresolved' in pages[2] and 'Neither full source is formalized' in pages[2] and 'Historical software' in pages[2] and 'Magma' in pages[2], 'Reader scope')
    return dict(status='PASS_ROOT_INDEPENDENT_OVERVIEW48',exact_fractions=66,unchanged_topics=17,
                unchanged_individual_records=46,SVG_bars=150,PDF_bars=150,reader_pages=6,
                recovered=48,pending=58,software_inclusive_factor=None,new_question_credit=0,
                source_measurement_or_science_rerun=False,current_author_code_imported=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--public',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'Fresh output')
    result=check(a.packet,a.public);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
