#!/usr/bin/env python3
"""Distinct consolidation check; exact prior topics and independently checked new costs."""
from pathlib import Path
import argparse,copy,csv,hashlib,importlib.util,json,math,subprocess
from pypdf import PdfReader
PIN='ea43de7db427900f65f06f94c73cbf81414b61910e1fdf760242fe56597a3b1d'
OLD_CHECK='eba42a6b2b3621aebe0cc5d9875bae33157b103ca369bf3e3335e2a55bffba5c'
OPERATIONS='c211bfc7a4ae9e0855874aa0584b0f8dfa85c855390e59fa49659b5b517ef978'
REVIEW='d301b71e5743aa9e5d29a048d6553db644295a6fa4081d5686ab0e42a9f578f5'
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
    previous=load(public/'audit/overview/v4/packet/results.json')
    # Exact earlier accepted objects carry all thirteen unaffected mathematical boundaries.
    before={t['topic']:t for t in previous['topics']}
    need([t for t in data['topics'] if t['topic']!='Operations']==[t for t in previous['topics'] if t['topic']!='Diagonal'],'all thirteen complete prior topic records')
    need(data['topic_count']==len(data['topics'])==14 and data['original_manuscript_count']==36,'fourteen topics/36 originals')
    need(data['registry_manuscripts']==161 and data['pooled_factor'] is None and data['cross_topic_deduplication'] is False and not data['all_registry_manuscripts_completed'],'no pooled/corpus completion claim')
    need(not any(k in data for k in ['accessible_originals','currently_admitted_originals','accessible_pending_complete_recovery','pending_source_retrieval','unmeasured']),'counts do not infer recovery/accessibility')
    need(data['pending_numerical_acceptance']==[] and data['pending_overview_review'] and data['currently_published_measured_originals']==35 and data['proposed_measured_originals']==36 and data['recovery_status_not_derived_from_measurement'],'preserved author submission scope')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no credit from consolidation')
    base=public/'audit/topic-operations/v1/measurement'
    review=load(base/'independent_review/review.json');need(review['status']=='ROOT_ACCEPTED_COMPLETE_OPERATIONS_NUMBERS' and review['author_manifest_sha256']==OPERATIONS and sha(base/'independent_review/manifest.json')==REVIEW,'distinct Operations numerical acceptance')
    p=load(base/'packet/results.json')['primary'];g=next(t for t in data['topics'] if t['topic']=='Operations')
    need(g['source_count']==3 and g['source_ids']==['N005','N006','N007'],'three complete originals')
    need(g['common_components']=={'whole_current_common':p['common_theory']} and g['application_components']=={'OP1':{'N005_complete':p['application_costs']['N005']},'DG2':{k:p['document_costs'][k] for k in ['A2','A2nine','A2HN']},'DG1':{'N007_complete':p['application_costs']['N007']}},'complete common and all companion segments')
    need((g['common_theory'],g['source_sum'],g['applications_sum'],g['written_denominator'],g['raw_program_alternative'])==tuple(p[k] for k in ['common_theory','source_sum','all_applications','written_denominator','whole_software_cost']),'all complete new amounts')
    need(g['printed_program_cost'] is None and g['no_complete_printed_route'] and g['including_printed_programs'] is None and g['including_optional_validation'] is None,'no invented printed/optional factor')
    need(g['raw_program_components']==dict(twenty_three_full_files=p['whole_program_cost'],both_required_decoders=p['required_decoder_cost']) and g['separate_raw_inventory']==p['raw_file_costs'] and g['partial_printed_alternatives']==p['partial_printed_costs'],'all complete files and only partial alternatives')
    need(g['conditional_prepaid']==dict(full_common=p['common_theory'],full_declared_raw_software=p['whole_software_cost'],total=p['common_theory']+p['whole_software_cost'],required_external_data_already_acquired=True,external_bytes_separate=True),'full acquisition paid')
    need(g['representation']=='calibrated_selected_pdf' and g['normalization']=='NFC' and g['unit']=='characters_without_whitespace' and g['graphic_proxy_sensitivities_required'],'preserved measurement unit/proxy limits')
    need(g['external_bytes']==dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249),'separate full data costs')
    for row,sid,aid in zip(g['pairs'],['N005','N006','N007'],['OP1','DG2','DG1']):
        need(tuple(row[k] for k in ['source','application','source_cost','application_cost'])==(sid,aid,p['original_costs'][sid],p['application_costs'][sid]),'complete source/application pair')
    count=0;ids=[]
    for t in data['topics']:
        need(t['common_theory']==sum(t['common_components'].values()) and t['source_sum']==sum(q['source_cost'] for q in t['pairs']) and t['applications_sum']==sum(q['application_cost'] for q in t['pairs']) and t['written_denominator']==t['common_theory']+t['applications_sum'],'all topic sums')
        for name,cost in [('written',0),('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:
            if cost is None:need(t[name] is None,'absent alternative stays null');continue
            need(t[name]==ratio(t['source_sum'],t['written_denominator']+cost),'whole exact fraction');count+=1
        if t.get('including_optional_validation') is not None:
            q=t['including_optional_validation'];need(q==ratio(q['numerator'],q['denominator']),'preserved optional fraction');count+=1
        for q in t['pairs']:need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'exact conditional fraction');count+=1;ids.append(q['source'])
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknown costs remain null')
    need(len(ids)==len(set(ids))==36 and set(ids)=={q['source'] for t in previous['topics'] for q in t['pairs']}|{'N005'} and count==77,'all36 originals/77 fractions')
    return count
def graphs(packet,data,old):
    total=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=old.expected_bars(data,stem);svg=old.svg_rects((packet/(stem+'.svg')).read_bytes());n=old.svg_costs(svg,bars);rects,h=old.pdf_rects(packet/(stem+'.pdf'));need(old.pdf_costs(rects,h,svg,bars,stem=='whole_topics')==n,'actual PDF bars');total+=n
    need(total==142,'all142 actual bars');return total
def csv_check(packet,data):
    topics=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()));need(len(topics)==14 and len(apps)==36,'50 CSV rows')
    def strs(d):return {k:''if v is None else str(v)for k,v in d.items()}
    for row,t in zip(topics,data['topics']):
        expected=dict(topic=t['topic'],title=t['title'],originals=t['source_count'],representation=t['representation'],sources=t['source_sum'],common=t['common_theory'],applications=t['applications_sum'],written=t['written_denominator'],written_factor=t['written']['decimal'],printed_programs=t['printed_program_cost'],printed_factor=None if t['including_printed_programs']is None else t['including_printed_programs']['decimal'],raw_programs=t['raw_program_alternative'],raw_factor=None if t['including_raw_programs']is None else t['including_raw_programs']['decimal'],numerical_status=t.get('numerical_status','unchanged_admitted'))
        need(row==strs(expected),'every topic CSV cell')
    for row,(t,p)in zip(apps,[(t,p)for t in data['topics']for p in t['pairs']]):
        diag=t['topic']=='Operations';expected=dict(topic=t['topic'],title=t['title'],source=p['source'],application=p['application'],source_cost=p['source_cost'],application_cost=p['application_cost'],conditional_exact=p['conditional']['exact_fraction'],conditional_factor=p['conditional']['decimal'],full_common_prepaid=t['common_theory'],full_program_or_software_prepaid=t['raw_program_alternative']if diag else t['printed_program_cost'],acquisition_representation='whole_raw_software_and_external_data'if diag else 'whole_printed_programs',source_representation=p['source_representation'])
        need(row==strs(expected),'every application CSV cell')
