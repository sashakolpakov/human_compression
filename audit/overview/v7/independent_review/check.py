#!/usr/bin/env python3
"""Distinct whole-corpus arithmetic and vectors; no overview-author imports."""
from pathlib import Path
import argparse,copy,csv,hashlib,importlib.util,json,math
from pypdf import PdfReader
PIN='66edf6c8ad5d0b1ce23bc152546beaac6c98c523097fcc12ded1d4543d806cfd'
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
    s=importlib.util.spec_from_file_location('root_overview40_vectors',p);q=importlib.util.module_from_spec(s);s.loader.exec_module(q);return q
def bindings(packet,public):
    routes={f'previous_{k}':f'audit/overview/v6/{v}' for k,v in [('results','packet/results.json'),('manifest','packet/manifest.json'),('admission','admission.json'),('review','independent_review/review.json')]}
    for key,slug in [('LocallyProjective','locally-projective'),('MathieuCensus','mathieu')]:
        for suffix in ['results','manifest','protocol','review','review_manifest']:
            path='packet/'+suffix+'.json' if suffix in ['results','manifest','protocol'] else 'independent_review/'+('manifest' if suffix=='review_manifest' else 'review')+'.json'
            routes[key+'_'+suffix]='audit/topic-'+slug+'/v1/measurement/'+path
    protocol=load(packet/'protocol.json');need(set(protocol['bindings'])==set(routes),'all14 numerical inputs')
    for name,path in routes.items():
        r=protocol['bindings'][name];f=packet/r['local'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'] and f.read_bytes()==(public/path).read_bytes(),'exact accepted input '+name)
    return len(routes)
def arithmetic(d,public):
    old=load(public/'audit/overview/v6/packet/results.json')
    need(d['topics'][:-2]==old['topics'],'fifteen whole previous records unchanged')
    need(d['topic_count']==len(d['topics'])==17 and d['original_manuscript_count']==40 and d['registry_manuscripts']==161,'fixed161/17topics40originals')
    need(d['pooled_factor'] is None and not d['cross_topic_deduplication'] and not d['all_registry_manuscripts_completed'],'no pooled, free-theory or completion claim')
    need(d['currently_published_measured_originals']==37 and d['proposed_measured_originals']==40 and d['pending_numerical_acceptance']==[] and d['pending_overview_review'],'preserved author stage')
    need(all(d[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'overview earns no mathematical credit')
    lp,mc=d['topics'][-2:]
    wanted=[(lp,'LocallyProjective','locally-projective','0d548c296855637641592e539c4401895ac38c4c094eaf6f6aa8923f57e058a4','2f9ded604bd5ca6b4b9b882c5b694124eacb653102b9f44e823f04ac731c519a','ROOT_ACCEPTED_COMPLETE_LOCALLY_PROJECTIVE_NUMBERS'),(mc,'MathieuCensus','mathieu','1f7256e911cc3bf0797672e4237a7ef8fe6e6b24cbcca30d13142c82c7dc2d36','b163f3c5bf37ef0406016be81e036c1b7f52a7d5be3245d43f2586081ca88307','ROOT_ACCEPTED_COMPLETE_L073_NUMBERS')]
    for t,key,slug,author,review,status in wanted:
        base=public/'audit'/('topic-'+slug)/'v1/measurement';p=load(base/'packet/results.json')['primary'];r=load(base/'independent_review/review.json')
        need(t['topic']==key and sha(base/'packet/manifest.json')==author and sha(base/'independent_review/manifest.json')==review and r['author_manifest_sha256']==author and r['status']==status,'independent acceptance of exact numerical editions')
        if key=='LocallyProjective':
            c=p['document_costs'];u=c['U']+c['TABLES'];app=c['A1']+c['A2'];raw=p['raw_program_cost'];data=p['mandatory_data_cost'];source=c['L084']+c['L095']
            need(t['common_components']==dict(whole_common_proof=c['U'],whole_common_tables=c['TABLES']) and t['application_components']=={'LP1':{'complete_erratum_application':c['A1']},'LP2':{'complete_parent_application':c['A2']}},'all LP common and application papers')
            pairs=[dict(source=s,application=a,source_cost=c[s],application_cost=c[k],source_representation='complete_PDF_calibrated_selected',conditional=ratio(c[s],c[k])) for s,a,k in [('L084','LP1','A1'),('L095','LP2','A2')]]
            need((t['entire_source_pages'],t['entire_common_pages'],t['entire_application_pages'],t['entire_program_pages'])==({'L084':2,'L095':15},[7,5],{'LP1':2,'LP2':3},6),'complete LP pages')
            need(t['separate_raw_inventory']==dict(programs=raw,mandatory_data=data,drivers=p['operational_driver_cost_separate'],formal=0,generated_output_literal_bytes=3470182),'LP separate whole inventories')
            need(t['mandatory_data_literal_bytes']==39150 and t['mandatory_data_files']==1 and t['representation']=='calibrated_selected_pdf' and 'Unseen journal text' in t['scientific_boundary'],'LP editions and required data')
        else:
            c=p['costs'];u=c['U'];app=sum(c[k] for k in ['A1','CLASSES','ROWS']);raw=p['raw_costs']['programs'];data=p['raw_costs']['required_raw_data'];source=c['L073']
            need(t['common_components']==dict(whole_common=u) and t['application_components']=={'MC1':dict(main_application=c['A1'],all_class_tables=c['CLASSES'],all_source_row_dispositions=c['ROWS'])},'all Mathieu companion papers')
            pairs=[dict(source='L073',application='MC1',source_cost=source,application_cost=app,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(source,app))]
            need((t['entire_source_pages'],t['entire_common_pages'],t['entire_application_pages'],t['entire_program_pages'])==(9,[2],dict(main=5,classes=10,source_rows=9),11),'complete Mathieu pages')
            need(t['separate_raw_inventory']==dict(programs=raw,mandatory_data=data,drivers=p['raw_costs']['drivers'],generated_outputs=p['raw_costs']['generated_outputs'],generated_output_literal_bytes=1567120,formal=0),'Mathieu separate whole inventories')
            need(t['mandatory_data_literal_bytes']==83965 and t['mandatory_data_files']==2 and t['representation']=='raw_untrimmed_pdf' and 'not unavailable historical geo[] identities' in t['scientific_boundary'] and 'not another recovered original' in t['scientific_boundary'],'Mathieu exact corrected scope')
        need(t['pairs']==pairs and (t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['printed_program_cost'],t['raw_program_alternative'],t['mandatory_data_cost'])==(source,u,app,u+app,c['CODE'],raw,data),'complete new cost boundary')
        need(t['conditional_prepaid']==dict(full_common=u,full_declared_printed_programs=c['CODE'],mandatory_data=data,total=u+c['CODE']+data) and t['conditional_raw_alternative_prepaid']==dict(full_common=u,full_declared_raw_programs=raw,mandatory_data=data,total=u+raw+data),'full alternative acquisition')
        need(t['mandatory_data_paid_in_both_program_routes'] and not t['old_umbrella_free_premise'] and t['normalization']=='NFC' and t['unit']=='characters_without_whitespace','fixed accounting conventions')
    ids=[];count=0
    for t in d['topics']:
        need(t['source_ids']==[q['source'] for q in t['pairs']] and t['source_count']==len(t['pairs']),'original roster')
        need(t['common_theory']==sum(t['common_components'].values()) and t['source_sum']==sum(q['source_cost'] for q in t['pairs']) and t['applications_sum']==sum(q['application_cost'] for q in t['pairs']) and t['written_denominator']==t['common_theory']+t['applications_sum'],'complete topic sums')
        # A missing field in an unchanged older record is not an assertion of zero external data cost.
        data=t.get('mandatory_data_cost',0)
        for k,cost in [('written',0),('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:
            denominator=t['written_denominator']+(0 if k=='written' else data)+(cost or 0)
            need(t[k]==(None if cost is None else ratio(t['source_sum'],denominator)),'all exact whole-topic factors');count+=cost is not None
        if t.get('including_optional_validation') is not None:
            f=t['including_optional_validation'];need(f==ratio(f['numerator'],f['denominator']),'optional exact fraction');count+=1
        for q in t['pairs']:
            need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'exact conditional');ids.append(q['source']);count+=1
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknowns remain unknown')
    need(len(ids)==len(set(ids))==40 and set(ids)=={q['source'] for t in old['topics'] for q in t['pairs']}|{'L073','L084','L095'} and count==90,'exact40originals90fractions')
    return count
def graphs(packet,data,old):
    count=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=old.expected_bars(data,stem);svg=old.svg_rects((packet/(stem+'.svg')).read_bytes());n=old.svg_costs(svg,bars);pdf,h=old.pdf_rects(packet/(stem+'.pdf'));need(old.pdf_costs(pdf,h,svg,bars,stem=='whole_topics')==n,'actual SVG/PDF rectangle costs');count+=n
    need(count==165,'all165 actual rectangles');return count
def csv_check(packet,data):
    def strings(d):return {k:'' if v is None else str(v) for k,v in d.items()}
    topics=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()));need(len(topics)==17 and len(apps)==40,'all57 CSV rows')
    for row,t in zip(topics,data['topics']):
        expected=dict(topic=t['topic'],title=t['title'],originals=t['source_count'],representation=t['representation'],sources=t['source_sum'],common=t['common_theory'],applications=t['applications_sum'],written=t['written_denominator'],written_factor=t['written']['decimal'],printed_programs=t['printed_program_cost'],mandatory_data=t.get('mandatory_data_cost'),printed_factor=None if t['including_printed_programs'] is None else t['including_printed_programs']['decimal'],raw_programs=t['raw_program_alternative'],raw_factor=None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal'],numerical_status=t.get('numerical_status','unchanged_admitted'))
        need(row==strings(expected),'every topic CSV cell')
    for row,(t,p) in zip(apps,[(t,p) for t in data['topics'] for p in t['pairs']]):
        op=t['topic']=='Operations';rep='whole_raw_software_and_external_data' if op else 'whole_printed_programs_and_mandatory_data' if 'mandatory_data_cost' in t else 'whole_printed_programs'
        expected=dict(topic=t['topic'],title=t['title'],source=p['source'],application=p['application'],source_cost=p['source_cost'],application_cost=p['application_cost'],conditional_exact=p['conditional']['exact_fraction'],conditional_factor=p['conditional']['decimal'],full_common_prepaid=t['common_theory'],full_program_or_software_prepaid=t['raw_program_alternative'] if op else t['printed_program_cost'],mandatory_data_prepaid=t.get('mandatory_data_cost'),full_known_upfront=t['conditional_prepaid']['total'],acquisition_representation=rep,source_representation=p['source_representation'])
        need(row==strings(expected),'every conditional CSV cell')
def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'frozen overview author edition')
    for e in load(a.packet/'manifest.json')['exports']:
        f=a.packet/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'complete frozen export')
    nb=bindings(a.packet,a.public_root);d=load(a.packet/'results.json');nf=arithmetic(d,a.public_root);old=prior_checker(a.public_root);ng=graphs(a.packet,d,old);csv_check(a.packet,d)
    pages=PdfReader(a.packet/'summary.pdf').pages;need(len(pages)==6,'six complete reader pages');text='\n'.join(p.extract_text() or '' for p in pages);need(all(q['source'] in text for t in d['topics'] for q in t['pairs']),'all forty source labels')
    controls=[]
    mutations=[('alter older topic',lambda d:d['topics'][0].update(common_theory=0)),('drop common tables',lambda d:d['topics'][-2]['common_components'].pop('whole_common_tables')),('drop source row companion',lambda d:d['topics'][-1]['application_components']['MC1'].pop('all_source_row_dispositions')),('free required data',lambda d:d['topics'][-1].update(mandatory_data_cost=0)),('hide data as printed code',lambda d:d['topics'][-2].update(printed_program_cost=51269)),('incomplete prepayment',lambda d:d['topics'][-1]['conditional_prepaid'].update(total=36760)),('include unseen journal',lambda d:d['topics'][-2]['entire_source_pages'].update(L095=12)),('invent geo identities',lambda d:d['topics'][-1].update(scientific_boundary='complete original labels')),('old theory free',lambda d:d['topics'][-1].update(old_umbrella_free_premise=True)),('unknown cost zero',lambda d:d['topics'][-1].update(external_proof_cost=0)),('round fraction',lambda d:d['topics'][-1]['written'].update(exact_fraction='0.332')),('pooled factor',lambda d:d.update(pooled_factor=1)),('cross-topic discount',lambda d:d.update(cross_topic_deduplication=True))]
    for name,edit in mutations:
        bad=copy.deepcopy(d);edit(bad)
        try:arithmetic(bad,a.public_root)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted corruption '+name)
    bars=old.expected_bars(d,'whole_topics');svg=old.svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(svg);key='bar-MathieuCensus-common-whole_common';x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:old.svg_costs(bad,bars)
    except ValueError:controls.append('distorted new SVG common')
    else:raise ValueError('accepted actual SVG corruption')
    pdf,height=old.pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(pdf);role,x,y,w,h=bad[-4];bad[-4]=(role,x,y,w+1,h)
    try:old.pdf_costs(bad,height,svg,bars,True)
    except ValueError:controls.append('distorted new PDF rectangle')
    else:raise ValueError('accepted actual PDF corruption')
    report=dict(status='PASS_DISTINCT_OVERVIEW40',author_manifest_sha256=PIN,input_bindings=nb,topics=17,distinct_originals=40,exact_comparisons=nf,actual_SVG_bars=ng,actual_PDF_bars=ng,CSV_rows=57,reader_pages=6,controls_rejected=controls,author_implementation_imported=False,prior_independent_vector_parser_reused=True,primary_reextraction=False,new_mathematical_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
