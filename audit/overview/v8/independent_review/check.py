#!/usr/bin/env python3
"""Distinct whole-corpus arithmetic and vectors; no overview-author imports."""
from pathlib import Path
import argparse,copy,csv,hashlib,importlib.util,json,math
from pypdf import PdfReader
PIN='3df08f128c5924f599f58a4299a6934914f56a96a3f27b756b63bd05aa2cff55'
VECTOR_PIN='eba42a6b2b3621aebe0cc5d9875bae33157b103ca369bf3e3335e2a55bffba5c'
def need(b,m):
    if not b:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,exact_fraction=str(n//g) if d==g else f'{n//g}/{d//g}',decimal=f'{q//10**12}.{q%10**12:012d}')
def prior_checker(public):
    p=public/'audit/overview/v3/independent_review/check.py';need(sha(p)==VECTOR_PIN,'pinned root vector parser')
    s=importlib.util.spec_from_file_location('root_overview41_vectors',p);q=importlib.util.module_from_spec(s);s.loader.exec_module(q);return q
def bindings(packet,public):
    routes={f'previous_{k}':f'audit/overview/v7/{v}' for k,v in [('results','packet/results.json'),('manifest','packet/manifest.json'),('admission','admission.json'),('review','independent_review/review.json')]}
    routes['previous_corpus_pointer']='audit/topic-rank-augmentation/v1/previous_corpus_pointer.json'
    for suffix in ['results','manifest','protocol','review','review_manifest']:
        path='packet/'+suffix+'.json' if suffix in ['results','manifest','protocol'] else 'independent_review/'+('manifest' if suffix=='review_manifest' else 'review')+'.json'
        routes['RankAugmentation_'+suffix]='audit/topic-rank-augmentation/v1/measurement/'+path
    routes.update(new_admission='audit/topic-rank-augmentation/v1/admission.json',current_corpus_snapshot='audit/corpus/updates/rank-augmentation-measured.json',current_catalogue='papers/catalogue_rank_augmentation_measured.json')
    protocol=load(packet/'protocol.json');need(set(protocol['bindings'])==set(routes),'all13 actual numerical and programme bindings')
    for name,path in routes.items():
        r=protocol['bindings'][name];f=packet/r['local'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'] and f.read_bytes()==(public/path).read_bytes(),'exact accepted input '+name)
    return len(routes)
def arithmetic(d,public):
    old=load(public/'audit/overview/v7/packet/results.json');need(d['topics'][:-1]==old['topics'],'seventeen previous topic objects exact')
    need(d['topic_count']==len(d['topics'])==18 and d['original_manuscript_count']==41 and d['registry_manuscripts']==161,'fixed161/18topics41originals')
    need(d['pooled_factor'] is None and not d['cross_topic_deduplication'] and not d['all_registry_manuscripts_completed'],'no pooling or completion claim')
    need(d['currently_published_measured_originals']==40 and d['proposed_measured_originals']==41 and d['pending_numerical_acceptance']==[] and d['pending_overview_review'],'preserved author stage')
    need(all(d[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no mathematical credit from overview')
    t=d['topics'][-1];base=public/'audit/topic-rank-augmentation/v1/measurement';p=load(base/'packet/results.json')['primary'];r=load(base/'independent_review/review.json');c=p['costs'];raw=p['raw_costs'];u=c['U'];app=c['A1']+c['COUNTER'];source=c['L020']
    need(t['topic']=='RankAugmentation' and sha(base/'packet/manifest.json')=='b4232452cba25cae64bef0091a4adc947d8f679418fe73f1d439b5966ff587b7' and sha(base/'independent_review/manifest.json')=='444797a88e089d973c1c9df3e82558903c12326c42843ca62c591e8b7c92c59e' and r['status']=='ACCEPTED_UNCHANGED_DISTINCT_L020_NUMBERS','accepted exact new numbers')
    need(t['common_components']==dict(whole_common=u) and t['application_components']=={'RA1':dict(main_application=c['A1'],required_counterproof=c['COUNTER'])},'whole common and both local papers')
    need(t['pairs']==[dict(source='L020',application='RA1',source_cost=source,application_cost=app,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(source,app))],'complete original/application correspondence')
    need((t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['printed_program_cost'],t['raw_program_alternative'])==(source,u,app,u+app,c['CODE'],raw['programs']),'whole new boundary')
    need(t['conditional_prepaid']==dict(full_common=u,full_declared_printed_programs=c['CODE'],total=u+c['CODE']) and t['conditional_raw_alternative_prepaid']==dict(full_common=u,full_declared_raw_programs=raw['programs'],total=u+raw['programs']),'full alternative acquisition')
    need(t['separate_raw_inventory']==dict(programs=raw['programs'],program_literal_bytes=11533,drivers=raw['operational_drivers'],driver_literal_bytes=15947,formal=raw['formal_files'],formal_literal_bytes=6855),'whole separate inventories')
    need((t['entire_source_pages'],t['entire_common_pages'],t['entire_application_pages'],t['entire_program_pages'])==(19,[5],dict(main=3,counterproof=3),3),'all complete physical pages')
    need(not any(t[k] for k in ['old_umbrella_free_premise','counterproof_free','old_two_page_program_appendix_added','full_source_formalized']) and t['scoped_Lean_declarations']==15,'no free proof or formal inflation')
    need(t['representation']=='raw_untrimmed_pdf' and t['normalization']=='NFC' and t['unit']=='characters_without_whitespace' and all(x in t['scientific_boundary'] for x in ['case3 is false','Table1 is retained','not regenerated','remain unresolved']),'source edition and corrected scientific boundary')
    ids=[];count=0
    for t in d['topics']:
        need(t['source_ids']==[q['source'] for q in t['pairs']] and t['source_count']==len(t['pairs']),'original roster')
        need(t['common_theory']==sum(t['common_components'].values()) and t['source_sum']==sum(q['source_cost'] for q in t['pairs']) and t['applications_sum']==sum(q['application_cost'] for q in t['pairs']) and t['written_denominator']==t['common_theory']+t['applications_sum'],'all complete topic sums')
        # An absent older field remains absent; this does not assign zero external cost.
        data=t.get('mandatory_data_cost',0)
        for k,cost in [('written',0),('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:
            denominator=t['written_denominator']+(0 if k=='written' else data)+(cost or 0)
            need(t[k]==(None if cost is None else ratio(t['source_sum'],denominator)),'all exact whole factors');count+=cost is not None
        if t.get('including_optional_validation') is not None:
            f=t['including_optional_validation'];need(f==ratio(f['numerator'],f['denominator']),'optional exact fraction');count+=1
        for q in t['pairs']:need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'exact conditional');ids.append(q['source']);count+=1
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknowns remain null')
    need(len(ids)==len(set(ids))==41 and set(ids)=={q['source']for t in old['topics']for q in t['pairs']}|{'L020'} and count==94,'exact41originals94fractions')
    current=load(public/'audit/corpus/updates/rank-augmentation-measured.json');previous=load(public/'audit/topic-rank-augmentation/v1/previous_corpus_pointer.json')
    keys=['status','originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','pending_source_retrieval','currently_measured_originals','all_originals_remain_active','all_original_proofs_recovered','all_conjectures_resolved']
    need(d['programme_snapshot']=={k:current[k]for k in keys} and current['status']=='CURRENT_PROGRAMME_41_ADMITTED_ORIGINALS_106_ACCESSIBLE' and d['programme_counts_not_inferred_from_measurement'],'independent complete programme snapshot')
    admitted=set(current['admitted_original_ids']);pending=set(current['accessible_pending_original_ids']);missing=set(current['retrieval_original_ids'])
    need((len(admitted),len(pending),len(missing))==(41,65,55) and not(admitted&pending or admitted&missing or pending&missing) and len(admitted|pending|missing)==161 and admitted==set(ids),'complete original partition')
    need(admitted==set(previous['admitted_original_ids'])|{'L020'} and pending==set(previous['accessible_pending_original_ids'])-{'L020'} and current['retrieval_original_ids']==previous['retrieval_original_ids'],'single original transferred')
    return count
def graphs(packet,data,old):
    count=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=old.expected_bars(data,stem);svg=old.svg_rects((packet/(stem+'.svg')).read_bytes());n=old.svg_costs(svg,bars);pdf,h=old.pdf_rects(packet/(stem+'.pdf'));need(old.pdf_costs(pdf,h,svg,bars,stem=='whole_topics')==n,'actual SVG/PDF rectangle costs');count+=n
    need(count==172,'all172 actual rectangles');return count
def csv_check(packet,data):
    def strings(d):return {k:'' if v is None else str(v) for k,v in d.items()}
    topics=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()));need(len(topics)==18 and len(apps)==41,'all59 CSV rows')
    for row,t in zip(topics,data['topics']):
        expected=dict(topic=t['topic'],title=t['title'],originals=t['source_count'],representation=t['representation'],sources=t['source_sum'],common=t['common_theory'],applications=t['applications_sum'],written=t['written_denominator'],written_factor=t['written']['decimal'],printed_programs=t['printed_program_cost'],mandatory_data=t.get('mandatory_data_cost'),printed_factor=None if t['including_printed_programs'] is None else t['including_printed_programs']['decimal'],raw_programs=t['raw_program_alternative'],raw_factor=None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal'],numerical_status=t.get('numerical_status','unchanged_admitted'))
        need(row==strings(expected),'every topic CSV cell')
    for row,(t,p) in zip(apps,[(t,p) for t in data['topics'] for p in t['pairs']]):
        op=t['topic']=='Operations';rep='whole_raw_software_and_external_data' if op else 'whole_printed_programs_and_mandatory_data' if 'mandatory_data_cost' in t else 'whole_printed_programs'
        expected=dict(topic=t['topic'],title=t['title'],source=p['source'],application=p['application'],source_cost=p['source_cost'],application_cost=p['application_cost'],conditional_exact=p['conditional']['exact_fraction'],conditional_factor=p['conditional']['decimal'],full_common_prepaid=t['common_theory'],full_program_or_software_prepaid=t['raw_program_alternative'] if op else t['printed_program_cost'],mandatory_data_prepaid=t.get('mandatory_data_cost'),full_known_upfront=t['conditional_prepaid']['total'],acquisition_representation=rep,source_representation=p['source_representation'])
        need(row==strings(expected),'every conditional CSV cell')

def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');need(sha(a.packet/'manifest.json')==PIN,'frozen author edition')
    for e in load(a.packet/'manifest.json')['exports']:
        f=a.packet/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'exact frozen export')
    nb=bindings(a.packet,a.public_root);d=load(a.packet/'results.json');nf=arithmetic(d,a.public_root);old=prior_checker(a.public_root);ng=graphs(a.packet,d,old);csv_check(a.packet,d)
    pages=PdfReader(a.packet/'summary.pdf').pages;need(len(pages)==6,'six complete reader pages');text='\n'.join(p.extract_text()or''for p in pages);need(all(q['source']in text for t in d['topics']for q in t['pairs']),'all41 reader source labels')
    controls=[]
    for name,edit in [('alter old topic',lambda d:d['topics'][0].update(common_theory=0)),('omit counterproof',lambda d:d['topics'][-1]['application_components']['RA1'].pop('required_counterproof')),('free code acquisition',lambda d:d['topics'][-1]['conditional_prepaid'].update(total=0)),('wrong source pages',lambda d:d['topics'][-1].update(entire_source_pages=18)),('free old common',lambda d:d['topics'][-1].update(old_umbrella_free_premise=True)),('unknown becomes zero',lambda d:d['topics'][-1].update(external_proof_cost=0)),('round factor',lambda d:d['topics'][-1]['written'].update(exact_fraction='1.2')),('pool topics',lambda d:d.update(pooled_factor=1)),('discount overlaps',lambda d:d.update(cross_topic_deduplication=True)),('stale programme37 status',lambda d:d['programme_snapshot'].update(status='CURRENT_PROGRAMME_37_ADMITTED_ORIGINALS_106_ACCESSIBLE')),('drop pending original',lambda d:d['programme_snapshot'].update(accessible_pending_complete_recovery=64)),('infer counts from lengths',lambda d:d.update(programme_counts_not_inferred_from_measurement=False)),('inflate formalization',lambda d:d['topics'][-1].update(full_source_formalized=True))]:
        bad=copy.deepcopy(d);edit(bad)
        try:arithmetic(bad,a.public_root)
        except(ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted corruption '+name)
    bars=old.expected_bars(d,'whole_topics');svg=old.svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(svg);key='bar-RankAugmentation-common-whole_common';x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:old.svg_costs(bad,bars)
    except ValueError:controls.append('distorted new SVG common')
    else:raise ValueError('accepted actual SVG corruption')
    pdf,height=old.pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(pdf);role,x,y,w,h=bad[-4];bad[-4]=(role,x,y,w+1,h)
    try:old.pdf_costs(bad,height,svg,bars,True)
    except ValueError:controls.append('distorted PDF rectangle')
    else:raise ValueError('accepted actual PDF corruption')
    report=dict(status='PASS_DISTINCT_OVERVIEW41',author_manifest_sha256=PIN,input_bindings=nb,topics=18,distinct_originals=41,exact_comparisons=nf,actual_SVG_bars=ng,actual_PDF_bars=ng,CSV_rows=59,reader_pages=6,controls_rejected=controls,author_implementation_imported=False,prior_independent_vector_parser_reused=True,primary_reextraction=False,new_mathematical_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