def bindings(packet,public):
    protocol=load(packet/'protocol.json');paths={
      'previous_results':'audit/overview/v4/packet/results.json','previous_manifest':'audit/overview/v4/packet/manifest.json',
      'previous_admission':'audit/overview/v4/admission.json','previous_review':'audit/overview/v4/independent_review/review.json',
      'Operations_results':'audit/topic-operations/v1/measurement/packet/results.json','Operations_manifest':'audit/topic-operations/v1/measurement/packet/manifest.json',
      'Operations_protocol':'audit/topic-operations/v1/measurement/packet/protocol.json','Operations_input_review':'audit/topic-operations/v1/measurement/input_review/review.json',
      'Operations_review':'audit/topic-operations/v1/measurement/independent_review/review.json','Operations_review_manifest':'audit/topic-operations/v1/measurement/independent_review/manifest.json'}
    need(set(protocol['bindings'])==set(paths),'all ten numerical inputs')
    for key,row in protocol['bindings'].items():
        raw=(packet/row['local']).read_bytes();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'exact bound input')
        need(raw==(public/paths[key]).read_bytes(),'exact admitted public input '+key)
    need(protocol['bindings']['Operations_manifest']['sha256']==OPERATIONS and protocol['bindings']['Operations_review_manifest']['sha256']==REVIEW,'exact accepted Operations editions')
    return len(paths)
