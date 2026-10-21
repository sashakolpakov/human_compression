#!/usr/bin/env python3
"""Distinct consolidation check; exact prior topics and independently checked new costs."""
from pathlib import Path
import argparse,copy,csv,hashlib,importlib.util,json,math,subprocess
from pypdf import PdfReader
PIN='37ba7781a0f9c99e8cd210e3a72215c20d3ef7cd8640302ef7a2244d871a13bd'
OLD_CHECK='eba42a6b2b3621aebe0cc5d9875bae33157b103ca369bf3e3335e2a55bffba5c'
GLUING='d52e82dc1b613ae9cb9f43937bc514f7818b3da92a58c3ffd87eccfbb611bc80'
REVIEW='8239745069c688b960566bbf091e1d7bfce20cb32a92c19b68731340a443387c'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prior_checker(public):
    path=public/'audit/overview/v3/independent_review/check.py';need(sha(path)==OLD_CHECK,'exact prior independent implementation')
    spec=importlib.util.spec_from_file_location('overview34_distinct_reused',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def ratio(n,d):
    g=math.gcd(n,d);q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,exact_fraction=str(n//g)if d==g else f'{n//g}/{d//g}',decimal=f'{q//10**12}.{q%10**12:012d}')
def arithmetic(data,public,old):
    previous=load(public/'audit/overview/v3/packet/results.json')
    count=old.arithmetic(previous,old.expected(public))
    need(data['topics'][:-1]==previous['topics'],'all thirteen prior complete topic records preserved')
    need(data['topic_count']==len(data['topics'])==14 and data['original_manuscript_count']==35,'fourteen topics and35 originals')
    need(not any(k in data for k in ['accessible_originals','currently_admitted_originals','accessible_pending_complete_recovery','pending_source_retrieval','unmeasured']),'no inference of accessibility or recovery from measurements')
    need(data['registry_manuscripts']==161 and data['pooled_factor']is None and data['cross_topic_deduplication']is False and data['all_registry_manuscripts_completed']is False,'fixed intake and no pooled or completion claim')
    need(data['pending_numerical_acceptance']==[] and data['pending_overview_review']is True and data['currently_published_measured_originals']==34 and data['proposed_measured_originals']==35 and data['recovery_status_not_derived_from_measurement']is True,'immutable author stage')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new mathematical credit')
    base=public/'audit/gluing-measurement/v1';a=load(base/'admission.json');review=load(base/'independent_review/review.json')
    need(a['status']=='ROOT_ADMITTED_COMPLETE_TOPIC_NUMERICAL_COMPARISON' and a['source_ids']==['L010'] and a['author_manifest']['sha256']==GLUING and a['independent_manifest']['sha256']==REVIEW and review['status']=='ROOT_ACCEPTED_GLUING_NUMERICAL_COMPARISON','distinct Gluing acceptance')
    p=load(base/'packet/results.json')['primary'];need(p==a['primary'],'admitted primary costs');c=p['costs'];raw=p['raw_costs'];g=data['topics'][-1]
    need(g['topic']=='Gluing' and g['source_count']==1 and g['source_ids']==['L010'],'one added original')
    need(g['common_components']==dict(U1_common_point=c['U1'],U2_synchronized_trees=c['U2']) and g['application_components']=={'GL1':{'complete_application':c['A1']}},'complete common and application')
    u=c['U1']+c['U2'];app=c['A1'];s=c['L010']
    need((g['common_theory'],g['source_sum'],g['applications_sum'],g['written_denominator'],g['printed_program_cost'],g['raw_program_alternative'])==(u,s,app,u+app,c['CODE'],raw['programs']),'all complete amounts')
    need(g['conditional_prepaid']==dict(full_common=u,full_declared_printed_programs=c['CODE'],total=u+c['CODE']),'whole common and whole program acquisition')
    need(g['representation']=='calibrated_selected_pdf' and g['normalization']=='NFC' and g['unit']=='characters_without_whitespace','exact Gluing coordinate')
    need([g[k]for k in ['entire_source_pages','entire_common_pages','entire_application_pages','entire_program_pages']]==[15,[5,6],5,4] and g['separate_raw_inventory']==raw,'complete documents and raw inventory')
    for name,den in [('written',u+app),('including_printed_programs',u+app+c['CODE']),('including_raw_programs',u+app+raw['programs'])]:need(g[name]==ratio(s,den),'exact new combined fraction');count+=1
    need(g['including_optional_validation']is None,'no invented optional cost')
    need(len(g['pairs'])==1,'one whole application');q=g['pairs'][0]
    need(tuple(q[k]for k in ['source','application','source_cost','application_cost'])==('L010','GL1',s,app) and q['conditional']==ratio(s,app) and q['source_representation']=='complete_PDF_calibrated_selected','exact conditional application');count+=1
    need(all(g[k]is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknown costs null')
    ids=[q['source']for t in data['topics']for q in t['pairs']]
    need(len(ids)==len(set(ids))==35 and count==76,'all35 originals and76 fractions')
    return count
def graphs(packet,data,old):
    total=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=old.expected_bars(data,stem);svg=old.svg_rects((packet/(stem+'.svg')).read_bytes());n=old.svg_costs(svg,bars);rects,h=old.pdf_rects(packet/(stem+'.pdf'));need(old.pdf_costs(rects,h,svg,bars,stem=='whole_topics')==n,'actual PDF bars');total+=n
    need(total==139,'all139 actual bars');return total
def csv_check(packet,data):
    topics=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()));need(len(topics)==14 and len(apps)==35,'49 CSV rows')
    def strs(d):return {k:''if v is None else str(v)for k,v in d.items()}
    for row,t in zip(topics,data['topics']):
        expected=dict(topic=t['topic'],title=t['title'],originals=t['source_count'],representation=t['representation'],sources=t['source_sum'],common=t['common_theory'],applications=t['applications_sum'],written=t['written_denominator'],written_factor=t['written']['decimal'],printed_programs=t['printed_program_cost'],printed_factor=None if t['including_printed_programs']is None else t['including_printed_programs']['decimal'],raw_programs=t['raw_program_alternative'],raw_factor=None if t['including_raw_programs']is None else t['including_raw_programs']['decimal'],numerical_status=t.get('numerical_status','unchanged_admitted'))
        need(row==strs(expected),'every topic CSV cell')
    for row,(t,p)in zip(apps,[(t,p)for t in data['topics']for p in t['pairs']]):
        diag=t['topic']=='Diagonal';expected=dict(topic=t['topic'],title=t['title'],source=p['source'],application=p['application'],source_cost=p['source_cost'],application_cost=p['application_cost'],conditional_exact=p['conditional']['exact_fraction'],conditional_factor=p['conditional']['decimal'],full_common_prepaid=t['common_theory'],full_program_or_software_prepaid=t['raw_program_alternative']if diag else t['printed_program_cost'],acquisition_representation='whole_raw_software_and_external_data'if diag else 'whole_printed_programs',source_representation=p['source_representation'])
        need(row==strs(expected),'every application CSV cell')
def bindings(packet,public):
    protocol=load(packet/'protocol.json')
    for key,b in protocol['bindings'].items():
        raw=(packet/b['local']).read_bytes();need(len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'],'exact copied input '+key)
        if b['commit']is not None:other=subprocess.check_output(['git','show',b['commit']+':'+b['path']],cwd=public)
        else:other=(public/b['public_path']).read_bytes()
        need(raw==other,'published exact input '+key)
    need(protocol['bindings']['Gluing_manifest']['sha256']==GLUING and protocol['bindings']['Gluing_root_manifest']['sha256']==REVIEW,'accepted numerical editions')
    return len(protocol['bindings'])
def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'exact author freeze')
    for r in load(a.packet/'manifest.json')['exports']:
        f=a.packet/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'exact export '+r['path'])
    nb=bindings(a.packet,a.public_root);old=prior_checker(a.public_root);data=load(a.packet/'results.json');nf=arithmetic(data,a.public_root,old);ng=graphs(a.packet,data,old);csv_check(a.packet,data)
    reader=PdfReader(a.packet/'summary.pdf');need(len(reader.pages)==6,'six complete reader pages');text='\n'.join(p.extract_text()or''for p in reader.pages)
    need(all(q['source']in text for t in data['topics']for q in t['pairs']),'all35 original labels visible')
    controls=[]
    for label,mut in [('alter prior topic',lambda d:d['topics'][0].update(common_theory=0)),('omit second common',lambda d:d['topics'][-1]['common_components'].pop('U2_synchronized_trees')),('partial program acquisition',lambda d:d['topics'][-1]['conditional_prepaid'].update(full_declared_printed_programs=0)),('omit source',lambda d:d['topics'][-1].update(source_ids=[])),('corrupt combined ratio',lambda d:d['topics'][-1]['written'].update(denominator=1)),('corrupt conditional ratio',lambda d:d['topics'][-1]['pairs'][0]['conditional'].update(numerator=1)),('unknown cost zero',lambda d:d['topics'][-1].update(external_proof_cost=0)),('pool topics',lambda d:d.update(pooled_factor=2)),('cross-topic discount',lambda d:d.update(cross_topic_deduplication=True)),('infer recovery count',lambda d:d.update(currently_admitted_originals=35))]:
        bad=copy.deepcopy(data);mut(bad)
        try:arithmetic(bad,a.public_root,old)
        except (ValueError,KeyError):controls.append(label)
        else:raise ValueError('accepted negative control '+label)
    bars=old.expected_bars(data,'whole_topics');svg=old.svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(svg);key=next(k for k in bad if k=='bar-Gluing-common-U2_synchronized_trees');x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:old.svg_costs(bad,bars)
    except ValueError:controls.append('distorted new SVG common')
    else:raise ValueError('accepted SVG distortion')
    rects,H=old.pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(rects);role,x,y,w,h=bad[-4];bad[-4]=(role,x,y,w+1,h)
    try:old.pdf_costs(bad,H,svg,bars,True)
    except ValueError:controls.append('distorted new PDF application')
    else:raise ValueError('accepted PDF distortion')
    report=dict(status='PASS_DISTINCT_OVERVIEW35',author_manifest_sha256=PIN,input_bindings=nb,topics=14,distinct_originals=35,exact_comparisons=nf,actual_SVG_bars=ng,actual_PDF_bars=ng,CSV_rows=49,reader_pages=6,controls_rejected=controls,author_implementation_imported=False,prior_independent_routes_and_vector_checker_reused=True,primary_reextraction=False,new_mathematical_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