def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'exact author freeze')
    for r in load(a.packet/'manifest.json')['exports']:
        f=a.packet/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'exact export '+r['path'])
    nb=bindings(a.packet,a.public_root);old=prior_checker(a.public_root);data=load(a.packet/'results.json');nf=arithmetic(data,a.public_root,old);ng=graphs(a.packet,data,old);csv_check(a.packet,data)
    reader=PdfReader(a.packet/'summary.pdf');need(len(reader.pages)==6,'six complete reader pages');text='\n'.join(p.extract_text()or''for p in reader.pages)
    need(all(q['source']in text for t in data['topics']for q in t['pairs']),'all36 original labels visible')
    controls=[]
    op=next(i for i,t in enumerate(data['topics']) if t['topic']=='Operations')
    for label,mut in [('alter prior topic',lambda d:d['topics'][0].update(common_theory=0)),('omit whole common',lambda d:d['topics'][op]['common_components'].clear()),('omit companion',lambda d:d['topics'][op]['application_components']['DG2'].pop('A2HN')),('partial program acquisition',lambda d:d['topics'][op]['conditional_prepaid'].update(full_declared_raw_software=0)),('omit source',lambda d:d['topics'][op].update(source_ids=[])),('corrupt combined ratio',lambda d:d['topics'][op]['written'].update(denominator=1)),('corrupt conditional ratio',lambda d:d['topics'][op]['pairs'][0]['conditional'].update(numerator=1)),('unknown cost zero',lambda d:d['topics'][op].update(external_proof_cost=0)),('pool topics',lambda d:d.update(pooled_factor=2)),('cross-topic discount',lambda d:d.update(cross_topic_deduplication=True)),('infer recovery count',lambda d:d.update(currently_admitted_originals=36))]:
        bad=copy.deepcopy(data);mut(bad)
        try:arithmetic(bad,a.public_root,old)
        except (ValueError,KeyError):controls.append(label)
        else:raise ValueError('accepted negative control '+label)
    bars=old.expected_bars(data,'whole_topics');svg=old.svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(svg);key=next(k for k in bad if k=='bar-Operations-common-whole_current_common');x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:old.svg_costs(bad,bars)
    except ValueError:controls.append('distorted new SVG common')
    else:raise ValueError('accepted SVG distortion')
    rects,H=old.pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(rects);role,x,y,w,h=bad[-4];bad[-4]=(role,x,y,w+1,h)
    try:old.pdf_costs(bad,H,svg,bars,True)
    except ValueError:controls.append('distorted new PDF application')
    else:raise ValueError('accepted PDF distortion')
    report=dict(status='PASS_DISTINCT_OVERVIEW36',author_manifest_sha256=PIN,input_bindings=nb,topics=14,distinct_originals=36,exact_comparisons=nf,actual_SVG_bars=ng,actual_PDF_bars=ng,CSV_rows=50,reader_pages=6,controls_rejected=controls,author_implementation_imported=False,prior_independent_routes_and_vector_checker_reused=True,primary_reextraction=False,new_mathematical_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
